#!/usr/bin/env python3
"""Merge a fused base/grants pass into `subclass-bases.json`, and say what changed.

`listo-base` already reads `base-brief.md`, `grants-brief.md`, the axis rubrics and its assigned
class sections. Then a second pass read the same four things again to correct one field group. The
reconstruction is the expensive part and it was paid for twice, so the fused pass returns both
halves of what it already knows:

```jsonc
{"bases":   {"ranger/Gloom Stalker": {"verdict": "candidate", "scores": [...], "prof": [...]}},
 "arrives": {"ranger/Gloom Stalker": {"wis": 7, "int": 7}}}
```

Two explicit top-level maps, keyed the same way, in one response. Not a per-record representation
a later pass has to reinterpret — that is how the two halves drift apart in the first place.

**`arrives` must be present for every assigned key, even when it is `{}`.** An omitted map is an
evidence gap: nobody can tell "this subclass grants nothing after level 1" from "the agent did not
look". The empty object says the first; absence says nothing at all, and a dip that fails to reach
a grant it does reach is an understated score on the heaviest-weighted axis in the model.

    scripts/merge_bases.py out-*.json --into assets/subclass-bases.json -o candidate.json
"""
import json, os, sys, argparse, copy

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)),
                                "listo-build", "scripts"))
import seed_index as SI                                        # noqa: E402


def read_pass(paths):
    """`({key: base}, {key: arrives}, [problem, ...])` across one or more agent responses."""
    bases, arrives, problems = {}, {}, []
    for path in paths:
        with open(path) as fh:
            doc = json.load(fh)
        name = os.path.basename(path)
        for half in ("bases", "arrives"):
            if not isinstance(doc.get(half), dict):
                problems.append(f"{name}: no `{half}` object — the fused pass returns both maps, "
                                f"and an absent one is a gap rather than an empty answer")
        if problems:
            continue
        for k, rec in doc["bases"].items():
            if k in bases:
                problems.append(f"{name}: {k} was already returned by another response")
                continue
            bases[k] = rec
            if k not in doc["arrives"]:
                problems.append(f"{name}: {k} has no `arrives` entry — write `{{}}` to say the "
                                f"subclass adds nothing after level 1")
                continue
            arrives[k] = doc["arrives"][k]
        for k in doc["arrives"]:
            if k not in doc["bases"]:
                problems.append(f"{name}: arrives names {k}, which the response does not score")
    return bases, arrives, problems


def merge(paths, into=None, expect=None):
    """Returns `(candidate document, report)`. Raises on anything that would enter unvalidated."""
    new_bases, new_arrives, problems = read_pass(paths)
    if problems:
        raise SI.SeedError("the pass is not mergeable:\n  " + "\n  ".join(problems))
    if expect:
        missing = sorted(set(expect) - set(new_bases))
        extra = sorted(set(new_bases) - set(expect))
        if missing or extra:
            raise SI.SeedError(
                (f"{len(missing)} assigned subclass(es) missing: {missing[:5]}\n" if missing else "")
                + (f"{len(extra)} unassigned subclass(es) returned: {extra[:5]}" if extra else ""))

    doc = {"provenance": "", "bases": {}, "arrives": {}}
    if into:
        with open(into) as fh:
            doc = json.load(fh)
    doc = copy.deepcopy(doc)
    old_bases = doc.setdefault("bases", {})
    old_arrives = doc.setdefault("arrives", {})

    report = {"added": [], "changed": {}, "unchanged": [],
              "arrives_added": [], "arrives_changed": {}}
    for k, rec in sorted(new_bases.items()):
        before = old_bases.get(k, {})
        # `src` and `base_deps` are the cache stamps, not judgements: carry them and let
        # `--bases --stamp` set them, so merging a pass never silently marks it current.
        after = {f: v for f, v in rec.items() if f not in ("src", "base_deps")}
        for f in ("src", "base_deps"):
            if f in before:
                after[f] = before[f]
        fields = sorted(f for f in set(before) | set(after)
                        if f not in ("src", "base_deps") and before.get(f) != after.get(f))
        old_bases[k] = after
        if not before:
            report["added"].append(k)
        elif fields:
            report["changed"][k] = fields
        else:
            report["unchanged"].append(k)

        was = old_arrives.get(k)
        now = new_arrives[k]
        if now:
            old_arrives[k] = now
        else:
            old_arrives.pop(k, None)
        if was is None and now:
            report["arrives_added"].append(k)
        elif was != now and (was or now):
            report["arrives_changed"][k] = [was, now]

    # Validate the *merged* document, not the incoming fragment: a record is only safe once it
    # sits beside the rest, because `arrives` is checked against the profile it annotates and a
    # dupe's `dupe_of` is checked against the whole key set.
    with_tmp = os.path.join(os.path.dirname(into or ASSETS) or ".", ".merge_bases_check.json")
    with open(with_tmp, "w") as fh:
        json.dump(doc, fh)
    try:
        SI.load_bases(with_tmp)
    finally:
        os.remove(with_tmp)
    return doc, report


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("responses", nargs="+", help="the fused pass's JSON responses")
    ap.add_argument("--into", default=os.path.join(ASSETS, "subclass-bases.json"))
    ap.add_argument("--expect", metavar="KEY,KEY|@FILE",
                    help="the subclasses the pass was assigned; a mismatch fails rather than "
                         "silently narrowing the inventory")
    ap.add_argument("-o", "--out", help="candidate path; omit for a report-only run")
    a = ap.parse_args()
    expect = None
    if a.expect:
        expect = (open(a.expect[1:]).read().split("\n") if a.expect.startswith("@")
                  else a.expect.split(","))
        expect = [x.strip() for x in expect if x.strip()]
    try:
        doc, report = merge(a.responses, a.into, expect)
    except SI.SeedError as e:
        sys.exit(str(e))
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(doc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    print(f"{len(report['added'])} added, {len(report['changed'])} changed, "
          f"{len(report['unchanged'])} unchanged; arrives: "
          f"{len(report['arrives_added'])} added, {len(report['arrives_changed'])} changed",
          file=sys.stderr)
    for k, fields in sorted(report["changed"].items()):
        print(f"  {k}: {', '.join(fields)}", file=sys.stderr)


if __name__ == "__main__":
    main()
