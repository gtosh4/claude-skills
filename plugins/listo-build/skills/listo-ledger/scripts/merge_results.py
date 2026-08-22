#!/usr/bin/env python3
"""Merge per-chassis scoring results into a candidate ledger, and say what changed.

The scoring pass writes one validated file per chassis; this is what turns a directory of them
into a ledger. It is deliberately not a dict update. Four things have to happen between the files
and a publishable ledger, and each of them has been the source of a real defect:

  * **coverage** — a missing address is a chassis that silently vanishes from the roster;
  * **identity** — parallel agents propose names blind to each other, so ids are resolved centrally
    by `naming.py` against the whole set at once, and an id already published stays put;
  * **completeness** — a scoring result carries no `skills` map, because the evidence passes author
    it. Merging into a live ledger keeps the map that is already there; a chassis that has never
    had one is reported as an evidence gap rather than rendered with a hole;
  * **change** — nothing is replaced silently. A field-level report says what moved, and the
    candidate is written beside the published ledger, never over it.

    scripts/merge_results.py --run DIR --into assets/ledger-v6.json -o candidate.json
"""
import json, os, sys, argparse, copy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                "listo-build", "scripts"))
import result_store as RS                                      # noqa: E402
import score_deps as SD                                        # noqa: E402
import seed_index as SI                                        # noqa: E402
import naming                                                  # noqa: E402
import scoring                                                 # noqa: E402

ASSETS = os.path.join(os.path.dirname(HERE), "assets")
# Fields a scoring result may write. `skills` and `redirect` are on the list but a *split* pass
# never carries them, so the `if f in rec` guard below is what keeps the evidence passes'
# authorship intact: a unified result overwrites the map it authored, a score-only result leaves
# the published one exactly where it was.
OWNED = ("split", "reach", "concentration", "saves", "types", "scores", "damage",
         "note", "strength", "wants", "uncertain", "meta", "skills", "redirect")
# `address` is written by this merger rather than authored, and is not in OWNED for that reason.


def assignments(run):
    d = os.path.join(run, "assignments")
    if not os.path.isdir(d):
        raise RS.StoreError(f"no assignments directory under {run}")
    return sorted(f[:-5] for f in os.listdir(d) if f.endswith(".json"))


def collect(run, names=None):
    """`({address: document}, [problem, ...], {address: manifest entry})` across assignments."""
    docs, problems, wanted = {}, [], {}
    for name in names or assignments(run):
        man = RS.read_manifest(run, name)
        got, probs = RS.read_results(run, name, man)
        problems += [f"{name}: {p}" for p in probs]
        for b in man["builds"]:
            if b["address"] in wanted:
                problems.append(f"{name}: {b['address']} is also in another assignment")
                continue
            wanted[b["address"]] = b
        for addr, doc in got.items():
            if addr in docs:
                problems.append(f"{name}: duplicate result for {addr}")
                continue
            moved = SD.stale(doc.get("deps", {}), wanted[addr]["deps"])
            if moved:
                problems.append(f"{name}: {addr} is stale ({', '.join(moved)})")
                continue
            docs[addr] = doc
    return docs, problems, wanted


def existing_ids(seeds, chassis=None):
    """`{address: published chassis id}`, best evidence first.

    A published record's own `address` is authoritative, because it is written by this merger and
    survives `naming.py` resolving a proposed name into a different one. The seeds file's
    `chassis` field is only the *proposal* the sweep wrote down, so it is a fallback and a weak
    one: measured against the v6 ledger, 78 of 298 published ids match a seed proposal and one
    body matches by split. Anything the two cannot map is left unmapped rather than guessed —
    handing a re-scored body a fresh id orphans every anchor and pairing that named the old one,
    and a wrong guess does that silently.
    """
    out = {}
    for cid, rec in (chassis or {}).items():
        if rec.get("address"):
            out[rec["address"]] = cid
    for addr, b in SI.builds(seeds).items():
        if addr not in out and b.get("chassis") and b["chassis"] in (chassis or {}):
            out[addr] = b["chassis"]
    return out


def diff(old, new):
    """Field-level differences between two chassis records, as `{field: [old, new]}`."""
    out = {}
    for f in sorted(set(old) | set(new)):
        if old.get(f) != new.get(f):
            out[f] = [old.get(f), new.get(f)]
    return out


def merge(run, into=None, names=None, seeds_path=None, partial=False):
    """Returns `(candidate ledger, report)`. Raises rather than publishing an incomplete roster."""
    seeds = SI.load(seeds_path or os.path.join(ASSETS, "chassis-seeds.json"))
    docs, problems, wanted = collect(run, names)
    missing = sorted(a for a in wanted if a not in docs)
    if problems:
        raise RS.StoreError("results are not mergeable:\n  " + "\n  ".join(problems))
    if missing and not partial:
        raise RS.StoreError(f"{len(missing)} assigned address(es) have no result:\n  "
                            + "\n  ".join(missing[:10]))

    ledger = {"chassis": {}}
    if into:
        with open(into) as fh:
            ledger = json.load(fh)
    ledger = copy.deepcopy(ledger)
    chassis = ledger.setdefault("chassis", {})

    known = existing_ids(seeds, chassis)
    fresh = [(a, docs[a]) for a in sorted(docs) if known.get(a) not in chassis]
    # Resolve every new body's name in one pass, against the ids already published, exactly as a
    # single scoring run would have. Bodies whose id is already in the ledger keep it.
    picked = naming.assign([(d["record"].get("proposed_id") or known.get(a) or "Chassis",
                             a.rsplit(":", 1)[0]) for a, d in fresh],
                           taken=tuple(chassis))
    ids = {a: known[a] for a in docs if known.get(a) in chassis}
    for i, (addr, _doc) in enumerate(fresh):
        ids[addr] = picked[i]

    report = {"run": run, "into": into, "merged": [], "added": [], "changed": {},
              "missing": missing, "evidence_gaps": []}
    for addr in sorted(docs):
        cid = ids[addr]
        rec = docs[addr]["record"]
        old = chassis.get(cid, {})
        new = dict(old)
        for f in OWNED:
            if f in rec:
                new[f] = rec[f]
        # The join key, written into the record itself. Without it the next merge has only the
        # sweep's proposed name to go on, and a name that `naming.py` had to resolve away leaves
        # the body looking new.
        new["address"] = addr
        if "skills" not in new:
            report["evidence_gaps"].append(addr)
        changed = diff(old, new)
        chassis[cid] = new
        report["merged"].append({"address": addr, "chassis": cid})
        if not old:
            report["added"].append(cid)
        elif changed:
            report["changed"][cid] = changed

    # Completeness is checked once, on the merged record, because that is the first point at
    # which a chassis is supposed to be whole. A scoring result on its own never is.
    if not report["evidence_gaps"]:
        for cid, c in chassis.items():
            scoring.validate_chassis(cid, c)
    return ledger, report


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run", required=True, help="the run directory holding assignments/results")
    ap.add_argument("--assignment", action="append",
                    help="merge only these assignments; repeatable (default: all in the run)")
    ap.add_argument("--into", help="the published ledger to merge on top of")
    ap.add_argument("--seeds", help="seeds file (default: the published one)")
    ap.add_argument("-o", "--out", help="candidate ledger path; omit for a report-only run")
    ap.add_argument("--report", help="write the change report here as well as to stderr")
    ap.add_argument("--partial", action="store_true",
                    help="report coverage without requiring every assigned address — for "
                         "inspecting a run in progress, never for publishing")
    a = ap.parse_args()
    try:
        ledger, report = merge(a.run, a.into, a.assignment, a.seeds, a.partial)
    except (RS.StoreError, SD.DepsError, SI.SeedError, scoring.ScoringError) as e:
        sys.exit(str(e))
    if a.out:
        RS._atomic(a.out, ledger)
    if a.report:
        RS._atomic(a.report, report)
    print(f"{len(report['merged'])} merged, {len(report['added'])} new, "
          f"{len(report['changed'])} changed, {len(report['missing'])} missing",
          file=sys.stderr)
    for cid, fields in sorted(report["changed"].items()):
        print(f"  {cid}: {', '.join(sorted(fields))}", file=sys.stderr)
    if report["evidence_gaps"]:
        print(f"{len(report['evidence_gaps'])} chassis have no `skills` map yet — run the "
              f"evidence passes before publishing", file=sys.stderr)


if __name__ == "__main__":
    main()
