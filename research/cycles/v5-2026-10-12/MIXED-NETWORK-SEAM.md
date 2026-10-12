# Mixed certified frontiers in the reciprocal network

2026-10-12. Root source design, before changed-boundary implementation/tests.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
The full v5 goal is ACTIVE. This seam is not release acceptance.

## Problem and invariant

The existing formal index already identifies semantic modules independently of
their proof representation. The used network path stores only legacy-I/native
delta packets. The used mixed receiver can check bounded native extensions above
typed I/A frontiers, but the network cannot yet deliver those packets to it.

For semantic module M, a locator is an untrusted pair (wire profile, blob hash).
Storage and transport establish only exact bytes and structural target binding.
Only the independently configured, still-live MixedDeltaVerifier may establish
mathematical authority. Proof representation changes must not change ModuleID,
formal feature extraction, query coverage or grant additional search resources.

The one-A profile stays explicit: fixed I/foundation/policy and one adopted A.
This is not arbitrary image trust or the future compatible-image mechanism.

## Smallest implementation

Use fresh `software/v5/mixed_network/{__init__,custody,transport}.py`.
Do not edit used delta/network, mixed parser or mixed verifier sources.

Reuse the existing delta HTTP routes: offer requests contain a wire-profile ID;
blob requests contain only exact digest and size, and responses are opaque bytes.
Offer validation plus local packet parsing enforce the profile, not the raw blob
endpoint. A distinct canonical profile
and offer schema discriminate mixed packets. An old provider refuses an unknown
profile; an old client refuses a mixed offer. A deployment chooses its profile;
this first seam does not add implicit content negotiation or automatic fallback.

- Custody: new exact mixed profile, schema and database name. Reuse frozen
  PacketStore's transactions/quota accounting/get/status/close methods through a
  subclass, with explicit new initialization, inspect and offer. Inherited put
  dispatches to the new inspect. Old exact-type admission gates reject subclass.
- Parsing: use the already tested mixed packet parser with locally selected A,
  enforce target ModuleID, and never decode receipt payloads in storage. Parsing
  binds member openings and fixed relation/policy but does not prove a receipt.
- Provider: subclass the old composite provider, replace only role/profile
  construction. Retain its exact bounded HTTP framing and dispatch. Mixed store
  offers supply the distinct mixed schema/proof form.
- Acquisition: inherit unchanged original handoff, location/search grant,
  exact-hash acquisition, structural semantic custody and live-origin mechanics.
  Override construction, mixed-offer validation, admission and result labels.
  Configure exactly MixedDeltaVerifier, not duck-typed authority.
- Charge cryptographic work per *claim*, not per selected member/frontier:
  `claims * receipt_cpu_cap + deltas * native_cpu_cap`. Match the mixed receiver's
  existing conservative reservation; do not refund cache hits or failures.

These are explicit narrow subclasses of frozen mechanical code, not monkeypatches
of global constants. Before implementation adoption, independently review every
inherited method for hardcoded old semantic assumptions. If a method embeds an
old proof-form/schema requirement, override it; do not trick the old validator.

## Local obligations and sufficient tests

1. New/old wire profiles and offers cannot be confused. A/profile mutations,
   invalid member openings, wrong target and old packet schema refuse.
2. Exact packet bytes survive transaction, reopening and original provider loss;
   changed bytes refuse. Store insertion and download never grant authority.
3. Same original aggregate acquisition budget/deadline covers search, framing,
   replies and admission reservation; no renewed allowance per provider/member.
4. Only the exact live mixed verifier can admit. Final selected group/summary
   matches the semantic index opening, with origin checks before promotion.
   Revalidate the exact handle after structural readback; checking the network
   deadline alone does not detect expiration of the mathematical owner.
5. One bounded synthetic loopback acquisition is sufficient for changed transport
   plumbing. Reuse prior actual unknown-ID routing evidence rather than rerunning
   that campaign. Synthetic receipt bytes do not qualify mathematical acceptance.
6. Actual A receipt integration remains a later explicit gate once one exists:
   BASE+FIRST frontiers, newly authored SECOND; no old FIRST witness/I receipt
   below the cut. Reuse the already specified AGGREGATE-PUBLIC-ADMISSION workload.

## Scale and growth scope

Index and routing costs are unchanged by replacing the packet representation.
Transfer/admission cost depends on selected claims/member paths, bounded unsealed
deltas and demanded semantics, not mandatory ancestral theorem proofs. Packet
limits refuse too-large closures; they do not assert every theorem fits.

Shared packet storage still duplicates a large receipt across different packet
blobs. Existing bounded aggregate claim deduplication is intra-packet only. Cross-
packet receipt deduplication/content-addressed manifests are a future measured
optimization, not necessary for this sound transport seam. No claim of indefinite
exponential knowledge growth follows from successful packet transfer.

Public hostile-input isolation, cross-image revocation, installer/update/recovery,
rights and independent-host operation are unchanged open release obligations.

## Status

Root selects source implementation of the three fresh files only. No network,
proof or test run is selected yet. Existing source/evidence stays frozen.

Independent source review found no inherited old-profile trap. Root repaired
the final live-handle recheck and clarified the unprofiled exact-blob route.
Seven fresh synthetic controls target these changed boundaries.

### Actual changed-boundary result: independently adopted

Root ran exactly the reviewed selection `3273d116a942916cb3f57b5ad4441f37cbba0edb0950034483f61e11c30bf331`
under `experiments/v5-local-checks/mixed-network-controls-01`. All seven groups
passed; one loopback provider served exactly three requests following two prepaid
grants. It then stopped, and exact packet bytes remained available in reopened
local custody. No native/guest/cryptographic work was performed.

- Outer RESULT: `f026936975bc5c0ae022e2cab95619e5c4182470134edd2ed2849246be6aa831`.
- Inner RESULT: `4e490df100b83e20260539f0d333e7f8a04776efc8570d989951e356d0263b09`.
- Seven-group log: `45e8a3d6` (full digest in the independent ASSURANCE checkpoint).
- Inclusive worker Job CPU: 0.984375 seconds; disjoint wrapper: 0.296875 seconds;
  outer wall: 2.3894802 seconds. Clean exit/reap/closure; zero active processes.
- Independent audit checked 96 current/snapshot bindings and exact selection/argv.

The four used Python sources and selector are frozen. Do not rerun this passing
campaign. The actual A mathematical admission and network contribution gate stays
open; these controls explicitly use fake receipts and cannot close that gate.
