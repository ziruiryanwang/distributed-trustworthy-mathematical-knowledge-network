# Restricted composition: concrete integration and refinement boundary

2026-10-21, core_release. Source design and source-implementation handoff; no
build, test, proof, image adoption or installed distribution change is authorized
by this note. Root's RESTRICTED-COMPOSITION-IMPLEMENTATION.md owns that selection.

## Decision

**GO for the narrow source implementation.** RC0 may check structural typed
applications/abstractions over authenticated ordinary theorem interfaces, using
the compiled exact foundation equality signature. It need not reconstruct the
413 foundation rows or call the general native checker on every contribution.

**NO for broad beta/zeta conversion, imported definitions, or proof funding.**
The imported-abbreviation counterexample in RESTRICTED-COMPOSITION-REFINEMENT.md
is a real old-checker simulation obstruction, not an efficiency caveat. The
restricted lane must refuse unsupported terms instead of silently broadening
the semantic predicate. A source-level GO is neither a certificate nor a
measured savings claim.

The remaining binder issue has a concrete narrow repair: preserve native binder
name/style/origin in the internal compiled foundation signature. Canonical
submitted binders reconstruct with anonymous name index zero. Exact comparison
must compare this native structure, not only an alpha-erased encoding. Only a
direct Pi/lambda-root recursive comparison can ignore names/styles, reproducing
the old checker's binder path with the same opened locals and recursively
approved comparisons. In particular, alpha equality underneath an application
is not automatically an old-checker quick-path equality. Select Eq and the
particular equality theorems needed by the workload; do not grant every compiled
foundation declaration an unrestricted conversion role.

## Exact semantic and transport separation

The RC delta is a strict six-field JSON record:

```text
{schema, image, rank, local_spec, parents, proofs}
schema = "DMKN_RESTRICTED_COMPOSITION_V1"
parents = [{journal, openings}, ...]
proofs = [proof for local ordinary group 0, ...]
```

There is exactly one local ordinary theorem per group, and one proof in matching
order. Existing module-spec/group/opening encodings are unchanged. The theorem
descriptor retains `value_hash: null` and empty metadata. Proofs are checking
witnesses, not transparent bodies and not part of ModuleSpecID. There is no
`rows`, `bodies`, caller-supplied signature, checker callback, successful-check
boolean, receipt-authority flag or caller-supplied virtual-bound certificate.

The delta's image is the fixed semantic I image
`9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.
Its conditional conclusion is the same 184-byte J and exact parent-J sequence
as the constructively emitted original witness. It is **not** an independently
verified I receipt. The fresh aggregate guest verifies real I or same-image
A-RC assumptions and commits the existing 192-byte H format with its own actual
aggregate image. Receipt-image verification is what grants authority.

Use fresh outer magic `DMKNRC01` and version 1. Preserve the existing bounded
binary aggregate layout after that prefix: image, counts, assumption descriptors,
frontier openings, exact targets, length-prefixed delta frames, exact EOF.
Tag 0 means a genuine fixed-I journal receipt. Tag 1 means a genuine H from
this exact same A-RC image and a checked member opening. An old-A H is not
accepted as if it were A-RC. A future bridge would be separate work.

The aggregate graph stays keyed by exact J bytes, not module identity alone.
Preserve unique receipt claims/frontiers/targets; established parent checks;
strict exact rank; maximum parent seal height plus one; no unused assumptions;
and no member outside the target dependency closure. Every new graph node must
come from the restricted module checker. Returning a conditional graph result
alone never authenticates it.

## Minimal file/API ownership

All new paths below are under `software/v5/restricted_composition/`.

| Part | Reuse or fresh source | Owner |
|---|---|---|
| Canonical JSON, commitments, J, policy, conclusion type | Reuse retained `dmkn_module_relation` crate | Growth/root |
| Exact compiled signature, RC inference, virtual-W bounds, delta relation | Fresh `dmkn_rc_relation` source; no native-checker calls | Growth |
| `census.rs`, `wire.rs` | Fresh strict RC shape and shared stream census | Release |
| `aggregate_relation.rs` | Fresh successor of existing graph relation; only RC introduction path | Release |
| `aggregate_lib.rs` | Fresh wrapper, existing header/member source by path | Release |
| Guest entry | Reuse existing verify-every-pending-claim/commit-H entry source if API agrees | Root |
| Host linking/build/image adoption | Fresh exact selected source maps and records | Root |

Root selected the existing `dmkn_module_relation` dependency rather than another
thin primitive wrapper. The new `dmkn_rc_relation` exports
`relation::check_with_census(Value) -> (RelationConclusion, SourceCensus)` and
`check(Value) -> RelationConclusion`; the latter drops diagnostics. The aggregate
calls only `check_with_census`. The retained crate's general/native dependency
may be linked for native differential controls, but the RC acceptance path must
never invoke it. A later guest link-map/artifact check must establish removal
of unused general code; a source dependency name proves neither cost nor dead
code elimination. No parallel canonical implementation is being introduced.

The conclusion contains `journal` and `parent_journals`. These public data are
not authority; only a successful internal checker call may feed the private
aggregate graph. Aggregate public APIs remain `check_reader`,
`check_bytes`, private-construction `ConditionalConclusion`, exact pending
claim getters, and header/member/census getters. The guest and host must link
the **same** selected RC relation library. A current host executable contains
the old parser, so changing an argv image ID cannot make it an RC host.

## Bounds without replaying the foundation

Initial proposed RC caps: 256 KiB per delta; eight parents; sixteen imported
ordinary groups; eight local ordinary groups; eight universe parameters;
relative names at most eight components, each string at most 64 UTF-8 bytes;
and JSON container depth at most 64 (expression depth48). Whole aggregate limits retain eight assumptions,
32 frontiers, sixteen deltas, 48 total members, 128 edges and 16 MiB total wire.
Charge all delta expressions/levels cumulatively, not independently per proof
or per delta; the first aggregate occurrence envelope is 8,192. These caps are
fail-closed restrictions, not a claim that every useful theorem fits RC0.

There are three separate accounting jobs:

1. Raw input length is checked before frame allocation; generic JSON nodes,
   depth and parents/openings are checked before the mathematical core. Strict
   parsing precedes the node census but is itself bounded by the256KiB frame
   and parser recursion limit. The core checks source syntax before inference.
   Its internally derived expression/level counters are accumulated after that
   frame's core check, before the delta can enter the aggregate graph. Thus8192
   is the whole-stream expression **acceptance** cap, not a pre-work runtime
   cap: a refused stream may process8192 previously accepted occurrences plus
   one additional8192-occurrence frame before detecting the excess. The analogous
   bounded one-frame overshoot applies to the derived level/address census.
   There is no refund and no accepted conclusion on that path. A final EOF
   check is mandatory.
2. The kernel charges actual inference, substitution, internal expression
   construction and comparison work. Tiny input does not imply cheap inference.
   No local declaration resets a frame's200,000-work allowance. Aggregate census
   adds actual work across frames, with whole-stream cap3,200,000 (=16*200,000),
   expression visits8192 and universe visits65536. This is not a200,000-work
   whole-stream claim. Each frame's internal32768-node arena is released before
   the next frame; cumulative allocation is bounded separately by16*32768.
3. The virtual original witness W must fit **every** original limit. This is a
   refinement condition even though W is not materialized in the fast path.

A conservative implementable W census does not require a foundation traversal:
pin offline-derived constants for the exact fixed prefix (bytes, JSON nodes,
depth, table sizes) in the source; charge suffix constructors as they are decoded.
The virtual emitter uses a deterministic full-structure interner seeded by that
prefix. A no-dedup count of suffix emissions upper-bounds emitted rows; duplicate
native rows are NOT allowed because the old parser rejects duplicate interning.
The theorem proof can remain a virtual expression DAG; its fully expanded
occurrences must nevertheless fit correspondence's cumulative 250,000 visits.

For a concrete conservative budget implementation, let E/L/N/D count submitted
expression occurrences, universe occurrences, generated name components and
import/local declaration records, counting repeats. With at most eight levels
per constant and 64-byte name components, each emitted suffix expression row
fits 256 canonical bytes, level row 64, name row 512 and declaration row 512
(indices are bounded u32). Thus an intentionally loose envelope is

```text
bytes(W) <= fixed_prefix_bytes + canonical_bytes(RC_frame) + 4096
            + 256 E + 64 L + 512 N + 512 D
nodes(W) <= fixed_prefix_nodes + nodes(RC_frame) + 256
            + 32 E + 8 L + 8 N + 32 D
rows(W)  <= 413 + E + L + N + D.
```

Charge the `DMKN.Mod.<owner>` prefix and every universe-name component in N,
not merely user-relative names. Validate these per-record maxima against the
actual selected emitter grammar before adopting them; reject when any bound
cannot be established. The 4,096 envelope covers outer-field replacement only,
not an unbounded omitted parent or descriptor. Existing RC fields copied into
W are already charged by the full RC canonical size, even when this overcounts
proofs which are replaced by row references. Every old node/string/index limit
must also be enforced. A loose upper bound may reject a large otherwise-valid
input; it must never undercount an accepted input.

Correspondence visits types and new theorem proofs with repeated occurrences;
its bound follows from the charged E+L, not distinct DAG node count. Native row
expressions contain integer references, so copying RC descriptor/opening trees
does not increase their depth substantially; bound W depth by the maximum of
the compiled prefix depth, copied frame depth plus a conservative fixed margin,
and flat row depth. Require a margin below serde_json's original default
recursion limit, not only the nominal canonical depth256/correspondence depth192.
The eight-universe/expression-depth48/open-binders64 caps also fit u16
de Bruijn/local-counter bounds. CORE-PLAN's audited prefix and address-union
limits give tighter concrete upper bounds than the loose per-occurrence formula
above; the actual core bounds are authoritative for source review.

If constants or per-record limits cannot yet be audited, keep that input refused;
do not restore a full native-row traversal as an unnoticed default fast path.
An optional host-only original-witness emitter is useful for differential tests,
but it must not become a guest prerequisite.

## Producer and ordinary receiver integration

`aggregate_small/producer.py` cannot be reused unchanged. Its host-build and
image-adoption methods require exact old schemas, source maps and executable
names. The `prover_memory/producer.py` successor demonstrates a narrow checked
override seam, but handles only its own stage-build schema. Select a fresh RC
producer adoption successor that verifies the actual RC build/assembly chain
and pins the whole loaded runtime closure. Do not fabricate old-format build
reports or weaken a successful-process/source/image binding to accept RC.

The staged crypto host sources and `aggregate/receipt.rs` may be reusable with
the new linked relation and exact support profile; unchanged source is not an
unchanged executable. Preserve complete, resolved receipt verification, actual
image/J/H matching, parent claim binding, finite stage authorization and cleanup.
Existing po18/N256 orchestration is a reusable mechanism, not renewed funding.

The integrated ordinary route is:

```text
prepare RC contribution from selected admitted interfaces and explicit proof
  -> conditional RC preflight and exact target J
  -> finite actual A-RC proof production and independent receipt verification
  -> pack_terminal(H, J, member opening, actual receipt, A-RC image, envelope)
  -> ordinary publication/custody/discovery/acquisition
  -> AggregateReceiptVerifier -> select_member -> open_group
  -> terminal evidence admission -> A-member LiveWarrant
  -> MixedImportSession.use_aggregate_member -> next ordinary contribution.
```

Use the authoritative installed SDK source map in
`experiments/v5-local-checks/distribution-terminal-i-01-input.json`.
Its terminal-I implementation also contains the actual A-member route; it does
not convert A members into fabricated VerifiedModule objects. The selected
packet/custody wire and client support bind an aggregate image, so A-RC requires
an explicit fresh owner trust/support profile. F/P-compatible discovery alone
does not authorize a new image. Old installed trust/state stays untouched.

The first target is the refinement's three binary_congr applications over four
universes and sixteen binders. A later consumer must import its actual A-RC
member and make a further valid contribution, potentially using Eq.trans.
FIRST is still uncertified and outside this target's evidence. This is a useful
composition/economics discriminator, not a difficult discovery benchmark.

## Minimum changed-boundary evidence

Before runtime selection, independently review the exact source closure and
compiled signature derivation. Focused controls should reject wrong I image,
extra/duplicate fields, unsupported terms, unbound universes/bvars, mismatched
proof order, forward/local cycles, imported definitions, a conversion needing
beta/delta, alpha-only app comparisons, bad imported openings, aggregate budget
reset, wrong-A parents, unestablished premises, trailing bytes and length bombs.

Compare accepted RC0 inputs with their constructively emitted original witnesses
for equal J/parents. Then measure the identical target/parents through the best
qualified general lane and RC0 before funding a real proof. No useful-growth
claim follows solely from fewer rows, a smaller wire, or an easier theorem.

This design reuses the existing terminal/custody/import path and replaces one
costly checking lane. It does not add a second general mathematics protocol or
claim to close all final-v5 deployment obligations.

## Source implementation checkpoint

The four release-owned files are implemented, unbuilt and unexecuted:
`census.rs`, `wire.rs`, `aggregate_relation.rs`, `aggregate_lib.rs`.
The aggregate successor preserves the old graph algorithm exactly apart from
the RC core introduction/census call, distinct wire/schema and control-module
selection. Existing header/membership sources are referenced unchanged.
The census uses strict six-field object records, exact fixed-I image words,
per-frame and whole-stream JSON counters, parent/opening counters, and derived
core counters. It does not accept row/body variants or a callback checker.
An aggregate that exceeds a shared counter returns no conditional conclusion;
the bounded final refusing core call is not treated as free work.

Independent changed-boundary review/controls are assigned to adaptive_audit.
No compilation, runtime, image adoption, host rebuild or proof has been selected
by this implementation checkpoint. Root owns all such later decisions.
