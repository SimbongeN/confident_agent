"""
Build a BLIND scoring sheet for the responses the agent CHANGED.

Responses the agent left unchanged are identical to the baseline text, so they inherit the
baseline score and need no re-scoring. For every prompt whose delivered answer differs from
the baseline (regenerated, filtered or taken from the pool) the sheet contains BOTH the
baseline response and the agent response, shuffled and unlabelled. Scorers do not know which
system wrote which answer. Re-scoring the baseline texts also gives you scorer-agreement data.

    python make_blind_sheet.py --baseline results_baseline_llama3.2_3b_scored.csv ^
        --agent results_agent_llama3.2_3b__qwen2.5_3b_open.csv --split 3

Writes blind_sheet.csv (or blind_sheet_part1..N.csv) and blind_key.csv (DO NOT open the key
while scoring).
"""
import argparse
import csv
import random

CHANGED = {"ACCEPTED_AFTER_REGEN", "ACCEPTED_FILTERED", "ACCEPTED_POOL"}
FIELDS = ["code", "prompt", "ground_truth", "response", "correct", "hallucination", "hall_type", "notes"]


def read(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--agent", required=True, nargs="+", help="one or more agent result CSVs")
    ap.add_argument("--split", type=int, default=1, help="number of scorers")
    ap.add_argument("--seed", type=int, default=2026)
    args = ap.parse_args()

    base = {r["id"]: r for r in read(args.baseline)}
    agent = {}
    for p in args.agent:
        for r in read(p):
            agent.setdefault(r["id"], r)

    items = []
    for i, a in agent.items():
        if a["status"] in CHANGED and a["final_response"].strip() != base[i]["response"].strip():
            items.append((i, "baseline", base[i]["response"], a))
            items.append((i, "agent", a["final_response"], a))
    random.Random(args.seed).shuffle(items)

    sheet, key = [], []
    for n, (i, system, resp, a) in enumerate(items, 1):
        code = f"R{n:03d}"
        sheet.append({"code": code, "prompt": a["prompt"], "ground_truth": a["ground_truth"],
                      "response": resp, "correct": "", "hallucination": "", "hall_type": "", "notes": ""})
        key.append({"code": code, "id": i, "system": system})

    with open("blind_key.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["code", "id", "system"])
        w.writeheader()
        w.writerows(key)
    parts = max(1, args.split)
    for k in range(parts):
        chunk = sheet[k::parts]
        name = "blind_sheet.csv" if parts == 1 else f"blind_sheet_part{k + 1}.csv"
        with open(name, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(chunk)
        print(f"wrote {name}: {len(chunk)} responses to score")
    print(f"{len(agent)} prompts in agent results; {len(items) // 2} changed answers -> "
          f"{len(items)} blind rows. Key saved to blind_key.csv (keep it closed while scoring).")


if __name__ == "__main__":
    main()
