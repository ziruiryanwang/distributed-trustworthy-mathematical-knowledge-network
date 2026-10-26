"""Two changed-boundary negative calls using a saved public request as test data.

Only the selected native worker is invoked, never an owner or admission API.
Mutated requests are explicitly unwarranted negative fixtures, not new content
identities or admissible evidence. All outputs are fresh and failures retained.
"""
from copy import deepcopy
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
LEAN = ROOT / "software/runtime/lean-4.34.0-windows"
HELPER = ROOT / "software/v5/ordinary_fair_search/assemble.py"
HELPER_SHA = "9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30"
START, CPU = time.monotonic(), time.process_time()


def need(ok, code):
    if not ok:
        raise ValueError(code)


def check():
    need(time.monotonic()-START < 100 and time.process_time()-CPU < 15,
         "EXACT_NEGATIVE_ORIGINAL_ALLOWANCE")


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "profile-sha256", "export", "request-sha256",
                "inventory-sha256", "anchor-plan-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "EXACT_NEGATIVE_CONTEXT")
    raw = HELPER.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == HELPER_SHA, "EXACT_NEGATIVE_HELPER")
    spec = importlib.util.spec_from_file_location("_exact_negative_files", HELPER)
    H = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(HELPER), "exec"), H.__dict__)
    H.ordinary(HELPER)
    package = H.ordinary(Path(args.package), directory=True)
    saved = H.ordinary(Path(args.export), directory=True)
    output = H.ordinary(Path(args.output), directory=True, fresh=True)
    need(all(path.is_relative_to(LOCAL) for path in (package, saved, output)) and
         not output.is_relative_to(package) and not package.is_relative_to(output) and
         not output.is_relative_to(saved) and not saved.is_relative_to(output),
         "EXACT_NEGATIVE_PATHS")
    profile, profile_pin = H.read_json(package/"PROFILE.json", args.profile_sha256, check)
    request, request_pin = H.read_json(saved/"request.json", args.request_sha256, check)
    inputs = {"request.json": request_pin}
    for filename, expected in (("inventory.json", args.inventory_sha256),
                               ("anchor-plan.json", args.anchor_plan_sha256)):
        inputs[filename] = H.pin(saved/filename, check)
        need(inputs[filename]["sha256"] == expected, "EXACT_NEGATIVE_INPUT_PIN")
    need(request["anchor_id"] == "" and len(request["units"]) == 10,
         "EXACT_NEGATIVE_COLD_REQUEST")
    for logical, pin in profile["files"].items():
        H.relative(logical)
        need(H.pin(package/logical, check) == pin, "EXACT_NEGATIVE_SUPPORT_PIN")
    output.mkdir()
    def text_name(encoded):
        return ".".join(bytes(item[1]["$bytes"]).decode("utf-8") for item in encoded)
    cases = []
    descriptor = deepcopy(request)
    singleton = next(unit for unit in descriptor["units"]
                     if unit[1][0] == 0 and text_name(unit[1][1]) == "Membership.mem")
    old_hint = singleton[1][5]
    singleton[1][5] = [0] if old_hint != [0] else [1]
    cases.append(("descriptor-row-disagreement", descriptor,
                  "MATCHED_DESCRIPTOR_INVENTORY_MISMATCH"))
    partial = deepcopy(request)
    group = next(unit for unit in partial["units"] if unit[1][0] == 3 and
                 any(row[1] == 4 and text_name(row[0]) == "List.Mem" for row in unit[2]))
    recursor = next(row for row in group[2] if row[1] == 6)
    recursor[0] = [[0, {"$bytes": list(part.encode("ascii"))}]
                  for part in ("List", "Mem", "DMKNMissingRecursorNegative")]
    cases.append(("partial-installed-group", partial, "PARTIAL_INSTALLED_GROUP"))
    results = []
    for label, altered, expected in cases:
        check()
        directory = output/label
        directory.mkdir()
        H.fresh_bytes(directory/"request.json", H.canonical(altered))
        module_name = text_name(altered["module_name"])
        argv = [sys.executable, "-I", "-S", "-B", str(package/"module_worker.py"),
                str(LEAN/"bin/lean.exe"), str(package/"module/OrdinaryModule.lean"),
                str(package/"authoring/helpers"), str(LEAN), str(saved/"inventory.json"),
                str(directory/"request.json"), str(saved/"anchor-plan.json"),
                str(directory/(module_name+".olean")), str(directory/"native-report.json")]
        H.fresh_bytes(directory/"COMMAND.json", H.canonical({"argv": argv,
            "expected_refusal": expected, "fixture_authority": "NONE_NEGATIVE_TEST_ONLY"}))
        with (directory/"stdout.txt").open("xb") as out, (directory/"stderr.txt").open("xb") as err:
            code = subprocess.call(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=out,
                                   stderr=err, creationflags=subprocess.CREATE_NO_WINDOW)
        for filename in ("stdout.txt", "stderr.txt"):
            need((directory/filename).stat().st_size <= H.MIB, "EXACT_NEGATIVE_LOG_BOUND")
        diagnostics = (directory/"stdout.txt").read_text(encoding="utf-8") + \
                      (directory/"stderr.txt").read_text(encoding="utf-8")
        need(code != 0 and expected in diagnostics and
             not (directory/"native-report.json").exists() and
             not (directory/"native-report.json.pending").exists(),
             "EXACT_NEGATIVE_WRONG_OUTCOME:"+label)
        results.append({"case": label, "exit_code": code, "expected_refusal": expected})
    for logical, pin in profile["files"].items():
        need(H.pin(package/logical, check) == pin, "EXACT_NEGATIVE_SUPPORT_CHANGED")
    need(H.pin(package/"PROFILE.json", check) == profile_pin, "EXACT_NEGATIVE_PROFILE_CHANGED")
    for filename, pin in inputs.items():
        need(H.pin(saved/filename, check) == pin, "EXACT_NEGATIVE_INPUT_CHANGED")
    result = {"status": "PASS_TWO_NATIVE_REFUSALS", "cases": results,
              "wall_seconds": time.monotonic()-START,
              "claim": "CHANGED_MATCH_BOUNDARY_ONLY_NO_MATHEMATICAL_ACCEPTANCE"}
    raw = H.canonical(result)
    H.fresh_bytes(output/".RESULT.pending", raw)
    need(H.pin(output/".RESULT.pending", check) ==
         {"bytes": len(raw), "sha256": H.digest(raw)}, "EXACT_NEGATIVE_READBACK")
    check()
    H.ordinary(output/"RESULT.json", fresh=True)
    (output/".RESULT.pending").rename(output/"RESULT.json")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
