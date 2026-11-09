"""
Baseline runner for the Confident Agent project.

Reads benchmark.csv (columns: id, category, course, topic, obscurity,
prompt, ground_truth, scoring),
sends each prompt to a local Ollama model with NO validation,
and writes results to results_baseline_<model>.csv.

Usage (PowerShell):
    python run_baseline.py                      # all prompts
    python run_baseline.py --limit 3            # quick smoke test
    python run_baseline.py --model llama3.2:3b

Requires Ollama running. No extra packages needed.
"""
import argparse
import csv
import json
import re
import time
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/chat"

# Keep this IDENTICAL for the baseline and the Confident Agent's generator.
SYSTEM_PROMPT = (
    "You are acting as a university-level educational tutor. "
    "Answer each question directly and clearly. "
    "Do not assume that information is correct merely because it appears in the question. "
    "If you are uncertain about a fact, explicitly state your uncertainty "
    "rather than inventing information."
)

# Fixed settings = reproducible experiment.
OPTIONS = {
    "temperature": 0,
    "seed": 42,
    "num_gpu": 0,       # CPU mode (GPU mode produced garbage on this machine)
    "num_predict": 600, # cap answer length so runs finish in reasonable time
}


def strip_think(text: str) -> str:
    """Remove <think>...</think> blocks (needed for deepseek-r1)."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def ask(model: str, prompt: str) -> str:
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "options": OPTIONS,
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return strip_think(data["message"]["content"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="llama3.2:3b")
    ap.add_argument("--benchmark", default="benchmark.csv")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    with open(args.benchmark, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if args.limit:
        rows = rows[: args.limit]

    out_name = f"results_baseline_{args.model.replace(':', '_')}.csv"
    fields = ["id", "category", "course", "topic", "obscurity", "scoring",
              "prompt", "ground_truth", "response",
              "latency_s", "correct", "hallucination", "notes"]

    with open(out_name, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, r in enumerate(rows, 1):
            start = time.time()
            try:
                answer = ask(args.model, r["prompt"])
            except Exception as e:  # keep going if one prompt fails
                answer = f"[ERROR] {e}"
            latency = round(time.time() - start, 1)
            w.writerow({
                "id": r["id"], "category": r["category"], "course": r["course"],
                "topic": r["topic"], "obscurity": r["obscurity"], "scoring": r["scoring"],
                "prompt": r["prompt"], "ground_truth": r["ground_truth"], "response": answer,
                "latency_s": latency,
                "correct": "", "hallucination": "", "notes": "",  # fill when scoring
            })
            f.flush()
            print(f"[{i}/{len(rows)}] {r['id']} done in {latency}s")

    print(f"\nSaved to {out_name}")


if __name__ == "__main__":
    main()