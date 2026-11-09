# Analysis scripts (run AFTER the full agent run)

1. make_blind_sheet.py  - builds shuffled, unlabelled scoring sheets for answers the agent changed
2. (team scores the sheets by hand: correct / hallucination / hall_type / notes)
3. analyze.py           - McNemar, Wilson and bootstrap intervals, FRR, breakdowns, cost, charts

See the docstring at the top of each script for the exact commands.
Optional: pip install matplotlib   (for the two PNG charts)
