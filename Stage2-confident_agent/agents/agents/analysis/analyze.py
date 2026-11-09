"""
Statistical analysis: baseline vs Confident Agent on the same benchmark.

Inputs
  --baseline   results_baseline_..._scored.csv   (your adjudicated baseline scores)
  --agent      one or more agent result CSVs      (merge shards or list them all)
  --blind      filled blind_sheet*.csv files      (scores for responses the agent changed)
  --key        blind_key.csv

Outcome definitions (per prompt)
  * unchanged answer      -> inherits the baseline score (identical text)
  * FLAGGED               -> content withheld: no hallucination reaches the student, not a correct answer
  * changed answer        -> score from the blind sheet
Primary baseline scores are your original adjudicated ones; a sensitivity analysis uses the
blind re-score of the baseline text wherever one exists. Cohen's kappa between the two sets of
baseline scores is reported as scorer agreement.

    python analyze.py --baseline ..\results_baseline_llama3.2_3b_scored.csv ^
        --agent ..\results_agent_*.csv --blind blind_sheet_part1.csv blind_sheet_part2.csv ^
        blind_sheet_part3.csv --key blind_key.csv
"""
import argparse
import csv
import glob
import math
import random
from collections import Counter, defaultdict

CHANGED = {"ACCEPTED_AFTER_REGEN", "ACCEPTED_FILTERED", "ACCEPTED_POOL"}


# ------------------------------------------------------------------ io
def read(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def expand(patterns):
    out = []
    for p in patterns:
        out.extend(sorted(glob.glob(p)) or [p])
    return out


def flag(v):
    v = (v or "").strip()
    return int(v) if v in ("0", "1") else None


# ------------------------------------------------------------------ statistics
def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (100 * (c - h), 100 * (c + h))


def mcnemar_exact(b, c):
    """Two-sided exact McNemar (binomial) p-value on discordant pairs."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def kappa(x, y):
    n = len(x)
    if n == 0:
        return float("nan")
    po = sum(a == b for a, b in zip(x, y)) / n
    px1, py1 = sum(x) / n, sum(y) / n
    pe = px1 * py1 + (1 - px1) * (1 - py1)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def boot_ci(pairs, fn, reps=10000, seed=7):
    rnd = random.Random(seed)
    vals = []
    n = len(pairs)
    for _ in range(reps):
        s = [pairs[rnd.randrange(n)] for _ in range(n)]
        vals.append(fn(s))
    vals.sort()
    return vals[int(0.025 * reps)], vals[int(0.975 * reps)]


def pct(k, n):
    return 100 * k / n if n else float("nan")


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--agent", required=True, nargs="+")
    ap.add_argument("--blind", nargs="*", default=[])
    ap.add_argument("--key", default="blind_key.csv")
    ap.add_argument("--out", default="analysis_results")
    args = ap.parse_args()

    base = {r["id"]: r for r in read(args.baseline)}
    agent = {}
    for p in expand(args.agent):
        for r in read(p):
            agent.setdefault(r["id"], r)
    ids = sorted(i for i in base if i in agent)
    missing = sorted(set(base) - set(agent))
    if missing:
        print(f"WARNING: {len(missing)} prompts have no agent result and are excluded: {missing}")

    # blind scores
    blind = {}
    if args.blind:
        key = {r["code"]: r for r in read(args.key)}
        for p in expand(args.blind):
            for r in read(p):
                k = key.get(r["code"])
                if k and flag(r["correct"]) is not None and flag(r["hallucination"]) is not None:
                    blind[(k["id"], k["system"])] = (flag(r["correct"]), flag(r["hallucination"]))

    rows, unscored = [], []
    for i in ids:
        b, a = base[i], agent[i]
        b_c, b_h = flag(b["correct"]), flag(b["hallucination"])
        if b_c is None or b_h is None:
            unscored.append(i + " (baseline)")
            continue
        status = a["status"]
        if status == "FLAGGED":
            a_c, a_h, kind = 0, 0, "withheld"
        elif status in CHANGED and a["final_response"].strip() != b["response"].strip():
            if (i, "agent") not in blind:
                unscored.append(i + " (agent, blind sheet)")
                continue
            a_c, a_h = blind[(i, "agent")]
            kind = "changed"
        else:
            a_c, a_h, kind = b_c, b_h, "unchanged"
        sens = blind.get((i, "baseline"))
        rows.append({"id": i, "category": b["category"], "course": b.get("course", ""),
                     "obscurity": b.get("obscurity", ""), "status": status, "kind": kind,
                     "base_c": b_c, "base_h": b_h, "agent_c": a_c, "agent_h": a_h,
                     "base_h_blind": sens[1] if sens else b_h,
                     "base_c_blind": sens[0] if sens else b_c,
                     "agent_latency": float(a["latency_s"] or 0), "agent_calls": int(a["llm_calls"] or 0),
                     "base_latency": float(b.get("latency_s") or 0)})
    if unscored:
        print(f"WARNING: unscored rows excluded ({len(unscored)}): {unscored}")
    N = len(rows)
    if N == 0:
        raise SystemExit("No scored rows to analyse.")

    out = []
    P = out.append

    # ---- primary comparison
    hb = sum(r["base_h"] for r in rows)
    ha = sum(r["agent_h"] for r in rows)
    b_only = sum(1 for r in rows if r["base_h"] == 1 and r["agent_h"] == 0)   # prevented
    a_only = sum(1 for r in rows if r["base_h"] == 0 and r["agent_h"] == 1)   # introduced
    p_val = mcnemar_exact(b_only, a_only)
    lo_b, hi_b = wilson(hb, N)
    lo_a, hi_a = wilson(ha, N)
    rel = 100 * (hb - ha) / hb if hb else float("nan")
    pairs = [(r["base_h"], r["agent_h"]) for r in rows]
    d_lo, d_hi = boot_ci(pairs, lambda s: 100 * (sum(x for x, _ in s) - sum(y for _, y in s)) / len(s))
    P("# Results: baseline vs Confident Agent\n")
    P(f"Prompts analysed: **{N}**\n")
    P("## 1. Hallucination rate (paired, primary analysis)\n")
    P("| System | Hallucinated | Rate | 95% Wilson CI |")
    P("|---|---|---|---|")
    P(f"| Baseline | {hb}/{N} | {pct(hb, N):.1f}% | {lo_b:.1f}% to {hi_b:.1f}% |")
    P(f"| Confident Agent | {ha}/{N} | {pct(ha, N):.1f}% | {lo_a:.1f}% to {hi_a:.1f}% |")
    P(f"\n- Absolute reduction: **{pct(hb, N) - pct(ha, N):.1f} percentage points** "
      f"(paired bootstrap 95% CI {d_lo:.1f} to {d_hi:.1f})")
    P(f"- Relative reduction: **{rel:.1f}%**")
    P(f"- Discordant pairs: prevented (baseline hallucinated, agent not) = {b_only}; "
      f"introduced (agent hallucinated, baseline not) = {a_only}")
    P(f"- McNemar exact test: **p = {p_val:.4f}** ({'significant' if p_val < 0.05 else 'not significant'} at 0.05)\n")

    # ---- side effects
    base_correct = [r for r in rows if r["base_c"] == 1]
    flagged = [r for r in rows if r["kind"] == "withheld"]
    false_rej = [r for r in base_correct if r["kind"] == "withheld"]
    degraded = [r for r in base_correct if r["kind"] == "changed" and r["agent_c"] == 0]
    base_hall = [r for r in rows if r["base_h"] == 1]
    caught_w = [r for r in base_hall if r["kind"] == "withheld"]
    caught_f = [r for r in base_hall if r["kind"] == "changed" and r["agent_h"] == 0 and r["agent_c"] == 1]
    caught_p = [r for r in base_hall if r["kind"] == "changed" and r["agent_h"] == 0 and r["agent_c"] == 0]
    missed = [r for r in base_hall if r["agent_h"] == 1]
    P("## 2. Side effects and trade-offs\n")
    P("| Metric | Value |")
    P("|---|---|")
    P(f"| Withheld (flagged) answers | {len(flagged)}/{N} ({pct(len(flagged), N):.1f}%) |")
    fr_lo, fr_hi = wilson(len(false_rej), len(base_correct))
    P(f"| **False rejection rate** (correct baseline answers withheld) | {len(false_rej)}/{len(base_correct)} "
      f"({pct(len(false_rej), len(base_correct)):.1f}%, CI {fr_lo:.1f}% to {fr_hi:.1f}%) |")
    P(f"| Degradation rate (correct baseline answer replaced by an incorrect one) | "
      f"{len(degraded)}/{len(base_correct)} ({pct(len(degraded), len(base_correct)):.1f}%) |")
    P(f"| Flag precision (withheld answers that were hallucinated in the baseline) | "
      f"{sum(r['base_h'] for r in flagged)}/{len(flagged)} "
      f"({pct(sum(r['base_h'] for r in flagged), len(flagged)):.1f}%) |")
    P(f"| Baseline correct-answer rate | {sum(r['base_c'] for r in rows)}/{N} "
      f"({pct(sum(r['base_c'] for r in rows), N):.1f}%) |")
    P(f"| Agent correct-answer rate (answers shown and correct) | {sum(r['agent_c'] for r in rows)}/{N} "
      f"({pct(sum(r['agent_c'] for r in rows), N):.1f}%) |\n")
    P("**What happened to the baseline's hallucinations** "
      f"(n = {len(base_hall)}):\n")
    P(f"- withheld by the agent: {len(caught_w)}")
    P(f"- repaired (regenerated/filtered answer is correct): {len(caught_f)}")
    P(f"- replaced by an answer that is not hallucinated but not fully correct: {len(caught_p)}")
    P(f"- missed (still hallucinated): {len(missed)}\n")

    # ---- status distribution
    P("## 3. Pipeline decisions\n")
    P("| Status | Count |")
    P("|---|---|")
    for s, c in Counter(r["status"] for r in rows).most_common():
        P(f"| {s} | {c} |")
    P("")

    # ---- breakdowns
    def breakdown(title, keyfn):
        groups = defaultdict(list)
        for r in rows:
            groups[keyfn(r)].append(r)
        P(f"## {title}\n")
        P("| Group | n | Baseline HR | Agent HR | Prevented | Introduced | Withheld |")
        P("|---|---|---|---|---|---|---|")
        res = {}
        for g in sorted(groups):
            rs = groups[g]
            n = len(rs)
            hb_, ha_ = sum(x["base_h"] for x in rs), sum(x["agent_h"] for x in rs)
            pv = sum(1 for x in rs if x["base_h"] == 1 and x["agent_h"] == 0)
            it = sum(1 for x in rs if x["base_h"] == 0 and x["agent_h"] == 1)
            wh = sum(1 for x in rs if x["kind"] == "withheld")
            P(f"| {g} | {n} | {pct(hb_, n):.1f}% ({hb_}) | {pct(ha_, n):.1f}% ({ha_}) | {pv} | {it} | {wh} |")
            res[g] = (pct(hb_, n), pct(ha_, n))
        P("")
        return res

    by_cat = breakdown("4. By category", lambda r: r["category"])
    by_obs = breakdown("5. By obscurity level", lambda r: f"level {r['obscurity']}")
    breakdown("6. By course", lambda r: r["course"])

    # ---- cost
    P("## 7. Cost and latency\n")
    P("| | Baseline | Confident Agent |")
    P("|---|---|---|")
    bl = sum(r["base_latency"] for r in rows) / N
    al = sum(r["agent_latency"] for r in rows) / N
    ac = sum(r["agent_calls"] for r in rows) / N
    P(f"| Mean seconds per prompt | {bl:.1f} | {bl + al:.1f} (generation {bl:.1f} + validation {al:.1f}) |")
    P(f"| Mean LLM calls per prompt | 1 | {1 + ac:.1f} |")
    P(f"| Slow-down factor | 1.0x | {(bl + al) / bl:.1f}x |\n" if bl else "")

    # ---- sensitivity + agreement
    both = [r for r in rows if r["base_h_blind"] is not None and
            (r["id"], "baseline") in {(k[0], k[1]) for k in blind}]
    if both:
        x = [r["base_h"] for r in both]
        y = [r["base_h_blind"] for r in both]
        xc = [r["base_c"] for r in both]
        yc = [r["base_c_blind"] for r in both]
        P("## 8. Scorer agreement and sensitivity\n")
        P(f"Baseline answers re-scored blind: {len(both)}")
        P(f"- Agreement on 'hallucination': {pct(sum(a == b for a, b in zip(x, y)), len(x)):.1f}% "
          f"(Cohen's kappa = {kappa(x, y):.2f})")
        P(f"- Agreement on 'correct': {pct(sum(a == b for a, b in zip(xc, yc)), len(xc)):.1f}% "
          f"(Cohen's kappa = {kappa(xc, yc):.2f})")
        hb2 = sum(r["base_h_blind"] for r in rows)
        bo2 = sum(1 for r in rows if r["base_h_blind"] == 1 and r["agent_h"] == 0)
        ao2 = sum(1 for r in rows if r["base_h_blind"] == 0 and r["agent_h"] == 1)
        P(f"- Sensitivity (using the blind re-score for those baseline answers): baseline HR "
          f"{pct(hb2, N):.1f}%, agent HR {pct(ha, N):.1f}%, McNemar p = {mcnemar_exact(bo2, ao2):.4f}\n")
    else:
        P("## 8. Scorer agreement\n\nNo blind re-scores of baseline answers were supplied.\n")

    text = "\n".join(out)
    print(text)
    with open(args.out + ".md", "w", encoding="utf-8") as f:
        f.write(text)
    with open(args.out + "_per_item.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # ---- charts
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        def chart(res, title, fname):
            labels = list(res.keys())
            xs = range(len(labels))
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar([x - 0.2 for x in xs], [res[k][0] for k in labels], 0.4, label="Baseline")
            ax.bar([x + 0.2 for x in xs], [res[k][1] for k in labels], 0.4, label="Confident Agent")
            ax.set_xticks(list(xs))
            ax.set_xticklabels([l.replace("_", "\n") for l in labels], fontsize=8)
            ax.set_ylabel("Hallucination rate (%)")
            ax.set_title(title)
            ax.legend()
            fig.tight_layout()
            fig.savefig(fname, dpi=160)
            plt.close(fig)

        chart(by_cat, "Hallucination rate by category", args.out + "_by_category.png")
        chart(by_obs, "Hallucination rate by obscurity level", args.out + "_by_obscurity.png")
        print(f"\nCharts saved: {args.out}_by_category.png, {args.out}_by_obscurity.png")
    except ImportError:
        print("\n(matplotlib not installed: run 'pip install matplotlib' to also get the charts)")
    print(f"Saved {args.out}.md and {args.out}_per_item.csv")


if __name__ == "__main__":
    main()
