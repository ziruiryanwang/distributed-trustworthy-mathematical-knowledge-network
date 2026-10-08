"""Independent actual-native negative and demand controls, not certification.

Root selects the binary, interpreter, fixture and this source under its bounded
Job supervisor. This harness imports no implementation/emitter code: mutations
operate on the exact independently inspected fusion request. Every input and
response is retained. NEED is exit zero, and is never interpreted as acceptance.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import subprocess
import time

FIXTURE_SHA = "81475a04de77c7a65077d2b0722d297c533a8c21441ca8dfc2881a3c9833b5e5"
BASE = "28b3e7c40f06795f1ac5aa7b9ddd356f15f47e02e58f58836ac5dcde9f8d52d7"
MODULE = "4b09f9821e27c9edcc7528e3db5b91e0d21c3637a012951361ef6260802ae293"
BODY = "0b5f265dfb01a1ed1232443bfdc79c5217be78664b15ee9d12e01fa77d2e6e55"
CONDITIONAL = "CONDITIONAL_MODULE_EXTENSION_ONLY"
CORRESPONDENCE = "STRUCTURAL_CORRESPONDENCE_ONLY_UNVERIFIED_HASHES_AND_PREMISES"
DECL_TAGS = {"def", "thm", "opaque", "inductive", "constructor", "recursor",
             "axiom", "quot", "moduleImportDef", "moduleImportOpaque", "moduleImportTheorem"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def names(rows):
    """Independent native name-DAG reconstruction, preserving numeric parts."""
    found = {0: ()}
    for row in rows:
        if "in" not in row:
            continue
        index = row["in"]
        assert index not in found
        tag = "str" if "str" in row else "num"
        record = row[tag]
        found[index] = found[record["pre"]] + (("s" if tag == "str" else "n", record["str" if tag == "str" else "i"]),)
    return found


def full(owner, *parts):
    return tuple(("s", part) for part in ("DMKN", "Mod", owner, *parts))


def declaration(request, wanted):
    inventory = names(request["rows"])
    matches = []
    for position, row in enumerate(request["rows"]):
        if "inductive" in row:
            group = row["inductive"]
            for field, tag in (("types", "inductive"), ("ctors", "constructor"), ("recs", "recursor")):
                for record in group[field]:
                    if inventory[record["name"]] == wanted:
                        matches.append((position, tag, record))
            continue
        for tag in DECL_TAGS.intersection(row):
            if inventory[row[tag]["name"]] == wanted:
                matches.append((position, tag, row[tag]))
    assert len(matches) == 1, ("EXACT_DECLARATION", wanted, len(matches))
    return matches[0]


def selected_group(request, owner, *parts):
    wanted = [["s", part] for part in parts]
    matches = [(i, g) for i, g in enumerate(request["correspondence"]["groups"])
               if g["owner"] == owner and any(d["name"] == wanted for d in g["descriptor"]["declarations"])]
    assert len(matches) == 1
    return matches[0]


def controls(original):
    fold_position, fold_tag, fold = declaration(original, full(BASE, "CommonsV5", "fold"))
    theorem_position, theorem_tag, theorem = declaration(original, full(MODULE, "CommonsV5", "fusion"))
    assert fold_tag == "def" and theorem_tag == "thm"
    fold_group_position, fold_group = selected_group(original, BASE, "CommonsV5", "fold")
    assert fold_group["imported"] is True
    assert len(fold_group["descriptor"]["declarations"]) == 1
    assert fold_group["descriptor"]["declarations"][0]["value_hash"] == BODY
    local_group_position, local_group = selected_group(original, MODULE, "CommonsV5", "fusion")
    assert local_group["imported"] is False

    missing = copy.deepcopy(original)
    header = {key: copy.deepcopy(fold[key]) for key in ("name", "levelParams", "type", "hints")}
    header["bodyHash"] = list(bytes.fromhex(BODY))
    missing["rows"][fold_position] = {"moduleImportDef": header}
    yield "missing-fold-body", missing, {"status": "NEED", "exit": 0,
        "demand": {"kind": "NeedBody", "native_name_index": fold["name"], "body_hash": BODY}}

    # A fresh call restores exactly the original row, not a forged success flag.
    recovered = copy.deepcopy(missing)
    recovered["rows"][fold_position] = copy.deepcopy(original["rows"][fold_position])
    assert recovered == original
    yield "exact-body-recovery", recovered, {"status": CONDITIONAL, "exit": 0,
        "checked_local_names": [theorem["name"]], "premises": len(original["premises"])}

    false_proof = copy.deepcopy(original)
    false_proof["rows"][theorem_position]["thm"]["value"] = theorem["type"]
    yield "false-new-proof", false_proof, {"status": "REFUSED", "exit": 2,
        "reason": "NATIVE_CHECKER_PANIC", "stderr_contains": "self.def_eq(u, v)"}

    mismatch = copy.deepcopy(original)
    mismatch["correspondence"]["groups"][local_group_position]["descriptor"]["declarations"][0]["type"] = ["sort", ["zero"]]
    yield "descriptor-native-mismatch", mismatch, {"status": "REFUSED", "exit": 2,
        "reason": "NATIVE_CHECKER_PANIC", "stderr_contains": "CORRESPONDENCE_DECLARATION_TYPE"}

    skip = copy.deepcopy(original)
    foundation = [p for p in skip["premises"] if p["authority"]["kind"] == "foundation"]
    assert len(foundation) == 1
    foundation[0]["names"].append(theorem["name"])
    yield "malicious-local-skip", skip, {"status": "REFUSED", "exit": 2,
        "reason": "CORRESPONDENCE_EXACT_IMPORT_ROLE"}

    partial = copy.deepcopy(original)
    partial["mode"] = "conditional_module"
    del partial["correspondence"]
    _, _, leaf = declaration(original, full(BASE, "CommonsV5", "Tree", "leaf"))
    groups = [p for p in partial["premises"] if leaf["name"] in p["names"]]
    assert len(groups) == 1 and len(groups[0]["names"]) == 4
    groups[0]["names"].remove(leaf["name"])
    yield "partial-inductive-role-unbound-diagnostic", partial, {"status": "REFUSED", "exit": 2,
        "reason": "NATIVE_CHECKER_PANIC", "stderr_contains": "PARTIAL_IMPORTED_INDUCTIVE_GROUP"}

    absent = copy.deepcopy(original)
    del absent["rows"][fold_position]
    del absent["correspondence"]["groups"][fold_group_position]
    groups = [p for p in absent["premises"] if fold["name"] in p["names"]]
    assert len(groups) == 1 and groups[0]["names"] == [fold["name"]]
    absent["premises"].remove(groups[0])
    yield "missing-fold-declaration", absent, {"status": "NEED", "exit": 0,
        "demand": {"kind": "NeedDeclaration", "native_name_index": fold["name"]}}


def write_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True)
    parser.add_argument("--binary-sha", required=True)
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()
    binary, fixture, output = map(Path, (args.binary, args.fixture, args.evidence))
    assert all(p.is_absolute() for p in (binary, fixture, output)) and not output.exists()
    assert binary.stat().st_size <= 64 * 1024 * 1024 and digest(binary) == args.binary_sha
    assert fixture.stat().st_size <= 1024 * 1024 and digest(fixture) == FIXTURE_SHA
    original = json.loads(fixture.read_bytes())
    assert original["schema"] == "DMKN_V5_NATIVE_PREFLIGHT_V1"
    assert original["mode"] == "corresponding_module" and original["module"] == MODULE
    assert original["permitted_axioms"] == []
    cases = list(controls(original))
    assert len(cases) == 7
    output.mkdir()
    results = []
    for label, request, expected in cases:
        dest = output / label
        dest.mkdir()
        input_path = dest / "input.json"
        write_json(input_path, request)
        write_json(dest / "EXPECTED.json", expected)
        start = time.monotonic()
        response = None
        returncode = None
        error = None
        passed = False
        try:
            with (dest / "stdout.txt").open("xb") as stdout, (dest / "stderr.txt").open("xb") as stderr:
                run = subprocess.run([str(binary), str(input_path)], cwd=str(output),
                    stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=30, check=False)
            returncode = run.returncode
            assert (dest / "stdout.txt").stat().st_size <= 65536
            assert (dest / "stderr.txt").stat().st_size <= 1024 * 1024
            response = json.loads((dest / "stdout.txt").read_bytes())
            diagnostic = (dest / "stderr.txt").read_text(encoding="utf-8", errors="replace")
            assert returncode == expected["exit"], "EXIT"
            assert response.get("status") == expected["status"], "STATUS"
            assert response.get("mathematical_admission") is False, "NO_ADMISSION_AUTHORITY"
            assert response.get("certificate_verification_performed") is False, "NO_CERTIFICATE_AUTHORITY"
            for key in ("reason", "demand", "checked_local_names"):
                if key in expected:
                    assert response.get(key) == expected[key], key
            if "stderr_contains" in expected:
                assert expected["stderr_contains"] in diagnostic, "EXACT_REFUSAL_BOUNDARY"
            if expected["status"] == CONDITIONAL:
                assert response["module"] == MODULE
                assert response["unverified_premise_count"] == expected["premises"]
                corr = response["correspondence"]
                assert corr["status"] == CORRESPONDENCE
                assert corr["hash_verification_performed"] is False
                assert corr["mathematical_admission"] is False
            passed = True
        except Exception as exc:
            error = {"type": type(exc).__name__, "message": str(exc)[:4096]}
        record = {"label": label, "pass": passed, "expected": expected,
            "input_sha256": digest(input_path), "input_bytes": input_path.stat().st_size,
            "exit_code": returncode, "response": response, "error": error,
            "wall_seconds": time.monotonic() - start,
            "stdout_sha256": digest(dest / "stdout.txt"), "stderr_sha256": digest(dest / "stderr.txt")}
        write_json(dest / "RESULT.json", record)
        results.append(record)
    pins_unchanged = digest(binary) == args.binary_sha and digest(fixture) == FIXTURE_SHA
    report = {"schema": "DMKN_V5_INDEPENDENT_NATIVE_CONTROLS_V1", "results": results,
        "all_pass": pins_unchanged and all(r["pass"] for r in results), "pins_unchanged": pins_unchanged,
        "binary_sha256": args.binary_sha, "fixture_sha256": FIXTURE_SHA,
        "mathematical_admission": False,
        "scope": "ACTUAL_NATIVE_DEMAND_AND_REFUSAL_NOT_CRYPTOGRAPHIC_CERTIFICATION"}
    write_json(output / "RESULT.json", report)
    print(json.dumps(report, sort_keys=True))
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
