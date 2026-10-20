"""One image-bound retained-DAG check, not a benchmark or full semantic import.

The saved target is only a requested statement. Authority is obtained solely
from a fresh same-call NativeClosureOwner invocation and revoked before exit.
"""
import hashlib
import json
from pathlib import Path
import sys
import time

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE))
from modules import codec as C
from aggregate_claims import bindings as B
from native_closure.owner import NativeClosureOwner

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
INSTALL = ROOT / "product-local/v4-library-commons-02/commons-v4"
BASE = "experiments/v5-local-checks/module-base-snapshot-03/evidence/profile2-request.json"
PACKET = ("product-local/v5-distribution-03/contributor-commons/operations/"
          "e045a52cdcb18dec0bcea6ae9a79a899565f2024522b099b6c067e1e4562bf5a/"
          "preparation/author-1/mixed-packet.json")
PRIOR = ("product-local/v5-distribution-03/contributor-commons/operations/"
         "e045a52cdcb18dec0bcea6ae9a79a899565f2024522b099b6c067e1e4562bf5a/"
         "delta/2/native-1/stdout.txt")
NATIVE = ROOT / "experiments/v5-local-checks/bounded-parse-native-build-02/native_aggregate.exe"
MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
IMAGE = "99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60"
TARGET = "6ea8fa600c3ec9eb64992466c2c897d6455b53a6d0461a2b655fcb3f2c86d55f"
FIXTURES = {
    BASE: (91311, "ce554d4877e0b865690f565384381a188ce13166e960a55d39106159f46c067c"),
    PACKET: (658554, "6998ba92d064c8ce790192a434655d4b99bf0e7018f422ec24be757de55db2eb"),
    PRIOR: (2153, "ced1681cfe5fa2f4a2c852a8b38136742c2d34ebb0b493e827070d58ba864258"),
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def fixture(relative):
    size, digest = FIXTURES[relative]
    path = ROOT / relative
    C.require(path.stat().st_size == size, "ACTUAL_FIXTURE_SIZE")
    raw = path.read_bytes()
    C.require(len(raw) == size and sha(raw) == digest, "ACTUAL_FIXTURE_PIN")
    return raw


def main():
    started = time.monotonic()
    C.require(len(sys.argv) == 3 and sys.argv[1] == "--output", "ACTUAL_ARGUMENTS")
    output = Path(sys.argv[2])
    selection = json.loads((output / "selection.json").read_bytes())
    C.require(output.is_absolute() and output.is_relative_to(ROOT / "experiments/v5-local-checks"),
              "ACTUAL_OUTPUT")
    pins = {}
    for path, digest in selection["runtime_pins"].items():
        pins[path] = {"bytes": Path(path).stat().st_size, "sha256": digest}
    for relative, digest in selection["sources"].items():
        path = output / "sources" / relative
        pins[str(path)] = {"bytes": path.stat().st_size, "sha256": digest}

    raw_base, raw_packet, raw_prior = (fixture(p) for p in (BASE, PACKET, PRIOR))
    packet, prior = C.parse_json(raw_packet), C.parse_json(raw_prior)
    C.require(packet["schema"] == "DMKN_MIXED_DELTA_PACKET_V1"
              and len(packet["deltas"]) == 2, "ACTUAL_PACKET")
    # No receipt from packet is passed to this owner, and no earlier success
    # field is consulted. The adopted native checker checks all three modules.
    base = C.parse_json(raw_base)
    C.fields(base, {"schema", "image", "rank", "local_spec", "rows", "parents", "bodies"})
    C.require(base["schema"] == "DMKN_CERTIFIED_MODULES_V2"
              and type(base["rank"]) is int and base["rank"] == 0
              and base["parents"] == [] and base["image"] == [0]*8
              and all(type(word) is int for word in base["image"]), "ACTUAL_UNBOUND_BASE")
    # The preparation input contains an uninitialized image, not a prior
    # aggregate-compatible warrant. Bind only metadata, then check all math.
    prepared = dict(base)
    prepared["image"] = [int.from_bytes(bytes.fromhex(B.RELATION_IMAGE)[i:i+4], "little")
                         for i in range(0, 32, 4)]
    C.require({k: v for k, v in prepared.items() if k != "image"}
              == {k: v for k, v in base.items() if k != "image"}, "ACTUAL_ONLY_IMAGE_CHANGED")
    C.require(len(packet["frontiers"]) == 1 and len(packet["claims"]) == 1
              and packet["claims"][0]["tag"] == 0, "ACTUAL_SINGLE_BASE_FRONTIER")
    base_list = packet["frontiers"][0]["journal"]
    C.require(type(base_list) is list and len(base_list) == 184, "ACTUAL_BASE_JOURNAL")
    for byte in base_list:
        C.uint(byte, 255)
    base_journal = bytes(base_list)
    base_statement = B.member_journal(base_journal)
    C.require(base_statement["rank"] == 0
              and base_statement["summary"] == C.summarize(prepared["local_spec"])
              and packet["claims"][0]["statement"] == base_list, "ACTUAL_EXACT_BASE_STATEMENT")
    base_parents = [parent["journal"] for delta in packet["deltas"] for parent in delta["parents"]
                    if bytes(parent["journal"])[108:140].hex() == base_statement["module"]]
    C.require(len(base_parents) == 2 and all(raw == base_list for raw in base_parents),
              "ACTUAL_EXACT_BASE_PARENT_REFERENCES")
    bound_base = C.canonical(prepared)
    witnesses = [bound_base] + [C.canonical(item) for item in packet["deltas"]]
    C.require(type(prior["journal"]) is list and len(prior["journal"]) == 184,
              "ACTUAL_REQUESTED_J")
    for byte in prior["journal"]:
        C.uint(byte, 255)
    target = bytes(prior["journal"])
    requested = B.member_journal(target)
    C.require(requested["module"] == TARGET and requested["rank"] == 2,
              "ACTUAL_SAME_REQUESTED_TARGET")
    final_spec = packet["deltas"][-1]["local_spec"]
    C.require(C.summarize(final_spec) == requested["summary"], "ACTUAL_TARGET_SUMMARY")
    names = [item["name"] for group in final_spec["groups"] for item in group["declarations"]]
    C.require(names == [[["s", "ClientV5"], ["s", "project_summary"]]], "ACTUAL_TARGET_EXPORT")

    owner = None
    try:
        owner = NativeClosureOwner(
            supervisor_manifest=INSTALL / "RELEASE-MANIFEST.json",
            supervisor_manifest_sha256=MANIFEST_SHA,
            executable=NATIVE, runtime_pins=pins, adopted_image=IMAGE,
            deadline=started + 60, submitted_bytes=1024**2,
            reserved_cpu_seconds=30, controller_cpu_seconds=20)
        tokens = owner.check(witnesses, [target], output / "native",
                             cpu_seconds=30, wall_seconds=45, memory_mib=256)
        descriptions = [owner.describe(token) for token in tokens]
        C.require(len(tokens) == 3 and owner.members() == tokens
                  and sum(item["journal"] == base_journal for item in descriptions) == 1,
                  "ACTUAL_COMPLETE_INVENTORY")
        matches = [item for item in descriptions if item["journal"] == target]
        C.require(len(matches) == 1 and matches[0]["module"] == TARGET
                  and matches[0]["summary"] == requested["summary"], "ACTUAL_LIVE_TARGET")
        report = owner.report()
        owner.close()
        try:
            owner.describe(tokens[0])
        except ValueError:
            revoked = True
        else:
            revoked = False
        C.require(revoked, "ACTUAL_CLOSED_HANDLE_REFUSAL")
        for relative in FIXTURES:
            fixture(relative)
        result = {
            "schema": "DMKN_V5_NATIVE_CLOSURE_ACTUAL_V1",
            "status": "ACTUAL_SAME_CALL_ZERO_ASSUMPTION_MEMBERSHIP_PASSED",
            "scope": "VERIFICATION_COMPONENT_NOT_READY_CONTEXT_OR_GROWTH_COMPARISON",
            "authority": "SAVED_EVIDENCE_ONLY_ALL_LIVE_TOKENS_REVOKED",
            "target": target.hex(), "module": TARGET,
            "base_preparation": {"source_sha256": sha(raw_base), "bound_sha256": sha(bound_base),
                "changed_fields": ["image"], "requested_journal": base_journal.hex(),
                "authority": "FRESH_UNTRUSTED_WITNESS_CHECKED_IN_THIS_CALL"},
            "witness_bytes": [len(raw) for raw in witnesses],
            "witness_sha256": [sha(raw) for raw in witnesses],
            "members": [item["journal"].hex() for item in descriptions],
            "report_before_close": report, "report_after_close": owner.report(),
            "closed_handle_refused": revoked, "wall_seconds": time.monotonic() - started,
            "receipt_verifications": 0, "native_invocations": 1,
        }
        with (output / "actual-result.json").open("xb") as stream:
            stream.write(C.canonical(result))
        print(json.dumps({"status": result["status"], "members": len(tokens),
                          "scope": result["scope"]}), flush=True)
    finally:
        if owner is not None:
            owner.close()


if __name__ == "__main__":
    main()
