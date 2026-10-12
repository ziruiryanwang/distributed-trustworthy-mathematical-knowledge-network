"""Bind exact aggregate-verifier stdout; this helper grants NO authority.

Only an adopted host, run in a same-call supervised operation with successful
closure and unchanged pins, can supply trustworthy verification evidence.
A fabricated JSON object can pass this pure structural helper.
"""
import hashlib

from aggregate import bindings as B
from modules import codec as C

SCHEMA = "DMKN_AGGREGATE_VERIFY_RESULT_V1"
STATUS = "VERIFIED_RESOLVED_AGGREGATE_RECEIPT"
FIELDS = {"schema", "status", "aggregate_image", "header", "receipt_sha256", "receipt_bytes"}


def bind_output(raw, receipt, expected_header, *, adopted_image):
    """Match an actual call's bytes to its locally selected A and exact header.

    This is not a receipt parser, cryptographic verifier, persisted authority,
    owner handle or member-opening check. In particular it must never accept a
    saved report instead of running the real verifier.
    """
    C.require(type(raw) is bytes and 0 < len(raw) <= 16384,
              "AGGREGATE_ADMISSION_OUTPUT_BOUND")
    C.require(type(receipt) is bytes and 0 < len(receipt) <= 64 * 1024**2,
              "AGGREGATE_ADMISSION_RECEIPT_BOUND")
    decoded = B.decode_header(expected_header, adopted_image=adopted_image)
    value = C.parse_json(raw, C.Limits(max_bytes=16384, max_nodes=1024, max_depth=8))
    C.fields(value, FIELDS)
    C.require(value["schema"] == SCHEMA and value["status"] == STATUS,
              "AGGREGATE_ADMISSION_STATUS")
    C.digest_string(value["aggregate_image"])
    C.digest_string(value["receipt_sha256"])
    C.uint(value["receipt_bytes"], 64 * 1024**2)
    C.require(type(value["header"]) is list and len(value["header"]) == B.HEADER_BYTES,
              "AGGREGATE_ADMISSION_HEADER_BYTES")
    for byte in value["header"]:
        C.uint(byte, 255)
    C.require(value["aggregate_image"] == adopted_image
              and bytes(value["header"]) == expected_header,
              "AGGREGATE_ADMISSION_EXACT_STATEMENT")
    digest = hashlib.sha256(receipt).hexdigest()
    C.require(value["receipt_bytes"] == len(receipt) and value["receipt_sha256"] == digest,
              "AGGREGATE_ADMISSION_EXACT_RECEIPT")
    return {"header": expected_header, "statement": decoded,
            "receipt_sha256": digest, "receipt_bytes": len(receipt)}
