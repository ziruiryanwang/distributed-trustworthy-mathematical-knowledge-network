"""Only the unfinished inert controls after preserved controls01 failure.

Reuses pinned frozen helper definitions, never its main or execute methods.
No positive preparation, product import, native/process/network/DB operation.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from types import ModuleType


FROZEN_TEST = "software/v5/ordinary_current_operator_kit/control_tests.py"
FROZEN_SHA = "91b40f6273d27a842d2ed4d7496a2dca3de39373b84dea58a3d9a664b55644ab"


def main():
    if not (os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
        raise ValueError("REMAINING_ISOLATED_WINDOWS_PYTHON_REQUIRED")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root, output = args.source_root, args.output
    if not (root.is_absolute() and output.is_absolute() and root.is_dir() and
            output.parent.is_dir() and not output.exists()):
        raise ValueError("REMAINING_SELECTED_FRESH_PATHS")
    started, cpu = time.monotonic(), time.process_time()
    path = root / FROZEN_TEST
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != FROZEN_SHA:
        raise ValueError("REMAINING_FROZEN_TEST_PIN")
    frozen = ModuleType("_frozen_operator_control_helpers")
    frozen.__file__ = str(path)
    # __name__ differs from __main__; frozen main/Controls.execute never run.
    exec(compile(raw, str(path), "exec", dont_inherit=True), frozen.__dict__)

    sources = {name: (root / frozen.PREFIX / name).read_bytes() for name in frozen.SOURCE_PINS}
    frozen.need(all(frozen.digest(sources[name]) == pin for name, pin in frozen.SOURCE_PINS.items()), "SOURCE_PINS")
    mapping = json.loads(sources["compatibility.json"])
    profile_raw = (root / frozen.PACKAGE / "PROFILE.json").read_bytes()
    frozen.need(frozen.digest(profile_raw) == frozen.CURRENT, "ACTUAL_PROFILE_PIN")
    selected_inputs = {root / frozen.PREFIX / name: dict(bytes=len(data), sha256=frozen.digest(data))
                       for name, data in sources.items()}
    selected_inputs[root / frozen.PACKAGE / "PROFILE.json"] = dict(bytes=len(profile_raw), sha256=frozen.CURRENT)
    for name, pin in mapping["direct_sources"].items():
        selected_inputs[root / frozen.PACKAGE / name] = pin
    raws = {}
    for label, (relative, size, sha) in frozen.FIXTURES.items():
        data = (root / relative).read_bytes()
        frozen.need(len(data) == size and frozen.digest(data) == sha, "FIXTURE_PIN:" + label)
        raws[label] = data
        selected_inputs[root / relative] = dict(bytes=size, sha256=sha)
    selected_inputs[path] = dict(bytes=len(raw), sha256=FROZEN_SHA)
    frozen.need(len(selected_inputs) == 63, "REMAINING_INPUT_CENSUS")

    output.mkdir()
    with frozen.inert_boundary(set(selected_inputs), output) as opened:
        controls = frozen.Controls(root, output, raws, sources, json.loads(profile_raw), mapping)
        request = controls.contribute()
        unwrapped = controls.doc("receive")["result"]
        frozen.need(unwrapped.get("operation") == "receive" and
                    unwrapped.get("ok") is not True and "profile_sha256" not in unwrapped,
                    "ACTUAL_UNWRAPPED_REPORT_SHAPE")
        request["parent_report"] = controls.fixture(unwrapped)
        controls.run(request, "KIT_PARENT_SUCCESS")
        controls.group("unwrapped-report-refusal-corrected-expectation")

        # These ten variants are the still-unexecuted tail of frozen execute().
        # No earlier successful preparation or completed rejection is repeated.
        variants = []
        def variant(error, change):
            request = controls.contribute()
            change(request)
            variants.append((request, error))
        variant("KIT_EXPLICIT_LOCAL_SOURCE_APPROVAL", lambda r: r.update(approve_local_source=False))
        variant("KIT_EXPLICIT_LOCAL_PROJECT_APPROVAL", lambda r: r.update(approve_local_project=False))
        variant("KIT_PROJECT_APPROVAL_FIELDS", lambda r: r.pop("approve_local_project"))
        def remove_project(request):
            del request["project_authoring"], request["approve_local_project"]
        variant("KIT_FRONTIER_REQUIRES_PROJECT", remove_project)
        variant("KIT_DUPLICATE_TARGET", lambda r: r["acquired"][0].update(target_indices=[0, 0]))
        variant("KIT_INTEGER", lambda r: r["acquired"][0].update(target_indices=[1]))
        variant("KIT_DUPLICATE_OUTPUT_NAME", lambda r: r["output_names"].append(deepcopy(r["output_names"][0])))
        variant("KIT_DUPLICATE_TARGET_NAME", lambda r: r["acquired"].append(deepcopy(r["acquired"][0])))
        variant("KIT_OUTPUT_IS_ACQUIRED", lambda r: r.update(output_names=[controls.doc("receive")["result"]["target"]["name"]]))
        variant("KIT_INPUT_PIN", lambda r: r["source"].update(sha256="0"*64))
        for request, error in variants:
            controls.run(request, error)
        controls.group("remaining-approval-target-selection-and-source-pin-refusals")

        frozen.need(controls.positives == 0 and controls.negatives == 11, "REMAINING_CASE_CENSUS")
        for selected_path, pin in selected_inputs.items():
            data = selected_path.read_bytes()
            frozen.need(pin == dict(bytes=len(data), sha256=frozen.digest(data)), "INPUT_CHANGED:" + str(selected_path))
        controls.group("selected-input-integrity-and-no-side-effects")
        frozen.need(time.monotonic()-started < 60 and time.process_time()-cpu < 30, "COOPERATIVE_ALLOWANCE")
        result = dict(schema="DMKN_CURRENT_OPERATOR_REMAINING_CONTROLS_V1", ok=True,
                      groups=controls.groups, positive_preparations=0, refused_preparations=controls.negatives,
                      selected_input_count=len(selected_inputs), frozen_test_sha256=FROZEN_SHA,
                      prior_run="current-operator-controls01", prior_run_status="FAILED_PRESERVED",
                      commands_executed=0, protected_state_opened=False, product_modules_imported=False,
                      native_artifacts_checked=False, mathematical_acceptance=False,
                      interpretation="ONLY_CORRECTED_REFUSAL_AND_UNEXECUTED_TAIL_NOT_A_REPLACEMENT_RUN",
                      reads=sorted({path for path, mode in opened if "r" in mode}),
                      wall_seconds=time.monotonic()-started, controller_cpu_seconds=time.process_time()-cpu)
        frozen.write(output / "RESULT.json", frozen.canonical(result))
    print(frozen.canonical(result).decode("utf-8"))


if __name__ == "__main__":
    main()
