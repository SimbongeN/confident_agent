# Confident Agent - Stage 2 code

Pipeline controlled by a Chief Agent (plain Python, no framework):

    candidate (baseline response, reused)
        -> classify request (quiz / materials / free text)
        -> Verifier checks it (different model family + external lookups)
        -> Confidence Estimator scores it
        -> Chief Agent: ACCEPT / REGENERATE once (grounded on notes) / FLAG

| File | Role |
|---|---|
| config.py | models, settings, thresholds (fixed BEFORE evaluation) |
| agents.py | Generator, Verifier, Suggestion Agent, Confidence Estimator |
| chief.py | Chief Agent and decision policy |
| lookup.py | Open Library, Crossref, arXiv and URL checks (no LLM) |
| notes.py | topic-keyed reference notes (no vector database) |
| run_agent.py | runs the benchmark, resumable, shardable |
| test_offline.py | self-test with fake Ollama and fake web (no models/internet needed) |
| reference_notes/ | YOUR topic notes (see _TEMPLATE.md) |
| resource_pool.json | curated pool for materials condition A |

## Setup
    ollama pull qwen2.5:3b
    python test_offline.py          (all tests must pass)

## Run (from this folder; use your real path to the scored baseline CSV)
    python run_agent.py --baseline ..\results_baseline_llama3.2_3b_scored.csv --limit 3
    python run_agent.py --baseline ..\results_baseline_llama3.2_3b_scored.csv --shard 1/3     (PC 1)
    python run_agent.py --baseline ..\results_baseline_llama3.2_3b_scored.csv --shard 2/3     (PC 2)
    python run_agent.py --baseline ..\results_baseline_llama3.2_3b_scored.csv --shard 3/3     (PC 3)

Materials condition A (curated pool) - run after the main run, on the F prompts only:
    python run_agent.py --baseline ..\results_baseline_llama3.2_3b_scored.csv --materials-mode pool --ids F

Tip: materials (F) prompts do not use the reference notes, so they can be run first:
    python run_agent.py --baseline ..\results_baseline_llama3.2_3b_scored.csv --ids F
and the rest later with --exclude F (add --shard i/n as above).

Merge the shard CSVs into one file before scoring.

## Rules that keep the experiment valid
1. Write reference_notes/*.md from your LECTURE SLIDES at topic level. Never paste the
   benchmark ground_truth column into them (circular evaluation).
2. Do not change thresholds in config.py after looking at benchmark results.
3. The agent sees only the prompt and the baseline candidate - never ground truth/category/scoring.
4. SYSTEM_PROMPT and GEN_OPTIONS in config.py must match run_baseline.py.
5. resource_pool.json: verify every entry yourselves before the run and extend it from your
   course reading list. Entries were seeded from general knowledge, not checked by the tool.
