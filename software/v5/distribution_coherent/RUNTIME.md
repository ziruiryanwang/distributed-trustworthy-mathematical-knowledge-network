# Ordinary local runtime construction with explicit trust

`client.runtime.RuntimeProfile` constructs the existing real client owners
without requiring a particular theorem, receipt, fixture directory, phase,
port, or experiment script. It creates no mathematical authority by itself.
The caller remains trusted local code inside the existing launcher and its
enclosing Windows Job; resource containment is not a hostile-code sandbox.

## Explicit adoption is a separate owner action

The consolidated runtime requires `admission.trust.TrustDomain`. First review
and adopt the installed release and the support it selects. In a SEPARATE trusted
`run` entry, supply `runtime_adoption={"$installed":"runtime_adoption"}` and an
explicit fresh persistent policy directory/domain ID:

```python
from admission.trust import TrustDomain, support_id
from client.runtime import RuntimeProfile

support = RuntimeProfile.support_manifest(context, context.parameters["runtime_adoption"])
expected_support = support_id(support)
TrustDomain.create(fresh_policy_directory, owner_selected_64_hex_domain_id, support)
trust_configuration = {"directory": str(fresh_policy_directory),
    "domain_id": owner_selected_64_hex_domain_id, "support_id": expected_support}
```

Persist that three-field configuration in owner-controlled files. The directory
parent must exist, and the policy directory must be separate from installation,
operation trees and mathematical workspace. `support_manifest` itself creates
no domain, verifier, mathematical authority or allowance. Its identity binds the
selected SDK/checker/Lean/producer support, not per-run paths or strategy code.

Ordinary startup NEVER calls `create`. It opens the existing exact directory and
IDs; missing, changed or withdrawn policy fails closed. Do not turn failure into
a new adoption or delete withdrawal state. Changed software/checker support
requires deliberate new adoption. `domain.withdraw(reason)` persists local
denial with no reinstate API. Checks observe withdrawal at the next live gate;
they cannot recall returned bytes or instantly cancel already-running workers.
See [the policy contract](../trust_withdrawal/TRUST-WITHDRAWAL.md).

## Ordinary runtime construction

The launcher must already select `client/runtime.py` and the complete imported
SDK closure. Digests come from its selected source map. Runtime construction
checks those digests against actual snapshot bytes; it never discovers arbitrary
code and then treats its freshly computed hash as adoption.
Profile loading checks the factory, producer and authoring-worker minimum source
set; the unchanged concrete owners reject any missing deeper mode-specific
closure during operation construction, before ownership transfers.

```python
from admission.trust import TrustDomain
from client.runtime import RuntimeProfile

trust = boot_context.parameters["trust_domain"]
domain = TrustDomain.open(trust["directory"], trust["domain_id"], trust["support_id"])
runtime = RuntimeProfile.from_context(boot_context, {
    "schema": "DMKN_V5_CLIENT_RUNTIME_V1",
    "preparation_profile": locally_adopted_profile_pin,
    "native": locally_adopted_native_checker_pin,
    "receipt": locally_adopted_I_verifier_pin,  # None in A-only mode
    "aggregate": None,  # or {"executable": A_verifier_pin, "image": adopted_A_image}
}, trust_domain=domain)
```

Every pin has exactly `path`, `bytes`, and `sha256`. Paths are absolute ordinary
local paths, selected by the owner, never by a peer. The preparation profile is
the existing `DMKN_V5_PREPARATION_PROFILE_V1` data format. It is required even
for a reader because its producer subprofile supplies the adopted supervisor
and embedded-Python runtime roles. Its receipt-production `host` is not silently
used as the receipt verifier: `receipt` and `aggregate` select those separately.

The producer's manifest-bound Python, Python DLL and runtime rows are rebased
to `boot_context.installation` only after checking their exact unchanged
manifest entries. The source rows and authoring worker are rebound to the
actual launcher snapshot. External preparation-host, Lean, guest-image and
frontend paths retain the exact profile's pins: relocating those assets requires
an explicitly adopted profile pointing at their new locations. This helper
does not itself package those assets. The installed distribution separately packages
and pins its selected support roles; this establishes no cross-platform support.

`runtime.describe()` returns a deep-copied configuration for inspection. It is
not a credential and cannot recreate a receipt, live warrant or consumed grant.
No mathematical bytes are part of runtime construction.

## Reserve, construct, then use the existing client

```python
grant = workspace.reserve(operation_limits, outer_deadline=boot_context.deadline)
client = runtime.open_operation(
    workspace, grant, mode="atomic", authoring=True,
    foundation_bytes=foundation_bytes,
    foundation_sha256=foundation_sha256,
)
try:
    # Existing admit_receipt/admit_local/acquire/import_context/author/publish APIs.
    ...
finally:
    await client.close()
    workspace.close()
```

The explicit modes select exact existing Workspace classes:

| Mode | Workspace module | Required issuer configuration |
|---|---|---|
| `atomic` | `client.workspace_atomic` | I present; A absent |
| `mixed` | `client.workspace_mixed` | A present; I optional |
| `evidence` | `client.workspace_evidence` | A present; I optional |
| `staged` | `client.workspace_staged` | A present; I optional |
| `validated` | `client.workspace_validated` | A present; I optional |

Missing or mismatched A never falls back to I. Modes do not migrate stored
schemas, mint certificates, or select research questions. The existing issuer
constructors and Workspace operation verify required loaded-source origins,
exact issuer pairing, profile identities, original deadlines, pristine counters
and applicable source closure. A mode's module must be in the selected launch
closure; no unselected import is enabled by the mode table.

All owner ceilings derive from the original grant. Admission owners share the
acquisition worker allowance; these nested ceilings are not additive CPU
allocations. Native admission receives at most the original public admission
count, capped at 128 calls. Each receipt issuer can service up
to the original count times the packet envelope's maximum claims (at most its existing
4,096-call ceiling): one mixed packet may contain several distinct certified
premises. Receipt CPU and submitted-byte ceilings are unchanged shared limits,
not multiplied by the claim count. Preparation receives only
the positive difference between total and acquisition worker budgets, capped
at its existing 3,600-second/16-call limit. The original grant still enforces
overall calls, input, output and controller limits. Preparation has its existing
600-controller-second/1-GiB/4,096-entry ceilings. No sublimit is raised and no
failed operation is automatically retried or refunded.

Remaining time is recomputed before each owner is constructed. Outputs are the
fresh `grant.directory/delta` and `grant.directory/preparation`. The grant must
belong to the selected workspace and end no later than the launcher's deadline.
The caller chooses storage configuration and limits; a numerical maximum is
not a workload recommendation.

Ownership transfers only when `workspace.operation` succeeds. On failure the
factory attempts to close every owner that it successfully constructed, even
when one close raises. It preserves the original error and cleanup errors in a
`BaseExceptionGroup` and poisons the workspace when cleanup is uncertain.
The caller must still close the workspace and require enclosing Job closure;
this constructor cannot reclaim an object whose own constructor raised before
returning it. Existing constructors must retain their own failure safety.

## Paired indexes and evidence boundary

For ordinary evidence/staged/validated use, the legacy evidence workspace schema
keeps its original namespace. The optional
`DMKN_V5_CLIENT_EVIDENCE_CONJUNCTION_WORKSPACE_V1` adds an immutable
`discovery_profile` with 1..8 canonical atomic pairs. Providers and consumers
must adopt the same profile. Use `workspace.adapter.compile_query(specs)` for
route keys. A changed profile requires a fresh workspace; no hidden migration
or cross-profile fallback exists. The mathematical runtime owners are unchanged.

Retained constructor, genuine receipt-withdrawal, interface-only import and
pair-index controls cover their respective selected sources, not every later
package or deployment. Consolidated builder and installed integration require
their own exact saved evidence. Do not run a historical `runtime_check` caller
that omits mandatory trust: its old parameter schema is not this startup API.
No new theorem/proof or performance benefit follows from runtime construction.

This guide and source do not establish final v5, independent hosting/security
review, recurring economical certification or positive full-cost growth.
