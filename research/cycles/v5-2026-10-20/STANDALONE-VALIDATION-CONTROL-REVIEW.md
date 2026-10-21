# Standalone validation: independent harness and selector review

2026-10-21; core_growth. **GO for the specified source-only control launch
preparation.** No imports, tests, builds or selectors were executed during this
review. This is independent review of adaptive_audit's harness and root's two
selectors, **not independent review of my own three product source changes**.
Product assurance belongs to root and adaptive_audit's separate source review.

## Exact reviewed artifacts

| Artifact | SHA-256 |
|---|---|
| software/v5/standalone_validation/controls.py (32014 B) | e944888dbd137298163eaba666024bf620eb9aa0f11678d9edea6be3e9f74667 |
| STANDALONE-VALIDATION-CONTROLS.md | e25a740dee2de233885ad545c3b6c81d74c8177a4d56583818b24c07f0d4a850 |
| Select-StandaloneValidation01.ps1 | fadcd05aab8243107d62e0ab06cd4d03d489b3b2955ae56db80485dfb0b7e85a |
| Select-StandaloneValidationDistribution01.ps1 | 37431a1cdb7e7bd0e070c0ceb805ad76f783d8dbe295cab90b1ac4eebef8da06 |

The final three product hashes consumed by the harness/selectors are
ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881,
835d59809045c3e49f9d7e5483108f4034c591a3a82224e4155f4f7d0f6dcced,
8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595,
for pin_phase, receiver and imports_atomic respectively. These are consumed
bindings here, not self-authored independent product qualification.

## Control selector and source loading

Read-only inspection confirms the exact d3519be1 terminal-I114 map contains
114 logical entries and 114 distinct physical paths. The selector validates
all old path/byte/hash bindings and adds one runner, three fresh successors
and one new harness: **119 physical sources**. The two AST predecessors already
belong to that map; neither is added twice or executed as an old test suite.

The retained terminal-I selection b43f3eb4 supplies exactly 18 Python runtime
pins; adding the fixed source map gives **19 runtime pins**. Source-only review
confirms exact runner44a7bf1b, canonical cwd, fresh selection/output refusal,
isolated `-I -S -B` invocation and unchanged 45 CPU / 90 wall seconds,
384 MiB / two-process bounds. No native executable/prover input is selected.

The harness derives SOURCE from its snapshotted file, checks the fixed map,
copies/hash-checks 114 logical product files with only the three replacements,
then imports from those copied v5/portable roots. Product import origins are
checked before the suite. Selected-source bytes are preserved by the existing
runner's final snapshot/runtime checks. No installed state is reused or edited.

## Actual paths versus inert fixtures

The exact-class shells are explicit structural test instruments, not ordinary
constructor adoptions. They invoke real selected `_active`, `_check_install`,
`_check`, `_check_phase` and `_live` paths with genuine local TrustDomain files,
bindings, module origins and byte/hash pin reads. Counting wrappers delegate;
time injection changes only test clocks. No acceptance result is fabricated.

The fixtures have no I executable, no mixed native executable, no mathematical
handles, and empty import source inventory. Thus nonempty source-handle binding,
constructor setup and mathematical admission are **not** dynamically covered.
The unchanged bodies/order are separately AST-compared to two pinned predecessor
files, without importing them. Receive/process/network traps detect accidental
calls; they are not a hostile-code sandbox. No mirror or old suite is rerun.

## Ten-method review

The explicit SELECTED tuple names exactly ten defined methods; the future report
requires all ten, no skips/failures/errors and no forbidden calls. Read all method
bodies: original-body equality; standalone observation reduction; actual import
borrowing; tighter deadlines; live guards; independent nesting; copied-context
closure; pin/registration conflicts; deferred final failure; body-failure cleanup.

The expected counts are source-derived, not guessed timings: standalone's one
issuer gives first+final trust reads and one fresh read at each origin-tail guard
(four). Import's active guard reaches that same issuer directly and through
mixed ownership, so its two tail guards add four reads (six total). Both make
two actual trust-origin resolutions. Each distinct pin is read first/final only;
independent nested phases deliberately produce four reads for a selected pin.
No numerical CPU speedup is inferred from those counts.

Refusal ordering is consistent with selected paths. Live withdrawal latches
denial; binding/profile/CPU/owner faults are caught by real guards. Persisted
marker/adoption changes remain cached until the real final trust read raises,
before its next issuer callback, so independent I ownership is not newly closed.
The final-origin fault is injected after the real final resolution, outside the
issuer callback; no fake resolver return is claimed. Pin mutation occurs after
the initial real read and is detected at the final real read. Completion flags
distinguish body failures from deferred-finalization failure and assert correct
original mixed/import revocation. Copied views refuse even with inert guards.

## Later distribution selector: conditional GO

The second selector preserves all 114 logical entries and replaces exactly the
three reviewed paths. It retains builder eb1348f6, inherited assets/runtime,
120 CPU / 600 wall seconds, 128 MiB / two-process packaging bounds, and uses
fresh input/selection/install/output names. It stages only; it launches no build.

Its ControlsOutcomeSha256 argument authenticates the exact future outcome note;
it does **not** parse a PASS verdict. Root must first read and adopt a passing
actual outcome for these exact bytes, then supply its hash. This is the intended
human/root selection gate, not autonomous qualification by any hashed document.
No actual controls outcome or distribution adoption is established by this review.
