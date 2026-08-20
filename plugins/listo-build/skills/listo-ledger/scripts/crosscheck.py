#!/usr/bin/env python3
"""Check built bodies against the tier-1 base profiles, which are the authority on subclasses.

The fail-closed doctrine, one level up. `scoring.py` raises on a value it does not RECOGNISE —
an unknown booster id, an unknown reach. Nothing checked for a value that was simply OMITTED: an
effect that exists, has a registry id, is reachable at this body's level, and is not recorded.
That is the same invisible failure the doctrine exists for, because a missing booster scores as
nothing and a score that is too low reads exactly like an honest one.

The base profiles know what each subclass contributes on its own. A built body reaching that
subclass must carry at least that. It may carry MORE — anything extra came from the dip, and
sibling variants are supposed to differ, so this is a subset test and never an equality test.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, HERE)
import seed_index as S                                            # noqa: E402


def check(chassis, keys, bases_path=None):
    """Returns `(errors, review)`. Errors are omissions; review is a judgement queue."""
    doc = json.load(open(bases_path or os.path.join(ASSETS, "subclass-bases.json")))
    base, arrives = doc["bases"], doc.get("arrives", {})
    errors, review = [], []
    for cid, ch in sorted(chassis.items()):
        own = keys.get(cid)
        b = base.get(own or "")
        if not b or b["verdict"] != "candidate":
            continue
        cls = own.split("/")[0]
        lv = {c.lower().replace(" ", ""): n for c, n in S.parse_split(ch["split"]).items()}
        n = lv.get(cls, 0)
        if not n:
            continue
        # Check the LAST act. A booster arriving at class level 20 is an Act III effect and is
        # correctly absent from Act II; reading Act II alone would flag every late grant. By Act
        # III the body has all twenty of its levels, so anything it ever gets should be recorded.
        got, late = set(ch["saves"]["III"]["boosters"]), arrives.get(own, {})
        for bo in b["boosters"]:
            if n >= late.get(bo, 1) and bo not in got:
                errors.append((cid, own, bo, n, late.get(bo, 1)))
        if b["concentration"] and not ch.get("concentration"):
            review.append((cid, own, ch["split"]))
    return errors, review


if __name__ == "__main__":
    d = json.load(open(sys.argv[1]))
    e, r = check(d["chassis"], d.get("keys", {}))
    print(f"{len(e)} omitted boosters (ERROR), {len(r)} concentration judgements (REVIEW)")
    for cid, key, bo, n, need in e:
        print(f"  ERROR  {cid}: {key} grants {bo} at {need}; body has {n} and omits it")
    for cid, key, sp in r:
        print(f"  REVIEW {cid}: {key} rides concentration, body says false — {sp}")
