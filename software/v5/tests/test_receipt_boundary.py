"""Independent actual relation-binding controls, never parent certification.

Uses one root-pinned, semantically repinned fusion request. Pure Python framing,
hashing and journal parsing here import no product codec/witness helpers. The
separate author vector suite covers canonical syntax and odd Merkle parity; this
suite does not duplicate those calls or the native algebra-negative campaign.
Root must select all inputs and run under the bounded process-tree supervisor.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import struct
import subprocess
import time

FOUNDATION_SHA = "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"
FOUNDATION_ID = "d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481"
SUCCESS = "BOUND_RELATION_NATIVE_ONLY_PENDING_PARENT_PROOF_VERIFICATION"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def tagged_hash(domain, value):
    tag, encoded = domain.encode("ascii"), canonical(value)
    frame = b"DMKN-V5-MODULE\0" + struct.pack(">I", len(tag)) + tag
    return hashlib.sha256(frame + struct.pack(">Q", len(encoded)) + encoded).hexdigest()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary(spec):
    nodes = [tagged_hash("group-leaf", {"index": i, "group": group})
             for i, group in enumerate(spec["groups"])]
    assert nodes
    while len(nodes) > 1:
        nodes = [tagged_hash("group-node", [nodes[i], nodes[min(i + 1, len(nodes) - 1)]])
                 for i in range(0, len(nodes), 2)]
    return {"schema": "DMKN_MODULE_SUMMARY_V1", "foundation": spec["foundation"],
            "policy": spec["policy"], "group_count": len(spec["groups"]), "group_root": nodes[0]}


def journal(raw):
    assert len(raw) == 216 and raw[:8] == b"DMKNM001"
    assert struct.unpack_from("<I", raw, 8)[0] == 1
    result = {"image": list(struct.unpack_from("<8I", raw, 12)),
              "foundation": raw[44:76].hex(), "policy": raw[76:108].hex(),
              "module": raw[108:140].hex(), "group_root": raw[140:172].hex(),
              "group_count": struct.unpack_from("<I", raw, 172)[0],
              "rank": struct.unpack_from("<Q", raw, 176)[0], "witness": raw[184:216].hex()}
    result["summary"] = {"schema": "DMKN_MODULE_SUMMARY_V1", **{key: result[key]
        for key in ("foundation", "policy", "group_root", "group_count")}}
    assert result["module"] == tagged_hash("module-spec", result["summary"])
    return result


def changed_hex(value):
    return ("1" if value[0] != "1" else "2") + value[1:]


def verify_fixture(request):
    assert set(request) == {"schema", "image", "rank", "local_spec", "rows", "parents", "bodies"}
    assert request["schema"] == "DMKN_CERTIFIED_MODULES_V1"
    assert request["rank"] == 1 and len(request["parents"]) == 1
    assert len(request["image"]) == 8
    seed = request["rows"][:413]
    assert hashlib.sha256(canonical(seed)).hexdigest() == FOUNDATION_SHA
    assert tagged_hash("owner-workload-foundation-candidate", seed) == FOUNDATION_ID
    spec = request["local_spec"]
    assert spec["foundation"] == FOUNDATION_ID
    assert len(spec["groups"]) == 1
    declarations = spec["groups"][0]["declarations"]
    assert len(declarations) == 1 and declarations[0]["kind"] == "theorem"
    assert declarations[0]["name"] == [["s", "CommonsV5"], ["s", "fusion"]]
    parent = journal(bytes(request["parents"][0]["journal"]))
    assert parent["image"] == request["image"] and parent["rank"] == 0
    assert parent["foundation"] == FOUNDATION_ID and parent["policy"] == spec["policy"]
    assert request["parents"][0]["openings"] and request["bodies"]
    for body in request["bodies"]:
        assert tagged_hash("body", {"universes": body["universes"], "expr": body["expression"]}) == body["digest"]


def cases(original):
    bad = copy.deepcopy(original)
    bad["rows"][0]["meta"]["exporter"]["name"] += "/independent-negative"
    yield "altered-adopted-foundation", bad, "exact adopted foundation bytes and identifier"

    bad = copy.deepcopy(original)
    bad["local_spec"]["policy"] = changed_hex(bad["local_spec"]["policy"])
    yield "wrong-local-policy", bad, "local spec schema/foundation/policy"

    # Recompute the parent ModuleID after changing its policy, so this reaches
    # the exact parent policy guard rather than an earlier journal-ID failure.
    bad = copy.deepcopy(original)
    raw = bytearray(bad["parents"][0]["journal"])
    raw[76] ^= 1
    changed_summary = {"schema": "DMKN_MODULE_SUMMARY_V1", "foundation": raw[44:76].hex(),
        "policy": raw[76:108].hex(), "group_root": raw[140:172].hex(),
        "group_count": struct.unpack_from("<I", raw, 172)[0]}
    raw[108:140] = bytes.fromhex(tagged_hash("module-spec", changed_summary))
    journal(bytes(raw))
    bad["parents"][0]["journal"] = list(raw)
    yield "wrong-parent-policy-valid-journal-shape", bad, "parent exact image/foundation/policy/distinct module"

    bad = copy.deepcopy(original)
    bad["image"][0] ^= 1
    yield "different-alleged-parent-image", bad, "parent exact image/foundation/policy/distinct module"

    bad = copy.deepcopy(original)
    bad["rank"] += 1
    yield "nonminimal-child-rank", bad, "strict exact parent rank"

    bad = copy.deepcopy(original)
    raw = bytearray(bad["parents"][0]["journal"])
    struct.pack_into("<Q", raw, 176, bad["rank"])
    bad["parents"][0]["journal"] = list(raw)
    yield "parent-rank-not-below-child", bad, "strict exact parent rank"

    bad = copy.deepcopy(original)
    body = bad["bodies"][0]
    replacement = ["sort", ["zero"]]
    assert tagged_hash("body", {"universes": body["universes"], "expr": replacement}) != body["digest"]
    body["expression"] = replacement
    yield "altered-computation-body", bad, "actual canonical body hash"

    bad = copy.deepcopy(original)
    bad["parents"].append(copy.deepcopy(bad["parents"][0]))
    yield "duplicate-parent-module", bad, "duplicate parent module"

    bad = copy.deepcopy(original)
    bad["premises"] = [{"all_local_declarations_verified": True}]
    yield "sender-role-override-is-not-an-input", bad, "unknown field `premises`"


def write(path, value):
    with path.open("xb") as stream:
        stream.write(canonical(value))


def validate_success(response, request):
    assert response["certificate_verification_performed"] is False
    assert response["pending_parent_statements"] == 1
    expected_summary = summary(request["local_spec"])
    assert response["summary"] == expected_summary
    assert response["module"] == tagged_hash("module-spec", expected_summary)
    assert response["rank"] == request["rank"]
    assert response["witness"] == tagged_hash("module-witness", request)
    decoded = journal(bytes(response["journal"]))
    assert decoded["image"] == request["image"]
    assert decoded["summary"] == expected_summary
    assert decoded["rank"] == request["rank"] and decoded["witness"] == response["witness"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True)
    parser.add_argument("--binary-sha", required=True)
    parser.add_argument("--fixture", required=True)
    parser.add_argument("--fixture-sha", required=True)
    parser.add_argument("--baseline-result", required=True)
    parser.add_argument("--baseline-sha", required=True)
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()
    binary, fixture, baseline, output = map(Path, (args.binary, args.fixture, args.baseline_result, args.evidence))
    assert all(p.is_absolute() for p in (binary, fixture, baseline, output)) and not output.exists()
    assert binary.stat().st_size <= 128 * 1024 * 1024 and digest(binary) == args.binary_sha
    assert fixture.stat().st_size <= 16 * 1024 * 1024 and digest(fixture) == args.fixture_sha
    original = json.loads(fixture.read_bytes())
    verify_fixture(original)
    # Root's fresh preparation already exercised the successful changed wrapper.
    # Audit its saved raw result rather than repeating that mathematical call.
    assert baseline.stat().st_size <= 65536 and digest(baseline) == args.baseline_sha
    previous = json.loads(baseline.read_bytes())
    assert previous["status"] == SUCCESS and previous["mathematical_admission"] is False
    validate_success(previous, original)
    selected = list(cases(original))
    assert len(selected) == 9
    output.mkdir()
    write(output / "RETAINED-SUCCESS-AUDIT.json", {
        "status": "PASS_EXACT_RETAINED_CONDITIONAL_RESULT_NOT_REEXECUTED",
        "baseline_sha256": args.baseline_sha, "fixture_sha256": args.fixture_sha,
        "pending_parent_statements": previous["pending_parent_statements"],
        "mathematical_admission": False, "certificate_verification_performed": False})
    results = []
    for label, request, expected_reason in selected:
        dest = output / label
        dest.mkdir()
        input_path = dest / "input.json"
        write(input_path, request)
        start = time.monotonic()
        response, returncode, error, passed = None, None, None, False
        try:
            with (dest / "stdout.txt").open("xb") as stdout, (dest / "stderr.txt").open("xb") as stderr:
                run = subprocess.run([str(binary), "check", str(input_path)], cwd=str(output),
                    stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=30, check=False)
            returncode = run.returncode
            assert (dest / "stdout.txt").stat().st_size <= 65536
            assert (dest / "stderr.txt").stat().st_size <= 1024 * 1024
            response = json.loads((dest / "stdout.txt").read_bytes())
            assert response.get("mathematical_admission") is False, "NEVER_CRYPTOGRAPHIC_ADMISSION"
            assert returncode == 2 and response["status"] == "REFUSED", "EXACT_REFUSAL"
            if expected_reason.startswith("unknown field"):
                assert expected_reason in response.get("reason", ""), "UNKNOWN_ROLE_FIELD_REFUSAL"
            else:
                assert response.get("reason") == expected_reason, "EXACT_BINDING_REFUSAL"
            passed = True
        except Exception as exc:
            error = {"type": type(exc).__name__, "message": str(exc)[:4096]}
        record = {"label": label, "pass": passed, "expected_reason": expected_reason,
            "input_sha256": digest(input_path), "input_bytes": input_path.stat().st_size,
            "exit_code": returncode, "response": response, "error": error,
            "wall_seconds": time.monotonic() - start,
            "stdout_sha256": digest(dest / "stdout.txt"), "stderr_sha256": digest(dest / "stderr.txt")}
        write(dest / "RESULT.json", record)
        results.append(record)
    unchanged = (digest(binary) == args.binary_sha and digest(fixture) == args.fixture_sha
                 and digest(baseline) == args.baseline_sha)
    report = {"schema": "DMKN_V5_INDEPENDENT_RELATION_BINDING_CONTROLS_V1", "results": results,
        "all_pass": unchanged and all(item["pass"] for item in results), "pins_unchanged": unchanged,
        "binary_sha256": args.binary_sha, "fixture_sha256": args.fixture_sha,
        "baseline_sha256": args.baseline_sha, "retained_success_not_reexecuted": True,
        "mathematical_admission": False, "certificate_verification_performed": False,
        "scope": "ACTUAL_NATIVE_RELATION_BINDINGS_WITH_SYNTHETIC_UNVERIFIED_PARENT_STATEMENTS"}
    write(output / "RESULT.json", report)
    print(json.dumps(report, sort_keys=True))
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
