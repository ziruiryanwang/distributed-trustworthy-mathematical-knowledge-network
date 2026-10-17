# Actual client 01: exact contract failure and minimal source successor

2026-10-16. Author: `memo_independent_review`. Canonical guard PASS. Initial
assignment was source-only diagnosis; root subsequently selected only fresh
`client/actual_assets02.py` and `client/actual_owner02.py`. No product/test code
was executed, imported or compiled; no Git state was changed. All actual01
sources, plan and evidence remain unchanged.

## Cause, not a speculative hypothesis

The preserved traceback ends at actual01's snapshot `actual_assets.py:105`:

```python
C.fields(params["assets"], RETAINED)
```

The exact retained callee `modules/codec.py:48-50` is:

```python
def fields(value: Any, names: set[str]) -> dict:
    require(type(value) is dict and set(value) == names, "EXACT_RECORD_FIELDS")
    return value
```

`RETAINED` is a dictionary mapping asset names to size/hash pairs. The left
operand is a set; the right operand is a dictionary. They do not compare equal
even when the key collections match. Thus the correctly shaped selected asset
map deterministically refuses. This is a new caller/callee contract mismatch,
not a corrupt asset, unsupported receipt, bad theorem, failed source export or
network problem. The shared strict codec must NOT be weakened to accept it.

Both author's self-review and the independent whole-source clearance missed
this exact type requirement. The earlier clearance is superseded by this
observed failure at that boundary; the source mathematics review is unaffected.
No new broad test campaign is warranted to prove elementary set/dict semantics.

## Actual reached extent and conserved evidence

`main(context)` evaluates `Strategy(context)` before calling `run()`. Strategy's
first assignment evaluates `Assets(context)`; the failing field check occurs
before its asset-reading loop. Therefore no mathematical workspace, grant,
receipt/native/preparation owner, source authoring or Node service was created.
The actual `work/` directory has zero entries. There is no `actual-result.json`
because the strategy's report/run/finally block was never reached. The outer
launcher correctly preserved `BOOT-FAILED.json`, stderr and failed result.

| Preserved evidence under `product-local/v5-client-owner-runs/client-actual-01/` | Bytes | SHA-256 |
|---|---:|---|
| `RESULT.json` | 2253 | `342303c66d75ac3d7987d7ad72eae74b4640417d498f12a742d3ecf8b8bf448c` |
| `BOOT-FAILED.json` | 87 | `c99ab7e76b9858a8a895eec36c74935906186f7044aff90a1f227da8ecf44bc9` |
| `command/stderr.txt` | 1830 | `3ac74b9eee0d5e714f89879ab0c441f771d204f9d4593a718ecf4c180834aaa4` |
| `sources/v5/client/actual_assets.py` | 10738 | `0cef5f4e8ff7590d52f51d73f3fa42ca23ab4ace4a75eeff16dd0df49f68ef87` |
| `sources/owner/actual_owner.py` | 22521 | `2f2f07aa6ac91618120b210abec99ddbef4818332bd2d7915e6b0c837efc1016` |

Selected plan SHA:
`dad9f1d436c71f836d467fe14713d38e975563bd067836996eb292ec0d9b60d2`.
Outer status `COMMAND_FAILED`, direct child exit 1, reaped, Job closed, no
cleanup errors or termination request, final active/terminated processes 0/0.
Known Job CPU is 1.046875 seconds; wrapper CPU is 0.328125 seconds, including
the reported 0.296875 bootstrap subset. Add Job + wrapper only: 1.375 seconds,
not a triple count. Outer wall is 1.4552277 seconds. These are retained costs,
not a refund or authorization to renew the old allocation. Pre-clock interpreter
startup remains unmeasured. Independent outcome audit is owned separately.

## Selected successor: exactly two textual substitutions

Root authorized exact fresh copies of the two predecessor files. Before editing,
their SHA-256 hashes matched the predecessors byte for byte. `apply_patch` then
made only these substitutions:

```diff
# actual_assets02.py
- C.fields(params["assets"], RETAINED)
+ C.fields(params["assets"], set(RETAINED))

# actual_owner02.py
- from client.actual_assets import ...
+ from client.actual_assets02 import ...
```

A read-only exact UTF-8 comparison confirms each complete successor equals its
predecessor with just its shown replacement. No line-ending or incidental
source rewrite occurred. The used predecessor hashes were checked again and
remain unchanged.

| Fresh source under `software/v5/client/` | Bytes | SHA-256 |
|---|---:|---|
| `actual_assets02.py` | 10743 | `4ec62954467e9c2a62a66ffeb4f1ec945b6d33cbe1ae7b484cc1a2869c0b2c69` |
| `actual_owner02.py` | 22523 | `6fa4f0253c0f23bbc3b6d5b4005c40d6f8b40d02251bb4b78e03e3a37f65e12c` |

The bounded static scan of both new owner files found all five `C.fields`
calls: the asset map now explicitly supplies `set(RETAINED)`; the other four
already supply literal sets. No additional field-helper mismatch was found
in these newly introduced files. This is not a claim that every future runtime
boundary or entire repository has been tested.

## Exact next ownership and no duplicate passing work

Root owns a fresh selector/plan/run, with `owner_entry=actual_owner02.py`,
`owner/actual_owner02.py` and `v5/client/actual_assets02.py` selected. Remove the
old helper from the selected import closure unless some explicit unchanged
dependency needs it; do not leave the new module unpinned. All other selected
product/portable/worker/data/runtime bytes and finite mathematical workload
stay unchanged. Independent reviewer checks the exact two-source delta and
emitted selection before root decides any launch.

Do not restart actual01, alter its result, or rerun the passed profile/client
control suites. No mathematics phase passed in actual01, so the intended three
phases have no accepted intermediate output to resume. The necessary fresh
bootstrap is not a repeat of receipt or theorem work; those calls never began.
If a new operation reaches a later failure, its actual reached extent must be
used before choosing another successor. The full v5 goal and affordable-frontier
obligations remain open.

## Actual02: real admission followed by an author-source namespace refusal

The next operation, `product-local/v5-client-owner-runs/client-actual-02`,
reached genuine receipt verification and constructed its import context. Its
saved author stdout then refused the imported `open` namespace, followed by
unknown `Tree`, `fold` and `Tree.rec`. This is not the earlier zero-stage
failure. Its exact seed operation is
`32e6ddf7d813b557cc208294db3a4725d0a08a4da149c6c6fd1713d3252c273b`.

The saved `source-request.json` actually contains the selected base-owned
declarations `CommonsV5.Tree`, its constructors and `Tree.rec`,
`CommonsV5.fold`, and `CommonsV5.binary_congr`. The absent convenience is a
registered namespace for `open`, not missing mathematical declarations.
The existing `software/v5/authoring/API.md`, under **Names and compatibility
envelope**, already explicitly requires qualified names and explicit recursors
when namespace, notation, instance and attribute registries are not restored.
The strategy violated that existing contract; the importer need not change.

The selected frontend source is `authoring/native02/AuthorLean.lean`, not its
failed-build predecessor. Its `structuredName` restores exact string/numeric
name components, and `absoluteName` prefixes the module's exact string identity
with `DMKN.Mod`. `addChecked` uses `addDeclCore` with `doCheck := true`.
`installGroup` verifies both kernel and frontend constant presence with exact
names. That constant visibility is distinct from namespace registration.
The retained `workloads/ReceivedFoldMap.lean` uses the qualified spelling
throughout and supplies a directly relevant established source pattern.

Actual02's preserved report records one 223,594-byte I receipt attempt, one
import session and one author call; zero publication attempts, mixed native
admissions, search or network services. `receipt-1/binding.json` records
`SAME_CALL_BINDINGS_VALIDATED_BEFORE_HANDLE` for the exact base and retained
receipt hash. The subsequent successful import-context step used that live
authority. Author preparation charged 2.90625 worker CPU seconds against its
60-second reservation, with known closure. Controller CPU since grant is
20.03125 seconds, inclusive of preparation controller work, not an additional
independent total. Seed-grant elapsed time is 52.9288467 seconds. Cleanup errors
are empty and owners are closed. The empty `phases` map means no phase reached
its post-publication recording point, not that no mathematical work occurred.
Outer process costs and lifecycle are independently audited by the root's
separate reviewer; these component numbers must not be double counted.

## Fresh03: naming-only correction selected and implemented

Root selected exactly one new source, `software/v5/client/actual_owner03.py`,
with unchanged `actual_assets02.py`. `Copy-Item` first made an exact fresh copy
of02; its initial SHA-256 matched02. `apply_patch` then changed only the three
source generators (`prefix`, `seed_source`, `projection_source`):

- Remove `open DMKN.Mod.«BASE».CommonsV5` from the emitted prelude.
- Spell each imported `Tree`, `fold`, `Tree.rec` and `binary_congr` with its
  full `DMKN.Mod.«BASE».CommonsV5` prefix. The fixed `@BASE@` template marker is
  replaced by the existing exact `BASE` constant, not a caller-selected name.
- Preserve the already fully qualified discovered-module `ClientV5.fusion`
  reference and its existing `C.digest_string` validation. Digest strings cannot
  contain the `@BASE@` marker, so the fixed replacement cannot rewrite the
  discovered identity.

No theorem, definition, notation, instance, axiom, helper lemma or imported
constant is added. The two mathematical declarations remain generic fusion and
paired-fold projection with exactly the same proof strategy and obligations.
Formatting wraps the now-long qualified expressions only. There is no namespace
registration workaround or trusted importer/checker change.

A read-only complete UTF-8 comparison confirmed identical text before
`def prefix()` and from `def inspect_author(` to EOF. The exact `git diff
--no-index` contains only the described generator region. All grants, evidence
inspection, actual exported-proof-edge requirements, owner/worker limits,
search/publication logic, and cleanup remain unchanged. No Git index/config or
branch operation was performed. Used02 and helper02 hashes were rechecked.

| Source under `software/v5/client/` | Bytes | SHA-256 |
|---|---:|---|
| New `actual_owner03.py` | 22854 | `5342d9e1b0f79e1a2530ecc82ef9493167996fee3bcadea535a812c86ac5912a` |
| Preserved `actual_owner02.py` | 22523 | `6fa4f0253c0f23bbc3b6d5b4005c40d6f8b40d02251bb4b78e03e3a37f65e12c` |
| Reused `actual_assets02.py` | 10743 | `4ec62954467e9c2a62a66ffeb4f1ec945b6d33cbe1ae7b484cc1a2869c0b2c69` |

This assignment executed/imported/compiled no product or test code. Root owns
the fresh03 selection and launch after independent changed-boundary review.
Do not rerun actual02 or erase its successful receipt/failed-author evidence.
A fresh operation still requires a genuine new live admission of the retained
I receipt because actual02's owners are closed: a saved report cannot recreate
mathematical authority. This is receipt verification, not new receipt production,
and the failed author work remains charged and visible.
