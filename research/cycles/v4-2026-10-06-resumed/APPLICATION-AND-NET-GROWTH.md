# Explicit proof application and net useful capability growth

2026-10-06 resumed work; mechanism owner. This is a design and conditional
argument, not an executed result. The frozen local handoff is the comparator,
not satisfactory v4 completion. Companion implementation is selected only in
`experiments/action-application-01/CONTRACT.md`.

## Decision and the actual missing operation

The old `prepare --source` can already apply and compose acquired Lean theorems.
There is no missing mandatory task planner, human-intention gate, research-goal
tree, or proof-search coordinator. Independent agents remain responsible for
choosing mathematics, discovering candidates and constructing formal arguments.
Documentation or agent skills can teach that strategy; the network need not own
it. Adding another theorem wrapper would not repair an absent system capability.

The missing narrower operation is **source-free explicit proof assembly and
application**. An agent with an exact formal term should not have to generate
Lean source, import and elaborate it, export it through the native bridge, then
submit it to the same final checker. A bounded inert plan can identify an exact
formal endpoint and a proof DAG, select acquired interfaces, instantiate their
universe and term parameters, supply premise proofs, and assemble the ordinary
proof packet directly. The final checker still checks the complete local proof
over authenticated certified frontier interfaces. Unsealed acquired proofs are
substituted, not promoted to axioms. This is a real alternate contribution route,
not autonomous proof search or automatic instantiation.

The workflow owner separately reduces repeated hashing from all installed
authoring assets to the exact action-specific execution/read closure. Neither
change may skip the final proof check, weaken frontier authentication, introduce
a proof-result cache, or trust a peer's success label.

## Philosophy sufficient to guide an implementation

We use a minimal pluralist position, not a claim to resolve philosophy of
mathematics. Under an explicitly adopted formal foundation, a checked assertion
is a derivability claim independent of an author's intention. A valid derivation
does not become false because it is uninteresting, duplicated, or unused. On the
other hand, a database containing more theorem names need not make any agent more
capable. These are different predicates.

An operational knowledge asset is therefore a **verified, accessible capability**:
a formal assertion, definition, algorithm, reduction, or reusable proof method,
together with enough representation and custody to use it within a stated
resource envelope. This does not restrict valid mathematics to algorithms or
decidable propositions. The resource envelope describes what the system makes
available, not what is mathematically true.

For a local agent state L and a finite budget vector b, write Reach(L,b) for the
set of exact formal outputs attainable by a stated family of allowed procedures.
This is a conceptual denotation, not a computable global ranking oracle. A shared
asset can enlarge Reach by making an output cheaper, even when it proves no new
logical consequence of the foundation. Every theorem already derivable from a
fixed foundation is, in that extensional sense, not a new consequence; useful
growth is often intensional compression of discovery, justification and reuse.

An observed or bounded cost improvement for a specified output family is a
legitimate local growth claim. It is not a universal value ordering, a lower bound
on an optimal independent mathematician, or evidence of exponential corpus value.
Usage frequency may be a fallible local ranking signal, but cannot decide proof
validity. Duplicate and complementary assets must be evaluated at the capability
level rather than rewarded automatically by theorem counts. No global task list
or human-intention metadata is required by these definitions.

## Explicit data contract

The pure helper has this interface (installed pinned schema reads are inherited
from the existing capsule codec; it does not open agent-supplied paths):

```text
assemble(plan_raw, expected_capsule_raw, semantic_contexts,
         registry, foundation_witness)
    -> (packet_bytes, target_name_index, exact_capsule, assembly_record)
```

The plan is strict JSON with exactly four fields:

```json
{
  "schema": "DMKN_EXPLICIT_APPLICATION_PLAN_V1",
  "expected_capsule_sha256": "64 lowercase hex digits",
  "graph": [],
  "proof": 0
}
```

`graph` contains only the existing explicit name, level and expression DAG rows.
It has no source text, imports, elaborator actions, metavariables, declarations,
new axioms or definition bodies supplied as a declaration. `proof` selects its
expression root. `app`, `lam`, `forallE`, `letE`, `bvar`, explicit universes and
the other existing supported expression constructors are available. Every term
argument and universe argument is explicit. The separate canonical expected
capsule gives the output name, ordered universe parameters and complete type.
Its exact supplied bytes must have the plan's hash, and its reprojected output
must equal the independently supplied canonical capsule.

Contexts are bounded, exact capsule objects taken from operation snapshots.
They are *not* acceptance evidence. Foundation declarations come only from the
registry-authenticated complete fixed witness. Selected semantic definitions
retain exact canonical values. Selected proposition interfaces become temporary
assumptions in this candidate only. Existing workflow authentication and proof
composition must discharge every such assumption into either a genuine certified
frontier or an actual substituted fragment proof before final acceptance.

Ordinary conditional hypotheses remain lambda/forall binders: proving `P -> Q`
does not require proving P. This is distinct from leaving an acquired unsealed
theorem as an unauthorized global axiom. No output may collide with a foundational
or selected-context declaration name.

## Structural obligations and assurance

1. Reject unknown fields/tags, duplicate JSON keys, floats, forward references,
   duplicate structural nodes, out-of-range indices and exceeded byte/work caps.
2. Bind each context and foundation declaration exactly; reject conflicting
   owners of a name. Include proof-only selected definitions, not just definitions
   appearing in the output type.
3. Validate free-variable closure using `(expression index, binder depth)` states.
   `letE` binds only its body. No bvar shifting or expression substitution occurs
   in the assembler, so structural interning does not change lexical scopes.
4. Restrict plan universe parameters to the ordered target parameters. Check exact
   constant universe arity against all authenticated declaration headers, including
   foundation constructors and recursors. Never infer or fill missing universes.
5. Only known foundation/selected-context names may occur as plan constants or
   projection type names. A known projection name need not be a valid structure;
   actual type and projection correctness remain final-checker obligations.
6. Emit one output theorem with the separately supplied type and plan proof.
   Reproject and compare the full exact output capsule after assembly and again
   after fragment substitution. Record hashes and structural counts, never PASS
   mathematical authority from successful assembly.
7. Verify frontier receipts and execute the pinned full final guest relation.
   Refuse invalid application, wrong argument types, mismatched premises and
   malformed proof even if all structural checks passed.

The final guest acceptance relation is unchanged. The old source route additionally
ran conditional native Lean authoring; the new route does not. It must advertise
**guest-checked output**, not unchanged two-checker/native-authoring evidence.
Soundness remains conditional on the adopted foundation, guest implementation,
receipt system and host/runtime assumptions. A target hash is a formal request
binding, not a representation of human intention.

## Bounds and limits

Let S be total bounded input bytes; V and E be the actually processed graph nodes
and reference edges across plan, expected target, contexts and fixed witness; W
be distinct `(node, depth)` states inspected for closure. Name/string lengths and
schema arrays have existing finite caps. Parsing, structural checking, hashing,
reference remapping and interning use O(S + V + E + W) operations under standard
expected constant-time hash-table assumptions, with hash cost charged in S.
Implementation work counters also bound scheduling of repeated pending edges;
the byte cap alone is not presented as an operational CPU timeout.

No term substitution is done in this helper. Existing fragment composition has
separate bounds for distinct universe-specialization states; it cannot claim an
O(input DAG nodes) bound for arbitrarily many instantiations. Encoding DAG sharing
does not imply evaluator memoization. Full type checking may be expensive and
must retain its separate CPU/memory limits. Reaching a limit is safe refusal,
not a proof of nonderivability or lack of useful mathematics.

The new operation is confined to the currently adopted foundation and semantic
definition profile. It does not solve the separate broader compositional-definition
limitation, semantic matching, decentralized completeness, or global availability.

## Full-cost comparison and an honest benefit region

Compare the same exact target and accepted final relation, against the actually
available source route, not against an imaginary agent with no local library.
For use i, let common cost C_i include discovery, acquisition, applicable profile
adoption, authenticated frontier verification, storage/retention, and the shared
part of final checking. Let H_i be native authoring/import/export/bridge cost;
B_i be explicit bounded assembly; A_i be extra formal-plan construction/adaptation
relative to the source route; D_i include any changed final guest/composition
cost, maintenance or deployment overhead. A_i can be negative but is never silently
set to zero. Charge one-time plan/tool construction and incremental adoption K.

```text
source total = sum_i (C_i + H_i)
plan total   = K + sum_i (C_i + A_i + B_i + D_i)
net saving   = sum_i (H_i - A_i - B_i - D_i) - K
```

Hence a specified finite workload is strictly cheaper **if and only if** the
last expression is positive under the chosen complete cost accounting. This is
an identity, not yet a speedup theorem. If justified per-use bounds give
`H_i - A_i - B_i - D_i >= d > 0`, then every supported workload with `q*d > K`
is a sufficient net-benefit region. q counts actual selected uses; no unknown
demand or inevitable future adoption is assumed. If measured/derived d is not
positive, the source-free API has not established a net-growth advantage.

There is already a separate deterministic resource distinction: the old receiver
hashes approximately 5.185 GB of installed assets per operation; the selected
receiving closure model hashes approximately 692 MB at the same seven validation
boundaries. This is a strict reduction in selected validation byte-work, not a
measured CPU speedup and not by itself mathematical growth. Changed scope is
valid only under the execution/read-closure invariant in OPERATION-COST-MODEL.
New plan/context bytes, validation, plan construction and resulting checker cost
must still be charged. The mathematical repeat-use inequality has a nonempty
conditional region once an actual positive margin is established; claiming that
the real system occupies it requires the targeted comparison below.

For an independent proof-search baseline, let R_i be the *specified* local
procedure's derivation cost and U_i the complete shared reuse cost. The analogous
criterion `sum_i(R_i - U_i) > K_shared` is valid. No positive R_i lower bound is
asserted for optimal agents. The prior repeated-squaring operation-count result
concerns named algorithms only, and cannot supply missing software constants or
prove growth in novel mathematics.

## Required consequential evidence, not a large benchmark campaign

- Independently inspect exact new helper and workflow delta, including target
  substitution, binder-depth reuse, wrong universes, unknown names, exceeded work,
  proof-only definitions, and incomplete imported assumptions.
- One generic parameterized composition using real acquired inputs should traverse
  the new public action and unchanged final guest, then be independently received.
  A valid wrapper alone is conformance, not new useful knowledge.
- Invalid but structurally valid proof must reach the real final checker and be
  refused before export. Unit rejection is not a substitute for this boundary.
- Account for the removed native stage and all changed setup/assembly/checking
  work. Reuse preserved baseline evidence only when inputs/endpoint/measurement
  scope justify comparison; otherwise report unmatched costs explicitly.
- Produce the applicable numerical or symbolic break-even region, with actual
  positive margin evidence and construction/adaptation charged. Do not turn an
  unmeasured conditional inequality into the claim that v4 growth is solved.

The concrete next deliverable is an executable ordinary proof-term contribution
route plus a justified operating envelope. The broader deployment and growth goal
remains open if its lower-cost accepted use has not been established.
