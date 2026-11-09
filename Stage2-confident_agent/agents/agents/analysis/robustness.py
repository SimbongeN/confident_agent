import csv, math

rs = list(csv.DictReader(open('../analysis_results_per_item.csv', encoding='utf-8-sig')))

def mcnemar(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)

def report(name, sub):
    n = len(sub)
    hb = sum(int(r['base_h']) for r in sub)
    ha = sum(int(r['agent_h']) for r in sub)
    prevented = sum(1 for r in sub if r['base_h'] == '1' and r['agent_h'] == '0')
    introduced = sum(1 for r in sub if r['base_h'] == '0' and r['agent_h'] == '1')
    print(f"{name:32} n={n:3}  baseline {hb:2} ({100*hb/n:4.1f}%)  agent {ha:2} ({100*ha/n:4.1f}%)  "
          f"prevented {prevented:2}  introduced {introduced}  p={mcnemar(prevented, introduced):.4f}")

dev = {'A01', 'A03', 'A05', 'D04', 'E02'}
report('All prompts', rs)
report('Excluding development prompts', [r for r in rs if r['id'] not in dev])
report('A-E only (no external lookup)', [r for r in rs if r['category'][0] != 'F'])
report('A-E excluding development', [r for r in rs if r['category'][0] != 'F' and r['id'] not in dev])
report('F only (materials lookup)', [r for r in rs if r['category'][0] == 'F'])