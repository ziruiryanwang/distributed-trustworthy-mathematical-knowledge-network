# Standalone mixed validation: three-source successor

2026-10-21; core_growth. Implements only STANDALONE-VALIDATION-SELECTION.md.
Source-only; no imports, tests, builds, installations, proofs or Git changes.

## Exact source basis and output

Basis: terminal-I114 `distribution-terminal-i-01-input.json`, prefix d3519be1;
the live terminal-I build and its five selected replacements are untouched.
Only these three fresh files beneath `software/v5/standalone_validation` change:

| Logical path | Original source SHA-256 | Successor SHA-256 |
|---|---|---|
| admission/pin_phase.py | c00e1259488415b390b651eab307a91ee5db1966a57f4c236ac054c2445bac21 | ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881 |
| mixed_claims/receiver.py | aa591a1829deff82576ba30af484ab560ee04900200fd79ac93c19a9c2c7bf7f | 835d59809045c3e49f9d7e5483108f4034c591a3a82224e4155f4f7d0f6dcced |
| mixed_claims/imports_atomic.py | e38ac52a888f354e8e878984397a5c93c82ac38284b9e6fc89051063537aa459 | 8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595 |

Predecessors: origin_phase/admission/pin_phase.py,
runtime_efficient/mixed_claims/receiver.py and interface_views/imports_atomic.py.
Read-only source diffs confirm receiver's old `_check` body is unchanged and
ordered identically in `_check_phase`; no mathematical or wire logic changed.

## Stable internal API

`phase(active, *, borrowers=())` retains independent default/nested semantics.
The optional exact tuple snapshots original owner identities, never peer data.
One `_PinPhase` owns pin records, borrower identities and its open lifetime.
Each `_PinView` has its own open lifetime and guard; no records escape closure.
Pin/expected-checker conflicts retain their original errors and comparisons.

`borrow_or_phase(active, *, owner)` borrows only when the current view and root
are open and `owner is original` for an explicitly registered identity. No
match means a new independent complete phase. A closed copied context refuses,
even with an inert active callback. Borrowing installs a short-lived view of
the same records; its pin guard invokes both the enclosing original guard and
the borrower's own guard. Entry and successful exit invoke both as well.
It performs no extra pin/trust/origin final sweep. Its view closes on all exits,
so a copied-out borrowed view refuses even if its enclosing phase remains open.

## Standalone call graph

`mixed._check(deadline)` closes the phase callback over exactly that deadline:
`lambda: self._active(deadline)`. With no compatible enclosing scope it enters
the existing origin -> trust -> pin transaction, calls the unchanged check body,
then completes all three finalizations before `_check` returns. Failure at any
stage reaches the existing mixed revocation path. All original guards remain;
added pin/final callbacks enforce the supplied deadline and original CPU cap.

No external operation is newly enclosed: the scope ends at `_check` return,
before receipt/native execution, data writes or live-handle promotion. Existing
pre/post-execution `_check` call sites are unchanged and remain separate phases.

## Already-enclosed import call graph

`import._live` captures only `self._origins[2]` as the permitted mixed borrower.
Its existing active checks reject owner substitution before body use. Original
I/A validation, mixed `_check`, source-handle/binding checks and final guards
remain in their existing order. Repeated mixed checks share this exact import's
phase, not an arbitrary surrounding caller's scope. No usable import result
returns before the enclosing pin, trust and origin finalizations complete.

If `_live_phase` succeeds but outer finalization fails, import revokes its
captured original mixed owner and closes itself; it never revokes a substituted
current object or independently owned I/A issuers. A completion flag confines
this new cleanup to deferred finalization failures. Original body-only import
failure cleanup remains unchanged; mixed-check failures still revoke themselves.
All exception paths restore enclosing independent context and discard records.

## Refinement claim and deliberate limits

Under fixed owner-controlled serialized local state, unchanged mathematical,
installation, identity, binding and conflict predicates are evaluated with
unchanged meaning/order inside the old body. This is **not equivalence of exact
resource-refusal timing**: added final guards can legitimately refuse a call
near its deadline/CPU cap. Disk observations coalesce within the existing
first/final sampling model, not hostile concurrent mutation/rollback protection.

Standalone repeated full trust reads per pin become phase-local first/final
reads plus the existing final origin-tail observations. Original live denial,
generation and binding checks remain; no lifetime trust/receipt/native cache.
Do not promise exactly two total trust reads or a numerical speedup. Import
borrowing avoids independent nested sweeps, but adds borrower guard calls.

## Review/control handoff

adaptive_audit received the stable API and hashes. Root owns later integration
and one separately selected changed-boundary test. Suggested controls: actual
standalone persisted/pin counts; registered versus wrong owner; default nested
independence; copied root/borrowed closure; supplied deadline; pin/checker
conflicts; withdrawal; final pin/trust/origin refusal and original-owner cleanup.
No previous mirror/control campaign is repeated or renewed by this source note.
