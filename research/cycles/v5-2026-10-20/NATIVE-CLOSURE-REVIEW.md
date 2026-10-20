# Ordinary native closure: independent principle review

2026-10-20. Reviewer: `core_search`. Canonical guard PASS. Read-only source/data
inspection; no product imports, tests, native calls, builds or memory work.

**Disposition: proceed with a narrowly scoped zero-assumption owner.** The
mathematical reduction is valid under the already adopted foundation, checker
soundness and descriptor/hash assumptions. It does not require a new kernel or
cryptographic proof. It does require a new same-call authority boundary: neither
the existing conditional JSON nor the pure context builder is an admission API.

## Why the reduction works

Use the adopted `bounded_parse/aggregate_relation.rs`, whose graph rules agree
with the reviewed `aggregate_claims/relation.rs`; the changed parsing seam
passes an immutable bounded token to the same module checking relation.

Let \(F\) be the exact adopted foundation and \(J_1,\ldots,J_n\) the journals
actually produced by successive native module checks. With zero claims and zero
frontiers, the aggregate graph starts empty. For each \(i\):

1. The module checker establishes a valid local extension conditional only on
   \(F\) and its explicit parent journals.
2. `Graph.delta` requires every parent to equal an already established journal,
   byte for byte, with strictly smaller rank. A parent cannot be introduced
   merely by supplying an opening or naming its semantic ModuleID.
3. The exact rank is zero for no parents and one plus the maximum parent rank
   otherwise. Duplicate exact nodes and duplicate premises are refused.

Induction on insertion order therefore discharges every module premise using
an earlier checked extension. The result is derivability relative to \(F\),
not relative to any unverified cryptographic claim. `Graph.closure` additionally
requires the selected exact targets to be newly checked nodes and every supplied
node to lie in their ancestor closure. It prevents dead work from being counted
as target support; it is not itself the kernel-soundness argument.

Zero assumptions must be checked in **both the submitted frame and the actual
native output**. The encoder permits both counts to be zero; it does not grant
authority. The relation returns an empty pending-assumption vector in this case.

## No added axiom hole found at this seam

The module relation checks the first 413 rows against the exact adopted static
foundation, not against a sender-supplied digest label. Its current policy
identifies the previously adopted 22-declaration, no-axiom foundation.
This is a retained foundational assumption, not a fresh proof of all Lean.

The relation derives imported/local roles from verified group openings and
structural correspondence; checks actual committed body hashes; demands exact
group/body coverage; rejects skipped axioms; and invokes the native extension
checker on every local declaration. The native checker prohibits new axioms,
quotient primitives and missing local proof/definition values. Imported atomic
inductive blocks cannot be partly skipped. The proof-validation correspondence
refinement validates new proof syntax without materializing an unused duplicate
tree; the native kernel still checks the actual proof.

Missing demanded computation fails rather than becoming a trusted opaque
definition. These checks and the inductive graph argument leave no additional
external mathematical premise at the proposed zero-assumption boundary.
This is a source argument under the adopted checker, not an independent formal
proof of that checker's Lean correspondence.

## Exact retained implementation and target

Reuse the **newer bounded-parse native driver**, not the older aggregate-claims
or proof-validation driver:

| Retained artifact | Bytes | SHA-256 |
|---|---:|---|
| `experiments/v5-local-checks/bounded-parse-native-build-02/native_aggregate.exe` | 1,801,216 | `2306e9f32292bdee6e6638a5f9c9cc9f1f9bc288c967a6443ec8862886e942c9` |
| Same directory, `RESULT.json` | 18,078 | `026770a3a3f1a74e04b872a13b4572471048362514c52ca2aea2179d7e8ba3b1` |

Both identities were rehashed. The retained build has no
`FINALIZATION-FAILED.json`. `BOUNDED-PARSE-NATIVE.md` records independent adoption
of this build and the actual ten-control/two-native comparison. Its comparison
RESULT still hashes to
`ddd411125b809fda24be93280329f6d7b7bd3d4b32ac5cbd71beab46e4948a20`.
Reuse that evidence without repeating compiler history.

The build source map binds `bounded_parse/aggregate_relation.rs` at `6a2425aa`,
`bounded_parse/module_relation.rs` at `0f78c166`, and the unchanged driver at
`b153bdd3`; the checker artifact is the proof-validation refinement `c0c0b10b`.
The bounded parsing change does not weaken `check_bound` or graph rules.

Rehashed the proposed base input `ce554d48` and retained packet `6998ba92`.
Data inspection confirms V2 schema throughout: base rank 0 / zero parents /
1,072 rows; fusion rank 1 / one parent / 1,168 rows; projection rank 2 /
two parents / 1,036 rows. The latter two have one theorem group each, exporting
`ClientV5.fusion` and `ClientV5.project_summary`.

The selected target must be the **same complete 184-byte projection journal**,
not merely the same ModuleID or a fresh aggregate header. Preserve each witness
value, including its parents, local specification and rank. The module journal
function depends on the local specification, fixed image/foundation/policy and
rank, not on whether an earlier journal was established natively or by receipt.
Replacing the base frontier with its full rank-0 witness therefore preserves
the target journal if all checks succeed. Require exact equality to the target
already selected by the retained V route, plus committed descriptor/name/type
binding to ModuleID `6ea8fa600c3ec9eb64992466c2c897d6455b53a6d0461a2b655fcb3f2c86d55f`.
The proposed three-node invocation itself has not run.

## Minimum trustworthy owner boundary

- Adopt the exact executable, policy and controller/parser/supervisor code as
  local configuration. Bind and recheck their identities around one supervised
  invocation; use immutable input bytes in a fresh non-overlapping output area.
- Strictly bound and parse the input/output. Require the expected frame/profile,
  zero claims/frontiers, exact target list, complete successful process cleanup,
  exit zero, and no resource/finalization failure.
- Bind stdout to the **actual same-call** input hash/length and complete wire
  consumption. Require exact conditional-success schema/status, empty output
  assumptions, exact member journals and their committed header/openings, and
  the selected target's membership. A header's aggregate-image field comes
  from the input: it is **not** authentication of the native executable.
- Mint a distinct opaque, owner-local handle only after successful final checks.
  Keep packet/member/evidence identity and resource allowance in owner state;
  describe/use rechecks must reject fabricated, cross-owner, stale or closed
  handles. Failure must mint nothing. Saved JSON/header bytes cannot reopen
  authority and cannot be labeled a genuine I/A receipt.
- A semantic session must bind every selected opening to an established exact
  journal and every supplied body to its committed descriptor. Reuse the pure
  context algorithm only behind this separate live native owner/view. Its
  `UNTRUSTED_AUTHORING_CONTEXT_READY` output alone is deliberately non-authoritative.
  Do not impersonate `VerifiedMixedDelta` or relax existing exact-type I/A checks.

This assumes a trusted local owner process/installation. Hash bracketing and
Windows Jobs are not a security sandbox against a hostile local account.

## Comparator challenge and fair interpretation

The proposed O is a useful **matched-representation, deduplicated native DAG
baseline**. It checks each module once and does not reprove fusion. However,
`module_relation::check_bound` still reconstructs a separate export environment
for each witness, with repeated foundation/import rows. It is not an optimally
shared persistent Lean environment. A win against O is not a lower-bound proof
against every optimized ordinary library; a loss is already meaningful.

Keep mathematical endowment, target, reusable method and accepted semantics
equal. Both routes may extract needed semantic groups/bodies from already
obtained witnesses, reuse caches and avoid redundant body requests. Both must
reach the same selected context (2 modules / 9 groups / 12 declarations /
9 bodies) before claiming read/use comparison. The split-provider experiment
tests a service boundary, not an optimized cost comparator.

Distinguish cold mathematical acceptance from warm reuse; do not erase O's
legitimate persistent cache. Factor out discovery only when equal, and include
unequal acquisition, decoding, binding, installation/owner setup and common-work
amortization explicitly. Full-cost growth still charges certificate production
and maintenance. The existing receipt being larger than the base witness already
precludes asserting a demonstrated byte saving for that base.

**Recommended scope:** first implement/check the small verification-component
owner and exact endpoint binding. Add semantic-owner integration only if it
remains a thin reuse boundary. Do not claim whole read/use from a native-only
timing. This bounded O option does not replace the unresolved large-ancestry
certified route or establish positive useful-growth margin.
