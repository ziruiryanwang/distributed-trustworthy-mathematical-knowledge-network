# Proved guest-work reduction: smallest justified next seam

2026-09-30 UTC. Source-only decision by `/root/diversity_review`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Owned checkpoint only; no product edit, import, build, execution, certificate,
network operation or runtime launch. Existing used sources and evidence remain
frozen. This is a prospective design decision, not an optimization result.

## Decision

**Do not replace the delivered checker image now.** The strongest narrow
source-backed candidate remains the authenticated Value-to-owned-typed-row
handoff already identified in
[PRODUCER-NEXT-SEAM](../../../experiments/certified-collection-01/PRODUCER-NEXT-SEAM.md).
This note does not count that proposal as a new discovery. It sharpens the
implementation boundary, alternative comparison, equivalence obligations and
image-migration gate needed before paying for it.

For a separately selected successor, first remove only the normalized JSON
buffer and lexical reparse between structural authentication and native DAG
construction. Reuse the existing Nanoda construction and finalization bodies;
retain the initial Value parse, strict relation schema, structural digests,
derived axiom policy, all selected proof/Prop checks, journal contents and real
parent-assumption discharge. Preserve the normalized-length limit with an
exact counting serializer. Do not silently combine a new raw parser, hash
format, foundation snapshot, checker policy, collection size or bridge.

The candidate removes real guest computation, not merely an enclosing host
overhead. **The available evidence does not establish that it removes a
material fraction of trace work.** No numerical speedup follows from seeing
two parses in source. The first consequential decision is therefore a bounded
execution-work falsifier under a newly built image, after representation
equivalence review; it is not another full certificate campaign.

## Why this addresses the central cost, without repeating attribution

Root's adopted
[completed public-cost decomposition](PRODUCER-PRIORITY-FROM-ACTUAL-COSTS.md)
is the authority for the actual 122-stage campaign and its CPU arithmetic.
Segment proving dominates that particular measured producer workflow; removing
only non-stage overhead cannot yield its proposed large saving. This review
does not recompute or replace those costs, terminal samples or charges.

The relevant distinction is:

```text
host preparation/elaboration optimisation -> may reduce preparation cost
guest computation optimisation           -> may reduce authenticated trace work
fewer trace rows/segments                 -> may reduce expensive proving work
full marginal-cost comparison            -> decides actual economic benefit
```

The last two arrows are empirical obligations, not algebraic identities.
Padding, page work, assumptions and backend costs can prevent a linear mapping.
Cheap native execution does not make its proved trace cheap. Conversely, an
optimised native Lean elaboration performed outside the guest does not itself
shorten the guest's already observed segment computation.

## Exact source-backed path and edit seam

Paths in this section are under
`experiments/certified-collection-01` unless stated otherwise.

| Existing path | Actual work | Proposed boundary |
|---|---|---|
| `guest/src/relation.rs:238,253` | Parse metadata and each raw line as `serde_json::Value` | Keep unchanged in the first seam |
| `relation.rs:114-156,261-262` | Validate schema; clone transformed Values and referenced hex digests; construct canonical structural encoding | Keep unchanged initially |
| `relation.rs:240-241,314-316` | Serialize authenticated Values into aggregate normalized NDJSON and enforce its 4 MiB cap | Count exactly the same serialization, but do not retain the text |
| `relation.rs:324-332` | Derive Config only after authentication; call text parser | Derive the identical Config, then feed owned typed rows |
| `build-01/project/checker/src/parser.rs:547-550` | Typed JSON decoding inside private `go1`, then construction match | Separate decode from apply; expose a constrained owned-row entry |
| `parser.rs:550-887` | Build DAGs/declarations; enforce native insertion/index/config conditions | Share the existing match bodies, not a second implementation |
| `parser.rs:402-452` | Final checks, name cache, constructor membership, recursor association and ExportFile assembly | Share one finalization body |
| `relation.rs:333-351` | Native census/name binding, selected role checks, actual proof checks and parent Prop checks | Keep unchanged |

The actual checker used by the assembled image is the copied checker under
`build-01/project/checker`, not an arbitrarily newer upstream checkout.
The path above must be specified against that exact pinned source.

The parser's `ExportJsonObject`, `ExportJsonVal`, metadata types and BackRef
are currently private. The minimal extraction is conceptually:

```text
old go1(line) = decode_json(line); apply(decoded_row)
new entry    = apply(decode_authenticated_value(value))
both         = same Parser state transitions; same finalize
```

`apply` must receive parsed data, never caller-supplied native pointers,
ExportFiles or allegedly checked declarations. The adapter belongs inside the
selected library/guest trust boundary. Its API need not expose Nanoda's private
row representation to network callers. Exact visibility, ownership and Rust
lifetimes still require a reviewed implementation; this note is not a claim
that `serde_json::from_value` compiles unchanged for every borrowed row type.

Authentication finishes before Config is derived because the permitted-axiom
list depends on the complete authenticated declaration sequence. A streaming
native builder cannot simply accept an unverified provisional whitelist.
The narrow design retains bounded owned typed rows until that policy exists;
it consumes/drops each original Value after authentication rather than retaining
both whole Value and typed collections. Whether this is cheaper in memory is
unmeasured and is a release-blocking gate, not an assumed benefit.

## Alternatives and why they are not the first selected redesign

| Alternative | Source-backed opportunity | Extra correctness/operability cost | Disposition |
|---|---|---|---|
| Direct transformed-STRUCT02 encoder over the existing Values | Avoid cloned transformed trees, cloned field-name Values and cloned referenced hex strings in `transform`/`digest` | Requires byte-for-byte canonical-encoding equivalence for every admitted schema shape | Separate second seam if the narrow handoff fails to offer adequate leverage; not bundled invisibly |
| Direct raw typed parse plus authentication | Avoid initial generic Value allocation as well as text round-trip | Changes duplicate-key/unknown-field/flattening/alias behaviour; needs a stricter owned relation schema than Nanoda's existing types | Defer; substantially more semantic churn |
| Memoise `native_name` hashes by native Name pointer | `relation.rs:205-211,337` recursively rebuilds/re-hashes prefixes for each declaration name | Cache validity must be tied to this immutable export and preserve depth checks, exact STRUCT02 bytes and native name binding | Smaller isolated function-level candidate, but no saved phase attribution establishes material leverage; do not advertise it as the dominant fix |
| Preconstructed native fixed-support environment | Avoid some support DAG/declaration construction | Exact environment contents, remapping, duplicate conditions, construction invariants, memory/page cost and new image adoption | Larger redesign; no nonexistent repeated support-proof loop is available to remove |
| Remove foundation or output checking | None justified for new outputs; support proof checks are already not in `to_check` | Weakens the acceptance relation or invents a saving for a loop absent from source | Reject |
| Larger or dependent batches | May amortise shared construction/proving work when suitable independent work is available | Changes `MAX_MEMBERS`, journal/parent selection bounds, scheduling and possibly output-reference rules | Not a small decoder optimisation; existing max-two batching is already measured |
| Speed native Lean source elaboration/search/controller scans | Can improve another part of a complete workflow | Does not directly remove the already dominant proved segment work | Evaluate for its own demonstrated bottleneck, not as the main proof-cost answer |

The native-name memoisation possibility is a source observation, not an
approved code cut or benchmark. Merely having fewer hash calls does not give
a percentage of total execution rows. Caching a name hash without retaining or
proving the relevant depth invariant could bypass the old recursion guard.

The direct encoder, if later justified, should initially emit the same
per-record canonical byte buffer rather than requiring an uninspected streaming
SHA API. It may represent digests as 32 bytes internally, but the authenticated
encoding must still emit the exact old `s` tag, length 64 and lower-case
hexadecimal UTF-8 bytes where a reference is a string. Replacing those fields
by 32 raw digest bytes changes mathematical commitments and is **not** an
equivalent optimisation. Schema object keys remain lexically ordered; domain
prefixes, lengths, scalar widths and UTF-8 byte counts remain exact.

Saved collection evidence already shows that AB uses 17,301,504 padded rows
and 66 segments versus the same-image singleton sum of 25,427,968 padded rows
and 97 segments: a 31.95876289% padded-row saving. This is prior execution-work
evidence, not a new batch result or proof-CPU/growth improvement. The current
public child has a saved 40-segment snapshot, but its snapshot marker does not
report total/nonpadding rows or instructions. Do not infer an exact row count
from 40 times a guessed uniform segment size or compare it to a different arm
as though they were a matched optimisation measurement.

## Formal acceptance and representation obligations

Let `V(P)` be the existing initial Value parsing and structural authentication
of raw packet `P`; let `S` be the old JSON serialization with newline framing;
let `D` be the old Nanoda row decoder; let `B` and `F` be its construction and
finalization; let `C(P)` be the Config derived by the unchanged relation.
Define old and candidate checking on the same selected input:

```text
E_old(P) = F(B(D(S(V(P))), C(P)))
E_new(P) = F(B(A(V(P)),    C(P)))
```

The required adapter congruence is `A(v) = D(S(v))` on every structurally
admitted row, where equality preserves field values, ordered sequences,
variant/BackRef identity and construction transitions. It is not equality of
allocation addresses. For positive complete inputs, exported Names, Levels,
Exprs, declaration roles/order, universe lists, mutual blocks and Config must
have the same relevant observations, and the old/new selected checker results
must agree. No old mathematical/schema/policy refusal may become acceptance.
For the proposed equivalent seam, old admissible inputs must not be rejected
merely because the new deserializer changes syntax interpretation either.

The acceptance relation includes at least these obligations:

- Same raw frame/header/packet/line bounds, UTF-8 and line handling, exact
  metadata, tag/index fields and shape checks. Count exactly `S(V(P))` including
  newline bytes and preserve the old normalized 4 MiB bound; do not assert it
  follows from the raw bound without an actual implication argument.
- Preserve current initial Value duplicate-key behaviour before adaptation.
  The first seam must not secretly replace that parse by a raw typed parse.
  Unknown fields and aliases must not be accepted merely because Nanoda ignores
  them. For example its `Thm` type at `parser.rs:330-338` omits `all`, whereas
  the relation authenticates and constrains `all` at `relation.rs:308`.
- Exact unsigned-number validation, integer conversions/widths, string byte
  limits, Unicode/escape meanings, binder/safety/hint variants and ordered
  arrays. JSON key order is not semantic; sequence/universe order is.
- Exact contiguous DAG indices, forward-reference refusal, native duplicate
  insertion checks and native BackRef checks. Do not independently rebuild a
  looser parser. Preserve present pointer/index semantics rather than slipping
  an unrelated parser repair into an optimisation.
- Same support/reserved-name commitments and ordering, declaration census,
  rendered-name collisions, selected parent/output roles, distinct interfaces,
  fixed-vocabulary type policy, and output self/cross-member reference refusal.
- Identical derived axiom allowlist and fixed Config flags, including disabled
  nat/string extensions and `unsafe_permit_all_axioms=false`. Native support
  construction is not permission to check no new proof.
- Same actual `check_declar` calls for selected parents/outputs, same parent
  `is_prop` checks, full checked/native-name census, constructor membership,
  inductive-to-recursor associations and finalization.
- Same foundation, rank, ordered output interfaces and SHA-256 of **original
  raw packet bytes**, not the counted normalized representation. Main still
  authenticates each distinct selected parent journal with `env::verify`, and
  final acceptance still requires real discharge of every assumption.

The semantic obligation is separate from resource refinement. A candidate
with the same eventual answer but worse peak memory or unbounded row retention
is not qualified for the existing bounded workflow. Old-invalid refusal
diagnostics need not have identical private Rust wording unless the public
contract requires it, but the tested stopping boundary must not be relabelled
from syntax failure to actual proof rejection or vice versa.

## New image, unchanged journal layout, real migration

The current adopted image is
`ccaf83d7890224f08ba9cb53c2fb25163a7867fecf94aa8bc5338db69b349b19`.
Any compiled guest/library change requires a new image, new exact build/input
map, review/adoption, package assets and installed/profile bindings. This holds
even when the mathematical relation and journal layout are intended to be
unchanged. Never relabel an old image ID, receipt, seal or outcome.

For a parent-free same-packet comparison, the new journal should have the old
length/magic/profile version, foundation, rank, member order, interfaces and raw
packet hash. Only its deliberately new image field differs. This is a
prospective comparator, not permission to edit a saved journal. The existing
format puts image words at bytes 12..43 inclusive; a comparison may decode the
fields and explicitly compare all non-image fields.

Parent compatibility is not automatically inherited. `journal.rs:51,88`
requires each parent journal's image to equal the selected child image, and
`main.rs` verifies that same image. Therefore an old-image parent cannot
authenticate a new-image child under the existing relation. Options are:

- Keep the old profile/receipts available and certify new parent-free work in
  the new profile; this initially yields disjoint reuse lanes.
- Recertify selected useful old parents under the new image, paying for
  available packet/source reconstruction and their relevant ancestor work.
- Separately specify, review and qualify a cross-image bridge. None is
  implemented or authorised by this recommendation.

Do not add an image allowlist and assume that resolves the bridge theorem.
Cross-image acceptance must bind each parent to a deliberately adopted
semantically adequate relation, exact foundation/interfaces and authenticated
receipt, with well-founded descent and real assumptions discharged.

There is also a direct search migration cost: the current
`product-local/certified-diverse-peer-source-04/cert_index.py:154-158` computes
the discovery namespace from `profile_id`, **image words**, foundation and
discovery version. A new image changes that namespace even if interface hashes
stay equal. Existing advertisements, postings, store configurations and cursors
cannot be silently carried over. Preserve old stores; any explicit reindexing,
new announcements, multiple-profile query or translation costs must be included
in adoption economics. A compatible mathematical commitment is not an already
compatible catalogue entry.

With one common measured resource unit and `N` future equal-opportunity
contributions, a necessary economic condition is:

```text
N * (C_old_marginal - C_new_marginal)
  > C_build/adopt/qualify + C_migrate/recertify + C_added_maintenance
```

This condition is useful only after the marginal difference is actually
positive and measured with the same endpoint/opportunity. At huge scale,
recertification can be impossible if the needed old packet/source is no longer
available. Keeping two lanes also has a maintenance and search-fragmentation
cost. No finite break-even population is established by present evidence.

## Finite prospective gates and stop conditions

These gates are proposals for a **separate root selection**, not execution
authority. Root must freeze exact input leaves, mutation bytes, source maps,
output ceilings, containment and CPU/memory/wall budgets before launch.

1. **Source congruence gate.** Independently review the extracted common
   apply/finalize bodies and adapter. Reject checker/config changes, duplicate
   policy drift, loss of authentication fields, caller-supplied native objects,
   lifetime shortcuts or unbounded retention. Host-side differential tests
   alone cannot prove all-input congruence; require the extraction argument too.
2. **Finite host differential gate.** Use the retained A, B and AB packets
   plus a frozen maximum of 24 mutated packets spanning metadata/unknown
   fields, duplicate raw keys, integer widths, Unicode/escapes, DAG continuity
   and duplicates, universe ordering, support/reserved-name drift, output
   self/cross-reference, role/group fields, proof/type errors and bounds.
   Fix expected old/new outcomes and the relevant construction/journal
   observations before execution. Reuse actual already qualified negatives
   when their bytes reach the changed seam; a host-preflight negative that
   never reaches adaptation is not adapter coverage. No fake certificate
   counts as a positive or negative receipt test.
3. **One new-image parent-free execution screen.** For the exact retained AB
   raw packet and unchanged non-image header semantics, same exponent 18 and
   cycle cap 2^26, compare against retained baseline 17,301,504 padded rows,
   15,609,378 nonpadding rows, 15,411,179 instructions and 66 segments. Do not
   rerun that old baseline or invent current-child trace counters. Proposed
   worth-continuing threshold: at least 10% fewer padded rows
   (`new_padded <= 15,571,353`), fewer segments, unchanged non-image journal
   fields, no weakened bounds, and within an explicitly fixed memory cap.
   Measure setup/execution CPU, wall, peak memory and bytes. If this candidate
   fails, record and stop it; no post-hoc threshold/workload change or full proof.
4. **Migration gate before a proof.** Even a trace-screen pass authorises no
   adopted receipt. Choose an honest cold-use/parent-compatibility route, assess
   packet availability and namespace transition, and bound its costs. If no
   workable route or credible finite use population exists, retain the old
   image and stop adoption. No replayed old positive may be called new-image
   evidence.
5. **Only then a separately selected cost/correctness qualification.** A real
   new-image certificate and authentic parent use need their own full-cost and
   receipt/discharge audit. A material trace saving is a reason to investigate,
   not proof of proportional producer CPU saving or quicker useful knowledge
   growth. Equal-endpoint local-library/direct-proof comparisons remain the
   later growth test; do not force the control to reconstruct unnecessary
   ancestry or count raw theorem quantity as benefit.

The 10% bar is a prospective engineering screen inherited from the earlier
candidate note, not a mathematical theorem. Additional decoder/schema edge
cases may be needed after source review; if they change the selected finite
allocation, they require a new prelaunch selection, not an in-run expansion.

## Pins and disposition

Read-only SHA-256 checks matched the existing recorded sources:

| Source under `experiments/certified-collection-01` | SHA-256 |
|---|---|
| `guest/src/relation.rs` | `8f3973c4a27a5f7c7dd52ffad4381920dbdf7ac72f2c56e4372905d7cbf32aa1` |
| `guest/src/journal.rs` | `3a3162898a5beb3c1cf3f84cbf967730cf1a65a8f57f7e7485f3cf158dac0dec` |
| `guest/src/fixed.rs` | `2df61cb2ea3635dffd7ecdcc36edf1c655a6c0f437a92f6f12f7e992be19ba29` |
| `build-01/project/checker/src/parser.rs` | `5b0eaf937857a17be3c944628855231a58d99c07dd0241cae2d43b70e7343b72` |
| `build-01/project/checker/src/tc.rs` | `522134805c82cb7522aafc2550a3bfc520455f44f893fb18a94acec5fb162c6f` |

Additional read sources: `GUEST-NOTES.md`, `ASSEMBLY-OUTCOME.md`,
`EXECUTION-OUTCOME.md`, `HOST-SOURCE-REVIEW.md`, current `main.rs`/journal,
actual prepared child packet/snapshot marker, source04 namespace construction,
AGENTS/GOAL/current NOW and the earlier next-seam decision. No package/bin or
completed campaign was rebuilt/replayed to make this note.

Disposition: **SOURCE_SUPPORTED_CONDITIONAL_HANDOFF_CANDIDATE_NO_SPEEDUP_OR_ADOPTION**.
The central unresolved questions remain affordable proved production, preserved
trustworthy cross-version reuse, huge-network useful discovery and causal net
useful-growth advantage. This note advances the first decision boundary; it
does not close those goals or alter the frozen tentative-v3 delivery.
