"""Conditional native authoring controls, not positive receipt/session tests.

The selected retained base bundle has structural group openings and semantic
bodies, but no certificate authority and no imported theorem proofs. The native
context below is explicitly a TEST-ONLY UNTRUSTED packet. No verifier, session,
handle, journal, receipt success or positive mathematical admission is fabricated.
Only a root-selected outer Job may launch this harness. Each native call is a
distinct input; stop on the first unexpected outcome and preserve the prefix.
"""
from pathlib import Path
import argparse
from copy import deepcopy
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
RUNTIME = ROOT/"software/runtime/lean-4.34.0-windows"
MODULE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
FOUNDATION = "d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481"
POLICY = "5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377"


def need(ok, why):
    if not ok: raise ValueError(why)


def load_native_api():
    # Link-only mode needs no product Python API, so its snapshot stays small.
    global C, Address, SourceRows, decode_source, SCHEMA, _records
    global REQUEST_SCHEMA, EXPORT_SCHEMA, NATIVE_NAME_LIMITS
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from modules import codec as C
    from modules.model import Address
    from modules.source_rows import SourceRows, decode_source
    from authoring.context import SCHEMA, _records
    from authoring.source import REQUEST_SCHEMA, EXPORT_SCHEMA, NATIVE_NAME_LIMITS


def pinned(path, digest, maximum):
    path = Path(path)
    need(path.is_absolute() and path.is_file() and path.stat().st_size <= maximum, "TEST_PINNED_FILE")
    with path.open("rb") as stream: raw = stream.read(maximum+1)
    need(len(raw) <= maximum and hashlib.sha256(raw).hexdigest() == digest, "TEST_INPUT_PIN")
    return raw


def save(path, raw):
    with path.open("xb") as stream: stream.write(raw)


def named(*parts): return [["s", part] for part in parts]


def runtime_configuration(path, digest):
    raw = pinned(path, digest, 131072)
    manifest = json.loads(raw)
    need(set(manifest) == {"schema", "root", "files", "scope"}
         and manifest["schema"] == "DMKN_AUTHOR_LEAN_LINK_RUNTIME_V1"
         and Path(manifest["root"]) == RUNTIME and RUNTIME.resolve() == RUNTIME
         and 1 <= len(manifest["files"]) <= 200, "TEST_RUNTIME_MANIFEST")
    required = {"bin/leanc.exe", "bin/clang.exe", "bin/ld.lld.exe", "bin/lld.exe",
                "bin/libclang-cpp.dll", "bin/libLLVM-22.dll", "bin/libleanshared.dll",
                "bin/libleanshared_1.dll", "bin/libleanshared_2.dll", "bin/libInit_shared.dll",
                "include/lean/lean.h", "lib/lean/libleanmanifest.a", "lib/lean/libleanshared.dll.a"}
    need(required <= set(manifest["files"]), "TEST_RUNTIME_REQUIRED_COMPONENTS")

    def verify():
        for relative, item in manifest["files"].items():
            parts = relative.split("/")
            need(all(part not in ("", ".", "..") and "\\" not in part and ":" not in part for part in parts),
                 "TEST_RUNTIME_RELATIVE_PATH")
            file = RUNTIME.joinpath(*parts)
            need(file.resolve() == file and file.is_file() and set(item) == {"bytes", "sha256"}
                 and file.stat().st_size == item["bytes"] <= 512*1024**2, "TEST_RUNTIME_FILE")
            with file.open("rb") as stream: actual = hashlib.file_digest(stream, "sha256").hexdigest()
            need(actual == item["sha256"] and file.stat().st_size == item["bytes"], "TEST_RUNTIME_PIN")
        need(Path(path).read_bytes() == raw, "TEST_RUNTIME_MANIFEST_CHANGED")

    verify()
    # Explicit operation-local owner configuration, never persistent environment
    # mutation. OS DLLs/headers/olean imports are NOT a hermetic build proof.
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith("LEAN_") and key.upper() not in
           {"CPATH", "C_INCLUDE_PATH", "CPLUS_INCLUDE_PATH", "LIBRARY_PATH", "CC", "CFLAGS", "LDFLAGS"}}
    env["LEAN_SYSROOT"] = str(RUNTIME)
    env["PATH"] = str(RUNTIME/"bin") + os.pathsep + os.environ.get("PATH", "")
    return verify, env


def run_captured(argv, destination, environment, timeout):
    """Preserve bounded partial logs even on timeout; whole tree is outer-Job-owned.

    capture_output is bounded by the outer memory/CPU allocation; the1MiB log
    check is POSTHOC, not a hard quota on pipe capture. Only pinned owner inputs
    run here. Logs exceeding the limit retain their first1MiB and actual counts.
    """
    try:
        run = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL, capture_output=True,
                             env=environment, timeout=timeout, check=False)
        stdout, stderr, code, timed_out = run.stdout, run.stderr, run.returncode, False
    except subprocess.TimeoutExpired as error:
        stdout, stderr, code, timed_out = error.stdout or b"", error.stderr or b"", None, True
    save(destination/"stdout.txt", stdout[:1024**2]); save(destination/"stderr.txt", stderr[:1024**2])
    disposition = {"argv": argv, "exit_code": code, "timed_out": timed_out,
                   "stdout_bytes": len(stdout), "stderr_bytes": len(stderr),
                   "logs_truncated": len(stdout) > 1024**2 or len(stderr) > 1024**2,
                   "outer_job_tree_supervision_required": True, "log_cap_is_posthoc": True}
    save(destination/"command.json", json.dumps(disposition, sort_keys=True).encode("utf-8"))
    need(not timed_out, "TEST_NATIVE_CALL_TIMEOUT")
    need(not disposition["logs_truncated"], "TEST_RETURN_LOG_LIMIT")
    return code, stdout, stderr


def fresh_output(value):
    output = Path(value)
    need(output.is_absolute() and output.resolve() == output
         and output.is_relative_to(ROOT/"experiments/v5-local-checks") and not output.exists(),
         "TEST_FRESH_EVIDENCE")
    output.mkdir()
    return output


def link_main(args):
    """One fixed native link from retained successful C; NO Lean elaboration."""
    generated = pinned(args.generated_c, args.generated_c_sha, 2*1024**2)
    verify, environment = runtime_configuration(args.runtime_manifest, args.runtime_manifest_sha)
    output = fresh_output(args.output)
    report = {"schema": "DMKN_AUTHOR_LEAN_LINK_V1", "status": "FAIL", "lean_elaboration_calls": 0,
              "mathematical_acceptance": False, "generated_c_sha256": args.generated_c_sha,
              "runtime_manifest_sha256": args.runtime_manifest_sha,
              "runtime_scope": "EXPLICIT_TOOL_LIBRARY_PINS_NOT_HERMETIC_BUILD",
              "owner_environment": {"LEAN_SYSROOT": str(RUNTIME), "PATH_prefix": str(RUNTIME/"bin")}}
    start = time.monotonic()
    try:
        executable = output/"AuthorLean.exe"
        argv = [str(RUNTIME/"bin/leanc.exe"), "-O0", "-leanshared", args.generated_c, "-o", str(executable)]
        code, unused, unused_error = run_captured(argv, output, environment, 120)
        need(code == 0 and executable.is_file() and 0 < executable.stat().st_size <= 64*1024**2, "TEST_NATIVE_LINK_REQUIRED")
        verify(); need(pinned(args.generated_c, args.generated_c_sha, 2*1024**2) == generated, "TEST_C_REBINDING")
        report.update(status="PASS", executable=str(executable), executable_bytes=executable.stat().st_size,
                      executable_sha256=hashlib.sha256(executable.read_bytes()).hexdigest())
    except BaseException as error:
        report["error"] = repr(error)
    report["wall_seconds"] = time.monotonic()-start
    save(output/"RESULT.json", json.dumps(report, sort_keys=True).encode("utf-8"))
    print(json.dumps(report), flush=True)
    return 0 if report["status"] == "PASS" else 1


def foundation_view(raw):
    """Test-only structural view using the same existing canonical decoder.

    This does not mock a verifier/session and never claims to adopt a foundation.
    The runtime must still compare every supplied descriptor/value with Init.
    """
    rows = C.parse_json(raw)
    C.require(C.canonical(rows) == raw and
              C.hash_value("owner-workload-foundation-candidate", rows) == FOUNDATION,
              "TEST_EXACT_FOUNDATION")
    reader = SourceRows(rows, [], [])
    names = [reader.name(d["name"]) for row in reader.declarations for d in _records(row)]
    env = SourceRows(rows, names, []).module(FOUNDATION, POLICY)
    values = []
    for group in env.spec["groups"]:
        for d in group["declarations"]:
            if d["kind"] not in ("definition", "theorem", "opaque"): continue
            key = (env.local_proofs[Address.of(env.module, d["name"])] if d["kind"] == "theorem"
                   else d["value_hash"])
            values.append({"name": d["name"], "expression": C.parse_json(env.bodies[d["universes"], key])})
    return {"groups": env.spec["groups"], "names": names, "values": values,
            "bodies": [{"universes": u, "digest": digest, "expression": C.parse_json(raw_body)}
                       for (u, digest), raw_body in sorted(env.bodies.items())]}


def test_only_context(bundle_raw, foundation_raw):
    bundle = C.parse_json(bundle_raw)
    C.require(bundle["schema"] == "DMKN_V5_OWNER_WORKLOAD_BUNDLE_V1"
              and bundle["module"] == MODULE and C.module_id(bundle["spec"]) == MODULE
              and bundle["spec"]["foundation"] == FOUNDATION
              and bundle["spec"]["policy"] == POLICY
              and bundle["mathematical_admission"] is False
              and bundle["certificate_verification"] == "NOT_PERFORMED", "TEST_EXACT_CONDITIONAL_BUNDLE")
    spec = bundle["spec"]
    C.require(len(bundle["openings"]) == len(spec["groups"]), "TEST_COMPLETE_OPENINGS")
    bodies = {}
    for item in bundle["bodies"]:
        key = item["universes"], item["digest"]
        C.require(key not in bodies and C.body_id(item["expression"], item["universes"]) == item["digest"],
                  "TEST_SEMANTIC_BODY_BINDING")
        bodies[key] = item
    imports, used = [], set()
    # This retained bundle preserves the source export's dependency-first order.
    # Native checked addition will reject any actual forward/missing dependency.
    for i, group in enumerate(spec["groups"]):
        opening = bundle["openings"][i]
        C.require(opening["index"] == i and C.verify_group_opening(MODULE, opening) == group,
                  "TEST_EXACT_GROUP_OPENING")
        required = set()
        for d in group["declarations"]:
            if d["kind"] == "definition": required.add((d["universes"], d["value_hash"]))
            elif d["kind"] == "recursor":
                required.update((d["universes"], rule["value_hash"]) for rule in d["meta"]["rules"])
        C.require(required <= set(bodies), "TEST_SEMANTIC_BODY_MISSING")
        used.update(required)
        imports.append({"owner": MODULE, "index": i, "group": deepcopy(group),
                        "bodies": [deepcopy(bodies[key]) for key in sorted(required)]})
    # The selected base has no opaque body and no imported theorem proof body.
    C.require(used == set(bodies), "TEST_NO_UNSELECTED_OR_THEOREM_PROOF_BODIES")
    return {"schema": SCHEMA, "foundation": FOUNDATION, "policy": POLICY,
            "foundation_sha256": hashlib.sha256(foundation_raw).hexdigest(),
            "foundation_view": foundation_view(foundation_raw), "imports": imports,
            "selection_binding": C.hash_value("conditional-native-authoring-test-not-a-session", {
                "bundle_sha256": hashlib.sha256(bundle_raw).hexdigest(),
                "foundation_sha256": hashlib.sha256(foundation_raw).hexdigest()}),
            "mathematical_acceptance": False}


def owner_source():
    prefix = "DMKN.Mod.«"+MODULE+"».CommonsV5"
    source = """set_option autoImplicit false
noncomputable section
universe u v w
namespace OwnerV5
theorem fold_map_received {A : Type u} {B : Type v} {C : Type w}
    (f : A -> B) (leaf : B -> C) (node : C -> C -> C) (e : BASE.Tree A) :
    BASE.fold leaf node (BASE.map f e) = BASE.fold (fun x => leaf (f x)) node e := by
  induction e using BASE.Tree.rec with
  | leaf x => rfl
  | node l r ihl ihr => exact BASE.binary_congr node ihl ihr
theorem binder_implicit {A : Sort u} (a : A) : a = a := rfl
theorem binder_explicit (A : Sort u) (a : A) : a = a := rfl
end OwnerV5
""".replace("BASE", prefix)
    return source, [named("OwnerV5", x) for x in
                    ("fold_map_received", "binder_implicit", "binder_explicit")]


def request(context, source, roots):
    return {"schema": REQUEST_SCHEMA, "context": context, "source": source, "roots": roots,
            "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
            "mathematical_acceptance": False}


def references(expr):
    result, pending = set(), [expr]
    children = {"sort": (), "bvar": (), "const": (), "app": (1, 2),
                "lam": (2, 3), "forall": (2, 3), "let": (1, 2, 3), "proj": (3,)}
    while pending:
        node = pending.pop()
        if node[0] in ("const", "proj"):
            ref = node[1]
            if ref[0] == "external": result.add((ref[1], C.name_key(ref[2])))
        pending.extend(node[i] for i in children[node[0]])
    return result


def inspect_positive(export_raw, selected):
    exported = C.parse_json(export_raw)
    C.require(set(exported) == {"schema", "source_sha256", "selection_binding", "roots", "rows",
                               "local_names", "status", "mathematical_acceptance"}, "TEST_EXPORT_FIELDS")
    C.require(exported["schema"] == EXPORT_SCHEMA and exported["source_sha256"] == selected["source_sha256"]
              and exported["selection_binding"] == selected["context"]["selection_binding"]
              and exported["roots"] == selected["roots"] and exported["mathematical_acceptance"] is False
              and exported["status"] == "OWNER_FRONTEND_EXPORT_REQUIRES_INDEPENDENT_RELATION", "TEST_EXPORT_BINDING")
    reader = SourceRows(exported["rows"], [], [], limits=NATIVE_NAME_LIMITS)
    names = [reader.name(d["name"]) for row in reader.declarations for d in _records(row)]
    C.require(len({C.name_key(n) for n in names}) == len(names)
              and sorted(C.name_key(n) for n in names) == sorted(C.name_key(n) for n in exported["local_names"]),
              "TEST_ACTUAL_EXPORT_CENSUS")
    packet = selected["context"]
    externals = [{"source_name": C.relocated_name(item["owner"], d["name"]), "module": item["owner"],
                  "relative_name": d["name"]} for item in packet["imports"] for d in item["group"]["declarations"]]
    env = decode_source(exported["rows"], names, packet["foundation_view"]["names"], FOUNDATION, POLICY,
                        externals, NATIVE_NAME_LIMITS)
    C.validate_spec(env.spec)
    descriptors = {C.name_key(d["name"]): d for group in env.spec["groups"] for d in group["declarations"]}
    roots = selected["roots"]
    C.require(all(C.name_key(n) in descriptors for n in roots), "TEST_ROOT_CAPTURE")
    d = descriptors[C.name_key(roots[0])]
    proof = C.parse_json(env.bodies[d["universes"], env.local_proofs[Address.of(env.module, roots[0])]])
    combined = references(d["type"]) | references(proof)
    expected = {(MODULE, C.name_key(named("CommonsV5", n))) for n in ("Tree", "fold", "map", "binary_congr")}
    C.require(expected <= combined and
              (MODULE, C.name_key(named("CommonsV5", "binary_congr"))) in references(proof),
              "TEST_SUBSTANTIVE_IMPORTED_USE")
    implicit = descriptors[C.name_key(roots[1])]["type"]
    explicit = descriptors[C.name_key(roots[2])]["type"]
    C.require(implicit[0:2] == ["forall", "implicit"] and explicit[0:2] == ["forall", "default"]
              and implicit[2:] == explicit[2:], "TEST_BINDER_INFO_PRESERVED")
    for (u, unused), raw in env.bodies.items(): C.validate_expr(C.parse_json(raw), u)
    return {"conditional_local_module": env.module, "local_groups": len(env.spec["groups"]),
            "local_declarations": len(descriptors), "substantive_import_kinds": ["inductive", "definition", "theorem"],
            "binder_info_distinction_preserved": True, "imported_theorem_proof_bytes": 0,
            "final_relation_checked": False, "positive_handle_or_receipt": False}


def cases(base):
    source, roots = owner_source()
    yield "tree-source-and-binder-capture", request(deepcopy(base), source, roots), None
    damaged = deepcopy(base)
    chosen = next(d for g in damaged["foundation_view"]["groups"] for d in g["declarations"]
                  if d["type"][0] == "forall")
    chosen["type"][1] = "implicit" if chosen["type"][1] == "default" else "default"
    yield "foundation-binder-mismatch", request(damaged, source, roots), "AUTHOR_DECLARATION_TYPE"
    damaged = deepcopy(base)
    chosen_item, rec = next((item, d) for item in damaged["imports"] for d in item["group"]["declarations"]
                            if d["kind"] == "recursor" and d["meta"]["rules"])
    wrong = ["sort", ["zero"]]
    digest = C.body_id(wrong, rec["universes"])
    chosen_item["bodies"].append({"universes": rec["universes"], "digest": digest, "expression": wrong})
    rec["meta"]["rules"][0]["value_hash"] = digest
    yield "regenerated-recursor-rhs-mismatch", request(damaged, source, roots), "AUTHOR_RECURSOR_RULE_RHS"
    damaged = deepcopy(base)
    chosen_item, d = next((item, d) for item in damaged["imports"] for d in item["group"]["declarations"]
                          if d["kind"] == "definition")
    chosen_item["bodies"] = [body for body in chosen_item["bodies"] if body["digest"] != d["value_hash"]]
    yield "missing-transparent-body", request(damaged, source, roots), "AUTHOR_MISSING_BODY"
    bad_source = "axiom OwnerV5.bad (P : Prop) : P\ntheorem OwnerV5.escape (P : Prop) : P := OwnerV5.bad P\n"
    yield "fresh-axiom-refusal", request(deepcopy(base), bad_source, [named("OwnerV5", "escape")]), "NEW_AXIOM_REFUSED"


def controls_main(args):
    load_native_api()
    input_pins = ((args.binary, args.binary_sha, 64*1024**2),
                  (args.bundle, args.bundle_sha, 2*1024**2), (args.foundation, args.foundation_sha, 2*1024**2))
    raws = [pinned(*item) for item in input_pins]
    verify, environment = runtime_configuration(args.runtime_manifest, args.runtime_manifest_sha)
    output = fresh_output(args.output)
    started = time.monotonic(); deadline = started+240
    report = {"schema": "DMKN_CONDITIONAL_NATIVE_AUTHORING_CONTROLS_V1", "status": "FAIL", "cases": [],
              "scope": "TEST_ONLY_UNTRUSTED_CONTEXT_COMPATIBILITY_NOT_LIVE_IMPORT_OR_RECEIPT_ADMISSION",
              "mathematical_acceptance": False, "receipt_verification_calls": 0,
              "positive_handles_created": 0, "final_relation_checked": False}
    try:
        template = test_only_context(raws[1], raws[2])
        for label, selected, expected_error in cases(template):
            destination = output/label; destination.mkdir()
            input_path = destination/"request.json"
            raw = C.canonical(selected); save(input_path, raw)
            remaining = deadline-time.monotonic()
            C.require(remaining > 0, "TEST_ORIGINAL_DEADLINE")
            code, stdout, stderr = run_captured([args.binary, str(input_path), str(destination/"export")],
                                               destination, environment, min(90, remaining))
            result = {"case": label, "exit_code": code,
                      "request_sha256": hashlib.sha256(raw).hexdigest(), "pass": False,
                      "expected_error": expected_error}
            report["cases"].append(result)
            export = destination/"export/EXPORT.json"
            if expected_error is None:
                C.require(code == 0 and export.is_file(), "TEST_NATIVE_POSITIVE_REQUIRED")
                C.require(export.stat().st_size <= 16*1024**2, "TEST_EXPORT_BYTES")
                result["details"] = inspect_positive(export.read_bytes(), selected)
            else:
                combined = stdout.decode("utf-8", errors="replace") + stderr.decode("utf-8", errors="replace")
                C.require(code != 0 and expected_error in combined and not export.exists(), "TEST_EXACT_NATIVE_REFUSAL")
            result["pass"] = True
            save(destination/"RESULT.json", C.canonical(result))
        for item in input_pins: pinned(*item)
        verify()
        report["status"] = "PASS"
    except BaseException as error:
        report["error"] = repr(error)
    report["wall_seconds"] = time.monotonic()-started
    save(output/"RESULT.json", json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    print(json.dumps(report), flush=True)
    return 0 if report["status"] == "PASS" else 1


def main():
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode and not sys.flags.optimize, "CANONICAL_ISOLATED_OWNER_TEST")
    parser = argparse.ArgumentParser()
    modes = parser.add_subparsers(dest="mode", required=True)
    link = modes.add_parser("link")
    control = modes.add_parser("controls")
    for mode in (link, control):
        for key in ("runtime-manifest", "runtime-manifest-sha", "output"):
            mode.add_argument("--"+key, required=True)
    for key in ("generated-c", "generated-c-sha"): link.add_argument("--"+key, required=True)
    for key in ("binary", "binary-sha", "bundle", "bundle-sha", "foundation", "foundation-sha"):
        control.add_argument("--"+key, required=True)
    args = parser.parse_args()
    return link_main(args) if args.mode == "link" else controls_main(args)


if __name__ == "__main__": raise SystemExit(main())
