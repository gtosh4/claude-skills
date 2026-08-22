#!/usr/bin/env python3
"""What a scoring assignment costs to *read*, split into its fixed and per-agent parts.

The sweep has a measured cost model — `total ≈ 77k + 16.9k × agents` — and agent count is the dial
because of the shape of it. Scoring has never had the equivalent, so every argument about how to
make it cheaper has been an argument about a number nobody had.

This measures the half that can be measured without running anything: the bytes on disk, and a
token estimate derived from them. It deliberately does **not** report a byte count as a token
count. The estimate is bytes/4, which is a rule of thumb for English prose and is wrong for JSON,
tables and code — so both numbers are printed and the estimate is labelled as one.

The half it cannot measure is the agent's own output and its tool-call overhead, which only a real
run produces. Fit the model from two runs at different agent counts:

    total ≈ fixed + per_agent × agents

where this script's `shared` is the term multiplied by agent count, and `assigned` is the term
that is paid once however the work is divided. If the shared term dominates, fewer and fatter
agents is the lever, and evidence packets are not.

    scripts/read_cost.py --agents 4
    scripts/read_cost.py --run RUN --assignment score-001
"""
import json, os, sys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
BUILD = os.path.join(os.path.dirname(os.path.dirname(HERE)), "listo-build")
REFS = os.path.join(BUILD, "references")
sys.path.insert(0, HERE)
import seed_index as SI                                        # noqa: E402
import score_deps as SD                                        # noqa: E402

# Exactly what `scoring-brief.md` tells a scoring agent to read in full, in order, plus the brief
# itself. Every agent pays this, which is why it is the term worth attacking first.
SHARED = [os.path.join(REFS, "scoring-model.md"),
          os.path.join(REFS, "axis-rubrics.md"),
          os.path.join(REFS, "gates.md"),
          os.path.join(ASSETS, "ledger-schema.md"),
          os.path.join(ASSETS, "scoring-brief.md")]

BYTES_PER_TOKEN = 4      # a rule of thumb for prose, not a measurement


def size(path):
    return os.path.getsize(path)


def shared_cost():
    return [{"path": os.path.relpath(path, BUILD), "bytes": size(path)} for path in SHARED]


def assigned_cost(addresses, splits):
    """Per-address class-section bytes, deduplicated the way one agent's context would be.

    A scoring agent reads at-a-glance and subclass sections, not whole class files. Two chassis in
    the same assignment that share a class share that read, so the honest per-agent figure is the
    union of their sections rather than the sum — which is also the reason class-coherent batching
    is worth anything.
    """
    inv = SI.inventory()
    seen, per = {}, {}
    for addr, split in zip(addresses, splits):
        want = {}
        for cls, _lv, display in SD.split_parts(split):
            if cls not in inv:
                continue
            glance, blocks = SI.sections(cls)
            want[f"{cls}.md#at-a-glance"] = len(glance)
            head = SD.resolve_subclass(cls, display, inv) if display else None
            if head:
                want[f"{cls}.md#{head}"] = len(blocks[head])
        per[addr] = sum(want.values())
        seen.update(want)
    return {"unique_bytes": sum(seen.values()), "sections": len(seen),
            "naive_sum_bytes": sum(per.values()), "per_address": per}


def report(addresses, splits, agents):
    shared = shared_cost()
    shared_bytes = sum(x["bytes"] for x in shared)
    assigned = assigned_cost(addresses, splits)
    return {
        "note": "bytes are measured; tokens are bytes/4 and are an ESTIMATE, not a measurement",
        "shared": {"files": shared, "bytes": shared_bytes,
                   "tokens_estimate": shared_bytes // BYTES_PER_TOKEN},
        "assigned": {"chassis": len(addresses),
                     "unique_bytes": assigned["unique_bytes"],
                     "unique_tokens_estimate": assigned["unique_bytes"] // BYTES_PER_TOKEN,
                     "saved_by_sharing_sections_bytes":
                         assigned["naive_sum_bytes"] - assigned["unique_bytes"],
                     "sections": assigned["sections"]},
        "agents": agents,
        "read_total_bytes": shared_bytes * agents + assigned["unique_bytes"],
        "read_total_tokens_estimate":
            (shared_bytes * agents + assigned["unique_bytes"]) // BYTES_PER_TOKEN,
        "unmeasured": ["agent output tokens", "tool-call overhead", "retries and corrections"],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run", help="a run directory, to cost one real assignment")
    ap.add_argument("--assignment")
    ap.add_argument("--agents", type=int, default=1,
                    help="how many agents each pay the shared read")
    ap.add_argument("--seeds")
    a = ap.parse_args()
    try:
        if a.run and a.assignment:
            import result_store as RS
            man = RS.read_manifest(a.run, a.assignment)
            addresses = [b["address"] for b in man["builds"]]
            splits = [b["split"] for b in man["builds"]]
        else:
            seeds = SI.load(a.seeds or os.path.join(ASSETS, "chassis-seeds.json"))
            builds = SI.builds(seeds)
            addresses, splits = list(builds), [b["split"] for b in builds.values()]
        rep = report(addresses, splits, a.agents)
    except (SI.SeedError, SD.DepsError) as e:
        sys.exit(str(e))
    rep["assigned"].pop("per_address", None)
    json.dump(rep, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    s, g = rep["shared"], rep["assigned"]
    print(f"shared read {s['bytes']} bytes (~{s['tokens_estimate']}t) × {a.agents} agents; "
          f"assigned {g['unique_bytes']} bytes (~{g['unique_tokens_estimate']}t) across "
          f"{g['chassis']} chassis; total read ~{rep['read_total_tokens_estimate']}t estimated",
          file=sys.stderr)


if __name__ == "__main__":
    main()
