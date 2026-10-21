"""Pure three-crate support guest recipes from the successful RC guest03.

Reuse its module/Nanoda/dependency artifacts; compile no retained project.
"""
from pathlib import Path

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
PRIOR = HERE / "restricted-guest-build-03"
TYPED = HERE / "typed-guest-build-01"
TARGET = "riscv32im-risc0-zkvm-elf"


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def replace_once(argv, old, new):
    need(argv.count(str(old)) == 1, "EXACT_RECIPE_REPLACEMENT:" + str(old))
    argv[argv.index(str(old))] = str(new)


def commands(retained, run):
    run = Path(run)
    need(run == HERE / "restricted-support-guest-build-01", "EXACT_FRESH_SUPPORT_GUEST_RUN")
    need(retained["schema"] == "DMKN_V5_RC_GUEST_FOUR_CRATE_RECIPES_V1"
         and retained["basis"] == "RECONSTRUCTED_EQUIVALENT_PROFILE_NOT_CAPTURED_CARGO_ARGV",
         "ADOPTED_RECIPE_BASIS")
    prior = retained["recipes"]
    need([row["label"] for row in prior] == ["module", "rc-core", "aggregate", "guest"]
         and [row["name"] for row in prior] == ["dmkn_module_relation", "dmkn_rc_relation",
             "dmkn_aggregate_relation", "dmkn-aggregate-claim-guest"], "EXACT_RETAINED_RECIPE_ORDER")
    out = []
    for relative, base in zip(("restricted_support/lib.rs", "restricted_composition/aggregate_lib.rs",
                              "aggregate/main.rs"), prior[1:]):
        argv = list(base["argv"])
        label, name = base["label"], base["name"]
        is_bin, crate = label == "guest", name.replace("-", "_")
        need(argv[argv.index("--crate-name") + 1] == crate
             and argv[argv.index("--crate-type") + 1] == ("bin" if is_bin else "rlib")
             and argv[argv.index("--target") + 1] == TARGET
             and all(flag in argv for flag in ("opt-level=3", "overflow-checks=on", "panic=abort"))
             and "--test" not in argv, "RETAINED_EXACT_PROFILE")
        source = run / "project/software/v5" / relative
        replace_once(argv, base["source"], source)
        output = run / "outputs" / (name if is_bin else "lib" + name + ".rlib")
        metadata = None if is_bin else run / "outputs" / ("lib" + name + ".rmeta")
        emit = "dep-info=" + str(run / "outputs" / (crate + ".d")) + ",link=" + str(output)
        if metadata is not None:
            emit += ",metadata=" + str(metadata)
        emits = [arg for arg in argv if arg.startswith("--emit=")]
        need(len(emits) == 1, "ONE_EMIT_OPTION")
        replace_once(argv, emits[0], "--emit=" + emit)
        identity = "dmkn_v5_rc_support_guest01_" + crate
        replace_once(argv, "metadata=" + base["fresh_metadata"], "metadata=" + identity)
        replace_once(argv, "dependency=" + str(PRIOR / "outputs"), "dependency=" + str(run / "outputs"))
        replace_once(argv, "dmkn_module_relation=" + str(PRIOR / "outputs/libdmkn_module_relation.rlib"),
                     "dmkn_module_relation=" + str(run / "retained/modules/libdmkn_module_relation.rlib"))
        if label == "aggregate":
            replace_once(argv, "dmkn_rc_relation=" + str(PRIOR / "outputs/libdmkn_rc_relation.rlib"),
                         "dmkn_rc_relation=" + str(run / "outputs/libdmkn_rc_relation.rlib"))
        if is_bin:
            replace_once(argv, "dmkn_aggregate_relation=" + str(PRIOR / "outputs/libdmkn_aggregate_relation.rlib"),
                         "dmkn_aggregate_relation=" + str(run / "outputs/libdmkn_aggregate_relation.rlib"))
        replace_once(argv, "link-arg=-Map=" + str(PRIOR / "guest-link.map"),
                     "link-arg=-Map=" + str(run / "guest-link.map"))
        argv += ["-L", "dependency=" + str(run / "retained/modules")]
        search = [argv[index + 1] for index, arg in enumerate(argv) if arg == "-L"]
        need(search == ["dependency=" + str(path) for path in (
            run / "outputs", TYPED / "retained/libraries", TYPED / "retained/macros",
            PRIOR / "retained/projects", run / "retained/modules")], "EXACT_FIVE_ISOLATED_SEARCH_PATHS")
        need(not any(str(PRIOR / "outputs") in arg or str(PRIOR / "project") in arg
                     or "dmkn_rc_baseline" in arg for arg in argv), "NO_OLD_RC_OR_AGGREGATE_LINK_INPUT")
        externs = [argv[index + 1] for index, arg in enumerate(argv) if arg == "--extern"]
        need(len(externs) == (10 if label == "rc-core" else 11), "EXACT_DIRECT_EXTERN_COUNT")
        project = {arg.split("=", 1)[0]: arg.split("=", 1)[1] for arg in externs if arg.startswith("dmkn_")}
        expected = {"dmkn_module_relation": str(run / "retained/modules/libdmkn_module_relation.rlib")}
        if label == "aggregate":
            expected["dmkn_rc_relation"] = str(run / "outputs/libdmkn_rc_relation.rlib")
        if is_bin:
            expected["dmkn_aggregate_relation"] = str(run / "outputs/libdmkn_aggregate_relation.rlib")
        need(project == expected, "EXACT_PROJECT_EXTERN_BINDING")
        out.append({"label": label, "name": name, "argv": argv, "source": str(source),
                    "output": str(output), "metadata_output": None if metadata is None else str(metadata),
                    "fresh_metadata": identity, "kind": "bin" if is_bin else "rlib"})
    return out
