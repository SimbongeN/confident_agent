"""
Check your reference notes BEFORE the long run.

    python check_notes.py --benchmark ..\benchmark.csv

Reports: files with a bad format, which note(s) the agent will retrieve for every benchmark
prompt, and which prompts get no notes at all (the verifier then relies on its own knowledge).
"""
import argparse
import csv
import os
import re

from notes import ReferenceNotes
from parsing import quiz_kind

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", default="benchmark.csv")
    ap.add_argument("--notes-dir", default=os.path.join(HERE, "reference_notes"))
    args = ap.parse_args()

    bad = []
    files = [f for f in sorted(os.listdir(args.notes_dir)) if f.lower().endswith(".md") and not f.startswith("_")]
    for fn in files:
        with open(os.path.join(args.notes_dir, fn), encoding="utf-8") as f:
            lines = f.read().splitlines()
        if len(lines) < 3 or not lines[0].startswith("# ") or not lines[1].lower().startswith("keywords:"):
            bad.append(fn)
        elif len(lines[1].split(":", 1)[1].strip()) < 3:
            bad.append(fn + " (empty keywords)")
    print(f"{len(files)} notes found. Bad format: {bad if bad else 'none'}")
    print("Format: line 1 '# Title', line 2 'keywords: a, b, c', then '- fact' bullets.\n")

    notes = ReferenceNotes(args.notes_dir)
    with open(args.benchmark, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    none = []
    for r in rows:
        p = r["prompt"]
        stem = re.sub(r"(?m)^\s*[A-D][\.\)]\s.*$", "", p) if quiz_kind(p) == "mcq" else p
        _, topics = notes.lookup(stem)
        print(f"{r['id']:4s} {r['topic'][:30]:30s} -> {topics if topics else '(none)'}")
        if not topics:
            none.append(r["id"] + " " + r["topic"])
    print(f"\nPrompts with NO notes: {len(none)} / {len(rows)}")
    for x in none:
        print("  -", x)
    print("\n(Materials prompts F01-F15 do not need notes: they are checked against Open Library, "
          "Crossref, arXiv and live URLs.)")


if __name__ == "__main__":
    main()
