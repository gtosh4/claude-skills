#!/usr/bin/env python3
"""Merge the routine-skills evidence pass into a ledger, with calibration.

Three skills carry the whole Skills axis now — Perception, Investigation and Persuasion — so this
checks agent output before it lands rather than after. Three checks, in order of what has actually
gone wrong before:

  coverage     every chassis, every act, all three skills, integers. A missing value used to be
               read as "untrained" and is now an evidence gap, so it must never merge silently.
  calibration  Perception and Investigation already existed on some bodies. A new number that
               disagrees with the old one is either a correction or agent drift, and the two look
               identical in a merged file. Reported, never auto-resolved.
  progression  modifiers should rise across acts. The pinned proficiency bonus is +3/+4/+5, so a
               fall means an agent recomputed it from character level instead of using the pin.
"""
import json, sys, collections, pathlib

SKILLS = ("Perception", "Investigation", "Persuasion")
ACTS = ("I", "II", "III")


def load(outdir):
    merged, dupes = {}, []
    for f in sorted(pathlib.Path(outdir).glob("out*.json")):
        for cid, rec in json.load(open(f)).items():
            if cid in merged:
                dupes.append(cid)
            merged[cid] = dict(rec, _src=f.name)
    return merged, dupes


def check(merged, chassis):
    problems = collections.defaultdict(list)
    for cid in chassis:
        if cid not in merged:
            problems["missing chassis"].append(cid); continue
        rec = merged[cid]
        for act in ACTS:
            if act not in rec:
                problems["missing act"].append(f"{cid} {act}"); continue
            for sk in SKILLS:
                v = rec[act].get(sk)
                if v is None:
                    problems["missing skill"].append(f"{cid} {act} {sk}")
                elif not isinstance(v, int):
                    problems["non-integer"].append(f"{cid} {act} {sk}={v!r}")
        # progression: pinned PB rises +3/+4/+5, so no skill may fall between acts
        for sk in SKILLS:
            vals = [rec.get(a, {}).get(sk) for a in ACTS]
            if all(isinstance(v, int) for v in vals) and (vals[1] < vals[0] or vals[2] < vals[1]):
                problems["falls across acts"].append(f"{cid} {sk} {vals} [{rec['_src']}]")
    return problems


def calibrate(merged, chassis):
    """New values against what was already recorded. Not an error — a disagreement to look at."""
    diffs = collections.defaultdict(list)
    for cid, c in chassis.items():
        if cid not in merged:
            continue
        for act in ACTS:
            for sk in ("Perception", "Investigation"):
                old = c["skills"][act].get(sk)
                new = merged[cid].get(act, {}).get(sk)
                if isinstance(old, int) and isinstance(new, int) and old != new:
                    diffs[merged[cid]["_src"]].append((cid, act, sk, old, new))
    return diffs


def main(ledger, outdir, dest=None):
    L = json.load(open(ledger))
    chassis = L["chassis"]
    merged, dupes = load(outdir)
    if dupes:
        print(f"! {len(dupes)} chassis returned by more than one agent: {dupes[:5]}")

    problems = check(merged, chassis)
    for kind, items in sorted(problems.items()):
        print(f"! {kind}: {len(items)}")
        for x in items[:6]:
            print(f"    {x}")

    diffs = calibrate(merged, chassis)
    total = sum(len(v) for v in diffs.values())
    print(f"\ncalibration: {total} disagreements with previously recorded values")
    for src, rows in sorted(diffs.items()):
        by = collections.Counter(n - o for _c, _a, _s, o, n in rows)
        print(f"  {src}: {len(rows):4d}  delta spread {dict(sorted(by.items()))}")
    if total:
        print("  (a whole-slice constant offset is drift; a scatter is per-body correction)")

    if any(k != "falls across acts" for k in problems):
        print("\nnot merging — fix coverage first")
        return 1
    for cid, rec in merged.items():
        if cid not in chassis:
            continue
        for act in ACTS:
            chassis[cid]["skills"][act].update({sk: rec[act][sk] for sk in SKILLS})
            chassis[cid]["skills"][act].pop("Religion", None)
    json.dump(L, open(dest or ledger, "w"), indent=2, ensure_ascii=False)
    print(f"\nmerged {len(merged)} chassis into {dest or ledger}")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
