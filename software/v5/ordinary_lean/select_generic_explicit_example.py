"""One owner-source-only successor of the preserved elaboration refusal.

No checker, API, wrapper, acquired meaning or target statement changes. The
caller spells method parameters explicitly instead of relying on higher-order
implicit inference through its new transparent definition.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
OLD = "ordinary-generic-contribution-actual-02"
NEW = "ordinary-generic-contribution-actual-03"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True,
                     separators=(",", ":"), allow_nan=False).encode("ascii")
    with path.open("xb") as stream: stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def main():
    if Path.cwd() != ROOT or (LOCAL/NEW).exists(): raise ValueError("FRESH_CANONICAL_SOURCE_SELECTION")
    selection_path, plan_path = LOCAL/(OLD+".selection.json"), LOCAL/(OLD+".plan.json")
    if sha(selection_path) != "6322c9a1c918a60dabf5127e9120424f6da4509cbcc0cab1c79cfdf26870b16e" or \
       sha(plan_path) != "bd057824a33cea8435172143b1cd80bc83afb8296f3ba7657dcab8b7916ae176":
        raise ValueError("EXACT_PREDECESSOR_SELECTION")
    selection, plan = json.loads(selection_path.read_bytes()), json.loads(plan_path.read_bytes())
    for relative, expected in selection["sources"].items():
        if sha(ROOT/relative) != expected: raise ValueError("PRODUCT_SOURCE_CHANGED:"+relative)
    for path, expected in selection["runtime_pins"].items():
        if sha(Path(path)) != expected: raise ValueError("RETAINED_INPUT_CHANGED:"+path)
    plan.update(wall_seconds=165, cpu_seconds=90)
    plan["source_body"] = "software/v5/ordinary_lean/examples/GenericContributionExplicitBody.lean"
    selection["sources"][plan["source_body"]] = sha(ROOT/plan["source_body"])
    fresh_plan = LOCAL/(NEW+".plan.json")
    fresh_plan_pin = save(fresh_plan, plan)
    selection["runtime_pins"].pop(str(plan_path))
    selection["runtime_pins"][str(fresh_plan)] = fresh_plan_pin
    selection["name"] = NEW
    selection["argv"][selection["argv"].index("--plan")+1] = str(fresh_plan)
    selection["argv"][selection["argv"].index("--plan-sha256")+1] = fresh_plan_pin
    selection["limits"].update(cpu_seconds=105, wall_seconds=195)
    own = Path(__file__).resolve().relative_to(ROOT).as_posix()
    selection["sources"][own] = sha(Path(__file__).resolve())
    pin = save(LOCAL/(NEW+".selection.json"), selection)
    print(json.dumps({"selection": NEW, "sha256": pin, "source_body": plan["source_body"],
                      "runtime": "NOT_STARTED"}, sort_keys=True))


if __name__ == "__main__":
    main()
