"""Run one retained-fixture native check inside the selected outer Windows Job.

The outer owner pins the executable, fixture, build records and this snapshot
before/after use and retains native stdout. No fixture generation, proof or
admission occurs here. The outcome audit checks the exact named control list.
"""
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
CHECKS = ROOT / "experiments/v5-local-checks"
BINARY = CHECKS / "restricted-support-build-01/restricted_support_controls.exe"
FIXTURE = CHECKS / "restricted-composition-controls-01/evidence/fixture.json"


def main():
    source = Path(__file__).resolve(strict=True)
    if not (os.name == "nt" and Path.cwd() == ROOT and len(sys.argv) == 1
            and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
            and not sys.flags.optimize
            and source == CHECKS / "restricted-support-controls-01/sources/software/v5/restricted_support/run_controls.py"):
        raise ValueError("EXACT_ISOLATED_SELECTED_CONTROL_SNAPSHOT")
    env = {key: os.environ[key] for key in ("SystemRoot", "WINDIR", "ComSpec") if key in os.environ}
    if "SystemRoot" not in env:
        raise ValueError("WINDOWS_SYSTEM_ROOT_REQUIRED")
    env.update(PATH=str(Path(env["SystemRoot"]) / "System32"), RUST_BACKTRACE="0")
    # Inherited stdout/stderr are bounded and retained by Run-V5-Check. Its
    # enclosing Job owns this process and the child, including any failure.
    result = subprocess.run([str(BINARY), str(FIXTURE)], cwd=ROOT, env=env,
                            timeout=30, check=False)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
