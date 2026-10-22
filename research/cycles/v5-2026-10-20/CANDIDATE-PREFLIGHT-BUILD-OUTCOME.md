# Combined preflight distribution: independent build-outcome audit

2026-10-22, `storage_outcome_audit`.
**PASS_SELECTED_FILE_ONLY_BUILD; INSTALLED_MALFORMED-PEER_WORKFLOW_NOT_YET_TESTED.**

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Operation: `experiments/v5-local-checks/distribution-candidate-preflight-build-01`.
Installation: `product-local/v5-distribution-candidate-preflight-01/Mathematical Commons v5`.

Release manifest SHA-256:
`bd9f161c43551a578605d5e0c7da34c332cb838c1c70ddb859d2ebd0062b8f03`.

This is a saved-evidence/map/installation audit after root reported terminal
completion. No process polling, rerun, product import, mathematical verification,
database/credential read, installation mutation or Git change was performed.
Root retains adoption and later runtime-selection authority.

## Actual result and exact composition

The unchanged builder returned `DIRECTORY_CREATED_AND_EXACTLY_VERIFIED`, with
9875 payload files totaling842762131 bytes and mathematical_acceptance false.
The release manifest itself is an additional2371187-byte file, excluded from
the payload count/sum. Its independently calculated hash matches the builder's
360-byte stdout. Stderr is empty; both raw logs and the full saved supervisor
result were read.

The new2813950-byte input is pinned to
`25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364`.
Its top-level keys and every non-SDK value match the authoritative exact-packet
input `328c21bb...`. The logical SDK comparison finds precisely six replacements,
one addition, zero removals and123 unchanged rows:

| Change | Logical module |
|---|---|
| Replace | `v5/delta/custody.py` |
| Replace | `v5/admission/verifier.py` |
| Replace | `v5/aggregate_claims/aggregate_admission.py` |
| Replace | `v5/evidence_network/transport.py` |
| Replace | `v5/client/workspace_evidence.py` |
| Replace | `v5/client/managed_owner.py` |
| Add | `v5/admission/clean_refusal.py` |

All130 installed SDK files were independently read/hash-checked against the new
input, installed release map **and the actual passed controls'130-source map**.
They total1728896 bytes and all match. Their set is109 v5 sources plus21 portable
sources. The preparation profile has exactly109 unique source-pin paths equal
to the complete installed v5 Python set; each size/hash agrees with the installed
SDK map. No dropped, duplicated or untested replacement was found.

Comparing the complete current9875-entry payload map with the preceding9874-entry
release map finds exactly the six SDK replacements and single helper addition
above, with no other payload change/removal. All other release fields except
the intended files/SDK/preparation/input-identity fields are unchanged; every
preparation field other than its source pins is also unchanged. No wrapper,
foundation, runtime, image, profile policy or protocol asset was silently replaced.

## Build and verification binding

Original and saved selection hashes both equal
`1329ea5ee86d223c65ccb949bf0ebf66f3f3646c975ad58055aa8a5545662d14`.
Saved argv/cwd/limits bind the selected isolated Python `-I -S -B`, snapshotted
builder, exact input hash and fresh canonical installation destination.

Both outer build-source snapshots and originals match their selected pins.
The installed builder remains54824 bytes at
`eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`;
the runner remains `44a7bf1b...`. The29 runtime-pin entries consist of28 unchanged
entries already checked in the controls audit and the independently verified new
input pin. The executed runner performs its own pre/post runtime-pin checks; its
terminal result records no final binding failure. This audit did not redundantly
rehash those unchanged runtime files again.

The exact builder calls `verify_release(output, manifest, full=True)` after
writing the installation and before returning success. That executed path performs
the full payload census/length/hash and base-projection checks. Independent audit
covered the manifest, all complete-map differences, every installed SDK file,
preparation pins, builder/source snapshots and saved result. It did **not** repeat
an842MB payload-hashing sweep. Unchanged runtime payload assurance here uses the
selected builder's successful full verification, not a claimed second auditor sweep.

## Closure and cost

The supervisor records natural child exit0, `COMMAND_EXITED_ZERO_AND_CLOSED`,
direct child reaped, Job closed, no requested termination and no cleanup errors.
Final and last-observed Job reports agree: active0, terminated0, cumulative total2.
No live service/proof allocation is reported by this finite file-only build.

| Measurement | Recorded value |
|---|---:|
| Job user / kernel CPU |32.46875 /28.984375 s|
| Inclusive Job CPU |61.453125 s|
| Separate outer wrapper CPU |1.4375 s|
| Known combined CPU |62.890625 s|
| Outer wall |290.0570288002491 s|
| Command wall through cleanup |289.97358650015667 s|
| Peak Job private commit |56614912 bytes|
| stdout / stderr |360 /0 bytes|

The1.171875s inner supervision measurement is part of the outer wrapper CPU and
is not added again. The envelope was120 CPU seconds,600 wall seconds,128MiB,
two active processes and1MiB per log, using the existing sampled-limit semantics.
No performance improvement or mathematical result follows from these build costs.

## Evidence pins and adoption boundary

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| Saved `selection.json` |8554|`1329ea5ee86d223c65ccb949bf0ebf66f3f3646c975ad58055aa8a5545662d14`|
| `RESULT.json` |2272|`1e4f4e302358f47798764ca82e48dd8074622d5b79c8364e4046aa18ecc66202`|
| `command/stdout.txt` |360|`3b7e93e3eea96ebdd9ff55f6e3bfd73adaa89897f0362a7e5dedc9410f54aac8`|
| `command/command.json` |919|`bd2fc1d1aa5f1e4b6216231a9a80c3f5e6adcd49a5cd197bb040121fa24ca75c`|

This immutable installation packages the exact reviewed and focused-control-tested
candidate. It does not yet establish its real malformed-peer/context-continuation
workflow. That single installed boundary remains separately selected/reviewed;
no proof production, state migration, public publication or full-v5 completion
is authorized or established by the passing build. Preserve all used bytes and
do not repeat this completed build merely to improve its label.
