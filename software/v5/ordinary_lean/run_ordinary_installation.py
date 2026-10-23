"""Selected file-only adapter: human-readable owner plan -> canonical assembler.

The external plan's exact bytes are pinned by the enclosing selection. This
adapter changes only JSON whitespace/key order, not source paths or pins. No
native calls/catalog operations occur. Partial destination remains on failure.
"""
from pathlib import Path
import json
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_installation as I
import ordinary_evidence as E
import local_catalog as C


def main():
    C.need(len(sys.argv) == 5, "INSTALLATION_ADAPTER_ARGUMENTS")
    output, plan_path, python_root, lean_root = map(Path, sys.argv[1:])
    C.ordinary(output, directory=True)
    raw = C.read_bounded(C.ordinary(plan_path), 2*1024**2)
    def pairs(rows):
        result = {}
        for key, value in rows:
            C.need(key not in result, "INSTALLATION_PLAN_DUPLICATE_KEY")
            result[key] = value
        return result
    def reject(_):
        raise ValueError("INSTALLATION_PLAN_NONINTEGER")
    plan = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=reject, parse_constant=reject)
    canonical = E.canonical_json(plan)
    result = I.assemble(output/"installation", canonical, I.P.sha(canonical),
        runtime_roots={"python_runtime": python_root, "lean_runtime": lean_root},
        deadline=time.monotonic()+90)
    # Retain provenance even though the installation manifest contains only
    # relocation-neutral pins and not these machine-specific source paths.
    I.P.PortableCatalog._write_fresh(output/"CANONICAL-PLAN.json", canonical)
    I.P.PortableCatalog._write_fresh(output/"ASSEMBLY-RESULT.json", E.canonical_json(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
