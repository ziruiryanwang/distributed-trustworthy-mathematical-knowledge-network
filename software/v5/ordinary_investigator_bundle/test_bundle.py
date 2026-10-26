"""One file-only investigator handoff gate under a separately selected outer Job.

Pack once, verify a fresh relocation, check changed manifest selection and current
guide links, then prepare inert inputs using the exact current interface. No
native build, mathematical operation, state opening, service or network call.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys
import types
from urllib.parse import unquote, urlsplit

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_investigator_bundle/"
HELPER = "software/v5/ordinary_workflow_bundle/test_bundle02.py"
HELPER_SHA = "17cd0c44568ac347c4013b1e1564afb7bd92441ced4de5dae08fda3af6dcb66a"


def load(path, digest, label):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError("TEST_SOURCE_PIN:" + str(path))
    module = types.ModuleType(label)
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for option in ("source-root", "workflow-root", "bundle-sha256", "package",
                   "profile-sha256", "selector-test", "selector-test-sha256", "output"):
        parser.add_argument("--" + option, required=True)
    args = parser.parse_args()
    if not (Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
            and sys.dont_write_bytecode and not sys.flags.optimize):
        raise ValueError("ISOLATED_CANONICAL_TEST")
    root, prior_root, output = map(Path, (args.source_root, args.workflow_root, args.output))
    T = load(ROOT / HELPER, HELPER_SHA, "_investigator_test_files")
    B = T.load_source(root / PREFIX / "bundle.py", args.bundle_sha256,
                      "_investigator_bundle_subject")
    _, base = B.helpers()
    output = base.ordinary(output, directory=True, fresh=True)
    base.ordinary(output.parent, directory=True)
    T.need(root == ROOT and output.is_relative_to(ROOT / "experiments/v5-local-checks")
           and not output.exists() and output.parent.is_dir(), "TEST_FRESH_SCOPE")
    output.mkdir()
    cases = []
    try:
        receipt = B.pack(root, prior_root, output / "packed", check=T.check)
        T.need(receipt["status"] == "PACKED_INVESTIGATOR_SOURCE_NOT_BUILT",
               "PACK_TERMINAL")
        packed = T.read(output / "packed/source.zip")
        T.need(T.pin(packed) == receipt["archive"], "ARCHIVE_RECEIPT")
        members = T.archive_members(packed, B.COUNT + 1)
        doc = json.loads(members[B.MANIFEST])
        prior_raw = T.read(prior_root / "WORKFLOW-SOURCE-MANIFEST.json", 2*T.MIB)
        original = json.loads(prior_raw)["files"]
        T.need(len(original) == 154 and T.digest(prior_raw) == B.PRIOR_SHA256
               and members[B.PRIOR_MANIFEST] == prior_raw, "PRIOR_ASSOCIATION")
        T.need(set(members) == set(original) | set(B.SOURCES) |
               {B.MANIFEST, B.PRIOR_MANIFEST}, "NEW_FULL_CENSUS")
        for name, pin in original.items():
            T.need(T.pin(members[name]) == pin and
                   members[name] == T.read(prior_root / name, 2*T.MIB), "OLD_PAYLOAD:" + name)
        for name, source in B.SOURCES.items():
            T.need(members[name] == T.read(root / source, 2*T.MIB), "NEW_PAYLOAD:" + name)
        T.need(T.pin(members[B.MANIFEST]) == receipt["manifest"], "MANIFEST_RECEIPT")
        cases.append("exact-154-plus-current-source-projection")

        relocated = output / "relocated"
        T.extract(members, relocated)
        verified = T.cli(output, "relocated-verify", relocated / B.UTILITY,
            ["verify", "--source-root", str(relocated), "--manifest-sha256",
             receipt["manifest"]["sha256"]])
        T.need(verified["status"] == "VERIFIED_EXACT_INVESTIGATOR_SOURCE_NOT_BUILT"
               and verified["manifest"] == receipt["manifest"]
               and verified["payload_files"] == B.COUNT, "RELOCATED_VERIFY")
        cases.append("relocated-public-verify")

        mutations = [
            ("missing-new-query", lambda d: d["files"].pop("software/v5/ordinary_anchor_query/query.py")),
            ("old-payload-changed", lambda d: d["files"]["START-HERE.md"].update(sha256="0"*64)),
            ("new-fixed-source-changed", lambda d: d["files"][PREFIX+"prepare_selected.py"].update(sha256="0"*64)),
            ("old-operator-selected", lambda d: d["entrypoints"].update(operator="software/v5/ordinary_bounded_transport/prepare_selected.py")),
            ("wrong-prior-identity", lambda d: d["prior_manifest"].update(sha256="0"*64)),
        ]
        refusals = []
        for label, alter in mutations:
            changed = deepcopy(doc)
            alter(changed)
            refusals.append(T.refuses(lambda: B.validate_manifest(base, changed, original,
                                                                  prior_raw), label))
        cases.append("five-changed-manifest-refusals")
        extra = dict(members, **{"unexpected.txt": b"unexpected"})
        extra_root = output / "extra-member"
        T.extract(extra, extra_root)
        refusals.append(T.refuses(lambda: B.verify(extra_root,
            receipt["manifest"]["sha256"], check=T.check), "extra-file-refused"))
        cases.append("actual-extra-member-refusal")

        guides = [name for name in B.SOURCES if name.endswith(".md")]
        links = []
        for guide in guides:
            for target in re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", members[guide].decode("utf-8")):
                parsed = urlsplit(target.strip())
                if parsed.scheme or parsed.netloc:
                    T.need(parsed.scheme in ("https", "http"), "GUIDE_URL_SCHEME")
                    continue
                if not parsed.path:
                    continue
                path = (relocated / guide).parent.joinpath(unquote(parsed.path)).resolve()
                T.need(path.is_relative_to(relocated) and path.is_file() and
                       path.relative_to(relocated).as_posix() in doc["files"],
                       "CURRENT_GUIDE_LINK:" + guide + ":" + target)
                links.append({"guide": guide, "target": target})
        T.need(len(guides) == 4 and links, "CURRENT_GUIDE_CENSUS")
        cases.append("four-current-guides-local-link-closure")

        S = load(Path(args.selector_test), args.selector_test_sha256,
                 "_investigator_selector_tests")
        selector = S.run(relocated, Path(args.package), args.profile_sha256,
                         output / "selector")
        T.need(selector["passed"] and len(selector["cases"]) == 9,
               "SELECTOR_CHANGED_BOUNDARY")
        cases.append("relocated-selector-nine-cases")
        final_census = T.census(relocated, members)
        T.need(len(cases) == 6, "SUITE_CENSUS")
        result = {"passed": True, "cases": cases, "refusals": refusals,
                  "receipt": receipt, "verified": verified, "guide_links": links,
                  "selector": selector, "final_census": final_census,
                  "native_operations": 0, "mathematical_acceptance": False}
        T.save(output / "RESULT.json", result)
        print(json.dumps(result, sort_keys=True))
    except BaseException as error:
        T.save(output / "FAILURE.json", {"error_type": type(error).__name__,
            "error": str(error)[:1000], "completed_cases": cases,
            "retention": "PRESERVED_NO_AUTOMATIC_RETRY"})
        raise


if __name__ == "__main__":
    main()
