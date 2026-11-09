# Development-phase changes (made BEFORE the full 76-prompt run)

Development prompts used for smoke tests: A01, A03, A05, D04, E02. Report results with and without these.
No thresholds in config.py were changed.

1. agents.py  VerifierAgent.consensus(): asks "do the answers contradict?" (wording/structure/code differences
   do not count); raw verifier output is logged. Regeneration prompt no longer lists books/papers and
   meta-commentary is stripped (clean_regen).
2. chief.py  _text(): consensus_raw / consensus_votes written to the trace.
3. chief.py  _text(): a regenerated answer with NO checkable claims and no honest abstention is FLAGGED
   (it previously passed because the neutral score 0.6 equals REGEN_ACCEPT). trace["regen_unverified"] added.
4. reference_notes/covariant-return-types.md: keywords no longer include generic words (java, subtype,
   polymorphism, method overriding). It was being retrieved for 22/76 prompts.
5. reference_notes/open-closed-principle.md: keywords add "Open/Closed Principle" and "open closed", and
   drop generic ones (polymorphism, abstraction, software design). A05 previously missed this note.
6. test_offline.py: new tests for (3), (4), (5). All pass.

Known limitations to report: verifier cannot judge code; honest-abstention cue bypasses claim checking (E02);
UNSURE-only regenerations are accepted if nothing is contradicted; 3 non-materials prompts have no note (C09, C13, E08).
