# One new module image, no guest execution

`assemble_guest.py` is source-only until a new guest build actually passes and
root selects the resulting exact RESULT/ELF plus this adapter. It runs under
the existing bounded `Run-V5-Check.py` owner Job, not as an unsupervised process.
Suggested outer ceiling:120CPU/120wall seconds,1024MiB private Job memory and
two active processes, with1MiB outer stdout/stderr caps. The sole assembler
child also has a60-second timeout; no proof or execution command is exposed.

Root selection snapshots the adapter/this plan and pins the retained assembler
RESULT/executable, exact kernel, actual new guest RESULT/ELF, Python/runtime and
supervisor. The command uses isolated Python with:

```text
assemble_guest.py --guest-result ABSOLUTE_NEW_GUEST_RESULT
                 --guest-result-sha256 EXACT_RESULT_SHA
                 --output FRESH_ASSEMBLY_SUBDIRECTORY
```

It requires the new module build's actual pass and zero-active Job, never a
candidate ELF lying beside a failed build. The exact target must be that fresh
run's `release/dmkn-module-guest`. It does not accept an old collection guest.

The assembler is the previously qualified driver-build04 executable, pinned by
its actual result. The v1compat kernel is the exact58736-byte retained artifact
already used successfully with the same adopted SDK. Only `assemble USER_ELF
KERNEL_ELF FRESH_IMAGE` runs. No new assembler/compiler/backend is built.

All inputs are rebound before/after. The output must have the exact successful
COMBINED_IMAGE record, no diagnostics and matching byte count; actual image
bytes receive their own file hash. `image_id` is the pinned assembler's actual
cryptographic image measurement, deliberately distinguished from file SHA256.
The future module host recomputes it from the actual image before execution.

Pass is only `PASS_NEW_MODULE_IMAGE_ASSEMBLY_ONLY`. Root adoption of this actual
image/source profile remains explicit, and separate host execution/cycle screens,
genuine proof generation, recursive receiving and public integration remain open.
No exact selection can be completed before the actual successful guest artifact
exists; do not invent hashes, a success result or a v5 image ID.
