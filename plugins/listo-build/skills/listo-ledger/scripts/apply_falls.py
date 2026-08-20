#!/usr/bin/env python3
"""Apply the falling-series repairs, then assert the defect is actually gone.

A modifier cannot fall between acts: the pinned proficiency bonus rises +3/+4/+5 and ability
scores only ever go up. Every falling series is an error, and this refuses to write unless every
one it touched came back monotonic — a repair that silently leaves the defect in place is worse
than no repair, because the next audit reads the file as clean.
"""
import json, sys, glob, collections

ACTS = ("I", "II", "III")


def falling(skills):
    out = {}
    for sk in skills["I"]:
        v = [skills[a].get(sk) for a in ACTS]
        if all(isinstance(x, int) for x in v) and (v[1] < v[0] or v[2] < v[1]):
            out[sk] = v
    return out


def main(ledger, outdir, dest=None):
    L = json.load(open(ledger))
    C = L["chassis"]
    before = {cid: falling(c["skills"]) for cid, c in C.items()}
    before = {k: v for k, v in before.items() if v}

    fixes, seen = {}, collections.Counter()
    for f in sorted(glob.glob(f"{outdir}/out*.json")):
        for cid, rec in json.load(open(f)).items():
            fixes.setdefault(cid, {}).update({a: rec[a] for a in ACTS if a in rec})
            seen[cid] += 1
    dupes = [c for c, n in seen.items() if n > 1]
    if dupes:
        print(f"! {len(dupes)} chassis returned by both agents: {dupes}")

    missing = sorted(set(before) - set(fixes))
    if missing:
        print(f"! {len(missing)} defective chassis got no repair: {missing}")
        return 1

    changed = 0
    for cid, rec in fixes.items():
        if cid not in C:
            print(f"! unknown chassis {cid}")
            return 1
        for a in ACTS:
            for sk, v in rec.get(a, {}).items():
                if not isinstance(v, int):
                    print(f"! {cid} {a} {sk}: {v!r} is not an integer")
                    return 1
                if C[cid]["skills"][a].get(sk) != v:
                    changed += 1
                C[cid]["skills"][a][sk] = v

    after = {cid: falling(c["skills"]) for cid, c in C.items()}
    after = {k: v for k, v in after.items() if v}
    print(f"repaired {len(before)} chassis, {changed} values changed")
    if after:
        print(f"! {len(after)} chassis STILL fall across acts — not writing")
        for cid, bad in list(after.items())[:6]:
            print(f"    {cid}: {bad}")
        return 1
    json.dump(L, open(dest or ledger, "w"), indent=2, ensure_ascii=False)
    print(f"no falling series remain; wrote {dest or ledger}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
