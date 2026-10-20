# Local adoption and withdrawal

This policy answers one question: **does this operator still trust this exact
checking stack?** It does not change theorem truth, revoke other operators'
trust, delete custody, or establish that the checker itself is correct.

Use the selected `admission.trust`, receipt/aggregate owner and client runtime
successors together. Their launcher source map must include `admission/trust.py`.
Old constructor calls without an explicit binding/domain now refuse; there is
no compatibility path that silently invents trust.

## Explicit first adoption

The owner first reviews a selected stack and chooses a persistent directory
outside temporary operation output. `context` and `adoption` are the ordinary
trusted launcher context and runtime configuration, not peer-supplied values.

```python
from admission.trust import TrustDomain, support_id
from client.runtime import RuntimeProfile

support = RuntimeProfile.support_manifest(context, adoption)
expected_support = support_id(support)
# An owner-selected 64-hex identity, retained in ordinary startup configuration.
domain_id = owner_selected_domain_id
domain = TrustDomain.create(fresh_policy_directory, domain_id, support)
```

This is an explicit adoption command, **never an error-recovery branch** of
startup. Keep the directory, domain ID and expected support ID in owner-controlled
configuration. Missing, changed or withdrawn state is not permission to create
a replacement. Deliberately adopting a different domain is a new trust decision.

`support_manifest` creates no domain, verifier, allowance or mathematical
authority. It uses the same configuration validator as runtime construction.
The identity includes relative names and byte pins of all selected SDK sources,
native/I/A checkers, author/producer roles, selected Lean runtime, I/A image IDs,
foundation and policy. The exact supervisor-manifest commitment covers its full
static installation file table, including the launcher's Python census; those
hundreds of rows are not redundantly copied into the support record.

Per-run paths, budget choices, owner strategy code, and the generated preparation
profile's raw digest are excluded. Its actual selected role contents are included.
Relocating unchanged roles therefore does not evade withdrawal. Existing owners
still check their actual executable/source bytes before use. These identities do
not claim a hermetic OS/DLL closure or give authority to a caller-asserted
incomplete role list: RuntimeProfile derives and compares the selected support.

## Ordinary startup and use

```python
domain = TrustDomain.open(policy_directory, domain_id, expected_support)
runtime = RuntimeProfile.from_context(context, adoption, trust_domain=domain)
client = runtime.open_operation(
    workspace, grant, mode="validated", foundation_bytes=foundation,
    foundation_sha256=foundation_sha256,
)
# Use existing client APIs. Always perform their usual cleanup.
try:
    ...
finally:
    await client.close()
```

Reopen the same policy directory on later process starts. Runtime construction
rederives the complete support and rejects mismatches. It retains its original
binding, which both I and A owners share; owner, handle, cache and post-worker
checks remain live. A source or cryptographic-stack change needs a deliberate
new adoption, not reuse of the old support identity.

The ordinary remote-reader example now requires schema
`DMKN_V5_REMOTE_READER_WITHDRAWAL_V1` and an additional `trust_domain` object with
exact fields `directory`, `domain_id`, `support_id`. It calls `TrustDomain.open`
only. Its existing `read(client, query)` helper still uses the supplied live
client; it neither opens nor adopts policy itself. The lower-level
`DeadlineReceiptVerifier` forwards `trust_binding` through its existing explicit
owner-adoption arguments. Historical frozen experiment callers are not rewritten.

## Withdrawal and precise ordering

```python
operator_domain = TrustDomain.open(policy_directory, domain_id, expected_support)
operator_domain.withdraw("The selected checker is no longer locally trusted")
```

The newly created marker is flushed before success is acknowledged. An existing
marker already means denial; idempotent withdrawal does not claim a fresh flush.
Any marker, including incomplete content, denies; ordinary restart cannot clear
it. Observed policy invalidity latches denial in the original object. There is
no clear/reinstate method. Inert reports and cleanup remain available, and costs
already charged are not refunded. Custody bytes are retained as data.

The owner serializes operations. Operation construction linearizes at the final
live check immediately before transferring owners to `workspace.operation`;
there is no intervening owner callback or await. Actual mathematical use checks
the original issuer again. A concurrent external-process withdrawal after that
construction check is observed at the next gate, not treated as instantaneous
cross-process cancellation. An in-flight worker can finish; its result must pass
the existing post-worker live gate. Already returned bytes cannot be recalled.

Trusted filesystem rollback, deliberate new-domain adoption and an adversarial
local owner are outside this local policy's guarantee. Missing/corrupt state
fails closed; it is not a recovery protocol or a worldwide revocation service.
