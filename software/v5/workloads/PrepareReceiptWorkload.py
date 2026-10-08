"""Owner-selected native wrapper binding experiment, NEVER certification.

Re-decode the exact retained owner export under the new semantic policy.
No old ModuleID is relabeled. Diagnostics create conditional journals only;
the real guest must later discharge every parent with genuine cryptography.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import PrepareWorkload as W
from modules import codec as C
from modules.receipt import witness as R


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", required=True)
    parser.add_argument("--binary-sha256", required=True)
    parser.add_argument("--export", required=True)
    parser.add_argument("--export-sha256", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    binary, source, out = Path(args.binary), Path(args.export), Path(args.output)
    C.require(binary.is_absolute() and source.is_absolute() and out.is_absolute()
              and not out.exists(), "EXPLICIT_FRESH_PATHS")
    C.require(binary.stat().st_size <= 128 * 1024**2 and source.stat().st_size <= 2**20,
              "WORKLOAD_INPUT_BYTE_BOUNDS")
    C.require(hashlib.sha256(binary.read_bytes()).hexdigest() == args.binary_sha256,
              "NATIVE_BINARY_PIN")
    raw = source.read_bytes()
    C.require(hashlib.sha256(raw).hexdigest() == args.export_sha256, "WORKLOAD_EXPORT_PIN")
    out.mkdir()

    def call(action, label, path=None):
        command = [str(binary), action] + ([] if path is None else [str(path)])
        result = subprocess.run(command, capture_output=True, timeout=30, check=False)
        (out / (label + ".stdout")).write_bytes(result.stdout)
        (out / (label + ".stderr")).write_bytes(result.stderr)
        answer = C.parse_json(result.stdout)
        C.require(result.returncode == 0 and answer.get("mathematical_admission") is False,
                  "NATIVE_DIAGNOSTIC_EXPECTED_RESULT:" + label)
        return answer

    profile = call("profile", "profile")
    C.require(profile["status"] == "PROFILE_DESCRIPTION_ONLY", "PROFILE_ONLY")
    C.require(profile["policy"] == C.hash_value("semantic-policy", profile["semantic_descriptor"]),
              "PROFILE_POLICY_BINDING")
    journals, specs, evidence = {}, {}, []
    image = [0] * 8  # Explicit diagnostic placeholder, not an adopted image.

    def observe(label, env, seed, dependencies, base):
        C.require(env.spec["foundation"] == profile["foundation"]
                  and len(seed) == profile["foundation_rows"]
                  and hashlib.sha256(C.canonical(seed)).hexdigest()
                  == profile["foundation_canonical_sha256"], "EXACT_PROFILE_FOUNDATION")
        parents = [{"journal": journals[dep], "openings": [C.group_opening(specs[dep], i)
                    for i in range(len(specs[dep]["groups"]))]} for dep in dependencies]
        request = R.make_input(env, seed, image, parents)
        path = base / "receipt-input.json"
        W.write(path, request)
        answer = call("check", label, path)
        C.require(answer["status"] == "BOUND_RELATION_NATIVE_ONLY_PENDING_PARENT_PROOF_VERIFICATION"
                  and answer["certificate_verification_performed"] is False
                  and answer["pending_parent_statements"] == len(parents), "RELATION_STAYS_CONDITIONAL")
        journal = bytes(answer["journal"])
        decoded = R.decode_journal(journal)
        C.require(decoded["image"] == image and decoded["module"] == env.module
                  and decoded["summary"] == C.summarize(env.spec)
                  and decoded["rank"] == request["rank"]
                  and decoded["witness"] == C.hash_value("module-witness", request),
                  "EXACT_DIAGNOSTIC_CONCLUSION")
        W.write(base / "receipt-result.json", answer)
        journals[label], specs[label] = journal, env.spec
        evidence.append({"label": label, "module": env.module, "rank": decoded["rank"],
                         "input_bytes": path.stat().st_size,
                         "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                         "parent_statements": len(parents), "body_openings": len(request["bodies"]),
                         "status": answer["status"]})

    rows = [C.parse_json(line) for line in raw.splitlines()]
    report = W.prepare(rows, out, semantic_policy=profile["semantic_descriptor"], observe=observe)
    report.update(status="PASS_NATIVE_WRAPPER_BINDING_NOT_CERTIFICATION", profile=profile,
                  native_evidence=evidence, source_sha256=args.export_sha256,
                  native_binary_sha256=args.binary_sha256, certificate_verification_performed=False,
                  image_adopted=False, journal_authority="CONDITIONAL_DIAGNOSTICS_NOT_RECEIPTS")
    W.write(out / "RESULT.json", report)
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
