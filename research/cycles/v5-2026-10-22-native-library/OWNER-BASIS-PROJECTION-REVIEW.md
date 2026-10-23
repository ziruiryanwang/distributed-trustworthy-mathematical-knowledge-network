# Owner semantic-basis projection: independent review

Reviewer: `admission_event_audit`, 2026-10-23. Assigned actual saved consumer01
failure and source-only projection review. No consumer, preparation, compiler,
native checker or admission was rerun. Source review is complete below; actual
successor behavior is not established merely by this document.

## Actual consumer01 failure

Operation: `experiments/v5-local-checks/ordinary-owner-consumer-01`.

| File | SHA-256 |
|---|---|
| selection.json | `34467e91d63ea7db070a6d6a2f4a8f0a5af82dcad59ec1a51ea67b2174653e2a` |
| RESULT.json | `a71fcb9e8cd10fb0e227b8dc5083ffff068e0e42a27119b8d4cad6761fdf0d3e` |
| CONSUMER-SOURCE-MAP.json | `0d4e4c3f36ffa5f6093c2b8e1c18321e99e72217c667a4b46c1c328051aa2326` |
| consumer.stdout.txt | `e45b10b8cdfe26a7c6aa1813ae41cfa6cdd85cf4f8f7e9093a65c4f7447aa069` |
| consumer.stderr.txt | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| generated consumer source | `3ff9981130fd3e6e5c0760523bd9e39880d76ac45f69aef0eafeeefa272efe35` |

All selected source snapshots and runtime/helper pins were independently checked
and match. The generated consumer retains the original proof body verbatim,
imports the ordinary Std module and selected commands, and does not import the
producer. The first semantic diagnostic is:

```text
NONPERMITTED_AXIOM_OR_INCOMPLETE_RECORD name=Nat.gcd importLevel=private
```

The command entered the existing owner and matched the seven-field header with
387 groups, 581 basis rows and three targets. The failure arises in
OwnerRebind.matchBasisRow's non-theorem `BootstrapProbe.screen` call, before the
group loop. Therefore no acquired group was checked or installed and no completed
BoundContext existed. The later `ReadsOnly`, `Avoids`, `readsOnly_insertMany`
unknown identifiers and final `NO_LOCAL_BOUND_CONTEXT` are consequences of that
earlier refusal. Error-recovery `sorry` diagnostics are not accepted mathematics.

The lean-build directory has no output file; neither consumer-export.json nor
CONSUMER-RESULT.json exists. The wrapper reached its explicit nonzero-compiler
refusal after the request's post-run check. The outer operation reports clean
closure, child exit 1, zero active processes, no termination request or cleanup
errors. It records 3.890625 s Job plus 0.453125 s wrapper CPU (4.34375 s known
total), 4.7498921 s outer wall and 908746752 bytes peak Job private commit. This
is not timeout/OOM evidence. Preserve and charge this failed attempt.

## Projection principle

The accepted receiver basis and its identity remain unchanged. Authoring need
only establish correspondence for the selected mathematical meanings reachable
from the acquired interface and necessary construction, not every unrelated
foundation declaration. Let S be all required references of the unchanged group
packets and targets, including full construction dependencies for missing units.
Let D map a basis name to the references needed by its accepted semantic row.
The authoring basis projection should be the least finite closure B* satisfying

```text
S ∩ basis ⊆ B*
n ∈ B*  ⇒  D(n) ∩ basis ⊆ B*
```

All references outside the basis must already belong to the unchanged ordered
group map; an uncovered reference is a refusal, not permission to omit it.
The receiver still checks every new successor against the actual full accepted
context. Projection changes an owner-side correspondence request, not the
foundation, mathematical policy, accepted catalog or meaning of any ID.

The dependency function must include types, transparent definition and
non-theorem opaque bodies, inductive group/constructor metadata, constructor
owners, recursor group/rule-constructor/rule-body dependencies, and implicit
literal support. It omits only already warranted theorem proof bodies. Missing
unit construction proofs remain needed. Merely scanning named constants in DAGs
is insufficient because native literals contain implicit semantic references.
Needed Nat.gcd or another hidden non-theorem computation cannot be dropped to
make the current owner pass.

Original basis rows must be authenticated against the fixed accepted inventory,
with only the previously authorized theorem-proof projection. IDs must still be
computed against the unchanged full basis identity. Existing 387 group packet
bytes are reused exactly. Raw bounds, exact input authentication, aggregate
resource accounting and the existing final Lean correspondence checks remain.

## Completed projection source review

No blocking source defect found in
`software/v5/ordinary_lean/owner_basis_projection.py`, SHA-256
`c800cf081dc8a1bceb61c6b3978bce0302d93c172e0b738676c4a4d955db6a4f`,
under the authenticated original-request premise. The complete author checkpoint
OWNER-BASIS-PROJECTION was also read, cut
`21710467d6abaa4e6e6a5eb5c18ce3da948857f458bdd13fc71b920e2a408797`.

The implementation pins the fixed inventory digest and reconstructs every one
of the original 581 projected basis entries and their IDs before selecting any
subset. The whole header basis list must equal that reconstruction. Ordinary
row scanners retain required type/body/generated metadata references; optional
construction units use the full existing unit census, including theorem proofs.
Both legacy and ordinary DAGs add implicit literal support. Legacy name wrappers
are handled separately rather than confusing their grammar with ordinary DAGs.
Uncovered group references and a basis closure escaping the fixed inventory
refuse. A visited worklist handles mutual metadata without recursive expansion.
Original basis order is retained and only the header basis_rows field changes.
No group bytes or accepted identities are regenerated.

The reviewer independently inspected installed Lean/Expr.lean's Literal.type and
the exact upstream commit `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`:

- [type_checker.cpp](https://raw.githubusercontent.com/leanprover/lean4/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/type_checker.cpp),
  infer_lit and reduce_nat: literal typing uses Nat/String; arithmetic dispatch
  compares the explicit application head. A literal does not imply Nat.gcd.
- [inductive.cpp](https://raw.githubusercontent.com/leanprover/lean4/293d5d0c0c3f3dded4688b3ccd6a33939ac5102b/src/kernel/inductive.cpp),
  literal conversion and initialization: Nat.zero/succ and the recorded
  String.ofList, Char, Char.ofNat, List.nil/cons support agree with the code.

These are targeted source checks, not a new kernel correctness or binary
reproducibility proof. The existing pinned runtime/profile assumptions remain.
The finite syntactic scan conservatively includes all represented nodes; no
semantic-minimality or universally optimal projection claim is needed. Literal
nodes are charged again for their separate scan. One aggregate work cap and
fixed input bounds prevent unbounded per-row allowance renewal. This helper
has no IO, native launch or catalog authority.

`materialized_units` counts ordinary non-generated optional units; generated
optional units may be present or absent in the actual owner and are separately
counted. Only the later Lean helper determines real membership and checks any
missing unit. Empty basis closure is expressly unsupported rather than padded
with an arbitrary root.

## Revised consumer driver and selection

Root-owned run_owner_consumer.py successor
`b65828a3696b7b39b22e23a337eea80f82c25ae6b402768a3ba9888e908e4d40`
and Select-OwnerConsumer.ps1 successor
`679e997b6b9a5ccf196c462828bd550fb44397717de660b6d2ebbdefc3c4c6b8`
were read completely. No blocking changed-boundary defect found for the
prospective consumer02 using the adopted command-build02 artifact set.

The driver first authenticates the original 388 files, reads the small pinned
inventory, projects the header and writes a fresh output-local owner-request.
All 387 original group bytes are copied unchanged. The new file map is checked
before and after native execution; the original file map is also rechecked.
Groups and parsed projection state leave local function scope before Lean starts.
The original consumer body, command imports, expected IDs, timeout and honest
nonacceptance result label remain unchanged. Snapshot-local import resolution
loads projection, owner_request and ordinary_evidence; the selector snapshots
all three and adds the fixed inventory pin. Successful native helper artifacts
are reused, not rebuilt.

The new PREPARE report inherits original preparation's evidence/setup counters.
Those are historical costs of the authenticated original preparation, not
evidence that consumer02 repeated the 49 MB setup scan. Actual outcome reporting
must distinguish this provenance metadata from newly measured work. Fresh header
bytes and file maps are the operative new correspondence input, not a new
mathematical basis warrant.

Disposition: GO for root's finite changed-boundary consumer operation, subject
to the usual exact selection and aggregate supervision. Actual projection counts,
owner matching, source use, inert export and independently checked successor
remain unperformed at this review cut. No old failure is relabeled and no helper
or accepted prefix replay is authorized by this review.
