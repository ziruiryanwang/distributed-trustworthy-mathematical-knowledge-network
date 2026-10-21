# Trust-validation phase: focused control plan

2026-10-20, adaptive_audit. **Source-only prospective plan; no implementation or
runtime selected by this document.** Root selects the two-file seam: extend
`admission.pin_phase.phase` and `admission.trust`, without changing
`MixedImportSession` or the mathematical relation. Core_growth owns the candidate
implementation; core_release independently reviews its principle/source contract. This
plan owns the disjoint changed-boundary controls, not another diagnosis or broad
regression campaign.

## Exact basis and required semantics

The current installed map is
`experiments/v5-local-checks/distribution-body-custody-01-input.json`, SHA-256
`995525c5cbf2746718cbf583a3e3e401bc56c2f88d1cef8664ffeb1b644454be`.
Relevant selected predecessors:

- `software/v5/runtime_efficient/admission/pin_phase.py`:
  `4b302fc472ced49a7681deb019c20a92674353d9adf109949cba7d3034b0deca`.
- `software/v5/trust_withdrawal/admission/trust.py`:
  `a60fd123845c7cd732967f995363b3132ebab1522cd90870ab728e6a54dd83ee`.

Both files and relevant existing pin-phase, withdrawal and synchronous import
control paths were read. Prior controls are reference material; no historical
test suite or used output is rerun or modified.

The proposed optimization shares only successful persisted-adoption validation
inside one existing trusted, synchronous, non-yielding phase. The first touch of
each exact domain performs the unchanged full `_read` and exact raw/directory/
record comparison. The successful-exit trust sweep performs fresh full reads
**after** the existing final installation-pin sweep. The original active callback
must run after those reads, so their cost cannot evade deadline/resource checks.
Different domain objects, even for the same persisted path, have independent
records. Nested scopes have independent caches. Nothing survives scope exit.

Every original exact-domain, original registered-binding and sticky-denial check
still runs at every relevant call; owner profile, origin, resource and deadline
callbacks remain in place. Local `withdraw` must immediately set denial and must
not be prevented by the optimization. Persisted changes need not be noticed at
every repeated call inside a stable-owner phase, but must prevent successful
phase exit when present at its final check. This changed sampling boundary is
explicit: not hostile-concurrent-filesystem defense or transferable authority.

## Real-fixture and counting discipline

Use fresh finite fixture directories only below a separately selected controls
output. Construct real `TrustDomain` records with a syntactically valid inert
support manifest; create real bindings through `bind`. These are local policy
fixtures, not adopted mathematical executables or proof evidence.

Count calls by wrapping the actual selected `trust._read` and delegating every
call to its original implementation. Do not replace its return values or mock
`_directory`, `_ordinary`, raw-byte comparison, marker detection or codecs in the
positive/counting cases. Count real directory/record observations indirectly
through `_read`; elapsed time is not an oracle. Provisioning/open/bind reads are
recorded separately, then reset the measurement counter before the tested phase.

The principal count control uses an active callback that only counts calls and
checks a deterministic resource/deadline guard. With 17 explicit checks of one
domain, outside-phase calls require 17 real reads; one successful phase requires
one first read and one final read. The selected implementation installs the trust
scope before the unchanged original phase-entry callback, so a composition whose
active callback checks that same domain also requires exactly two reads. The
controls include that entry callback rather than excluding its cost. This is two
reads per touched domain per successful phase, not per whole public operation.

No sleeps, native executable, receipt verification, network, service, proof
production, timing benchmark or large allocation is needed. A class-preserving
socket/subprocess guard may fail forbidden calls; these synchronous controls do
not need an asyncio loop. Test failures and deliberately tampered inert fixture
bytes remain preserved.

## Selected control groups

| Group | Required observable result |
|---|---|
| Real repeated-domain reduction | 17 ordinary valid checks produce 17 `_read` calls outside a phase; the same 17 inside one successful phase produce exactly two, with identical identity results. Check at least two registered bindings of that domain, so caching is not accidental binding aliasing. |
| Domain-object separation | Two domains with equal support IDs but different paths/IDs each receive first/final reads. Two independently opened domain objects referring to the same adoption also each receive first/final reads. Neither path nor support hash merges authority registrations. |
| Per-call binding/type guard | After a successful cached check, wrong-domain, unregistered and manufactured binding values still refuse. A valid original binding remains usable unless an actual denial occurred; do not invent a new latch for the old unregistered-binding error. |
| Outside-scope freshness | Two successive successful phases read twice each; a subsequent ordinary check reads again. A changed adoption or persisted marker between phases refuses on the next ordinary/first phase read. No new phase revives a denied object. |
| Independent nested scopes | Outer first + inner first/final + outer final give four real reads for the same domain. Inner body failure restores the outer scope and cannot leak an inner successful result. If inner validation observes tampering and latches denial, the outer cached call must refuse immediately. |
| Adoption change and object identity | After first success, modify actual adoption bytes, or replace the record with a different filesystem identity, in a controlled fresh fixture. Successful exit must fail and latch denial. Exact-byte restoration afterward does not revive that object. Separately alter the domain's expected snapshot fields to ensure cached hits cannot silently accept changed in-memory authority. |
| Persisted withdrawal | Place a real empty/partial `WITHDRAWN` marker after first success, without calling `withdraw`. Exit must fail and latch. Also create the marker during the final installation-pin callback: trust finalization must occur later and catch it. No claim of immediate detection at every cached disk-free call. |
| Immediate local withdrawal | Call real `domain.withdraw` after a cached success. A subsequent cached check refuses on sticky denial; exit cannot report success. Marker content must match the original adoption. The optimization must not intercept withdrawal before denial is set. |
| Exception and first-read failure | A body exception propagates and discards scoped state; the next ordinary check is fresh. A missing/malformed first-read fixture refuses without caching success and latches where the unchanged `_current` contract requires. Restoring test bytes does not silently restore that denied domain. |
| Original active/resource guards | On a cached pin/trust path, make the deterministic original active guard expire; both cached-hit and final-exit paths refuse. In a final-read wrapper, advance the guard's synthetic clock only after the real `_read` returns: the post-read active callback must detect the expiration. Original deadlines, budget objects and call ownership must not be replaced or renewed. |
| Finalization-set discipline | If a final active callback attempts first touch of a previously unseen domain, the finalized set must not silently expand or skip that domain's fresh exit read. Require the candidate's explicit fail-closed contract and error, not accidental dictionary-iteration behavior. Existing touched-domain callbacks must not recurse into unbounded real reads. |
| Pin-phase integration preservation | Exercise the same phase with one real small-file pin and one real trust domain. Both have first/final checks; late pin change refuses and never promotes the phase. Verify ordering with an event trace, and source-check that the existing synchronous import seam and original active/deadline call sites are unchanged. No await, native/network dispatch or publication is introduced into the phase. |

Some rows may be subcases of one test method; the final explicit method list and
expected counts must be frozen after the private API is finalized. No result is
accepted merely because a test count is large. Any test that injects an I/O error
must label that injection, and retain separate real-I/O positive/tamper controls.

## Outcome and implementation gate

Before execution, pin the two fresh product successors, focused control source,
runner and complete required import map. The current 114-map basis plus two
replacements can be staged without importing obsolete logical-path predecessors;
an exact smaller dependency closure is also acceptable if reviewed. Templates,
old runs and the real trust domains from Mirror01 must never serve as mutable
fixtures. Only root may select the eventual finite test envelope and launch.

The control result must record each selected method, failures/errors/skips, actual
`_read` counts by domain and phase, active-callback trace, exact source identities,
zero native/network/proof calls and the inert policy boundary. Audit full logs,
Job closure and known aggregate CPU separately; never count nested CPU reports
as disjoint. A deterministic reduction establishes eliminated validation reads,
not measured end-to-end speedup or successful mirror contribution.

No installation, new mathematical trust adoption, repaired mirror runtime,
larger budget or release claim follows automatically from this plan or its future
finite controls. The failed Mirror01 and all used sources remain unchanged.
