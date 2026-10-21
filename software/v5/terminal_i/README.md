# Direct module certificates through the ordinary client

This source successor connects the existing individual module certificate
("I") to discovery, custody, staged semantic import and contribution. It adds
no verifier, proof producer or alternative mathematical trust rule. The selected
installation/source map, not this directory alone, determines the running SDK.

## Explicit capability

For a **fresh** workspace, choose the closed V2 profile:

```python
from evidence_network.custody import public_profile

config["wire_profile"] = public_profile(adopted_aggregate_image, terminal_i=True)
```

The default remains V1. Do not edit an existing workspace's stored profile to
upgrade it; no automatic migration is supported. The current runtime still
requires its configured I, A and mixed owners. Selecting the wire capability
does not itself adopt a mathematical policy or authorize any verifier.

| Packet kind | Meaning |
|---|---|
| `terminal-i` | One exact 184-byte module journal and individual receipt; V2 only. |
| `terminal` | Existing aggregate (A) certificate plus member opening; unchanged. |
| `mixed` | Existing certificate frontier plus checked native extensions; unchanged. |

`verify_offer(value, request, *, profile=selected_profile)` now requires the
selected profile explicitly, including for V1 callers. Its opaque profile ID
alone does not establish which proof-form label is allowed. Both internal
callers are updated; external callers of the former two-argument helper need
the keyword argument. V1 wire bytes and default interpretation stay unchanged.

## Authority and workflow

Use the same ordinary client: discover candidates, request evidence offers,
stage the selected packet and committed groups/bodies with `SemanticReader`,
resolve semantic demands, then finish admission/import. Already acquired bytes
can be used after the serving endpoint closes. Missing required semantics still
prevent completion: a certificate does not contain or recover those bytes.

For I packets, admission invokes the existing individual verifier. Its live
journal must equal the **entire** packet journal, including rank, even on a
same-live cache hit and even without a caller-supplied expected journal. Only
then can authenticated interfaces enter the unchanged sealed import session.
Store, index, preview and publication results alone grant no proof authority.

The imported live context can feed `contribute_from_context` for ordinary
authoring, independent child admission and publication. The resulting child
is normally a mixed/native extension, **not** a newly generated I certificate.
The inherited native tail still needs checking; this feature does not bound an
indefinitely growing uncertified tail or make advancing certificates cheap.

Closing or withdrawing an owner revokes its live authority, not retained public
bytes. A subsequent consumer needs its own policy adoption and checking. There
is no global mathematical task list, consensus ledger or human-intention gate.

The focused controls use inert issuers and establish API/binding/lifecycle
behavior only. Genuine installed receipt/import/contribution evidence has a
separate owner workload in `software/v5/examples/terminal_i/` and must be judged
from its actual audited outcome, not inferred from these controls or this guide.
