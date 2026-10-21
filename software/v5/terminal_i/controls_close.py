"""Run only the corrected close-refusal control from the frozen Terminal-I suite.

All product sources, staging, inert factories, forbidden-call traps and cleanup
remain in the exact original harness. The other nine test methods are not run.
No cryptographic or mathematical acceptance is established by this control.
"""
import hashlib
import importlib.util
from pathlib import Path
import sys

ORIGINAL = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network\software\v5\terminal_i\controls.py")
ORIGINAL_SHA = "42749d5968bd4dea19ac0cc59fd6bd86e0dead7fe4fd9f6e23b65bf2ab6ee372"
METHOD = "test_live_I_dispatch_cache_export_and_close"


def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--output":
        raise ValueError("OUTPUT_REQUIRED")
    output = Path(sys.argv[2])
    if not output.is_absolute() or not output.is_dir() or output.is_symlink():
        raise ValueError("EXISTING_ORDINARY_OUTPUT_REQUIRED")
    raw = ORIGINAL.read_bytes()
    if hashlib.sha256(raw).hexdigest() != ORIGINAL_SHA:
        raise ValueError("FROZEN_TERMINAL_I_HARNESS_CHANGED")
    snapshot = output/"original-controls.py"
    with snapshot.open("xb") as stream:
        if stream.write(raw) != len(raw):
            raise ValueError("ORIGINAL_HARNESS_SHORT_WRITE")
    if snapshot.read_bytes() != raw:
        raise ValueError("ORIGINAL_HARNESS_COPY_CHANGED")
    spec = importlib.util.spec_from_file_location("terminal_i_close_original", snapshot)
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)

    class CloseControl(original.Controls):
        async def test_live_I_dispatch_cache_export_and_close(self):
            # Exact predecessor method, except its post-close refusal regex.
            workspace, client, owners = self.operation("live")
            spec, exact, raw = self.packet()
            args = self.stored(workspace, raw)
            token = client.admit_local(*args, **original.ADMISSION)
            self.assertEqual(client.describe(token)["kind"], "I")
            self.assertEqual(client.describe(token)["live"]["journal"], exact)
            self.assertEqual(client.export_evidence(token), raw)
            self.assertIs(client.admit_local(*args, **original.ADMISSION), token)
            self.assertEqual(owners.receives, {"I": 1, "A": 0, "mixed": 0})
            self.assertEqual(client._budget.used["verify_attempts"], 1)
            self.assertEqual(client._budget.used["verification_input_bytes"], len(original.T.RECEIPT))
            self.assertEqual(client._budget.used["worker_cpu_seconds"], 1)
            self.assertEqual(client._counts["same_live_hits"], 1)
            await client.close()
            self.assertFalse(client._warrants)
            self.assertEqual(workspace.packets.get(original.sha(raw), len(raw)), raw)
            with self.assertRaisesRegex(ValueError, "^CLIENT_GRANT_CHANGED_OR_EXPIRED$"):
                client.describe(token)
            self.note(inert_I_calls=1, inert_A_calls=0, inert_mixed_calls=0, one_shared_reservation=True,
                      byte_exact_reexport=True, close_revokes_live_not_data=True)

    # Original main constructs its suite explicitly from these names; inherited
    # methods are never discovered or executed. setUp retains original factories.
    original.Controls = CloseControl
    original.SELECTED = (METHOD,)
    return original.main()


if __name__ == "__main__":
    raise SystemExit(main())
