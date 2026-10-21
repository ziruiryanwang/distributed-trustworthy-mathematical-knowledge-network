# Restricted guest preflight failure and fresh correction

Disposition: **build01 and build02 failed separately before compilation.**
Build02 corrected the first failure at its narrow source gate, but its actual
preflight then correctly refused an overridden predecessor RESULT. Neither
attempt produced a guest. The snapshot-host adapter does not repeat the first
saved-selection error. Root owns fresh selections and execution. This review
ran no compiler, guest, proof, product import, network operation or replacement
experiment.

## Actual failed attempt

Root invoked the selected guest builder once using `D:\Python314\python.exe
-I -S -B`. Its selection was
`experiments/v5-local-checks/restricted-guest-build-01-selection.json`, SHA-256
`afc4eeb4836b8510b8f2e40d0c3bfefd6b573cf0cc209be911b5aac9e9aa9c13`.
The used builder `software/v5/restricted_guest/build.py` has SHA-256
`79a19fb822cbaed734f737e723ac9a2eabcfc8b0f13256ca1814ed728dcdff02`;
used `recipes.py` has SHA-256
`b2fc5d26e4504c4caf8a41c62ff47048daf13dd2c3653af8a67f7ef8e09903ed`.

The invocation exited 1 at `NATIVE_SAVED_SELECTION_BINDING` (original line184).
This check precedes fresh-run directory creation, the normal report
`try/finally`, phase creation and every compiler invocation. Independently
checked: neither `restricted-guest-build-01/` nor
`restricted-guest-build-01-attempt.json` exists. The selection remains preserved.
Their absence is consistent with this early preflight refusal; it must not be
reported as successful build cleanup.

The tool reported wall time **0.2681722 seconds** to root. There is no CPU
measurement or worker Job closure report for this attempt. Do not convert the
wall number into CPU or invent worker statistics. No compilation occurred.

## Exact cause: two legitimate serializations were confused

The native builder `software/v5/restricted_composition/build02.py` saves its
parsed selection using `h.save(run / "selection.json", chosen)` and checks its
parsed contents later. Its RESULT correctly identifies the **original input
selection's bytes**, not the reserialized saved copy's bytes.

| Record | SHA-256 |
|---|---|
| Native original `restricted-composition-build-02-selection.json` | `659c780e902b69cfb039b854abae05d6a570c389f463dc8bfc6fff9bfa455244` |
| Native saved `restricted-composition-build-02/selection.json` | `ba75f861370d976aabdea528334743cc7ca9dd1d714e623bc8cb5967886d71ba` |
| Native `source-map.json` | `32e95e4b67377ac2f8b6cf1b7087a006c675c15db98f954415ab996f7393ac04` |

The two native selections parse to exactly the same four top-level fields and
15 source pins. Their differing raw digests are not evidence of changed source
selection. The failed guest builder nevertheless required the saved copy's raw
digest to equal the original digest in native RESULT.

Other conjuncts were checked separately and hold: native source map equals the
saved selection's `sources`; the native attempt exactly binds native status and
RESULT digest; controls' saved selection digest is
`7dd9e6b651f91ddf6638bceffc78593e7696d2df95c234075b15a68136f26291`,
matching controls' outer RESULT. That controls wrapper preserved raw bytes.

The earlier `RESTRICTED-GUEST-BUILD-REVIEW.md` source PASS missed this
byte-versus-parsed-identity distinction. It remains preserved at SHA-256
`86cf6cd3f175e6acdd04d000167c37e67de723bb539a68536843fe89a5d50f35`.
This document corrects that review; it does not rewrite the PASS or the failure.

## Fresh build02: exact changed boundary reviewed

| Fresh source | SHA-256 |
|---|---|
| `software/v5/restricted_guest/build02.py` | `bf52078077622ec1412e14be73063ad4ee0a1fa22b802d8843ecdd548f718b26` |
| `software/v5/restricted_guest/recipes02.py` | `8a47c8467c21f3a41d9649151ffdbbed91b6c9adbf38261cee0dfcdf2b5fc235` |
| This cycle's `Select-RestrictedGuestBuild02.ps1` | `7eaa5ffa8a4cb3419dff82f5d3f0df33164869ad601ba9578fff53c0078691af` |

Read the actual predecessor/successor diffs and both selectors. The correction:

- Pins the original external native selection alongside the saved records.
- Requires its raw SHA-256 to equal native RESULT's `selection_sha256`.
- Requires parsed saved selection to equal parsed original selection.
- Retains exact native source-map, attempt and controls bindings.
- Uses fresh run `restricted-guest-build-02` and exact adapters `build02.py` and
  `recipes02.py`; the builder's own-filename guard and recipe loader agree.
- Uses fresh crate metadata `dmkn_v5_rc_guest02_…` and the same run02 recipe
  guard. The production12 sources, three-compile sequence, retained library and
  helper chain, native adoption gates, output limits and process limits do not
  change.

An intermediate unused draft still loaded frozen `recipes.py`, whose run01
guard would refuse run02. Review caught this before use. The final `recipes02`
and builder pins above resolve it; this was **not another executed failure**.
The selector differs from01 only in the run name and two adapter paths. Its
recorded expected pins remain supplied explicitly by root.

The assembler `software/v5/restricted_guest/assemble.py`, unused at this review,
SHA-256
`b2fa03edc27419611fba51238a1cd3504f332c9977bf07529b9639909b179fdd`,
now names run02 and the two02 adapters. This is a narrow binding read-back, not
a new full assembly review. Its raw saved-selection check is appropriate here:
the guest builder explicitly copies original selection bytes and checks their
digest before writing and again during finalization.

**Source-gate conclusion:** the observed preflight defect and run-name mismatch
are corrected without weakening the native evidence bindings. This permits
root to consider its fresh finite build02 selection; it supplies no claim that
the compiler succeeds, a guest executes, a receipt exists or any mathematics is
certified. No rerun was made by this reviewer.

## Actual second attempt: overridden predecessor correctly refused

After that narrow source clearance, root invoked build02 once with fresh
selection SHA-256
`679a81a019ddc6777636074307c06c9a608c9fe82a154771690f7a657f90a6b0`.
The build02/recipes02 bytes above are now used and frozen. This invocation
exited 1 at `NO_OVERRIDING_FINALIZATION_FAILURE` inside preflight `rebind`
(line245), before `run.mkdir()` and before any compiler. Independently checked:
neither run02 directory nor run02 attempt JSON exists. Root's reported tool wall
time is **1.1595377 seconds**; again, no CPU measurement or worker Job closure
report exists.

The offending retained predecessor is
`experiments/v5-local-checks/aggregate-guest-compile-01`. Its
`FINALIZATION-FAILED.json` has SHA-256
`d0d6d8980c492d43a8927825aa153271543fa18d960305db5bde1e51c323dd54`
and explicitly contains:

```json
{
  "error": "REMAINING_TOTAL_ENVELOPE",
  "overrides_result_and_attempt": true,
  "result_sha256": "81cce68d9b20f22b12d12d5d698084eb8eb101493de71c6e35cd6acb7b44f47a",
  "status": "FAIL_FINALIZATION"
}
```

Root reports no analogous marker in the selected native, typed or controls
predecessors. The exact offending marker was read independently. The current
builder's refusal is appropriate: its pinned aggregate RESULT cannot be treated
as an unqualified successful terminal record in the presence of this explicit
override. This second failure is distinct from the resolved serialization bug.

Both failures and their cost remain preserved. The next design question is
whether the required artifact bytes have an independently justified later
adoption path. It is **not** whether to delete, ignore or waive the marker.
Artifact identity, artifact usability and the earlier operation's terminal
success are different propositions. Any successor must state which proposition
its predecessor evidence actually establishes, bind the authoritative record
for that proposition, and preserve the failed original operation. The
independent adoption-path critique is a subsequent source-only assignment;
this checkpoint does not clear another guest launch.

## Snapshot-host adapter: same-class check

Reviewed `software/v5/restricted_guest/build_snapshot_host.py`, SHA-256
`719ed9058ca9a8d5dfa59a07a362f4438bd8e9b13753b7883bfb48333021c984`,
against its preparation note and actual retained native/old-host records.

Its `RECORDS` pins the **original external selection files**. It compares the
native source map structurally to the original selection's `sources`, and
checks RESULT's `selection_sha256` against that original file's pinned digest.
It never equates a reserialized saved-selection digest with the original digest.
Actual original/RESULT digest pairs agree for both predecessors:

- Native: `659c780e902b69cfb039b854abae05d6a570c389f463dc8bfc6fff9bfa455244`.
- Small host: `e4493418256735529f7fc19ed606ea459bf35b613b57680d2e0a31a7b858e4bd`.

The native output records also match its replacement libraries: restricted
core1,719,004 bytes, SHA-256
`1bdfd6a0943b6a09248ae99aefd793b63384a957bf8d98c0cd8d8b430fd04a0b`;
restricted aggregate1,050,594 bytes, SHA-256
`be8bdcb4c815e5c610145e5fea28a6d6601fe8dd9ae8cd04f3bf35c5b9dbcbba`.

**Bounded conclusion:** no same-class saved-selection/schema blocker found.
This is not a full host qualification, runtime launch or receipt-verification
claim. No old-host/native build or controls campaign should be repeated for
this bookkeeping correction. Root and the assigned host reviewer own subsequent
host selection and any broader changed-boundary review.
