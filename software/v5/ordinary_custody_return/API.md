# Existing custody to ordinary Lean reuse

Source-only candidate, 2026-10-24. No execution, package inclusion or mathematical
acceptance is established by this document. The adapter is independent of cuts.

## Purpose and workflow

A locally held proof may be useful in a new definition, structure or theory.
Recover its complete ordinary V2 unit from existing custody, hand the resulting
file bundle to the existing `owner.py intake-baseline`, then use the independently
accepted mathematics through ordinary authoring. The receiver chooses its own
compatible, warranted parent. Neither custody nor this adapter provides that
warrant; no native/cut catalog is opened and a cut root is never a native root.

Two explicit policies differ in cost and obligations:

| Policy | Acquired units | Exact imports the receiver must supply |
|---|---|---|
| `selected-units` | Only whole units containing selected export IDs | Fixed-basis imports and all imports absent from these units |
| `closed-basis` | Selected units plus every proof-import unit until the pinned basis | Only used fixed-basis imports |

Selected mode does not silently expand when its receiver lacks a dependency.
Closed mode is a full cold proof-closure acquisition, **not ancestry-free reuse**.
Availability failure, conflicts, malformed evidence, exhausted limits or a cycle
refuse the operation; there is no retry, renewed allowance or policy fallback.

## Callable API

After the approved ordinary profile loader and exact approved helper source load:

```python
result = custody_return.write_bundle(
    loaded, custody, export_ids,
    policy="selected-units", output=absolute_fresh_output,
    limits=custody_return.Limits(), check=original_budget.check,
)
```

`loaded` is the existing `profile.load` namespace; `custody` is its open exact
`OrdinaryStore`. Export IDs are a nonempty duplicate-free list/tuple, at most 1024
by default. The helper checks exact module identity and semantics. It reads the
installation inventory, pins its existing SHA-256 and 581-name census, and uses
the existing basis/export identity functions. It does not accept a caller-made
basis or alternate claim schema. The caller serializes owner access and supplies
one nonresetting finite wall/CPU callback. The API does not own/close custody;
the caller must enforce its opening/recovery policy.

`Limits` is exactly `baseline_bundle.Limits`; all fields can only be lowered.
Default ceilings include 8192 units, 64 MiB evidence, 8 MiB per unit, 20 million parsed
nodes, 262144 import edges and 262144 distinct touched names. The name cap covers
outputs and unresolved imports. `max_binding_bytes` also separately caps total
locator bytes, stored name-binding bytes and the advisory obligations file, each
at 16 MiB by default. Pending unique lookups are bounded by targets plus names.

Before each lookup, the remaining locator/evidence-byte allowance is passed to
`OrdinaryStore`, which checks SQL lengths before BLOB materialization. Node and
import limits are reduced for the selected unit's existing parser; zero remaining
import allowance is checked immediately after bounded parsing, before another
acquisition. A single bounded unit is parsed before its distinct-name census can
be charged; no further acquisition occurs if that cap is exceeded. Whole groups
are never split to fit a cap. Existing bundle split/manifest helpers independently
validate remaining batch and aggregate bounds.

These are cooperative data/time controls, not a hard RAM, CPU or disk sandbox.
The raw evidence retained in memory is bounded by 64 MiB at default settings, but
parsing objects, indexes and selected support add memory overhead. Use a separate
whole-operation supervisor for hard process limits. No worker process is started.

## Public command

Run the owner-approved `return_bundle.py` using the exact selected Python with
`-I -S -B`. All file/directory arguments are absolute. Required arguments:

```text
--package <approved ordinary package directory>
--profile-sha256 <exact PROFILE.json SHA-256>
--helper-sha256 <approved sibling custody_return.py SHA-256>
--python-runtime <selected runtime directory>
--lean-runtime <selected runtime directory>
--custody <existing custody directory>
--custody-limits <JSON with the store's original exact limits>
--custody-limits-sha256 <exact input hash>
--targets <JSON array of exact export IDs>
--targets-sha256 <exact input hash>
--policy selected-units|closed-basis
--output <fresh disjoint directory whose parent exists>
--wall-seconds <1..3600>
--cpu-seconds <1..200000>
--approve-local-custody
```

Optional `--limits <JSON>` plus `--limits-sha256 <hash>` select lowered bundle
caps; omission uses existing defaults. All paired inputs are hash-selected before
parsing. The entrypoint first pins `owner.py` from the selected PROFILE and reuses
its `bootstrap` and complete ordinary profile loader. Only then does it execute
the exact hash-selected fixed sibling helper. No arbitrary peer-supplied code
path is accepted. Hash selection is not initial publisher trust: entrypoint,
interpreter, approved support and protected owner storage remain premises.

Compatibility baseline for review:
`experiments/v5-local-checks/bounded-investigator-src01/distribution/package`,
PROFILE SHA-256
`9c41b9a3fe36f7283af130ac6ef290e82c2a78c432980b2bea75ccdcf197a6d4`.
This does not modify or install into that frozen package. The existing public
package launcher does not automatically authorize this new standalone command;
an outer supervisor must be selected separately before running it.

The command refuses preexisting SQLite journal/WAL/SHM sidecars before opening,
so it does not intentionally recover an old store. Existing `OrdinaryStore`
nevertheless uses a **read/write SQLite handle and connection pragmas**. This is
not a physically read-only database open. The adapter calls only exact getters
and performs no logical custody writes. Owner-serialized use with no concurrent
mutation is required; the command opens no native/cut owner just to obtain a
lock. Stop other users of this selected custody before calling. Interrupted-state
recovery is an owner's separate operation, never silently attempted here.

## Files and acceptance boundary

Output contains complete exact `units/<unit_id>.json` files, `obligations.json`,
then `manifest.json` written last. It is disjoint from custody, the approved
package, attached runtimes and the helper source directory. Existing output is
refused, never overwritten. Every output uses exclusive creation, flushing and
bounded reread. Failure preserves partial files, which are not a success report.
A partially written manifest is not usable: intake requires its exact selected
hash and valid schema. A late failure may leave complete inert bytes; no authority
or automatic resumption follows.

`obligations.json` records exact targets, used fixed-basis imports, remaining
`receiver_parent` imports, counters and manifest hash. It is advisory operational
metadata, not a new mathematical claim or trust token. Existing intake reads
only exact manifest-listed units and does not census this directory, so this
extra file does not change the existing intake format. Pass the returned bundle
directory, manifest path and SHA-256 to the existing `intake-baseline`, with an
explicit independently approved receiver parent. Its actual checking still owns
acceptance and must independently satisfy these imports; it need not trust the
advisory obligations file.

Units are ordered by exact dependency edges, using iterative topological sorting.
Every whole generated group is preserved. Target locators must bind their exact
unit/name/export; all selected names have a single exact symbol binding. Fixed
basis shadowing, conflicting versions, absent generated outputs and cycles refuse.
No global name-renaming or cross-environment reconciliation is attempted.

## Claim and cost

This seam removes an unnecessary **re-export of already held proof bytes**. It
does not remove receiving checks, solve mixed-theory import cost, invent concepts,
or prove useful growth. It enables ordinary new-concept development to reuse
preserved mathematics without treating inert custody as trust. The complete
workflow's full cost still includes selected support loading, exact custody
lookups, parsing, repeated existing bundle validation, writing, receiving checks
and any later authoring. There is no network-size or constant-time claim.
