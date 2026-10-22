"""Narrow renewal controls: real shape algorithms, explicitly INERT authority.

Only root selects/runs this file. The retained fixture is comparison data, not
a genuine A receipt. No native checker, proof stage, DB or service is opened.
"""
import asyncio
from contextlib import ExitStack
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MAP = PROJECT/"experiments/v5-local-checks/distribution-candidate-preflight-01-input.json"
MAP_SHA = "25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364"
FIXTURE = PROJECT/"experiments/v5-local-checks/restricted-composition-controls-01/evidence/fixture.json"
FIXTURE_SHA = "019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a"
SELF = "software/v5/typed_renewal/controls02.py"
ADDITIONS = {"v5/typed_renewal/"+name: "software/v5/typed_renewal/"+name for name in
             ("__init__.py", "source.py", "owner.py", "controls02.py")}
# Producer-only pure helpers are test support, not product130 additions.
ADDITIONS.update({
    "v5/aggregate_claims/prepare_mixed.py": "software/v5/aggregate_claims/prepare_mixed.py",
    "v5/aggregate_claims/input.py": "software/v5/aggregate_claims/input.py",
})
SELECTED = (
    "test_01_retained_semantics_and_structural_seal",
    "test_02_material_and_packet_refusals",
    "test_03_exact_source_and_decoded_edge_with_inert_decoder",
    "test_04_separate_preparation_refuses_wrong_return",
    "test_05_inert_owner_success_order",
    "test_06_inert_owner_failure_cleanup",
)
OBSERVED, FORBIDDEN, SOURCE_ROWS = {}, [], {}


def need(ok, reason):
    if not ok:
        raise AssertionError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ordinary(path):
    need(path.is_absolute() and path.resolve() == path and all(
        not part.is_symlink() and not part.is_junction() for part in (path, *path.parents)),
        "RENEWAL_CONTROL_ORDINARY")
    return path


def write_new(path, raw):
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "RENEWAL_CONTROL_WRITE")


def forbidden(*args, **kwargs):
    FORBIDDEN.append("FORBIDDEN_EXTERNAL_OR_DB_CALL")
    raise AssertionError(FORBIDDEN[-1])


def stage(output):
    selection = json.loads((output/"selection.json").read_bytes())
    pins, snapshot = selection["sources"], output/"sources"
    need(len(pins) == 137 and Path(__file__).resolve() == snapshot/SELF,
         "RENEWAL_CONTROL_EXACT_SNAPSHOT")
    need(sha((snapshot/SELF).read_bytes()) == pins[SELF], "RENEWAL_CONTROL_SELF_PIN")
    raw = ordinary(MAP).read_bytes()
    need(len(raw) == 2813950 and sha(raw) == MAP_SHA, "RENEWAL_CONTROL_MAP_PIN")
    basis = json.loads(raw)["sdk_sources"]
    need(len(basis) == 130 and not set(basis) & set(ADDITIONS), "RENEWAL_CONTROL_DISJOINT_ADDITIONS")
    code = output/"selected-code"; code.mkdir()
    for logical in sorted(set(basis) | set(ADDITIONS)):
        if logical in ADDITIONS:
            relative = ADDITIONS[logical]; expected = pins[relative]
        else:
            row = basis[logical]
            relative = Path(row["path"]).relative_to(PROJECT).as_posix()
            expected = row["sha256"]
            need(pins[relative] == expected, "RENEWAL_CONTROL_BASE_PIN")
        data = ordinary(snapshot/relative).read_bytes()
        need(0 < len(data) <= 2*1024**2 and sha(data) == expected, "RENEWAL_CONTROL_SOURCE_PIN")
        target = code/logical; target.parent.mkdir(parents=True, exist_ok=True)
        write_new(target, data)
        need(target.read_bytes() == data, "RENEWAL_CONTROL_SOURCE_READBACK")
        SOURCE_ROWS[logical] = dict(source=relative, bytes=len(data), sha256=expected)
    need(len(SOURCE_ROWS) == 136 and not any(name in sys.modules for name in
         ("admission", "aggregate_claims", "client", "modules", "typed_renewal")),
         "RENEWAL_CONTROL_IMPORT_ORDER")
    raw = ordinary(FIXTURE).read_bytes()
    need(len(raw) == 84727 and sha(raw) == FIXTURE_SHA, "RENEWAL_CONTROL_FIXTURE_PIN")
    sys.path[:0] = [str(code/"v5"), str(code/"portable")]
    return raw


def material_and_packet():
    """Synthetic header/receipt; retain real U/V specifications and V witness.

    The opaque sibling is not evidence that any second mathematical member
    exists. This constructs only a self-consistent membership opening, never
    passes it to a verifier, and must not be counted as actual A admission.
    """
    parent = DATA["second"]["parents"][0]
    exact = bytes(parent["journal"])
    sibling = b"\x55"*32
    root = B._root(2, B._node(2, 0, B._leaf(2, 0, exact), sibling))
    header = (B.MAGIC+B.VERSION.to_bytes(4, "little")+bytes.fromhex(S.A_IMAGE)
        +bytes.fromhex(B.RELATION_IMAGE)+bytes.fromhex(B.FOUNDATION)+bytes.fromhex(B.POLICY)
        +root+(2).to_bytes(4, "little")+(1).to_bytes(8, "little")+(1).to_bytes(8, "little"))
    material = dict(schema=S.MATERIAL_SCHEMA, receipt=b"INERT-NOT-A-RECEIPT", header=header,
        journal=exact, member_index=0, siblings=[sibling], opening=deepcopy(parent["openings"][0]))
    value = dict(schema=MP.SCHEMA,
        claims=[dict(tag=1, statement=list(header), receipt_hex=material["receipt"].hex())],
        frontiers=[dict(claim_index=0, journal=list(exact), member_index=0, siblings=[list(sibling)])],
        deltas=[deepcopy(DATA["second_witness"])])
    raw = C.canonical(value)
    target = EXPECTED(C.summarize(DATA["second"]["local_spec"]), 2, B.RELATION_IMAGE)
    envelope = MP.Envelope(packet_bytes=1024**2, receipt_bytes=4096, witness_bytes=512*1024)
    return material, value, raw, target, envelope


class Controls(unittest.TestCase):
    def reject(self, call, reason, exception=None):
        with self.assertRaises(C.StructureError if exception is None else exception) as caught:
            call()
        self.assertEqual(str(caught.exception), reason)
        self.assertEqual(FORBIDDEN, [])

    def test_01_retained_semantics_and_structural_seal(self):
        material, unused, raw, target, envelope = material_and_packet()
        parsed = S.validate_material(material)
        self.assertEqual((parsed["module"], parsed["rank"]), (S.U_MODULE, 1))
        self.assertEqual(sha(material["journal"]), S.U_J_SHA)
        self.assertEqual(C.module_id(DATA["second"]["local_spec"]), S.V_MODULE)
        self.assertEqual(DATA["second_witness"]["local_spec"], DATA["second"]["local_spec"])
        shape = S.validate_renewal_packet(raw, target, material, envelope=envelope)
        calls = []
        class InertProducer:
            def prepare(inner, packet, exact, *, envelope):
                calls.append((packet, exact))
                return SEAL(packet, exact, adopted_image=S.A_IMAGE, envelope=envelope)
            snapshot = forbidden
            run = forbidden
        prepared = S.prepare_renewal(InertProducer(), raw, target, material, envelope=envelope)
        self.assertEqual(calls, [(raw, target)])
        self.assertFalse(prepared.mathematical_admission)
        self.assertEqual(prepared.status, "UNTRUSTED_MIXED_SEAL_PREPARATION")
        self.assertEqual(prepared.members, tuple(sorted((material["journal"], target))))
        self.assertEqual(prepared.parents[0].receipt, material["receipt"])
        self.assertEqual(shape["witness"]["parents"], [dict(journal=list(material["journal"]),
                                                           openings=[material["opening"]])])
        self.assertEqual(shape["witness"]["bodies"], [])
        OBSERVED[self._testMethodName] = dict(scope="REAL_PINNED_FIXTURE_AND_PURE_PACKET_SEAL_ALGORITHMS",
            synthetic_receipt=True, synthetic_membership_companion=True, U=S.U_MODULE, V=S.V_MODULE,
            packet_bytes=len(raw), claims=1, frontiers=1, deltas=1, members=2, edges=1,
            rank=2, height=2, actual_cryptographic_verifications=0)

    def test_02_material_and_packet_refusals(self):
        material, value, raw, target, envelope = material_and_packet()
        self.reject(lambda: S.validate_material({**material, "witness": DATA["first_witness"]}),
                    "EXACT_RECORD_FIELDS")
        self.reject(lambda: S.validate_material({**material, "receipt": b""}),
                    "RENEWAL_ACTUAL_RECEIPT_REQUIRED")
        self.reject(lambda: S.validate_material({**material, "journal": target}), "RENEWAL_EXACT_U_JOURNAL")
        bad = deepcopy(material); bad["header"] = material["header"][:-8]+(2).to_bytes(8, "little")
        self.reject(lambda: S.validate_material(bad), "RENEWAL_U_AGGREGATE_SHAPE")
        # A structurally valid terminal-I substitution must still be rejected.
        wrong = deepcopy(value)
        wrong["claims"] = [dict(tag=0, statement=list(material["journal"]), receipt_hex="01")]
        wrong["frontiers"][0].update(member_index=0, siblings=[])
        self.reject(lambda: S.validate_renewal_packet(C.canonical(wrong), target, material,
                    envelope=envelope), "RENEWAL_SOLE_A_CLAIM")
        wrong = deepcopy(value); wrong["claims"][0]["receipt_hex"] = "02"
        self.reject(lambda: S.validate_renewal_packet(C.canonical(wrong), target, material,
                    envelope=envelope), "RENEWAL_SOLE_A_CLAIM")
        self.reject(lambda: S.validate_renewal_packet(raw, material["journal"], material,
                    envelope=envelope), "RENEWAL_EXACT_V_JOURNAL")
        OBSERVED[self._testMethodName] = dict(scope="REAL_STRUCTURAL_REFUSALS_NO_AUTHORITY", cases=7)

    def test_03_exact_source_and_decoded_edge_with_inert_decoder(self):
        material, unused, unused_raw, unused_target, unused_env = material_and_packet()
        text = S.v_source(); name = C.relocated_name(S.U_MODULE, S.U_NAME)
        quoted = ".".join("\u00ab"+part[1]+"\u00bb" for part in name)
        self.assertEqual(text.count(quoted), 1)
        self.assertEqual(text.count("@Eq.trans.{z}"), 1)
        self.assertTrue(text.startswith("universe u v w z\n"))
        self.assertIn(".{u, v, w, z} A B C D f g h a aa b bb c cc ha hb hc) hd", text)
        self.assertNotIn("sorry", text)
        request = dict(source=text, source_sha256=sha(text.encode()), roots=[S.V_NAME], context=dict(
            definition_mode="interface-only", foundation_view=dict(names=[]), imports=[dict(
                owner=S.U_MODULE, index=0, group=material["opening"]["group"], bodies=[])]))
        exported = dict(roots=[S.V_NAME], source_sha256=request["source_sha256"],
                        rows=[{"INERT_DECODER_INPUT": True}], local_names=[S.V_NAME])
        proof = DATA["second"]["proofs"][0]
        def inspect(selected):
            env = MODEL(DATA["second"]["local_spec"])
            env.supply_local_value(S.V_NAME, selected)
            # Explicitly doubled decoder, NOT an actual frontend export. Real
            # conditional model and exact proof-edge inspection remain in use.
            with patch.object(S, "decode_source", return_value=env) as decoder:
                result = S.inspect_source_export(request, exported, DATA["second_witness"], material)
                self.assertEqual(decoder.call_args.args[5], [dict(source_name=name,
                    module=S.U_MODULE, relative_name=S.U_NAME)])
                return result
        result = inspect(proof)
        self.assertTrue(result["exact_U_feeds_trans"])
        self.assertEqual(result["proof_sha256"], sha(C.canonical(proof)))
        # Preserve one U and one Eq.trans while reversing their proof arguments.
        wrong = deepcopy(proof); tail = wrong
        for unused in range(18): tail = tail[3]
        tail[2], tail[1][2] = tail[1][2], tail[2]
        self.reject(lambda: inspect(wrong), "RENEWAL_EXACT_U_FEEDS_TRANS")
        wrong = deepcopy(proof); wrong[1] = "default"
        self.reject(lambda: inspect(wrong), "RENEWAL_EXACT_PROOF_TELESCOPE")
        OBSERVED[self._testMethodName] = dict(scope="REAL_FIXED_SOURCE_AND_AST_INSPECTION_WITH_INERT_DECODER",
            actual_frontend_runs=0, exact_retained_proof=True, same_occurrence_wrong_edge_refused=True)

    def test_04_separate_preparation_refuses_wrong_return(self):
        material, unused, raw, target, envelope = material_and_packet()
        good = SEAL(raw, target, adopted_image=S.A_IMAGE, envelope=envelope)
        cases = ((replace(good, parents=()), "RENEWAL_PREPARED_A_PARENT"),
                 (replace(good, mathematical_admission=True), "RENEWAL_PREPARED_A_PARENT"),
                 (replace(good, input_sha256="00"*32), "RENEWAL_PREPARED_A_PARENT"),
                 (replace(good, selected_delta_indices=()), "RENEWAL_PREPARED_EXACT_SELECTION"),
                 (replace(good, census=replace(good.census, edges=0)), "RENEWAL_PREPARED_CENSUS"),
                 (replace(good, expected_header=good.expected_header[:-8]+(3).to_bytes(8, "little")),
                  "RENEWAL_PREPARED_RANK_HEIGHT"))
        for value, reason in cases:
            with self.subTest(reason=reason):
                producer = SimpleNamespace(prepare=lambda *args, **kwargs: value,
                                           snapshot=forbidden, run=forbidden)
                self.reject(lambda: S.prepare_renewal(producer, raw, target, material, envelope=envelope), reason)
        OBSERVED[self._testMethodName] = dict(scope="PREPARE_RETURN_VALIDATION_WITH_EXPLICIT_PRODUCER_DOUBLE", cases=len(cases))

    def owner_case(self, fault=None):
        material, unused, raw, target, envelope = material_and_packet()
        events, saved = [], {}
        work = OUTPUT/"INERT-NO-OWNER-STATE"
        paths = dict(workspace_path=work/"workspace", domain_path=work/"domain")
        context = SimpleNamespace(location_workspace=work, deadline=time.monotonic()+30)
        params = dict(runtime_adoption=dict(receipt=None, aggregate=dict(image=S.A_IMAGE)),
            workspace_config=dict(wire_profile=dict(aggregate_image=S.A_IMAGE),
                                  packet_envelope=dict(envelope.__dict__)),
            domain_id="33"*32, operation_limits={}, receipt_limits={}, author_limits={}, admission_limits={})
        pins = dict(foundation=b"INERT-NOT-A-FOUNDATION", receipt=material["receipt"], header=material["header"],
            journal=material["journal"], membership=C.canonical(dict(index=0, siblings=[material["siblings"][0].hex()])),
            opening=C.canonical(material["opening"]))
        params.update({name: name for name in pins})
        trust = dict(domain_id="33"*32, support_id="44"*32, adoption_sha256="55"*32)
        grant = SimpleNamespace(identifier="INERT-GRANT", directory=work/"grant", remaining_seconds=lambda: 10)
        parent_token, child_token, context_token = object(), object(), object()
        request_raw, export_raw = b"{}", b"{}"
        worker = dict(status="PASS_NATIVE_EXPORT_ONLY", request_sha256=sha(request_raw),
            export_sha256=sha(export_raw), export_bytes=len(export_raw), native_return_code=0,
            native_timed_out=False, direct_child_reaped=True)
        def event(name):
            events.append(name)
            if fault == name: raise RuntimeError("INERT_FAULT:"+name)
        class InertDomain:
            def identity(inner): return deepcopy(trust)
            def withdraw(inner, reason): event("withdraw")
        domain = InertDomain()
        class InertClient:
            def admit_aggregate_member(inner, receipt, header, exact, index, siblings, **kwargs):
                event("verify-A")
                self.assertEqual((receipt, header, exact, index, siblings), (material["receipt"],
                    material["header"], material["journal"], 0, material["siblings"]))
                return parent_token
            def describe(inner, token):
                if token is parent_token:
                    return dict(kind="A-member", live=dict(journal=material["journal"], module=S.U_MODULE))
                self.assertIs(token, child_token)
                return dict(kind="mixed", live=dict(journal=target, module=S.V_MODULE,
                    summary=C.summarize(DATA["second"]["local_spec"]), packet_sha256=sha(raw)))
            def import_context(inner, warrants, selected, openings, bodies, **kwargs):
                event("import")
                self.assertEqual(warrants, [dict(warrant=parent_token, resolutions=None)])
                self.assertEqual(selected, [material["journal"]])
                self.assertEqual(openings, [dict(module=S.U_MODULE, opening=material["opening"])])
                self.assertEqual((bodies, kwargs), ([], dict(definition_mode="interface-only")))
                return dict(status="UNTRUSTED_AUTHORING_CONTEXT_READY", demands=[], context=context_token,
                    cost=dict(groups=1, declarations=1, frontend_theorem_ancestor_proof_bytes=0))
            def author(inner, author_context, source, roots, **kwargs):
                event("author")
                self.assertIs(author_context, context_token)
                self.assertEqual((source, roots), (S.v_source(), [S.V_NAME]))
                return dict(status="UNTRUSTED_MIXED_DELTA_PACKET_PREPARED", mathematical_acceptance=False,
                    child=dict(packet=raw, summary=C.summarize(DATA["second"]["local_spec"]), local_module=S.V_MODULE,
                        roots=[S.V_NAME], packet_sha256=sha(raw), source_sha256=sha(source.encode())))
            def admit_local(inner, module, digest, size, **kwargs):
                event("admit-V")
                self.assertEqual((module, digest, size, kwargs["expected_exact_journal"]),
                                 (S.V_MODULE, sha(raw), len(raw), target))
                return child_token
            def report(inner): return dict(scope="INERT_CLIENT_REPORT")
            async def close(inner):
                event("client-close")
                return dict(closed=True, cleanup_uncertain=False, receipt=None, aggregate=dict(closed=True),
                    mixed=dict(closed=True), preparation=dict(closed=True), status="CLOSED", failures=[])
        client = InertClient()
        def put(module, packet, *, before_commit):
            event("put")
            self.assertEqual((module, packet), (S.V_MODULE, raw)); before_commit()
        workspace = SimpleNamespace(packets=SimpleNamespace(put=put))
        def reserve(*args, **kwargs): event("reserve"); return grant
        workspace.reserve = reserve
        def open_operation(*args, **kwargs):
            event("open-operation")
            self.assertEqual(kwargs["mode"], "validated"); self.assertTrue(kwargs["authoring"])
            return client
        runtime = SimpleNamespace(open_operation=open_operation)
        def support(*args): event("support"); return {"INERT": True}
        def create(*args): event("create-domain"); return domain
        def bind(*args, **kwargs): event("runtime"); self.assertIs(kwargs["trust_domain"], domain); return runtime
        def open_workspace(*args, **kwargs): event("workspace"); return workspace
        def close_workspace(*args): event("workspace-close"); return True
        def raw_read(path, maximum=16*1024**2):
            if path.name == "WITHDRAWN":
                return C.canonical(dict(schema="DMKN_LOCAL_TRUST_WITHDRAWN_V1", adoption=trust))
            return {"mixed-packet.json": raw, "source-request.json": request_raw,
                    "EXPORT.json": export_raw, "worker-result.json": C.canonical(worker)}[path.name]
        def save_bytes(path, data):
            event("save-"+path.name); saved[path.name] = data
            return dict(path=str(path), bytes=len(data), sha256=sha(data))
        helper = SimpleNamespace(**{name: getattr(S, name) for name in
            ("A_IMAGE", "U_MODULE", "V_MODULE", "V_NAME", "MATERIAL_SCHEMA", "validate_material",
             "v_source", "validate_renewal_packet")}, inspect_source_export=lambda *args: {"INERT_DECODER": True})
        with ExitStack() as stack:
            for name, value in dict(ordinary=lambda value, **kwargs: Path(value),
                _parameters=lambda unused: (deepcopy(params), paths), _helper=lambda unused: helper,
                read_pin=lambda key, maximum: pins[key], _raw=raw_read, _save_bytes=save_bytes,
                RuntimeProfile=SimpleNamespace(support_manifest=support, from_context=bind),
                TrustDomain=SimpleNamespace(create=create), Workspace=SimpleNamespace(open=open_workspace),
                _close_workspace=close_workspace).items():
                stack.enter_context(patch.object(O, name, value))
            stack.enter_context(patch.object(O.remote_reader, "_save", lambda path, value: saved.update(report=deepcopy(value))))
            report = asyncio.run(O.run(context))
        self.assertEqual(report, saved["report"])
        self.assertFalse(work.exists())
        self.assertEqual((report["snapshot_calls"], report["cryptographic_production_calls"], report["network_calls"]), (0, 0, 0))
        return report, events, saved

    def test_05_inert_owner_success_order(self):
        report, events, saved = self.owner_case()
        self.assertEqual(report["status"], "COMPLETED")
        self.assertEqual(events, ["support", "create-domain", "runtime", "workspace", "reserve", "open-operation",
            "verify-A", "import", "author", "put", "admit-V", "save-V.packet.json", "save-V.journal", "save-V.lean",
            "client-close", "workspace-close", "withdraw"])
        self.assertTrue(report["client_closed"] and report["workspace_closed"] and report["domain_withdrawn"])
        self.assertFalse(report["mathematical_acceptance"])
        self.assertEqual(saved["V.journal"], material_and_packet()[3])
        OBSERVED[self._testMethodName] = dict(scope="REAL_OWNER_FLOW_WITH_INERT_AUTHORITY_IO_AND_CLIENT_SEAMS",
            actual_cryptographic_verifications=0, actual_native_checks=0, actual_domain_creations=0)

    def test_06_inert_owner_failure_cleanup(self):
        faults = ("create-domain", "runtime", "workspace", "open-operation", "verify-A", "author", "admit-V",
                  "client-close", "workspace-close", "withdraw")
        for fault in faults:
            with self.subTest(fault=fault):
                report, events, saved = self.owner_case(fault)
                self.assertEqual(report["status"], "FAILED")
                if fault == "create-domain":
                    self.assertEqual(report["domain_creation"], "ATTEMPTED_STATE_UNCONFIRMED")
                    self.assertFalse(report["domain_withdrawn"]); self.assertNotIn("withdraw", events)
                else:
                    self.assertIn("withdraw", events)
                    self.assertEqual(report["domain_withdrawn"], fault != "withdraw")
                if fault in ("verify-A", "author", "admit-V", "client-close", "workspace-close", "withdraw"):
                    self.assertIn("client-close", events); self.assertIn("workspace-close", events)
                if fault in ("create-domain", "runtime", "workspace", "open-operation", "verify-A", "author", "admit-V"):
                    self.assertNotIn("V.journal", saved)
        OBSERVED[self._testMethodName] = dict(scope="REAL_OWNER_FAILURE_FLOW_WITH_EXPLICIT_INERT_FAILURES",
            cases=len(faults), no_db_no_native_no_trust_state=True)


def main():
    global OUTPUT, C, B, S, O, MP, EXPECTED, SEAL, DATA, MODEL
    need(len(sys.argv) == 3 and sys.argv[1] == "--output", "RENEWAL_CONTROL_OUTPUT")
    OUTPUT = ordinary(Path(sys.argv[2]))
    need(OUTPUT.is_dir() and OUTPUT.is_relative_to(PROJECT) and os.name == "nt"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "RENEWAL_CONTROL_ISOLATED_WINDOWS")
    fixture_raw = stage(OUTPUT)
    with patch.object(subprocess, "Popen", forbidden), patch.object(os, "system", forbidden), \
         patch.object(sqlite3, "connect", forbidden), \
         patch.object(asyncio, "create_subprocess_exec", forbidden), \
         patch.object(asyncio, "create_subprocess_shell", forbidden):
        from modules import codec
        from modules.model import ConditionalEnvironment
        from aggregate_claims import bindings
        from aggregate_claims.prepare_mixed import prepare_mixed_seal
        from delta_claims.claims import expected_journal
        from mixed_claims import packet
        from typed_renewal import source, owner
        C, B, S, O, MP = codec, bindings, source, owner, packet
        EXPECTED, SEAL, MODEL = expected_journal, prepare_mixed_seal, ConditionalEnvironment
        DATA = C.parse_json(fixture_raw)
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(Controls(name) for name in SELECTED))
    passed = result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped and not FORBIDDEN
    report = dict(schema="DMKN_TYPED_RENEWAL_CONTROLS_V1", harness_revision=2, status="PASS" if passed else "FAIL",
        selected=list(SELECTED), tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        skipped=len(result.skipped), forbidden_calls=FORBIDDEN, sources=SOURCE_ROWS, observations=OBSERVED,
        source_map_sha256=MAP_SHA, fixture_sha256=FIXTURE_SHA, mathematical_acceptance=False,
        native_calls=0, proof_calls=0, actual_cryptographic_verifications=0,
        scope="PINNED_FIXTURE_PURE_SHAPES_AND_EXPLICITLY_INERT_DECODER_CLIENT_IO_AUTHORITY")
    write_new(OUTPUT/"typed-renewal-controls-result.json",
        json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()+b"\n")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
