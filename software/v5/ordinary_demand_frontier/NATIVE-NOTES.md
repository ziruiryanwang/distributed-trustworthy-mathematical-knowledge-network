# Native scratch-authoring frontier

Status: source-only implementation for the local demand-frontier contract.
No compilation, test, native invocation, package edit, database access or Git
mutation was performed by this lane. Static source comparison is not runtime
qualification. The canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Source identities

Both files were copied byte-for-byte from `software/v5/ordinary_lean` to this
directory before editing. The initial copy hashes matched; the base hashes were
checked again after editing and remained unchanged.

| File | Base SHA-256 | Fresh source SHA-256 |
|---|---|---|
| OwnerConstruction.lean | `04f605717af3b907195756455c2ec645e37e20ce9897c0510f47d7da24895ed3` | `859386991c464c9410681596deaca5dce878b176c442e26838662ab0d308545c` |
| PortableOwnerConstructCommand.lean | `250a8dd1292c1dd5d228d69eaeb7abdbb5f0e9ad96c48a8b32d80203c27619b2` | `2e558269652f15a3afbfd9a34b72ee687ea14a205f97388f95fcdebc59ab45c2` |

## Interface and bounds

`OwnerRebind.Prepared` stays unchanged. The helper adds one optional last argument:

```lean
constructPrepared (owner : Environment) (prepared : OwnerRebind.Prepared)
  (limits : OwnerRebind.Limits := {}) (frontierLabels : Array Json := #[])
  : IO Constructed
```

The portable command retains the same command syntax and three expected identity
arguments. V2 requests retain their seven fields, original native limits, empty
frontier, ordinary group grammar and default successful-path diagnostics. V3
requires exactly those seven fields plus `frontier_root` and `frontier_labels`.
The root must be a lowercase 64-character hexadecimal identity; its protected
context/ancestry authentication remains the controller's responsibility.

V3 native limits match the coordinated Python bounds: 32 fetched groups, 32
targets, 4096 combined basis/frontier/group labels, 1 MiB header, 1 MiB per group,
and 4 MiB actual header-plus-group bytes. Existing codec, scan and kernel limits
are unchanged. Python additionally retains its acquired-byte/node/edge limits.
The public direct helper uses caller-selected limits as before; the tighter V3
limits belong to this portable wrapper.

Frontier entries are exact `[structured_name, export_id]` pairs. Names use the
existing bounded decoder, identities use the existing shape check, and names
are re-encoded for strict canonical-JSON ordering. This grammar contains only
ASCII arrays, unsigned integers and `$bytes` objects, so Lean string comparison
agrees with Python `E.name_key` byte comparison. Equal or descending keys fail.
Frontier names are inserted after basis names and before every fetched group;
duplicate names and basis/frontier/group overlap therefore fail even when the
conflicting group is never demanded. An empty V3 frontier is allowed.

The internal `payloadBytes` counter retains its old V2 value. It additionally
charges a nonempty frontier array. It is not the raw transport total: the wrapper
separately bounds and reports the actual header and all fetched group bytes,
including the frontier root and JSON field names.

## Meaning and failure behavior

A frontier label authorizes stopping authoring traversal at an installed name.
When that name is actually demanded, the helper requires both a kernel record
and an already visible frontend record (`skipRealize := true`). Both pass the
existing safety check, which excludes unsafe and partial declarations. A missing
kernel/frontend record fails in that invocation. The helper does not realize,
expose, reconstruct or retry a frontier declaration. The frontier branch precedes
the old kernel-existence shortcut, so that shortcut cannot bypass visibility.

This check says nothing about semantic agreement between the approved frontend
and the accepted receiver parent. The controller must authenticate each label's
exact name/export binding in the frontier and parent and authenticate the
frontier's exact import-plan prefix. The final candidate binder and actual-parent
native admission remain mandatory. A complete proof valid under that actual
parent may pass; a proof false there must fail even if it checked while authoring.

Unchanged paths include complete fetched group inventory/unit census, rejection
of partially existing groups, exact private names, missing-theorem signature
construction, actual new-group checking, and delayed command-state installation.
No durable anchor, receiver relation/schema or implementation identity changes.

## Remaining integration work

Root owns independent source review and any fresh finite build/runtime selection.
The proposed helper rebuild order is OwnerConstruction,
PortableOwnerConstructCommand, PortableConstructExportCommand,
PortableContributionExportCommand. Admission modules remain untouched.

Required controls include absent-flag V2 equivalence, V3 field/bound/order and
binding refusals, retained preparation, a missing visible native frontier name
with no fallback, and a deliberately mismatched frontend whose resulting proof
reaches final actual-parent checking and is genuinely rejected. A later real
finite-map use should demonstrate zero ancestor-evidence fetching below the Std
frontier. None of these controls has been executed by this lane.
