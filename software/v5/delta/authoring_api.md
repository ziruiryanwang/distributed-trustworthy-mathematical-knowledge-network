# Ordinary Lean authoring after native-delta acceptance

This fresh source is not yet runtime-qualified. It extends preparation, not the
mathematical checker or the cryptographic proof relation. It uses the existing
native Lean frontend and `OwnerPreparation` worker/resource controller unchanged.

## Public lifecycle

1. Construct the actual `ReceiptVerifier` and `DeltaVerifier` under the owner's
   fixed installation, profile, deadlines and finite allowances.
2. Obtain a real `VerifiedDelta` by `DeltaVerifier.receive(complete_packet,
   expected_summary)`. Saved reports and caller-created handles cannot replace it.
3. Construct `DeltaImportSession(verifier)`, then `use_handle(handle)`. More than
   one actual handle is supported, up to the finite owner cap. This registers its
   complete checked member inventory; it does not select all groups for authoring.
4. `open_group(module_id, opening)` for every selected imported declaration group;
   use `supply_body(module_id, universes, expression)` for exact committed
   definitions or recursor rules. The module can be any actual checked closure
   member, including a receipt-backed ancestor or an intermediate delta.
5. Construct `DeltaSourceOperation(session, foundation_bytes, foundation_sha256,
   owner_source, structured_roots)`. Its `prepare()` either returns finite typed
   context demands, or the ordinary fixed frontend request. Missing data does not
   trigger automatic downloads; extend the selection and construct a new operation.
6. Pass that SAME operation to `DeltaOwnerPreparation.author(...)`. It runs the
   existing pinned worker/frontend once, checks its exact returned bindings, and
   returns `UNTRUSTED_DELTA_PACKET_PREPARED`. `child.packet` is immutable complete
   onward-checking material; `packet` is the pin of its retained file.
7. A receiving owner must perform a new actual `DeltaVerifier.receive` to admit
   this child. Neither frontend success nor source export nor prepared bytes
   grant mathematical acceptance.

The first actual target is the retained receipt-backed `ReceivedFoldMap` child
from `receipt-source-integration-01`, not a substituted toy. Actual launch and
finite selection remain root-owned and are not performed by this module.

## Why this is a separate API

`VerifiedDelta` is not `VerifiedModule`; a delta packet is not a succinct receipt.
The receipt-only classes and their exact-class gates remain unchanged. No fake
`ImportClaim.receipt_hash`, fake receipt witness or `parent_receipts` is produced
for delta parents. The ordinary frontend receives proof-form-neutral interfaces;
the later receiver independently establishes their authority.

The session revalidates its SAME originating verifier, profile, actual member
inventory, exact packet hash, and deadlines. Operation selection additionally
binds all opened groups and supplied bodies. Closing the verifier/session,
changing its selected material, or reaching its deadline invalidates the source
operation. Every failed/deduplicated session request consumes the call budget;
one export return consumes the source operation even when malformed.

## Complete ancestry, finite cost

The frontend does not replay imported theorem proofs. This does NOT mean the
onward delta packet omits those proofs. It carries each needed uncertified
ancestor witness back to actual succinct-receipt frontiers. Shared exact nodes
are deduplicated; irrelevant branches may be pruned. Alternative journal/rank,
witness bytes or receipt bytes for the same module refuse conservatively.

Onward composition traverses the union of the selected handles' bounded closure,
then emits ancestors in increasing checked rank and the new child last. The
packet parser applies the same aggregate bounds for bytes, witnesses, receipts,
edges, rows, bodies, openings, values and depth. A long/large uncertified chain
must be sealed or left incomplete; this API cannot confer unlimited cheap reuse.

Definitions required by conversion and recursor rules remain semantic inputs.
Imported theorem proof bodies are absent only from the authoring context. The
fixed adopted foundation still contains its actual foundation proof bodies.
The context counter is a bound on selected reconstruction visits, not total CPU.

## Owner preparation and outputs

`DeltaOwnerPreparation` requires the same preparation profile plus source pins
for `delta/authoring.py`, `delta/receiver.py`, `delta/packet.py`, `delta/__init__.py`,
`admission/verifier.py`, and `admission/bindings.py`. The inherited loader requires
the existing preparation/authoring/codec/producer dependency pins too. Its source
paths must identify the actually loaded source tree, not a lookalike snapshot.

The original operation, worker CPU, owner CPU, wall, memory, process, output byte
and entry limits apply. Space reservation includes the whole onward packet as
well as the native export. Worker telemetry uses the existing float-capable
operational parser; mathematical packets use the strict integer parser. Original
live selection and file pins are checked after native return, packet construction,
final writes, result reporting and immediately before public return.

`FINALIZATION-FAILED.json` overrides a preceding candidate `RESULT.json`. These
files are evidence, never transferable admission. `snapshot()` explicitly refuses:
this successor does not forge a receipt-backed snapshot request or launch proofs.

All calls assume trusted owner Python, owner-selected source and OS. Resource
supervision is not hostile-source isolation. No network, discovery, automatic
certification, retry, allowance renewal or public-release claim is added here.
