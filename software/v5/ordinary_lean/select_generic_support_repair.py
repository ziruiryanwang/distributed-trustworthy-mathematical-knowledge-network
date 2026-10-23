"""One file-only successor: complete the selected retained helper census.

No product source/build/checker changes. The failed operation stays immutable.
Root must separately launch this exact finite selection after review.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
OLD = "ordinary-generic-contribution-actual-01"
NEW = "ordinary-generic-contribution-actual-02"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=True,
                     separators=(",", ":"), allow_nan=False).encode("ascii")
    with path.open("xb") as stream: stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def main():
    if Path.cwd() != ROOT or (LOCAL/NEW).exists(): raise ValueError("FRESH_CANONICAL_REPAIR")
    selection_path, plan_path = LOCAL/(OLD+".selection.json"), LOCAL/(OLD+".plan.json")
    if sha(selection_path) != "6d626a1b4c9d926385c114f3ca0ed6928c893ad857431dadf45bdcef7219b1fa" or \
       sha(plan_path) != "e3f6f49fdd29c76c5c7df9470d22847baf26993c4dd72a9efdaee74efb6eda24":
        raise ValueError("EXACT_PREDECESSOR_SELECTION")
    selection, plan = json.loads(selection_path.read_bytes()), json.loads(plan_path.read_bytes())
    for relative, expected in selection["sources"].items():
        if sha(ROOT/relative) != expected: raise ValueError("PRODUCT_SOURCE_CHANGED:"+relative)
    for path, expected in selection["runtime_pins"].items():
        if sha(Path(path)) != expected: raise ValueError("RETAINED_INPUT_CHANGED:"+path)
    added = {}
    directory = LOCAL/"ordinary-deferred-import-helpers-01/lean-build"
    for suffix in ("ir", "ir.sig", "olean", "olean.private", "olean.server"):
        path = directory/("ConstructExportCommand."+suffix)
        if str(path) in selection["runtime_pins"]: raise ValueError("NOT_MISSING_SUPPORT")
        added[str(path)] = sha(path)
    selection["runtime_pins"].update(added)
    # One explicitly selected repair; account the failed attempt separately.
    # This is not permission to renew an old running worker or retry forever.
    plan.update(wall_seconds=175, cpu_seconds=97)
    fresh_plan = LOCAL/(NEW+".plan.json")
    fresh_plan_pin = save(fresh_plan, plan)
    selection["runtime_pins"].pop(str(plan_path))
    selection["runtime_pins"][str(fresh_plan)] = fresh_plan_pin
    selection["name"] = NEW
    selection["argv"][selection["argv"].index("--plan")+1] = str(fresh_plan)
    selection["argv"][selection["argv"].index("--plan-sha256")+1] = fresh_plan_pin
    selection["limits"].update(cpu_seconds=112, wall_seconds=205)
    own = Path(__file__).resolve().relative_to(ROOT).as_posix()
    selection["sources"][own] = sha(Path(__file__).resolve())
    if len(selection["runtime_pins"]) > 256: raise ValueError("SUPPORT_CENSUS_BOUND")
    pin = save(LOCAL/(NEW+".selection.json"), selection)
    print(json.dumps({"selection": NEW, "sha256": pin, "added_support": added,
                      "runtime": "NOT_STARTED"}, sort_keys=True))


if __name__ == "__main__":
    main()
