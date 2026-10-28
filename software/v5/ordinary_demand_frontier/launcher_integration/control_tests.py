"""Native-free frontier-option controls; no owner, service or launcher run()."""
import hashlib
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
BASE = ROOT / "experiments/v5-local-checks/demand-frontier-package01/distribution/package/run.py"
BASE_SHA = "47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39"
SOURCE_SHA = "63f70a8f27645e4e3e3f2ae85296f9c43bc2f0337b4534744dbd5eb0411029dd"


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def load(path, digest):
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == digest, "CONTROL_SOURCE_PIN")
    # run.py imports standard libraries and defines helpers; its main guard is
    # false here. Never call run(), main(), arguments() or any supervisor.
    return raw, runpy.run_path(str(path), run_name="_frontier_parser_control")


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "CONTROL_PROCESS")
    source = Path(__file__).resolve().parent.parent / "run_frontier.py"
    old_raw, old = load(BASE, BASE_SHA)
    new_raw, new = load(source, SOURCE_SHA)
    parse, previous = new["child_arguments"], old["child_arguments"]
    passed = []

    def refuses(fn, tool, tokens, expected):
        try:
            fn(tool, tokens)
        except ValueError as error:
            need(str(error) == expected, "CONTROL_WRONG_REFUSAL:" + str(error))
        else:
            raise AssertionError("CONTROL_EXPECTED_REFUSAL:" + expected)

    frontier, parent = "ab" * 32, "cd" * 32
    tokens = ["--", "contribute", "--parent-root", parent,
              "--project-authoring", r"C:\inputs\project.json",
              "--project-authoring-sha256", "ef" * 32,
              "--authoring-frontier-root", frontier]
    original = list(tokens)
    tail, options = parse("owner", tokens)
    need(tail == tokens[1:] and tokens == original and
         options["authoring-frontier-root"] == frontier and
         options["parent-root"] == parent, "CONTROL_EXACT_FORWARDING")
    passed.append("valid_frontier_preserves_parent_and_tokens")

    for bad in ("a" * 63, "a" * 65, "A" * 64, "g" * 64):
        refuses(parse, "owner", ["contribute", "--authoring-frontier-root", bad], "RUN_SHA256")
    passed.append("new_frontier_rejects_malformed_hex")
    refuses(parse, "owner", ["contribute", "--authoring-frontier-root", frontier,
                             "--authoring-frontier-root", frontier], "RUN_DUPLICATE_OPTION")
    passed.append("new_frontier_rejects_duplicate")
    refuses(parse, "owner", ["contribute", "--authoring-frontier-root"],
            "RUN_UNAPPROVED_OPTION_OR_MISSING_VALUE")
    refuses(parse, "owner", ["contribute", "--authoring-frontier-root=" + frontier],
            "RUN_EXACT_OPTION")
    passed.append("new_frontier_rejects_missing_or_equals_value")
    for tool, prefix in (("peer", ["find"]), ("query", [])):
        refuses(parse, tool, prefix + ["--authoring-frontier-root", frontier],
                "RUN_UNAPPROVED_OPTION_OR_MISSING_VALUE")
    passed.append("new_frontier_rejected_for_other_tools")

    without_frontier = tokens[:-2]
    need(parse("owner", without_frontier) == previous("owner", without_frontier),
         "CONTROL_OLD_OWNER_GRAMMAR")
    refuses(previous, "owner", tokens, "RUN_UNAPPROVED_OPTION_OR_MISSING_VALUE")
    passed.append("unchanged_invocation_and_frozen_omission")

    a = b'"module-targets", "module-anchor", "output-names", "project-authoring",'
    b = a + b' "authoring-frontier-root",'
    c = b'        value = tokens.pop(0)\n        options[key] = value'
    d = (b'        value = tokens.pop(0)\n        if key == "authoring-frontier-root":\n'
         b'            hexid(value)\n        options[key] = value')
    need(old_raw.count(a) == old_raw.count(c) == 1 and
         new_raw == old_raw.replace(a, b).replace(c, d), "CONTROL_EXACT_TWO_DELTAS")
    need(new["OPTIONS"]["owner"] == old["OPTIONS"]["owner"] | {"authoring-frontier-root"} and
         all(new["OPTIONS"][k] == old["OPTIONS"][k] for k in ("peer", "query")) and
         new["PATH_OPTIONS"] == old["PATH_OPTIONS"] and new["CEILINGS"] == old["CEILINGS"],
         "CONTROL_NO_OTHER_ROUTING_OR_LIMIT_DELTA")
    passed.append("exact_source_and_other_grammar_preserved")
    print(json.dumps({"status": "FOCUSED_FRONTIER_LAUNCHER_CONTROLS_PASSED",
        "groups": passed, "source_sha256": SOURCE_SHA, "base_sha256": BASE_SHA,
        "native_calls": 0, "owner_operations": 0, "child_launches": 0,
        "claim": "PARSER_ONLY_NOT_INSTALLED_OPERATION_OR_MATHEMATICAL_ACCEPTANCE"}, sort_keys=True))


if __name__ == "__main__":
    main()
