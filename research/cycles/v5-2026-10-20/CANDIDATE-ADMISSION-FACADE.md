# Terminal-candidate admission: facade source checkpoint

2026-10-22. Author: `storage_integration_adapter`. **SOURCE ONLY; no execution, installation, test, Git mutation or adoption.**

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Authority: [CANDIDATE-ADMISSION-IMPLEMENTATION.md](CANDIDATE-ADMISSION-IMPLEMENTATION.md), including root's clarification that existing import sessions/staged selections must be preserved, not forbidden globally.

## Selected files

`software/v5/candidate_admission/client/workspace_evidence.py` is a fresh successor of selected `software/v5/exact_packet/client/workspace_evidence.py`, SHA-256 `3f39d9b594490f04e2737c0f0595c881785a9a6a168cf8fc679d25a5cdef700e`. The initial exact copy was hash checked before edits. After the independent final-census finding below, the current successor is63130 bytes, SHA-256 `e81407b9296d14a3f3f2f1a1c8554efa2747829fa6a2639fc29215c7ed29cb44`; the read-only full diff has179 added/9 removed lines.

`software/v5/candidate_admission/client/managed_owner.py` was copied exactly from selected `exact_packet/client/managed_owner.py`, predecessor SHA-256 `9a459df2cf2c81b953044b4b5172aaefb9a3001cede6f3a1a23b29f8beb6dcb1`. After independent review cleared the final-census correction, its sole change replaces the embedded workspace-evidence pin with `e81407b9...`. The successor is33789 bytes, SHA-256 `3fb4e619ddff115220eee4b6d594a41b2d051e6f8b6c731d63cca15b2c8555a3`; a read-only full diff confirms exactly that one line changed.

`software/v5/candidate_admission/README.md` documents the source-only status, exact signatures, result meanings, failure boundary and usage. The lower I/A successors/helper have a separate author/checkpoint. The combined product scope is four replaced logical SDK files plus one new helper, composed with the separately frozen offer-enumeration custody source. Root owns the final130-entry map and writer identity; there is no state migration.

## Implemented interface

- `try_admit_terminal_local(module, packet_sha256, packet_bytes, *, expected_exact_journal=None, receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024)`.
- `await try_acquire_terminal(candidate, entry, *, expected_exact_journal=None, receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024)`.
- `await try_acquire_terminal_exact(candidate, entry, *, expected_exact_journal=None, receipt_cpu_seconds=30, wall_seconds=600, memory_mib=1024)`.

Every call is explicitly serialized with the original entry/fatal-cleanup/grant contract. The three new APIs use trial-only finalization wrappers described below; strict methods retain their original wrappers. No new trial body acquisition or native-verification argument is exposed. Offered acquisition keeps original exact offer membership; exact acquisition uses existing known-identity transport. Both use the existing live candidate/supplier/contact constraints, transfer/custody readback, input charging and finite limits.

The result has status, evidence kind, module, packet digest/size and a local-operational authority label. Only `ADMITTED` includes the ordinary live warrant. `NOT_ADMITTED` is produced only when the original selected issuer's `try_receive` returns `None`. `UNSUPPORTED_TRIAL_FORM` is produced for structurally valid mixed/native evidence before any verifier call. The latter retains transfer/input/custody charges and does not silently run strict mixed admission.

## Positive-path preservation

The new private `_admit_i` body is the prior atomic I-admission accounting/cache body, with the mixed facade's original I-owner guard. The new `_admit_a_member` body is the prior mixed A receipt/member accounting/cache body. Their only authority-path addition is an internal trial flag selecting the same owner's `try_receive` and a `None` return **before** cache/handle/member publication.

Ordinary public `admit_receipt` and `admit_aggregate_member` override the inherited facade methods solely to use these shared helpers with trial false. `_admit_evidence` uses these same helpers for all terminal forms, eliminating separate ordinary/trial positive implementations within the selected facade. The frozen atomic/mixed base sources are unchanged; the exact input/counter/profile/cache/member rules are ported without relaxation.

I cache hits still revalidate the same live warrant. A cache hits still validate exact aggregate/header/receipt state and rebind/create the requested exact member, retaining all member charges. Positive terminal admission still requires the exact live journal and summary to equal the packet's claim, even with no optional caller-expected journal. Packet cache insertion remains after this equality.

Network success retains the ordinary final owner `open_group`, custody-readiness, live-warrant and exact-journal checks. Trial refusal/unsupported outcomes also recheck custody readiness before normal return. No escaped exception is reclassified as nonacceptance.

Independent review found the inherited wrappers returned after `_active(); _census()` without checking expiry/withdrawal during that final census. Root authorized two trial-only wrappers in this fresh facade, preserving original `_enter`, fatal `_fail` and finally-clear-busy behavior. Their shared `_terminal_final` performs `_active(); _census(); _active()`, then nonblocking original grant/all-original-owner deadline and controller CPU checks. No I/O occurs after these final checks. This applies to all three trial outcomes, not only nonacceptance; strict predecessor wrappers and frozen base files remain unchanged. The reviewer cleared this correction before the final managed-owner pin update.

## Noninterference, not rollback

No trial path assigns to `_session`, `_context`, `_selection_view` or `_staged`, calls staging/import/authoring, or copies/restores a registry. Existing contexts and selected staged packets may be present. A different admitted packet does not replace a staged variant: it only gets a distinct positive packet-cache key and ordinary new warrant. Existing failed reader/client/owner objects remain failed and cannot enter the public wrapper successfully.

On `NOT_ADMITTED`, neither I/A helper inserts a receipt/aggregate cache item, member handle or warrant; `_admit_evidence` returns before its packet-cache insertion. Existing authority therefore remains unchanged by branch non-mutation, conditional on the lower owner's full live clean-nonacceptance gate and final facade guards. Counters and untrusted custody/evidence changes remain; all costs are charged. A clean nonacceptance does not claim false mathematics or identify the refusal's cause.

On success, new positive authority is permitted without changing existing context selections. On any escaped error, normal client `_fail` still closes original owners and invalidates authority; cleanup uncertainty still poisons the workspace. This is not general rollback or isolated mixed/native verification.

## Review and execution boundary

Self-review read the full successor diff and the exact predecessor I/A admission/cache bodies. The author checked the new paths' writes/calls for staging/import noninterference and sent source hash/signatures to the independent reviewer and root. Independent reviewer `storage_launch_review` initially cleared dispatch/accounting/nonmutation at `897978bb`, then identified the inherited final-census hole and superseded that limited clearance. The reviewer subsequently cleared the narrowly authorized correction at `e81407b9`, confirming post-census fresh authority plus nonblocking original deadline/controller checks and unchanged strict wrappers. Final managed pin is now updated. No Python import, compilation, test, executable or installation was run. Whole-source/control review and root-controlled focused execution remain required before use.

Relevant controls are: original positive warrant survives clean refusal; explicit alternative succeeds under original owners/grant; exact J/A member/opening violations stay fatal; existing contexts/selections remain unchanged; mixed trial invokes no verifier; strict APIs remain strict; positive cache reuse remains exact/live; all refusal charges remain and unsafe lower/final-custody outcomes fail closed. Add explicit expiry/withdrawal inside final census, plus expiry/CPU overrun inside the final active check. Lower cleanup/report predicates are reviewed and tested separately, not inferred from facade doubles.
