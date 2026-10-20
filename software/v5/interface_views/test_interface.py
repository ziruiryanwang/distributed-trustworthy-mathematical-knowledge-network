"""Focused interface-view controls: pure real algorithms, INERT authority only.

No receipt, foundation, admission, native executable or mathematical validity is
fabricated. Session constructor/installation authority is deliberately bypassed
to exercise its data lifecycle. No predecessor test suite is imported or run.
"""
import asyncio
from copy import deepcopy
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(SOURCE / "portable_runtime"), str(SOURCE)]


def overlay(name, relative):
    parent = importlib.import_module(name.rsplit(".", 1)[0])
    spec = importlib.util.spec_from_file_location(name, SOURCE / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    setattr(parent, name.rsplit(".", 1)[1], module)
    return module


overlay("admission.pin_phase", "runtime_efficient/admission/pin_phase.py")
overlay("admission.verifier", "runtime_efficient/admission/verifier.py")
overlay("mixed_claims.receiver", "runtime_efficient/mixed_claims/receiver.py")
I = overlay("mixed_claims.imports_atomic", "interface_views/imports_atomic.py")
overlay("mixed_claims.interface_projection", "interface_views/projection.py")
A = overlay("mixed_claims.authoring_atomic", "interface_views/authoring_atomic.py")
S = overlay("transport.semantic_staging", "interface_views/semantic_staging.py")
E = overlay("client.workspace_evidence", "interface_views/workspace_evidence.py")
W = overlay("client.workspace_staged", "interface_views/workspace_staged.py")
H = overlay("client.semantic_reader", "interface_views/semantic_reader.py")
from aggregate_claims import bindings as B
from delta.reprepare import emit_relation_rows
from delta_claims.claims import expected_journal
from mixed_claims.interface_projection import project_frontend_context
from modules import codec as C
from modules.model import ConditionalEnvironment
from modules.source_rows import decode_source

FOUNDATION = C.canonical([{"meta": {}}])  # INERT metadata, not an adopted foundation.
FOUNDATION_SHA = hashlib.sha256(FOUNDATION).hexdigest()
FOUNDATION_VIEW = {"groups": [], "bodies": [], "values": [], "names": []}
NAME = [["s", "item"]]
TYPE = ["sort", ["succ", ["zero"]]]
VALUE = ["sort", ["zero"]]
OBSERVED = {}


def spec_for(*, name=None, typ=None, body=None):
    body = deepcopy(VALUE if body is None else body)
    descriptor = {"kind": "definition", "name": deepcopy(NAME if name is None else name),
        "universes": 0, "type": deepcopy(TYPE if typ is None else typ),
        "value_hash": C.body_id(body, 0), "meta": {"hint": "abbrev", "safety": "safe"}}
    spec = {"schema": C.SPEC_SCHEMA, "foundation": B.FOUNDATION, "policy": B.POLICY,
            "groups": [{"kind": "ordinary", "declarations": [descriptor]}]}
    C.validate_spec(spec)
    return spec, body


def item_for(spec, body=None):
    return {"module": C.module_id(spec), "openings": [C.group_opening(spec, 0)],
        "bodies": [] if body is None else [{"universes": 0, "digest": C.body_id(body, 0),
                                           "expression": deepcopy(body)}]}


def context(items, mode="interface-only"):
    return I._build_context(items, "11" * 32, FOUNDATION, FOUNDATION_SHA,
        deepcopy(FOUNDATION_VIEW), 0, I.RelationBasis(), {}, I._context_limits(None),
        definition_mode=mode)


def inert_session(spec):
    """No authority owners or genuine warrants; retain real lifecycle methods."""
    session = I.MixedImportSession.__new__(I.MixedImportSession)
    session._owners = session._origins = (None, None, None)
    session._profiles = (None, None, None)
    session._basis = I.RelationBasis()
    session._aggregate_image = session._origin_aggregate_image = None
    session._deadline = time.monotonic() + 60
    session._caps = (64, 1024, 128, 4096, 256 * I.MIB, 16 * I.MIB)
    session._closed = False
    session._calls = session._submitted_bytes = session._data_bytes = session._representation_revision = 0
    session._sources, session._receipts, session._nodes = {}, {}, {}
    session._summaries, session._selected, session._groups, session._bodies = {}, {}, {}, {}
    session._sealed = session._batching = False
    session._view = session._view_payload = session._sealed_state = None
    session._definition_mode, session._origin_definition_mode = "eager", None
    session._profile = session._origin_profile = "INERT_INTERFACE_CONTROL_NO_AUTHORITY"
    session._live = lambda: session._active()  # Only installation/owner authority is bypassed.
    session._group = lambda exact, opening: C.verify_group_opening(
        B.member_journal(exact)["module"], opening)  # Hash structure, not issuer authority.
    exact = expected_journal(C.summarize(spec), 0, B.RELATION_IMAGE)
    session._nodes[exact] = (None, "INERT-NOT-A-PROOF", b"INERT-NOT-EVIDENCE", (), "inert")
    session._summaries[C.module_id(spec)] = C.canonical(C.summarize(spec))
    return session, exact


def batch(spec, exact, *, body=None, initial=True):
    return C.canonical({"selected": [list(exact)] if initial else [],
        "openings": [{"module": C.module_id(spec), "opening": C.group_opening(spec, 0)}]
                    if initial else [],
        "bodies": [] if body is None else [{"module": C.module_id(spec), "universes": 0,
                                            "expression": body}]})


class InterfaceControls(unittest.TestCase):
    def setUp(self):
        self.sessions = []
        self.foundation = patch.object(I, "_decode_context_foundation",
            return_value=(deepcopy(FOUNDATION_VIEW), 0))
        self.foundation.start()

    def tearDown(self):
        self.foundation.stop()
        for session in self.sessions:
            session.close()

    def session(self, spec):
        result = inert_session(spec)
        self.sessions.append(result[0])
        return result

    def ready(self, *, body_present=False, mode="interface-only"):
        spec, body = spec_for()
        session, exact = self.session(spec)
        ready, view = session.materialize(batch(spec, exact, body=body if body_present else None),
            FOUNDATION, FOUNDATION_SHA, definition_mode=mode)
        self.assertEqual(ready["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
        return session, spec, ready, view

    def test_absent_body_chain_has_constant_selected_semantic_demand(self):
        observations = []
        for length in (1, 32, 256):
            previous = None
            for index in range(length):
                body = VALUE if previous is None else ["const", ["external", previous, NAME], []]
                spec, body = spec_for(body=body)
                previous = C.module_id(spec)
            selected = [item_for(spec)]
            eager, interface = context(selected, "eager"), context(selected)
            self.assertEqual([row["kind"] for row in eager["demands"]], ["NeedBody"])
            self.assertEqual(interface["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
            self.assertEqual(interface["cost"]["deferred_definition_bodies"], 1)
            self.assertEqual(interface["packet"]["imports"][0]["group"], spec["groups"][0])
            observations.append((length, interface["cost"]["counted_expression_visits"],
                                 interface["cost"]["groups"], len(interface.get("demands", []))))
        self.assertEqual({row[1:] for row in observations}, {(1, 1, 0)})
        OBSERVED["synthetic_hidden_chain_length_visits_groups_demands"] = observations

    def test_missing_type_and_present_body_dependencies_still_demand(self):
        absent = "ab" * 32
        reference = ["const", ["external", absent, NAME], []]
        spec, unused = spec_for(typ=reference)
        result = context([item_for(spec)])
        self.assertEqual(result["demands"], [{"kind": "NeedVerifiedMixedMember", "module": absent, "name": NAME}])
        spec, body = spec_for(body=reference)
        result = context([item_for(spec, body)])
        self.assertEqual(result["demands"], [{"kind": "NeedVerifiedMixedMember", "module": absent, "name": NAME}])
        # Even an already selected module does not substitute for its missing declaration.
        result = context([item_for(spec), {"module": absent, "openings": [], "bodies": []}])
        self.assertEqual(result["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
        type_spec, unused = spec_for(typ=reference)
        result = context([item_for(type_spec), {"module": absent, "openings": [], "bodies": []}])
        self.assertEqual(result["demands"][0]["kind"], "NeedDeclaration")

    def test_projection_copies_only_missing_definition_kind_and_meta(self):
        spec, body = spec_for()
        original = context([item_for(spec)])
        frozen = C.canonical(original)
        projected, report = project_frontend_context(original)
        wanted = deepcopy(original)
        wanted["packet"]["imports"][0]["group"]["declarations"][0].update(
            kind="opaque", meta={"safety": "safe"})
        self.assertEqual(projected, wanted)
        self.assertEqual(C.canonical(original), frozen)
        self.assertIsNot(projected, original)
        self.assertEqual(report["projected_definitions"], 1)
        self.assertFalse(report["mathematical_acceptance"])
        for mode in ("eager", "interface-only"):
            present = context([item_for(spec, body)], mode)
            projected, report = project_frontend_context(present)
            self.assertEqual(projected, present)
            self.assertEqual(report["projected_definitions"], 0)

    def test_invalid_mode_and_projection_binding_refuse(self):
        spec, unused = spec_for()
        for mode in (None, True, "opaque", "INTERFACE-ONLY"):
            with self.assertRaisesRegex(ValueError, "MIXED_AUTHORING_DEFINITION_MODE"):
                context([item_for(spec)], mode)
        ready = context([item_for(spec)])
        bad = deepcopy(ready); bad["packet"]["selection_binding"] = "22" * 32
        with self.assertRaisesRegex(ValueError, "MIXED_FRONTEND_PROJECTION_BINDING"):
            project_frontend_context(bad)
        bad = deepcopy(ready); bad["packet"]["definition_mode"] = False
        with self.assertRaisesRegex(ValueError, "MIXED_AUTHORING_DEFINITION_MODE"):
            project_frontend_context(bad)

    def test_native_emitter_keeps_original_definition_hash_hint(self):
        imported, unused = spec_for()
        local_spec, body = spec_for(name=[["s", "new"]],
            typ=["sort", ["succ", ["succ", ["zero"]]]], body=TYPE)
        local = ConditionalEnvironment(local_spec)
        local.supply_local_value([["s", "new"]], body)
        ready = context([item_for(imported)])
        projected, unused = project_frontend_context(ready)
        self.assertEqual(projected["packet"]["imports"][0]["group"]["declarations"][0]["kind"], "opaque")
        rows = emit_relation_rows(FOUNDATION, local, ready["packet"]["imports"])
        imported_rows = [row["moduleImportDef"] for row in rows if "moduleImportDef" in row]
        self.assertEqual(len(imported_rows), 1)
        descriptor = imported["groups"][0]["declarations"][0]
        self.assertEqual(imported_rows[0]["bodyHash"], list(bytes.fromhex(descriptor["value_hash"])))
        self.assertEqual(imported_rows[0]["hints"], "abbrev")
        self.assertFalse(any("moduleImportOpaque" in row or "axiom" in row for row in rows))

    def test_new_local_axiom_is_rejected_by_real_source_decoder(self):
        spec, body = spec_for(name=[["s", "new"]])
        local = ConditionalEnvironment(spec); local.supply_local_value([["s", "new"]], body)
        rows = emit_relation_rows(FOUNDATION, local, [])
        selected = C.relocated_name(local.module, [["s", "new"]])
        for index, row in enumerate(rows):
            if "def" in row:
                rows[index] = {"axiom": {key: row["def"][key] for key in ("name", "levelParams", "type")}}
        with self.assertRaisesRegex(ValueError, "SOURCE_LOCAL_AXIOM"):
            decode_source(rows, [selected], [], B.FOUNDATION, B.POLICY)

    def test_mode_binds_selection_and_sealed_views_reject_reinterpretation(self):
        eager, spec, eager_ready, eager_view = self.ready(body_present=True, mode="eager")
        interface, unused, interface_ready, interface_view = self.ready(body_present=True)
        self.assertNotEqual(eager_ready["selection_binding"], interface_ready["selection_binding"])
        self.assertNotIn("definition_mode", eager_ready["packet"])
        items, bound = eager.view_selection(eager_view)
        expected = {"profile": eager._profile, "sources": sorted(eager._sources),
            "representation_revision": eager._representation_revision,
            "chosen": [{"journal": list(exact), "proof_form": node[1],
                "evidence_sha256": hashlib.sha256(node[2]).hexdigest(),
                "parents": [list(parent) for parent in node[3]], "source_id": node[4]}
                for exact, node in sorted(eager._nodes.items())],
            "warrants": [[module, list(exact)] for module, exact in sorted(eager._selected.items())],
            "selected": [I._encoded_fact(item) for item in items]}
        self.assertEqual(bound, C.hash_value("mixed-authoring-selection-v1", expected))
        with self.assertRaisesRegex(ValueError, "MIXED_IMPORT_FOREIGN_OR_UNSEALED_VIEW"):
            interface.require_view(eager_view)
        with self.assertRaisesRegex(ValueError, "MIXED_IMPORT_SEALED_OR_BATCH_ACTIVE"):
            interface.materialize(C.canonical({"selected": [], "openings": [], "bodies": []}),
                                 FOUNDATION, FOUNDATION_SHA, definition_mode="eager")

    def test_need_selection_continues_same_mode_to_ready(self):
        dependency, unused = spec_for(name=[["s", "typeInterface"]])
        module = C.module_id(dependency)
        spec, unused = spec_for(typ=["const", ["external", module, [["s", "typeInterface"]]], []])
        session, exact = self.session(spec)
        need, token = session.materialize(batch(spec, exact), FOUNDATION, FOUNDATION_SHA,
                                          definition_mode="interface-only")
        self.assertIsNone(token)
        self.assertEqual(need["status"], "NEED_AUTHORING_CONTEXT_DATA")
        session.require_selection(need["selection_binding"])
        later_exact = expected_journal(C.summarize(dependency), 0, B.RELATION_IMAGE)
        # Add one explicitly INERT pre-established warrant; this is not admission.
        session._nodes[later_exact] = (None, "INERT-NOT-A-PROOF", b"INERT-LATER", (), "inert")
        session._summaries[module] = C.canonical(C.summarize(dependency))
        ready, token = session.materialize(batch(dependency, later_exact), FOUNDATION, FOUNDATION_SHA,
                                           definition_mode="interface-only")
        self.assertEqual(ready["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
        session.require_selection(ready["selection_binding"]); session.require_view(token)
        other, exact = self.session(spec)
        other.materialize(batch(spec, exact), FOUNDATION, FOUNDATION_SHA, definition_mode="interface-only")
        with self.assertRaises(ValueError):
            other.materialize(C.canonical({"selected": [], "openings": [], "bodies": []}),
                              FOUNDATION, FOUNDATION_SHA, definition_mode="eager")
        tampered, unused, unused_ready, token = self.ready()
        tampered._definition_mode = "eager"
        with self.assertRaisesRegex(ValueError, "MIXED_IMPORT_DEFINITION_MODE_CHANGED"):
            tampered.require_view(token)

    def test_source_request_is_projected_but_finish_uses_original_descriptors(self):
        session, spec, ready, view = self.ready()
        local_spec, body = spec_for(name=[["s", "new"]],
            typ=["sort", ["succ", ["succ", ["zero"]]]], body=TYPE)
        local = ConditionalEnvironment(local_spec); local.supply_local_value([["s", "new"]], body)
        roots = [C.relocated_name(local.module, [["s", "new"]])]
        operation = A.MixedSourceOperation(session, FOUNDATION, FOUNDATION_SHA,
            "INERT SOURCE NOT EXECUTED", roots, view=view)
        request = C.parse_json(operation.prepare()["request"])
        self.assertEqual(request["context"]["imports"][0]["group"]["declarations"][0]["kind"], "opaque")
        self.assertEqual(operation._context, ready)
        exported = {"schema": A.EXPORT_SCHEMA, "source_sha256": operation._source_sha,
            "selection_binding": ready["selection_binding"], "roots": roots,
            "rows": emit_relation_rows(FOUNDATION, local, []), "local_names": roots,
            "status": "OWNER_FRONTEND_EXPORT_REQUIRES_INDEPENDENT_RELATION", "mathematical_acceptance": False}
        captured = []
        def inert_onward(witness, binding, envelope):
            captured.append(deepcopy(witness))
            return b"INERT-NOT-A-PACKET", {"inert": True}
        with patch.object(session, "onward_packet", side_effect=inert_onward):
            result = operation.finish(C.canonical(exported))
        self.assertFalse(result["mathematical_acceptance"])
        self.assertEqual(len(captured), 1)
        rows = captured[0]["rows"]
        self.assertEqual(len([row for row in rows if "moduleImportDef" in row]), 1)
        self.assertFalse(any("moduleImportOpaque" in row or "axiom" in row for row in rows))
        self.assertEqual(captured[0]["parents"][0]["openings"][0]["group"], spec["groups"][0])
        fresh = A.MixedSourceOperation(session, FOUNDATION, FOUNDATION_SHA,
            "INERT SOURCE NOT EXECUTED", roots, view=view)
        exported["selection_binding"] = "ff" * 32
        with self.assertRaisesRegex(ValueError, "MIXED_SOURCE_EXPORT_BINDING"):
            fresh.finish(C.canonical(exported))

    def test_public_reader_staged_preview_and_direct_import_forward_mode(self):
        """Actual public bodies with INERT grant, custody and issuer shells."""
        spec, unused = spec_for(); module = C.module_id(spec)
        session, exact = self.session(spec)
        opening = C.group_opening(spec, 0)
        selected = {"module": module, "journal": list(exact), "summary": C.summarize(spec),
                    "packet_sha256": "33" * 32, "packet_bytes": 1}
        token = W.StagedEvidence()
        grant = SimpleNamespace(_limits={"imports": {"max_sources": 64, "max_members": 128,
                                                      "data_bytes": 16 * I.MIB}},
                                remaining_seconds=lambda: 60)
        shell = SimpleNamespace(grant=grant, _foundation=FOUNDATION, _foundation_sha=FOUNDATION_SHA,
            _staging_counts={"previews": 0}, _charge=lambda raw: None,
            _stage=lambda candidate, unused: ({"selection": selected,
                "members": [{"module": module, "journal": list(exact), "summary": C.summarize(spec)}]}, False),
            _store=lambda action, *args: action(*args),
            workspace=SimpleNamespace(modules=SimpleNamespace(get_group=lambda *args: (opening, None))))
        # Preserve actual staged-token/member selection and actual structural preview.
        shell.preview_context = lambda *args, **kwargs: W.CommonsClient.preview_context.__wrapped__(
            shell, *args, **kwargs)
        reader = H.SemanticReader.__new__(H.SemanticReader)
        reader._client, reader._grant = shell, grant
        reader._definition_mode = reader._origin_definition_mode = "interface-only"
        reader._active = lambda: None  # No owner/client authority is asserted by this fixture.
        reader._state, reader._busy = "COLLECTING", False
        reader._steps = reader._bytes = reader._revision = 0
        reader._limits = dict(H.LIMITS)
        reader._selected = {module: (token, C.canonical(selected), b"[]")}
        reader._members = {module: (module, C.canonical(selected))}
        reader._groups, reader._bodies, reader._pending = {(module, 0): C.canonical(opening)}, {}, {}
        reader._ready_revision = None
        with patch.object(S, "_decode_context_foundation", return_value=(deepcopy(FOUNDATION_VIEW), 0)):
            result = reader.preview()
        self.assertEqual(result["status"], "STRUCTURAL_CLOSURE_STAGED")
        self.assertEqual(result["definition_mode"], "interface-only")
        self.assertEqual(shell._staging_counts["previews"], 1)
        shell._session = None
        shell.receipt = shell.aggregate = shell.delta = None
        shell._counts = {"new_import_sessions": 0}
        shell._context_data = lambda *args: E.CommonsClient._context_data(shell, *args)
        with patch.object(E, "MixedImportSession", return_value=session):
            result = E.CommonsClient.import_context.__wrapped__(shell, [], [exact],
                [{"module": module, "opening": opening}], [], definition_mode="interface-only")
        self.assertEqual(result["status"], "UNTRUSTED_AUTHORING_CONTEXT_READY")
        self.assertEqual(session._definition_mode, "interface-only")
        self.assertEqual(shell._counts["new_import_sessions"], 1)
        shell.preview_context = lambda *args, **kwargs: {"definition_mode": "eager"}
        with self.assertRaisesRegex(ValueError, "SEMANTIC_READER_PREVIEW_MODE"):
            reader.preview()


SELECTED = (
    "test_absent_body_chain_has_constant_selected_semantic_demand",
    "test_missing_type_and_present_body_dependencies_still_demand",
    "test_projection_copies_only_missing_definition_kind_and_meta",
    "test_invalid_mode_and_projection_binding_refuse",
    "test_native_emitter_keeps_original_definition_hash_hint",
    "test_new_local_axiom_is_rejected_by_real_source_decoder",
    "test_mode_binds_selection_and_sealed_views_reject_reinterpretation",
    "test_need_selection_continues_same_mode_to_ready",
    "test_source_request_is_projected_but_finish_uses_original_descriptors",
    "test_public_reader_staged_preview_and_direct_import_forward_mode",
)


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    output = Path(sys.argv[2])
    if not output.is_dir() or output.resolve() != output:
        raise ValueError("EXISTING_CANONICAL_OUTPUT_REQUIRED")
    suite = unittest.TestSuite(InterfaceControls(name) for name in SELECTED)
    with patch.object(subprocess, "Popen", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_exec", side_effect=AssertionError("NATIVE_FORBIDDEN")), \
         patch.object(asyncio, "create_subprocess_shell", side_effect=AssertionError("NATIVE_FORBIDDEN")):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    report = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "scope": "PURE_INTERFACE_CONTEXT_EMISSION_WITH_INERT_SESSION_AUTHORITY",
        "selected": list(SELECTED), "observed": OBSERVED, "native_calls": 0, "proof_calls": 0,
        "mathematical_acceptance": False}
    with (output / "controls-result.json").open("x", encoding="utf-8") as target:
        json.dump(report, target, sort_keys=True, indent=2)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
