"""Pure three-crate RC guest recipes; no filesystem, subprocess or new graph.

Reuse the adopted typed guest's exact profile/SDK argv. The RC core is an
explicit new unit, not a fabricated member of the old Cargo unit graph.
"""
from pathlib import Path

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
HERE = ROOT / "experiments/v5-local-checks"
TYPED = HERE / "typed-guest-build-01"
TARGET = "riscv32im-risc0-zkvm-elf"
MODULE = "libdmkn_module_relation-c98240db3a2d8c8d.rlib"


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def replace_once(argv, old, new):
    need(argv.count(str(old)) == 1, "EXACT_RECIPE_REPLACEMENT:" + str(old))
    argv[argv.index(str(old))] = str(new)


def commands(retained, run):
    run = Path(run)
    need(run.parent == HERE and run.name == "restricted-guest-build-02", "EXACT_FRESH_GUEST_RUN")
    need(retained["schema"] == "DMKN_V5_TYPED_GUEST_FOUR_CRATE_RECIPES_V1"
         and retained["basis"] == "RECONSTRUCTED_EQUIVALENT_PROFILE_NOT_CAPTURED_CARGO_ARGV",
         "ADOPTED_RECIPE_BASIS")
    prior = retained["recipes"]
    need([r["name"] for r in prior] == ["nanoda_lib", "dmkn_module_relation",
         "dmkn_aggregate_relation", "dmkn-aggregate-claim-guest"], "EXACT_RETAINED_RECIPE_ORDER")
    out = []
    for label, name, relative, base in (
            ("rc-core", "dmkn_rc_relation", "restricted_composition/lib02.rs", prior[2]),
            ("aggregate", "dmkn_aggregate_relation", "restricted_composition/aggregate_lib.rs", prior[2]),
            ("guest", "dmkn-aggregate-claim-guest", "aggregate/main.rs", prior[3])):
        argv = list(base["argv"])
        is_bin = label == "guest"
        crate = name.replace("-", "_")
        need(argv[argv.index("--crate-name") + 1] == base["name"].replace("-", "_")
             and argv[argv.index("--crate-type") + 1] == ("bin" if is_bin else "rlib")
             and argv[argv.index("--target") + 1] == TARGET
             and all(flag in argv for flag in ("opt-level=3", "overflow-checks=on", "panic=abort"))
             and "--test" not in argv, "RETAINED_EXACT_PROFILE")
        argv[argv.index("--crate-name") + 1] = crate
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
        identity = "dmkn_v5_rc_guest02_" + crate
        replace_once(argv, "metadata=" + base["fresh_metadata"], "metadata=" + identity)
        replace_once(argv, "dependency=" + str(TYPED / "outputs"), "dependency=" + str(run / "outputs"))
        replace_once(argv, "dmkn_module_relation=" + str(TYPED / "outputs/libdmkn_module_relation.rlib"),
                     "dmkn_module_relation=" + str(run / "retained/projects" / MODULE))
        if is_bin:
            replace_once(argv, "dmkn_aggregate_relation=" + str(TYPED / "outputs/libdmkn_aggregate_relation.rlib"),
                         "dmkn_aggregate_relation=" + str(run / "outputs/libdmkn_aggregate_relation.rlib"))
        if label == "aggregate":
            argv += ["--extern", "dmkn_rc_relation=" + str(run / "outputs/libdmkn_rc_relation.rlib")]
        replace_once(argv, "link-arg=-Map=" + str(TYPED / "guest-link.map"),
                     "link-arg=-Map=" + str(run / "guest-link.map"))
        argv += ["-L", "dependency=" + str(run / "retained/projects")]
        need(not any(str(TYPED / "outputs") in arg or str(TYPED / "project") in arg for arg in argv),
             "NO_OLD_PROJECT_COMPILATION_OR_LINK_INPUT")
        need(sum(arg == "--extern" for arg in argv) == (10 if label == "rc-core" else 11),
             "EXACT_DIRECT_EXTERN_COUNT")
        out.append({"label": label, "name": name, "argv": argv, "source": str(source),
                    "output": str(output), "metadata_output": None if metadata is None else str(metadata),
                    "fresh_metadata": identity, "kind": "bin" if is_bin else "rlib"})
    return out
