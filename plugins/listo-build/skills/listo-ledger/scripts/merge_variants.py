#!/usr/bin/env python3
"""Write the chosen splits back into the seeds, which is the step the search was missing.

`enumerate_splits.py` searches the split space and ranks what it finds. Nothing consumed the
result: the seeds kept the sweep's guess, `--check` went on reporting every build as never
enumerated, and the most consequential decision in the pipeline was made by the stage the SKILL
says is least qualified to make it. This is the other half.

It does not choose. A `listo-variant` pass chooses — which variants are different bodies, which
niche each expresses, which are the same body twice — because the ranking cannot: across the v7
run the four kept variants of a subclass were separated by a median of 0.95 points, and the axes
that would separate them are pinned at the ceiling by design. This merges what that pass decided,
and refuses anything it did not.

Three guards, in order:

* **Provenance.** Every split must be one the search produced for that subclass, or the one the
  sweep already had. A split from nowhere is a body nobody evaluated, which is the one thing
  neither stage can catch downstream.
* **Naming.** Chassis ids are proposals from agents that cannot see each other, so they collide —
  twelve times in the v7 sweep alone. `naming.assign` resolves them deterministically.
* **Forced builds.** `assets/forced-builds.json` is applied last and overwrites, because a forced
  body exists precisely where the search cannot reach it.

    scripts/merge_variants.py v*-*.json --into assets/chassis-seeds.json -o candidate.json
"""
import json, os, sys, re, argparse, copy, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, HERE)
import seed_index as SI                                        # noqa: E402
import naming                                                  # noqa: E402

# `enumerate_splits.py` used to append the level-1 class to the split string itself, which
# `check_split` cannot parse. The script no longer does, but a variants file produced before that
# fix still carries it, and so does any selection copied verbatim out of one.
_FIRST = re.compile(r"\s*\[[^\]]*first\]\s*$")
BUILD_FIELDS = ("chassis", "split", "peak", "peak_axis", "breadth", "why")


def clean(split):
    return _FIRST.sub("", split).strip()


def read_selection(paths):
    """`({key: record}, [problem, ...])` across the selection pass's per-class files."""
    out, problems = {}, []
    for path in sorted(paths):
        name = os.path.basename(path)
        with open(path) as fh:
            doc = json.load(fh)
        for key, rec in doc.items():
            if key in out:
                problems.append(f"{name}: {key} was already returned by another file")
                continue
            if not isinstance(rec.get("builds"), dict) or not rec["builds"]:
                problems.append(f"{name}: {key} has no builds")
                continue
            out[key] = rec
    return out, problems


def merge(paths, seeds_path, variants_path, forced_path=None):
    """Returns `(candidate seeds document, report)`. Raises rather than writing a body blind."""
    chosen, problems = read_selection(paths)
    with open(seeds_path) as fh:
        doc = copy.deepcopy(json.load(fh))
    seeds = doc["seeds"]
    with open(variants_path) as fh:
        variants = json.load(fh)["variants"]

    for key, rec in sorted(chosen.items()):
        if key not in seeds:
            problems.append(f"{key}: not a seeded subclass")
            continue
        allowed = {clean(v["split"]) for v in variants.get(key, [])}
        allowed |= {b["split"] for b in (seeds[key].get("builds") or {}).values()}
        for niche, b in sorted(rec["builds"].items()):
            split = clean(b.get("split", ""))
            if split not in allowed:
                problems.append(f"{key}:{niche}: split came from neither the search nor the "
                                f"sweep — {split!r}")
            if niche not in SI.NICHES:
                problems.append(f"{key}:{niche}: not one of the seven niches")
    if problems:
        raise SI.SeedError("the selection is not mergeable:\n  " + "\n  ".join(problems))

    report = {"subclasses": len(chosen), "builds": 0, "kept_sweep": 0, "searched": 0,
              "niches": collections.Counter(), "renamed": 0, "forced": []}
    for key, rec in sorted(chosen.items()):
        old = seeds[key].get("builds") or {}
        new = {}
        for niche, b in sorted(rec["builds"].items()):
            split = clean(b["split"])
            was = next((x for x in old.values() if x["split"] == split), None)
            entry = {"chassis": b.get("chassis") or (was or {}).get("chassis"),
                     "split": split, "why": b.get("why", "")}
            # `peak` and `breadth` are the sweep's one-act triage guesses, and the schema requires
            # them. A searched split has none: this pass authors no scores, deliberately. Where the
            # body is not the sweep's they are inherited from the sweep's build for the same
            # subclass and flagged `peak_inherited`, because they are then a number about a
            # different body.
            #
            # That is safe only while the roster is promoted whole. `peak` is read by nothing but
            # `--promote --limit`'s bar and tie-breaks, and rationing on an inherited peak would be
            # rationing on a guess about the wrong split. `--promote --limit` must not be trusted
            # on a roster carrying these until the scoring pass has replaced them with real rungs.
            src = was or next(iter(old.values()), None)
            for f in ("peak", "peak_axis", "breadth"):
                if src and f in src:
                    entry[f] = src[f]
            if was is None and src is not None:
                entry["peak_inherited"] = True
            new[niche] = entry
            report["builds"] += 1
            report["niches"][niche] += 1
            if b.get("keep_sweep_reason"):
                report["kept_sweep"] += 1
            else:
                report["searched"] += 1
        seeds[key]["builds"] = new
        if rec.get("uncertain"):
            seeds[key]["uncertain"] = rec["uncertain"]

    if forced_path and os.path.exists(forced_path):
        with open(forced_path) as fh:
            forced = json.load(fh)["builds"]
        for addr, b in sorted(forced.items()):
            key, niche = addr.rsplit(":", 1)
            if key not in seeds:
                raise SI.SeedError(f"forced build {addr}: {key} is not a seeded subclass")
            entry = {f: b[f] for f in BUILD_FIELDS if f in b}
            SI.check_split(entry["split"], addr)
            seeds[key].setdefault("builds", {})[niche] = entry
            report["forced"].append(addr)

    # Proposals from agents that cannot see each other collide; `naming` is the resolver that
    # already exists for it, and it is order-independent so the same selection always lands the
    # same ids. Forced builds go in first so a hand-picked name is the one that survives a tie.
    # A forced body's name is hand-picked, so it is seeded into `taken` and left out of the
    # resolution entirely. Passing it through would find its own name already taken and rename it.
    pinned = {tuple(a.rsplit(":", 1)) for a in report["forced"]}
    bodies, where = [], []
    for key in sorted(seeds):
        for niche in sorted(seeds[key].get("builds") or {}):
            if (key, niche) not in pinned:
                bodies.append((seeds[key]["builds"][niche]["chassis"], key))
                where.append((key, niche))
    taken = [seeds[k]["builds"][n]["chassis"] for k, n in pinned]
    ids = naming.assign(bodies, taken)
    for i, (key, niche) in enumerate(where):
        if seeds[key]["builds"][niche]["chassis"] != ids[i]:
            report["renamed"] += 1
        seeds[key]["builds"][niche]["chassis"] = ids[i]
    return doc, report


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("selections", nargs="+", help="the variant pass's per-class JSON files")
    ap.add_argument("--into", default=os.path.join(ASSETS, "chassis-seeds.json"))
    ap.add_argument("--variants", required=True, help="the variants file the pass chose from")
    ap.add_argument("--forced", default=os.path.join(ASSETS, "forced-builds.json"))
    ap.add_argument("-o", "--out", help="candidate path; omit for a report-only run")
    a = ap.parse_args()
    try:
        doc, report = merge(a.selections, a.into, a.variants, a.forced)
        if a.out:
            with open(a.out, "w") as fh:
                json.dump(doc, fh, indent=1, ensure_ascii=False)
                fh.write("\n")
            SI.load(a.out)                    # the merged file must load, not just the fragments
    except SI.SeedError as e:
        sys.exit(str(e))
    print(f"{report['subclasses']} subclasses, {report['builds']} builds "
          f"({report['searched']} searched, {report['kept_sweep']} kept from the sweep); "
          f"{report['renamed']} ids resolved; forced {', '.join(report['forced']) or 'none'}",
          file=sys.stderr)
    print("  niches: " + ", ".join(f"{k} {v}" for k, v in sorted(report["niches"].items())),
          file=sys.stderr)


if __name__ == "__main__":
    main()
