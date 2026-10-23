"""Small native-free changed-boundary controls for owner source contribution.

Root must separately select execution. All identities/units below are synthetic
inert fixtures, not mathematical acceptance. No native worker, installation,
catalog, network, output file or mock replacement of the admission pipeline.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_contribution as G
import ordinary_evidence as E
import ordinary_semantics as S
import portable_candidate as B
import portable_evidence as PE

MIB = 1024**2
SEMANTIC, FOUNDATION, ROOT = S.semantic_id(), S.foundation_id(), "a"*64


def ensure(ok, code):
    if not ok:
        raise AssertionError(code)


def refuses(action, label, marker=None):
    try:
        action()
    except ValueError as exc:
        ensure(marker is None or marker in str(exc), "WRONG_REFUSAL:"+label+":"+str(exc))
    else:
        raise AssertionError("MISSING_REFUSAL:"+label)


def report(label):
    print("ORDINARY_CONTRIBUTION_CHECK "+label+" PASS mathematical_acceptance=false", flush=True)


def name(text):
    return [[0, {"$bytes": list(text.encode("utf-8"))}]]


def identity(text):
    return hashlib.sha256(text.encode("ascii")).hexdigest()


def acquired(text, unit_label=None):
    own, unit = name(text), identity("unit:"+(unit_label or text))
    return {"name": own, "unit_id": unit,
            "export_id": S.export_id(SEMANTIC, unit, own)}


def input_controls():
    source = "-- owner source, not a sentinel template\ndef callerChosen : Nat := 0\n".encode()
    targets = [acquired("AcquiredSecond"), acquired("AcquiredFirst")]
    outputs = [name("CallerOutput"), name("\u7814\u7a76\u7d50\u679c")]
    checked = G.validate_inputs(SEMANTIC, targets, source, outputs)
    ensure(checked["source_body"] == source and type(checked["source_body"]) is bytes and
           len(checked["acquired_targets"]) == len(checked["output_names"]) == 2,
           "MULTI_INPUTS_PRESERVED")
    frozen = deepcopy(checked)
    targets[0]["name"][0][1]["$bytes"].append(88)
    outputs[0][0][1]["$bytes"].append(88)
    ensure(checked == frozen, "INPUT_CONTAINER_ALIAS")
    ensure(G.validate_inputs(SEMANTIC, [], source, frozen["output_names"])["acquired_targets"] == [],
           "EMPTY_ACQUIRED_REJECTED")
    # Encoded Lean names, not dotted display strings, determine equality.
    distinct = [name("A.B"), name("A")+name("B")]
    ensure(len(G.validate_inputs(SEMANTIC, [], source, distinct)["output_names"]) == 2,
           "DOTTED_NAME_ALIAS")
    stable = [acquired("AcquiredFirst"), acquired("AcquiredSecond")]
    for field in ("unit_id", "export_id", "name"):
        bad = deepcopy(stable)
        bad[0][field] = name("Different") if field == "name" else identity("wrong")
        refuses(lambda bad=bad: G.validate_inputs(SEMANTIC, bad, source, frozen["output_names"]),
                "ACQUIRED_EXACT_"+field)
    duplicate = [stable[0], deepcopy(stable[0])]
    refuses(lambda: G.validate_inputs(SEMANTIC, duplicate, source, frozen["output_names"]),
            "DUPLICATE_ACQUIRED")
    conflict = [stable[0], acquired("AcquiredFirst", "DifferentUnit")]
    refuses(lambda: G.validate_inputs(SEMANTIC, conflict, source, frozen["output_names"]),
            "CONFLICTING_ACQUIRED_NAME")
    refuses(lambda: G.validate_inputs(SEMANTIC, stable, source, [stable[0]["name"]]),
            "ACQUIRED_OUTPUT_COLLISION")
    refuses(lambda: G.validate_inputs(SEMANTIC, [], source, [name("Out"), name("Out")]),
            "DUPLICATE_OUTPUT")
    refuses(lambda: G.validate_inputs(SEMANTIC, [], source, []), "EMPTY_OUTPUTS")
    for body in (source.decode(), bytearray(source), b"\xff", b"x"*(MIB+1)):
        refuses(lambda body=body: G.validate_inputs(SEMANTIC, [], body, frozen["output_names"]),
                "SOURCE_TYPE_UTF8_OR_SIZE")
    ensure(len(G.validate_inputs(SEMANTIC, [], b"--"+b"x"*(MIB-2),
                                 [name("Bounded")])["source_body"]) == MIB,
           "SOURCE_EXACT_BYTE_BOUND")
    maximum_acquired = [acquired("Choice"+str(i)) for i in range(32)]
    maximum_outputs = [name("Result"+str(i)) for i in range(32)]
    ensure(len(G.validate_inputs(SEMANTIC, maximum_acquired, source, maximum_outputs)["output_names"]) == 32,
           "EXACT_TARGET_COUNT_BOUND")
    refuses(lambda: G.validate_inputs(SEMANTIC, maximum_acquired+[acquired("Overflow")], source,
                                      maximum_outputs), "ACQUIRED_COUNT_BOUND")
    refuses(lambda: G.validate_inputs(SEMANTIC, [], source, maximum_outputs+[name("Overflow")]),
            "OUTPUT_COUNT_BOUND")
    refuses(lambda: G.validate_inputs(SEMANTIC, [], source, [name("N"*22000)]),
            "OUTPUT_NAME_BYTE_BOUND")
    refuses(lambda: G.validate_inputs(SEMANTIC, [], source, [name("_kernel_fresh_forbidden")]),
            "RESERVED_OUTPUT_NAME")
    report("multiple_empty_detached_exact_inputs_and_bounds")
    return source, stable, frozen["output_names"]


def request_controls(acquired_targets):
    bindings = {E.name_key(row["name"]): row["export_id"] for row in acquired_targets}
    lookups = []

    def warranted(encoded):
        lookups.append(E.name_key(encoded))
        return bindings.get(E.name_key(encoded))

    targets = G.request_targets(SEMANTIC, acquired_targets, warranted)
    ensure({E.name_key(n): symbol for n, symbol in targets} == bindings and
           set(lookups) == set(bindings), "MULTIPLE_REQUEST_TARGETS")
    eq = name("Eq")
    eq_id = S.basis_symbol_id(SEMANTIC, FOUNDATION, eq)
    empty_lookups = []

    def basis_warranted(encoded):
        empty_lookups.append(encoded)
        return eq_id if encoded == eq else None

    ensure(G.request_targets(SEMANTIC, [], basis_warranted) == [[eq, eq_id]] and
           empty_lookups == [eq], "EMPTY_REQUEST_EXACT_PROTECTED_BASIS_ANCHOR")
    refuses(lambda: G.request_targets(SEMANTIC, [], lambda _: identity("wrong-eq")),
            "EMPTY_ANCHOR_IDENTITY")
    refuses(lambda: G.request_targets(SEMANTIC, acquired_targets, lambda _: None),
            "UNWARRANTED_ACQUIRED")
    refuses(lambda: G.request_targets(SEMANTIC, acquired_targets, lambda _: identity("wrong-meaning")),
            "ACQUIRED_WARRANT_IDENTITY")
    report("multiple_request_targets_and_empty_basis_anchor")


def assembly_controls():
    body = ("-- __DMKN_REQUEST_DIRECTORY__ is literal caller text, not a template marker.\n"
            "-- Unicode source stays byte-for-byte: \u6570\u5b66\n"
            "def callerChosen : Nat := 0\n").encode("utf-8")
    root = Path(__file__).resolve().parents[3] / "never-created-generic-controls"
    args = {"source_body": body, "request_directory": root/"owner request",
            "semantic_id": SEMANTIC, "context_root": ROOT, "foundation_id": FOUNDATION,
            "targets_file": root/"output names.json", "candidate_file": root/"candidate.json"}
    generated = G.assemble_source(**args)
    ensure(type(generated) is bytes and generated.count(body) == 1 and
           generated.count(b"__DMKN_REQUEST_DIRECTORY__") == 1,
           "CALLER_SOURCE_BYTES_OR_SENTINEL_REPLACEMENT")
    decoded = generated.decode("utf-8")
    ensure("public import Init" in decoded.splitlines() and "public section" in decoded.splitlines() and
           "PortableContributionExportCommand" in decoded and
           "#ordinary_construct_portable " in decoded and "#ordinary_export_contribution " in decoded and
           generated.index(body) > generated.index(b"#ordinary_construct_portable ") and
           generated.index(body) < generated.rindex(b"#ordinary_export_contribution "),
           "FIXED_PRELUDE_BODY_POSTLUDE")
    for field in ("request_directory", "targets_file", "candidate_file"):
        ensure(json.dumps(str(args[field]), ensure_ascii=True).encode("ascii") in generated,
               "GENERATED_PATH_QUOTING:"+field)
    as_strings = {key: str(value) if type(value) is type(root) else value for key, value in args.items()}
    ensure(G.assemble_source(**as_strings) == generated, "PATH_STRING_ASSEMBLY_DIFFERS")
    for source in (b"\xff", b"bad\0source", b"x"*(MIB+1)):
        refuses(lambda source=source: G.assemble_source(**{**args, "source_body": source}),
                "ASSEMBLY_SOURCE_VALIDATION")
    refuses(lambda: G.assemble_source(**{**args, "semantic_id": "not-an-id"}),
            "ASSEMBLY_ID_VALIDATION")
    report("marker_free_exact_utf8_source_and_fixed_name_file_postlude")


def synthetic_unit(text, dependency=None):
    own, nat = name(text), name("Nat")
    typ = [E.EXPR_FORMAT, [], [[2, nat, []]], 0]
    body = ([E.EXPR_FORMAT, [], [[7, {"$bytes": []}]], 0] if dependency is None else
            [E.EXPR_FORMAT, [], [[2, name(dependency), []]], 0])
    return [E.UNIT_FORMAT, [0, own, [], typ, body, [2, 1], [own]],
            [[own, 1, [], typ, [body, [2, 1], [own]]]]]


def multi_output_controls():
    first, second = synthetic_unit("GenericOne"), synthetic_unit("GenericTwo", "GenericOne")
    targets = [name("GenericTwo"), name("GenericOne")]
    nat = name("Nat")
    nat_id = S.basis_symbol_id(SEMANTIC, FOUNDATION, nat)
    prepared = {E.name_key(nat): nat_id}
    doc = {"schema": B.SCHEMA, "assurance": B.ASSURANCE, "semantic_id": SEMANTIC,
           "foundation_id": FOUNDATION, "context_root": ROOT, "targets": targets,
           "boundary_imports": [[nat, nat_id]], "unresolved_imports": [], "units": [first, second],
           "stats": {"source_records_enumerated": 0, "selected_units": 2,
                     "dependency_edges": 0, "scan_nodes": 0,
                     "unit_json_bytes": sum(len(E.canonical_json(x)) for x in (first, second)),
                     "boundary_imports": 1, "unresolved_imports": 0}}
    def bind(expected):
        return B.bind_candidate(E.canonical_json(doc), semantic_id=SEMANTIC,
            foundation_id=FOUNDATION, context_root=ROOT, expected_targets=expected,
            prepared_bindings=prepared, warranted_symbol=lambda encoded: prepared.get(E.name_key(encoded)))
    bound = bind(targets)
    ensure(bound.status == "READY" and bound.mathematical_acceptance is False and
           len(bound.raw_units) == 2 and bound.targets == tuple(E.name_key(n) for n in targets),
           "MULTI_TARGET_INERT_BINDING")
    published = G.publication_targets(SEMANTIC, bound.raw_units, targets)
    parsed = [PE.read_evidence(raw) for raw in bound.raw_units]
    expected = [{"name": name(label), "unit_id": item.unit_id,
                 "export_id": S.export_id(SEMANTIC, item.unit_id, name(label))}
                for item, label in ((parsed[1], "GenericTwo"), (parsed[0], "GenericOne"))]
    ensure(published == expected, "ALL_OUTPUTS_EXACT_UNIT_EXPORT_BINDING")
    refuses(lambda: bind(targets[:1]), "NO_DROPPED_EXPECTED_OUTPUT", "CANDIDATE_EXACT_TARGETS")
    refuses(lambda: G.publication_targets(SEMANTIC, bound.raw_units, [name("Absent")]),
            "UNPUBLISHED_OUTPUT_MISSING")
    # Two exported names can share one inert complete unit. This is a small
    # syntactically valid mutual-inductive inventory, not native-checked math.
    # This tests only the inert mapper; it does not qualify requesting inductive
    # outputs through the definition/theorem-only native wrapper.
    own = [name("EmptyTypeA"), name("EmptyTypeB")]
    sort = [E.EXPR_FORMAT, [[0]], [[1, 0]], 0]
    group = [E.UNIT_FORMAT, [3, [], 0, [[n, sort, []] for n in own]],
             [[n, 4, [], sort, [0, 0, own, [], 0, 0, 0, 0]] for n in own]]
    group_raw = E.canonical_json({"schema": PE.SCHEMA, "semantic_id": SEMANTIC,
                                 "imports": [], "unit": group})
    grouped = G.publication_targets(SEMANTIC, [group_raw], own)
    parsed_group = PE.read_evidence(group_raw)
    ensure(len(grouped) == 2 and {row["unit_id"] for row in grouped} == {parsed_group.unit_id} and
           [row["export_id"] for row in grouped] == [S.export_id(SEMANTIC, parsed_group.unit_id, n) for n in own],
           "MULTIPLE_EXPORTS_MUST_SHARE_UNIT_EVIDENCE")
    refuses(lambda: G.publication_targets(SEMANTIC, [group_raw, group_raw], own),
            "DUPLICATE_PUBLICATION_UNITS")
    wrong_semantic = PE.read_evidence(group_raw).document
    wrong_semantic["semantic_id"] = identity("unsupported-semantic")
    refuses(lambda: G.publication_targets(SEMANTIC, [E.canonical_json(wrong_semantic)], own),
            "PUBLICATION_SEMANTICS")
    report("multiple_inert_candidate_outputs_and_publication_locators")


def failure_report_controls():
    # Direct error-payload contract only. No fake owner.admit, forged checker
    # report or claim that this test has admitted mathematics.
    accepted = {"status": "SYNTHETIC_TEST_ONLY_NOT_ADMISSION", "local_root": identity("retained-root")}
    problem = OSError("synthetic publication storage failure")
    error = G.ContributionError("PUBLICATION_BYTES", problem, accepted=accepted,
                                native_cpu_seconds=2.5)
    ensure(isinstance(error, Exception) and error.report["phase"] == "PUBLICATION_BYTES" and
           error.report["error_type"] == "OSError" and error.report["error"] == str(problem) and
           error.report["accepted"] == accepted and error.report["native_cpu_seconds"] == 2.5 and
           "PRESERVED" in error.report["retention"], "POST_ADMISSION_FAILURE_INFORMATION")
    accepted["local_root"] = identity("changed-caller-copy")
    ensure(error.report["accepted"]["local_root"] == identity("retained-root"),
           "FAILURE_REPORT_ALIASES_CALLER_STATE")
    early = G.ContributionError("REQUEST", ValueError("synthetic preparation refusal"))
    ensure(early.report["accepted"] is None and early.report["native_cpu_seconds"] == 0.0,
           "EARLY_FAILURE_MUST_NOT_INVENT_ACCEPTANCE")
    report("failure_payload_retains_state_without_filesystem_or_acceptance")


def main():
    source, targets, outputs = input_controls()
    request_controls(targets)
    assembly_controls()
    multi_output_controls()
    failure_report_controls()
    print("ORDINARY_CONTRIBUTION_ALL_PASS groups=5 mathematical_acceptance=false", flush=True)


if __name__ == "__main__":
    main()
