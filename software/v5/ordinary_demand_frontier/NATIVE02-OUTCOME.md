# Native02: checked positive capability; suite incomplete

2026-10-28. Independent saved-data/source review. No product import, database
open, native execution, rerun, Git or old-evidence modification occurred.

**The real V3 positive contribution is checked under its actual parent. The
three-case fixture nevertheless FAILED on a harness proof-shape assertion.**
Neither the false-parent nor missing-name case ran. Preserve that distinction;
this is not a passing safety suite or final-v5 qualification.

## What actually completed

Run: `experiments/v5-local-checks/demand-frontier-native02`.
All four live/snapshotted source pins, 164 external pins and ten saved compiled
frontend pins independently match. The three contribution results' evidence and
preview sizes/hashes match their saved files. All four native admission workers
exited zero, reported their expected checked units and closed/reaped cleanly.
There are exactly four admission-call directories and four operation directories.

| Step | Checked content | Accepted local root |
|---|---|---|
| basis | 456 units / 581 names | `98a16868395176d32c862058a8a201b78c05f7d3f28bb247a1b497e4c7da3059` |
| F | `Base.c : Nat := Nat.zero` | `90825f1b8218c08af43335b1692e8b3a7918c84732bf1a450ef359484c20fefd` |
| P | `Above.d : Nat := Nat.succ Base.c` | `d0b4bcfa16e72ec840e52aa0b31ecd94b3457e7bd717c1d34b1f2bff0b57453c` |
| positive | `Above.d = Nat.succ Nat.zero` | `eb70c84911a9d9ff7e9e99cd6b137bb463f330a32756ca2833a8d1bbde9d3a1b` |

The positive REQUEST and V3 header bind parent P, frontier F, one acquired
Above.d group and the exact Base.c frontier export. Its single construction log
reports `checkedUnits=1` and `CONSTRUCTED_READY_FOR_AUTHORING_INSTALL`.
The trace records only Above.d's 1283-byte evidence and the new theorem's
2478-byte evidence; it does not fetch Base.c evidence at the frontier.
Approved compiled OrdinaryProducer supplies Base.c's semantics. Thus this
demonstrates stopping the acquired-evidence traversal at the selected frontier,
not eliminating necessary semantics or making arbitrary imports free.

The final admission worker's input unit equals the saved theorem unit exactly;
its parent module is the module for P and its worker report checks one theorem,
FrontierPositive.correct. Final acceptance is separate from scratch authoring.
All three authoring processes and the alternate-frontend compilation succeeded
with clean closure. The alternate was built but never used by a negative case.

## Why the harness failed

The generated source says `:= rfl`. Saved theorem type is exactly
`Eq Nat Above.d (Nat.succ Nat.zero)` and its proof is exactly `@rfl Nat Above.d`
(universe successor zero). The harness required the literal constant `Eq.refl`
at the proof head, so it raised `FRONTIER_NATIVE_EXACT_REFLEXIVITY_PROOF` after
the contribution had already returned checked acceptance.

The positive unit imports rfl at export identity
`3283177d544594fb6194cdbb21b5aa4b6fff29a5dbf2b5130dc21a185e254dd9`.
The header's basis entry has exactly the same universe-parameter count, type
and body as the pinned foundation seed's rfl declaration. That declaration has
type `{A : Sort u} -> {a : A} -> Eq a a` and body
`fun {A} {a} => @Eq.refl A a`. Pinned Lean Init/Prelude.lean:343 states the same
definition. The basis worker includes rfl among its 581 checked names.
This is an existing definitional alias, not an axiom, an alternate theorem
statement, or a checker discrepancy. Under P, Above.d reduces to successor zero.

The original test failure stays recorded. Its positive-OUTCOME.json was never
written, and its later root-inventory/parent-unchanged assertions never executed.
This audit establishes the exact positive saved native input/parent/output chain;
it does not pretend those unexecuted harness assertions passed or open the database
to reconstruct a wider state audit. False-parent and missing directories are absent.

## Costs, closure and preserved bindings

Outer status COMMAND_FAILED, child exit 1, no termination request, zero final
active processes, job closed, child reaped, empty cleanup and owner-close errors.
Elapsed time is 58.5762007 seconds; outer Job CPU is 23.03125 seconds and outer
wrapper CPU is 0.65625 seconds, totaling 23.6875 known CPU seconds. Nested
supervision figures are included in the Job scope and must not be added again.
The original 420-wall/260-Job-CPU/2048-MiB/eight-process allowance was not renewed.

| Evidence | SHA-256 |
|---|---|
| selected native02 configuration | `d0e2e7ab4f6eae8234a8161356768133677f4aa95e7740ef875bf1b75a7eb0b9` |
| outer RESULT.json | `2fd85217844d559a6a7f11376fd610453e24810c2d14daf7843f0836c3aee300` |
| workflow OUTCOME.json | `b7c325064c378a137c55d182ebe18190e4494ddb19642138d7bb20f5b525f277` |
| positive RESULT.json | `db978c788563580ed9a36a1fd1e8880c6b271575c4abdebb21fdb41e904619fc` |
| positive evidence | `2bac06bc8c709d5802e31c441e7cb9f5b6b3fb6976dfb4a42ea97bdb513a4399` |

No passed setup needs repetition. A separately selected finite continuation can
reuse the closed fixture's actual P and compiled alternate for the two genuinely
unrun outcomes, preserving all prior output and charges. Its proof-shape check
must recognize the exact verified rfl alias without weakening statement, parent,
native-arrival or refusal checks. That continuation is not selected by this audit.
