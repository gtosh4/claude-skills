#!/usr/bin/env python3
"""One validated file per chassis, so a scoring turn cannot lose a batch.

`listo-score` used to return its whole batch as one final message. That message was both the data
and the thing subject to the turn's output limit, so a batch that ran long was lost entirely and
had to be hand-split into halves to fit. The fix is not a bigger message: it is to stop treating
the message as the transport.

The no-write rule the spec used to carry existed to stop parallel agents colliding on shared
state, and that reason survives intact. An agent writes only inside its own assignment's result
directory, never the live ledger, and ids are still resolved centrally by `naming.py` afterwards.

    <run>/assignments/score-001.json          the manifest: addresses, splits, filenames
    <run>/results/score-001/<slug>--<hash>.json   one validated result per chassis
    <run>/results/score-001/*.json.tmp        interrupted work; never read as a result

A result is keyed by `(address, deps)` — the same staleness rule the rest of the pipeline uses,
not a separate immutability protocol. Every recorded dependency still matching means the result is
valid and is skipped; one having moved means it is stale and may be replaced, but only after the
new candidate validates.

    scripts/result_store.py manifest --run DIR --assignment score-001 --addresses @FILE
    scripts/result_store.py put      --run DIR --assignment score-001 \
                                     --address "cleric/Tempest:lockdown" --record cand.json
    scripts/result_store.py status   --run DIR --assignment score-001
"""
import json, os, re, sys, argparse, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                "listo-build", "scripts"))
import score_deps as SD                                        # noqa: E402
import seed_index as SI                                        # noqa: E402
from scoring import KEYS, SAV_IDX, REACH, DAMAGE_TYPES         # noqa: E402

FORMAT = 1
ACTS = ("I", "II", "III")

# The fields the scoring pass owns. `skills` is deliberately absent: the evidence passes author
# the modifier map, and a scoring result that invented one would be a second authority on it.
REQUIRED = ("split", "reach", "concentration", "saves", "types", "scores",
            "note", "strength", "wants")


class StoreError(Exception):
    pass


def _require(cond, msg):
    if not cond:
        raise StoreError(msg)


def filename(address):
    """A filesystem-safe locator for one build address.

    The readable half is a slug, which is lossy: two headings that differ only in punctuation
    normalise to the same words, and one result would silently overwrite the other. The digest
    half is taken over the exact address, so distinct addresses cannot collide however they slug.
    The document's own `address` field stays authoritative — this is a filename, not a key.
    """
    slug = re.sub(r"[^a-z0-9]+", "_", address.lower()).strip("_")[:60]
    return f"{slug}--{hashlib.sha256(address.encode()).hexdigest()[:10]}.json"


def _paths(run, assignment):
    return (os.path.join(run, "assignments", f"{assignment}.json"),
            os.path.join(run, "results", assignment))


def write_manifest(run, assignment, entries, pak_evidence=None):
    """`entries` is `[(address, split), ...]`. Agents never invent a filename; this hands them out.

    The manifest is also where the dependency set is fixed for the assignment, so every result in
    it was checked against the same source state rather than against whatever the tree looked
    like when each individual chassis happened to be authored.
    """
    man_path, res_dir = _paths(run, assignment)
    os.makedirs(os.path.dirname(man_path), exist_ok=True)
    os.makedirs(res_dir, exist_ok=True)
    inv, seen = SI.inventory(), set()
    builds = []
    for address, split in entries:
        _require(address not in seen, f"duplicate address in assignment: {address!r}")
        seen.add(address)
        doc = SD.deps_for(address, split, (pak_evidence or {}).get(address, ()), inv=inv)
        builds.append({"address": address, "split": split, "file": filename(address),
                       "deps": doc["deps"], "selection_provenance": doc["selection_provenance"]})
    man = {"format": FORMAT, "assignment": assignment, "builds": builds}
    _atomic(man_path, man)
    return man


def read_manifest(run, assignment):
    man_path, _ = _paths(run, assignment)
    _require(os.path.exists(man_path), f"no manifest at {man_path}")
    with open(man_path) as fh:
        man = json.load(fh)
    _require(man.get("format") == FORMAT,
             f"{man_path}: format {man.get('format')!r}, expected {FORMAT}")
    return man


def _atomic(path, doc):
    """Write through a temporary sibling and rename. A reader never sees a half-written file."""
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, path)


def validate_record(address, rec):
    """The score-only checks, mirroring `scoring.py` for exactly the fields this pass authors.

    `scoring.validate_chassis` is the full contract and runs at merge time, once the evidence
    passes have supplied `skills`. Running it here would either reject every score result for a
    map the scoring pass is not allowed to author, or tempt someone into inventing a placeholder
    one — and a placeholder skills map is the invisible under-score the whole model refuses.
    """
    for f in REQUIRED:
        _require(f in rec, f"{address}: missing `{f}`")
    _require(rec["reach"] in REACH, f"{address}: unknown reach {rec['reach']!r}")
    _require(isinstance(rec["concentration"], bool),
             f"{address}: `concentration` must be true or false")
    _require(isinstance(rec["types"], list) and rec["types"], f"{address}: `types` is empty")
    for t in rec["types"]:
        _require(t in DAMAGE_TYPES, f"{address}: unknown damage type {t!r}")
    SI.check_split(rec["split"], address)
    for act in ACTS:
        _require(act in rec["scores"], f"{address}: `scores` missing act {act}")
        _require(act in rec["saves"], f"{address}: `saves` missing act {act}")
        row = rec["scores"][act]
        _require(len(row) == len(KEYS),
                 f"{address} {act}: scores has {len(row)} entries, expected {len(KEYS)}")
        _require(row[SAV_IDX] is None,
                 f"{address} {act}: index {SAV_IDX} (saves) must be null — it is derived")
        for i, v in enumerate(row):
            if i == SAV_IDX:
                continue
            _require(isinstance(v, int) and 0 <= v <= 5,
                     f"{address} {act}: {KEYS[i]} is {v!r}, expected an integer 0-5")
    for f in ("note", "strength", "wants"):
        _require(isinstance(rec[f], str) and rec[f].strip(), f"{address}: `{f}` is empty")


def put(run, assignment, address, rec, man=None):
    """Validate one candidate record and promote it atomically. Returns its path.

    An existing *valid* result is left alone — re-authoring one that nothing invalidated would
    discard a judgement for no reason. A stale one is replaced only once the new candidate has
    passed every check, so a failed re-score cannot destroy the result it was meant to improve.
    """
    man = man or read_manifest(run, assignment)
    entry = next((b for b in man["builds"] if b["address"] == address), None)
    _require(entry, f"{address!r} is not in assignment {assignment!r}")
    _require(rec.get("split") == entry["split"],
             f"{address}: record splits {rec.get('split')!r}, assignment says {entry['split']!r}")
    validate_record(address, rec)
    _, res_dir = _paths(run, assignment)
    path = os.path.join(res_dir, entry["file"])
    if os.path.exists(path):
        with open(path) as fh:
            old = json.load(fh)
        if not SD.stale(old.get("deps", {}), entry["deps"]):
            return path                        # already valid; nothing invalidated it
    os.makedirs(res_dir, exist_ok=True)
    _atomic(path, {"format": FORMAT, "assignment": assignment, "address": address,
                   "deps": entry["deps"],
                   "selection_provenance": entry["selection_provenance"],
                   "record": rec})
    return path


def read_results(run, assignment, man=None):
    """`({address: document}, [problem, ...])` for the assignment's *final* files only.

    `.tmp` files are interrupted work and are never read as results. A file whose embedded
    address disagrees with the filename it was found under is a problem, not a result: the
    filename is derived from the address, so the two disagreeing means something wrote by hand.
    """
    man = man or read_manifest(run, assignment)
    _, res_dir = _paths(run, assignment)
    by_file = {b["file"]: b for b in man["builds"]}
    out, problems = {}, []
    for name in sorted(os.listdir(res_dir)) if os.path.isdir(res_dir) else []:
        if not name.endswith(".json"):
            continue                            # `.json.tmp` lands here and is skipped
        entry = by_file.get(name)
        if entry is None:
            problems.append(f"{name}: not an address in {assignment}")
            continue
        with open(os.path.join(res_dir, name)) as fh:
            doc = json.load(fh)
        if doc.get("address") != entry["address"]:
            problems.append(f"{name}: holds address {doc.get('address')!r}")
            continue
        out[entry["address"]] = doc
    return out, problems


def status(run, assignment):
    """What a resuming turn needs: what is done, what moved, and what is left."""
    man = read_manifest(run, assignment)
    done, problems = read_results(run, assignment, man)
    _, res_dir = _paths(run, assignment)
    valid, stale, missing = [], [], []
    for b in man["builds"]:
        doc = done.get(b["address"])
        if doc is None:
            missing.append(b["address"])
        elif SD.stale(doc.get("deps", {}), b["deps"]):
            stale.append(b["address"])
        else:
            valid.append(b["address"])
    interrupted = sorted(n for n in (os.listdir(res_dir) if os.path.isdir(res_dir) else [])
                         if n.endswith(".tmp"))
    return {"assignment": assignment, "result_directory": res_dir,
            "completed": len(valid), "remaining": len(missing) + len(stale),
            "valid": valid, "stale": stale, "missing": missing,
            "interrupted": interrupted, "problems": problems}


def _addresses(arg):
    if arg.startswith("@"):
        with open(arg[1:]) as fh:
            return [l.strip() for l in fh if l.strip()]
    return [x for x in arg.split(",") if x]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("manifest", help="create an assignment's manifest and result directory")
    m.add_argument("--run", required=True)
    m.add_argument("--assignment", required=True)
    m.add_argument("--addresses", required=True, metavar="ADDR,ADDR|@FILE",
                   help="build addresses; @file takes one per line, which is the form that can "
                        "carry the comma-bearing subclass headings")
    m.add_argument("--seeds", default=None,
                   help="seeds file the splits come from (default: the published one)")

    p = sub.add_parser("put", help="validate one candidate record and promote it")
    p.add_argument("--run", required=True)
    p.add_argument("--assignment", required=True)
    p.add_argument("--address", required=True)
    p.add_argument("--record", required=True, help="path to the candidate JSON, or `-` for stdin")

    s = sub.add_parser("status", help="what is done, what is stale, what is left")
    s.add_argument("--run", required=True)
    s.add_argument("--assignment", required=True)

    a = ap.parse_args()
    try:
        if a.cmd == "manifest":
            seeds = SI.load(a.seeds or os.path.join(
                os.path.dirname(HERE), "assets", "chassis-seeds.json"))
            builds = SI.builds(seeds)
            entries = []
            for addr in _addresses(a.addresses):
                _require(addr in builds, f"{addr!r} is not a build address")
                entries.append((addr, builds[addr]["split"]))
            man = write_manifest(a.run, a.assignment, entries)
            print(f"{len(man['builds'])} builds in {a.assignment}", file=sys.stderr)
            json.dump(man, sys.stdout, indent=2, ensure_ascii=False)
        elif a.cmd == "put":
            rec = json.load(sys.stdin if a.record == "-" else open(a.record))
            print(put(a.run, a.assignment, a.address, rec))
        else:
            json.dump(status(a.run, a.assignment), sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    except (StoreError, SD.DepsError, SI.SeedError) as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
