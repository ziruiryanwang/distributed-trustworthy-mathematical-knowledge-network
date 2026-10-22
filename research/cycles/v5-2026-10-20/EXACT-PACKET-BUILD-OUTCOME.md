# Exact-packet distribution: independent actual build outcome

2026-10-22. Reviewer: `storage_outcome_audit`.
**PASS_SELECTED_FILE_ONLY_BUILD; INSTALLED_MATHEMATICS_NOT_YET_TESTED.**

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Operation: `experiments/v5-local-checks/distribution-exact-packet-build-01`.
Fresh installation: `product-local/v5-distribution-exact-packet-01/Mathematical Commons v5`.

Release manifest SHA-256:
`ffecdc80e2dc57f062aac0aadf37be2a9dadafa24539b34a2e702c0ec24ee4bb`.

This is a read-only saved-outcome/source-map audit. No program import, receipt
verification, database connection, credential read, runtime restart, installation
mutation or Git mutation was performed. Root retains adoption authority.

## Actual result and source identity

The selected unchanged builder returned `DIRECTORY_CREATED_AND_EXACTLY_VERIFIED`,
reporting 9,874 payload files / 842,727,795 bytes and `mathematical_acceptance=false`.
The release manifest itself is an additional 2,370,856-byte file, not included in
that payload count/sum. Its hash agrees with the builder output. The saved command
and supervisor bind exact input `328c21bb...`, selected builder snapshot and fresh
destination. The outer selection is `539cdda9...`.

I independently compared the complete new input with the authoritative prior
storage input `a629df82...`. Top-level keys and all non-SDK values are unchanged.
The 129 logical SDK key sets are equal: precisely six rows replaced, zero added
or removed, and 123 unchanged. The new input has 108 preparation-source rows.

I independently read/hash-checked all 129 installed SDK payloads (1,694,560 bytes)
against both the new input and release map, and checked the preparation profile's
108 source-pin length/hash bindings. All match. Comparing the full new and prior
release payload maps finds the same 9,874 keys and exactly these six changes:

| Logical module | Bytes | Selected SHA-256 |
|---|---:|---|
| `v5/evidence_network/transport.py` | 8581 | `b34032085bca3ddbd248afe57e655777a140d2c34b6f33ea61b80721a07b926c` |
| `v5/placement/controller.py` | 18008 | `77820241984b9dc7ba5d2117a4b11bc89bf217b81697ed8d8ce90fff15e115f2` |
| `v5/client/workspace_evidence.py` | 53636 | `3f39d9b594490f04e2737c0f0595c881785a9a6a168cf8fc679d25a5cdef700e` |
| `v5/client/workspace_staged.py` | 17110 | `5d96c8cb891eabeb083b0bc501df1a7b268c21b73f4c17da7eb536d2428ad995` |
| `v5/client/semantic_reader.py` | 35110 | `253b0ffb5825de15c239be785edcda7e15647038716679402cdf990b81f4128d` |
| `v5/client/managed_owner.py` | 33789 | `9a459df2cf2c81b953044b4b5172aaefb9a3001cede6f3a1a23b29f8beb6dcb1` |

The installed builder is 54,824 bytes/SHA-256
`eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`.
Both selected outer source snapshots match their selected hashes; 29 explicit
runtime/input pins are retained. The source/map comparison found no additional
SDK, wrapper, runtime, foundation, image or protocol replacement.

## Full payload verification versus this audit

The exact builder source calls `verify_release(output, manifest, full=True)`
after writing the installation, before producing the successful result. That
path validates the manifest, performs the exact file census, checks each payload
against its length/hash, and checks the named base projection. It is the executed
full-payload verification used here.

In accordance with the selected efficient audit scope, I did **not** repeat an
842 MB runtime-payload hash sweep. Independent checks cover the exact manifest,
complete map differences, every installed SDK file, preparation pins, selected
outer sources and saved outcome. Unchanged runtime payload identity relies on
the selected builder's successful full verification, not on a second auditor
rehash. Hash identity and successful packaging do not establish mathematical
correctness, security assurance or installed workflow compatibility.

## Clean closure and actual costs

The supervisor records child exit 0, `COMMAND_EXITED_ZERO_AND_CLOSED`, direct child
reaped, Job closed, zero final active processes, no cleanup errors and no requested
termination. stdout is exactly the 353-byte build result; stderr is empty.
The selected envelope was 120 CPU seconds / 600 wall seconds / 128 MiB / two
active processes / 1 MiB per log. There was no proof or service allocation.

| Measurement | Actual value |
|---|---:|
| Aggregate Job CPU | 32.71875 s |
| Outer wrapper CPU | 0.890625 s |
| Known combined measured CPU | **33.609375 s** |
| Outer wall time | 229.22007669974118 s |
| Command wall through cleanup | 229.14919860009104 s |
| Peak Job private commit | 57,491,456 B |

The inner supervision CPU value (0.609375 s) is part of the outer wrapper's
measured process CPU and is not added again.

## Exact evidence pins

| File | Bytes | SHA-256 |
|---|---:|---|
| Build `selection.json` | 8526 | `539cdda982392f8f128103909b53c9c74b014c5613562b9252e679979c4185ed` |
| Build `RESULT.json` | 2248 | `407a0ff925fc633f576827e9c0d43b6736138c17f72d38805c925d2787e08dc5` |
| Build `command/stdout.txt` | 353 | `41301bc3507268650e348ab0744c46f0c6b0b308195a976e2fb883e25808a12c` |
| Fresh `distribution-exact-packet-01-input.json` | 2813358 | `328c21bb585881d654f1a23f1704fbaa277ee865f7adb1250cf6c19b85647561` |
| Installed `V5-RELEASE.json` | 2370856 | `ffecdc80e2dc57f062aac0aadf37be2a9dadafa24539b34a2e702c0ec24ee4bb` |

## Adoption boundary

This new immutable installation contains the reviewed, focused-control-tested
exact-packet successor. The prior managed-storage installation and all previous
evidence remain unchanged. No state migration, old-state reopen or public
publication occurred. Actual installed genuine-receipt acquisition/admission
remains its separately selected next gate. Full v5 remains unfinished; this
passing build is not a deployability, global-growth or worldwide-operation claim.
