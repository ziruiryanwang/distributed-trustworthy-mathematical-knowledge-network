"""Select complete installed support from retained bytes; never build or run."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys
from types import ModuleType

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT/"software/v5/distribution_complete"
CHECKS = ROOT/"experiments/v5-local-checks"
OLD_SHA = "fcfbbc751148a1f8d730eb88ff0050473d738d4eaf1c2dbb1ef5faa033cb2f6c"
GRAPH_SHA = "ecbece96120350a2c14df2b519c6500b82c607a4c17d31c0157ac370dde4bbcd"
ENVIRONMENT_SHA = "ee364e4788ce0560c87f621eeb3c4c3dfec62e8db4e15e099fd80e6adc533b86"
MODULE_NAME = re.compile(r"Init(?:\.[A-Za-z_][A-Za-z_0-9']*)*")
OVERRIDES = {"v5/admission/verifier.py", "v5/mixed_claims/receiver.py",
             "v5/mixed_claims/imports_atomic.py", "v5/admission/pin_phase.py"}
NEW_SOURCE = "v5/admission/pin_phase.py"
MIB = 1024**2


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


class Header:
    """Restricted retained-source header lexer, not a general Lean parser."""
    def __init__(self, text):
        self.text, self.pos = text, 0

    def token(self):
        text = self.text
        while self.pos < len(text):
            if text[self.pos].isspace():
                self.pos += 1
            elif text.startswith("--", self.pos):
                end = text.find("\n", self.pos+2)
                self.pos = len(text) if end < 0 else end+1
            elif text.startswith("/-", self.pos):
                depth = 1
                self.pos += 2
                while depth:
                    need(self.pos < len(text), "SELECT_UNCLOSED_HEADER_COMMENT")
                    if text.startswith("/-", self.pos):
                        depth += 1
                        self.pos += 2
                    elif text.startswith("-/", self.pos):
                        depth -= 1
                        self.pos += 2
                    else:
                        self.pos += 1
            else:
                break
        if self.pos == len(text):
            return ""
        match = re.match(r"[A-Za-z_][A-Za-z_0-9'.]*", text[self.pos:])
        if match:
            self.pos += len(match[0])
            return match[0]
        value = text[self.pos]
        self.pos += 1
        return value


def parse_header(text):
    lexer = Header(text)
    # The fixed retained namespace uses both markers. Refuse other source
    # conventions instead of inventing implicit imports or module semantics.
    need(lexer.token() == "module", "SELECT_EXPLICIT_MODULE_REQUIRED")
    need(lexer.token() == "prelude", "SELECT_EXPLICIT_PRELUDE_REQUIRED")
    token, imports = lexer.token(), []
    while True:
        public = token == "public"
        if public:
            token = lexer.token()
        meta = token == "meta"
        if meta:
            token = lexer.token()
        if token != "import":
            # This is the first ordinary command, e.g. `public section`.
            # No file body, string, quotation or source strategy is evaluated.
            break
        token = lexer.token()
        all_import = token == "all"
        if all_import:
            token = lexer.token()
        need(MODULE_NAME.fullmatch(token) is not None, "SELECT_INIT_IMPORT_NAME")
        need(not (public and all_import), "SELECT_PUBLIC_IMPORT_ALL")
        imports.append({"module": token, "public": public, "meta": meta, "all": all_import})
        need(len(imports) <= 256, "SELECT_HEADER_IMPORT_BOUND")
        token = lexer.token()
    return imports


def graph_fingerprint(source_rows, import_rows):
    text = "".join(
        name+"\t"+str(source_rows[name]["bytes"])+"\t"+source_rows[name]["sha256"]+"\t"
        +",".join(item["module"]+":"+str(int(item["public"]))+str(int(item["meta"]))
                  +str(int(item["all"])) for item in import_rows[name])+"\n"
        for name in sorted(source_rows))
    return hashlib.sha256(text.encode("utf-8")).hexdigest(), len(text.encode("utf-8"))


def load_helper(expected):
    need(re.fullmatch("[0-9a-f]{64}", expected) is not None, "SELECT_REVIEWED_HELPER_SHA")
    path = HERE/"distribution.py"
    need(path.is_file() and all(not item.is_symlink() and not item.is_junction()
         for item in (path, *path.parents)), "SELECT_ORDINARY_HELPER")
    with path.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(0 < len(raw) <= 2*MIB and hashlib.sha256(raw).hexdigest() == expected,
         "SELECT_REVIEWED_HELPER_CHANGED")
    module = ModuleType("_selected_complete_distribution")
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
    return module, {"path": str(path), "bytes": len(raw), "sha256": expected}


def support_from_retained(D, lean_root):
    source_root = lean_root/"src/lean"
    D.ordinary(source_root, directory=True)
    D.ordinary(source_root/"Init", directory=True)
    paths = [source_root/"Init.lean", *(source_root/"Init").rglob("*.lean")]
    need(1 <= len(paths) <= 4096, "SELECT_SOURCE_INVENTORY_BOUND")
    sources, imports, modules = {}, {}, {}
    for path in sorted(paths):
        relative = path.relative_to(source_root).as_posix()
        name = relative[:-5].replace("/", ".")
        need(MODULE_NAME.fullmatch(name) is not None and name not in sources,
             "SELECT_SOURCE_MODULE_NAME")
        raw = D.read(path, 4*MIB)
        sources[name] = {"path": str(path), "bytes": len(raw),
                         "sha256": hashlib.sha256(raw).hexdigest()}
        imports[name] = parse_header(raw.decode("utf-8"))
        # Public/meta repetitions are important provenance but not additional
        # graph edges. Do not discard flags from the source fingerprint.
        modules[name] = sorted({item["module"] for item in imports[name]})
    fingerprint, fingerprint_bytes = graph_fingerprint(sources, imports)
    need(fingerprint == GRAPH_SHA, "SELECT_RETAINED_SOURCE_GRAPH_CHANGED")
    files = {}
    for name in sorted(modules):
        for suffix in D.LEAN_SUFFIXES:
            relative = "lib/lean/"+name.replace(".", "/")+suffix
            files[relative] = D.pin(lean_root.joinpath(*relative.split("/")))
    support = {"profile": D.LEAN_SUPPORT, "modules": modules, "files": files}
    D.support_layout(support)  # All source nodes reachable, no missing edge/part.
    environment = D.pin(source_root/"Lean/Environment.lean")
    need(environment["sha256"] == ENVIRONMENT_SHA, "SELECT_RETAINED_LOADER_CHANGED")
    return support, {
        "schema": "DMKN_V5_LEAN_SOURCE_CLOSURE_SELECTION_V1",
        "source_root": str(source_root), "sources": sources, "header_imports": imports,
        "source_graph_sha256": fingerprint, "source_graph_utf8_bytes": fingerprint_bytes,
        "loader_source": environment,
        "parser_source": D.pin(source_root/"Lean/Parser/Module.lean"),
        "parser_syntax_source": D.pin(source_root/"Lean/Parser/Module/Syntax.lean"),
        "assumptions": [
            "RETAINED_SOURCE_AND_TOOLCHAIN_ARTIFACT_CORRESPONDENCE_IS_TRUSTED",
            "EXPLICIT_MODULE_PRELUDE;ASCII_INIT_IDENTIFIERS;NESTED_AND_LINE_COMMENTS",
            "MULTILINE_WHITESPACE;ALL_PUBLIC_META_PRIVATE_EDGES_INCLUDED",
            "SOURCE_HEADER_GRAPH_NOT_INDEPENDENT_BINARY_OLEAN_METADATA_PROOF",
            "OWNER_CONTROLLED_STABLE_LOCAL_DIRECTORIES",
        ],
    }


def replace_sdk(D, sdk, override_path, override_sha):
    selected = D.checked_json(override_path, override_sha, MIB)
    need(type(selected) is dict and set(selected) == OVERRIDES, "SELECT_EXACT_SDK_OVERRIDES")
    need(NEW_SOURCE not in sdk and OVERRIDES-{NEW_SOURCE} <= set(sdk),
         "SELECT_EXISTING_SDK_OVERRIDE_KEYS")
    result = deepcopy(sdk)
    for name, row in selected.items():
        expected = D.absolute_pin(row)
        path = Path(row["path"])
        need(path == ROOT/"software/v5/runtime_efficient"/name.removeprefix("v5/")
             and expected["bytes"] <= 2*MIB, "SELECT_REVIEWED_SDK_OVERRIDE_ORIGIN")
        D.pinned(path, expected)
        result[name] = deepcopy(row)
    need(len(result) == len(sdk)+1
         and all(result[name] == row for name, row in sdk.items() if name not in OVERRIDES),
         "SELECT_UNCHANGED_SDK_ROWS")
    return result, D.pin(Path(override_path))


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode, "SELECT_CANONICAL_ISOLATED")
    need(len(sys.argv) in (2, 5) and (len(sys.argv) == 2 or sys.argv[2] == "--sdk-overrides"),
         "SELECT_HELPER_SHA_OPTIONAL_EXACT_OVERRIDE_PATH_SHA")
    D, helper = load_helper(sys.argv[1])
    with D.path_scope():
        input_path = CHECKS/"distribution-03-input.json"
        closure_path = CHECKS/"distribution-03-source-closure.json"
        D.ordinary(input_path, fresh=True)
        D.ordinary(closure_path, fresh=True)
        old_path = CHECKS/"distribution-02-input.json"
        old = D.checked_json(old_path, OLD_SHA, 8*MIB)
        D.fields(old, {"schema", "base_root", "base_manifest", "sdk_sources",
            "preparation_template", "assets", "aggregate_image", "lean_runtime",
            "distribution_source"})
        need(old["schema"] == "DMKN_V5_DISTRIBUTION_INPUT_V1"
             and len(old["sdk_sources"]) == 102, "SELECT_FROZEN_DISTRIBUTION_BASIS")
        value = deepcopy(old)
        for row in value["sdk_sources"].values():
            D.pinned(row["path"], D.absolute_pin(row))
        overrides = None
        if len(sys.argv) == 5:
            value["sdk_sources"], overrides = replace_sdk(
                D, value["sdk_sources"], sys.argv[3], sys.argv[4])
        template_pin = value["preparation_template"]
        D.pinned(template_pin["path"], D.absolute_pin(template_pin))
        template = D.checked_json(template_pin["path"], template_pin["sha256"], MIB)
        lean_root = D.ordinary(template["lean_root"], directory=True)
        need({Path(row["path"]).relative_to(lean_root).as_posix(): row
              for row in template["lean_runtime_pins"]} == value["lean_runtime"],
             "SELECT_UNCHANGED_MINIMUM_RUNTIME_PINS")
        support, provenance = support_from_retained(D, lean_root)
        for name in set(support["files"]) & set(value["lean_runtime"]):
            need(support["files"][name] == value["lean_runtime"][name],
                 "SELECT_IDENTICAL_RUNTIME_SUPPORT_OVERLAP")
        base_pin = value["base_manifest"]
        base = D.checked_json(base_pin["path"], base_pin["sha256"], 8*MIB)
        need(base_pin["sha256"] == D.BASE_SHA, "SELECT_UNCHANGED_BASE_MANIFEST")
        projection = D.base_projection(base["files"])
        value.update(schema=D.INPUT_SCHEMA, base_role=D.BASE_ROLE,
                     lean_support=support, distribution_source=helper)
        raw = json.dumps(value, sort_keys=True, indent=2).encode("utf-8")+b"\n"
        need(len(raw) <= 8*MIB, "SELECT_DISTRIBUTION_INPUT_BOUND")
        input_pin = {"path": str(input_path), "bytes": len(raw),
                     "sha256": hashlib.sha256(raw).hexdigest()}
        provenance.update(selected_input=input_pin, distribution_source=helper,
            predecessor_input={"path": str(old_path), "sha256": OLD_SHA},
            sdk_override_selection=overrides, artifact_files=len(support["files"]),
            artifact_bytes=sum(row["bytes"] for row in support["files"].values()),
            base_role=D.BASE_ROLE, selected_base_payload_files=len(projection),
            selected_base_payload_bytes=sum(row["bytes"] for row in projection.values()),
            selector=D.pin(Path(__file__)))
        provenance_raw = json.dumps(provenance, sort_keys=True, indent=2).encode("utf-8")+b"\n"
        need(len(provenance_raw) <= 8*MIB, "SELECT_PROVENANCE_BOUND")
        D.write_new(input_path, raw)
        D.write_new(closure_path, provenance_raw)
        need(D.read(input_path, 8*MIB) == raw and D.read(closure_path, 8*MIB) == provenance_raw,
             "SELECT_OUTPUT_READBACK")
        print(json.dumps({"input": input_pin, "source_closure": D.pin(closure_path),
            "sdk_sources": len(value["sdk_sources"]), "modules": len(support["modules"]),
            "support_files": len(support["files"]), "selected_base_files": len(projection),
            "pure_builder_helper_imported": True, "sdk_imports": 0,
            "copied": False, "built": False, "runtime_invoked": False, "proof_calls": 0}))


if __name__ == "__main__":
    main()
