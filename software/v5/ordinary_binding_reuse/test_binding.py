"""Source-only until root selects one bounded, native-free equivalence run."""
from __future__ import annotations

import copy
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import sys
import time
import types
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE_ROOT = Path(__file__).resolve().parents[3]
PACKAGE = "experiments/v5-local-checks/multi-source-package01/suite/assembled/package/"
FIXTURE = "experiments/v5-local-checks/ordinary-producer-public-export-01/bundle/"
PINS = {
    "ordinary_evidence": (PACKAGE + "installation/py/ordinary_evidence.py", "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6"),
    "ordinary_semantics": (PACKAGE + "installation/py/ordinary_semantics.py", "ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915"),
    "portable_evidence": (PACKAGE + "installation/py/portable_evidence.py", "f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8"),
    "portable_candidate": (PACKAGE + "authoring/py/portable_candidate.py", "29ae111a362472b09b2b1ff16b567b352be793d76c2cd1b5421e0aee29219331"),
    "old_bundle": (PACKAGE + "reference/baseline_bundle.py", "d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce"),
    "new_bundle": ("software/v5/ordinary_binding_reuse/baseline_bundle.py", "e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6"),
    "writer": (FIXTURE + "writer.json", "9768cb31cebb62c7743705d342caca6625cb92760010ede3c12d6bfc5dd9999b"),
    "inventory": (FIXTURE + "inventory.json", "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0"),
    "request": (FIXTURE + "request.json", "db0cf7d2a7ed204b0919e62afbcfca6c7f9e06d7834288bd0a1a385ad5686d32"),
    "manifest": (FIXTURE + "manifest.json", "b601bee8f6be2b2fc2315818ba81f340ed8bd72a43ac89cf547db001e7bc9cde"),
}
START_WALL, START_CPU = time.monotonic(), time.process_time()


def budget():
    if time.monotonic() - START_WALL > 45 or time.process_time() - START_CPU > 30:
        raise RuntimeError("TEST_FIXED_BUDGET")


def check(condition, label):
    budget()
    if not condition:
        raise AssertionError(label)


def pinned(key):
    budget()
    relative, expected = PINS[key]
    data = ((SOURCE_ROOT if key == "new_bundle" else ROOT) / relative).read_bytes()
    check(hashlib.sha256(data).hexdigest() == expected, "PIN:" + key)
    return data


def load(key):
    check(key not in sys.modules, "MODULE_ALREADY_LOADED:" + key)
    module = types.ModuleType(key)
    module.__file__ = str((SOURCE_ROOT if key == "new_bundle" else ROOT) / PINS[key][0])
    sys.modules[key] = module
    exec(compile(pinned(key), module.__file__, "exec"), module.__dict__)
    return module


def main():
    sys.dont_write_bytecode = True
    E, S, PE, C, old, new = [load(key) for key in (
        "ordinary_evidence", "ordinary_semantics", "portable_evidence",
        "portable_candidate", "old_bundle", "new_bundle")]
    writer, inventory, request, saved_manifest = [pinned(key) for key in (
        "writer", "inventory", "request", "manifest")]
    doc, targets = json.loads(writer), json.loads(request)["targets"]
    check(len(doc["units"]) == 6 and len(writer) == 82846, "REAL_SIX_UNIT_FIXTURE")
    encode = E.canonical_json
    passed, counts, bundles = [], {}, {}

    def bind(module, raw=writer, selected=targets, **limits):
        return module.bind_writer(raw, inventory, selected,
                                  limits=module.Limits(**limits), check_budget=budget)

    def refuses(label, action, expected):
        try:
            action()
        except ValueError as exc:
            check(str(exc) == expected, label + ":EXPECTED:" + expected + ":GOT:" + str(exc))
            return
        raise AssertionError(label + ":ACCEPTED")

    for split in (False, True):
        outputs = []
        for module in (old, new):
            calls = [0]
            original = E.inspect_unit

            def counted(*args, **kwargs):
                calls[0] += 1
                return original(*args, **kwargs)

            with patch.object(E, "inspect_unit", counted):
                result = bind(module, **({"max_batch_units": 1} if split else {}))
            expected = 12 if module is old else 6
            check(calls[0] == expected, "INSPECTION_COUNT")
            counts[module.__name__ + ("_single" if split else "_default")] = calls[0]
            check(not result.mathematical_acceptance, "NO_ACCEPTANCE_AUTHORITY")
            outputs.append(asdict(result))
            bundles[module.__name__, split] = result
        check(outputs[0] == outputs[1], "EXACT_OUTPUT_EQUIVALENCE")
        check(len(outputs[0]["batches"]) == (6 if split else 1), "BATCH_BOUNDARIES")
        if not split:
            check(outputs[0]["manifest"]["raw"] == saved_manifest, "SAVED_MANIFEST")
        passed.append("exact_default" if not split else "exact_one_unit_batches")

    # Independently re-read every generated byte string through unchanged readers.
    for module in (old, new):
        bundle = bundles[module.__name__, False]
        with patch.object(PE, "read_evidence", wraps=PE.read_evidence) as reader:
            census = module.validate_batch(bundle.manifest.batches[0], bundle.batches[0],
                                           check_budget=budget)
            check(reader.call_count == 6, "VALIDATE_BATCH_FULL_READER")
            check(census == bundle.census, "VALIDATE_BATCH_CENSUS")
            reader.reset_mock()
            rebuilt = module.make_manifest(bundle.batches, check_budget=budget)
            check(reader.call_count == 6, "MAKE_MANIFEST_FULL_READER")
            check(rebuilt == bundle.manifest, "REBUILT_MANIFEST")
    passed.append("external_reader_preservation")

    def paired(label, raw, code, selected=targets, **limits):
        for module in (old, new):
            refuses(label, lambda: bind(module, raw, selected, **limits), code)
        passed.append(label)

    def changed(label, mutate, code, *, repair_stats=False):
        modified = copy.deepcopy(doc)
        mutate(modified)
        if repair_stats:
            modified["stats"]["selected_units"] = len(modified["units"])
            modified["stats"]["unit_json_bytes"] = sum(map(len, map(encode, modified["units"])))
        paired(label, encode(modified), code)

    paired("duplicate_writer_key", b'{"schema":0,"schema":0}', "CANDIDATE_WRITER_DUPLICATE_KEY")
    changed("writer_fields", lambda d: d.update(extra=0), "BASELINE_WRITER_FIELDS")
    changed("unit_marker", lambda d: d["units"][0].__setitem__(0, "bad"), "UNIT_FORMAT")
    changed("empty_unit_inventory", lambda d: d["units"][0].__setitem__(2, []), "INVENTORY_EMPTY")
    changed("forward_reference", lambda d: d["units"].reverse(), "BASELINE_UNBOUND_OR_FORWARD_REFERENCE")
    changed("duplicate_output", lambda d: d["units"].append(d["units"][0]),
            "BASELINE_EXISTING_OR_DUPLICATE_OUTPUT", repair_stats=True)
    changed("wrong_unit_count", lambda d: d["stats"].__setitem__("selected_units", 7),
            "BASELINE_WRITER_STATISTICS_BOUND")
    changed("wrong_unit_bytes", lambda d: d["stats"].__setitem__("unit_json_bytes", 1),
            "BASELINE_WRITER_BYTE_CENSUS_OR_TARGET_OUTPUT")
    changed("missing_target", lambda d: d["units"].pop(),
            "BASELINE_WRITER_BYTE_CENSUS_OR_TARGET_OUTPUT", repair_stats=True)
    paired("duplicate_target", writer, "BASELINE_DUPLICATE_TARGET", targets + [targets[0]])
    for label, limits, code in (
        ("writer_byte_limit", {"max_writer_bytes": len(writer)-1}, "BASELINE_WRITER_BYTE_BOUND"),
        ("unit_byte_limit", {"max_unit_bytes": 1}, "BASELINE_UNIT_BYTE_BOUND"),
        ("aggregate_node_limit", {"max_nodes": 1}, "BASELINE_AGGREGATE_BOUND"),
        ("batch_node_limit", {"max_batch_nodes": 1}, "BASELINE_SINGLE_UNIT_EXCEEDS_BATCH"),
        ("batch_count_limit", {"max_batch_units": 1, "max_batches": 1}, "BASELINE_BATCH_COUNT_BOUND"),
    ):
        paired(label, writer, code, **limits)

    # One-shot encoder doubles alter ONLY envelope metadata/grammar, never unit
    # content after inspection. They probe retained guards, not a hostile local
    # interpreter threat model. The decoder's canonical re-encoder stays genuine.
    def envelope_fault(label, mutate, code, *, suffix=b"", syntax=None):
        for module in (old, new):
            injected = [False]
            original_reader = PE.read_evidence

            def faulty(value):
                if (not injected[0] and type(value) is dict and value.get("schema") == PE.SCHEMA
                        and len(value["imports"]) >= 2):
                    injected[0] = True
                    altered = copy.deepcopy(value)
                    mutate(altered)
                    return encode(altered) + suffix
                return encode(value)

            selected_limits = syntax or PE.DEFAULT_LIMITS
            with patch.object(E, "canonical_json", faulty), patch.object(PE, "DEFAULT_LIMITS", selected_limits), \
                    patch.object(PE, "read_evidence", lambda raw: original_reader(raw, selected_limits)):
                refuses(label, lambda: bind(module), code)
            check(injected[0], label + ":FAULT_NOT_REACHED")
        passed.append(label)

    envelope_fault("strict_generated_grammar", lambda d: None, "JSON_LEXICAL_TOKEN", suffix=b"\n")
    envelope_fault("envelope_fields", lambda d: d.update(extra=0), "PORTABLE_EVIDENCE_FIELDS")
    envelope_fault("envelope_schema", lambda d: d.update(schema="bad"), "PORTABLE_EVIDENCE_SCHEMA")
    envelope_fault("semantic_id_encoding", lambda d: d.update(semantic_id="bad"), "HASH_ENCODING")
    envelope_fault("semantic_id_binding", lambda d: d.update(semantic_id="0"*64), "BASELINE_EVIDENCE_SEMANTICS")
    envelope_fault("import_array", lambda d: d.update(imports={}), "ARRAY")
    envelope_fault("import_row", lambda d: d["imports"].__setitem__(0, [d["imports"][0][0]]), "ARRAY_ARITY")
    envelope_fault("import_name", lambda d: d["imports"][0].__setitem__(0, []), "SEMANTIC_NAME_ROOT")
    envelope_fault("import_id", lambda d: d["imports"][0].__setitem__(1, "bad"), "HASH_ENCODING")
    envelope_fault("import_order", lambda d: d["imports"].reverse(), "PORTABLE_IMPORT_CENSUS_OR_ORDER")
    envelope_fault("import_missing", lambda d: d["imports"].pop(), "PORTABLE_IMPORT_CENSUS_OR_ORDER")
    envelope_fault("import_duplicate", lambda d: d["imports"].append(d["imports"][0]), "PORTABLE_IMPORT_CENSUS_OR_ORDER")
    envelope_fault("import_count_bound", lambda d: None, "ARRAY_BOUND",
                   syntax=replace(PE.DEFAULT_LIMITS, max_imports=1))

    for key in PINS:
        pinned(key)
    return {"status": "PASS", "groups": passed, "inspection_counts": counts,
            "fixture_units": 6, "wall_seconds": time.monotonic()-START_WALL,
            "cpu_seconds": time.process_time()-START_CPU,
            "limits": {"wall_seconds": 45, "cpu_seconds": 30},
            "pins": {key: value[1] for key, value in PINS.items()},
            "claim": "finite byte/census/target equivalence and work-count reduction; no speedup or mathematical acceptance"}


if __name__ == "__main__":
    try:
        print(json.dumps(main(), sort_keys=True, separators=(",", ":")))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": type(exc).__name__ + ":" + str(exc),
                          "wall_seconds": time.monotonic()-START_WALL,
                          "cpu_seconds": time.process_time()-START_CPU}, sort_keys=True))
        raise SystemExit(1)
