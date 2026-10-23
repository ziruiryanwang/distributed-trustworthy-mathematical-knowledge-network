# Minimal retained-foundation grammar repair

2026-10-23, `project_hook_design`. Canonical guard PASS. Source/data inspection
only: no Python import, compilation, test, native operation, owner opening,
SQLite/network call or Git mutation. Root owns overlay/selection; review pending.

## Cause and grammar justification

The failed preparation01 retained-header path used `E._uint(row[1], 6)` for
**foundation** inventory rows. That is the upper bound of a different grammar:
new extension-unit inventory allows kinds 1 through 6 and deliberately excludes
new axioms and quotient primitives. It must remain unchanged.

The existing foundation grammar instead includes kinds 0 through 7:

- `BootstrapSupport.lean` `inventoryRow` emits `.quotInfo` as kind 7, with
  quotient subkind type=0, ctor=1, lift=2 or ind=3.
- `OwnerRebind.lean` `checkBasisRow` allows `kind <= 7`, permits kind 7 only for
  the fixed `BootstrapProbe.quotNames`, then checks the actual inventory row.
- `portable_owner_request.py` preserves the 581 rows from the exact pinned
  foundation inventory; its theorem projection does not remove quotient rows.

The exact retained `B-contribution/owner-request/header.json`, already pinned
in the controls as
`84839df3270083460a2c4733b382fadc7ddfb433913dc0da5bd4f44dcf400ffe`,
contains 581 basis rows and exactly four kind-7 rows. Read-only inspection found
`Quot`, `Quot.mk`, `Quot.lift`, `Quot.ind`, with the corresponding 0,1,2,3
subkind details. These are legitimate existing foundation declarations, not
unproved external theorems or newly admitted axioms.

## Exact fresh successor and regression

`software/v5/ordinary_library_support02/retained_preparation.py` is the exact
predecessor except the single-character basis bound **6 → 7**. Read-back
comparison confirmed that no other source text changed. Hashes:

| File | SHA256 |
|---|---|
| Frozen predecessor helper | `f4c51f1a90a75eb153dda10c6c17b9a8eeeca1692275c176f70a15f8499a9bc6` |
| Fresh helper02 | `49e9550f9d1d231654ef120b7fac8194d9d6707690675c1f0baa96be6463ddb3` |
| Frozen predecessor controls | `ea988574466558c513e17a6e2f311fa1313cfab160c834c889bdee3de3685122` |
| Fresh controls02 | `fcc401ed42c01b6c8a8b842101a3dab3079c920353557b58bc55aa0107368720` |

The fresh `ordinary_library_support02/preparation_controls.py` retains the seven
groups and all original fixtures/refusals. Its positive retained-byte group now
explicitly checks the four quotient names, their exact portable symbol IDs,
subkind details, 581/4 census and recovered bindings. Its negative group repins
one quotient row changed to kind 8 and requires `INTEGER_BOUND`. The report
records the expected quotient regression map, not an invented runtime pass.

No native checking rule, extension grammar, foundation hash/identity, protected
parent lookup, candidate completion, admission, resource cap or profile changes
in this source repair. The helper only reconstructs names/IDs that still require
the selected protected-parent match; it grants no mathematical acceptance.
Failure01, its charges and all used support01 files remain preserved. This is
not a silent retry: root must select fresh source/overlay/output before execution.
