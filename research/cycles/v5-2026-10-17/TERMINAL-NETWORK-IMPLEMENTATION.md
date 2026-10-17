# Two-form evidence network: source implementation checkpoint

2026-10-17, `memo_tests_review`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root selected only four new `software/v5/evidence_network` files and these
design/implementation notes under TERMINAL-IMPLEMENTATION-SELECTION.md.
Guard passed; existing source was read before specialization. All original
mixed/aggregate/atomic/transport source and used evidence remain unchanged.
No imports, tests, native calls, proofs, builds, services or Git were performed.

## Author-ready source pins

| New file | Bytes | SHA256 |
|---|---:|---|
| `__init__.py` | 167 | `bc68b38fd0564ba8f32bc32399e2ad11f874cd563f6d0b1746f61a6d1811d61e` |
| `packet.py` | 5192 | `b4080ed8d8c0438079a1291a7493dea9df863d269b7eea35e32b4be961d9188d` |
| `custody.py` | 7116 | `38246a2892e8a14f74c6e78e7c25d1d70ffbe26269c59c71e5436623bd5ef73c` |
| `transport.py` | 5585 | `f4734bff9bdfd2ac3fc7ae770a9bc3f0d4b6e47a41ab60fd65fa21ab50f7b880` |

These pins are ready for independent review, not a runtime qualification.
Later narrow source corrections need new pins before root's exact selection.

## Concrete API agreed with client author and root

```python
parse_terminal(raw, envelope, *, aggregate_image, terminal_receipt_bytes=8*MIB)
# -> receipt, H, J, index, tuple_siblings, member
inspect_evidence(raw, envelope, *, aggregate_image, terminal_receipt_bytes=8*MIB)
# -> kind, summary, J, census
pack_terminal(header, journal, index, siblings, receipt, *, aggregate_image,
              envelope, terminal_receipt_bytes=8*MIB)
# -> canonical bytes, revalidated structurally
PacketStore(root, profile, limits, *, envelope=None,
            terminal_receipt_bytes=8*MIB, create=False)
EvidenceAcquisition(adapter, endpoints, profile, budget, module_custody,
                    packet_custody, *, verifier=None)
```

`envelope` is the existing exact mixed Envelope; no new envelope class.
`public_profile(A)`/`profile_id` define one closed mixed-or-terminal profile.
`EvidenceAcquisition.from_search` preserves the old one-shot handoff ABI and
requires verifier=None. `declaration(provider,module,name,max_bytes)` wraps the
real existing same-contact semantic group request with storage/readback.

## Proof and authority boundaries

The packet dispatcher accepts only unchanged mixed schema or the distinct
canonical terminal schema. Mixed parsing delegates to the retained parser.
Terminal parsing binds the real existing H/J/index/path grammar but never
verifies a receipt. ModuleID and exactJ are distinct; both are returned for the
client's exact-target checks. Encoding also calls the parser, not a verifier.

The terminal receipt cap is1..8MiB, raw envelope at most configured mixed
packet cap (at most32MiB). Hex overhead counts. The direct A verifier's64MiB
input range is not falsely advertised as a transport guarantee. The C JSON
decoder's actual raw-byte behavior is documented; no nonexistent node/depth
census is claimed. Fixed field/array shapes bound post-decode work.
Independent source review queried lowered mixed-envelope rank policy. The
terminal branch now explicitly enforces the same configured rank ceiling in
addition to H's authenticated maximum. This107-byte localized correction is
the only change from initial packet pin37b6e52e; all other source pins remain.

New custody overrides constructor/inspect/offer only; legacy immutable blob,
quota, transaction, readback and close/status methods are reused. The new
database/profile/config is not a migration. Both forms consume one store quota.
Provider constructor alone is profile-specific; shared route ABI, framing,
limits and dispatch remain unchanged. Historical delta URL spelling does not
establish mathematical proof form.

Acquisition is structural-only. It cannot accept a verifier, callback or issuer;
`admit` always raises `PUBLIC_CLIENT_ADMISSION_REQUIRED`. It never reserves
verification work. The ordinary client alone dispatches actual mixed/A receipt
admission through its common original grant and receipt cache. Acquisition
does not fabricate a verified handle or duplicate client-side receipt checking.

`from_search`, `_active`, `_get`, `body` and `custody_ready` reuse existing neutral
algorithms. Construction/offers/assurance text/report are specialized. `close`
is a deliberate tiny override: pending/inflight checks and original budget
closure remain, but no object later assigned to `verifier` is closed because
this structural acquisition never owned an issuer. This avoids inheriting an
unowned callback path without adding a new lifecycle framework.

Demanded declaration acquisition invokes the existing real structural endpoint,
then commits/reads back the exact opening and descriptor. It is explicitly
labelled a declaration demand, not an index-discovered result or mathematics.
Its bytes/requests use the same `_SharedAcquisition` budget/contact policy.

## Still required

Independent source review and root's exact changed-boundary controls remain.
Root owns all execution and original/source snapshot pins; client owner owns
workspace_evidence integration and public terminal publication/reconciliation.
Actual A production, genuine semantic import, unknown-ID terminal acquisition,
substantive extension, supplier-offline reuse and full-cost benefit are open
gates. No successful low-level component is relabelled as final v5.
