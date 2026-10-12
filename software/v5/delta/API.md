# Native-delta receiving over certified frontiers

Source-only candidate, not built or executed. No mathematical acceptance or
release gate has passed for this new adapter yet. It supplements real succinct
receipts; it does not replace their current acceptance rules.

## Why this exists

An agent can publish a new checked proof without first paying for a large
cryptographic proof. A receiver verifies a few real certificate frontiers, then
checks the complete, bounded set of new proofs above them with the native
mathematical checker. It never requests theorem proofs below those frontiers.
The sender cannot omit an intermediate uncertified proof because it once checked
that proof locally. This route deliberately trades a bounded amount of native
checking for avoiding mandatory fresh cryptographic production on every theorem.

This has no unconditional speedup guarantee: frontier receipt cost, wire bytes,
semantics, all delta checks, failed attempts and custody/search must be included.
When the uncertified closure grows beyond a receiver envelope, another funded
seal, a different proof or a larger explicit envelope is needed.

## Public owner API

```python
from delta import DeltaVerifier, Envelope, DeltaError

# real_verifier is the existing independently configured ReceiptVerifier.
# All configuration below is LOCAL owner policy, not downloaded packet fields.
receiver = DeltaVerifier(
    real_verifier,
    native_executable=adopted_native_path,
    runtime_pins=adopted_native_and_controller_pins,
    output_directory=fresh_evidence_root,
    envelope=Envelope(),
    operations=8, submitted_bytes=128 * 1024**2,
    reserved_cpu_seconds=3600, controller_cpu_seconds=600,
    wall_seconds=3600, output_bytes=512 * 1024**2, output_entries=4096,
)
checked = receiver.receive(packet_bytes, requested_summary,
    native_cpu_seconds=30, receipt_cpu_seconds=30,
    wall_seconds=120, memory_mib=1024)
details = receiver.describe(checked)
group = receiver.open_group(checked, downloaded_opening)
onward_packet = receiver.export_packet(checked)
receiver.close()
```

These limits are illustrative caller choices, not a claim of affordable success.
The packet is immutable bytes. The request summary is an expected mathematical
identity, not authority. The method returns only after all actual calls close
cleanly, exact results/input/runtime pins match, whole closure is complete, real
frontier handles remain live and the original deadline still holds.

`VerifiedDelta` is a distinct opaque local class, not a `VerifiedModule` subclass.
Only the originating live delta receiver recognizes it. Construction by a caller,
serialization or a saved success report grants no authority. `describe` returns
the exact journal and summary, local profile identity, packet digest and proof
form. It revalidates native/controller pins and the original live real frontiers.
Closing either the delta owner or its original receipt verifier revokes use.
A failed receive invalidates this delta owner's earlier handles too.

`open_group` authenticates a selected module group against the accepted summary;
it does not make missing transparent bodies unnecessary. `export_packet` returns
the exact complete original onward-checking packet, **not a transferable local
acceptance token**. A cold recipient executes its own receipt and delta checks.

The source deliberately accepts only an exact `ReceiptVerifier`, not arbitrary
duck-typed verifier callbacks or caller-supplied success JSON. Existing receipt
verification remains unchanged. A cached frontier reuses only an exact receipt
digest/summary with a still-live handle minted by that same real verifier.

`members(handle)` lists copied module/summary/exact-journal/profile/packet-digest
data for the entire actual accepted closure. Each entry is labeled
`receipt-frontier` or `native-delta`, not converted into a receipt handle.
`describe_member(handle, module)` and
`open_member_group(handle, module, opening)` operate on those already established
members under the original closure handle's live pins/frontiers. This matters
when a new theorem's type mentions the certified base's Tree or other ancestors:
the authoring adapter can authenticate their interfaces without pretending the
target theorem alone exports them, or repeating the actual mathematical checks.

## Transfer packet

The current bounded JSON encoding has exactly three fields:

```text
{
  "schema": "DMKN_NATIVE_DELTA_PACKET_V1",
  "frontiers": [{"receipt_hex": lower_case_real_receipt_hex, "summary": summary}],
  "deltas": [complete_named_profile2_relation_witness, ...]
}
```

Every delta contains the existing relation's full named `schema`, `image`,
`rank`, `local_spec`, `rows`, `parents` and `bodies` fields. Opaque parent theorem
proofs below certificates do not appear. The exact existing relation still
checks local proofs, module correspondence, group/body commitments and semantics.
Each packet delta has all parent journals established earlier in the packet.
The final delta must equal the independently requested summary.

Graph edges come from the actual native relation's returned exact journal bytes,
cross-checked against the exact input. Comparing only ModuleIDs would be wrong:
the same committed module can have different proof instances/ranks. Duplicate or
alternative journals for one module in a packet refuse. All included material
must be reachable from the last target; disconnected extras are rejected.

Hex encoding doubles receipt wire size and is counted at that size in the packet
budget. Decoded receipt bytes have a separate bound. This conservative simple
encoding is not a compression result. Aggregate witnesses, JSON nodes/depth,
rows, parent edges, openings, bodies and frontier/delta counts are independently
bounded. Shared delta nodes are included/checked once per operation, not expanded
along every dependency path. The whole raw packet is retained for onward use.

## Failures and costs

`DeltaError.status` distinguishes `INVALID_OR_UNBOUND`, `MISSING_MATERIAL`,
`RESOURCE_INCOMPLETE` and `NEEDS_SEAL`. None means a mathematical theorem is false.
In particular, a clean native refusal can mean an unsupported or unresolved
semantic demand; its diagnostic is retained. The current native relation does
not provide a complete typed classification of all internal checker failures.
Operational filesystem/process exceptions may still propagate after invalidating
the receiver. No retry, larger budget or proof campaign follows automatically.

Attempts and submitted bytes are charged before parsing. CPU reservations cover
every supplied frontier and delta before any native work and remain charged on
failure or a frontier cache hit; this is deliberately conservative, not measured
CPU. Underlying `ReceiptVerifier` has its own allowance as well; those are nested
admission reservations, not two physical costs. `report()` labels successfully
observed worker CPU as partial; failed work is not assumed free. Controller CPU
is inclusive owner-process lifetime CPU, and final reporting/exit tails are not
a complete machine-wide measurement. Retained process reports support later
full-workflow accounting. Operational reports use a finite-float parser; the
mathematical packet and native conclusion remain strict integer-only JSON.

Output limits are checked with reservations and post-operation census; they are
not filesystem quotas. Owner JSON parsing, filesystem calls and process control
are trusted adapter work, not an operating-system memory/security sandbox. The
native worker has selected Job CPU/wall/memory/process/log limits. CPU/deadline
checks prevent late authority even when an operation cannot complete in budget.
Pins identify adopted files; they do not establish a hermetic OS/DLL closure.

## What must still be integrated

The current receipt-only `ImportSession`/`SourceOperation` cannot consume
`VerifiedDelta`. A fresh reviewed authoring successor must compose with this
distinct authority, preserve all selected uncertified proof material and return
a larger complete delta packet. It must never fabricate a parent receipt or
insert a delta handle into a receipt-only private registry.

Current cryptographic guest parents also remain real receipts. Sealing a delta
with uncertified parents requires certificates for those parents or a separately
specified aggregate-sealing relation; this receiver does not provide one.
Discovery, custody and provider transport still need explicit delta-artifact
integration before this becomes a publicly usable end-to-end network route.

`test_packet.py` contains nine unrun structural/refusal groups with synthetic
journals. They invoke no native checker or cryptographic verifier and produce no
positive authority. Actual required controls must use the real retained base
receipt, an actual ordinary-source child, wrong/fake/missing frontiers, altered
proof/body/target, a second delta and aggregate-envelope exhaustion.
