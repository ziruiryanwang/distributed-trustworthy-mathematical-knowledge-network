"""Synthetic structural controls only; ZERO cryptographic verifier invocations."""
from copy import deepcopy
import hashlib
from pathlib import Path
import sys
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from admission.bindings import bind_output, journal
from admission.verifier import ReceiptVerifier, VerifiedModule


def fixture():
    image, foundation, policy = "01"*32, "02"*32, "03"*32
    summary = {"schema": C.SUMMARY_SCHEMA, "foundation": foundation,
               "policy": policy, "group_count": 1, "group_root": "04"*32}
    module = C.summary_id(summary)
    raw = (b"DMKNM002" + (2).to_bytes(4, "little") + bytes.fromhex(image)
           + bytes.fromhex(foundation+policy+module+summary["group_root"])
           + (1).to_bytes(4, "little") + (5).to_bytes(8, "little"))
    receipt = b"DELIBERATELY_NOT_A_CRYPTOGRAPHIC_RECEIPT"
    parsed = journal(raw)
    reply = {key: parsed[key] for key in ("image", "foundation", "policy", "module", "summary", "rank")}
    reply.update(status="REAL_MODULE_RECEIPT_VERIFIED", fully_resolved=True,
                 mathematical_admission=True, receipt_kind="succinct-poseidon2",
                 receipt_sha256=hashlib.sha256(receipt).hexdigest(), receipt_bytes=len(receipt),
                 journal=list(raw), inner_verify_ms=1)
    return reply, receipt, summary, dict(image_id=image, foundation=foundation, policy=policy)


class StructuralBindingControls(unittest.TestCase):
    def setUp(self): self.value, self.receipt, self.summary, self.profile = fixture()

    def bind(self, value):
        return bind_output(C.canonical(value), self.receipt, self.summary, **self.profile)

    def test_structure_is_not_admission(self):
        result = self.bind(self.value)
        self.assertIs(type(result), dict)
        self.assertNotIsInstance(result, VerifiedModule)
        self.assertEqual(result["module"], C.summary_id(self.summary))
        self.assertNotIn("mathematical_admission", result)

    def test_exact_fields(self):
        for field in self.value:
            changed = deepcopy(self.value); del changed[field]
            with self.subTest(field=field), self.assertRaises(ValueError): self.bind(changed)
        changed = deepcopy(self.value); changed["verified"] = True
        with self.assertRaises(ValueError): self.bind(changed)

    def test_policy_and_module_substitutions(self):
        for key in ("image_id", "foundation", "policy"):
            profile = dict(self.profile); profile[key] = "07"*32
            with self.subTest(key=key), self.assertRaises(ValueError):
                bind_output(C.canonical(self.value), self.receipt, self.summary, **profile)
        summary = dict(self.summary); summary["group_root"] = "08"*32
        with self.assertRaises(ValueError):
            bind_output(C.canonical(self.value), self.receipt, summary, **self.profile)

    def test_false_or_wrong_status(self):
        for key, bad in (("status", "HASHES_COMPUTED"), ("fully_resolved", False),
                         ("mathematical_admission", False), ("receipt_kind", "fake"),
                         ("fully_resolved", 1), ("mathematical_admission", 1)):
            changed = deepcopy(self.value); changed[key] = bad
            with self.subTest(key=key, bad=bad), self.assertRaises(ValueError): self.bind(changed)

    def test_stdout_and_journal_must_agree(self):
        for key, bad in (("image", [2]*8), ("foundation", "07"*32), ("policy", "07"*32),
                         ("module", "07"*32), ("rank", 6)):
            changed = deepcopy(self.value); changed[key] = bad
            with self.subTest(key=key), self.assertRaises(ValueError): self.bind(changed)
        changed = deepcopy(self.value); changed["summary"]["group_count"] = 2
        with self.assertRaises(ValueError): self.bind(changed)

    def test_journal_mutations(self):
        for offset in (0, 8, 12, 44, 76, 108, 140, 172, 176, 183):
            changed = deepcopy(self.value); changed["journal"][offset] ^= 1
            with self.subTest(offset=offset), self.assertRaises(ValueError): self.bind(changed)
        for raw in ([], self.value["journal"][:-1], self.value["journal"]+[0]):
            changed = deepcopy(self.value); changed["journal"] = raw
            with self.assertRaises(ValueError): self.bind(changed)

    def test_strict_numeric_types(self):
        for key, bad in (("rank", True), ("receipt_bytes", True), ("inner_verify_ms", True),
                         ("rank", -1), ("rank", 2**64), ("inner_verify_ms", -1)):
            changed = deepcopy(self.value); changed[key] = bad
            with self.subTest(key=key, bad=bad), self.assertRaises(ValueError): self.bind(changed)
        for key, index, bad in (("image", 0, True), ("image", 0, 2**32),
                                ("journal", 0, True), ("journal", 0, 256)):
            changed = deepcopy(self.value); changed[key][index] = bad
            with self.subTest(key=key, bad=bad), self.assertRaises(ValueError): self.bind(changed)
        changed = deepcopy(self.value); changed["summary"]["group_count"] = True
        with self.assertRaises(ValueError): self.bind(changed)

    def test_v1_not_reinterpreted(self):
        current = bytes(self.value["journal"])
        old = b"DMKNM001" + (1).to_bytes(4, "little") + current[12:] + bytes.fromhex("06"*32)
        for raw in (old, old[:184], current+bytes(32), current[:8]+(1).to_bytes(4, "little")+current[12:]):
            with self.subTest(length=len(raw)), self.assertRaises(ValueError): journal(raw)
            changed = deepcopy(self.value); changed["journal"] = list(raw)
            with self.assertRaises(ValueError): self.bind(changed)

    def test_existential_statement_not_witness_attestation(self):
        bound = self.bind(self.value)
        self.assertEqual(len(bound["journal"]), 184)
        self.assertNotIn("witness", journal(bound["journal"]))
        self.assertNotIn("witness", bound)
        for key, value in (("witness", "06"*32), ("source_checked", True), ("proof_checked", True)):
            changed = deepcopy(self.value); changed[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError): self.bind(changed)

    def test_exact_receipt_bytes(self):
        for key, bad in (("receipt_bytes", len(self.receipt)+1), ("receipt_sha256", "07"*32)):
            changed = deepcopy(self.value); changed[key] = bad
            with self.subTest(key=key), self.assertRaises(ValueError): self.bind(changed)
        with self.assertRaises(ValueError):
            bind_output(C.canonical(self.value), self.receipt+b"changed", self.summary, **self.profile)

    def test_json_and_output_bounds(self):
        raw = C.canonical(self.value)
        for malformed in (b"", raw+b"{}", raw[:-1]+b',"rank":5}', b" "*16385,
                          raw.replace(b'"inner_verify_ms":1', b'"inner_verify_ms":1.0')):
            with self.subTest(length=len(malformed)), self.assertRaises(ValueError):
                bind_output(malformed, self.receipt, self.summary, **self.profile)

    def test_unregistered_and_expired_handles(self):
        # White-box empty state only: no forged/mocked successful receive call.
        owner = ReceiptVerifier.__new__(ReceiptVerifier)
        owner._closed = False; owner._busy = False
        owner._deadline = time.monotonic()+60; owner._handles = {}
        for unknown in (VerifiedModule(), {}, self.value, None):
            with self.assertRaises(ValueError): owner.describe(unknown)
        owner.close()
        with self.assertRaises(ValueError): owner.describe(VerifiedModule())
        owner._closed = False; owner._deadline = time.monotonic()-1
        with self.assertRaises(ValueError): owner.describe(VerifiedModule())


if __name__ == "__main__": unittest.main(verbosity=2)
