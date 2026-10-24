"""Read-only request preparation from current accepted mathematics.

The complete proof closure is authenticated once here; later native matching
must establish exact private/public correspondence to the selected snapshot.
Neither this request nor its snapshot/support identity labels register a local
reference. Owner locking/support integrity and the outer operation's nonrenewing
budget remain controller premises. No native import, build, or catalog write.
"""
from __future__ import annotations

from dataclasses import dataclass
import heapq
from pathlib import Path

import ordinary_admission as A
import baseline_bundle as B

MIB = 1024**2
SCHEMA = "DMKN_ORDINARY_REFERENCE_BASE_REQUEST_V1"
MAX_REQUEST, MAX_UNIT_ARRAY, MAX_TARGET_BYTES = 96*MIB, 64*MIB, MIB


@dataclass(frozen=True)
class ReferenceRequest:
    """Convenience inputs, not a transferable warrant or correspondence proof."""
    raw: bytes
    sha256: str
    inventory_raw: bytes
    unit_ids: tuple[str, ...]
    evidence_pins: tuple[tuple[str, int, str], ...]
    output_bindings: tuple[tuple[bytes, str, str], ...]
    nodes: int
    edges: int


def prepare_request(owner, parent_root, bundle_directory, manifest_raw, manifest_sha256, *,
                    targets, snapshot_id, support_id, check_budget):
    """Authenticate a full seed-relative closure without replaying its proofs.

    Only currently warranted units may be sent to the matcher. Merely existing
    in a bundle/custody is insufficient. The caller keeps this actual owner open
    and serialized through live matching and final registration; this read-only
    function cannot extend the lifetime of a context or authenticate a snapshot.
    """
    A.need(type(owner) is A.OrdinaryAdmission and B.E is A.E and B.S is A.S and
           B.PE is A.PE and callable(check_budget), "REFERENCE_REQUEST_CONFIGURATION")
    check = check_budget
    for identity in (parent_root, snapshot_id, support_id):
        A.C.hexid(identity)
    check()
    context = owner.catalog.context(parent_root)
    semantic = owner.installation.semantic_id
    A.need(context["semantic_id"] == semantic == A.S.semantic_id() and
           context["foundation_id"] == A.S.foundation_id(), "REFERENCE_REQUEST_CONTEXT")
    manifest = B.read_manifest(manifest_raw, manifest_sha256, check_budget=check)
    A.need(manifest.semantic_id == semantic, "REFERENCE_REQUEST_BUNDLE_SEMANTICS")
    directory = A.C.ordinary(Path(bundle_directory), directory=True)
    inventory_raw = owner.installation.read("inventory", MIB)
    A.need(A.sha(inventory_raw) == A.S.INVENTORY, "REFERENCE_REQUEST_FIXED_INVENTORY")
    inventory = A.E._array(A._writer_json(inventory_raw, MIB), 581)
    basis = {}
    for row in inventory:
        check()
        name = A.E._array(row, 5)[0]
        key = A.E.name_key(name)
        identity = A.S.basis_symbol_id(semantic, A.S.foundation_id(), name)
        A.need(key not in basis and context["bindings"].get(key) == identity,
               "REFERENCE_REQUEST_CURRENT_BASIS")
        basis[key] = identity

    units, bindings, pins = {}, {}, []
    total = B._empty_census()
    for batch in manifest.batches:
        batch_total = B._empty_census()
        for entry in batch:
            check()
            raw = A.C.read_bounded(directory/entry.relative_path, entry.raw_bytes)
            A.need(len(raw) == entry.raw_bytes and A.sha(raw) == entry.raw_sha256,
                   "REFERENCE_REQUEST_EXACT_EVIDENCE")
            item = A.PE.read_evidence(raw)
            measured = B._measure_parsed(item, semantic, B.DEFAULT_LIMITS, check)
            A.need(measured.entry == entry, "REFERENCE_REQUEST_UNIT_IDENTITY")
            batch_total = B._add(batch_total, measured.census)
            total = B._add(total, measured.census)
            A.need(B._fits_batch(batch_total, B.DEFAULT_LIMITS), "REFERENCE_REQUEST_BATCH_BOUND")
            B._total_bound(total, B.DEFAULT_LIMITS)
            A.need(total.native_array_bytes <= MAX_UNIT_ARRAY, "REFERENCE_REQUEST_UNIT_ARRAY_BOUND")
            outputs = []
            for row in item.document["unit"][2]:
                check()
                name = row[0]
                key = A.E.name_key(name)
                symbol = A.S.export_id(semantic, item.unit_id, name)
                A.need(key not in basis and key not in bindings and
                       context["bindings"].get(key) == symbol,
                       "REFERENCE_REQUEST_UNWARRANTED_OR_CONFLICTING_OUTPUT")
                bindings[key] = (symbol, item.unit_id)
                outputs.append({"name": name, "export_id": symbol})
            units[item.unit_id] = {"item": item, "outputs": outputs}
            pins.append((item.unit_id, len(raw), A.sha(raw)))

    # Existing acceptance may have used additional local premises. This exact
    # reference input nevertheless must include every nonbasis proof dependency;
    # being warranted elsewhere does not let it enter an unselected snapshot.
    dependencies, users = {}, {identity: set() for identity in units}
    for identity, data in units.items():
        check()
        required = set()
        for name, symbol in data["item"].document["imports"]:
            check()
            key = A.E.name_key(name)
            A.need(context["bindings"].get(key) == symbol, "REFERENCE_REQUEST_UNWARRANTED_IMPORT")
            if key in basis:
                A.need(basis[key] == symbol, "REFERENCE_REQUEST_BASIS_IMPORT")
            else:
                matched = bindings.get(key)
                A.need(matched is not None and matched[0] == symbol,
                       "REFERENCE_REQUEST_MISSING_PRIVATE_DEPENDENCY")
                required.add(matched[1])
        dependencies[identity] = required
        for dependency in required:
            users[dependency].add(identity)
    ready = [identity for identity, required in dependencies.items() if not required]
    heapq.heapify(ready)
    ordered = []
    while ready:
        check()
        identity = heapq.heappop(ready)
        ordered.append(identity)
        for user in users[identity]:
            dependencies[user].remove(identity)
            if not dependencies[user]:
                heapq.heappush(ready, user)
    A.need(len(ordered) == len(units), "REFERENCE_REQUEST_DEPENDENCY_CYCLE")

    A.E._array(targets, maximum=1024)
    A.need(bool(targets), "REFERENCE_REQUEST_TARGETS_EMPTY")
    raw_targets = A.E.canonical_json(targets)
    A.need(len(raw_targets) <= MAX_TARGET_BYTES, "REFERENCE_REQUEST_TARGET_BYTES")
    targets = A.E.strict_json(raw_targets, A.E.Limits(max_bytes=MAX_TARGET_BYTES))
    seen = set()
    for target in targets:
        check()
        A.need(type(target) is dict and set(target) == {"name", "export_id"},
               "REFERENCE_REQUEST_TARGET_FIELDS")
        key = A.E.name_key(target["name"])
        A.C.hexid(target["export_id"])
        A.need(key not in seen and key in bindings and bindings[key][0] == target["export_id"],
               "REFERENCE_REQUEST_TARGET_NOT_IN_PRIVATE_CLOSURE")
        seen.add(key)
    rows = [{"unit_id": identity, "unit": units[identity]["item"].document["unit"],
             "outputs": units[identity]["outputs"]} for identity in ordered]
    raw = A.E.canonical_json({"schema": SCHEMA, "semantic_id": semantic,
        "foundation_id": A.S.foundation_id(), "context_root": parent_root,
        "snapshot_id": snapshot_id, "support_id": support_id, "units": rows, "targets": targets})
    A.need(len(raw) <= MAX_REQUEST, "REFERENCE_REQUEST_TOTAL_BYTES")
    check()
    return ReferenceRequest(raw, A.sha(raw), inventory_raw, tuple(ordered), tuple(pins),
        tuple((key, symbol, unit) for key, (symbol, unit) in sorted(bindings.items())),
        total.nodes, total.edges)
