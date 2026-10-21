"""One selected real frontend export and zero-parent native relation check.

Run only beneath Run-V5-Check's immutable snapshot and outer Job. The frontend
packet is explicitly untrusted. No session, receipt, handle or admission is
fabricated; the unchanged checker must validate every new local declaration.
"""
from pathlib import Path
import argparse
from dataclasses import replace
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
V5 = Path(__file__).resolve().parents[1]
MAP_SHA = "1903bb44b6176dae5d43142f11cd90ddde6d494d51d5b5c1c377f3ebf5182528"
IMAGE = "9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e"
FOUNDATION = "d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481"
POLICY = "5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377"
SOURCE = ("set_option autoImplicit false\nnamespace OwnerV5\n"
          "def addTwo := fun n : Nat => Nat.add n 2\n"
          "theorem addTwo_spec : forall n : Nat, addTwo n = Nat.succ (Nat.succ n) := fun n => rfl\n"
          "end OwnerV5\n")
MAX_BYTES = 16 * 1024**2


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def bounded(path, maximum=MAX_BYTES):
    need(path.is_file() and 0 < path.stat().st_size <= maximum, "FILE_BOUND:" + str(path))
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    need(0 < len(raw) <= maximum and path.stat().st_size == len(raw), "FILE_CHANGED")
    return raw


def pin(path):
    raw = bounded(path)
    return {"path": str(path), "bytes": len(raw), "sha256": sha(raw)}


def save(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def records(row):
    tag, value = next(iter(row.items()))
    return [d for key in ("types", "ctors", "recs") for d in value[key]] if tag == "inductive" else [value]


def named(*parts):
    return [["s", part] for part in parts]


def run_checker(executable, input_path, evidence, deadline):
    """Persistent logs, finite direct-child lifetime; whole tree belongs to outer Job."""
    stdout, stderr = evidence / "checker.stdout.json", evidence / "checker.stderr.txt"
    argv = [str(executable), "check", IMAGE, str(input_path)]
    report = {"argv": argv, "exit_code": None, "direct_child_reaped": False,
              "outer_job_closure_required": True}
    child = None
    try:
        with stdout.open("xb") as out, stderr.open("xb") as err:
            child = subprocess.Popen(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=out, stderr=err)
            while child.poll() is None:
                need(time.monotonic() < deadline, "CHECKER_DEADLINE")
                need(stdout.stat().st_size <= 1024**2 and stderr.stat().st_size <= 1024**2,
                     "CHECKER_LOG_LIMIT")
                time.sleep(0.025)
            report["exit_code"] = child.wait()
            report["direct_child_reaped"] = True
    finally:
        if child is not None and not report["direct_child_reaped"]:
            if child.poll() is None:
                child.kill()
            report["exit_code"] = child.wait(timeout=5)
            report["direct_child_reaped"] = True
        save(evidence / "checker-process.json", json.dumps(report, sort_keys=True).encode())
    need(report["exit_code"] == 0, "FRESH_CHECKER_REFUSED")
    need(stderr.stat().st_size <= 1024**2, "CHECKER_STDERR_BOUND")
    return bounded(stdout, 1024**2), report


def run(args):
    started = time.monotonic()
    need(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "ISOLATED_CANONICAL_OWNER")
    output = Path(args.output)
    need(output.is_absolute() and output.resolve() == output
         and output.parent == ROOT / "experiments/v5-local-checks" and output.is_dir()
         and output / "sources/software/v5/nat_literals/native.py" == Path(__file__).resolve(),
         "EXACT_OUTER_SNAPSHOT")
    selection_raw = bounded(output / "selection.json", 1024**2)
    selection = json.loads(selection_raw)
    need(selection["schema"] == "DMKN_V5_LOCAL_CHECK_V1", "OUTER_SELECTION")
    map_path = Path(args.runtime_map)
    need(args.runtime_map_sha256 == MAP_SHA and map_path.is_absolute()
         and map_path.resolve() == map_path
         and selection["runtime_pins"].get(str(map_path)) == MAP_SHA, "RUNTIME_MAP_SELECTION")
    map_raw = bounded(map_path)
    need(sha(map_raw) == MAP_SHA, "RUNTIME_MAP_PIN")
    basis = json.loads(map_raw)
    assets = {key: basis["assets"][key] for key in ("frontend", "native", "foundation")}
    for asset in assets.values():
        need(selection["runtime_pins"].get(asset["path"]) == asset["sha256"], "SELECTED_ASSET_PIN")
        raw = bounded(Path(asset["path"]))
        need(len(raw) == asset["bytes"] and sha(raw) == asset["sha256"], "ACTUAL_ASSET_PIN")
    runtime = list(basis["lean_runtime"].values())
    need(len(runtime) == 6 and all(selection["runtime_pins"].get(p["path"]) == p["sha256"]
                                  for p in runtime), "SIX_EXISTING_LEAN_PINS")
    evidence = output / "evidence"
    evidence.mkdir()
    result = {"schema": "DMKN_NAT_LITERAL_NATIVE_V1", "status": "FAIL",
              "mathematical_admission": False, "certificate_verification_performed": False,
              "public_client_integration": False, "outer_job_closure_required": True,
              "helper_initialization": "REAL_PURE_DEPENDENCIES_ONLY_NO_AUTHORITY_OBJECTS"}
    try:
        sys.path.insert(0, str(V5))
        from modules import codec as C
        from modules.model import Address
        # Only this explicitly selected successor supplies the logical decoder.
        SR = load("modules.source_rows", V5 / "nat_literals/source_rows.py")
        from modules.receipt.witness import make_input, decode_journal
        helper = load("_nat_foundation_helper", V5 / "authoring/test_native_frontend.py")
        # These pure helpers otherwise initialize unused transport/authority APIs.
        # Supply their REAL structural dependencies, not fake sessions or outcomes.
        helper.C, helper.Address, helper.SourceRows, helper._records = C, Address, SR.SourceRows, records
        helper.REQUEST_SCHEMA = "DMKN_OWNER_LEAN_AUTHORING_REQUEST_V1"
        need((helper.FOUNDATION, helper.POLICY) == (FOUNDATION, POLICY), "HELPER_PROFILE")
        worker = load("_nat_author_worker", V5 / "authoring/worker.py")
        foundation_raw = bounded(Path(assets["foundation"]["path"]))
        foundation = C.parse_json(foundation_raw)
        source_raw = bounded(V5 / "nat_literals/Arithmetic.lean", 65536)
        need(source_raw.decode("utf-8") == SOURCE, "EXACT_SELECTED_ARITHMETIC_SOURCE")
        save(evidence / "Arithmetic.lean", source_raw)
        roots = [named("OwnerV5", name) for name in ("addTwo", "addTwo_spec")]
        view = helper.foundation_view(foundation_raw)
        binding = C.hash_value("nat-literal-native-untrusted-selection", {
            "foundation_sha256": sha(foundation_raw), "source_sha256": sha(source_raw), "roots": roots})
        context = {"schema": "DMKN_UNTRUSTED_AUTHORING_CONTEXT_V1", "foundation": FOUNDATION,
                   "policy": POLICY, "foundation_sha256": sha(foundation_raw),
                   "foundation_view": view, "imports": [], "selection_binding": binding,
                   "mathematical_acceptance": False}
        request = helper.request(context, SOURCE, roots)
        request_path = evidence / "request.json"
        save(request_path, C.canonical(request))
        deadline = started + min(90, selection["limits"]["wall_seconds"])
        config = {"schema": worker.SCHEMA, "worker": pin(V5 / "authoring/worker.py"),
                  "executable": assets["frontend"], "lean_root": str(ROOT / "software/runtime/lean-4.34.0-windows"),
                  "runtime_pins": runtime, "request": pin(request_path),
                  "output_directory": str(evidence / "frontend"),
                  "report_path": str(evidence / "worker-result.json"), "deadline_monotonic": deadline}
        config_path = evidence / "worker-config.json"
        save(config_path, C.canonical(config))
        report = worker.run(config_path, sha(config_path.read_bytes()))
        need(report["status"] == "PASS_NATIVE_EXPORT_ONLY" and report["direct_child_reaped"]
             and report["native_return_code"] == 0 and not report["native_timed_out"]
             and not report.get("cleanup_error") and report["request_sha256"] == config["request"]["sha256"],
             "REAL_FRONTEND_EXPORT_REQUIRED")
        exported_raw = bounded(evidence / "frontend/EXPORT.json")
        need(sha(exported_raw) == report["export_sha256"], "SAME_CALL_EXPORT_HASH")
        exported = C.parse_json(exported_raw)
        C.fields(exported, {"schema", "source_sha256", "selection_binding", "roots", "rows",
                            "local_names", "status", "mathematical_acceptance"})
        need(exported["schema"] == "DMKN_OWNER_LEAN_AUTHORING_EXPORT_V1"
             and exported["source_sha256"] == sha(source_raw) and exported["selection_binding"] == binding
             and exported["roots"] == roots and exported["mathematical_acceptance"] is False
             and exported["status"] == "OWNER_FRONTEND_EXPORT_REQUIRES_INDEPENDENT_RELATION", "EXPORT_BINDING")
        limits = replace(C.DEFAULT_LIMITS, max_name_parts=C.DEFAULT_LIMITS.max_name_parts + 3)
        census = SR.SourceRows(exported["rows"], [], [], limits=limits)
        names = [census.name(d["name"]) for row in census.declarations for d in records(row)]
        need(len({C.name_key(n) for n in names}) == len(names)
             and sorted(C.name_key(n) for n in names) == sorted(C.name_key(n) for n in exported["local_names"]),
             "ACTUAL_LOCAL_CENSUS")
        decoder = SR.SourceRows(exported["rows"], names, view["names"], limits=limits)
        environment = decoder.module(FOUNDATION, POLICY)
        C.validate_spec(environment.spec)
        for (arity, unused), raw in environment.bodies.items():
            C.validate_expr(C.parse_json(raw), arity)
        descriptors = {C.name_key(d["name"]): d for group in environment.spec["groups"] for d in group["declarations"]}
        required = [named("Nat"), named("Nat", "zero"), named("Nat", "succ"), named("Nat", "rec"),
                    named("Nat", "add"), named("OfNat"), named("OfNat", "ofNat"), named("instOfNatNat"), *roots]
        need(all(C.name_key(n) in descriptors for n in required), "COMPLETE_ARITHMETIC_VOCABULARY")
        const = lambda n, levels=(): ["const", ["local", n], list(levels)]
        nat, zero, succ = (const(named("Nat")), const(named("Nat", "zero")), const(named("Nat", "succ")))
        two = ["app", succ, ["app", succ, zero]]
        numeral = ["app", ["app", ["app", const(named("OfNat", "ofNat"), [["zero"]]), nat], two],
                   ["app", const(named("instOfNatNat")), two]]
        definition = descriptors[C.name_key(roots[0])]
        expected_body = ["lam", "default", nat,
                         ["app", ["app", const(named("Nat", "add")), ["bvar", 0]], numeral]]
        need(definition["kind"] == "definition" and definition["universes"] == 0
             and definition["type"] == ["forall", "default", nat, nat]
             and C.parse_json(environment.bodies[0, definition["value_hash"]]) == expected_body,
             "EXACT_ADD_TWO_NORMALIZED_BODY")
        theorem = descriptors[C.name_key(roots[1])]
        eq = ["const", ["foundation", named("Eq")], [["succ", ["zero"]]]]
        expected_type = ["forall", "default", nat,
                         ["app", ["app", ["app", eq, nat], ["app", const(roots[0]), ["bvar", 0]]],
                          ["app", succ, ["app", succ, ["bvar", 0]]]]]
        need(theorem["kind"] == "theorem" and theorem["universes"] == 0
             and theorem["type"] == expected_type, "EXACT_NONNUMERAL_TWO_SUCCESSOR_THEOREM")
        transcript = []
        for index, raw_expr in enumerate(decoder.expressions):
            if "natVal" not in raw_expr:
                continue
            text = raw_expr["natVal"]
            need(type(text) is str and text.isascii() and text.isdecimal() and len(text) <= 3,
                 "SMOKE_LITERAL_BOUND")
            number = int(text)
            need(number <= 191, "SMOKE_LITERAL_VALUE")
            expected = zero
            for unused in range(number):
                expected = ["app", succ, expected]
            actual = decoder.expression(index, ())
            need(actual == expected, "EXACT_RAW_TO_CONSTRUCTOR_CORRESPONDENCE")
            transcript.append({"native_expression_index": index, "decimal": text,
                               "normalized_sha256": sha(C.canonical(actual))})
        need(any(item["decimal"] == "2" for item in transcript), "REAL_RAW_TWO_REQUIRED")
        save(evidence / "normalization.json", C.canonical({"scope": "UNIQUE_RAW_ROWS_NOT_OCCURRENCE_TOTAL",
             "literals": transcript, "required_names": required, "source_work": decoder.work}))
        save(evidence / "normalized-spec.json", C.canonical(environment.spec))
        save(evidence / "normalized-bodies.json", C.canonical([
            {"universes": u, "digest": digest, "expression": C.parse_json(raw)}
            for (u, digest), raw in sorted(environment.bodies.items())]))
        image_raw = bytes.fromhex(IMAGE)
        image_words = [int.from_bytes(image_raw[i:i+4], "little") for i in range(0, 32, 4)]
        actual_input = make_input(environment, foundation, image_words, [])
        need(actual_input["parents"] == [] and actual_input["rank"] == 0, "ZERO_PARENT_INPUT")
        need(not any("natVal" in row or "strVal" in row for row in actual_input["rows"]), "NO_RESIDUAL_LITERAL_ROWS")
        input_path = evidence / "native-input.json"
        input_raw = C.canonical(actual_input)
        save(input_path, input_raw)
        output_raw, process = run_checker(Path(assets["native"]["path"]), input_path, evidence, deadline)
        checked = C.parse_json(output_raw)
        C.fields(checked, {"schema", "status", "input_sha256", "input_bytes", "journal", "parents", "mathematical_admission"})
        need(checked["schema"] == "DMKN_NATIVE_DELTA_CONCLUSION_V1"
             and checked["status"] == "CHECKED_CONDITIONAL_RELATION_NOT_ADMISSION"
             and checked["input_sha256"] == sha(input_raw) and checked["input_bytes"] == len(input_raw)
             and checked["parents"] == [] and checked["mathematical_admission"] is False, "EXACT_ZERO_PARENT_CONCLUSION")
        journal_raw = bytes(checked["journal"])
        journal = decode_journal(journal_raw)
        need(journal["image"] == image_words and journal["foundation"] == FOUNDATION
             and journal["policy"] == POLICY and journal["module"] == environment.module
             and journal["summary"] == C.summarize(environment.spec) and journal["rank"] == 0, "EXACT_CHECKED_JOURNAL")
        need(bounded(input_path) == input_raw and bounded(request_path) == C.canonical(request)
             and bounded(map_path) == map_raw and bounded(output / "selection.json", 1024**2) == selection_raw,
             "FINAL_INPUT_BINDINGS")
        result.update(status="PASS_REAL_LITERAL_EXPORT_AND_FRESH_RELOCATED_CHECK", module=environment.module,
                      roots=roots, local_declarations=len(descriptors), raw_literal_rows=len(transcript),
                      source_sha256=sha(source_raw), export_sha256=sha(exported_raw),
                      native_input_sha256=sha(input_raw), native_input_bytes=len(input_raw),
                      native_journal_sha256=sha(journal_raw), native_process=process,
                      parent_count=0, rank=0, all_local_declarations_fresh_checked=True)
    except BaseException as error:
        result["error"] = str(error)[:4096]
    result["wall_seconds"] = time.monotonic() - started
    save(evidence / "NATIVE-RESULT.json", json.dumps(result, sort_keys=True).encode())
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0 if result["status"] == "PASS_REAL_LITERAL_EXPORT_AND_FRESH_RELOCATED_CHECK" else 1


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--output", required=True)
    parser.add_argument("--runtime-map", required=True)
    parser.add_argument("--runtime-map-sha256", required=True)
    return run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
