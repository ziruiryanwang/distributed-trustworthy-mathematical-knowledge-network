# Persisted withdrawal: source implementation checkpoint

Fresh source only, under the root's TRUST-WITHDRAWAL-SELECTION. Predecessors
are unchanged. No tests, product imports, native/guest/prover execution, builds
or Git operations were performed by this author.

## Implemented boundary

`software/v5/trust_withdrawal/admission/trust.py` implements the agreed API:
`support_id`, explicit create-only `TrustDomain.create`, existing-only `open`,
registered exact-class `bind`/`check`, checked `identity`, `check_binding` and
create-only `withdraw`. A canonical bounded immutable `ADOPTION.json` identifies
one domain and whole-runtime support manifest. Missing/corrupt/replaced/redirected
state refuses. Any `WITHDRAWN` entry denies without interpreting its contents;
observed denial stays latched in the live domain. New writes use exclusive
creation, flush and fsync; write failures propagate, with partial marker denial
preserved. Existing markers need no rewrite and do not claim a new flush.
Domain registrations use weak references, so expired profiles do not accumulate
forever; live profiles and issuers retain their original binding strongly.
No reset, automatic reprovisioning, deletion or authority-from-report path exists.

Support records contain exact relation/aggregate/foundation/policy/scheme IDs
and at most 512 stable role rows, under 128 KiB and 8 GiB summed role bytes.
The runtime author binds the selected static supervisor manifest as one role;
its complete Python census is transitively committed, not redundantly flattened.
Selected source/runtime/helper roles remain explicit. Generated preparation
profile digests, operation budgets and absolute runtime paths are not support
identities. Source validation is performed by the runtime factory, not asserted
by this generic digest helper.

The fresh `admission/verifier.py` succeeds the actual runtime_efficient owner.
Mandatory `trust_binding` enters its profile identity. Liveness retains and
checks the original binding/domain, loaded helper module/origin and persisted
identity. The helper source must be in runtime pins. Denial uses an internal
busy-safe revoke that clears handles; it never calls public close while busy.
Direct describe also has a final live gate before returning copied facts.

The fresh `aggregate_claims/aggregate_admission.py` forwards the same mandatory
binding before base initialization, pins the helper origin and includes trust
identity in its separately replaced aggregate profile hash. Existing aggregate
revoke clears aggregate/member handles and member cache. Existing mixed-owner,
session, cache and post-authoring liveness propagation is reused; no unnecessary
preparation overlay was added.

## Assumptions and exact scope

The owner/controller/OS remain trusted. Acceptance linearizes at the final
owner-serialized guard read; withdrawal linearizes at marker creation. A worker
may finish after withdrawal, but its post-worker gate refuses the result. No
instant cancellation, cross-process atomic recall, whole-directory antirollback
or hardware/power-loss guarantee is claimed. A complete record left after a
failed create acknowledgment may later validate on explicit open; the failure
is not rewritten into an acknowledged successful/durable create. Incomplete
records are unusable, and no recovery happens implicitly.

No mathematical statement, verifier policy or cryptographic assurance changed.
This closes a concrete local trust-update design gap, not full secure update
distribution or the whole v5 release. Independent source/changed-boundary review
and root-selected finite execution remain required.

## Initial source identities

| File under `software/v5/trust_withdrawal` | SHA-256 |
|---|---|
| `admission/trust.py` | `a60fd123845c7cd732967f995363b3132ebab1522cd90870ab728e6a54dd83ee` |
| `admission/verifier.py` | `01fb93b5d0063110fe82978dcc8a593557b34eaa8b6497f596715ca65064e38c` |
| `aggregate_claims/aggregate_admission.py` | `2ef830f849ff214b4e4b3c314332d8d3d3d23844c1a763828e1be5a5f37732aa` |

Cross-read of the complete fresh runtime found support normalization and I/A
forwarding consistent. The runtime author was asked to add an explicit
binding-to-original-domain identity check without a duplicate metadata read.
Independent author cross-review read all 11 reviewer controls and both source
selectors. No blocking source finding: fixture fields match the actual owner
and grant interfaces; the actual I.receive post-worker gate refuses before the
patched binding callback can run. Controls assert retained charges, no handle
minting and busy-safe cleanup. Native entry points are explicitly blocked;
these inert shells/operational-closure fixtures are not receipt acceptance.
The source-only controls selector preserves its exact predecessor graph and
sets 30 CPU / 60 wall seconds, 256 MiB. The separate actual selector validates
the existing 108-source SDK, replaces four sources and adds one helper, plus
one genuine-receipt adapter, without copying or rebuilding runtime assets.
The actual adapter's public failure entry clears caches and closes originals;
its retained receipt count is one, not a new proof. Neither selection nor this
review asserts execution or adoption. Root owns those decisions and outcomes.

Reviewed selector hashes: `Select-TrustWithdrawal.ps1`
`a90dc623eaa260294c191e12566849808d612e66137306f1b53cf7e87c24d856`;
`select_withdrawal_actual.py`
`5f9bd42bef62f8b35a5c58069941f5c3db16aca9d793f29ae5b967f4c644d517`.
Final controls source `748bd8bd6ddeed3680c74f67ef84f5e9fa62427af8f1943c6f2d8ccebec6dfef`
adds one source-reviewed forged binding with an actual domain pointer but no
registration; `check_binding` must refuse `TRUST_UNREGISTERED_BINDING`. This
distinguishes actual membership enforcement from only a missing-attribute check.
