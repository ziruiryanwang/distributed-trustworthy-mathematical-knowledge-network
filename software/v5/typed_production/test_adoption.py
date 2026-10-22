"""Focused typed adoption controls: one real binding pass, no native dispatch.

Real retained files/profile/request are selected by the enclosing owner. Later
record-mutation controls explicitly replace reads/checks on shallow owner clones;
they test validation logic, not disk binding or cryptographic verification.
No compiler, guest, proof stage, receipt verifier or network is executed.
"""
from contextlib import redirect_stdout
from copy import copy, deepcopy
import argparse
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE))
from production import producer as P
from aggregate_small import producer as S, operator as O
from aggregate_lifecycle import snapshot as N
from typed_production import producer as T, host_adoption as H
from typed_production import image_adoption as I, snapshot_adoption as R
from typed_production import operator as Q

CONTEXT = None
OPTIONS = None
OUTPUT = None
DISPATCHES = []


def forbidden_dispatch(*args, **kwargs):
    DISPATCHES.append("FORBIDDEN_PROCESS_DISPATCH")
    raise AssertionError("This adoption suite must never dispatch a process")


def require_equal(actual, expected):
    if actual != expected:
        raise AssertionError((actual, expected))


class Context:
    def __init__(self):
        self.owner = None
        self.reads = {}
        self.profile, self.profile_pin = O.document(OPTIONS.profile, OPTIONS.profile_sha256)
        self.request, self.request_pin = O.document(OPTIONS.request, OPTIONS.request_sha256)
        original_read = P.Producer._read

        def capture(support, pin, maximum=P.MIB):
            raw = original_read(support, pin, maximum)
            old = self.reads.get(pin["path"])
            if old is not None and old != raw:
                raise AssertionError("Real bound read changed during controls")
            self.reads[pin["path"]] = raw
            if sum(map(len, self.reads.values())) > 16*P.MIB:
                raise AssertionError("Control capture bound exceeded")
            return raw

        try:
            with patch.object(P.Producer, "_read", capture):
                self.owner = T.TypedLifecycleProducer(self.profile)
                self.profile_document = self.owner.profile_document()
                quotes = []
                real_preflight = self.owner.preflight

                def quoted(request):
                    result = real_preflight(request)
                    quotes.append(deepcopy(result))
                    return result

                request = self.request
                with patch.object(self.owner, "preflight", quoted):
                    rebuilt = self.owner.production_request(
                        request["session"]["snapshot_evidence"],
                        **{key: request[key] for key in (
                            "allowance_id", "budget", "checkpoints", "prior_attempts",
                            "output_directory", "stage_limit", "carried_external_costs")})
                require_equal(rebuilt, request)
                require_equal(len(quotes), 1)
                self.quote = quotes[0]
            self.retained_pins = request["session"]["snapshot_evidence"]
            self.retained = {role: P.parse(self.reads[pin["path"]])
                             for role, pin in self.retained_pins.items()}
            self.image_pins = self.profile["base_profile"]["image_adoption"]
            self.host_pins = self.profile["base_profile"]["host_build"]
            self.expected = self.reads[request["session"]["expected"]["path"]]
        except BaseException:
            if self.owner is not None:
                self.owner.close()
            raise

    def logical(self, changes=None):
        """Explicit non-binding double, never passed as a production owner.

        Original captured reads were genuinely verified once. Mutated bytes are
        injected *after* that boundary to exercise structural field checks. File
        hashes are not recomputed here; pin/path shape and real file-prefix reads
        in unchanged request plumbing remain, but this is not another adoption.
        """
        owner = copy(self.owner)
        owner.profile = deepcopy(self.owner.profile)
        owner._pins = deepcopy(self.owner._pins)
        owner._lifecycle_profile = deepcopy(self.owner._lifecycle_profile)
        owner._history = deepcopy(self.owner._history)
        replacements = {} if changes is None else changes
        owner.control_read_paths = []
        owner.control_check_calls = []

        def read(pin, maximum=P.MIB):
            path = str(P.pin_fields(pin, maximum))
            if path not in self.reads:
                raise AssertionError("Unexpected uncaptured logical read: "+path)
            raw = replacements.get(path, self.reads[path])
            if not isinstance(raw, bytes) or len(raw) > maximum:
                raise AssertionError("Logical read fixture malformed")
            owner.control_read_paths.append(path)
            return raw

        def check(pins):
            for path, pin in pins.items():
                require_equal(str(P.pin_fields(pin)), path)
            owner.control_check_calls.append(tuple(pins))

        owner._read = read
        owner._check = check
        return owner

    def changed(self, pins, role, mutate):
        path = pins[role]["path"]
        value = P.parse(self.reads[path])
        mutate(value)
        return {path: P.encoded(value)}


class TypedAdoptionControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global CONTEXT
        CONTEXT = Context()

    @classmethod
    def tearDownClass(cls):
        CONTEXT.owner.close()
        require_equal(CONTEXT.owner.report()["closed"], True)
        require_equal(DISPATCHES, [])

    def reject(self, function, reason):
        with self.assertRaises(P.ProductionError) as caught:
            function()
        self.assertEqual(str(caught.exception), reason)
        self.assertEqual(DISPATCHES, [])

    def test_real_retained_adoption_and_full_graph_quote(self):
        c = CONTEXT
        self.assertEqual(c.profile_document, c.profile)
        self.assertEqual(c.owner.profile_id,
                         P.hash_bytes(T.PROFILE_DOMAIN+P.encoded(c.profile)))
        q, request = c.quote, c.request
        self.assertEqual(q["status"], "PASS_REQUEST_PREFLIGHT_ONLY")
        self.assertEqual((q["host_calls"], q["proof_calls"], q["mathematical_admission"], q["funding"]),
                         (0, 0, False, False))
        self.assertEqual((request["session"]["segments"], request["session"]["assumptions"]), (36, 1))
        self.assertEqual(c.retained["result"]["status"], "FAIL_RC_INVESTMENT_SCREEN")
        self.assertEqual(c.retained["outer"]["result"]["child_exit_code"], 1)
        self.assertFalse(Path(request["output_directory"]).exists())
        nodes = S.graph(36, 1)
        self.assertEqual(len(nodes), 109)
        stages = request["budget"]["stages"]
        cpu = sum(stages[key.split(":")[0]]["cpu_seconds"] for key, _ in nodes)
        wall = sum(stages[key.split(":")[0]]["wall_seconds"] for key, _ in nodes)
        output = sum(sum(stages[key.split(":")[0]][field] for field in
                         ("output_bytes", "stdout_bytes", "stderr_bytes"))
                     +2*P.MIB+S.MANIFEST_LIMIT for key, _ in nodes)+4*P.MIB
        envelope = q["full_path_envelope"]
        self.assertEqual(envelope["missing_host_calls"], 109)
        self.assertEqual(envelope["selected_worker_cpu_envelope"], cpu)
        self.assertEqual(envelope["selected_worker_wall_envelope"], wall)
        self.assertEqual(envelope["new_output_envelope"], output)
        self.assertEqual(envelope["new_entry_envelope"], 109*9+4)
        self.assertTrue(envelope["full_path_fits_requested_envelopes"])
        self.assertEqual(q["prior_allowance_charges"], [0, 0, 0, 0, 0])

    def test_real_source_pin_refusal_and_logical_closure_hooks(self):
        c = CONTEXT
        self.assertEqual(len(T.source_paths()), 29)
        self.assertEqual(len(Q.entry_sources()), 31)
        pin = deepcopy(c.profile["source_pins"][0])
        pin["sha256"] = "00"*32 if pin["sha256"] != "00"*32 else "11"*32
        self.reject(lambda: c.owner._support._read(pin), "INPUT_PIN_CHANGED")
        chosen = T.source_paths()[0]
        owner = c.logical()
        owner.profile["support_profile"]["runtime_pins"] = [p for p in owner.support["runtime_pins"]
                                                           if Path(p["path"]) != chosen]
        with patch.object(H, "adopt_build", side_effect=AssertionError("Hook must reject before adopter")):
            self.reject(lambda: owner._adopt_host_build({}, {}, "stage"),
                        "TYPED_SOURCE_NOT_SELECTED:"+str(chosen))
        owner = c.logical()
        owner.support["runtime_pins"].append(deepcopy(owner.support["runtime_pins"][0]))
        self.reject(lambda: owner._adopt_host_build({}, {}, "stage"), "TYPED_DUPLICATE_RUNTIME_PIN")
        # Only the inherited disk recheck is doubled; composite identity checks run.
        owner = copy(c.owner)
        owner._lifecycle_profile = deepcopy(c.owner._lifecycle_profile)
        owner._lifecycle_profile["schema"] = "CHANGED"
        with patch.object(c.owner._support, "_check", lambda pins: None):
            self.reject(lambda: T.TypedLifecycleProducer._check(owner, {}), "LIFECYCLE_PROFILE_MUTATED")

    def test_constructor_closes_attached_support_on_failure(self):
        error = RuntimeError("EXPLICIT_CONSTRUCTOR_CONTROL")
        attached = []

        class Support:
            closed = False
            def close(self):
                self.closed = True

        support = Support()

        def fail(owner, profile):
            owner._support = support
            attached.append(owner)
            raise error

        with patch.object(S.AggregateProducer, "__init__", fail):
            with self.assertRaises(RuntimeError) as caught:
                T.TypedLifecycleProducer(deepcopy(CONTEXT.profile))
        self.assertIs(caught.exception, error)
        self.assertEqual(len(attached), 1)
        self.assertTrue(attached[0]._closed)
        self.assertTrue(support.closed)

    def test_host_provenance_and_failed_build_logical_mutations(self):
        c = CONTEXT
        descriptor = str(Path(c.host_pins["result"]["path"]).parent/
                         "source/adapters/software/v5/prover_memory/SOURCE.json")
        doc = P.parse(c.reads[descriptor])
        doc["preserved"]["aggregate_image"] = I.IMAGE_ID
        owner = c.logical({descriptor: P.encoded(doc)})
        self.reject(lambda: H.adopt_build(owner, c.host_pins, {}), "REFINEMENT_UNCHANGED_MATHEMATICS")
        self.assertIn(descriptor, owner.control_read_paths)
        owner = c.logical()
        owner.support["image_id"] = H.BUILD_PROVENANCE_IMAGE
        self.reject(lambda: H.adopt_build(owner, c.host_pins, {}), "REFINEMENT_UNCHANGED_MATHEMATICS")
        changes = c.changed(c.host_pins, "result", lambda r: r["commands"][0].update(exit_code=1))
        owner = c.logical(changes)
        self.reject(lambda: H.adopt_build(owner, c.host_pins, {}), "REFINEMENT_CLEAN_COMPILE")

    def test_image_binding_and_build_logical_mutations(self):
        c = CONTEXT
        owner = c.logical()
        owner.profile["image_adoption"]["result"]["sha256"] = "00"*32
        self.reject(lambda: I.adopt_image(owner), "TYPED_EXACT_RETAINED_IMAGE_RECORD")
        self.assertEqual(owner.control_read_paths, [])
        cases = (
            ("result", lambda r: r.update(image_id="00"*32), "TYPED_ADOPTED_IMAGE_ASSEMBLY"),
            ("guest_build", lambda r: r.update(status="FAIL"), "TYPED_GUEST_BUILD_CHAIN"),
            ("guest_build", lambda r: r["job"].update(active_processes=1), "TYPED_BUILD_JOB_CLOSURE"),
            ("guest_source_map", lambda r: r["project"].pop(next(iter(r["project"]))), "TYPED_SOURCE_MAP_CHAIN"),
            ("guest_build", lambda r: r["commands"][0].update(exit_code=1), "TYPED_CLOSED_COMPILE"),
        )
        for role, change, reason in cases:
            with self.subTest(role=role, reason=reason):
                owner = c.logical(c.changed(c.image_pins, role, change))
                self.reject(lambda: I.adopt_image(owner), reason)
                self.assertIn(c.image_pins[role]["path"], owner.control_read_paths)

    def test_intentional_screen_failure_not_arbitrary_failure(self):
        c = CONTEXT
        pins = c.retained_pins
        run = Path(pins["outer"]["path"]).parent
        cases = (
            ("result", lambda r: r.update(status="PASS"), "TYPED_INTENTIONAL_INVESTMENT_FAILURE_ONLY"),
            ("result", lambda r: r["screen"].update(padded_rows_at_most_three_quarters=True),
             "TYPED_INTENTIONAL_INVESTMENT_FAILURE_ONLY"),
            ("outer", lambda r: r["result"].update(child_exit_code=2), "TYPED_SCREEN_EXIT1_CLEAN_CLOSURE"),
            ("outer", lambda r: r["result"]["final_job"].update(active_processes=1),
             "TYPED_SCREEN_EXIT1_CLEAN_CLOSURE"),
        )
        for role, change, reason in cases:
            with self.subTest(role=role, reason=reason):
                records = deepcopy(c.retained)
                change(records[role])
                self.reject(lambda: R._screen_and_outer(records, pins, run), reason)

    def test_arm_session_header_parent_and_lineage_logical_mutations(self):
        c = CONTEXT
        pins, session = c.retained_pins, c.request["session"]
        changes = c.changed(pins, "result", lambda r: r["arms"][0].update(status="FAIL"))
        changes.update(c.changed(pins, "arm", lambda r: r.update(status="FAIL")))
        owner = c.logical(changes)
        self.reject(lambda: R.adopt(owner, session, c.expected, {}), "TYPED_COMPLETE_GENERAL_ARM")
        for role in ("wire", "capsule", "parents"):
            with self.subTest(role=role):
                altered = deepcopy(session)
                pin = altered[role][0] if role == "parents" else altered[role]
                pin["sha256"] = "00"*32
                owner = c.logical()
                self.reject(lambda: R.adopt(owner, altered, c.expected, {}), "TYPED_EXACT_RETAINED_SESSION")
        owner = c.logical()
        altered_header = bytes([c.expected[0] ^ 1])+c.expected[1:]
        self.reject(lambda: R.adopt(owner, session, altered_header, {}), "TYPED_COMPLETE_GENERAL_ARM")
        changes = c.changed(pins, "configuration", lambda r:
                            r["general"]["assembly"]["guest_result"].update(sha256="00"*32))
        owner = c.logical(changes)
        self.reject(lambda: R.adopt(owner, session, c.expected, {}), "TYPED_RETAINED_IMAGE_LINEAGE")
        changes = c.changed(pins, "diagnostic", lambda r: r.update(elf_sha256="00"*32))
        owner = c.logical(changes)
        self.reject(lambda: R.adopt(owner, session, c.expected, {}), "TYPED_EXACT_EXECUTION_DIAGNOSTIC")

    def test_explicit_schema_dispatch_has_no_fallback(self):
        owner = CONTEXT.logical()
        error = RuntimeError("EXPLICIT_RETAINED_VALIDATION_FAILURE")
        calls = []

        def retained(*args):
            calls.append("retained")
            raise error

        def generic(*args):
            calls.append("generic")

        with patch.object(R, "adopt", retained), patch.object(N, "adopt", generic):
            with self.assertRaises(RuntimeError) as caught:
                owner._snapshot(deepcopy(CONTEXT.request["session"]), CONTEXT.expected, {})
            self.assertIs(caught.exception, error)
            self.assertEqual(calls, ["retained"])
            owner._snapshot({"snapshot_evidence": {k: {} for k in N.EVIDENCE_FIELDS}}, b"", {})
            self.assertEqual(calls, ["retained", "generic"])
        self.reject(lambda: T._evidence_kind({**CONTEXT.retained_pins, "extra": {}}),
                    "TYPED_SNAPSHOT_EVIDENCE_FIELDS")

    def test_logical_prefix_quotes_preserve_full_graph_and_identity(self):
        c = CONTEXT
        quotes = []
        for limit in (1, 5):
            request = deepcopy(c.request)
            request["stage_limit"] = limit
            quotes.append(c.logical().preflight(request))
        self.assertEqual(quotes[0]["profile_id"], quotes[1]["profile_id"])
        self.assertEqual(quotes[0]["session_id"], quotes[1]["session_id"])
        self.assertEqual(quotes[0]["full_path_envelope"], quotes[1]["full_path_envelope"])
        self.assertEqual([len(q["selected_stages"]) for q in quotes], [1, 5])
        self.assertEqual([n["key"] for n in quotes[1]["selected_stages"]],
                         ["segment:0", "lift:0", "segment:1", "lift:1", "join:1"])
        request = deepcopy(c.request)
        request["budget"]["worker_cpu_seconds"] = 1
        quote = c.logical().preflight(request)
        self.assertFalse(quote["full_path_envelope"]["full_path_fits_requested_envelopes"])
        self.assertFalse(quote["funding"])
        self.assertFalse(Path(request["output_directory"]).exists())

    def test_operator_typed_constructor_and_close_failure_control(self):
        c = CONTEXT
        for fail_close in (False, True):
            with self.subTest(fail_close=fail_close):
                calls = []
                report_path = OUTPUT/("operator-close-failure.json" if fail_close else "operator-preflight.json")

                class FakeOwner:
                    """Explicit entry/control-flow double, not an adopted owner."""
                    _pins = {}
                    _install = c.owner._install
                    profile_id = c.owner.profile_id
                    closed = False
                    def _request(self, request):
                        require_equal(request, c.request)
                        calls.append("request")
                        q = c.quote
                        return (q["session_id"], {}, {}, [(n["key"], tuple(n["dependencies"]))
                                for n in q["selected_stages"]], Path(request["output_directory"]),
                                q["prior_allowance_charges"], q["full_path_envelope"])
                    def run(self, request):
                        raise AssertionError("Preflight must not run")
                    def close(self):
                        calls.append("close")
                        if fail_close:
                            raise RuntimeError("EXPLICIT_CLOSE_FAILURE")
                        self.closed = True
                    def report(self):
                        return {"closed": self.closed}

                def constructor(profile):
                    require_equal(profile, c.profile)
                    calls.append("typed-constructor")
                    return FakeOwner()

                args = ["preflight", "--profile", OPTIONS.profile, "--profile-sha256", OPTIONS.profile_sha256,
                        "--request", OPTIONS.request, "--request-sha256", OPTIONS.request_sha256,
                        "--owner-report", str(report_path)]
                # Only entry/control flow is under test here: no second large
                # artifact binding sweep. Genuine binding was exercised above.
                with patch.object(T, "TypedLifecycleProducer", constructor), \
                     patch.object(O, "rebind", lambda pins: None), redirect_stdout(io.StringIO()):
                    code = Q.main(args)
                report = P.parse(report_path.read_bytes())
                self.assertEqual(calls, ["typed-constructor", "request", "close"])
                self.assertEqual(code, 1 if fail_close else 0)
                self.assertEqual(report["status"], "FAIL" if fail_close else "PASS_REQUEST_PREFLIGHT_ONLY")
                self.assertEqual(report["run_calls_attempted"], 0)
                self.assertEqual(report["proof_calls"], 0)
                self.assertEqual(report["owner_closed"], not fail_close)
                if fail_close:
                    self.assertEqual(report["close_error"], "RuntimeError: EXPLICIT_CLOSE_FAILURE")


def main():
    global OPTIONS, OUTPUT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--profile-sha256", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--request-sha256", required=True)
    parser.add_argument("--output", required=True)
    OPTIONS = parser.parse_args()
    OUTPUT = Path(OPTIONS.output)
    if not OUTPUT.is_absolute() or OUTPUT.exists() or not OUTPUT.parent.is_dir():
        raise AssertionError("Fresh absolute control output with existing parent required")
    OUTPUT.mkdir()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TypedAdoptionControls)
    with patch.object(subprocess, "Popen", forbidden_dispatch):
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = result.wasSuccessful() and not DISPATCHES
    report = {"schema": "DMKN_TYPED_ADOPTION_CONTROLS_V1", "status": "PASS" if passed else "FAIL",
              "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
              "process_dispatch_attempts": list(DISPATCHES), "native_calls": 0, "proof_calls": 0,
              "mathematical_admission": False,
              "scope": "ONE_REAL_RETAINED_ADOPTION_AND_QUOTE;EXPLICIT_NONBINDING_LOGICAL_MUTATIONS",
              "real_quote": None if CONTEXT is None else CONTEXT.quote,
              "profile_sha256": OPTIONS.profile_sha256, "request_sha256": OPTIONS.request_sha256}
    O.save_new(OUTPUT/"RESULT.json", report, P.MIB)
    print(P.encoded(report).decode(), end="")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
