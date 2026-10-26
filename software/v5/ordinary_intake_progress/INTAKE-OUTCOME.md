# Independent Std intake02 outcome

Disposition: **CLOSED_REFUSAL_NATIVE_DIAGNOSTICS; NO_CONFIRMED_EXTENSION**.
The finite selected operation ended unsuccessfully. It is not a rich-library
acceptance or growth result. Read-only audit of saved files; reviewer performed
no rerun, product import, owner/status call, database API or native operation.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Checkpoint: `research/cycles/v5-2026-10-26-local-discovery/CHECKPOINT.md`.
Run: `experiments/v5-local-checks/std-intake02`.

## Selection and terminal evidence

All four source snapshot/current pairs and 220 selected external pins were
independently rehashed and match. The saved selection is the exact current
selection, not the retained stale draft. Fifteen files remain under the run.

| Saved evidence | Bytes | SHA-256 |
|---|---:|---|
| `selection.json` | 54,973 | `1f168a31dda79d80b6e2a933431999ac4e4a1beb1bbc27acd39d6464df60343b` |
| Outer `RESULT.json` | 3,280 | `9237a8965971736f421a8caf6556e5317dfd6f65988937475e08dd07fd013064` |
| `public-launch/RUN.json` | 1,157 | `b768c0da66c9187ac4eec19e18affaac61fc4052b1a5f372f3c26ce8027ac2e9` |
| `public-launch/SUPERVISION.json` | 2,782 | `e5720afb249eb5b78c0da784f907a8bcd17ae4c73a7173c8400c78fcf9fe5a40` |
| `public-launch/child/stdout.txt` | 1,773 | `a3b28e336de9ad3aee25bd656ce0f36741f842ed59ae7cad06d048469ba034fd` |

The owner reports operation=intake-baseline, ok=false, outer IntakeError with
detail CatalogError `ADMISSION_NATIVE_DIAGNOSTIC`, phase ADMIT, failed_batch=0,
batches=[], selected_root_validated=true and possible_unreported_commit=true.
Its last confirmed root remains the recovered basis
`3034986549a52b2a0b46f5fffe2c650879453f43ff85d4ef38cf3ff73b7a7d62`.
Top-level accepted=null does not override the detail's uncertainty.

## What failed and what did not establish acceptance

There is one new native call under `std-catalog01/admission-calls/`:
`ab49ae0949ff479e3f124209bdd967005f87dda7dd82ae3a35c0ca27d99e2c36`.
Its supervision result is 3,028 bytes, SHA-256
`755bcecff355efc56ef4e4bfdbe9b14fa3c6413238a93405d32555d6e52a40b1`.
Native execution exited zero, reaped and closed with no cleanup errors, zero
active/terminated processes and no termination request. Its stdout is empty;
stderr is **2,864 bytes**, SHA-256
`2c101abd5788e4483b62131c69b9fe7899bfcc2985201e8d0a225ccfcf892db5`.

The stderr contains twelve PANIC lines from Lean.AsyncConsts.add concerning
duplicate normalized declaration names: private PSigma.casesOn._arg_pusher
across modules, private List.filter.match_1.splitter across modules, and public
List.mem_cons_self versus its private counterpart. These are observed native
diagnostics; their architectural cause belongs to the separately assigned
source investigation, not to this outcome audit.

The pinned ordinary_admission.py diagnostic check (lines 664-672) requires
empty extension stdout and stderr after clean native closure. It refuses here,
before worker-report acceptance checks and `_commit_checked`. Do not suppress
the diagnostic or promote the output because execution exited zero.

The retained worker report advertises 1,024 units, 1,162 names and a 2,150,184-byte
artifact. Report SHA-256:
`c2546a936c646e8264fcfd96a3c8ace3273ecb448b56974dfde0bbf9d579c273`.
The actual retained chunk under operations/99b2e18991af7a0fcdff2e68bacea42b4f1c7f25274a63bee3e813e856a0c12c
has that length and SHA-256
`9596f8b04711bd21341d9498f67d7583a5f57b83466a2e6f323db854892abf9a`.
Neither file establishes acceptance. The source refusal precedes promotion,
but the official conservative uncertainty flag is preserved and no fresh
catalog inventory is asserted without a separately selected supported recovery.
No WITHDRAWN file is present; its absence is also not acceptance authority.
The original 669,968-byte basis artifact remains byte-identical (SHA-256
`e5e2698ca21e8f8e5566407e3804cfc20506718cd9387f8e815c3ba25cce0e0b`).

## Diagnostic and cost observations

The single new diagnostic directory is
`std-catalog01/intake-diagnostics/77da6a0438c687172593efb62913abd8`.
Fourteen records run from ENTRY through all three metadata batches, first-batch
read/preflight and ADMIT_INTENT to FAILED. There is no BATCH_CONFIRMED or COMPLETE.

| Recorded boundary | Intake-relative wall seconds | Controller CPU seconds |
|---|---:|---:|
| METADATA_COMPLETE | 54.8219042 | 38.1875 |
| First ADMIT_INTENT | 62.8946008 | 46.0625 |
| FAILED | 137.6903501 | 63.03125 |

FAILED preserves zero confirmed batches and uncertainty=true. Its native
reservation is 60 seconds; observed worker CPU is 25.8125 seconds, explicitly
partial and not refundable authorization. This localizes the observed boundary;
it does not split all admission internals or establish a general performance law.

Outer/public processes exit one and report unsuccessful operation, but both
are reaped and Job-closed with no active/terminated processes, cleanup errors or
termination request. Their stderr files are empty. The native panic text is in
the separate native stderr above. No supervisor reports resource exhaustion.

- Outer wall: **140.3750267 seconds**.
- Inclusive outer Job CPU: 90.328125; wrapper CPU: 1.59375 seconds.
- Known combined CPU: **91.921875 seconds**; nested worker/public/controller
  observations are included or partial and must not be added again.
- Peak outer Job private commit: 1,023,553,536 bytes, within its selected cap.

All state, artifacts, diagnostics and prior evidence remain retained. The first
interrupted intake's cause/cost remain unknown; this failure does not explain it.
No automatic retry, status call, cap increase, private repair or acceptance from
the saved chunk/report follows. Resolve the native representation issue in
principle before selecting recovery or further mathematical execution.
