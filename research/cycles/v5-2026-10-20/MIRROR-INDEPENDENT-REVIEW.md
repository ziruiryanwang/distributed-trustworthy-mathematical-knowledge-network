# Mirror method: independent source review and minimal owner composition

2026-10-20, core_release. Source-only review requested by root. No import,
constructor evaluation, parsing of candidate data, comparison with a candidate's
encoded type, compilation, native/proof execution, network or Git operation.
No source, planner or used evidence was modified by this review.

## Finding

**No source-level mathematical, binder, universe or dependency blocker found.**
The constructor expresses the intended evaluator contract independently of a
candidate address; the two proposed applications are mathematically valid under
the stated imported interfaces. This is permission to consider a bounded ordinary
owner composition, not a claim of compilation, discovery or mathematical
admission. Exact exported-type agreement remains a later runtime boundary.

Two operational conditions are mandatory: render the first contribution from
the actually resolved/admitted method locator, and use a fresh owner operation
and fresh import for the onward injectivity contribution. A contribution report
does not supply a new authoring context or transferable warrant.

## Exact reviewed sources

| File | SHA-256 |
|---|---|
| `software/v5/examples/mirror_method/method_query.py` | `0ddbc8dac7e60180f3f9aad3216873158d8b2722a9d31c48112e20262298c642` |
| `software/v5/examples/mirror_method/MirrorInvolution.lean` | `766750ca8247fcd1d20eaf57f84475673878841a5d7304fa0b648bd7859ead1c` |
| `software/v5/examples/mirror_method/MirrorInjectivity.lean.in` | `9021d2150caefc7dd85844995ad63e4403237c6804701cc49df6919b9dd5a5f3` |
| Retained `software/v5/workloads/EvaluatorUniqueness.lean` | `e9beebfd492cfe3a809ee02fd1d010ca043ea33814161b580c5d62d97fcbb686` |

The actual source/import envelope was checked through the current 114-source
map: `modules/codec.py`, `interface_views/authoring_atomic.py`,
`interface_views/imports_atomic.py`, `interface_views/projection.py`,
`body_location/client/workspace_evidence.py` and
`body_location/client/semantic_reader.py`. The existing owner policy is
`software/v5/examples/contribution.py::contribute_from_context`.

## Query constructor review

The contract has exactly these outer binders, in order:

    A, B, L, N, h, k, h_leaf, h_node, k_leaf, k_node, t.

A and B are implicit; the others and all arrow/equation binders are default.
`_lower` checks a variable against the current nearest-first name context,
lowers each binder domain before extending that context, and extends it only
for the body. Its generated local argument names do not collide with the
outer contract names. Shadowed x/left/right names are confined to their own
equation domains. Thus no free variable, accidental capture or shifted domain
reference was found.

For example, in the final conclusion the indices are

    t=0, k_node=1, k_leaf=2, h_node=3, h_leaf=4,
    k=5, h=6, N=7, L=8, B=9, A=10.

Its conclusion is consequently `Eq B (h t) (k t)` with those indices. Inside
the h_node equation's right-binder body, right=0, left=1, h=4, N=5, B=7 and
A=8; both node arguments and both recursive evaluator applications use the
correct variables. Inner nondependent-arrow binders still shift B/A correctly.

A and B are respectively `Sort (succ u)` and `Sort (succ v)`. Tree and its
constructors receive universe u and their explicit A argument. Equality is
`Eq.{succ v}` applied to B, because B is a Type v rather than a Sort v
variable. The two fixed alternatives exchange the two declaration universe
parameter positions; they do not reorder logical binders or learn from a
candidate. This addresses parameter-order sensitivity only, not arbitrary
normalization, elaborator encoding differences or mathematical equivalence.

The constructor contains only the caller's known Tree module, Tree/leaf/node
names and foundation Eq. It reads no file, packet, candidate, M identifier,
evaluator_unique name or saved answer hash. Dummy-owner relocation equality is
a useful guard against local-owner dependence; source inspection also confirms
all constructor references are foundation/external. The declared-type hash uses
the same domain and relocated form as current export extraction.

This is **unknown-ID discovery of a specified formal contract**, not discovery
of an unknown problem statement. The local agent is allowed to know the
evaluator property it wants. The reviewed retained signature helps audit that
property; a runtime owner must not use the retained M source, its encoded type,
private packet or answer digest to repair/filter a failing query. Freeze both
alternative queries before any response. If neither matches, retain the miss.

## Involution source argument

The source defines mirror using the imported `CommonsV5.Tree.rec`. For fixed A,
write m for mirror. The recursor gives the definitional equations

    m(leaf a) = leaf a,
    m(node l r) = node (m r) (m l).

Thus h(t)=m(m(t)) and k(t)=t both satisfy the same Tree evaluator equations with
L=leaf and N=node. For a node, two reductions give

    m(m(node l r)) = node (m(m(l))) (m(m(r))).

All four equation arguments supplied to evaluator_unique are therefore reflexive
after definitional reduction; no induction hypothesis is being assumed by an
`rfl`. Instantiating the method at B=Tree A yields the desired `m(m(t))=t` for
all t. The new declaration genuinely depends on the reusable method's interface.

The relevant inductive group includes Tree, both constructors and its recursor.
The authoring context must supply the certified group's exact recursor rules:
an opaque type declaration alone does not support these reductions. Current
semantic closure and frontend projection preserve inductive/recursor groups;
the interface-only projection changes only missing ordinary definition bodies.
M's theorem proof need not be unfolded for source use, although its offered
native evidence must still pass the ordinary admission lane.

## Injectivity source argument

Let V(t):m(m(t))=t be the imported involution theorem. Given h:m(x)=m(y),
`Eq.ndrec` uses motive

    z |-> m(m(x)) = m(z).

At z=m(x), `Eq.refl (m(m(x)))` inhabits the motive. Transport along h gives
q:m(m(x))=m(m(y)). The outer transitivity term is

    symm(V(x)) ; q ; V(y) : x=y.

Equality orientation, motive endpoint and transitivity endpoints agree. No
function extensionality, extra axiom or unfolding of imported m is needed.
An interface-only import is consequently appropriate for this second source;
the unchanged final checker remains authoritative if actual conversion needs
additional data. The source cannot treat a projected opaque frontend surrogate
as a replacement for the authenticated original definition descriptor.

## Minimal owner file plan, not a new product mechanism

Keep the current fixed-target `.lean` as a readable reviewed reference only.
Root could select one new `MirrorInvolution.lean.in` containing a single
`__METHOD_REF__` placeholder for the entire applied method reference. Render it
only after actual candidate resolution, exact contract checking and live
admission/import. Do not leave the fixed M address as fallback data in the
operational template.

The supported renderer can be deliberately narrow: validate the returned module
as 64 lowercase hexadecimal characters; validate the returned relative name by
the adopted codec; accept only nonempty string components matching
`[A-Za-z_][A-Za-z0-9_]*` for this example; quote every accepted component with
Lean identifier quotes; and construct the `DMKN.Mod` module prefix locally.
Refuse numeric components, quote characters and unsupported forms rather than
interpolating arbitrary Lean text. This supports the actual expected method name
without claiming a general Lean-name printer. Require one placeholder occurrence
and no remaining marker. The full source bytes are then bound by existing
authoring/return checks.

The current onward template may retain its explicitly chosen relative names
`OwnerV5.mirror` and `OwnerV5.mirror_involution`. Before substituting the freshly
admitted module ID, the second owner must verify these declarations' authenticated
descriptors and intended types in its live selected context. The replacement
is a validated module ID, never arbitrary text or a publication report token.

The only further file needed for a selected workload is a finite trusted-owner
orchestration entrypoint plus its ordinary bounded input. Reuse existing
`contribute_from_context`; do not create a second contribution helper, compiler,
solver, protocol, crypto path or query planner. No code for these files is
selected by this review.

## Minimal operation sequence

1. An explicitly selected direct provider serves the retained M packet and its
   ordinary index/semantic custody. It may prepare this fixture from retained
   data; the receiver must not read those private fixture paths. Do not author
   or certify M again. This isolates unknown result ID, not unknown provider.
2. Open a fresh ordinary receiver workspace/client with authoring enabled and
   its actual trust adoption. Before any acquisition, reserve one finite direct
   query envelope with at most two generations and the summed original caps.
   Compute the two query alternatives solely from the known BASE and codec.
3. Use existing `next_query`, `search_offer`, `search_page` and `resolve` at the
   explicitly authorized endpoint. Only a genuinely selected candidate advances
   to semantics. A second predeclared universe alternative may use its existing
   slice if the first does not yield the contract; it does not obtain a refund,
   new deadline or third query. Record scoped coverage/refusals, not global absence.
4. Compare the resolved descriptor to the exact independently constructed type
   for that alternative before using its address. Then use the existing
   `SemanticReader` and actual selected module evidence to complete the required
   interfaces/rules and obtain a live context through `finish`. Do not rotate
   queries after staging the successful candidate: that retires its reader.
5. Render the parameterized source from the returned admitted locator. Invoke
   `contribute_from_context` once with roots/exports mirror and involution. It
   authors once, independently admits the new packet and publishes it locally;
   any demand/failure remains a non-contribution. Close original owners normally.
6. For onward use, open a **fresh independently scoped owner operation** against
   the now-published mirror result, with a separately prospectively selected
   finite budget. Its ordinary fresh acquisition/admission produces the new live
   context. Verify both required imported descriptors/types, render the existing
   injectivity template with the actual module ID, and invoke the same helper
   once to author/admit/publish injectivity. Its finite allocation is part of
   the selected workload, not a renewal after failure in steps 2-5.

Step 6 cannot be a second `SemanticReader.finish` on the first client: current
`import_context` requires `_session is None`, and a ready selection view is
sealed. `contribute_from_context` returns inert evidence about its checked child,
not a new context containing that child. No saved report recreates a warrant.

Use one finite direct-provider composition, not another P/Q/R body-location
scenario: that boundary has its own running/adopted evidence. No scaling or
cost benchmark is needed to decide these source equations. Actual later checks
would settle constructor/codec/elaborator agreement and the new mathematical
composition boundary, not establish a universal speedup or sustained growth.

## Remaining claim boundaries

This route can demonstrate a newly checked reusable operation/law and a distinct
onward application, rather than another copy of M or a new theorem-count score.
It does not establish an optimal proof-search lower bound, positive full-cost
margin, global discovery completeness, producer-independent data survival or an
advancing succinct certificate frontier. These are native deltas above retained
evidence; no new cryptographic shortcut is silently claimed. The unchanged full
v5 goal remains open.
