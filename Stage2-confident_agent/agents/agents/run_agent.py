"""
Run the Confident Agent over the benchmark.

The baseline response (temperature 0, seed 42) is reused as the agent's first candidate,
so baseline and agent are compared prompt by prompt on identical generator output.

Examples (PowerShell, from this folder):
    python run_agent.py --baseline ..\results_baseline_llama3.2_3b_scored.csv --limit 3
    python run_agent.py --baseline ..\results_baseline_llama3.2_3b_scored.csv --shard 1/3
    python run_agent.py --baseline ..\results_baseline_llama3.2_3b_scored.csv --materials-mode pool

Output is appended row by row and can be resumed: re-run the same command after a crash
and finished prompts are skipped.
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.request

import config
import llm
import lookup
from agents import GeneratorAgent, SuggestionAgent, VerifierAgent
from chief import ChiefAgent
from notes import ReferenceNotes

HERE = os.path.dirname(os.path.abspath(__file__))

OUT_FIELDS = ["id", "category", "course", "topic", "obscurity", "scoring", "prompt",
              "ground_truth", "baseline_response", "final_response", "withheld_response",
              "status", "kind", "confidence", "regenerated", "llm_calls", "latency_s",
              "topics_used", "trace", "correct", "hallucination", "hall_type", "notes"]


def check_models(gen_model, ver_model):
    try:
        with urllib.request.urlopen(config.OLLAMA_TAGS_URL, timeout=10) as r:
            names = [m["name"] for m in json.loads(r.read().decode("utf-8")).get("models", [])]
    except Exception:
        print("ERROR: cannot reach Ollama at localhost:11434. Start Ollama and try again.")
        sys.exit(1)
    for m in (gen_model, ver_model):
        if not any(n == m or n.startswith(m + ":") or n.split(":")[0] == m for n in names):
            print(f"ERROR: model '{m}' not installed. Run: ollama pull {m}")
            sys.exit(1)


def matches(item_id, specs):
    """specs: IDs ('A01') or single-letter category prefixes ('F')."""
    return any(item_id == x or (len(x) == 1 and item_id.startswith(x)) for x in specs)


def done_ids(path):
    if not os.path.exists(path):
        return set()
    with open(path, newline="", encoding="utf-8-sig") as f:
        return {r["id"] for r in csv.DictReader(f)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", default="results_baseline_llama3.2_3b_scored.csv")
    ap.add_argument("--out", default=None)
    ap.add_argument("--generator", default=config.GENERATOR_MODEL)
    ap.add_argument("--verifier", default=config.VERIFIER_MODEL)
    ap.add_argument("--notes-dir", default=os.path.join(HERE, "reference_notes"))
    ap.add_argument("--pool", default=os.path.join(HERE, "resource_pool.json"))
    ap.add_argument("--materials-mode", choices=["open", "pool"], default="open")
    ap.add_argument("--samples", type=int, default=config.N_SAMPLES)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--ids", default=None, help="only these IDs or letters, e.g. A01,C03 or F")
    ap.add_argument("--exclude", default=None, help="skip these IDs or letters, e.g. F or A01,C")
    ap.add_argument("--shard", default=None, help="i/n, e.g. 2/3 to split work across PCs")
    args = ap.parse_args()

    check_models(args.generator, args.verifier)
    if not lookup.selftest():
        print("WARNING: Open Library is unreachable - materials checks will be UNCHECKED "
              "(treated as not verified). Check your internet connection.")

    with open(args.baseline, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if args.ids:
        wanted = [x.strip() for x in args.ids.split(",") if x.strip()]
        rows = [r for r in rows if matches(r["id"], wanted)]
    if args.exclude:
        skip = [x.strip() for x in args.exclude.split(",") if x.strip()]
        rows = [r for r in rows if not matches(r["id"], skip)]
    if args.shard:
        i, n = (int(x) for x in args.shard.split("/"))
        rows = [r for k, r in enumerate(rows) if k % n == i - 1]
    if args.limit:
        rows = rows[: args.limit]

    tag = f"{args.generator}__{args.verifier}".replace(":", "_")
    suffix = f"_{args.materials_mode}" + (f"_shard{args.shard.replace('/', 'of')}" if args.shard else "")
    out_path = args.out or f"results_agent_{tag}{suffix}.csv"

    already = done_ids(out_path)
    todo = [r for r in rows if r["id"] not in already]
    print(f"{len(rows)} prompts selected, {len(already)} already done, {len(todo)} to run -> {out_path}")

    gen = GeneratorAgent(llm.OllamaClient(args.generator))
    ver = VerifierAgent(llm.OllamaClient(args.verifier))
    sug = SuggestionAgent(args.pool)
    notes = ReferenceNotes(args.notes_dir)
    print(f"Reference notes loaded for {len(notes.topics)} topics; pool entries: {len(sug.pool)}")
    chief = ChiefAgent(gen, ver, sug, notes, materials_mode=args.materials_mode,
                       n_samples=args.samples)

    new_file = not os.path.exists(out_path)
    with open(out_path, "a", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=OUT_FIELDS)
        if new_file:
            w.writeheader()
        for k, r in enumerate(todo, 1):
            llm.reset_stats()
            start = time.time()
            try:
                # the agent sees ONLY the prompt and the baseline candidate
                d = chief.handle(r["prompt"], candidate=r["response"])
            except Exception as e:
                print(f"[{k}/{len(todo)}] {r['id']} FAILED ({e}); will be retried on re-run")
                continue
            elapsed = round(time.time() - start, 1)
            stats = llm.get_stats()
            w.writerow({
                "id": r["id"], "category": r.get("category", ""), "course": r.get("course", ""),
                "topic": r.get("topic", ""), "obscurity": r.get("obscurity", ""),
                "scoring": r.get("scoring", ""), "prompt": r["prompt"],
                "ground_truth": r.get("ground_truth", ""), "baseline_response": r["response"],
                "final_response": d.final_response, "withheld_response": d.withheld_response,
                "status": d.status, "kind": d.kind, "confidence": d.confidence,
                "regenerated": int(d.regenerated), "llm_calls": stats["calls"],
                "latency_s": elapsed, "topics_used": ";".join(d.topics),
                "trace": json.dumps(d.trace, ensure_ascii=False),
                "correct": "", "hallucination": "", "hall_type": "", "notes": "",
            })
            f.flush()
            print(f"[{k}/{len(todo)}] {r['id']} {d.status:22s} conf={d.confidence:<5} "
                  f"calls={stats['calls']} {elapsed}s")
    print("Finished. Score the 'final_response' column the same way as the baseline.")


if __name__ == "__main__":
    main()
