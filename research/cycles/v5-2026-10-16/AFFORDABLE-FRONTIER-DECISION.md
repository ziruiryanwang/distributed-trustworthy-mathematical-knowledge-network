# Affordable frontier: next intervention and when not to implement it

2026-10-16. Source/theory decision only. No client source, compiler, guest,
proof, test, runtime selection or Git mutation. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision

**Complete the selected integrated client/growth-cost path before starting
another guest optimizer.** Its present blocker and user-facing benefit are
concrete. A further guest rewrite has real effort/security cost, while the
retained failed-prefix samples do not establish its whole-run payoff. This
ordering does not waive affordable certified-frontier advancement: the I-only
client retains unsealed native deltas and is not the final scalable v5.

Keep exactly one next representation candidate: **directly decode the existing
JSON proof rows into a typed row representation shared by correspondence and
native row application**. Do not change the wire to binary first and then
reconstruct all the generic `Value` trees. Do not change mathematical checking,
semantic hashes, proof ancestry policy or recursive assumption verification.

This is an implementation option with a specific refinement obligation, not a
selected rewrite or a prediction that the 2^25-cycle screen will pass. The next
frontier decision should choose between this priced source intervention and a
separately budgeted complete-path capability investment; it must not default to
another optimizer merely because a copy or traversal can be removed.

## What is already known, and must not be repeated

The controlling records are [MEMO-SCREEN-DECISION](MEMO-SCREEN-DECISION.md),
[AFTER-BOUNDED-PARSE-OPTIONS](../v5-2026-10-12/AFTER-BOUNDED-PARSE-OPTIONS.md),
[COMPACT-WITNESS-FEASIBILITY](../v5-2026-10-12/COMPACT-WITNESS-FEASIBILITY.md),
[NEXT-AGGREGATE-COST-DECISION](../v5-2026-10-12/NEXT-AGGREGATE-COST-DECISION.md)
and [GROWTH-CRITICAL-PATH](GROWTH-CRITICAL-PATH.md). This note reuses their
comparators, lifetime decision, trust assumptions and preserved failure accounts.

The selected memo image still refused at `33557665 >= 33554432`; there is no
complete A capsule or receipt. The 128 partial segments are not resumable proof
evidence. The screen cost is 5.796875 known CPU seconds, not a completed proof
price. Its deterministic saturated samples cannot supply whole-run fractions.

Existing optimized source already:

- Removes repeated canonical-size scans through the immutable parse token.
- Reuses structural census counts and moves the parsed top-level fields.
- Avoids materializing discarded theorem-proof syntax and memoizes successful
  syntax-DAG visits while charging original logical work.
- Bypasses two outer Serde-flatten buffers for the supported singleton row shape;
  `decode_corresponded_owned_row` is already present. It must not be proposed as
  a new optimization.

The retained complete native *conditional* result reports 215,540 input bytes,
2,364 rows, 29,858 `Value` nodes, 22 bodies, 23 openings and three parent edges.
Those are whole-input structural counts, not accepted guest execution or causal
cost shares. The foundation prefix has 413 rows in each delta, hence 826 of the
2,364 rows. Removing their transmission alone would not remove their semantic
construction/checking, and row fraction is not cycle fraction.

The preserved source fact is more useful than an invented speedup: all 2,364
rows currently pass through generic JSON `Value` representation, and then the
selected relation consumes each through `decode_corresponded_owned_row` before
`parse_owned_rows`. The correspondence inventory separately indexes the same
generic rows. The first row is metadata; it is not a proof operation.

## One concrete option: shared typed rows, unchanged JSON wire

The current and proposed paths are:

```text
Current:
JSON -> generic witness Value -> correspondence over row Values
     -> per-row owned Serde decoding -> native row application -> kernel

Proposed:
same JSON -> bounded typed rows + unchanged non-row Values
          -> correspondence borrowing those rows
          -> native row application consuming those rows -> same kernel
```

This is deliberately smaller than a wholly typed mathematical codec. Local
module specifications, imported openings, bodies and canonical mathematical
expressions remain in their existing representation. The proposal removes the
generic representation of **export rows**, not every JSON object or every
correspondence expression. Correspondence may still construct the same canonical
type/body Values where matching and commitments require them. The Lean native
DAG still exists and still requires construction; neither is claimed as a saving.

### Concrete boundaries

1. Add a private owned row type/view at the existing parser boundary, with
   explicit names, universe nodes, expression nodes and declaration records.
   The existing `OwnedExportRow` and native enum already enumerate the native
   fields; use them as the semantic target rather than inventing a second kernel
   instruction set. Expose immutable field views for correspondence, not a
   public constructor for already-verified rows.
2. Introduce a bounded witness decoder for the **same** JSON bytes. It directly
   decodes `rows` into those records while retaining current Values for the
   other fields. Detect duplicate keys, exact integer widths, invalid strings,
   unknown fields, malformed shapes and trailing bytes at the same boundary.
   A derived Serde struct that silently discards fields is insufficient.
3. Change the correspondence inventory's row accessors to the typed view.
   Preserve exact row ordering, name/level/expression index domains, dependency
   order, owner/universe contexts, group matching and the existing proof-syntax
   memo's logical work/depth accounting. Names and output expressions used by
   semantic matching may remain Values for this increment.
4. After correspondence succeeds, consume these same immutable records through
   the existing native `apply_row` and finalization rules. Do not serialize them
   back to JSON or `Value` to call the old decoder: that merely moves the cost.
5. Preserve the unchanged relation's foundation, group/body commitments,
   conditional-premise construction, kernel checks, all-local-declarations count,
   aggregate graph/rank/closure checks and actual `env::verify` obligations.

This requires fresh selected source successors; no used parser, guest, image or
client source is edited in place. A changed guest still has a new image identity
even with an unchanged wire. No old A certificate is relabeled. The genuine I
receipt and member mathematical identities can remain unchanged if refinement
holds. Retained old proof material is reused only at its existing exact boundary.

### Keep compatibility precise

The old accepted domain is the intersection of the strict JSON parser,
correspondence and native decoder, not whichever one is easiest to imitate.
The existing native decoder has aliases, positional forms, fixed-width fields,
metadata and additional expression variants; the correspondence layer further
restricts many of these. A decoder rewrite must not silently erase that detail.

Preferred first scope is equality on that intersection, including existing
refusals. Build a finite constructor/field table from the actual source before
coding. If exact equality proves disproportionately costly, root may instead
select an explicitly restricted input profile with an injective old-input
projection. That is a separate compatibility decision with disclosed refusals,
not a passing claim for the unchanged full input domain. In particular, an
unreachable malformed row cannot be discarded just because a chosen proof does
not mention it: the native parser still reads all supplied rows.

No foundation-prefix elision, persistent environment cache, speculative new
proof rule, binary transport or generic plugin hook belongs in this first option.
Each would add a different refinement/trust obligation and obscure the payoff.

## The soundness argument to establish before a build

Let `P(b)` be the current strict JSON input Value, `D(b)` the proposed decoder,
and `R(t)` the *mathematical* projection of typed witness `t` back to the old
Value representation. `R` is an argument/specification function; production must
not materialize its full output to obtain the claimed representation saving.
Let `Old` denote the exact current conditional relation, and `New` the proposed
one before its guest wrapper discharges receipt assumptions.

The required successful-input refinement is:

\[
D(b)=t \Longrightarrow R(t)=P(b),\qquad
New(t)=(J,\Pi) \Longrightarrow Old(R(t))=(J,\Pi).
\]

For compatibility on the supported domain, require the converse acceptance
direction too. For failures distinguish semantic rejection, resource refusal
and diagnostics; a reordered error is not evidence of preserved first-failure
behavior. First-failure equivalence is specifically retained for the existing
memoized syntax walk, not automatically asserted for a changed parser.

The source proof decomposes into four local obligations:

1. **Decoder projection.** Each typed field is the exact old JSON value with
   its type, range, Unicode content and order preserved. Key uniqueness and
   exact schemas are established before ignored data could disappear. Every
   accepted row has a unique old interpretation; indices are not renumbered.
2. **Correspondence simulation.** Starting from corresponding inventories,
   each old field lookup and typed field access observes equal values. Recursive
   type/body outputs and successful proof-syntax summaries agree. All original
   logical visits, maximum depths, owner/parameter contexts and failed-boundary
   fallbacks are preserved. Row typing alone authenticates no group or theorem.
3. **Native application simulation.** The record consumed by native `apply_row`
   is exactly what `decode_corresponded_owned_row(R(row))` would produce.
   Retain duplicate/interleaved index checks, safety flags, import-without-body
   semantics, declaration ordering, inductive/recursor finalization and config.
   No public typed-row constructor bypasses these checks.
4. **Relation composition.** Inputs to the unchanged commitment, conditional
   module checker and aggregate graph are equal, so the same J and pending
   premise list result. The guest still verifies every exact pending image and
   journal before committing H. Cryptographic assumptions and checker-to-Lean
   obligations remain the existing ones; the new decoder adds a reviewed
   representation boundary, not a new mathematical axiom.

Consequently, assuming the existing relation and recursive proof system are
sound, a valid new-image receipt warrants the same mathematics. A consumer
still verifies the selected certificate/interfaces plus demanded semantics and
new bounded deltas, without downloading sealed ancestral proofs. Producer
representation changes do not establish search coverage or availability.

## Resource refinement: do not discount work by changing its representation

The current aggregate census charges old Value nodes and depth, rows, bodies,
openings and parent edges. Typed records have fewer allocations, but their
**virtual old census** must still fit the same envelope.

The streaming decoder can count nodes/depth at JSON token consumption and bind
those counts to the returned private typed input. It must count all non-row
Values as well, reserve declared child capacity before allocation, use checked
arithmetic and retain strict JSON container/UTF-8/integer limits. A sender's
claimed count or byte size is not such evidence. The unchanged raw-byte bound
and existing canonical-length argument may be reused only on their actual
strict-parser domain; a custom escape/numeric interpretation needs a new proof.

Logical correspondence work remains the old work, not typed-record count.
Actual heap reduction is a separate physical improvement. The actual enclosing
execution/proof memory and CPU limits remain necessary even after all syntax
counts pass. Type conversion and kernel reduction are not generally linear in
proof-row count; this proposal cannot make that claim.

## Cost argument, without pretending the bottleneck is measured

For one accepted input, decompose the actual old producer work as

\[
T_o=L_{json}+A_{rows}+A_{other}+C_{rows}+D_{rows}+N+H+K+V,
\]

where `L` is lexical parsing; `A` generic allocations; `C` correspondence;
`D_rows` owned-row conversion; `N` native DAG construction; `H` commitments;
`K` kernel work; `V` receipt/aggregate machinery. These terms are conceptual
disjoint costs, not fractions recovered from the PC samples.

The proposed path has

\[
T_n=L'_{json}+A_{typed}+A_{other}+C'_{rows}+N+H+K+V+E_{bounds}.
\]

It removes generic row map/key construction and the subsequent per-row generic
Value-to-owned-row conversion. It adds typed decode/view work and exact census
maintenance; JSON lexical work remains. Existing outer-flatten optimization
is already reflected in `D_rows`, so its saving cannot be counted again.

A sufficient *producer execution* saving condition is

\[
A_{rows}+D_{rows}+(C_{rows}-C'_{rows})
> A_{typed}+E_{bounds}+(L'_{json}-L_{json}).
\]

No current source or retained sample establishes the numerical inequality,
completion under 2^25 cycles, or a smaller final proof price. Both paths retain
at least linear input processing; this is a representation constant/memory
improvement, not an asymptotic theorem of faster arbitrary proof checking.
It avoids the specific bottleneck displacement of binary-to-Value encoding,
but can still expose commitments or the kernel as the dominant cost.

At deployment scale, if a successful supported seal saves producer resource
`s > 0`, adoption/rebuild/assurance/migration cost is `F`, and maintenance delta
over the supported horizon is `M`, then `n*s > F+M` is only the producer-side
break-even condition. The existing two full-cost comparisons against optimized
local development and ordinary shared libraries still apply. Warm cached reuse
does not create artificial savings; historical failed builds/proofs remain
charged. A smaller guest cycle count need not yield proportional proving savings
because segment sizes and proof stages are discrete.

## Marginal-payoff ordering now

| Action | Known decision value | Cost/risk | Recommendation now |
|---|---|---|---|
| Complete current client integration and useful cost reporting | Removes fixture dependence and reveals real end-to-end overhead, recovery and reuse choices | Bounded selected interfaces; no new cryptographic relation | First; keep affordable A visibly open |
| Source-price shared typed JSON rows | Identifies an exact removed representation and refinement obligations | Decoder/correspondence boundary is nontrivial; total saving unknown | This checkpoint; at most a finite constructor/projection audit next if root chooses |
| Implement/build typed rows immediately | Could reduce a repeated producer cost | New image/adoption, source review and differential controls before any useful measurement | Not selected merely from avoidable work |
| Another isolated clone/hash-buffer tweak | Certain local operation can be removed | No evidence it changes the feasibility decision; repeated rebuild overhead | Lower priority, not an optimizer queue |
| Binary-to-Value wire | Removes part of lexical input work | Leaves row Values/redecode, adds wire/native-host migration and expansion bounds | Worse first choice than the shared-row design |
| Larger execution envelope | Could reveal a complete capsule and full execution work | Saves no work; cycles/po2/128-segment/capsule/proof funding are coupled | Separate finite capability decision, not automatic retry or efficiency evidence |

Neither native-only checking for all future users, a trusted producer signature
nor a quorum substitutes for certificate-based no-ancestral-replay acceptance.
They change the trust/scale requirement rather than resolving this cost problem.

## What can be settled without execution, and the minimum later discriminator

From current source/retained data, settle:

- The exact pipeline and unchanged/changed modules listed above; no new profiler.
- A constructor/field table and explicit projection for every supported row.
- Preservation of fixed-width fields, schema/duplicate-key behavior, foundations,
  index domains, import roles, logical bounds and receipt obligations.
- The removed classes of allocation/redecode and the introduced classes of work;
  explain which remain unknown rather than assigning sample-based percentages.
- Native/guest build dependency impact. With unchanged JSON, the existing native
  old-relation preflight can remain an independent comparator if the new guest
  is proved equivalent on the supported domain; it is not itself proof that
  a new decoder ran correctly. New source/profile support must be explicit.

Do **not** claim, without execution, actual runtime, peak memory, segment count,
proof cost or completion. The pending source audit should stop if the proposed
implementation must recreate all row Values, loses the old census/refusal
domain, or requires a broad kernel/commitment rewrite. Those outcomes remove
the claimed narrow intervention and require a new decision, not sunk-cost coding.

If root later selects implementation, the minimum changed-boundary evidence is
one decoder/projection-and-row-application differential control set, with the
retained exact input and targeted malformed/limit cases. Reuse established
kernel and wire controls. Source-derived operation counts are not timing.
Only after that boundary is independently reviewed should one selected guest
execution decide completion/cost; no duplicated baseline or cap ladder.

If the integrated product needs genuine A sooner than an adequately priced
rewrite can deliver it, root should explicitly compare a **one-off complete
capability investment** under a jointly finite execution/storage/proof envelope
against postponement. Do not call that optimization or infer a repeatable
economical service from one receipt. All options leave the final v5 goal open
until genuine end-to-end scalable-frontier and full-cost obligations are met.

## Source anchors inspected

Paths below are relative to `software/v5`; hashes bind this reasoning to the
actual selected files, not an older similarly named implementation.

| Source | SHA-256 |
|---|---|
| `bounded_parse/module_relation.rs` | `0f78c1663673f291c7b612cc3bdef423124cc6cc47fd649b71e5bc13d4cd808a` |
| `bounded_parse/aggregate_relation.rs` | `6a2425aa6d26bf10ab6053d92f498d09b6c7bdde598efe118a5bc7bd2ceb0947` |
| `bounded_parse/census.rs` | `48cad55b54d3cd233d760871308ccfdc54bb50711adb89651f7d2861caa5a1d5` |
| `modules/native/proof_memo/module_correspondence.rs` | `7877ee22c7e1d4350858e67c8cebbedf057dee1820cd9f61940e37cf51f6508e` |
| `modules/native/checker/src/parser.rs` | `7a183a1c9e6ff3ee2c32ee6542ed85d3de0835b00e235f80f6982c3e7038d218` |
| `modules/receipt/src/foundation_static.rs` | `1dd5bd98389d54d09dce554c6a9d82cf841254e3249dadf921360e154c5ebcd5` |
| `modules/receipt/src/commitments.rs` | `ec77943fb15b15ec84c82a864c926536c1356b300cdd616fea93473202d9ed91` |
| `modules/receipt/src/policy.rs` | `cd254a0a591d73d69f3e504bca75ac50f1962f5e61d730340db029970baae902` |

The retained native result is
`experiments/v5-local-checks/aggregate-claims-controls-02/evidence/actual-two-delta/stdout.txt`,
SHA-256 `01d7c9cc45a16f520980e80672f90c0a97a69e31e344f748910df5abb24ffd0b`.
The latest screen binds that result and its 215,540-byte wire; no fresh parsing,
profiling, compiler, guest or proof was run for this note.
