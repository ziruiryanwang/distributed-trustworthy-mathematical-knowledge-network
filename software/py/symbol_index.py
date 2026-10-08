"""Local raw type-symbol lookup, not a wire service or mathematical checker.

The caller supplies the configured, hash-pinned Gate A source_codec module and
prepared stores. No dynamic imports, CLI, file/network reads or proof execution.
Constant keys are canonical external Native2 references under one foundation:
seed [0,index], declaration [1|2|4,CID], group [3,GroupID,exact selector].
No name matching, group-selector erasure, unfolding or closure/body scanning.

Complete scans at the inclusive ceilings are accepted. This is a finite local
MENTIONS_ALL semantic cut, not qualification of STRUCT1 boundary flags, shapes,
ExtractorIDs, FIND_WINDOW authentication/expiry, or any new network profile.
"""
from collections import namedtuple
import hashlib


MAX_OCCURRENCES = 4096
MAX_DEPTH = 64
MAX_SYMBOLS = 32
MAX_ROWS = 128  # Local helper admission ceiling, not a new protocol profile.
MAX_PAGE_ROWS = 64
MAX_PAGE_BYTES = 1024 * 1024
IndexedRow = namedtuple("IndexedRow", "descriptor_id descriptor_bytes symbol_keys seed_count")
Snapshot = namedtuple("Snapshot", "provider foundation seed_count rows snapshot_id")
Cursor = namedtuple("Cursor", "provider snapshot_id predicate_id next_offset")


class _Issue(Exception):
    def __init__(self, status, reason):
        self.status, self.reason = status, reason


def _failure(error):
    if isinstance(error, _Issue):
        return {"status": error.status, "reason": error.reason}
    return {"status": "INVALID", "reason": "INVALID_INPUT", "detail": str(error)}


def _ref(S, ref, seed_count):
    S.array(ref)
    S.require(bool(ref), "empty semantic reference")
    tag = S.uint(ref[0], 7)
    if tag == 0:
        S.array(ref, 2)
        S.require(S.uint(ref[1]) < seed_count, "seed index range")
    elif tag in (1, 2, 4):
        S.array(ref, 2)
        S.typed(ref[1], {1: 0x11, 2: 0x13, 4: 0x19}[tag], 2)
    elif tag == 3:
        S.array(ref, 3)
        S.typed(ref[1], 0x18, 2)
        selector = S.array(ref[2])
        S.require(bool(selector), "empty group selector")
        kind = S.uint(selector[0], 2)
        S.array(selector, 3 if kind == 1 else 2)
        for value in selector[1:]:
            S.uint(value)
    else:
        raise ValueError("source/local/witness reference is not an external semantic key")
    return ref


def _canonical(S, raw):
    S.require(type(raw) is bytes, "canonical bytes required")
    value = S.C.loads(raw)
    S.require(S.C.dumps(value) == raw, "noncanonical encoding")
    return value


def extract_type_symbols(S, dag, arity, seed_count):
    """Return first-occurrence symbols and complete occurrence-work trace.

    Input is a closed effective TYPE, not a body or root closure. Mathematical
    checking and exact type/root correspondence are caller preconditions.
    No partial symbol set is returned after a support/bound failure.
    """
    trace = {"occurrences": 0, "maximum_depth": 0, "distinct_symbols": 0,
             "normalization": "NONE", "native_acceptance": False}
    try:
        S.require(S.C is not None, "preserved codec must be configured")
        S.uint(seed_count)
        S.uint(arity, S.MAX_UNIVERSES)

        def resolve(ref, projection):
            if projection:
                raise _Issue("NOT_SUPPORTED", "NATIVE_SYNTAX_OUTSIDE_TYPE_FRAGMENT")
            return _ref(S, ref, seed_count)

        checked = S.transform_dag(dag, arity, resolve)
        S.require(checked == dag, "noncanonical type DAG")
        nodes = dag[1]
        if any(node[0] not in (0, 1, 2, 3, 4, 5) for node in nodes):
            raise _Issue("NOT_SUPPORTED", "NATIVE_SYNTAX_OUTSIDE_TYPE_FRAGMENT")
        symbols, keys, seen = [], [], set()
        pending = [(dag[2], 0)]
        while pending:
            index, depth = pending.pop()
            if depth > MAX_DEPTH:
                raise _Issue("NOT_SUPPORTED", "TYPE_DEPTH_BOUND")
            if trace["occurrences"] == MAX_OCCURRENCES:
                raise _Issue("NOT_SUPPORTED", "TYPE_OCCURRENCE_BOUND")
            node = nodes[index]
            trace["occurrences"] += 1
            trace["maximum_depth"] = max(trace["maximum_depth"], depth)
            if node[0] == 2:
                key = S.C.dumps(node[1])
                if key not in seen:
                    if len(keys) == MAX_SYMBOLS:
                        raise _Issue("NOT_SUPPORTED", "TYPE_SYMBOL_BOUND")
                    seen.add(key)
                    keys.append(key)
                    symbols.append(S.C.loads(key))
                    trace["distinct_symbols"] = len(keys)
            if node[0] in (3, 4, 5):
                pending.append((node[2], depth + 1))
                pending.append((node[1], depth + 1))
        return {"status": "OK", "symbols": symbols, "symbol_keys": tuple(keys), "trace": trace}
    except (_Issue, ValueError, TypeError, IndexError, KeyError, RecursionError) as error:
        return {**_failure(error), "trace": trace}


def describe_root(S, store, root):
    """Derive F4 schema-3 public metadata from an exact prepared package root.

    Checks local content commitments and inspected type/root links only. The
    proof/body, representative context and complete closure must already have
    been independently checked by the caller; this function does not admit them.
    It never fetches a proof/definition body just to extract its TYPE symbols.
    """
    try:
        replay = S.array(store.get(root, 0x15, 3), 3)
        foundation, typed_root, representative_map = replay
        S.typed(foundation, 1, 2)
        S.require(foundation == store.foundation, "root foundation mismatch")
        S.typed(representative_map, 0x24, 1)
        S.array(typed_root, 2)
        S.uint(typed_root[0], 4)
        seed_count = len(S.array(store.seed[2]))
        if typed_root[0] == 4:
            instance = S.array(store.get(typed_root[1], 0x23, 1), 2)
            judgment_id = instance[0]
            S.typed(instance[1], 0x22, 1)
            judgment = S.array(store.get(judgment_id, 0x13, 2), 4)
            context = S.array(store.get(judgment[0], 0x12, 2), 2)
            S.require(context[0] == foundation, "judgment context foundation mismatch")
            S.array(judgment[2])
            if judgment[2]:
                raise _Issue("NOT_SUPPORTED", "EXPLICIT_JUDGMENT_TELESCOPE")
            arity, type_id = judgment[1], judgment[3]
            # A checked PI root need not install a canonical judgment alias.
            # This is a local declaration handle, NOT a semantic symbol key.
            judgment_option, native_ref = [1, judgment_id], [7, typed_root[1]]
            semantic_ref = [2, judgment_id]
            semantic_target = judgment_id
        elif typed_root[0] == 1:
            declaration = S.array(store.get(typed_root[1], 0x11, 2), 4)
            S.require(declaration[0] == foundation, "definition foundation mismatch")
            S.typed(declaration[3], 0x10, 2)
            arity, type_id = declaration[1], declaration[2]
            judgment_option, native_ref = [0], [1, typed_root[1]]
            semantic_ref = [1, typed_root[1]]
            semantic_target = typed_root[1]
        else:
            raise _Issue("NOT_SUPPORTED", "ROOT_KIND_OUTSIDE_THEOREM_DEFINITION_CUT")
        S.uint(arity, S.MAX_UNIVERSES)
        term = S.array(store.get(type_id, 0x10, 2), 5)
        S.require(term[0] == foundation and term[1] == arity, "type foundation/arity mismatch")
        dag = term[2:]
        extraction = extract_type_symbols(S, dag, arity, seed_count)
        if extraction["status"] != "OK":
            return extraction
        descriptor = [foundation, typed_root, judgment_option, root, [0]]
        raw = S.C.dumps(descriptor)
        S.require(len(raw) <= 4096, "public descriptor byte bound")
        identifier = S.C.cid(0x8111, 3, descriptor)
        row = IndexedRow(S.C.dumps(identifier), raw,
                         tuple(sorted(extraction["symbol_keys"])), seed_count)
        return {"status": "OK", "row": row, "descriptor": descriptor,
                "descriptor_id": identifier, "native_ref": native_ref,
                "semantic_ref": semantic_ref, "semantic_target": semantic_target, "type_id": type_id,
                "type_dag": dag, "universe_arity": arity,
                "symbols": extraction["symbols"], "trace": extraction["trace"],
                "native_acceptance": False}
    except (_Issue, ValueError, TypeError, IndexError, KeyError, RecursionError) as error:
        return _failure(error)


def _validate_row(S, row):
    S.require(type(row) is IndexedRow, "IndexedRow required")
    S.uint(row.seed_count)
    descriptor = S.array(_canonical(S, row.descriptor_bytes), 5)
    S.require(len(row.descriptor_bytes) <= 4096, "public descriptor byte bound")
    identifier = _canonical(S, row.descriptor_id)
    S.typed(identifier, 0x8111, 3)
    S.require(identifier == S.C.cid(0x8111, 3, descriptor), "descriptor CID mismatch")
    S.typed(descriptor[0], 1, 2)
    typed_root = S.array(descriptor[1], 2)
    tag = S.uint(typed_root[0], 4)
    if tag == 4:
        S.typed(typed_root[1], 0x23, 1)
        option = S.array(descriptor[2], 2)
        S.require(type(option[0]) is int and option[0] == 1, "theorem judgment option")
        S.typed(option[1], 0x13, 2)
    elif tag == 1:
        S.typed(typed_root[1], 0x11, 2)
        S.require(S.same(descriptor[2], [0]), "definition judgment option")
    else:
        raise ValueError("unsupported public root kind")
    S.typed(descriptor[3], 0x15, 3)
    S.require(S.same(descriptor[4], [0]), "this cut has no STRUCT2 hint")
    S.require(type(row.symbol_keys) is tuple and len(row.symbol_keys) <= MAX_SYMBOLS,
              "immutable bounded symbol keys")
    S.require(list(row.symbol_keys) == sorted(set(row.symbol_keys)), "symbol keys order/duplicates")
    for key in row.symbol_keys:
        _ref(S, _canonical(S, key), row.seed_count)
    return descriptor[0]


def build_snapshot(S, provider, rows):
    """Freeze up to 128 rows; exact duplicate rows coalesce, conflicts reject."""
    try:
        S.require(type(provider) is bytes and 0 < len(provider) <= 128, "local provider key")
        S.require(type(rows) in (list, tuple) and 0 < len(rows) <= MAX_ROWS, "bounded nonempty rows")
        unique = {}
        foundation, seed_count = None, None
        for row in rows:
            current = S.C.dumps(_validate_row(S, row))
            if foundation is None:
                foundation, seed_count = current, row.seed_count
            S.require(current == foundation and row.seed_count == seed_count, "mixed snapshot foundation")
            if row.descriptor_id in unique:
                S.require(unique[row.descriptor_id] == row, "conflicting same-CID index row")
            unique[row.descriptor_id] = row
        ordered = tuple(unique[key] for key in sorted(unique))
        # Local commitment only, not a typed protocol object or authentication.
        binding = [provider, foundation, seed_count,
                   [[r.descriptor_id, r.descriptor_bytes, list(r.symbol_keys)] for r in ordered]]
        snapshot_id = hashlib.sha256(b"DTMKN-LOCAL-SYMBOL-SNAPSHOT-1" + S.C.dumps(binding)).digest()
        snapshot = Snapshot(provider, foundation, seed_count, ordered, snapshot_id)
        return {"status": "OK", "snapshot": snapshot, "coalesced_rows": len(rows) - len(ordered)}
    except (_Issue, ValueError, TypeError, IndexError, KeyError, RecursionError) as error:
        return _failure(error)


def find(S, snapshot, keys, cursor=None, *, row_limit=64, byte_limit=1048576):
    """Local MENTIONS_ALL page; an offset cursor is NOT a FIND_WINDOW token.

    keys: 1..8 distinct external semantic references, canonical-byte sorted.
    Page rows are {descriptor_id, descriptor}; no body, evaluator label, symbol
    posting or arbitrary type is sent. encoded_page is a local accounting
    envelope, not a network response grammar. Its size includes local cursor
    binding/position metadata. LIMIT returns no partial successful page.
    """
    try:
        S.require(type(snapshot) is Snapshot, "Snapshot required")
        rebuilt = build_snapshot(S, snapshot.provider, snapshot.rows)
        S.require(rebuilt["status"] == "OK" and rebuilt["snapshot"] == snapshot,
                  "snapshot content/order/binding mismatch")
        S.require(type(row_limit) is int and 1 <= row_limit <= MAX_PAGE_ROWS, "page row ceiling")
        S.require(type(byte_limit) is int and 1 <= byte_limit <= MAX_PAGE_BYTES, "page byte ceiling")
        S.array(keys)
        S.require(1 <= len(keys) <= 8, "one to eight symbol keys required")
        encoded_keys = [S.C.dumps(_ref(S, key, snapshot.seed_count)) for key in keys]
        S.require(encoded_keys == sorted(set(encoded_keys)), "query keys order/duplicates")
        predicate_id = hashlib.sha256(b"DTMKN-LOCAL-MENTIONS-ALL-1" +
                                     S.C.dumps([snapshot.foundation, encoded_keys])).digest()
        postings = [(key, tuple(i for i, row in enumerate(snapshot.rows) if key in row.symbol_keys))
                    for key in encoded_keys]
        source_key, posting = min(postings, key=lambda pair: (len(pair[1]), pair[0]))
        start = 0
        if cursor is not None:
            S.require(type(cursor) is Cursor, "Cursor required")
            S.require(cursor.provider == snapshot.provider and cursor.snapshot_id == snapshot.snapshot_id
                      and cursor.predicate_id == predicate_id, "cursor provider/snapshot/predicate mismatch")
            start = S.uint(cursor.next_offset, len(posting))
        position, inspected, selected = start, 0, []

        def encode(position_value, selected_rows):
            return S.C.dumps([snapshot.provider, snapshot.snapshot_id, predicate_id,
                              start, position_value, int(position_value == len(posting)),
                              selected_rows])

        if len(encode(position, [])) > byte_limit:
            raise _Issue("LIMIT", "PAGE_METADATA_DOES_NOT_FIT")
        while position < len(posting) and len(selected) < row_limit:
            row = snapshot.rows[posting[position]]
            inspected += 1
            if not all(key in row.symbol_keys for key in encoded_keys):
                position += 1
                continue
            candidate = [_canonical(S, row.descriptor_id), _canonical(S, row.descriptor_bytes)]
            tentative = encode(position + 1, selected + [candidate])
            if len(tentative) > byte_limit:
                if not selected:
                    raise _Issue("LIMIT", "NEXT_MATCH_DOES_NOT_FIT")
                break
            selected.append(candidate)
            position += 1
        page = encode(position, selected)
        if len(page) > byte_limit:
            # A position integer changing CBOR width cannot authorize overflow.
            raise _Issue("LIMIT", "PAGE_POSITION_METADATA_DOES_NOT_FIT")
        complete = position == len(posting)
        next_cursor = None if complete else Cursor(snapshot.provider, snapshot.snapshot_id,
                                                   predicate_id, position)
        return {"status": "OK", "rows": [{"descriptor_id": row[0], "descriptor": row[1]}
                                           for row in selected],
                "cursor": next_cursor, "complete": complete, "encoded_page": page,
                "byte_count": len(page), "inspected": inspected, "source_key": source_key,
                "processed_offsets": [start, position], "snapshot_id": snapshot.snapshot_id,
                "provider": snapshot.provider, "native_acceptance": False}
    except (_Issue, ValueError, TypeError, IndexError, KeyError, RecursionError) as error:
        return _failure(error)
