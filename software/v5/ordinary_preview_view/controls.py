"""Focused offline renderer/wrapper controls; root selects execution separately."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
TYPE_START = "\n\nTYPE (complete):\n"
TYPE_END = "\n\nSYMBOLS (binding index, exact name, SymbolID):\n"
START, CPU = time.monotonic(), time.process_time()


def need(ok, code):
    if not ok:
        raise AssertionError("PREVIEW_CONTROL_" + code)


def check():
    need(time.monotonic()-START < 45 and time.process_time()-CPU < 20, "ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def write(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def name(*parts):
    return [[1, part] if type(part) is int else
            [0, {"$bytes": list(part.encode("utf-8"))}] for part in parts]


def refuses(call, code=None):
    try:
        call()
    except ValueError as error:
        need(code is None or str(error) == code, "WRONG_REFUSAL:" + str(error))
    else:
        raise AssertionError("PREVIEW_CONTROL_REFUSAL_EXPECTED:" + str(code))


def type_text(view):
    check()
    need(view["status"] == "TYPE_DISPLAY_COMPLETE" and view["complete"] is True
         and view["limitation"] is None and view["mathematical_acceptance"] is False,
         "COMPLETE_STATUS")
    text = view["view_text"]
    need(type(text) is str and text.isascii() and
         len(text) == view["counters"]["output_bytes"], "ASCII_OUTPUT")
    need(all(0 <= n <= view["limits"][key] for key, n in view["counters"].items()),
         "COUNTER_BOUND")
    need(text.count(TYPE_START) == 1 and text.count(TYPE_END) == 1, "SECTIONS")
    return " ".join(text.split(TYPE_START, 1)[1].split(TYPE_END, 1)[0].split())


def incomplete(view, counter=None):
    check()
    need(view["status"] == "TYPE_DISPLAY_INCOMPLETE" and view["complete"] is False
         and view["view_text"] is None and view["mathematical_acceptance"] is False,
         "NO_PARTIAL_VIEW")
    need(view["limitation"]["code"] == "DISPLAY_LIMIT" and
         (counter is None or view["limitation"]["counter"] == counter), "LIMIT_REASON")
    need(all(0 <= n <= view["limits"][key] for key, n in view["counters"].items()),
         "INCOMPLETE_COUNTER_BOUND")


def pure_controls(modules, report):
    E, P = modules["ordinary_evidence"], modules["portable_preview"]
    OP, R = modules["ordinary_preview"], modules["_ordinary_preview_view_render"]
    render = lambda raw, **kw: R.render_preview(raw, codec=P, evidence=E, **kw)
    groups = []

    def fixture(nodes, levels=(), params=()):
        # Existing validators define fixture syntax and the exact reference census.
        header = [2, list(params), [E.EXPR_FORMAT, list(levels), nodes, len(nodes)-1]]
        keys, _ = OP._type_census(header, OP.DEFAULT_LIMITS)
        return E.canonical_json(dict(schema=P.SCHEMA,
            semantic_id=report["result"]["preview"]["semantic_id"], unit_id="a"*64,
            export_name=name("Fixture", "claim"), header=header,
            type_bindings=[[E.strict_json(key), "f"*64] for key in keys]))

    raw = E.canonical_json(report["result"]["preview"])
    calls = []
    def read_once(value):
        calls.append(sha(value))
        return P.read_preview(value)
    real = R.render_preview(raw, codec=SimpleNamespace(read_preview=read_once), evidence=E)
    text = type_text(real)
    need(calls == [sha(raw)] and real["preview_sha256"] == sha(raw) and
         real["preview_bytes"] == 4798 and real["root_node"] == 74, "REAL_IDENTITY_PARSE_ONCE")
    for fragment in (
        "forall {A#b0 : Sort(succ(u#u0))}", "forall {S#b1 : Sort(succ(v#u1))}",
        "observe#b2", "step#b4", "effect#b7", "atomic_law#b9",
        "(observe#b2 (step#b4 a#b10 s#b11))",
        "(ResetEffects.Mode.eval#c7 (effect#b7 a#b10) (observe#b2 s#b11))",
        "(Eq#c3.{succ(zero)} Bool#c2 (observe#b2 s0#b12) Bool.false#c0)",
        "(Eq#c3.{succ(zero)} Bool#c2 (observe#b2 s1#b13) Bool.true#c1)",
        "ResetEffects.ContextuallyRefines#c6.{u#u0,v#u1} A#b0 S#b1 observe#b2 step#b4 p#b16 q#b17",
        "(ResetEffects.summary#c5.{u#u0} A#b0 effect#b7 p#b16)",
        "(ResetEffects.summary#c5.{u#u0} A#b0 effect#b7 q#b17)"):
        need(fragment in text, "REAL_PREMISE_OR_REFERENCE:" + fragment)
    need(text.count("forall ") == 18, "REAL_BINDER_CENSUS")
    for _, identity in report["result"]["preview"]["type_bindings"]:
        need(identity in real["view_text"], "REAL_SYMBOL_ID")
    groups.append("retained-complete-type-all-premises-identities-and-one-parse")

    # One shared lambda node is expanded twice; its shared bvar must change scope.
    shared = fixture([[1, 0], [0, 0], [4, name("x"), 0, 0, 1], [3, 2, 2]], [[0]])
    need(type_text(render(shared)) ==
         "((fun (x#b0 : Sort(zero)) => x#b0) (fun (x#b1 : Sort(zero)) => x#b1))",
         "SHARED_BINDER_CAPTURE")
    domain = fixture([[1, 0], [0, 0], [5, name("x"), 0, 1, 1],
                      [5, name("A"), 1, 0, 2]], [[0]])
    need(type_text(render(domain)) ==
         "forall {A#b0 : Sort(zero)}, forall (x#b1 : A#b0), x#b1", "DOMAIN_SCOPE")
    for nondep in (0, 1):
        let = fixture([[1, 0], [0, 0], [6, name("x"), 1, 1, 1, nondep],
                       [5, name("y"), 0, 0, 2]], [[0]])
        need(type_text(render(let)) == "forall (y#b0 : Sort(zero)), " +
             "(let[nondep=" + str(nondep) + "] (x#b1 : y#b0) := y#b0 in x#b1)",
             "LET_SCOPE_AND_FLAG")
    nodes = [[1, 0], [0, 0]] + [[4, name("x"), code, 0, 1] for code in range(4)]
    nodes.extend([[3, 2, 3], [3, 6, 4], [3, 7, 5]])
    infos = type_text(render(fixture(nodes, [[0]])))
    for code, (left, right) in enumerate((("(", ")"), ("{", "}"), ("{{", "}}"), ("[", "]"))):
        token = "x#b" + str(code)
        need("(fun " + left + token + " : Sort(zero)" + right + " => " + token + ")" in infos,
             "BINDER_INFO:" + str(code))
    groups.append("shared-occurrence-domain-let-and-all-binder-information-scopes")

    names = [name("A.B"), name("A", "B"), name("Root", "1"), name("Root", 1),
             name("\u00e9"), name("e\u0301"), name("\u202e"), name("Root", "")]
    nodes = [[2, value, []] for value in names]
    current = 0
    for index in range(1, len(names)):
        nodes.append([3, current, index]); current = len(nodes)-1
    distinct = render(fixture(nodes))
    need(type_text(distinct).count("#c") == len(names), "DISTINCT_REFERENCE_ROWS")
    for exact in ('str("A.B")', 'str("A") / str("B")', 'str("Root") / str("1")',
                  'str("Root") / num(1)', 'str("\\u00e9")', 'str("e\\u0301")',
                  'str("\\u202e")', 'str("Root") / str("")'):
        need(exact in distinct["view_text"], "EXACT_NAME:" + exact)
    need(distinct["view_text"].count("f"*64) == len(names), "SAME_ID_DISTINCT_NAMES")
    levels = [[4, 0], [4, 1], [2, 0, 1], [3, 1, 0], [1, 2]]
    universe = render(fixture([[1, 4], [2, name("C"), [2, 3, 0, 1]], [3, 1, 0]],
                              levels, [name("u"), name("v"), name("unused")]))
    need(type_text(universe) ==
         "(C#c0.{max(u#u0,v#u1),imax(v#u1,u#u0),u#u0,v#u1} Sort(succ(max(u#u0,v#u1))))",
         "UNIVERSE_ORDER_AND_SORT")
    need('unused#u2 | str("unused")' in universe["view_text"], "UNUSED_PARAMETER")
    literal = fixture([[7, {"$bytes": []}], [7, {"$bytes": [1, 0, 255]}],
                       [9, {"$bytes": list("A\n\u03bb".encode("utf-8"))}],
                       [8, name("Struct"), 3, 2], [3, 1, 0], [3, 4, 3]])
    need(type_text(render(literal)) ==
         '(nat[be:0x0100ff] nat[be:0x;zero] (proj Struct#c0 field=3 string("A\\u000a\\u03bb")))',
         "LITERAL_AND_PROJECTION")
    groups.append("typed-names-symbol-ids-universes-literal-bytes-and-projection-binding")

    levels = [[0]] + [[1, i-1] for i in range(1, 1101)]
    deep = type_text(render(fixture([[1, 1100]], levels)))
    need(deep.count("succ(") == 1100 and deep.startswith("Sort("), "ITERATIVE_DEEP_LEVELS")
    levels = [[0]] + [[2, i-1, i-1] for i in range(1, 23)]
    incomplete(render(fixture([[1, 22]], levels), limits={"universe_occurrences": 16}),
               "universe_occurrences")
    nodes = [[2, name("C"), []]] + [[3, i-1, i-1] for i in range(1, 20)]
    incomplete(render(fixture(nodes), limits={"expression_occurrences": 16}),
               "expression_occurrences")
    simple = fixture([[1, 0]], [[0]])
    complete = render(simple); type_text(complete)
    incomplete(render(simple, limits={"output_bytes": len(complete["view_text"])-1}), "output_bytes")
    incomplete(render(domain, limits={"binder_tokens": 1}), "binder_tokens")
    incomplete(render(simple, limits={"live_frames": 1}), "live_frames")
    for limits in ({"output_bytes": True}, {"output_bytes": 0},
                   {"output_bytes": R.DEFAULT_LIMITS["output_bytes"]+1}, {"unknown": 1}):
        refuses(lambda limits=limits: render(simple, limits=limits))
    refuses(lambda: render(b"{}"))
    groups.append("deep-input-shared-expansion-output-rollback-and-lowering-only-budgets")
    return groups


def wrapper_controls(W, args, output, original, report):
    groups, serial = [], 0
    def invoke(raw, error=None, *, wrong_hash=False, existing=False):
        nonlocal serial
        serial += 1; check()
        path, destination = output / ("report-%02d.json" % serial), output / ("view-%02d" % serial)
        write(path, raw)
        if existing:
            destination.mkdir(); write(destination / "sentinel", b"retained")
        call = lambda: W.view_selected(Path(args.package), args.profile_sha256, path,
                                       "0"*64 if wrong_hash else sha(raw), destination)
        if error:
            refuses(call, error)
            need(destination.exists() == existing, "REFUSAL_OUTPUT")
            if existing:
                need((destination / "sentinel").read_bytes() == b"retained" and
                     len(list(destination.iterdir())) == 1, "NO_OVERWRITE")
            return
        receipt = call()
        view = json.loads((destination / "VIEW.json").read_bytes())
        need(receipt["status"] == "TYPE_DISPLAY_COMPLETE" and
             (destination / "TYPE.txt").read_bytes() == view["view_text"].encode("ascii"),
             "WRAPPER_OUTPUT")
        need(set(p.name for p in destination.iterdir()) == {"VIEW.json", "TYPE.txt"} and
             view["report_sha256"] == sha(raw) and
             view["selected_profile_sha256"] == args.profile_sha256 and
             view["original_report_profile_sha256"] == report["profile_sha256"] and
             not any(view[k] for k in ("mathematical_acceptance", "network_reverified",
                                      "evidence_bound", "package_authenticated")), "WRAPPER_ASSURANCE")

    invoke(b'{"operation":"preview","operation":"preview"}', "VIEW_JSON_DUPLICATE")
    invoke(original, "VIEW_REPORT_PIN", wrong_hash=True)
    changed = deepcopy(report); changed["result"]["preview_bytes"] += 1
    invoke(encoded(changed), "VIEW_RECORD_BYTES")
    invoke(original, "VIEW_OUTPUT_EXISTS", existing=True)
    groups.append("actual-wrapper-duplicate-mismatch-hash-and-existing-output-refusals")
    changed = deepcopy(report)
    changed["catalog"] = changed["custody"] = str(ROOT / "DO-NOT-OPEN-preview-control.sqlite")
    changed["source"] = {"path": str(ROOT / "DO-NOT-OPEN-preview-control.lean")}
    invoke(encoded(changed))
    refuses(lambda: W.strict_report(b"["*65 + b"0" + b"]"*65), "VIEW_JSON_DEPTH")
    refuses(lambda: W.strict_report(b"1"*21), "VIEW_JSON_INTEGER")
    refuses(lambda: W.strict_report(b"1e9999"), "VIEW_JSON_FLOAT")
    groups.append("actual-wrapper-ignores-report-paths-preserves-provenance-and-bounds-json")
    return groups


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    for key in ("package", "profile-sha256", "report", "report-sha256", "wrapper-sha256", "output"):
        parser.add_argument("--"+key, required=True)
    args = parser.parse_args()
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "PYTHON")
    wrapper = Path(__file__).absolute().parent / "view_preview.py"
    raw = wrapper.read_bytes(); need(sha(raw) == args.wrapper_sha256, "WRAPPER_PIN")
    spec = importlib.util.spec_from_file_location("_preview_control_wrapper", wrapper)
    W = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(wrapper), "exec", dont_inherit=True), W.__dict__)
    output = W.ordinary_path(Path(args.output), fresh=True, directory=True)
    need(output.is_relative_to(ROOT / "experiments/v5-local-checks"), "OUTPUT_SCOPE")
    report_path = Path(args.report)
    original = W.read(report_path, 2*W.MIB)
    need(sha(original) == args.report_sha256, "REPORT_PIN")
    report = W.strict_report(original)
    profile_path = Path(args.package) / "PROFILE.json"
    profile_raw = W.read(profile_path, 2*W.MIB)
    need(sha(profile_raw) == args.profile_sha256, "PROFILE_PIN")
    allowed = {wrapper, wrapper.parent / "render.py", report_path, profile_path}
    allowed.update(Path(args.package) / relative for _, relative, _ in W.CODECS)
    pins = {str(path): sha(path.read_bytes()) for path in allowed}
    output.mkdir()
    original_open = Path.open
    def guarded_open(path, mode="r", *a, **kw):
        path = path.absolute()
        if any(flag in mode for flag in "wax+"):
            need(path.is_relative_to(output) and "x" in mode and
                 not any(flag in mode for flag in "wa+"), "UNSELECTED_WRITE")
        else:
            need(path in allowed or path.is_relative_to(output), "UNSELECTED_READ:" + str(path))
        return original_open(path, mode, *a, **kw)
    def forbidden(*a, **kw):
        raise AssertionError("PREVIEW_CONTROL_UNSELECTED_EXECUTION")
    with ExitStack() as stack:
        stack.enter_context(patch.object(Path, "open", guarded_open))
        for target in ("subprocess.Popen", "socket.socket", "socket.create_connection",
                       "sqlite3.connect", "os.system", "os.startfile"):
            stack.enter_context(patch(target, forbidden))
        with W.selected_modules(Path(args.package)) as modules:
            groups = pure_controls(modules, report)
        groups.extend(wrapper_controls(W, args, output, original, report))
        for path, pin in pins.items():
            need(sha(Path(path).read_bytes()) == pin, "INPUT_PRESERVED:" + path)
    check()
    result = dict(status="PASS_OFFLINE_PREVIEW_CONTROLS", groups=groups,
        group_count=len(groups), profile_sha256=args.profile_sha256,
        report_sha256=args.report_sha256, source_and_input_pins=pins,
        mathematical_acceptance=False, product_commands_executed=0,
        scope="PURE_VALIDATED_DISPLAY_AND_OFFLINE_WRAPPER_NOT_NATIVE_OR_NETWORK",
        wall_seconds=time.monotonic()-START, controller_cpu_seconds=time.process_time()-CPU)
    write(output / "RESULT.json", encoded(result))
    print(encoded(result).decode("utf-8"), flush=True)


if __name__ == "__main__":
    main()
