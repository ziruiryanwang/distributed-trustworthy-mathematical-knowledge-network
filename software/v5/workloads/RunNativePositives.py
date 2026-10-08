"""Seven distinct real native checks over one selected exported workload.

This is owner test orchestration, not a public verifier. The outer selected Job
bounds the entire process tree. A zero native exit is never sufficient: require
the exact mode-specific status and disclosed unresolved premises.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import time


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binary", required=True); p.add_argument("--binary-sha", required=True)
    p.add_argument("--fixtures", required=True); p.add_argument("--output", required=True)
    a = p.parse_args()
    binary, fixtures, out = Path(a.binary), Path(a.fixtures), Path(a.output)
    if not all(path.is_absolute() for path in (binary, fixtures, out)) or out.exists():
        raise ValueError("EXPLICIT_FRESH_PATHS")
    if hashlib.sha256(binary.read_bytes()).hexdigest() != a.binary_sha:
        raise ValueError("BINARY_PIN")
    cases = {"all-new": fixtures / "all-new.json", "foundation-check": fixtures / "foundation-check.json"}
    for label in ("base", "fusion", "fold_map", "fusion_map", "project_summary"):
        cases[label] = fixtures / label / "native.json"
    out.mkdir()

    def check(item):
        label, path = item
        raw = path.read_bytes()
        request = json.loads(raw)
        if request["permitted_axioms"] != []: raise ValueError("NO_AXIOMS_SELECTED")
        dest = out / label
        dest.mkdir()
        start = time.monotonic()
        with (dest/"stdout.txt").open("xb") as stdout, (dest/"stderr.txt").open("xb") as stderr:
            run = subprocess.run([str(binary), str(path)], cwd=str(fixtures), stdin=subprocess.DEVNULL,
                                 stdout=stdout, stderr=stderr, timeout=30, check=False)
        response = (dest/"stdout.txt").read_bytes()
        if len(response) > 65536: raise ValueError("RESPONSE_LIMIT")
        result = json.loads(response)
        expected = ("ALL_DECLARATIONS_CHECKED_UNDER_EXPLICIT_AXIOMS" if request["mode"] == "all_new"
                    else "CONDITIONAL_MODULE_EXTENSION_ONLY")
        passed = run.returncode == 0 and result.get("status") == expected
        passed &= result.get("certificate_verification_performed") is False
        passed &= result.get("mathematical_admission") is False
        if request["mode"] == "corresponding_module":
            corr = result.get("correspondence") or {}
            passed &= corr.get("status") == "STRUCTURAL_CORRESPONDENCE_ONLY_UNVERIFIED_HASHES_AND_PREMISES"
            passed &= corr.get("hash_verification_performed") is False
            passed &= result.get("unverified_premise_count") == len(request["premises"])
            passed &= result.get("module") == request["module"]
            expected_locals = sum(len(g["descriptor"]["declarations"]) for g in
                                  request["correspondence"]["groups"] if not g["imported"])
            passed &= len(result.get("checked_local_names", [])) == expected_locals
        record = {"label": label, "input_sha256": hashlib.sha256(raw).hexdigest(),
                  "input_bytes": len(raw), "exit_code": run.returncode, "pass": bool(passed),
                  "wall_seconds": time.monotonic()-start, "result": result}
        with (dest/"RESULT.json").open("x", encoding="utf-8") as stream:
            json.dump(record, stream, sort_keys=True)
        return record

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, cases.items()))
    report = {"schema": "DMKN_V5_NATIVE_POSITIVES_V1", "results": results,
              "all_pass": all(r["pass"] for r in results), "mathematical_admission": False,
              "scope": "ACTUAL_NATIVE_CHECKS_NOT_CRYPTOGRAPHIC_MODULE_CERTIFICATION"}
    with (out/"RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True)
    print(json.dumps(report))
    return 0 if report["all_pass"] else 1


if __name__ == "__main__": raise SystemExit(main())
