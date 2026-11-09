"""The specialised agents: Generator, Verifier, Suggestion, Confidence Estimator."""
import json
import re

import config
import lookup
from parsing import parse_answer_only


CODE_BLOCK = re.compile(r"```.*?```", re.S)
CODE_START = re.compile(
    r"^(?:(?:public|private|protected|class|interface|import|package|static|void|return|if|for|while)\b|//|/\*|@)",
    re.I)


def strip_code(text):
    """Remove fenced code (including an unclosed block at a truncated end) and markdown marks."""
    text = CODE_BLOCK.sub(" ", text)
    text = re.sub(r"```.*", " ", text, flags=re.S)
    text = re.sub(r"\*\*|__", "", text)
    return re.sub(r"(?m)^#+\s*", "", text).strip()


def claim_like(line):
    """True for a full prose sentence; False for headings, code and separators."""
    if len(line) < 25 or len(line.split()) < 5:
        return False
    if any(ch in line for ch in "{};"):
        return False
    if CODE_START.match(line) or line.endswith(":"):
        return False
    return sum(c.isalpha() for c in line) / len(line) > 0.6


META = re.compile(
    r"(revised answer|corrected answer|improved answer|adheres? to the guidelines|the reviewer|"
    r"original text|previous answer|my answer|(I've|I have) avoided inventing)", re.I)


def clean_regen(text):
    """Drop short meta-commentary paragraphs the model sometimes adds about its own rewrite."""
    paras = text.split("\n\n")
    kept = [p for p in paras if not (META.search(p) and len(p) < 300 and "```" not in p)]
    return "\n\n".join(kept).strip() or text


# ============================================================ Generator Agent
class GeneratorAgent:
    """Produces candidate content. Uses the SAME model and settings as the baseline."""

    def __init__(self, client):
        self.client = client

    def generate(self, prompt):
        return self.client.chat(prompt, config.SYSTEM_PROMPT, config.GEN_OPTIONS)

    def sample(self, prompt, seed):
        opts = dict(config.SAMPLE_OPTIONS, seed=seed)
        return self.client.chat(prompt, config.SYSTEM_PROMPT, opts)

    def answer_only(self, prompt, kind, seed):
        tail = ("Respond with only the letter of the correct option." if kind == "mcq"
                else "Respond with only True or False.")
        opts = dict(config.ANSWER_ONLY_OPTIONS, seed=seed)
        text = self.client.chat(prompt + "\n\n" + tail, config.SYSTEM_PROMPT, opts)
        return parse_answer_only(text, kind)

    def regenerate(self, prompt, feedback, notes):
        user = (
            f"{prompt}\n\n---\nA reviewer checked your previous answer and found problems:\n"
            f"{feedback}\n\n"
            + (f"Reference notes (trusted):\n{notes}\n\n" if notes else "")
            + "Write an improved answer to the question above, in the same style as a normal answer. "
              "Use only facts you are confident about and rely on the reference notes where they "
              "apply. If the question assumes something you cannot confirm is real, say so instead "
              "of describing it. Do not mention the reviewer, the notes, these instructions, or "
              "that this is a revised answer."
        )
        return clean_regen(self.client.chat(user, config.SYSTEM_PROMPT, config.REGEN_OPTIONS))


# ============================================================ Verifier Agent
class VerifierAgent:
    """Independent checker on a different model family. Never writes content for students."""

    CLAIM_SYS = (
        "You extract factual claims. From the RESPONSE, list at most {n} short, self-contained "
        "factual statements about software concepts, Java classes/methods, names, authors or years. "
        "Each must be a complete sentence. One per line, no numbering. Ignore code, headings, "
        "opinions, and statements about what the author "
        "could not find or is unsure about. If there are no factual claims, output exactly NONE."
    )
    JUDGE_SYS = (
        "You are a strict fact checker for a university Java/OOP and software design course. "
        "Use the REFERENCE NOTES first, then your own reliable knowledge. "
        "Answer with exactly one word: SUPPORTED, CONTRADICTED or UNSURE."
    )
    CONSENSUS_SYS = (
        "Compare the two answers to the same question. Do they CONTRADICT each other on any fact "
        "or definition? Differences in wording, structure, examples, code, class names and level "
        "of detail are NOT contradictions. Answer with exactly one word: CONTRADICT or CONSISTENT."
    )

    def __init__(self, client):
        self.client = client

    def extract_claims(self, response, n=config.N_CLAIMS):
        prose = strip_code(response)
        if len(prose) < 15:
            return []
        text = self.client.chat("RESPONSE:\n" + prose[:3000],
                                self.CLAIM_SYS.format(n=n),
                                dict(config.VERIFIER_OPTIONS, num_predict=160))
        claims = []
        for ln in text.splitlines():
            ln = re.sub(r"^\s*(?:[-*\u2022]|\d+[\.\)])\s*", "", ln).strip()
            if ln.upper() != "NONE" and claim_like(ln):
                claims.append(ln)
        return claims[:n]

    def judge_claim(self, claim, notes):
        user = (f"REFERENCE NOTES:\n{notes or '(none available)'}\n\n"
                f"CLAIM: {claim}\nVerdict:")
        text = self.client.chat(user, self.JUDGE_SYS, dict(config.VERIFIER_OPTIONS, num_predict=4))
        m = re.match(r"\W*(SUPPORTED|CONTRADICTED|UNSURE)", text.strip().upper())
        return m.group(1) if m else "UNSURE"

    
    def consensus(self, answer_a, answer_b):
        a_ = strip_code(answer_a) or answer_a
        b_ = strip_code(answer_b) or answer_b

        user = (
            f"ANSWER 1:\n{a_[:1200]}\n\n"
            f"ANSWER 2:\n{b_[:1200]}\n\n"
            "Compare the factual meaning of these answers.\n"
            "Answer CONTRADICT only if they make at least one pair of "
            "explicitly incompatible factual claims about the same issue.\n"
            "If both answers are broadly correct and merely use different "
            "examples, class names, code, wording, or levels of detail, "
            "answer CONSISTENT.\n"
            "If no clear factual contradiction can be identified, answer "
            "CONSISTENT.\n"
            "Return exactly one word: CONSISTENT or CONTRADICT."
        )

        text = self.client.chat(
            user,
            self.CONSENSUS_SYS,
            dict(config.VERIFIER_OPTIONS, num_predict=8)
        )

        # Keep the raw output so we can diagnose incorrect decisions.
        self.last_consensus_raw = text

        result = re.search(
            r"\b(CONSISTENT|CONTRADICT)\b",
            text.strip().upper()
        )

        if not result:
            return False  # Fail closed if the output cannot be parsed.

        return result.group(1) == "CONSISTENT"


    def solve_quiz(self, prompt, kind, notes):
        sys_ = ("You are a careful university tutor. Use the reference notes if they help. "
                + ("Answer with only the letter of the correct option (A, B, C or D)."
                   if kind == "mcq" else "Answer with only True or False."))
        user = (f"REFERENCE NOTES:\n{notes}\n\n" if notes else "") + "QUESTION:\n" + prompt
        text = self.client.chat(user, sys_, dict(config.VERIFIER_OPTIONS, num_predict=8))
        return parse_answer_only(text, kind)

    def check_text(self, response, notes):
        claims = self.extract_claims(response)
        judged = [{"claim": c, "verdict": self.judge_claim(c, notes)} for c in claims]
        return judged

    def verify_references(self, refs, prompt):
        out = []
        for r in refs[:config.MAX_REFS]:
            res = lookup.check_reference(r, prompt)
            out.append({"ref": r, "result": res})
        return out


# ============================================================ Suggestion Agent
class SuggestionAgent:
    """Recommends learning materials.
    Condition A ('pool'): retrieve from a curated, pre-vetted resource pool.
    Condition B ('open'): pass the open-generated candidate on to the Verifier."""

    NUMS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}

    def __init__(self, pool_path):
        try:
            with open(pool_path, encoding="utf-8") as f:
                self.pool = json.load(f)
        except Exception:
            self.pool = []

    @staticmethod
    def is_recommendation_request(prompt):
        return bool(re.search(r"\b(recommend|suggest)\b", prompt, re.I))

    def from_pool(self, prompt):
        low = prompt.lower()
        want = "web" if re.search(r"\b(url|link|youtube|documentation|docs)\b", low) else (
            "paper" if "paper" in low else "book" if "book" in low else None)
        k = 3
        for w, n in self.NUMS.items():
            if re.search(rf"\b{w}\b", low):
                k = n
                break
        scored = []
        for e in self.pool:
            if want and e.get("type") != want:
                continue
            score = sum(1 for t in e.get("topics", []) if t in low)
            if score:
                scored.append((score, e.get("year", 0), e))
        scored.sort(key=lambda x: (-x[0], -x[1]))
        return [e for _, _, e in scored[:k]]

    @staticmethod
    def format_entries(entries):
        lines = []
        for i, e in enumerate(entries, 1):
            if e.get("type") == "web":
                lines.append(f'{i}. "{e["title"]}" - {e.get("url", "")}')
            else:
                lines.append(f'{i}. "{e["title"]}" by {e["authors"]} ({e["year"]})')
        return "\n".join(lines)


# ============================================================ Confidence Estimator
class ConfidenceEstimator:
    @staticmethod
    def quiz_confidence(candidate, votes):
        if candidate is None or not votes:
            return 0.0
        return round(sum(v == candidate for v in votes) / len(votes), 3)

    @staticmethod
    def support_score(judged, abstained=False):
        if not judged:
            # No checkable claims. An honest abstention is fine; anything else could not be
            # verified, so it only gets the neutral (UNSURE) weight.
            return 1.0 if abstained else config.SUPPORT_WEIGHTS["UNSURE"]
        w = config.SUPPORT_WEIGHTS
        return sum(w[j["verdict"]] for j in judged) / len(judged)

    @staticmethod
    def contradictions(judged):
        return sum(1 for j in judged if j["verdict"] == "CONTRADICTED")

    @staticmethod
    def text_confidence(support, consensus, contradictions):
        conf = 0.5 * support + 0.5 * consensus
        if contradictions:
            conf = min(conf, config.CONTRADICTION_CAP)
        return round(conf, 3)

    @staticmethod
    def regen_confidence(support, contradictions):
        return round(min(support, config.CONTRADICTION_CAP) if contradictions else support, 3)

    @staticmethod
    def reference_confidence(n_verified, n_total):
        return round(n_verified / n_total, 3) if n_total else 0.0