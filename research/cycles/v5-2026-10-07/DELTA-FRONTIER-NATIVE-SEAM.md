# Selective certification: actual v5 native seam

Source investigation for root's frontier contract; NOT selected implementation,
executed control, certificate or permission for a new runtime. The immediate
priority remains one actual module capsule followed by retained-work calibration.

This is the sole substantive delta-frontier proposal; the suggested alternate
CONTRACT filename is not a second specification. Root keeps the genuine
base-to-child recursive receipt and cold-admission gates: bounded native deltas
SUPPLEMENT that capability, never replace it with a narrower native-only release.
Receipt custody/acquisition (D18) still carries actual receipts; adding a delta
transport kind is a separately selected change, not an implicit extension of
that source assignment. Candidate ModuleIDs and group formats can remain;
availability of a particular proof form is separate advisory metadata.

## Existing seam, not a native-success report

`software/v5/modules/receipt/src/relation.rs::check_bytes` accepts bounded raw
JSON through the shared canonical parser, checks exact adopted foundation,
module summary/identities, authenticated imported group openings, exact parent
image/foundation/policy/rank, body commitments, raw-to-canonical correspondence,
native construction and local declarations. It returns a computed `Journal`
plus exact `parent_journals`. This is CONDITIONAL until every parent premise
is discharged. The guest currently calls real `env::verify` on each returned
parent, then commits only its computed journal. Native `receipt_native` does
not perform those cryptographic calls and cannot authorize imported premises.

`src/bin/module_host.rs::checked_receipt` already checks real succinct Poseidon2
receipt kind (not Fake/Composite), default verifier with dev mode disabled,
FULL application verification/no unresolved assumptions, and adopted
image/foundation/policy. Its public verify branch also compares exact journal
bytes. This is the actual frontier verifier to reuse. Saved JSON claiming
REAL_MODULE_RECEIPT_VERIFIED or native success is never a premise.

A minimally coherent fresh native host command would include the SAME relation
source and actual checker dependency, call `check_bytes` itself, and invoke the
actual receipt verifier on exact frontier receipt bytes within that command.
It would not request a native-success report from an arbitrary program or
reinterpret a persisted acceptance log. Its executable/source/runtime pins,
whole-operation supervision and same-call immutable input binding would be
owner-adopted, analogous to current admission/ReceiptVerifier. Adding relation
to the current host requires a fresh build and updated checker artifact; it is
NOT implemented merely by reusing host03, whose dependencies omit relation.

This native path broadens the receiver's trusted execution relative to portable
receipt verification. Matching source alone is not a proof that host-native and
guest targets implement identical judgments: pin actual native architecture,
integer/range policy, overflow-check settings, executable/dependencies and exact
instance profile, and qualify their changed-boundary refusals. Native host widths
must not silently enlarge accepted canonical numeric domains. The conditional
argument below includes adopted-native correctness, not only crypto soundness.

## Packet and acceptance invariant

Let F be a finite set of certified frontiers and D an ordered finite sequence
of uncertified delta witnesses. The packet includes exact frontier receipt
bytes, delta witness bytes, and a separately requested target ModuleID/summary.
Imported descriptors/openings/body demands remain in the existing witnesses;
no trusted remote flag is added. Receiver bounds the complete aggregate packet
before native work and charges its actual parse/check/receipt operations.

An owner-bound host keeps a private set A of exact journal BYTE strings:

1. For each supplied frontier, fully verify its real receipt against the adopted
   image/profile. Only its actual journal enters A. Reject duplicate/unused
   frontier material according to the selected canonical packet policy.
2. For each delta in order, call the unchanged relation on its exact bounded
   bytes. Validate its OWN computed Journal against the owner-adopted image,
   foundation and semantic policy, including a foundation-only zero-parent
   delta. Parent consistency is insufficient: relation input carries an image
   claim and the guest normally relies on external final receipt verification
   to pin its own image. The native host must impose that same profile binding
   explicitly on every delta. Its returned parent journals must all already belong to A, with no
   substitution by ModuleID alone, rank-only comparison, a digest claim, or a
   statement claimed by an unchecked later delta. Only then add its computed J.
3. The requested final target must match the last selected computed journal and
   independently requested summary. No handle or success authority is minted
   until all input binding, process closure and deadline checks complete.

Checking a delta before checking its parent membership is logically safe if
no conclusion is released before membership passes, but may waste resources;
the packet can prevalidate structure to reject clearly impossible order first.
The shared relation remains authoritative for computed parent references.
Topological order plus existing strict rank prevents circular self-support.

Derive graph edges, closure reachability, duplicate detection and unused-frontier
checks from the ACTUAL relation-returned parent journal bytes, not caller-supplied
edge claims. Every supplied delta/frontier must belong to the target's computed
closure under the selected no-extras policy. Charge and bound all submitted
bytes, nodes and edges even if later rejected as duplicate, malformed or unused.
Foundation-only deltas have no receipt premises; the adopted foundation is
their base case. Rank is not mathematical identity: ModuleID omits its exact
proof provenance. Consequently membership must use full exact journal bytes,
not merely matching modules, and alternate witness/rank instances must not be
silently interchangeable as parent conclusions.

Conditional soundness argument: assume correctness of the adopted native
relation/checker and cryptographic receipt soundness for the adopted image.
Induct on the finite processing order. Verified frontiers satisfy their module
judgments. Every relation-accepted delta is valid conditional on EXACT returned
premises, all of which are established by a frontier or an earlier induction
step. Hence each newly admitted delta, and the requested target, is valid under
the fixed foundation/policy. A control timeout, malformed packet, missing
premise or computation demand yields no admission. This is an architecture
argument, not a machine-checked soundness proof of Lean or the native checker.

## The no-ancestry boundary must be aggregate, not just depth

Each transferable delta packet must carry its COMPLETE uncertified dependency
closure back to genuine certified frontiers. An existing local cache may save
work only under explicit same-profile live verified evidence; an outbound
self-contained packet cannot omit that closure because its sender remembers it.
Depth alone is insufficient: bounded-depth high-fanout DAGs can still contain
arbitrarily many proofs. Bound at least total encoded bytes, unique delta nodes,
unique frontiers, total parent edges/openings/demanded bodies, parser expansion,
aggregate native CPU/wall/memory, receipt bytes and verification calls. Shared
nodes must be counted/processed once per operation, not expanded along paths.

With fixed receiver envelope B, successful cold receipt+delta verification
requires O(B) packet access and at most its enforced finite CPU/wall allocation,
independent of ancestral proof history BEYOND F, global corpus size or network
membership. This is a bounded-work acceptance guarantee, not a cheap completion
guarantee for arbitrary Lean reduction. Hard or oversized deltas may refuse even
when mathematically true. Timeout must be separately represented from falsehood.
Selected transparent bodies can be large or expensive; a frontier certificate
does not erase those semantic computation demands.

Composing more deltas grows the uncertified closure. When it no longer fits the
receiver's advertised envelope, contribution transfer needs a new seal at an
appropriate frontier, another affordable proof, or an explicitly larger owner
envelope. There is no indefinitely extendable cheap chain with fixed cold work
and no periodic cost. This is exactly where selective certification acts as
amortized proof compression, not as a source of mathematical authority by vote.

Externally distinguish `ACCEPTED_DELTA`, `INVALID_OR_UNBOUND`,
`RESOURCE_INCOMPLETE`, `MISSING_MATERIAL` and `NEEDS_SEAL` (or equally clear
typed outcomes). Envelope refusal is not a false-theorem claim; NEEDS_SEAL is
an actionable local policy result, not a promise that a funded seal exists or
that all nodes agree on one resource envelope. No receiver downloads below a
genuine verified frontier to repair missing uncertified material implicitly.

## Distinct authority classes and sealing

Local native-delta acceptance may support ordinary source authoring and further
bounded native-delta transfer, but must produce a DISTINCT `VerifiedDelta`
handle, not current `VerifiedModule` (which means a real certificate). Existing
ReceiptVerifier and cryptographic guest parent APIs must refuse such handles.
The packet's witness is what another cold recipient actually checks; the local
handle or saved JSON is not its proof. Receiving/custody/discovery may advertise
which proof form is available but offers never establish validity.

The current guest relation can certify ONE delta only if every referenced
parent has a genuine receipt. Therefore sealing a whole uncertified DAG without
certifying each intermediate needs a separately specified aggregate relation
that internally checks the DAG and exposes selected module roots, or a sound
repacking into a single module with identity consequences. It is incorrect to
claim current profile2 guest already compresses a native-delta packet for free.
The first operable conservative policy may certify the oldest/most reused delta
individually, reuse its receipt as a frontier, and advance outward. That removes
the relevant ancestry but pays ordinary certification for selected intermediates.
Batch sealing is a later architecture choice, not required to define acceptance.

Checkpoint/sealing decision remains explicit: first obtain a completed actual
base capsule, calibrate one retained proof segment under its selected finite
budget, then choose affordable real receipt stages. Do not interpret this note
as authorizing an old campaign restart or promising that a full receipt fits
the one-segment calibration allocation. A future packet-sealing relation/image
bridge needs its own relation and trust-profile review; current env::verify
continues to accept ONLY genuine matching-image receipt assumptions.

## Decision-relevant cost model

For a fixed valid target and receiver envelope, let C_D be receiver cost to check
its complete delta packet, C_R cost to verify a sealed form, and S additional
one-time cost to produce/distribute/retain that seal. Account for exact bytes,
CPU/memory/wall, proving failures, replication and freshness costs in consistent
units; do not add wall seconds to byte counts without an explicit valuation.
If n future cold users would each need this same delta, sealing is beneficial
in the selected scalar resource valuation only when n(C_D-C_R) > S, assuming
C_D>C_R and comparable semantics, selected bodies and endowments. Already sunk
authoring work cancels only if identical in both alternatives. Reusable cached
parents and warm verifiers belong in both comparator arms.

n and future reuse patterns are unknown; local usage frequency or predicted
benefit can trigger sealing heuristically, with funded budgets and no claim of
optimality or human-intention acceptance. A native frontier path can make cheap
experimentation usable now while concentrating expensive seals where measured
or modeled fanout justifies them. It does not by itself prove useful discovery,
exponential growth or globally affordable availability.

## Smallest decisive next implementation, if root selects it

After actual certificate availability, use one fresh host command that actually
checks a small delta over that real certified parent, returns a same-call live
delta handle, and rejects missing/wrong/fake frontier, changed target, modified
proof, extra uncertified ancestry and envelope exhaustion. One second delta
demonstrates bounded transitive closure without pretending it is already sealed.
Retain exact witness material for onward cold use. No broad new test campaign,
saved-success authority or fallback to replaying unlimited ancestry is needed.
