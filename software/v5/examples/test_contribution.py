"""Eight focused continuation controls with explicitly INERT issuers/custody.

The helper, pure parameter/hash checks and inherited public context-identity
guard are real. Authoring, admission, publication, grants and lifecycle effects
are synthetic. No mathematical acceptance, native process, network or proof.
Only this new suite runs; no predecessor suite or fixture campaign is invoked.
"""
import asyncio
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE/"portable_runtime"), str(SOURCE)]
from client import workspace_atomic as A
from examples import contribution as H
from modules import codec as C

SOURCE_TEXT = "theorem independentlyChosen : True := True.intro\n"
ROOTS = [[["s", "independentlyChosen"]]]
AUTHOR = {"cpu_seconds": 2, "wall_seconds": 5, "memory_mib": 128}
ADMISSION = {"native_cpu_seconds": 2, "receipt_cpu_seconds": 2,
             "wall_seconds": 5, "memory_mib": 128}
RAW = b"INERT-NEW-OUTPUT-NOT-A-MATHEMATICAL-PACKET"
SHA = hashlib.sha256(RAW).hexdigest()
SUMMARY = {"schema": C.SUMMARY_SCHEMA, "foundation": "11"*32, "policy": "22"*32,
           "group_count": 1, "group_root": "33"*32}
MODULE = C.summary_id(SUMMARY)
JOURNAL = b"INERT-JOURNAL-NOT-A-CERTIFICATE"
OBSERVED = {"inert_clients": 0, "public_context_guard_calls": 0,
            "successful_compositions": 0, "native_launch_attempts": 0}


def prepared():
    return {"status": "UNTRUSTED_MIXED_DELTA_PACKET_PREPARED",
        "mathematical_acceptance": False,
        "child": {"status": "UNTRUSTED_MIXED_DELTA_PACKET", "packet": RAW,
            "packet_sha256": SHA, "local_module": MODULE, "summary": deepcopy(SUMMARY),
            "source_sha256": hashlib.sha256(SOURCE_TEXT.encode()).hexdigest(),
            "roots": deepcopy(ROOTS), "mathematical_acceptance": False}}


class InertGrant:
    """Not a workspace-issued grant and never promoted to one."""
    identifier = "INERT-ORIGINAL-GRANT"

    def __init__(self, events):
        self.events = events
        self.deadline = 1234567  # Sentinel: not an actual temporal allowance.

    def remaining_seconds(self):
        self.events.append(("deadline", self))
        return 5


class InertPackets:
    def __init__(self, client):
        self.client = client

    def put(self, module, raw, *, before_commit):
        self.client.events.append(("put", module, raw, before_commit))
        if self.client.failure_stage == "put":
            raise self.client.failure
        before_commit()


class InertClient:
    """Only the allowed public suffix; no acquisition/import/open/close API."""
    def __init__(self):
        OBSERVED["inert_clients"] += 1
        self.events = []
        self.grant = InertGrant(self.events)
        self.workspace = SimpleNamespace(packets=InertPackets(self))
        self.context = object()  # Explicitly inert, not an AuthorContext.
        self.warrant = object()  # Explicitly inert, not a LiveWarrant.
        self.prepared = prepared()
        self.fact = {"kind": "mixed", "live": {"module": MODULE,
            "packet_sha256": SHA, "summary": deepcopy(SUMMARY), "journal": JOURNAL}}
        self.publication = {"phase": "LOCALLY_PUBLISHED", "publication_id": "44"*32,
            "intent": {"module": MODULE, "packet_sha256": SHA, "packet_bytes": len(RAW),
                "export_names": deepcopy(ROOTS),
                "retention_policy": {"mode": "quota-bounded-local-custody"}},
            "mathematical_acceptance": False, "remote_placement_confirmed": False}
        self.failure_stage = None
        self.failure = RuntimeError("INERT-SELECTED-FAILURE")

    def author(self, context, source, roots, **limits):
        self.events.append(("author", context, source, deepcopy(roots), limits))
        if context is not self.context:
            raise ValueError("INERT_FOREIGN_CONTEXT")
        if self.failure_stage == "author":
            raise self.failure
        return deepcopy(self.prepared)

    def admit_local(self, module, packet_sha256, packet_bytes, **limits):
        self.events.append(("admit", module, packet_sha256, packet_bytes, limits))
        if self.failure_stage == "admit":
            raise self.failure
        return self.warrant

    def describe(self, warrant):
        self.events.append(("describe", warrant))
        if warrant is not self.warrant:
            raise ValueError("INERT_WRONG_WARRANT")
        if self.failure_stage == "describe":
            raise self.failure
        return deepcopy(self.fact)

    def publish(self, packet, export_names, *, retention_policy):
        self.events.append(("publish", packet, deepcopy(export_names), retention_policy))
        if self.failure_stage == "publish":
            raise self.failure
        return deepcopy(self.publication)


class PublicGuardClient(InertClient):
    """Real inherited author/context guard; deliberately inert lifecycle shell.

    No real client construction or owner adoption is claimed. The public author
    method must refuse these cases before MixedSourceOperation is constructed.
    """
    _live_context = A.CommonsClient._live_context

    def __init__(self):
        super().__init__()
        self.context = A.AuthorContext()  # Synthetic allocation, not issuance.
        self._context = self.context, "INERT-SELECTION-BINDING"
        self._selection_view = object()
        self._session = SimpleNamespace(require_view=lambda view: None)
        self.preparation = None
        self._busy = False

    def _enter(self):
        self.events.append(("author",))
        self._busy = True

    def _fail(self, error):
        self.events.append(("inert_fail", str(error)))

    def _active(self):
        raise AssertionError("INVALID_CONTEXT_MUST_NOT_RETURN")

    def _census(self):
        raise AssertionError("INVALID_CONTEXT_MUST_NOT_RETURN")

    def author(self, *args, **kwargs):
        OBSERVED["public_context_guard_calls"] += 1
        return A.CommonsClient.author(self, *args, **kwargs)


def contribute(client, **changes):
    arguments = {"source": SOURCE_TEXT, "roots": deepcopy(ROOTS),
        "export_names": deepcopy(ROOTS), "author_limits": deepcopy(AUTHOR),
        "admission_limits": deepcopy(ADMISSION)}
    arguments.update(changes)
    return H.contribute_from_context(client, client.context, **arguments)


class ContributionControls(unittest.TestCase):
    def stages(self, client):
        return [event[0] for event in client.events if event[0] != "deadline"]

    def test_exact_live_context_new_packet_and_original_grant(self):
        client = InertClient()
        workspace, grant, deadline = client.workspace, client.grant, client.grant.deadline
        report = contribute(client)
        self.assertEqual(self.stages(client), ["author", "put", "admit", "describe", "publish"])
        self.assertEqual(report["status"], "CONTRIBUTED")
        self.assertEqual(report["schema"], "DMKN_V5_CONTEXT_CONTRIBUTION_RESULT_V1")
        self.assertEqual(report["operation_id"], grant.identifier)
        self.assertFalse(report["mathematical_acceptance"])
        self.assertEqual(report["authority"], "OPERATIONAL_CONTRIBUTION_REPORT_NOT_TRANSFERABLE_AUTHORITY")
        self.assertIs(client.events[0][1], client.context)
        self.assertEqual(client.events[0][2:], (SOURCE_TEXT, ROOTS, AUTHOR))
        events = {event[0]: event for event in client.events if event[0] != "deadline"}
        self.assertEqual(events["put"][1:3], (MODULE, RAW))
        self.assertIs(events["put"][3].__self__, grant)
        self.assertEqual(events["put"][3].__func__, InertGrant.remaining_seconds)
        self.assertEqual(events["admit"][1:], (MODULE, SHA, len(RAW), ADMISSION))
        self.assertIs(events["describe"][1], client.warrant)
        self.assertEqual(events["publish"][1:], (RAW, ROOTS, {"mode": "quota-bounded-local-custody"}))
        self.assertEqual(report["checked_output"], {"kind": "mixed", "module": MODULE,
            "journal": list(JOURNAL), "packet_sha256": SHA})
        self.assertEqual(report["publication"], client.publication)
        self.assertIs(client.workspace, workspace)
        self.assertIs(client.grant, grant)
        self.assertEqual(grant.deadline, deadline)
        self.assertEqual(sum(event[0] == "deadline" for event in client.events), 2)
        json.dumps(report)  # No live token is accidentally serialized as a warrant.
        OBSERVED["successful_compositions"] += 1

    def test_need_data_returns_without_custody_or_admission(self):
        client = InertClient()
        client.prepared = {"status": "NEED_AUTHORING_CONTEXT_DATA",
            "demands": [{"kind": "NeedBody", "module": "55"*32}],
            "mathematical_acceptance": False}
        report = contribute(client)
        self.assertEqual(self.stages(client), ["author"])
        self.assertEqual(report["status"], "NEED_AUTHORING_CONTEXT_DATA")
        self.assertEqual(report["demands"], client.prepared["demands"])
        self.assertIsNone(report["checked_output"])
        self.assertIsNone(report["publication"])
        self.assertFalse(report["mathematical_acceptance"])
        report["demands"][0]["kind"] = "changed-report"
        self.assertEqual(client.prepared["demands"][0]["kind"], "NeedBody")

    def test_public_author_guard_rejects_foreign_superseded_and_preview_context(self):
        for case in ("foreign", "superseded", "preview", "absent", "same-token-no-owner"):
            with self.subTest(case=case):
                client = PublicGuardClient()
                if case == "foreign": client.context = A.AuthorContext()
                elif case == "superseded": client._context = A.AuthorContext(), "replacement"
                elif case == "preview": client.context = {"status": "READY", "mathematical_acceptance": False}
                elif case == "absent": client._context = None
                code = "CLIENT_AUTHOR_OWNER_NOT_SELECTED" if case == "same-token-no-owner" \
                    else "CLIENT_FOREIGN_OR_SUPERSEDED_CONTEXT"
                with patch.object(A, "MixedSourceOperation", side_effect=AssertionError("NATIVE_PREPARATION_FORBIDDEN")) as native:
                    with self.assertRaisesRegex(ValueError, code): contribute(client)
                self.assertFalse(native.called)
                self.assertEqual(self.stages(client), ["author", "inert_fail"])
                self.assertFalse(client._busy)

    def test_invalid_parameters_refuse_before_author(self):
        invalid = [dict(source=b"not-text"), dict(roots=[]), dict(export_names=[]),
            dict(roots=ROOTS+ROOTS), dict(export_names=ROOTS+ROOTS),
            dict(author_limits={**AUTHOR, "cpu_seconds": 0}),
            dict(author_limits={**AUTHOR, "wall_seconds": True}),
            dict(admission_limits={**ADMISSION, "native_cpu_seconds": 0}),
            dict(admission_limits={**ADMISSION, "memory_mib": 63}),
            dict(author_limits={**AUTHOR, "extra": 1})]
        for changes in invalid:
            with self.subTest(changes=changes):
                client = InertClient()
                with self.assertRaises(ValueError): contribute(client, **changes)
                self.assertEqual(client.events, [])

    def test_untrusted_preparation_and_exact_input_binding_before_custody(self):
        cases = [None, {"status": "ACCEPTED", "mathematical_acceptance": True},
                 {**prepared(), "child": None}, {**prepared(), "mathematical_acceptance": True}]
        for field, value in (("status", "ACCEPTED"), ("mathematical_acceptance", True),
            ("packet", RAW.decode()), ("packet_sha256", "00"*32),
            ("source_sha256", "00"*32), ("roots", [[["s", "different"]]])):
            row = prepared(); row["child"][field] = value; cases.append(row)
        for index, response in enumerate(cases):
            with self.subTest(case=index):
                client = InertClient(); client.prepared = response
                with self.assertRaises(ValueError): contribute(client)
                self.assertEqual(self.stages(client), ["author"])

    def test_failures_propagate_without_retry_or_next_side_effect(self):
        order = ["author", "put", "admit", "describe"]
        for stage in order:
            with self.subTest(stage=stage):
                client = InertClient(); client.failure_stage = stage
                with self.assertRaises(RuntimeError) as caught: contribute(client)
                self.assertIs(caught.exception, client.failure)
                self.assertEqual(self.stages(client), order[:order.index(stage)+1])

    def test_live_admission_fact_must_match_exact_prepared_output(self):
        for field, value in (("module", "66"*32), ("packet_sha256", "77"*32),
                             ("summary", {**SUMMARY, "group_count": 2})):
            with self.subTest(field=field):
                client = InertClient(); client.fact["live"][field] = value
                with self.assertRaisesRegex(ValueError, "CONTEXT_CONTRIBUTION_OUTPUT_BINDING"):
                    contribute(client)
                self.assertEqual(self.stages(client), ["author", "put", "admit", "describe"])

    def test_publication_mismatch_or_partial_never_reports_contributed(self):
        cases = [("phase", "PACKET_READ_BACK"), ("module", "88"*32),
            ("packet_sha256", "99"*32), ("packet_bytes", len(RAW)+1),
            ("export_names", [[["s", "different"]]]), ("exception", None)]
        for field, value in cases:
            with self.subTest(field=field):
                client = InertClient()
                if field == "phase": client.publication[field] = value
                elif field == "exception":
                    client.failure_stage = "publish"
                    client.failure = A.PartialPublicationError("aa"*32, {"phase": "PACKET_READ_BACK"})
                else: client.publication["intent"][field] = value
                expected = A.PartialPublicationError if field == "exception" else ValueError
                with self.assertRaises(expected) as caught: contribute(client)
                if field == "exception": self.assertIs(caught.exception, client.failure)
                self.assertEqual(self.stages(client), ["author", "put", "admit", "describe", "publish"])


SELECTED = (
    "test_exact_live_context_new_packet_and_original_grant",
    "test_need_data_returns_without_custody_or_admission",
    "test_public_author_guard_rejects_foreign_superseded_and_preview_context",
    "test_invalid_parameters_refuse_before_author",
    "test_untrusted_preparation_and_exact_input_binding_before_custody",
    "test_failures_propagate_without_retry_or_next_side_effect",
    "test_live_admission_fact_must_match_exact_prepared_output",
    "test_publication_mismatch_or_partial_never_reports_contributed",
)


def forbidden_native(*args, **kwargs):
    OBSERVED["native_launch_attempts"] += 1
    raise AssertionError("NATIVE_FORBIDDEN")


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    output = Path(sys.argv[2])
    if not output.is_dir() or output.resolve() != output:
        raise ValueError("EXISTING_CANONICAL_OUTPUT_REQUIRED")
    if len(SELECTED) != 8 or len(set(SELECTED)) != 8:
        raise ValueError("EXACT_EIGHT_CONTROLS_REQUIRED")
    suite = unittest.TestSuite(ContributionControls(name) for name in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=forbidden_native), \
         patch.object(asyncio, "create_subprocess_exec", side_effect=forbidden_native), \
         patch.object(asyncio, "create_subprocess_shell", side_effect=forbidden_native):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = (result.wasSuccessful() and result.testsRun == 8 and not result.skipped
              and OBSERVED["native_launch_attempts"] == 0)
    report = {"status": "PASS" if passed else "FAIL", "tests": result.testsRun,
        "required_tests": 8, "failures": len(result.failures), "errors": len(result.errors),
        "skipped": len(result.skipped), "selected": list(SELECTED), "observed": OBSERVED,
        "scope": "REAL_HELPER_HASH_PARAMETER_AND_CONTEXT_IDENTITY_CHECKS_WITH_INERT_AUTHORITY_AND_STORAGE",
        "native_calls": 0, "proof_calls": 0, "mathematical_acceptance": False,
        "sources": {name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() for name in (
            "examples/contribution.py", "examples/test_contribution.py", "client/workspace_atomic.py")}}
    with (output/"controls-result.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, sort_keys=True, indent=2)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
