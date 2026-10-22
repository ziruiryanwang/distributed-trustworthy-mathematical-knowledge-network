# Ordinary renewal from a genuine typed aggregate frontier

2026-10-22, storage_integration_adapter. Source-only plan, not execution or
adoption. Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root owns source selection, finite launches, trust adoption, funding and Git.

## Decision

Only a small owner strategy and V source input are missing. Reuse the existing
client/import/author/seal APIs below. Its prerequisite is a **future genuine
resolved A*(H_U) receipt**; retained general36 execution and conditional native
fixtures are not that receipt. No consumer rewrite or new network campaign.

| Binding | Selected identity |
|---|---|
| Aggregate image A* | `9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865` |
| Underlying module-relation image I | `9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e` |
| U module | `ad0cc7c499ec6ca71cd211733c3f566f417b4d86a6064292510b927c4eb122c3` |
| Exact U journal SHA-256 | `0ba261cd27c816223aa56bc6cbe217e67f48264b8d1c707326095492620a1657` |
| U / V names | `RC0.context_transport` / `RC0.context_transport_then` |

U transports component equalities through `f (g a b) (h b c)`. V appends an
equality to `d` using exactly `Eq.trans (U ... ha hb hc) hd`. Both have four
universes; ranks are1/2. U's type uses foundation constants/bound variables
only: its group0 opening suffices, with no transparent body or BASE import.

## Reuse these sources and fixtures

Current130-entry source map: `experiments/v5-local-checks/distribution-candidate-preflight-01-input.json`
(SHA-256 `25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364`).
Under `software/v5/`, the relevant successors are:

- `trust_withdrawal/client/runtime.py`: current TrustDomain bootstrap.
- `candidate_preflight/client/workspace_evidence.py`: A-member admission/import.
- `continuing_context/client/workspace_atomic.py`: ordinary authoring.
- `continuing_context/mixed_claims/imports_atomic.py`: terminal A frontier/onward packet.
- `interface_views/authoring_atomic.py`: actual source-derived V witness.
- `aggregate_claims/prepare_mixed.py`: unchanged exact seal preparation.
- `typed_production/producer.py`: source-side producer inherits generic prepare/snapshot.

`restricted_composition/fixtures.py::frame(..., continuation=True)` specifies V.
Retained `experiments/v5-local-checks/restricted-composition-controls-01/evidence/fixture.json`
(84727B; SHA-256 `019219ca4548dafbdaa814c209a4ec087229091750db3f3cf48fcc155269f40a`)
contains `second`/`second_witness` comparators. Extract only U's group0 opening
and V's expected specification/proof-edge description; do not give the fresh
consumer the whole fixture, which also contains U's witness.

## Minimal ordinary operation

Root selects fresh paths, exact pins and finite limits. Explicitly adopt A* in
runtime, workspace wire profile and TrustDomain. Current runtime permits
`adoption["receipt"] = None` with aggregate/validated mode: use it to eliminate
the I-verifier dependency, while retaining native checking and foundation pins.
Compose these existing calls with exception-safe cleanup:

```python
support = RuntimeProfile.support_manifest(context, adoption)
domain = TrustDomain.create(fresh_domain_path, domain_id, support)
runtime = RuntimeProfile.from_context(context, adoption, trust_domain=domain)
# Existing Workspace.open(...), reserve(...): finite limits, fresh state.
client = runtime.open_operation(workspace, grant, mode="validated",
    authoring=True, foundation_bytes=foundation,
    foundation_sha256=foundation_sha256)
warrant = client.admit_aggregate_member(receipt_U, H_U, J_U, k_U, siblings_U,
    **receipt_limits)
imported = client.import_context(
    [{"warrant": warrant, "resolutions": None}], [J_U],
    [{"module": U_module, "opening": U_group0}], [],
    definition_mode="interface-only")
prepared = client.author(imported["context"], V_source_text, [V_name],
    **authoring_limits)
raw_V = prepared["child"]["packet"]
# Store exact bytes via existing packets.put(..., before_commit=...).
# Independently admit_local(..., expected_exact_journal=predicted_J_V, ...).
# Compare client.describe(checked)["journal"] with the exact target.
```

Require READY, one imported group/declaration, zero imported bodies and
`frontend_theorem_ancestor_proof_bytes == 0`. Admission verifies the actual
receipt/membership; author output still requires independent `admit_local`.

The missing V source must use `modules.codec.relocated_name(U_module, FIRST_NAME)`
with the exact universes/binders and U-then-`Eq.trans` proof, not inline U.
Reuse `candidate_preflight/actual_owner.py` for current trust setup/cleanup only.
Old `examples/contribute.py` is not directly runnable: its `from_context` lacks
`trust_domain`, and `_local_import` assumes mixed-packet semantic material.
These two gaps justify the small owner adapter, not a new product API.
Existing `client.publish` is optional after checking; no repeated network test.

## Mandatory no-history and renewal checks

`imports_atomic._direct` stores U as `a-member-frontier` with no parent edges;
`onward_packet` stops there. With U alone selected, inspect actual output:

```text
claims    = [tag1(H_U, byte-identical genuine receipt_U)]
frontiers = [J_U with its exact H_U member index and siblings]
deltas    = [W_V]
W_V.parents = [J_U plus U's group0 opening]
W_V.bodies  = []
```

Require no tag0 claim, U proof/native witness, BASE journal or original I receipt
in consumer inputs/output. U's theorem-import row and fixed foundation rows
are expected. Compare V's exact specification/type/universes and decoded proof
edge with the fixture, not necessarily byte-identical frontend witness rows.
Predicted J is only a binding target; use the actual admitted J for sealing.

After actual local admission, the existing typed producer can call:

```python
seal = producer.prepare(raw_V, actual_J_V, envelope=selected_envelope)
```

Require only tag1 H_U/receipt_U in `parents`; each selected index tuple `(0,)`;
census claims1/frontiers1/deltas1/members2/edges1; sorted members `[J_U,J_V]`;
maximum rank2 and seal height2 if H_U height1. Preparation is not acceptance.

Later `producer.snapshot` is new A-parent work, not another U layout. Price its
actual graph before separately funded production. The gate is real A-parent
resolution into A*(H_V), then fresh V acceptance/import without U's proof; two
independent I-parent receipts do not pass. No producer/runtime launch here.

This closes a missing renewal capability, not certificate profitability or
sustained growth. Consumer work excludes compulsory ancestral proofs but still
includes selected interfaces, membership, certificate, foundation and new proof.
Only source/data inspection and this note were performed. Full-graph budget-fit
enforcement remains root's launch policy, not an inherited automatic rejection.
