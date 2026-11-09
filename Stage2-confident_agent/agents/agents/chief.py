"""Chief Agent: coordinates the pipeline and decides what reaches the student.

Decision policy (fixed in config.py before evaluation):
    ACCEPT        - confident enough, show the candidate
    REGENERATE    - not confident: ask the Generator once more, grounded on reference notes
                    and the Verifier's objections, then re-check
    FLAG          - still not confident: withhold the content and show a low-confidence notice

The Chief Agent only sees (prompt, candidate answer). It never sees benchmark ground truth,
category or scoring metadata.
"""
import re
from collections import Counter
from dataclasses import dataclass, field

import config
import lookup
from agents import ConfidenceEstimator
from parsing import (is_materials_request, looks_like_error, parse_choice, quiz_kind)


@dataclass
class Decision:
    status: str
    final_response: str
    withheld_response: str = ""
    confidence: float = 0.0
    regenerated: bool = False
    kind: str = ""
    topics: list = field(default_factory=list)
    trace: dict = field(default_factory=dict)


class ChiefAgent:
    def __init__(self, generator, verifier, suggester, notes, estimator=None,
                 materials_mode="open", n_samples=config.N_SAMPLES):
        self.gen, self.ver, self.sug, self.notes = generator, verifier, suggester, notes
        self.est = estimator or ConfidenceEstimator()
        self.materials_mode = materials_mode
        self.n_samples = n_samples

    # ------------------------------------------------------------ entry point
    def handle(self, prompt, candidate=None):
        if candidate is None:
            candidate = self.gen.generate(prompt)
        qk = quiz_kind(prompt)
        # for multiple choice, search notes using the question stem only: the options
        # (distractors) would otherwise pull in notes about the wrong patterns
        stem = re.sub(r"(?m)^\s*[A-D][\.\)]\s.*$", "", prompt) if qk == "mcq" else prompt
        notes, topics = self.notes.lookup(stem)
        trace = {"topics": topics}
        if qk:
            d = self._quiz(prompt, candidate, qk, notes, trace)
        else:
            d = None
            if is_materials_request(prompt):
                d = self._materials(prompt, candidate, trace)
            if d is None:
                d = self._text(prompt, candidate, notes, trace)
        d.topics = topics
        return d

    def _flag(self, candidate, conf, regenerated, kind, trace):
        return Decision("FLAGGED", config.FLAG_MESSAGE, withheld_response=candidate,
                        confidence=conf, regenerated=regenerated, kind=kind, trace=trace)

    # ------------------------------------------------------------ quiz questions
    def _quiz(self, prompt, candidate, kind, notes, trace):
        cand = parse_choice(candidate, kind)
        votes = [cand] if cand else []
        v = self.ver.solve_quiz(prompt, kind, notes)
        if v:
            votes.append(v)
        for i in range(config.N_QUIZ_SAMPLES):
            a = self.gen.answer_only(prompt, kind, seed=i + 1)
            if a:
                votes.append(a)
        conf = self.est.quiz_confidence(cand, votes)
        trace.update({"candidate_answer": cand, "verifier_answer": v, "votes": votes})
        if conf >= config.QUIZ_ACCEPT:
            return Decision("ACCEPTED", candidate, confidence=conf, kind="quiz", trace=trace)

        arbiter = v or (Counter(x for x in votes if x != cand).most_common(1) or [(None, 0)])[0][0]
        feedback = (f"Your answer ({cand or 'unclear'}) disagrees with an independent check, "
                    f"which concluded {arbiter}. Re-read the question and every option carefully.")
        regen = self.gen.regenerate(prompt, feedback, notes)
        new = parse_choice(regen, kind)
        trace.update({"regenerated_answer": new, "arbiter": arbiter})
        if new and arbiter and new == arbiter:
            conf2 = self.est.quiz_confidence(new, votes + [new])
            return Decision("ACCEPTED_AFTER_REGEN", regen, withheld_response=candidate,
                            confidence=conf2, regenerated=True, kind="quiz", trace=trace)
        return self._flag(candidate, conf, True, "quiz", trace)

    # ------------------------------------------------------------ learning materials
    def _materials(self, prompt, candidate, trace):
        if self.materials_mode == "pool" and self.sug.is_recommendation_request(prompt):
            entries = self.sug.from_pool(prompt)
            if entries:
                trace["pool_entries"] = [e["title"] for e in entries]
                return Decision("ACCEPTED_POOL", self.sug.format_entries(entries),
                                withheld_response=candidate, confidence=1.0, kind="materials",
                                trace=trace)
        if looks_like_error(candidate):
            return None
        refs = lookup.extract_references(prompt, candidate)
        if not refs:
            return None                      # nothing checkable: use the text pipeline
        checked = self.ver.verify_references(refs, prompt)
        trace["references"] = [{"raw": c["ref"]["raw"][:160], "status": c["result"]["status"],
                                "detail": c["result"]["detail"]} for c in checked]
        verified = [c for c in checked if c["result"]["status"] == "VERIFIED"]
        conf = self.est.reference_confidence(len(verified), len(checked))
        if len(verified) == len(checked):
            return Decision("ACCEPTED", candidate, confidence=conf, kind="materials", trace=trace)
        if verified:
            body = "\n".join(f"- {c['ref']['raw']}" for c in verified)
            final = ("Verified resources:\n" + body +
                     "\n\n(Other suggestions could not be verified and were removed.)")
            return Decision("ACCEPTED_FILTERED", final, withheld_response=candidate,
                            confidence=conf, kind="materials", trace=trace)
        return self._flag(candidate, conf, False, "materials", trace)

    # ------------------------------------------------------------ free-text content
    def _text(self, prompt, candidate, notes, trace):
        if looks_like_error(candidate):
            return self._flag(candidate, 0.0, False, "text", trace)
        judged = self.ver.check_text(candidate, notes)
        abstained = bool(lookup.CUES.search(candidate))
        support = self.est.support_score(judged, abstained)
        contra = self.est.contradictions(judged)
        
        samples = [
            self.gen.sample(prompt, seed=i + 1)
            for i in range(self.n_samples)
        ]

        agree = []
        consensus_raw = []

        for sample in samples:
            agree.append(self.ver.consensus(candidate, sample))
            consensus_raw.append(
                getattr(self.ver, "last_consensus_raw", "")
            )

        consensus = sum(agree) / len(agree) if agree else 1.0

        trace["consensus_raw"] = consensus_raw
        trace["consensus_votes"] = agree

        conf = self.est.text_confidence(support, consensus, contra)
        trace.update({"claims": judged, "abstained": abstained, "support": round(support, 3),
                      "consensus": round(consensus, 3), "contradictions": contra})
        if conf >= config.TEXT_ACCEPT:
            return Decision("ACCEPTED", candidate, confidence=conf, kind="text", trace=trace)

        problems = [f"- Claim not supported: {j['claim']}" for j in judged
                    if j["verdict"] == "CONTRADICTED"]
        if consensus < 1.0:
            problems.append("- Independent answers to the same question disagreed on key facts, "
                            "so some details may be invented.")
        if not problems:
            problems.append("- Several statements could not be confirmed.")
        regen = self.gen.regenerate(prompt, "\n".join(problems), notes)
        judged2 = self.ver.check_text(regen, notes)
        support2 = self.est.support_score(judged2, bool(lookup.CUES.search(regen)))
        contra2 = self.est.contradictions(judged2)
        conf2 = self.est.regen_confidence(support2, contra2)
        trace.update({"regen_claims": judged2, "regen_support": round(support2, 3),
                      "regen_contradictions": contra2})
        # a regenerated answer with no checkable claims (and no honest abstention) is
        # unverified; it must not pass merely because the neutral score equals REGEN_ACCEPT
        unverified = (not judged2) and not lookup.CUES.search(regen)
        trace["regen_unverified"] = unverified
        if conf2 >= config.REGEN_ACCEPT and contra2 == 0 and not unverified:
            return Decision("ACCEPTED_AFTER_REGEN", regen, withheld_response=candidate,
                            confidence=conf2, regenerated=True, kind="text", trace=trace)
        return self._flag(candidate, conf2, True, "text", trace)
