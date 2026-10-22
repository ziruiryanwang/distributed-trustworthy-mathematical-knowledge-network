"""Bounded offer-window controls; real SQLite/HTTP, inert proof payloads only.

Reuse pinned predecessor fixture/containment helpers, never its selected tests.
Root alone selects execution. All output belongs to a fresh operation snapshot.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from copy import deepcopy
from unittest.mock import patch

PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SELF = Path("software/v5/offer_enumeration/controls.py")
HELPER = Path("software/v5/exact_packet/controls.py")
HELPER_BYTES = 34036
HELPER_SHA = "bd9a48119a3ae428e343a2d6061256026fc530cf0b281bf33e49e554214f2883"
MAP = PROJECT/"experiments/v5-local-checks/distribution-exact-packet-01-input.json"
MAP_BYTES = 2813358
MAP_SHA = "328c21bb585881d654f1a23f1704fbaa277ee865f7adb1250cf6c19b85647561"
REPLACEMENT = "software/v5/offer_enumeration/delta/custody.py"
REPLACEMENT_BYTES = 11389
REPLACEMENT_SHA = "e1e35cecd8f40154a98e40cb1a5a2cca1d8c376966e57ef529c7c878bdd6c634"
SELECTED = ("test_01_real64_store_http_and_response_refusals",
            "test_02_shared_legacy_grammar_and_response_bounds")


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def ordinary(path):
    need(path.is_absolute() and path.resolve() == path and all(
        not item.is_symlink() and not item.is_junction()
        for item in (path, *path.parents)), "OFFER_CONTROL_ORDINARY_PATH")
    return path


def main():
    need(len(sys.argv) == 3 and sys.argv[1] == "--output", "OFFER_CONTROL_OUTPUT_REQUIRED")
    output = ordinary(Path(sys.argv[2]))
    need(output.is_dir() and output.is_relative_to(PROJECT) and os.name == "nt"
         and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "OFFER_CONTROL_ISOLATED_WINDOWS")
    snapshot = output/"sources"
    source = ordinary(snapshot/SELF)
    need(Path(__file__).resolve() == source, "OFFER_CONTROL_SNAPSHOT_REQUIRED")
    selection = json.loads((output/"selection.json").read_bytes())
    pins = selection["sources"]
    need(type(pins) is dict and len(pins) == 133, "OFFER_CONTROL_SOURCE_CENSUS")
    need(pins.get(SELF.as_posix()) == hashlib.sha256(source.read_bytes()).hexdigest(),
         "OFFER_CONTROL_SELF_PIN")
    helper = ordinary(snapshot/HELPER)
    need(helper.stat().st_size == HELPER_BYTES and pins.get(HELPER.as_posix()) == HELPER_SHA
         and hashlib.sha256(helper.read_bytes()).hexdigest() == HELPER_SHA,
         "OFFER_CONTROL_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("offer_controls_frozen_helpers", helper)
    need(spec is not None and spec.loader is not None, "OFFER_CONTROL_HELPER_LOADER")
    base = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = base
    spec.loader.exec_module(base)

    def stage():
        ordinary(MAP)
        raw = MAP.read_bytes()
        need(len(raw) == MAP_BYTES and hashlib.sha256(raw).hexdigest() == MAP_SHA,
             "OFFER_CONTROL_MAP_PIN")
        basis = json.loads(raw)["sdk_sources"]
        need(len(basis) == 129, "OFFER_CONTROL_BASE_129")
        code = output/"selected-code"; code.mkdir(); base.CODE = code
        for logical, original in sorted(basis.items()):
            relative = Path(original["path"]).relative_to(PROJECT).as_posix()
            expected, size = original["sha256"], original["bytes"]
            if logical == "v5/delta/custody.py":
                relative, expected, size = REPLACEMENT, REPLACEMENT_SHA, REPLACEMENT_BYTES
            need(pins.get(relative) == expected, "OFFER_CONTROL_SELECTED_SOURCE")
            path = ordinary(snapshot/relative)
            data = path.read_bytes()
            need(len(data) == size and 0 < size <= 2*base.MIB
                 and hashlib.sha256(data).hexdigest() == expected, "OFFER_CONTROL_SOURCE_PIN")
            target = code/logical; target.parent.mkdir(parents=True, exist_ok=True)
            base.write_new(target, data)
            need(target.read_bytes() == data, "OFFER_CONTROL_STAGING_READBACK")
            base.SOURCES[logical] = dict(source=relative, bytes=size, sha256=expected)
        need(len(base.SOURCES) == 129 and not any(name in sys.modules for name in
             ("delta", "placement", "modules", "client", "discovery")), "OFFER_CONTROL_IMPORT_ORDER")
        sys.path[:0] = [str(code/"v5"), str(code/"portable")]

    old_configuration = base.configuration
    def configuration(terminal=True):
        cfg = old_configuration(terminal)
        cfg["packet_limits"].update(packets=128, offers=128, offers_per_module=64)
        return cfg

    class Controls(base.Controls):
        async def fixture64(self):
            fixture = await super().fixture()
            variants = list(fixture.variants)
            for number in range(9, 64):
                raw = base.EP.pack_terminal_i(fixture.journal,
                    b"EXACT-CONTROL-INERT-UNVERIFIED-RECEIPT-"+bytes([number]),
                    aggregate_image=base.IMAGE, envelope=base.ENV(), terminal_i=True)
                fixture.source_packets.put(fixture.module, raw)
                variants.append((base.sha(raw), raw))
            fixture.variants = sorted(variants)
            self.assertEqual(len({digest for digest, raw in fixture.variants}), 64)
            self.assertEqual(fixture.source_packets.status()["counts"]["packets"], 64)
            self.assertEqual(fixture.source_packets.status()["counts"]["offers"], 64)
            fixture.digest, fixture.raw = fixture.variants[-1]
            fixture.entry = dict(packet_sha256=fixture.digest, packet_bytes=len(fixture.raw))
            return fixture

        async def test_01_real64_store_http_and_response_refusals(self):
            f = await self.fixture64(); a = self.acquisition(f)
            request = dict(module_id=f.module, wire_profile_id=f.source_packets.profile_id,
                           max_offers=64, max_bytes=16384)
            local = f.source_packets.offer(request)
            expected = [dict(packet_sha256=digest, packet_bytes=len(raw)) for digest, raw in f.variants]
            self.assertEqual(local["packets"], expected)
            self.assertLessEqual(len(base.F.compact(local)), 16384)
            self.assertGreater(len(base.F.compact(local)), 4096)
            self.assertFalse(local["global_complete"]); self.assertFalse(local["mathematical_acceptance"])
            default = await a.offers("source", f.module)
            self.assertEqual(default["packets"], expected[:4])
            for count in range(1, 9):
                with self.subTest(old_prefix=count):
                    prefix = await a.offers("source", f.module, max_offers=count)
                    self.assertEqual(prefix["packets"], expected[:count])
            before = a.budget.used.copy()
            with self.assertRaisesRegex(ValueError, "NOT_OFFERED"):
                await a.packet("source", f.module, f.entry)
            self.assertEqual(a.budget.used, before)
            full = await a.offers("source", f.module, max_offers=64, max_bytes=16384)
            self.assertEqual(full, local); self.assertIn(f.entry, full["packets"])
            received = await a.packet("source", f.module, f.entry)
            self.assertFalse(received["mathematical_acceptance"])
            self.assertEqual(f.w.packets.get(f.digest, len(f.raw)), f.raw)
            self.assertEqual(a.budget.used["requests"], 11)
            self.assertEqual(f.provider.requests, 11)

            # Both schema-invalid requests are charged attempts, but rejected
            # by the real exchange validator before any new network connection.
            for count in (65, True):
                before = a.budget.used.copy(); calls = f.provider.requests
                with self.assertRaisesRegex(ValueError, "INTEGER_BOUND"):
                    await a.offers("source", f.module, max_offers=count, max_bytes=16384)
                self.assertEqual(f.provider.requests, calls)
                self.assertEqual(a.budget.used["requests"], before["requests"]+1)
                self.assertEqual(a.budget.used["reply_bytes"], before["reply_bytes"]+16384)
                self.assertIsNone(a.budget.pending)

            # No silent truncation when an explicit byte budget is too small.
            with self.assertRaisesRegex(ValueError, "EVIDENCE_OFFER_BYTES"):
                f.source_packets.offer({**request, "max_bytes": 4096})
            before = a.budget.used.copy(); failures = f.provider.failures
            with self.assertRaises(base.asyncio.IncompleteReadError):
                await a.offers("source", f.module, max_offers=64, max_bytes=4096)
            self.assertEqual(a.budget.used["requests"], before["requests"]+1)
            self.assertEqual(a.budget.used["reply_bytes"], before["reply_bytes"]+4096)
            self.assertIsNone(a.budget.pending)
            self.assertEqual(f.provider.failures, failures+1)
            self.assertEqual(f.provider.reserved_reply_bytes, 0)

            invalid = []
            for key, value in (("module_id", base.sha(b"wrong-module")),
                               ("wire_profile_id", base.sha(b"wrong-profile")),
                               ("proof_form", "bounded-native-delta-v1"),
                               ("global_complete", True), ("mathematical_acceptance", True)):
                bad = deepcopy(local); bad[key] = value
                invalid.append((key, bad, "EVIDENCE_OFFER_BINDING"))
            bad = deepcopy(local); bad["packets"].append(deepcopy(bad["packets"][-1]))
            invalid.append(("count65", bad, "EVIDENCE_OFFER_COUNT"))
            bad = deepcopy(local); bad["packets"].reverse()
            invalid.append(("reversed", bad, "EVIDENCE_OFFER_ORDER"))
            bad = deepcopy(local); bad["packets"][1] = deepcopy(bad["packets"][0])
            invalid.append(("duplicate", bad, "EVIDENCE_OFFER_ORDER"))
            bad = deepcopy(local); bad["packets"][0]["packet_bytes"] = True
            invalid.append(("boolean_size", bad, "INTEGER_BOUND"))
            bad = deepcopy(local); bad["unexpected"] = 1
            invalid.append(("extra_field", bad, "EXACT_FIELDS"))
            bad = deepcopy(local); bad["packets"] = {}
            invalid.append(("nonlist", bad, "EVIDENCE_OFFER_COUNT"))
            b = self.acquisition(f); actual_dispatch = f.provider.dispatch
            refused = []
            for label, bad, code in invalid:
                # Explicit malicious-response injection after actual store
                # dispatch. Framing, sockets, budgets and client checks stay real.
                def hostile(route, value, **kwargs):
                    result = actual_dispatch(route, value, **kwargs)
                    return deepcopy(bad) if route == base.DT.OFFER_ROUTE else result
                before = b.budget.used.copy()
                with self.subTest(malformed=label), patch.object(f.provider, "dispatch", hostile):
                    with self.assertRaisesRegex(ValueError, code):
                        await b.offers("source", f.module, max_offers=64, max_bytes=16384)
                self.assertFalse(b._offers); self.assertIsNone(b.budget.pending)
                self.assertEqual(b.budget.used["requests"], before["requests"]+1)
                self.assertEqual(b.budget.used["reply_bytes"],
                                 before["reply_bytes"]+len(base.F.compact(bad)))
                refused.append(label)
            with self.assertRaisesRegex(ValueError, "EVIDENCE_OFFER_PROFILE"):
                base.EC.verify_offer(local, request, profile=base.EC.public_profile(base.IMAGE))
            extra = base.EP.pack_terminal_i(f.journal, b"UNVERIFIED-65TH-VARIANT",
                aggregate_image=base.IMAGE, envelope=base.ENV(), terminal_i=True)
            with self.assertRaisesRegex(ValueError, "DELTA_CUSTODY_LOCAL_OFFERS"):
                f.source_packets.put(f.module, extra)
            self.assertEqual(f.source_packets.status()["counts"]["packets"], 64)
            self.assertEqual(f.source_packets.offer(request), local)
            self.assertEqual(f.provider.requests, 23)
            self.assertEqual(f.provider.failures, 1)
            self.assertEqual(f.provider.reserved_reply_bytes, 0)
            self.assertEqual(set(self.routes), {base.DT.OFFER_ROUTE, base.DT.PACKET_ROUTE})
            base.OBSERVED[self._testMethodName] = dict(variants=64, old_prefixes=list(range(1, 9)),
                default_count=4, full_offer_bytes=len(base.F.compact(local)), late_identity=f.entry,
                actual_http_requests=f.provider.requests, expected_provider_failures=1,
                malformed_http_refusals=refused, normal_acquisition=a.report(), hostile_acquisition=b.report(),
                provider_reply_bytes=f.provider.reply_bytes, provider_request_bytes=f.provider.request_bytes,
                provider_header_bytes=f.provider.header_bytes, mathematical_acceptance=False)

        def test_02_shared_legacy_grammar_and_response_bounds(self):
            legacy = base.importlib.import_module("delta.custody")
            self.assertIs(legacy.offer_request, base.EC.offer_request)
            self.assertIs(legacy.offer_request, base.DT.offer_request)
            request = dict(module_id="11"*32, wire_profile_id="22"*32,
                           max_offers=64, max_bytes=16384)
            value = dict(schema=legacy.OFFER_SCHEMA, module_id=request["module_id"],
                wire_profile_id=request["wire_profile_id"], proof_form="bounded-native-delta-v1",
                assurance="UNVERIFIED_DELTA_PACKET_LOCATORS_ONLY", global_complete=False,
                mathematical_acceptance=False, packets=[dict(packet_sha256=f"{n:064x}", packet_bytes=1)
                    for n in range(64)])
            for count in (1, 4, 8, 64):
                legacy.offer_request({**request, "max_offers": count})
                selected = {**value, "packets": value["packets"][:count]}
                self.assertEqual(legacy.verify_offer(selected, {**request, "max_offers": count}), selected)
            for count in (0, 65, True, False, 64.0):
                with self.subTest(invalid_request=count), self.assertRaisesRegex(ValueError, "INTEGER_BOUND"):
                    legacy.offer_request({**request, "max_offers": count})
            for key, replacement, reason in (("packets", value["packets"]+[value["packets"][-1]], "COUNT"),
                    ("packets", list(reversed(value["packets"])), "ORDER"),
                    ("proof_form", "mixed-or-certified-terminal-v2", "BINDING")):
                with self.subTest(legacy=reason), self.assertRaisesRegex(ValueError, "DELTA_OFFER_"+reason):
                    legacy.verify_offer({**value, key: replacement}, request)
            with self.assertRaisesRegex(ValueError, "DELTA_OFFER_BYTES"):
                legacy.verify_offer(value, {**request, "max_bytes": 4096})
            base.OBSERVED[self._testMethodName] = dict(scope="REAL_SHARED_VALIDATOR_SYNTHETIC_LEGACY_METADATA",
                shared_function_identity=True, legacy_counts=[1, 4, 8, 64], legacy_receipt_or_packet_import=False)

    base.stage = stage
    base.configuration = configuration
    base.SELECTED = SELECTED
    base.Controls = Controls
    base.MAP_SHA = MAP_SHA
    original_writer = base.write_new
    def write_report(path, raw):
        if path == output/"exact-packet-controls-result.json":
            report = json.loads(raw)
            need(report["selected"] == list(SELECTED) and report["tests_run"] == 2,
                 "OFFER_CONTROL_EXACT_TEST_SET")
            report.update(schema="DMKN_V5_OFFER_ENUMERATION_CONTROLS_V1",
                scope="REAL_TYPED_64_VARIANT_STORE_HTTP_PLUS_SHARED_LEGACY_METADATA_VALIDATION",
                helper_sha256=HELPER_SHA, selected_product_change=REPLACEMENT_SHA,
                predecessor_tests_rerun=False, malicious_response_injection="POST_REAL_DISPATCH_VALUES_ONLY")
            report.pop("higher_facade_scope")
            raw = json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()+b"\n"
            path = output/"offer-enumeration-controls-result.json"
        return original_writer(path, raw)
    base.write_new = write_report
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
