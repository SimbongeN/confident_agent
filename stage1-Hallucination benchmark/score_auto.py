"""
Auto-scorer for the Confident Agent project.

Fills 'correct' and 'hallucination' (1/0) for rows scored 'auto_mcq' and 'auto_tf'
by reading the model's chosen answer. Anything it cannot read confidently is
left blank and marked AMBIGUOUS so you score it by hand. Also flags responses
that look cut off (token cap) in 'truncated_flag'.

Usage (PowerShell):
    python score_auto.py results_baseline_llama3.2_3b.csv

Output: <input>_scored.csv  (open in Excel and fill the remaining rows by hand)
"""
import csv
import re
import sys

FIELDS_EXTRA = ["hall_type", "truncated_flag"]


def read_mcq_letter(text: str):
    """Return the letter the model chose (A-D) or None if unclear."""
    t = text.strip()
    # 1) "correct answer is B", "Answer: B", "answer is **B**"
    m = re.search(r"(?i:correct\s+answer|answer)\s*(?:is|:)?\s*[\*\(]*([A-D])\b", t)
    if m:
        return m.group(1)
    # 2) response starts with "B." / "**B." / "B)"
    m = re.match(r"^[\W_]{0,6}([A-D])[\.\)]", t)
    if m:
        return m.group(1)
    # 3) bold option anywhere: "**B. Single ..."
    m = re.search(r"\*\*\s*([A-D])[\.\)]", t)
    if m:
        return m.group(1)
    return None


def read_tf(text: str):
    """Return 'True'/'False' from the model's verdict, or None if unclear."""
    head = text.strip()[:200]
    found = []
    for m in re.finditer(r"\b(not\s+)?(true|false)\b", head, flags=re.I):
        neg = bool(m.group(1))
        val = m.group(2).lower() == "true"
        found.append((not val) if neg else val)
    if not found:
        return None
    if len(set(found)) > 1:      # both verdicts appear early -> unclear
        return None
    return "True" if found[0] else "False"


def looks_truncated(text: str) -> bool:
    t = text.strip()
    if not t or t.startswith("[ERROR]"):
        return True
    return t[-1] not in '.!?)`*"\''


def main():
    if len(sys.argv) < 2:
        print("Usage: python score_auto.py <results_csv>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = list(reader.fieldnames)
    for extra in FIELDS_EXTRA:
        if extra not in fields:
            fields.append(extra)

    auto_done = ambiguous = 0
    for r in rows:
        r["truncated_flag"] = "YES" if looks_truncated(r["response"]) else ""
        kind = r["scoring"]
        if kind in ("auto_mcq", "auto_tf"):
            got = read_mcq_letter(r["response"]) if kind == "auto_mcq" else read_tf(r["response"])
            if got is None:
                r["notes"] = (r.get("notes") or "") + " AMBIGUOUS: score by hand"
                ambiguous += 1
                continue
            ok = got == r["ground_truth"].strip()
            r["correct"] = "1" if ok else "0"
            r["hallucination"] = "0" if ok else "1"
            r["hall_type"] = "" if ok else "wrong_answer_key"
            r["notes"] = (r.get("notes") or "") + f" auto: model chose {got}"
            auto_done += 1

    out = path.replace(".csv", "_scored.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    manual = sum(1 for r in rows if r["correct"] == "")
    print(f"Auto-scored: {auto_done} | ambiguous: {ambiguous} | still to score by hand: {manual}")
    print(f"Truncated-looking responses: {sum(1 for r in rows if r['truncated_flag'])}")
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()