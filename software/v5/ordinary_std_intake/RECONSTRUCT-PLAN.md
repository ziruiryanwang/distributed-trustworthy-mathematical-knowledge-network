# Restore exact saved-manifest bytes, then consider public intake

2026-10-26. Source-only successor selected by root. This is one fixed local
data restoration, not a new producer, receiver, benchmark or trust mode. No
execution is authorized by this plan. The failed `std-materialize01` and
`std-export01` files, sources and reports remain frozen and failed.

## Reason for this smaller operation

The saved binding diagnostic already identified the exact 2,651 output objects
and their canonical raw byte hashes. Its saved manifest is 468097 bytes, SHA-256
`1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c`.
The failed materializer unnecessarily repeated arbitrary-input lexical validation
while trying to recover these already-selected inert bytes. It exhausted 70 CPU
seconds inside binding, before any unit write. The causal screen identifies no
proven reason for its cost increase; the old 28.125-second observation was not a
hard bound. No unchanged retry or cap escalation is selected.

The successor's question is narrower: can we cheaply reconstruct these exact
manifest-selected bytes from their already-pinned writer? Output hashes, not
confidence in a new transformation, decide whether restoration succeeded.

## Exactness argument

For each saved entry `(u,h,l)`, exclusive writing is allowed only after:

```text
len(raw) = l
SHA256(raw) = h
SHA256("DMKN-ORDINARY-EVIDENCE-V2" || NUL || raw) = u
```

The manifest hash is fixed independently of this transformation. Subject to
SHA-256 collision resistance, matching all three checks restores the selected
object. A construction mistake can refuse or emit the required exact object;
it cannot silently substitute a different accepted object. This is the same
content-identity assumption used by the current product, not a new mathematical
certificate. Actual mathematical acceptance still requires unchanged public
strict intake and its native checker.

We use standard `json.loads` only on the exact fixed writer, inventory, request,
manifest and canonical structured names produced by the unchanged inspector.
The fixed writer/inventory previously passed the general diagnostic; hashes are
checked before decoding. This does not relax arbitrary downloaded-input parsing.
There is no exposed general fast path or product-source change.

## Selected source and data

Reuse the exact frozen `ordinary_binding_reuse/measure_saved_writer.py` helper:
8449 bytes, SHA-256
`42670eb615d3ba69140804ce8af593a4f984d283156dfbab08a589684ceecd1c`.
Only its existing pinned loading/reading/hash/partial-census helpers are used;
its old `main` never runs. Load only `ordinary_evidence`, `ordinary_semantics`
and `portable_evidence`. Do not load or invoke `portable_candidate` or the
general binder. The selected helper has references to those unused modules,
but the successor does not execute those references.

Fixed retained inputs under `experiments/v5-local-checks/std-export01/bundle`:

| Input | Bytes | SHA-256 |
|---|---:|---|
| writer.json | 38154768 | 5a2f721127cfef3ae39613c1ec723b2f710cc410c872650fb2acfd7d04078b7a |
| inventory.json | 823690 | c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0 |
| request.json | 496 | bcb647fa96824cc82aebda1dab151a88d678ca3d8756cd150e0103e9f41993bd |

The 708 partials remain 6389257 bytes with the helper's complete map hash
`82df4b3e84e8e53a21ab87f94507f0ba8ecbf8c82fbc6fad1e3b0459d6bae4d0`.
Check this aggregate before and after restoration and compare all 708 raw byte
strings exactly when their corresponding complete units are constructed.

The exact manifest's ordered batches are (1024,9997243), (1024,17147916),
(603,17767684), totaling 2651 units/44912843 raw bytes. The old binder preserves
writer unit order through its splitting; the new operation zips that order
with saved entries and checks each exact hash, so an ordering mistake refuses.

## Restoration steps

1. Pin all fixed inputs and the saved helper; exclusively create
   `std-reconstruct01/materialized/units` under the existing local-check runner.
2. Decode the pinned writer, fixed basis and selected manifest. Derive exact
   basis-symbol bindings through the unchanged semantic module.
3. For each ordered unit, run unchanged `inspect_unit` to obtain external
   references. Require them to be available, build the portable wrapper, and
   canonically encode it once. Do not repeat the general lexical scan/reparse.
4. Check saved length, raw hash and domain-separated UnitID before writing.
   Compare any retained historical partial. Exclusively create, flush/fsync and
   read back this unit. Then extend the exact-name map with its output symbols.
5. Recheck fixed inputs and all old partial identities. Verify the complete new
   file census and every length/hash. Require the original selected target:
   UnitID `ab6f1b22d8760ba5615e9ec7e5a1fda99313c71a8cab34183c2fe88aad31381c`,
   ExportID `bf281176862c75a7c8be1d00359f85bdcfe4904f4aefd5977c954e822e79070c`.
6. Write bounded `RECONSTRUCTION.json`, status
   `PREPARED_FOR_MANIFEST_NOT_COMPLETION`. Write the original manifest last.
   Perform final full output census/hashes without writing more required files.

The exact output is 2653 files: 2651 units, RECONSTRUCTION.json and manifest.json.
Successful stdout is `RESTORED_EXACT_INERT_BASELINE_NOT_ACCEPTED`, with manifest,
prepared report and final census pins, zero binder calls and no mathematical
acceptance. Require the existing runner's clean exit-zero terminal result and
independent actual audit. Manifest presence/prepared report alone is insufficient.

Failures preserve the partial output and report the exact phase, active zero-based
unit index, fully written unit count/bytes, elapsed CPU/wall and error. Phases
distinguish input parsing, inspection, encoding, hash matching, writing, final
pins and census. These are cheap progress fields, not a profiler or extra test.

## Finite selection and costs

`select_reconstruct.py` accepts only `--reconstructor-sha256` and prepares one
fresh `std-reconstruct01.selection.json`. It does not launch a process or create
the run directory. It derives the fixed runtime list from adopted diagnostic
selection `412dd6bf0220eb98b03e1746295f840a5eda47a0af42b98bf299f5daa8578299`:
omit only unused portable_candidate; retain three Python files, three helper
modules and three fixed input files; add the saved manifest and old selection.
Thus **11 external pins** and **5 source snapshots**: runner, reconstructor,
selector, this plan and saved helper. No binder snapshot or hidden live import.

```text
D:\Python314\python.exe -I -S -B
  {snapshot}\software\v5\ordinary_std_intake\reconstruct.py
  {output}\materialized
```

Keep the same maxima: inner cumulative **90 wall / 70 process CPU seconds**;
outer **120 wall / 90 Job CPU / 1792 MiB / one active process**, 262144 stdout
and 131072 stderr bytes. The helper shares the reconstructor's clock origin.
All 2651 writes/fsyncs/readbacks and final hashes fit inside these allowances or
the operation refuses. No increase, restart or automatic retry is authorized.

The source reduction removes byte-by-byte Python lexical scans of roughly
38 MB input and 45 MB re-encoded output, plus portable reparse and general
manifest generation. Unit inspection, canonical encoding, hashing and filesystem
cost remain. Output is streamed one unit at a time rather than keeping a second
full output bundle. These changes justify a distinct finite attempt; they do
not prove a wall-time bound or predict completion on this PC.

Report the outer inclusive Job CPU plus wrapper once; inner costs are already
included. Neither process resource bounds nor the fixed-input reconstruction
is a hostile-code sandbox or hard filesystem quota. No native program, owner
state, catalog, custody, networking or package generation is touched.

## Strict receive remains separate

Only a reviewed complete `std-reconstruct01` outcome may replace the failed
materializer prerequisite in the unused public selector. Its exact report and
manifest become new explicit inputs; no failure is relabeled. The public
initialization/intake commands, 154-file package, actual profile, per-batch
native limits, quotas and acceptance conditions stay unchanged. Root owns any
subsequent selection, not this source plan.
