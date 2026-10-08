"""Pure output binding checks. Success here alone is NOT receipt verification."""
from __future__ import annotations

import hashlib
from modules import codec as C

JOURNAL_PROFILE = 2
JOURNAL_BYTES = 184
OUTPUT_FIELDS = {"status", "image", "foundation", "policy", "module", "summary",
                 "rank", "receipt_sha256", "receipt_bytes", "journal",
                 "inner_verify_ms", "fully_resolved", "receipt_kind", "mathematical_admission"}


def journal(raw):
    C.require(type(raw) is bytes and len(raw) == JOURNAL_BYTES and raw[:8] == b"DMKNM002"
              and int.from_bytes(raw[8:12], "little") == JOURNAL_PROFILE, "ADMISSION_JOURNAL_LAYOUT")
    result = {"image": [int.from_bytes(raw[i:i+4], "little") for i in range(12, 44, 4)],
              "foundation": raw[44:76].hex(), "policy": raw[76:108].hex(),
              "module": raw[108:140].hex(), "group_root": raw[140:172].hex(),
              "group_count": int.from_bytes(raw[172:176], "little"),
              "rank": int.from_bytes(raw[176:184], "little")}
    result["summary"] = {"schema": C.SUMMARY_SCHEMA, **{key: result[key]
        for key in ("foundation", "policy", "group_count", "group_root")}}
    C.require(C.summary_id(result["summary"]) == result["module"], "ADMISSION_JOURNAL_MODULE")
    return result


def bind_output(raw, receipt, expected_summary, *, image_id, foundation, policy):
    """Validate trusted same-call stdout, never create an acceptance handle.

    Callers MUST separately execute the adopted verifier and require clean
    supervised closure. A fabricated JSON can pass these structural checks.
    Profile 2 certifies that a valid module witness exists; it does not attest
    that any separately supplied proof/source bytes were checked.
    """
    C.require(type(raw) is bytes and 0 < len(raw) <= 16384, "ADMISSION_OUTPUT_BOUND")
    C.require(type(receipt) is bytes and 0 < len(receipt) <= 64*1024**2, "ADMISSION_RECEIPT_BOUND")
    for value in (image_id, foundation, policy): C.digest_string(value)
    module = C.summary_id(expected_summary)
    C.require(expected_summary["foundation"] == foundation and expected_summary["policy"] == policy,
              "ADMISSION_EXPECTED_POLICY")
    value = C.parse_json(raw, C.Limits(max_bytes=16384))
    C.fields(value, OUTPUT_FIELDS)
    C.require(value["status"] == "REAL_MODULE_RECEIPT_VERIFIED"
              and value["fully_resolved"] is True and value["mathematical_admission"] is True
              and value["receipt_kind"] == "succinct-poseidon2", "ADMISSION_STATUS")
    C.require(type(value["journal"]) is list and len(value["journal"]) == JOURNAL_BYTES,
              "ADMISSION_JOURNAL_BYTES")
    for byte in value["journal"]: C.uint(byte, 255)
    raw_journal = bytes(value["journal"])
    decoded = journal(raw_journal)
    words = [int.from_bytes(bytes.fromhex(image_id)[i:i+4], "little") for i in range(0, 32, 4)]
    C.require(type(value["image"]) is list and len(value["image"]) == 8, "ADMISSION_IMAGE_WORDS")
    for word in value["image"]: C.uint(word)
    C.uint(value["rank"], 2**64-1); C.uint(value["receipt_bytes"], 64*1024**2)
    C.uint(value["inner_verify_ms"], 2**64-1)
    C.validate_summary(value["summary"])
    for key in ("foundation", "policy", "module", "receipt_sha256"):
        C.digest_string(value[key])
    C.require(decoded["image"] == words and decoded["foundation"] == foundation
              and decoded["policy"] == policy and decoded["module"] == module
              and decoded["summary"] == expected_summary, "ADMISSION_ADOPTED_STATEMENT")
    C.require(all(value[key] == decoded[key] for key in
                  ("image", "foundation", "policy", "module", "summary", "rank")),
              "ADMISSION_STDOUT_JOURNAL_BINDING")
    C.require(value["receipt_bytes"] == len(receipt)
              and value["receipt_sha256"] == hashlib.sha256(receipt).hexdigest(),
              "ADMISSION_EXACT_RECEIPT")
    return {"module": module, "summary": expected_summary, "journal": raw_journal,
            "receipt_sha256": value["receipt_sha256"], "inner_verify_ms": value["inner_verify_ms"]}
