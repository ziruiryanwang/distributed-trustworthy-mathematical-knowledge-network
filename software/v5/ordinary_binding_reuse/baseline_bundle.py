"""Finite inert baseline bundles, never mathematical acceptance.

Bind a selected fixed-seed writer closure to portable V2 identities, partition
whole units, and validate exact manifests/batches. No owner, native, filesystem,
network or catalog calls. A producer's source/target approval and a receiver's
actual checking remain separate obligations. Parsed objects are conveniences;
revalidate exact raw bytes at a changed boundary.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as PE
import portable_candidate as C


MIB = 1024**2
SCHEMA = "DMKN_ORDINARY_BASELINE_BUNDLE_V1"
WRITER_SCHEMA = "DMKN_ORDINARY_EXPORT_BUNDLE_V1"
WRITER_ASSURANCE = "INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE"
INVENTORY_MAXIMUM = MIB
TARGET_BYTES_MAXIMUM = MIB


class BundleError(ValueError):
    """A syntax/identity/capacity refusal, not mathematical invalidity."""


def need(condition, code):
    if not condition:
        raise BundleError(code)


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class Limits:
    """Locally selected ceilings; a caller may lower, never enlarge them."""

    max_manifest_bytes: int = 2*MIB
    max_units: int = 8192
    max_batches: int = 64
    max_bytes: int = 64*MIB
    max_nodes: int = 20000000
    max_names: int = 262144
    max_edges: int = 262144
    max_binding_bytes: int = 16*MIB
    max_unit_bytes: int = 8*MIB
    max_writer_bytes: int = 64*MIB
    max_targets: int = 1024
    max_batch_units: int = 1024
    max_batch_bytes: int = 64*MIB
    max_batch_nodes: int = 2097152
    max_batch_names: int = 65536
    max_batch_edges: int = 1048576
    max_native_array_bytes: int = 64*MIB

    def __post_init__(self):
        ceilings = {
            "max_manifest_bytes": 2*MIB, "max_units": 8192, "max_batches": 64,
            "max_bytes": 64*MIB, "max_nodes": 20000000, "max_names": 262144,
            "max_edges": 262144, "max_binding_bytes": 16*MIB,
            "max_unit_bytes": 8*MIB, "max_writer_bytes": 64*MIB,
            "max_targets": 1024, "max_batch_units": 1024,
            "max_batch_bytes": 64*MIB, "max_batch_nodes": 2097152,
            "max_batch_names": 65536, "max_batch_edges": 1048576,
            "max_native_array_bytes": 64*MIB,
        }
        for key, ceiling in ceilings.items():
            value = getattr(self, key)
            need(type(value) is int and 0 < value <= ceiling,
                 "BASELINE_LIMIT:"+key)


DEFAULT_LIMITS = Limits()


def _configuration(limits, check_budget):
    need(type(limits) is Limits, "BASELINE_LIMITS_TYPE")
    need(check_budget is None or callable(check_budget), "BASELINE_BUDGET_CALLBACK")
    # Validate even an unusually constructed frozen object at the API boundary.
    limits.__post_init__()


def _check(check_budget):
    if check_budget is not None:
        check_budget()


@dataclass(frozen=True)
class Entry:
    unit_id: str
    raw_sha256: str
    raw_bytes: int

    def __post_init__(self):
        E._hex(self.unit_id)
        E._hex(self.raw_sha256)
        need(type(self.raw_bytes) is int and 0 < self.raw_bytes <= 8*MIB,
             "BASELINE_ENTRY_BYTES")

    @property
    def relative_path(self):
        # Derived from validated hex, never a peer-supplied path.
        self.__post_init__()
        return "units/"+self.unit_id+".json"


@dataclass(frozen=True)
class Manifest:
    raw: bytes
    sha256: str
    semantic_id: str
    batches: tuple[tuple[Entry, ...], ...]
    unit_count: int
    evidence_bytes: int

    @property
    def mathematical_acceptance(self):
        return False


@dataclass(frozen=True)
class BatchCensus:
    units: int
    bytes: int
    nodes: int
    names: int
    edges: int
    binding_bytes: int
    native_array_bytes: int


@dataclass(frozen=True)
class Target:
    """Exact canonical structured name bytes and inert portable identities."""

    name: bytes
    export_id: str
    unit_id: str


@dataclass(frozen=True)
class BoundBundle:
    manifest: Manifest
    batches: tuple[tuple[bytes, ...], ...]
    targets: tuple[Target, ...]
    census: BatchCensus

    @property
    def mathematical_acceptance(self):
        return False


@dataclass(frozen=True)
class _Measured:
    raw: bytes
    entry: Entry
    census: BatchCensus


def _empty_census():
    return BatchCensus(0, 0, 0, 0, 0, 2, 2)


def _add(left, right):
    # The byte counts describe single canonical arrays, including [] and commas.
    return BatchCensus(
        left.units+right.units, left.bytes+right.bytes, left.nodes+right.nodes,
        left.names+right.names, left.edges+right.edges,
        left.binding_bytes+right.binding_bytes-2+int(bool(left.names and right.names)),
        left.native_array_bytes+right.native_array_bytes-2+int(bool(left.units and right.units)))


def _total_bound(census, limits):
    need(census.units <= limits.max_units and census.bytes <= limits.max_bytes and
         census.nodes <= limits.max_nodes and census.names <= limits.max_names and
         census.edges <= limits.max_edges and census.binding_bytes <= limits.max_binding_bytes,
         "BASELINE_AGGREGATE_BOUND")


def _fits_batch(census, limits):
    return (census.units <= limits.max_batch_units and census.bytes <= limits.max_batch_bytes and
            census.nodes <= limits.max_batch_nodes and census.names <= limits.max_batch_names and
            census.edges <= limits.max_batch_edges and
            census.native_array_bytes <= limits.max_native_array_bytes)


def _measure_parsed(parsed, semantic_id, limits, check_budget):
    raw, doc = parsed.raw, parsed.document
    need(0 < len(raw) <= limits.max_unit_bytes, "BASELINE_UNIT_BYTE_BOUND")
    need(doc["semantic_id"] == semantic_id, "BASELINE_EVIDENCE_SEMANTICS")
    binding_bytes = 2
    rows = doc["unit"][2]
    for position, row in enumerate(rows):
        _check(check_budget)
        symbol = S.export_id(semantic_id, parsed.unit_id, row[0])
        binding_bytes += len(E.canonical_json([row[0], symbol]))+int(position != 0)
        need(binding_bytes <= limits.max_binding_bytes, "BASELINE_BINDING_BYTE_BOUND")
    unit_raw = E.canonical_json(doc["unit"])
    census = BatchCensus(1, len(raw), parsed.census.total_nodes, len(rows),
                        len(doc["imports"]), binding_bytes, len(unit_raw)+2)
    need(_fits_batch(census, limits), "BASELINE_SINGLE_UNIT_EXCEEDS_BATCH")
    _total_bound(census, limits)
    return _Measured(raw, Entry(parsed.unit_id, _sha(raw), len(raw)), census)


def _measure(raw, semantic_id, limits, check_budget):
    _check(check_budget)
    need(type(raw) is bytes and 0 < len(raw) <= limits.max_unit_bytes,
         "BASELINE_UNIT_BYTE_BOUND")
    parsed = PE.read_evidence(raw)
    return _measure_parsed(parsed, semantic_id, limits, check_budget)


def read_manifest(raw, expected_sha256, *, limits=DEFAULT_LIMITS, check_budget=None):
    """Validate canonical finite locator metadata; read no evidence or files."""
    _configuration(limits, check_budget)
    _check(check_budget)
    E._hex(expected_sha256)
    need(type(raw) is bytes and 0 < len(raw) <= limits.max_manifest_bytes,
         "BASELINE_MANIFEST_BYTE_BOUND")
    need(_sha(raw) == expected_sha256, "BASELINE_MANIFEST_HASH")
    doc = E.strict_json(raw, E.Limits(max_bytes=limits.max_manifest_bytes))
    need(type(doc) is dict and set(doc) == {"schema", "semantic_id", "batches"} and
         doc["schema"] == SCHEMA, "BASELINE_MANIFEST_FIELDS")
    semantic = S.semantic_id()
    need(doc["semantic_id"] == semantic, "BASELINE_MANIFEST_SEMANTICS")
    source_batches = E._array(doc["batches"], maximum=limits.max_batches)
    need(bool(source_batches), "BASELINE_BATCHES_REQUIRED")
    batches, seen, total_bytes, count = [], set(), 0, 0
    for source_batch in source_batches:
        _check(check_budget)
        entries = E._array(source_batch, maximum=limits.max_batch_units)
        need(bool(entries), "BASELINE_BATCH_EMPTY")
        batch, batch_bytes = [], 0
        for row in entries:
            _check(check_budget)
            need(type(row) is dict and set(row) == {"unit_id", "raw_sha256", "raw_bytes"},
                 "BASELINE_ENTRY_FIELDS")
            entry = Entry(row["unit_id"], row["raw_sha256"], row["raw_bytes"])
            need(entry.raw_bytes <= limits.max_unit_bytes, "BASELINE_UNIT_BYTE_BOUND")
            need(entry.unit_id not in seen, "BASELINE_DUPLICATE_UNIT")
            seen.add(entry.unit_id)
            count += 1
            total_bytes += entry.raw_bytes
            batch_bytes += entry.raw_bytes
            need(count <= limits.max_units and total_bytes <= limits.max_bytes and
                 batch_bytes <= limits.max_batch_bytes, "BASELINE_MANIFEST_AGGREGATE_BOUND")
            batch.append(entry)
        batches.append(tuple(batch))
    _check(check_budget)
    return Manifest(raw, expected_sha256, semantic, tuple(batches), count, total_bytes)


def validate_batch(entries, raw_units, *, limits=DEFAULT_LIMITS, check_budget=None):
    """Check exact evidence against entries and all structural batch ceilings.

    This does not check dependencies against a local mathematical environment.
    Caller must also accumulate returned census across the complete invocation.
    """
    _configuration(limits, check_budget)
    need(type(entries) in (list, tuple) and type(raw_units) in (list, tuple) and
         0 < len(entries) == len(raw_units) <= limits.max_batch_units,
         "BASELINE_BATCH_CENSUS")
    semantic, seen, total = S.semantic_id(), set(), _empty_census()
    for entry, raw in zip(entries, raw_units):
        _check(check_budget)
        need(type(entry) is Entry, "BASELINE_ENTRY_TYPE")
        entry.__post_init__()
        need(type(raw) is bytes and len(raw) == entry.raw_bytes and
             len(raw) <= limits.max_unit_bytes and _sha(raw) == entry.raw_sha256,
             "BASELINE_EVIDENCE_EXACT_BYTES")
        measured = _measure(raw, semantic, limits, check_budget)
        need(measured.entry == entry, "BASELINE_EVIDENCE_IDENTITY")
        need(entry.unit_id not in seen, "BASELINE_DUPLICATE_UNIT")
        seen.add(entry.unit_id)
        total = _add(total, measured.census)
        need(_fits_batch(total, limits), "BASELINE_BATCH_BOUND")
        _total_bound(total, limits)
    _check(check_budget)
    return total


def _split_measured(measured_units, limits, check_budget):
    batches, batch, current, total, seen = [], [], _empty_census(), _empty_census(), set()
    for measured in measured_units:
        _check(check_budget)
        need(measured.entry.unit_id not in seen, "BASELINE_DUPLICATE_UNIT")
        seen.add(measured.entry.unit_id)
        total = _add(total, measured.census)
        _total_bound(total, limits)
        need(_fits_batch(measured.census, limits), "BASELINE_SINGLE_UNIT_EXCEEDS_BATCH")
        combined = _add(current, measured.census)
        if batch and not _fits_batch(combined, limits):
            batches.append(tuple(batch))
            need(len(batches) < limits.max_batches, "BASELINE_BATCH_COUNT_BOUND")
            batch, current = [], _empty_census()
            combined = measured.census
        batch.append(measured)
        current = combined
    need(bool(batch), "BASELINE_UNITS_REQUIRED")
    batches.append(tuple(batch))
    need(len(batches) <= limits.max_batches, "BASELINE_BATCH_COUNT_BOUND")
    return tuple(batches), total


def split_units(raw_units, *, limits=DEFAULT_LIMITS, check_budget=None):
    """Greedy bounded whole-unit partition, preserving the supplied order.

    Generic inputs need their separate dependency/owner-context preflight. The
    fixed-seed binder below independently establishes its producer order.
    """
    _configuration(limits, check_budget)
    need(type(raw_units) in (list, tuple) and 0 < len(raw_units) <= limits.max_units,
         "BASELINE_UNIT_COUNT")
    semantic = S.semantic_id()
    measured = (_measure(raw, semantic, limits, check_budget) for raw in raw_units)
    batches, _ = _split_measured(measured, limits, check_budget)
    return tuple(tuple(unit.raw for unit in batch) for batch in batches)


def _manifest_from_measured(batches, limits, check_budget):
    rows = [[{"unit_id": unit.entry.unit_id, "raw_sha256": unit.entry.raw_sha256,
              "raw_bytes": unit.entry.raw_bytes} for unit in batch] for batch in batches]
    raw = E.canonical_json({"schema": SCHEMA, "semantic_id": S.semantic_id(), "batches": rows})
    return read_manifest(raw, _sha(raw), limits=limits, check_budget=check_budget)


def make_manifest(batches, *, limits=DEFAULT_LIMITS, check_budget=None):
    """Preserve exact chosen batch boundaries; validate evidence before indexing."""
    _configuration(limits, check_budget)
    need(type(batches) in (list, tuple) and 0 < len(batches) <= limits.max_batches,
         "BASELINE_BATCH_COUNT_BOUND")
    semantic, result, seen, total = S.semantic_id(), [], set(), _empty_census()
    for batch in batches:
        need(type(batch) in (list, tuple) and 0 < len(batch) <= limits.max_batch_units,
             "BASELINE_BATCH_CENSUS")
        selected, subtotal = [], _empty_census()
        for raw in batch:
            measured = _measure(raw, semantic, limits, check_budget)
            need(measured.entry.unit_id not in seen, "BASELINE_DUPLICATE_UNIT")
            seen.add(measured.entry.unit_id)
            selected.append(measured)
            subtotal = _add(subtotal, measured.census)
            total = _add(total, measured.census)
            need(_fits_batch(subtotal, limits), "BASELINE_BATCH_BOUND")
            _total_bound(total, limits)
        result.append(tuple(selected))
    return _manifest_from_measured(tuple(result), limits, check_budget)


def bind_writer(writer_raw, inventory_raw, expected_targets, *,
                limits=DEFAULT_LIMITS, check_budget=None):
    """Bind an inert, selected fixed-seed closure without fabricating a context.

    Inventory hash and 581-name census are fixed locally. No mutable project
    paths, owner grants, saved success reports or compiled artifacts are inputs.
    Native extraction/approval is the caller's separate job. The returned bundle
    still requires independent strict admission at every cold receiver.
    """
    _configuration(limits, check_budget)
    _check(check_budget)
    need(type(inventory_raw) is bytes and 0 < len(inventory_raw) <= INVENTORY_MAXIMUM and
         _sha(inventory_raw) == S.INVENTORY, "BASELINE_FIXED_INVENTORY_PIN")
    # This exact pinned Lean-written inventory is not required to be Python's
    # canonical portable JSON. Hash first, then bounded writer grammar.
    inventory = E._array(C._writer_json(inventory_raw, INVENTORY_MAXIMUM), 581)
    fixed_names = [E._array(row, 5)[0] for row in inventory]
    semantic, foundation = S.semantic_id(), S.foundation_id()
    available = {}
    for name in fixed_names:
        _check(check_budget)
        key = E.name_key(name)
        need(key not in available, "BASELINE_FIXED_BASIS_CENSUS")
        available[key] = S.basis_symbol_id(semantic, foundation, name)
    need(len(available) == 581, "BASELINE_FIXED_BASIS_CENSUS")
    E._array(expected_targets, maximum=limits.max_targets)
    need(bool(expected_targets), "BASELINE_TARGETS_REQUIRED")
    target_keys, target_bytes = [], 2
    for name in expected_targets:
        _check(check_budget)
        key = E.name_key(name)
        need(key not in available, "BASELINE_TARGET_ALREADY_IN_BASIS")
        need(key not in target_keys, "BASELINE_DUPLICATE_TARGET")
        target_bytes += len(key)+int(bool(target_keys))
        need(target_bytes <= TARGET_BYTES_MAXIMUM, "BASELINE_TARGET_BYTES")
        target_keys.append(key)

    need(type(writer_raw) is bytes and 0 < len(writer_raw) <= limits.max_writer_bytes,
         "BASELINE_WRITER_BYTE_BOUND")
    doc = C._writer_json(writer_raw, limits.max_writer_bytes)
    need(type(doc) is dict and set(doc) == {
        "schema", "assurance", "targets", "basis_names", "units", "stats"},
        "BASELINE_WRITER_FIELDS")
    need(doc["schema"] == WRITER_SCHEMA and doc["assurance"] == WRITER_ASSURANCE,
         "BASELINE_WRITER_SCHEMA")
    need(doc["basis_names"] == fixed_names and doc["targets"] == expected_targets,
         "BASELINE_WRITER_BASIS_OR_TARGETS")
    units = E._array(doc["units"], maximum=limits.max_units)
    need(bool(units), "BASELINE_UNITS_REQUIRED")
    stats = doc["stats"]
    need(type(stats) is dict and set(stats) == {
        "source_records", "selected_units", "dependency_edges", "scan_nodes", "unit_json_bytes"},
        "BASELINE_WRITER_STATISTICS_FIELDS")
    for value in stats.values():
        E._uint(value)
    need(stats["selected_units"] == len(units) and stats["source_records"] <= 262144 and
         stats["dependency_edges"] <= 262144 and stats["scan_nodes"] <= 20000000 and
         stats["unit_json_bytes"] <= limits.max_writer_bytes, "BASELINE_WRITER_STATISTICS_BOUND")

    measured_units, targets, target_set = [], {}, set(target_keys)
    total, unit_bytes = _empty_census(), 0
    for unit in units:
        _check(check_budget)
        census = E.inspect_unit(unit)
        unit_raw = E.canonical_json(unit)
        unit_bytes += len(unit_raw)
        need(unit_bytes <= limits.max_writer_bytes, "BASELINE_WRITER_UNIT_BYTE_BOUND")
        need(all(key in available for key in census.external_names),
             "BASELINE_UNBOUND_OR_FORWARD_REFERENCE")
        outputs, output_keys, output_seen = unit[2], [], set()
        for row in outputs:
            key = E.name_key(row[0])
            need(key not in available and key not in output_seen,
                 "BASELINE_EXISTING_OR_DUPLICATE_OUTPUT")
            output_keys.append(key)
            output_seen.add(key)
        imports = [[E.strict_json(key), available[key]] for key in census.external_names]
        raw = E.canonical_json({"schema": PE.SCHEMA, "semantic_id": semantic,
                                "imports": imports, "unit": unit})
        need(len(raw) <= limits.max_unit_bytes, "BASELINE_UNIT_BYTE_BOUND")
        # Closed construction: unit was inspected above and raw was just encoded
        # from it. Strict decoding preserves that same JSON unit; no caller can
        # provide a cached census here. Keep every other portable-reader check.
        syntax_limits = PE.DEFAULT_LIMITS
        E._need(type(syntax_limits) is E.Limits, "PORTABLE_EVIDENCE_LIMITS")
        document = E.strict_json(raw, syntax_limits)
        E._need(type(document) is dict and set(document) == {
            "schema", "semantic_id", "imports", "unit"}, "PORTABLE_EVIDENCE_FIELDS")
        E._need(document["schema"] == PE.SCHEMA, "PORTABLE_EVIDENCE_SCHEMA")
        E._hex(document["semantic_id"])
        import_keys = []
        for row in E._array(document["imports"], maximum=syntax_limits.max_imports):
            name, symbol = E._array(row, 2)
            import_keys.append(E.name_key(name, syntax_limits))
            E._hex(symbol)
        E._need(tuple(import_keys) == census.external_names,
                "PORTABLE_IMPORT_CENSUS_OR_ORDER")
        unit_id = hashlib.sha256(
            PE.EVIDENCE_DOMAIN.encode("ascii") + b"\0" + raw).hexdigest()

        # Same measurement as _measure_parsed, reusing only this iteration's
        # validated census and exact encoded unit. External raw-reader paths
        # continue to call _measure_parsed unchanged.
        need(0 < len(raw) <= limits.max_unit_bytes, "BASELINE_UNIT_BYTE_BOUND")
        need(document["semantic_id"] == semantic, "BASELINE_EVIDENCE_SEMANTICS")
        binding_bytes = 2
        rows = document["unit"][2]
        for position, row in enumerate(rows):
            _check(check_budget)
            symbol = S.export_id(semantic, unit_id, row[0])
            binding_bytes += len(E.canonical_json([row[0], symbol]))+int(position != 0)
            need(binding_bytes <= limits.max_binding_bytes, "BASELINE_BINDING_BYTE_BOUND")
        measured_census = BatchCensus(1, len(raw), census.total_nodes, len(rows),
            len(document["imports"]), binding_bytes, len(unit_raw)+2)
        need(_fits_batch(measured_census, limits), "BASELINE_SINGLE_UNIT_EXCEEDS_BATCH")
        _total_bound(measured_census, limits)
        measured = _Measured(raw, Entry(unit_id, _sha(raw), len(raw)), measured_census)
        total = _add(total, measured.census)
        _total_bound(total, limits)
        measured_units.append(measured)
        for row, key in zip(outputs, output_keys):
            _check(check_budget)
            symbol = S.export_id(semantic, unit_id, row[0])
            available[key] = symbol
            if key in target_set:
                targets[key] = Target(key, symbol, unit_id)
    need(unit_bytes == stats["unit_json_bytes"] and set(targets) == target_set,
         "BASELINE_WRITER_BYTE_CENSUS_OR_TARGET_OUTPUT")
    selected, checked_total = _split_measured(measured_units, limits, check_budget)
    need(checked_total == total, "BASELINE_INTERNAL_CENSUS")
    manifest = _manifest_from_measured(selected, limits, check_budget)
    _check(check_budget)
    return BoundBundle(manifest, tuple(tuple(unit.raw for unit in batch) for batch in selected),
                       tuple(targets[key] for key in target_keys), total)
