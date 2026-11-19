# Installed V snapshot01: bootstrap-size failure

2026-10-22; independent saved-evidence/source audit by `storage_outcome_audit`.
Canonical root only. No import, constructor, test, host call, repair, retry or
Git mutation was performed by this review.

**FAIL, preserved.** The selected public producer child refused its real
supervisor manifest at bootstrap: the entry helper hardcodes a1MiB document
limit, but that pinned manifest is1070384 bytes. No producer owner, snapshot
host, capsule or certificate was created. Process closure is clean. The failure
is not a malformed V packet, failed mathematical verification or exhausted proof
budget. It does not erase the separately adopted actual U-to-V admission.

## Exact cause and smallest repair

Used entry:
`product-local/v5-distribution-installed-producer-01/Mathematical Commons v5/sdk/v5/release_production/operator.py`,
26808 bytes, SHA-256
`f404f0ba4d5177654fd02e999b00c0d8d104f1a4b85295414dff2720ddf6021a`.
The copied `snapshot-01/entry.py` has identical bytes.

`_pin_document` at line81 imposes `size <= MIB` and reads `MIB+1`. Its first
bootstrap use reads the28402-byte selected profile successfully. The next call,
at line162, reads `support["supervisor_manifest"]` without a larger bound. The
actual `base/RELEASE-MANIFEST.json` is:

-1070384 bytes, which exceeds1048576 by21808 bytes;
- SHA-256 `a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`;
- exactly the supervisor pin in the selected profile and fixed installed base.

Therefore the saved `ValueError: LIFECYCLE_ENTRY_DOCUMENT_BOUND` follows
deterministically before parsing that document, before the584-file Python
binding/import gate and before any product owner construction. The size mismatch
can be diagnosed from source and bytes without a retry.

Smallest fresh correction: give `_pin_document` a bounded maximum parameter
with unchanged1MiB default; pass8MiB only at this supervisor-manifest call; use
that parameter consistently for both the size check and bounded read. Preserve
exact digest, returned size/pin equality, duplicate-key/document checks and all
other source/import/owner checks. This aligns this one call with existing
supervisor policy, rather than globally widening ordinary document caps.

The later checks already accommodate the same document: `verify_imports` uses
`_read_pin(manifest_pin, 8*MIB)` at line246, and main's protected-installation
extraction uses `P.pin_fields(..., 8*MIB)` at line327. `_pin_document` has only
the profile and supervisor call sites in this entry. There is no need to weaken
the profile/input/report limits, skip the manifest, change its contents, or
adjust mathematical/resource budgets. Root owns a fresh successor and selection;
this audit does not approve uninspected repair bytes.

## Actual operation and retained evidence

Use root-relative base
`W = product-local/v5-distribution-installed-producer-01/v-continuation01`.
Root reports terminal exit1. Saved `W/snapshot-01/RESULT.json` agrees:
`status=FAIL`, child exit1, and
`ValueError: PRODUCER_LAUNCH_CHILD_NOT_CLEANLY_COMPLETED`.

The selected release remains
`8a32634040ac940bb93f6f20681cbbe943a9396c168c7ce9aec548c4153c2403`.
I checked actual lengths/hashes for its manifest, descriptor, selected profile,
snapshot input, installed/copied entry and V packet. Both original and copied
selection have the exact6a629295 digest below. The command uses the selected
isolated bundled Python, copied entry, snapshot action, installed source root,
exact profile/input pins and original limits. It is the intended operation, not
an alternate executable or silently amended input.

Stdout contains the948-byte bootstrap failure report:

- error `ValueError: LIFECYCLE_ENTRY_DOCUMENT_BOUND`;
- `owner_creation=NOT_ATTEMPTED`, `owner_created=false`;
- prepare/snapshot/host/proof/run/request/preflight call counts all0;
- no snapshot result, production result or request;
- final binding diagnostic `LIFECYCLE_ENTRY_NO_SAFE_OWNER_REPORT_PATH`.

The latter is a consequence, not the root cause: bootstrap failed before the
code established a safe writable owner-report path. It emits diagnostics to
captured stdout rather than writing an unvalidated path. `owner_closed=false`
does not indicate a leaked constructed owner here; none was attempted.

Actual `W/capsule-01` and `W/snapshot-01/OWNER-RESULT.json` are absent.
`FINALIZATION-PENDING.json` remains; both failure-marker paths are absent.
This is consistent with a failed child and a noncommitted parent operation;
the pending marker continues to prohibit adoption. Never remove it to relabel
the attempt or infer success from absence of a separate failure marker.

## Closure and cost

The child Job reports exit1, direct child reaped, Job closed, no cleanup errors,
no termination requested,2 total processes,0 active and0 terminated. Stdout948
bytes, stderr0. Known measured cost is0.28125 inclusive Job CPU plus6.1875
separate parent CPU = **6.46875 CPU seconds**. Reported wall6.8545065 seconds;
peak Job private commit24129536 bytes. Limits remain360CPU/360wall/4096MiB/
2 active processes. No cap was raised or allowance renewed.

Parent finalization/report tails and pre-clock interpreter startup are not
claimed zero. `observed_output=null` is an absent output-census observation,
not zero output. The retained child controller0.015625CPU is nested in the Job
cost and must not be added again. No proof-production cost occurred.

## Exact pins

| File relative to W | Bytes | SHA-256 |
|---|---:|---|
| `SNAPSHOT-PREPARED.json` | 39235 | `fae80b3bd3aa2769c55117693b73d6cd9abdf25249e12f4c1a1d6569ef58fb11` |
| `inputs/snapshot-selection.json` and copied `snapshot-01/selection.json` | 17567 each | `6a629295953ed31ffed665a957ef91228001e4de4bccc34e7197db34f051a25a` |
| `inputs/snapshot.json` | 1764 | `c1a3c5dfd18e4c6fddf8d138fdf1f240d26100ea23e383970a0eddecf05607a9` |
| `profile/profile.json` | 28402 | `f63ca04b8b3f73212cd4f0757d0b8d16f53bfed2a2bf1dfa172dd627fc1b128a` |
| `snapshot-01/RESULT.json` | 3650 | `aa74d4e7192518173e4d4eb49b34b1672118566f85e2c79c412c045622090431` |
| `snapshot-01/command/command.json` | 1868 | `85597fa880bd3dfad1072f6d5d597d0f876f31fa253793f5b3b3996eb99f0308` |
| `snapshot-01/command/stdout.txt` | 948 | `c53ae3567d2d5d2be44f6ddbee0a4affbfacf4a09a53b055d9361c8c34c8e1ab` |
| `snapshot-01/FINALIZATION-PENDING.json` | 115 | `1f4267ff92e4da940e4b0a147bd60b8f1159e9401fa22fb3762b0fea9960a8ba` |

Selected V packet remains485109 bytes,
`20edd3884f6af9af365226519375236f6634af008c19090249d0343d4bc81bb1`;
no new result about its snapshot execution follows. Preserve this attempt and
its charges; any retry must use separately selected fresh paths/source identity.
