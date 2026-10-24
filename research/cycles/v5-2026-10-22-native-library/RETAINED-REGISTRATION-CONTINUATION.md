# Retained snapshot, fresh registration: narrow continuation

2026-10-24. Retained-registration agent. Source inspection and selected source
implementation only; no package installation, native execution, owner operation,
catalog mutation or saved-result adoption occurred. Root selected source work in
RETAINED-CONTINUATION-SELECTION.md after the initial source-only recommendation.

## Decision

Use the existing protected snapshot as immutable **input bytes**, while creating
a new operation, a new current-warrant request, one new live native correspondence
event and a new record-last commit. Do not reopen the failed operation, copy its
snapshot, change its metadata, or treat its saved correspondence as authority.

The requirement that a snapshot physically live inside the operation that commits
its reference is not a mathematical condition. An exact same-store pointer can
replace that layout assumption without changing the native relation. This is a
small storage/adoption seam, not general checkpoint recovery or support migration.

The earlier accepted initialization and library-intake roots remain intact. No
native helper compilation, mathematical readmission, source rebuild, snapshot
copy, or new expensive certificate is necessary for this repair.

## Inspected retained state

Failed workflow: `experiments/v5-local-checks/ordinary-reference-public-workflow-01`.
Protected source operation:

`97440ed1f77850e5b58a7256172246dc45efbded96ed160faef827e65b86874a`

Its original `CLOSED.json` says `LIVE_CORRESPONDENCE_CLEAN_BEFORE_COMMIT`.
`FAILURE.json` records `REFERENCE_OPERATION_FILE` at `PROTECTED_COMMIT`,
6.03125 native CPU seconds, no new catalog acceptance. The operation has events,
snapshot, supervision and the original four top-level metadata files, but no
staged reference record. The current records directory was previously audited
empty; this investigation does not manufacture a record from those files.

The prepared snapshot contains 389,559,024 artifact bytes, 650 modules and 3,250
parts. Its exact manifest identity is:

`71bc7058363c9972c71e7e560d70ccc467fc18cba4c8c93cdbb6c3bceae95f7b`

The old support identity is
`638fe7df42fa7f71c1648fe8a315561fdfc356eed32ce1bea51cdc122d6e51aa`.
The new source must generate a new support identity, not relabel that old one.

The existing store marker binds the installation, foundation, semantics,
implementation and quotas, not one support identity. Historical operation
reservations carry their own support identity; the census checks its syntax
without requiring current-support equality. A committed reference, by contrast,
must have the current support identity when loaded. Thus opening the store with
new support is compatible with retaining this closed failed history. It does not
constitute migration of any old accepted reference.

## Exact selected interface

The original-reference selection optionally gains:

```text
retained_snapshot = { operation_id: exact hexadecimal ID,
                      snapshot_id: exact manifest SHA-256 }
```

The original five fields remain the source context, targets, project-selection
pin, bundle-manifest pin and artifact-report pin. For retained input these must
equal the original operation's five fields exactly. The source operation must
be an original-reference operation in this same store, closed with an existing
clean original-registration reason. It must not itself be a retained-reference
selection. This deliberately rejects recursive reuse chains and unrelated
selection changes rather than inventing a general migration relation.

`store.retained_snapshot(grant, check)` requires a current live grant and returns
the existing `SnapshotView` after `snapshot_reopen.read_snapshot` validates its
exact manifest, source/replay metadata, module graph, allowed directory census,
artifact paths, file sizes and every artifact hash. The retained source operation
is not a warrant. Its old request and old native report are never inputs to the
new acceptance decision.

`bind_reference_inputs` requires either the grant's own snapshot, for unchanged
ordinary preparation, or precisely the selected retained source directory and
manifest identity. Its existing current-context checks, full request binding and
current-warrant collection still run. Fresh events are written only beneath the
new operation.

The existing reference record's `snapshot_manifest.path` can encode the source
operation. A dedicated parser accepts exactly:

```text
operations/<hexadecimal operation ID>/snapshot/prepared-manifest.json
```

It is not a general arbitrary-path allowance. Other record pins still require
their exact paths under the newly committing operation. No record field or
schema is added; the new support identity records this source-level behavior.

On reopening, the committed record is authenticated as before. Its own operation
reservation is checked against the current support, context and targets. The
selected origin must agree with the record's manifest path and manifest identity;
the source operation's same-store clean closure and matching selection are checked
again. The snapshot is then fully revalidated at that origin. Saved reference
metadata is interpreted only after this already-protected record has established
its authority; the parser does not become an alternate registration route.

## Safety argument and explicit premises

Assume the existing protected-owner model: the real owner lock is held; the
installation and selected source profile are authenticated; no hostile local
administrator mutates the protected state; the native checker/correspondence
relation and the existing request/report binders are correct for their stated
policy. Hash collision resistance supplies exact-byte binding, not mathematical
truth.

1. The source locator admits only a closed original-reference operation under the
   same protected store, with the same approved selection. Its snapshot is
   independently checked as exact retained data. No old acceptance is inferred.
2. The fresh request comes from the current owner context and current support,
   binding its selected unit bodies, targets, snapshot identity and basis. The
   existing binder rechecks every current warrant.
3. The unchanged native process reads the fresh request and retained replay
   input. Its output must be from the current clean supervised event and must
   satisfy the exact full request/report correspondence relation.
4. The controller validates the same snapshot again after that live event.
   The private commit rebinds the report, current warrants and actual fresh
   event files; the selected origin is checked again before its pin is recorded.
5. Only atomic record publication makes the reference available for later reuse.
   The retained source remains data custody throughout. A fresh process cannot
   call the private commit with a saved report under the supported API.

Therefore changing physical ownership of snapshot bytes introduces no new
mathematical premise into acceptance. It does introduce a retention dependency:
the origin snapshot must remain for the lifetime of every referencing record.
No deletion or garbage collector exists in this change. Any future collector
must trace these pins before reclaiming an old operation. Different operation
identities do not imply independently hosted custody or failure independence.

Failure of snapshot validation, support/profile checks, current warrants, live
matching, cleanup or record publication still refuses or conservatively reports
an uncertain commit as in the predecessor. No automatic retry or budget renewal
is introduced. The old failure remains failed even if a new operation succeeds.

## Resource and usefulness boundary

The global store census counts the retained operation and its artifact bytes once,
whether zero or several new references point to it. The new operation contains
fresh event/record metadata, not another artifact tree. Per-operation and total
quotas remain unchanged; reservation remains conservatively sized as before.

This avoids copying 389,559,024 artifact bytes and avoids repeating successful
init/intake. It does not remove native correspondence cost or whole-snapshot
hashing: the existing loader still performs O(selected artifact bytes) work.
Repeated hashing and repeated profile validation remain real receiver costs,
not constant-time assurance. No runtime speedup has been measured here.

The small repair makes ordinary-library adoption operable without enlarging the
cryptographic architecture. This example still demonstrates interoperability,
not useful mathematical growth relative to an equally capable ordinary package
workflow. Broader growth justification remains the controlling next priority.

## Implemented source and cross-review

Only this agent's new source file and this checkpoint were written:

- `software/v5/ordinary_reference/reference_store03.py`: 76,686 bytes,
  SHA-256 `5ad587b779eb0b81958706c3df17f108c330bd618379b4bcd2c289f6a3e6dc9f`.
- Its predecessor `reference_store02.py` remains unchanged at
  `bc15b9dd7c4386f05f58c36b9cd01887f709c6a75b6cb8418eec6309559080b1`.

The source was copied through apply_patch, then altered only at the described
selection, origin, record-pin, binding and loading boundaries. AST parsing passes;
this is syntax evidence, not execution or a test of the trust relation.

This agent also independently read root's complete predecessor/successor diffs:

- `reference_registration02.py`, SHA-256
  `9225d68660555e93266a7f0d35a067f76dceaad772520e90305b6f4d03782b19`.
- `ordinary_reference_package/owner02.py`, SHA-256
  `295fbb25f8f41ebd2b647ce02bb833d60cd039d4056737fbcf9c07ef918bc2f1`.

The controller/CLI require both retained IDs together and restrict them to local
registration. The retained branch bypasses resolution of original project paths,
as it should: selected bytes are already protected and revalidated; the original
working directory need not survive. Bundle inputs and the current context remain
checked. The fresh request, live supervision, report binding and record-last
flow are unchanged. No source-level mismatch was found in those two diffs.

An independent reviewer must still clear the integrated store/controller/package
boundary before root selects any runtime. A focused continuation should test the
remaining public path, not rerun the successful prefix. No test, native process,
catalog operation or package assembly has been launched by this agent.
