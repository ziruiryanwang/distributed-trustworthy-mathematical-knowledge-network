"""Pure dependency selection and equivalent-profile direct project recipes.

No subprocess/filesystem access. These are reconstructed recipes, not captured
Cargo argv or a claim that a new 297-unit Cargo build ran.
"""
from pathlib import Path
import re

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OLD = ROOT / "experiments/v5-local-checks/aggregate-guest-compile-01"
SOURCE_RUN = ROOT / "experiments/v5-local-checks/bounded-parse-guest-build-02"
RUST = ROOT / "experiments/scale-crypto-01/runs/run-01/rust"
TARGET = "riscv32im-risc0-zkvm-elf"
LIBDIR = OLD / ("target/" + TARGET + "/release/deps")
HOSTDIR = OLD / "target/release/deps"
FRESH_CRATES = {"dmkn_module_relation", "dmkn_aggregate_relation"}
STDLIB = {"alloc", "compiler_builtins", "core", "panic_abort", "panic_unwind", "proc_macro", "std"}


def need(value, reason):
    if not value:
        raise ValueError(reason)


def dependencies(rows):
    """Exact 108 target library pairs and 22 host macro DLLs, with no old pair."""
    need(type(rows) is list and len(rows) <= 4096, "FINITE_CARGO_ARTIFACT_ROWS")
    files, libraries, macros, scripts, completed = {}, {}, {}, [], []
    for row in rows:
        if row.get("reason") == "build-finished":
            completed.append(row.get("success"))
        if row.get("reason") == "build-script-executed":
            need(row["linked_libs"] == [] and row["linked_paths"] == [], "NO_EXTRA_NATIVE_LINK_INPUTS")
            scripts.append(row)
        if row.get("reason") != "compiler-artifact":
            continue
        target, paths = row["target"], [Path(name) for name in row["filenames"]]
        if target["kind"] in (["lib"], ["rlib"]) and paths and all(path.parent == LIBDIR for path in paths):
            name = target["name"]
            if name in FRESH_CRATES:
                continue
            identity = (row["package_id"], name)
            need(identity not in libraries and len(paths) == 2
                 and {path.suffix for path in paths} == {".rlib", ".rmeta"}
                 and len({path.stem for path in paths}) == 1, "ONE_MATCHED_TARGET_LIBRARY_PAIR")
            libraries[identity] = {"package_id": row["package_id"], "features": row["features"],
                               "rlib": str(next(path for path in paths if path.suffix == ".rlib"))}
            for path in paths:
                need(str(path) not in files, "DUPLICATE_RETAINED_ARTIFACT")
                files[str(path)] = "libraries/" + path.name
        if target["kind"] == ["proc-macro"]:
            dlls = [path for path in paths if path.suffix == ".dll"]
            need(len(dlls) == 1 and dlls[0].parent == HOSTDIR, "ONE_HOST_MACRO_DLL")
            path = dlls[0]
            need(str(path) not in files and target["name"] not in macros, "DUPLICATE_MACRO")
            files[str(path)] = "macros/" + path.name
            macros[target["name"]] = str(path)
    need(len(libraries) == 108 and len(macros) == 22 and len(files) == 238
         and len(scripts) == 41 and completed == [True], "EXACT_COMPLETE_RETAINED_ARTIFACT_CLOSURE")
    names = {name for _, name in libraries}
    need("serde_derive" in macros and STDLIB <= names and "nanoda_lib" in names,
         "EXPECTED_DIRECT_DEPENDENCIES")
    return files, libraries


def commands(graph, run, library_files, libraries, guest_flags):
    """Return three sequential argv lists with distinct, paired new crate IDs."""
    run = Path(run)
    need(run.parent == SOURCE_RUN.parent and run.name == "bounded-parse-direct-build-01",
         "ONE_FRESH_DIRECT_RUN")
    need(set(graph) == {"version", "roots", "units"} and graph["version"] == 1
         and len(graph["units"]) == 297, "RETAINED_EXACT_GRAPH")
    need(guest_flags == ["-C", "passes=lower-atomic", "-C", "link-arg=-Ttext=0x00200800",
         "-C", "link-arg=--fatal-warnings", "-C", "panic=abort", "--cfg",
         'getrandom_backend="custom"', "-C", "link-arg=-Map=" + str(OLD / "guest-link.map")],
         "EXACT_RETAINED_GUEST_FLAGS")
    flags = list(guest_flags)
    flags[-1] = "link-arg=-Map=" + str(run / "guest-link.map")
    sources = {
        "dmkn_module_relation": SOURCE_RUN / "project/software/v5/bounded_parse/module_lib.rs",
        "dmkn_aggregate_relation": SOURCE_RUN / "project/software/v5/bounded_parse/aggregate_lib.rs",
        "dmkn-aggregate-claim-guest": SOURCE_RUN / "project/software/v5/aggregate/main.rs",
    }
    compiled, recipes = {}, []
    for name in sources:
        matches = [unit for unit in graph["units"] if unit["target"]["name"] == name
                   and unit["pkg_id"].startswith("path+file:///") and "bounded_parse_guest" in unit["pkg_id"]]
        need(len(matches) == 1, "ONE_PROJECT_UNIT:" + name)
        unit = matches[0]
        is_bin = name == "dmkn-aggregate-claim-guest"
        profile = unit["profile"]
        need(unit["features"] == [] and unit["platform"] == TARGET and unit["mode"] == "build"
             and unit["target"]["edition"] == "2021"
             and unit["target"]["kind"] == (["bin"] if is_bin else ["lib"])
             and profile["opt_level"] == "3" and profile["lto"] == "true"
             and profile["panic"] == "abort" and profile["overflow_checks"] is True
             and profile["debug_assertions"] is False and profile["incremental"] is False,
             "UNCHANGED_PROJECT_PROFILE:" + name)
        # Normalize only the reviewed lexical .. source path; no filesystem resolution.
        source_path = str(unit["target"]["src_path"]).replace("\\", "/")
        expected_suffix = {"dmkn_module_relation": "/module/../../bounded_parse/module_lib.rs",
            "dmkn_aggregate_relation": "/../bounded_parse/aggregate_lib.rs",
            "dmkn-aggregate-claim-guest": "/../aggregate/main.rs"}[name]
        need(source_path.endswith("/bounded_parse_guest" + expected_suffix), "EXACT_PROJECT_SOURCE")
        crate = name.replace("-", "_")
        output = run / "outputs" / (name if is_bin else "lib" + name + ".rlib")
        metadata = run / "outputs" / ("lib" + name + ".rmeta")
        emits = "dep-info=" + str(run / "outputs" / (crate + ".d")) + ",link=" + str(output)
        if not is_bin:
            emits += ",metadata=" + str(metadata)
        argv = [str(RUST / "bin/rustc.exe"), "--crate-name", crate, "--edition=2021",
            str(sources[name]), "--crate-type", "bin" if is_bin else "rlib",
            "--emit=" + emits, "-C", "opt-level=3", "-C", "panic=abort",
            "-C", "overflow-checks=on", "-C", "debug-assertions=no", "-C", "strip=debuginfo",
            "-C", "metadata=dmkn_v5_bounded_direct01_" + crate,
            "--target", TARGET, "-C",
            "linker=" + str(RUST / "lib/rustlib/x86_64-pc-windows-msvc/bin/rust-lld.exe"),
            "-L", "dependency=" + str(run / "outputs"),
            "-L", "dependency=" + str(run / "retained/libraries"),
            "-L", "dependency=" + str(run / "retained/macros"), "-Z", "unstable-options",
            "--check-cfg", "cfg(docsrs,test)", "--check-cfg", "cfg(feature, values())"]
        argv += ["-C", "lto=fat", "-C", "embed-bitcode=yes"] if is_bin else ["-C", "linker-plugin-lto"]
        needed = set()
        for edge in unit["dependencies"]:
            dep = graph["units"][edge["index"]]
            extern = edge["extern_crate_name"]
            need(extern not in needed, "DUPLICATE_EXTERN")
            needed.add(extern)
            if extern in FRESH_CRATES:
                need(extern in compiled and not edge["noprelude"], "NEW_PROJECT_DEPENDENCY_ORDER")
                path = compiled[extern]
            else:
                identity = (dep["pkg_id"], dep["target"]["name"])
                if extern == "nanoda_lib":
                    # Frozen graph comparison permits only checker-wrapper
                    # relocation; the controller separately binds all16
                    # checker source files to the retained compile source map.
                    need(dep["pkg_id"] == "path+" + (SOURCE_RUN /
                         "project/software/v5/bounded_parse_guest/checker").as_uri()
                         + "#nanoda_lib@0.4.19", "EXACT_RELOCATED_CHECKER_PACKAGE")
                    old_checker = ROOT / "experiments/v5-local-checks/aggregate-guest-build-01/project/software/v5/aggregate_guest/checker"
                    identity = ("path+" + old_checker.as_uri() + "#nanoda_lib@0.4.19", "nanoda_lib")
                need(identity in libraries and dep["features"] == libraries[identity]["features"]
                     and dep["platform"] == TARGET, "EXACT_RETAINED_LIBRARY_FEATURES:" + extern)
                path = run / "retained" / library_files[libraries[identity]["rlib"]]
            need(edge["noprelude"] == (extern in STDLIB), "EXACT_BUILD_STD_EXTERN")
            argv += ["--extern", ("noprelude:" if edge["noprelude"] else "") + extern + "=" + str(path)]
        need(len(needed) == (10 if name == "dmkn_aggregate_relation" else 11), "EXACT_DIRECT_EXTERN_COUNT")
        argv += flags
        recipes.append({"name": name, "argv": argv, "source": str(sources[name]),
                        "output": str(output), "fresh_metadata": "dmkn_v5_bounded_direct01_" + crate,
                        "metadata_output": None if is_bin else str(metadata),
                        "kind": "bin" if is_bin else "rlib"})
        if not is_bin:
            compiled[name] = output
    return recipes
