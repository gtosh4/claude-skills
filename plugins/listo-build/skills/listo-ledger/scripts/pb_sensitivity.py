#!/usr/bin/env python3
"""How much does the act III proficiency-bonus convention actually move the ledger?

The evidence pass pins proficiency bonus at +3/+4/+5 by act. Strict rules would give +6 in act
III, and the previously collected data used both. The disagreement is exactly one point on act III
routine skills, so rather than litigate it per body, this measures the blast radius: rescore with
+1 on every act III routine skill and see how far the ranking moves.

If the top of the table is stable, the convention is a footnote. If it is not, it has to be
settled properly before anything is published.
"""
import json, sys, itertools, collections, copy

sys.path.insert(0, "/var/home/gordon/claude-skills/plugins/listo-build/skills/listo-build/scripts")
import scoring as S

ROUTINE = ("Perception", "Investigation", "Persuasion")


def rank(chassis, topn=20):
    ids = sorted(chassis)
    rows = []
    for a, b in itertools.combinations(ids, 2):
        try:
            r = S.score(chassis, a, b)
        except S.ScoringError:
            continue
        rows.append((r["score"], a, b))
    rows.sort(reverse=True)
    return rows[:topn], rows


def main(ledger):
    base = json.load(open(ledger))["chassis"]
    bumped = copy.deepcopy(base)
    for c in bumped.values():
        for sk in ROUTINE:
            if sk in c["skills"]["III"]:
                c["skills"]["III"][sk] += 1

    t0, all0 = rank(base)
    t1, all1 = rank(bumped)
    set0 = {(a, b) for _s, a, b in t0}
    set1 = {(a, b) for _s, a, b in t1}
    print(f"pairings scored: {len(all0)}")
    print(f"top 20 overlap : {len(set0 & set1)}/20")
    print(f"top 20 entering on the +6 convention: {sorted(x for x in set1 - set0)}")
    print(f"top 20 leaving : {sorted(x for x in set0 - set1)}")

    d = collections.Counter()
    m0 = {(a, b): s for s, a, b in all0}
    for s, a, b in all1:
        if (a, b) in m0:
            d[round(s - m0[(a, b)], 1)] += 1
    print(f"\nscore deltas across all pairings: {dict(sorted(d.items()))}")
    rungs = collections.Counter()
    for cid, c in base.items():
        r0 = S.derive_skills(c["skills"]["III"], "III", S._classes(c.get("split", "")))
        r1 = S.derive_skills(bumped[cid]["skills"]["III"], "III", S._classes(c.get("split", "")))
        rungs[(r0, r1)] += 1
    moved = sum(v for (x, y), v in rungs.items() if x != y)
    print(f"act III skl rung changed on {moved}/{len(base)} chassis")


if __name__ == "__main__":
    main(sys.argv[1])
