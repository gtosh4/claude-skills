#!/usr/bin/env python3
"""What actually needs redoing, across every stage, as one machine-readable plan.

`--check` answers "is the seeds file current?". `--bases --check` answers the same for the base
profiles. `score_deps.py --ledger` answers "can every published body still be traced to a source?".
`render_ledger.py --selection` answers "which entries changed?". Each is correct and each is a
different command with a different output shape, so the only thing that ever combined them was a
person reading four terminals and deciding what to run.

This composes them. The point is not convenience: it is that the *dependency types are different*
and conflating them is what makes an incremental update expensive.

  * a subclass body moved      → re-sweep it, refresh its structural records, enumerate, score
  * a dip section moved        → re-enumerate its consumers; score only bodies that actually changed
  * a base profile moved       → re-enumerate consumers, crosscheck existing bodies, score exposures
  * the sweep brief moved      → re-sweep governed seeds; do NOT rescore unchanged results
  * a rubric moved             → rescore governed chassis; keep the seeds
  * renderer arithmetic moved  → rerender; author nothing
  * the prose template moved   → review the prose layer only

The last two schedule no model-authored work at all, and saying so explicitly is most of the
value: "something changed" is what turns a two-agent update into a full rebuild.

    scripts/work_plan.py --ledger assets/ledger-v6.json --against assets/ledger-v6.json
"""
import json, os, sys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                "listo-build", "scripts"))
import seed_index as SI                                        # noqa: E402
import score_deps as SD                                        # noqa: E402


def plan(seeds_path=None, bases_path=None, ledger=None, against=None):
    """The work plan. Every list is a work-list; an empty plan means an unchanged tree."""
    inv = SI.inventory()
    seeds = SI.load(seeds_path or os.path.join(ASSETS, "chassis-seeds.json"))
    rep = SI.audit(inv, seeds)

    bases_path = bases_path or os.path.join(ASSETS, "subclass-bases.json")
    bases = SI.load_bases(bases_path) if os.path.exists(bases_path) else {}
    brep = SI.audit_bases(inv, bases)

    # A subclass whose own text moved has to be re-swept before anything downstream about it means
    # anything, so it heads the plan and everything else about it is suppressed — exactly as
    # `audit` already suppresses its builds' score and enumeration buckets.
    sweep = sorted(set(rep["unseeded"]) | set(rep["drifted"]) | set(rep["rules"]))
    base_work = sorted(set(brep["unseeded"]) | set(brep["drifted"]) | set(brep["rules"]))

    out = {
        "sweep": sweep,
        "sweep_stale_keys": rep["stale"],
        "bases": base_work,
        "bases_stale_keys": brep["stale"],
        "enumerate": sorted(set(rep["unenumerated"]) | set(rep["reenumerate"])),
        "score": sorted(set(rep["unscored"]) | set(rep["rescore"])),
        "retained": [],
        "unmapped": [],
        "untraceable": [],
        "prose": {"recheck": False, "reason": None},
        "renderer_only": False,
    }

    if ledger:
        total, bad = SD.audit_ledger(ledger)
        out["untraceable"] = [{"chassis": cid, "split": split, "why": why}
                              for cid, split, why in bad]
        scheduled = set(out["score"])
        with open(ledger) as fh:
            chassis = json.load(fh).get("chassis", {})
        import merge_results as MR
        by_addr = MR.existing_ids(seeds, chassis)
        mapped = {cid for cid in by_addr.values()}
        untraceable = {b[0] for b in bad}
        # "Retained" is a real output, not a footnote. An incremental plan that only ever names
        # work reads as if the rest of the roster were unaccounted for, and the whole risk of
        # incremental execution is silently narrowing the published field. Every chassis lands in
        # exactly one of retained / scheduled / untraceable / unmapped, and the four sum to the
        # roster — which is the only way to see that nothing fell out.
        out["retained"] = sorted(cid for cid in chassis
                                 if cid in mapped and cid not in scheduled
                                 and cid not in untraceable)
        # A published body with no `address` and no seed proposal matching its id cannot be
        # scheduled *or* retained honestly: nothing knows which build it came from. Naming them is
        # the fail-closed answer; guessing a mapping would silently rename bodies on the next merge.
        out["unmapped"] = sorted(cid for cid in chassis
                                 if cid not in mapped and cid not in untraceable)
        out["total_chassis"] = total

    if ledger and against:
        import render_ledger as RL
        with open(ledger) as fh:
            new = json.load(fh)
        with open(against) as fh:
            old = json.load(fh)
        sel = RL.selection_report(new, old)
        out["selection"] = {k: sel[k] for k in ("added", "removed", "partner_changed",
                                                "evidence_moved", "prose_missing")}
        moved = (sel["added"] or sel["removed"] or sel["partner_changed"]
                 or sel["evidence_moved"] or sel["prose_missing"])
        out["prose"] = {"recheck": bool(moved),
                        "reason": "selection moved" if moved else None}

    # Nothing authored is scheduled, but something in the tree still changed: that is a rerender,
    # and saying so is what stops it being mistaken for a rebuild.
    out["renderer_only"] = not any((out["sweep"], out["bases"], out["enumerate"], out["score"],
                                    out["untraceable"], out["prose"]["recheck"]))
    return out


def summary(p):
    lines = [f"sweep:      {len(p['sweep'])}",
             f"bases:      {len(p['bases'])}",
             f"enumerate:  {len(p['enumerate'])}",
             f"score:      {len(p['score'])}",
             f"retained:   {len(p['retained'])}",
             f"untraceable:{len(p['untraceable'])}",
             f"unmapped:   {len(p['unmapped'])}"]
    if p.get("selection"):
        s = p["selection"]
        lines.append(f"prose:      {len(s['added'])} new, {len(s['partner_changed'])} repartnered, "
                     f"{len(s['evidence_moved'])} evidence moved, {len(s['removed'])} removed")
    if p["renderer_only"]:
        lines.append("nothing authored is scheduled — this is a rerender")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seeds")
    ap.add_argument("--bases-file")
    ap.add_argument("--ledger", help="the candidate or published ledger to account for")
    ap.add_argument("--against", help="the previously published ledger, for the prose diff")
    ap.add_argument("-o", "--out", help="write the plan here as well as summarising it")
    a = ap.parse_args()
    try:
        p = plan(a.seeds, a.bases_file, a.ledger, a.against)
    except (SI.SeedError, SD.DepsError) as e:
        sys.exit(str(e))
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(p, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    else:
        json.dump(p, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    print(summary(p), file=sys.stderr)


if __name__ == "__main__":
    main()
