"""Finite ordinary-source PI1 bridge; candidate bytes are not native acceptance.

The predecessor codec is loaded only from an explicit, hash-pinned path.  No
producer environment, inventory claim, source name, or this program's success
is a substitute for the separately bound fresh native receiver execution.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

CODEC_SHA256 = "bb76d235275dbbf37a026b124181995e2da0c7dbd8bab579878870437008006b"
MAX_BYTES = 64 * 1024 * 1024
MAX_OBJECTS = 8192
MAX_UNITS = 256
MAX_EXPORTS = 1024
MAX_EXPR = 65536
MAX_LEVEL = 4096
MAX_UNIVERSES = 64
MAX_GROUP_TYPES = 16
MAX_GROUP_CONSTRUCTORS = 32
MAX_DEPTH = 4096
U32 = (1 << 32) - 1
C = None


def require(ok, message):
    if not ok:
        raise ValueError(message)


def uint(value, limit=U32):
    require(type(value) is int and 0 <= value <= limit, "unsigned integer/range")
    return value


def array(value, length=None):
    require(type(value) is list and (length is None or len(value) == length), "array/arity")
    return value


def fields(value, required):
    require(type(value) is dict and set(value) == set(required), "record fields")
    return value


def read_bytes(path, limit=MAX_BYTES):
    with Path(path).open("rb") as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, "bounded read exceeded")
    return raw


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON field")
            result[key] = value
        return result
    def reject(_):
        raise ValueError("noninteger JSON number")
    return json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=pairs,
                      parse_float=reject, parse_constant=reject)


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def configure_codec(path):
    global C
    path = Path(path).resolve(strict=True)
    require(hashlib.sha256(read_bytes(path, 1024 * 1024)).hexdigest() == CODEC_SHA256,
            "predecessor codec differs from preserved pin")
    spec = importlib.util.spec_from_file_location("source_composition_preserved_codec", path)
    require(spec is not None and spec.loader is not None, "codec loader")
    C = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(C)
    return C


def identity(ref):
    C.cidkey(ref)
    return C.dumps(ref).hex()


def typed(ref, tag, schema):
    identity(ref)
    require(ref[1:3] == [tag, schema], "typed identity mismatch")
    return ref


def namekey(name):
    return C._validate_name(name)


def child(name, component):
    return name + [[0, component.encode("utf-8")]]


def native_name(ref):
    tag = ref[0]
    if tag in (1, 2, 4, 7):
        expected = {1: (0x11, 2, "d"), 2: (0x13, 2, "j"),
                    4: (0x19, 2, "o"), 7: (0x23, 1, "w")}[tag]
        typed(ref[1], *expected[:2])
        return C.name_path("DTMKN." + expected[2] + "." + identity(ref[1]))
    require(tag == 3 and len(ref) == 3, "native name requires external reference")
    typed(ref[1], 0x18, 2)
    selector = array(ref[2])
    st = uint(selector[0], 3)
    require(st != 3, "nested auxiliary recursor unsupported in this finite cut")
    array(selector, 3 if st == 1 else 2)
    ti = uint(selector[1])
    base = C.name_path("DTMKN.i." + identity(ref[1]))
    base = child(base, "t" + str(ti))
    if st == 1:
        return child(base, "c" + str(uint(selector[2])))
    return child(base, "rec") if st == 2 else base


class Store:
    def __init__(self, seed):
        self.seed = seed
        self.objects = {}
        self.inventories = {}
        self.total_bytes = 0
        self.base = C.make_foundation(seed)
        for record in self.base.values():
            self.add(record["id"][1], record["id"][2], record["payload"])
        self.foundation = self.base["foundation"]["id"]

    def add(self, tag, schema, payload):
        ref = C.cid(tag, schema, payload)
        key = identity(ref)
        raw = C.dumps(payload)
        if key in self.objects:
            require(self.objects[key][1] == payload, "positive content collision")
        else:
            require(len(self.objects) < MAX_OBJECTS, "object-count allowance")
            require(self.total_bytes + len(raw) <= MAX_BYTES, "closure construction byte allowance")
            self.objects[key] = (ref, payload)
            self.total_bytes += len(raw)
        return ref

    def get(self, ref, tag=None, schema=None):
        if tag is not None:
            typed(ref, tag, schema)
        record = self.objects.get(identity(ref))
        require(record is not None, "missing exact object")
        require(record[0] == ref and C.cid(ref[1], ref[2], record[1]) == ref, "object commitment")
        return record[1]

    def closure(self, root):
        done, active = set(), set()
        stack = [(root, False)]
        while stack:
            ref, finishing = stack.pop()
            key = identity(ref)
            if finishing:
                active.remove(key)
                done.add(key)
                continue
            require(key not in active, "content dependency cycle")
            if key in done:
                continue
            active.add(key)
            require(len(active) <= 1024, "content dependency depth")
            stack.append((ref, True))
            pending = [self.get(ref)]
            refs = []
            while pending:
                item = pending.pop()
                if type(item) is not list:
                    continue
                if (len(item) == 4 and type(item[0]) is int and item[0] == 1
                        and type(item[1]) is int and type(item[2]) is int
                        and type(item[3]) is bytes and len(item[3]) == 32):
                    identity(item)
                    refs.append(item)
                else:
                    pending.extend(reversed(item))
            for item in reversed(refs):
                if identity(item) not in done:
                    stack.append((item, False))
        return done


def trie(store, entries, mapping=False):
    """Build the unique fixed-key Patricia tree; entries are key->value/None."""
    pairs = sorted(entries.items())
    require(all(type(k) is bytes and len(k) == 37 for k, _ in pairs), "trie key length")
    tag = 0x24 if mapping else 0x20
    def build(items):
        if not items:
            payload = [2]
        elif len(items) == 1:
            key, value = items[0]
            payload = [0, key, value] if mapping else [0, key]
        else:
            lo, hi = int.from_bytes(items[0][0], "big"), int.from_bytes(items[-1][0], "big")
            split = 296 - (lo ^ hi).bit_length()
            require(split < 296, "duplicate trie key")
            count = (split + 7) // 8
            prefix = bytearray(items[0][0][:count])
            if split % 8:
                prefix[-1] &= 255 << (8 - split % 8)
            middle = next(i for i, (k, _) in enumerate(items)
                          if k[split // 8] & (1 << (7 - split % 8)))
            require(0 < middle < len(items), "Patricia partition")
            payload = [1, split, bytes(prefix), build(items[:middle]), build(items[middle:])]
        require(len(C.dumps(payload)) <= 256, "Patricia node byte bound")
        return store.add(tag, 1, payload)
    return build(pairs)


def parse_trie(store, root, mapping=False):
    tag = 0x24 if mapping else 0x20
    entries, seen = {}, set()
    stack = [root]
    while stack:
        ref = stack.pop()
        key = identity(ref)
        require(key not in seen, "duplicate/cyclic Patricia subtree")
        seen.add(key)
        payload = array(store.get(ref, tag, 1))
        require(len(C.dumps(payload)) <= 256 and payload, "Patricia node bound")
        node = uint(payload[0], 2)
        if node == 2:
            array(payload, 1)
            require(ref == root, "empty Patricia child")
        elif node == 0:
            array(payload, 3 if mapping else 2)
            k = payload[1]
            require(type(k) is bytes and len(k) == 37 and k not in entries, "Patricia leaf key")
            decoded = [k[0], int.from_bytes(k[1:3], "big"), int.from_bytes(k[3:5], "big"), k[5:]]
            identity(decoded)
            require(decoded[1:3] in ([[0x13, 2]] if mapping else
                    [[0x11, 2], [0x13, 2], [0x18, 2], [0x19, 2]]), "Patricia key kind")
            if mapping:
                typed(payload[2], 0x23, 1)
            entries[k] = payload[2] if mapping else None
        else:
            array(payload, 5)
            uint(payload[1], 295)
            require(type(payload[2]) is bytes, "Patricia prefix")
            stack.extend([payload[4], payload[3]])
    expected = trie(store, entries, mapping)
    require(expected == root, "noncanonical Patricia tree")
    return entries


def transform_dag(dag, arity, resolve, *, source=False, raw_output=False, scope=0):
    """Validate a bounded DAG and rebuild canonical sharing after name erasure.

    resolve(ref, is_projection) owns reference-kind and membership validation.
    No recursive expansion of expression sharing or referenced declarations.
    """
    array(dag, 3)
    ls, es, root = dag
    array(ls); array(es)
    uint(arity, 1024); uint(scope)
    require(0 < len(es) <= MAX_EXPR and len(ls) <= MAX_LEVEL, "DAG node allowance")
    require(uint(root, len(es) - 1) == len(es) - 1, "DAG final root")
    require(len({C.dumps(n) for n in ls}) == len(ls), "duplicate level node")
    require(len({C.dumps(n) for n in es}) == len(es), "duplicate expression node")
    level_children, level_depth = [], []
    for i, node in enumerate(ls):
        array(node); require(node, "empty level")
        tag = uint(node[0], 4)
        array(node, 1 if tag == 0 else 3 if tag in (2, 3) else 2)
        children = node[1:] if tag in (1, 2, 3) else []
        for k in children:
            require(uint(k) < i, "level forward edge")
        if tag == 4:
            require(uint(node[1]) < arity, "universe parameter out of scope")
        depth = 1 + max((level_depth[k] for k in children), default=0)
        require(depth <= MAX_DEPTH, "level depth")
        level_children.append(children); level_depth.append(depth)
    children, level_uses, need, depths, converted = [], [], [], [], []
    for i, node in enumerate(es):
        array(node); require(node, "empty expression")
        tag = uint(node[0], 9)
        kids, us, needed = [], [], 0
        out = list(node)
        if tag == 0:
            array(node, 2); needed = uint(node[1]) + 1
        elif tag == 1:
            array(node, 2); us = [node[1]]
        elif tag == 2:
            array(node, 3); array(node[2]); us = node[2]
            out[1] = resolve(node[1], False)
        elif tag == 3:
            array(node, 3); kids = node[1:]
        elif tag in (4, 5):
            array(node, 4 if source else 3)
            if source:
                uint(node[1], 3)
            kids = node[-2:]
            out = [tag, 0, *kids] if raw_output else [tag, *kids]
        elif tag == 6:
            array(node, 4); kids = node[1:]
        elif tag in (7, 9):
            array(node, 2)
            require(type(node[1]) is bytes and len(node[1]) <= 1048576, "literal bytes")
            if tag == 7:
                require(not node[1] or node[1][0] != 0, "nonminimal natural magnitude")
            else:
                node[1].decode("utf-8", errors="strict")
        else:
            array(node, 4); uint(node[2]); kids = [node[3]]
            out[1] = resolve(node[1], True)
        for k in kids:
            require(uint(k) < i, "expression forward edge")
        for k in us:
            require(uint(k) < len(ls), "level index")
        if tag == 3:
            needed = max(need[kids[0]], need[kids[1]])
        elif tag in (4, 5):
            needed = max(need[kids[0]], max(0, need[kids[1]] - 1))
        elif tag == 6:
            needed = max(need[kids[0]], need[kids[1]], max(0, need[kids[2]] - 1))
        elif tag == 8:
            needed = need[kids[0]]
        depth = 1 + max([depths[k] for k in kids] + [level_depth[k] for k in us] + [0])
        require(depth <= MAX_DEPTH, "expression depth")
        children.append(kids); level_uses.append(us); need.append(needed)
        depths.append(depth); converted.append(out)
    require(need[root] <= scope, "open expression root")

    def order_from(start, edges):
        seen, ordered, stack = set(), [], [(k, False) for k in reversed(start)]
        while stack:
            k, end = stack.pop()
            if end:
                ordered.append(k)
            elif k not in seen:
                seen.add(k); stack.append((k, True))
                stack.extend((c, False) for c in reversed(edges[k]))
        return ordered
    eo = order_from([root], children)
    lo = order_from([l for k in eo for l in level_uses[k]], level_children)
    require(eo == list(range(len(es))) and lo == list(range(len(ls))), "noncanonical/unreachable DAG order")
    out_expr, emap, intern = [], {}, {}
    for i, node in enumerate(converted):
        tag = node[0]
        if tag == 3:
            node = [tag, emap[node[1]], emap[node[2]]]
        elif tag in (4, 5):
            node = [tag, *([0] if raw_output else []), emap[node[-2]], emap[node[-1]]]
        elif tag == 6:
            node = [tag, *(emap[k] for k in node[1:])]
        elif tag == 8:
            node = [tag, node[1], node[2], emap[node[3]]]
        key = C.dumps(node)
        if key not in intern:
            intern[key] = len(out_expr); out_expr.append(node)
        emap[i] = intern[key]
    require(emap[root] == len(out_expr) - 1, "canonicalized root")
    return [ls, out_expr, emap[root]]


def raw_refs(dag):
    array(dag, 3)
    for node in array(dag[1]):
        array(node); require(node, "empty raw expression")
        if node[0] in (2, 8):
            array(node[1], 2)
            require(node[1][0] == 6, "source reference must be explicit native NamePath")
            namekey(node[1][1])
            yield node[1][1]


def inventory_dags(row):
    array(row, 5)
    yield row[3]
    kind, data = uint(row[1], 7), array(row[4])
    if kind in (1, 2, 3):
        yield data[0]
    elif kind == 6:
        array(data, 8)
        for rule in array(data[5]):
            array(rule, 3)
            yield rule[2]


def normalize_inventory(rows, resolve, namer):
    """Preserve every generated field; replace only names/binder presentation."""
    result = []
    for row in rows:
        array(row, 5)
        kind, arity, data = uint(row[1], 7), uint(row[2], 1024), array(row[4])
        require(kind in (4, 5, 6), "ordinary group inventory kinds only")
        def dag(value):
            return transform_dag(value, arity, resolve, source=True, raw_output=True)
        if kind == 4:
            array(data, 8)
            uint(data[0]); uint(data[1]); uint(data[4])
            for flag in data[5:]:
                uint(flag, 1)
            require(data[4] == 0 and data[6] == 0, "nested/unsafe group unsupported")
            out = [data[0], data[1], [namer(n) for n in array(data[2])],
                   [namer(n) for n in array(data[3])], *data[4:]]
        elif kind == 5:
            array(data, 5)
            for n in data[1:4]:
                uint(n)
            require(uint(data[4], 1) == 0, "unsafe constructor")
            out = [namer(data[0]), *data[1:]]
        else:
            array(data, 8)
            for n in data[1:5]:
                uint(n)
            uint(data[6], 1)
            require(uint(data[7], 1) == 0, "unsafe recursor")
            rules = []
            for rule in array(data[5]):
                array(rule, 3); uint(rule[1])
                rules.append([namer(rule[0]), rule[1], dag(rule[2])])
            out = [[namer(n) for n in array(data[0])], *data[1:5], rules, *data[6:]]
        result.append([namer(row[0]), kind, arity, dag(row[3]), out])
    result.sort(key=lambda row: namekey(row[0]))
    require(len({namekey(r[0]) for r in result}) == len(result), "duplicate generated member")
    return result


class SourceCompiler:
    def __init__(self, seed, capture, inherited=None, inherited_roots=()):
        fields(capture, ["schema", "roots", "units"])
        require(type(capture["schema"]) is int and capture["schema"] == 1, "capture schema")
        self.store = Store(seed)
        self.roots = C.from_projection(capture["roots"])
        array(self.roots)
        for n in self.roots:
            namekey(n)
        array(capture["units"])
        require(len(capture["units"]) <= MAX_UNITS, "source unit allowance")
        self.units, self.owners, self.names = {}, {}, {}
        self.semantic, self.instances, self.choices = {}, {}, {}
        self.done, self.active = set(), set()
        self.group_members = {}
        for i, name in enumerate(seed[2]):
            key = namekey(name)
            self.semantic[key] = [0, i]
            self.names[key] = name
        if inherited is not None:
            require(inherited.seed == seed, "inherited foundation/seed mismatch")
            prepared = make_plan(inherited, list(inherited_roots))
            for ref, payload in inherited.objects.values():
                self.store.add(ref[1], ref[2], payload)
            self.store.inventories.update(inherited.inventories)
            for root in inherited_roots:
                self.choices.update(parse_trie(self.store, self.store.get(root, 0x15, 3)[2], True))
            for row in prepared["batch"]:
                ref = C.from_projection(row["id"])
                if row["kind"] == 3:
                    types = self.store.get(ref, 0x18, 2)[3]
                    for i, desc in enumerate(types):
                        selectors = [[0, i], [2, i]] + [[1, i, k] for k in range(len(desc[1]))]
                        for selector in selectors:
                            r = [3, ref, selector]; n = native_name(r); nk = namekey(n)
                            self.names[nk] = n; self.semantic[nk] = r
                elif row["kind"] in (0, 2):
                    r = [1 if row["kind"] == 0 else 4, ref]
                    n = native_name(r); nk = namekey(n)
                    self.names[nk] = n; self.semantic[nk] = r
                else:
                    if row["kind"] == 1:
                        pi, j = ref, self.store.get(ref, 0x23, 1)[0]
                        n = native_name([7, pi])
                    else:
                        # A semantic alias has its own actual source theorem body.
                        # Preserve that wrapper as a PI if referenced as source evidence.
                        j = ref; n = native_name([2, j])
                        body = C.from_projection(row["value"])
                        wt = self.store.add(0x22, 1, [self.store.foundation, row["u"], *body])
                        pi = self.store.add(0x23, 1, [j, wt])
                    nk = namekey(n)
                    self.names[nk] = n; self.semantic[nk] = [2, j]; self.instances[nk] = pi
                    self.choices.setdefault(C.cidkey(j), pi)
        for raw in capture["units"]:
            fields(raw, ["key", "descriptor", "inventory", "universeNames", "inventoryUniverseNames"])
            unit = {k: C.from_projection(v) for k, v in raw.items()}
            key = namekey(unit["key"])
            require(key not in self.units and key not in self.semantic, "duplicate/seed-shadowing source unit")
            d = array(unit["descriptor"])
            require(d and uint(d[0], 3) in (0, 1, 2, 3), "unsupported source declaration")
            array(d, 4 if d[0] == 3 else 5)
            arity = d[1] if d[0] == 3 else d[2]
            params = array(unit["universeNames"])
            require(len(params) == uint(arity, MAX_UNIVERSES), "source universe-order arity")
            require(len({namekey(n) for n in params}) == len(params), "duplicate source universe parameter")
            inventory = array(unit["inventory"])
            inventory_us = array(unit["inventoryUniverseNames"])
            require(len(inventory) == len(inventory_us), "inventory universe-name correspondence")
            for row, us in zip(inventory, inventory_us):
                array(row, 5); array(us)
                require(len(us) == uint(row[2], 1024), "inventory universe arity")
                require(len({namekey(n) for n in us}) == len(us), "duplicate inventory universe parameter")
                nk = namekey(row[0])
                require(nk not in self.owners and nk not in self.semantic, "duplicate source native name")
                self.owners[nk] = key; self.names[nk] = row[0]
            self.units[key] = unit
            if d[0] != 3:
                require(namekey(d[1]) == key and len(inventory) == 1 and namekey(inventory[0][0]) == key,
                        "ordinary unit/name inventory")
                require(inventory[0][1] == d[0] + 1 and inventory[0][2] == arity,
                        "ordinary source kind/arity")
                require(unit["inventoryUniverseNames"][0] == params, "ordinary universe order")
                data = array(inventory[0][4], 2 if d[0] == 1 else 3)
                require(data[-1] == [d[1]], "ordinary normalized source all list")
            else:
                self.group_members[key] = self.group_selectors(unit)
        require(len(self.owners) <= MAX_EXPORTS, "source export allowance")

    def group_selectors(self, unit):
        d, rows = unit["descriptor"], unit["inventory"]
        uint(d[2]); array(d[3])
        require(0 < len(d[3]) <= MAX_GROUP_TYPES, "group type count")
        result, type_names = {}, []
        by_name = {namekey(row[0]): row for row in rows}
        us_by_name = {namekey(row[0]): us for row, us in zip(rows, unit["inventoryUniverseNames"])}
        for i, desc in enumerate(d[3]):
            array(desc, 3); array(desc[2]); nk = namekey(desc[0])
            require(len(desc[2]) <= MAX_GROUP_CONSTRUCTORS, "group constructor count")
            type_names.append(desc[0]); result[nk] = [0, i]
            row = by_name.get(nk)
            require(row is not None and row[1] == 4 and row[2] == d[1], "source inductive kind/arity")
            require(row[3] == desc[1], "source group descriptor/inventory type")
            require(us_by_name[nk] == unit["universeNames"], "group universe parameter order")
            data = array(row[4], 8)
            require(data[0] == d[2] and data[4] == 0 and data[6] == 0, "group parameters/nested/safety")
            require(data[3] == [c[0] for c in desc[2]], "source constructor order")
            for ci, ctor in enumerate(desc[2]):
                array(ctor, 2); ck = namekey(ctor[0]); result[ck] = [1, i, ci]
                cr = by_name.get(ck)
                require(cr is not None and cr[1] == 5 and cr[2] == d[1], "constructor inventory kind/arity")
                require(cr[3] == ctor[1], "source constructor descriptor/inventory type")
                require(us_by_name[ck] == unit["universeNames"], "constructor universe parameter order")
                array(cr[4], 5)
                require(cr[4][0] == desc[0] and cr[4][1] == ci and cr[4][2] == d[2]
                        and cr[4][4] == 0, "constructor owner/index/parameters/safety")
            rec_key = namekey(child(desc[0], "rec"))
            require(rec_key in by_name and by_name[rec_key][1] == 6, "missing actual ordinary recursor")
            result[rec_key] = [2, i]
        require(type_names[0] == unit["key"], "group key/order")
        require(set(result) == set(by_name), "unexplained/missing generated member")
        for row in rows:
            if row[1] == 4:
                require(row[4][2] == type_names, "inductive all list")
            elif row[1] == 6:
                array(row[4], 8)
                require(row[4][0] == type_names and row[4][1] == d[2] and row[4][7] == 0,
                        "recursor actual association/safety")
        return result

    def resolve(self, ref, projection=False, *, witness=False, locals=None):
        array(ref, 2)
        require(ref[0] == 6, "non-source reference in capture")
        key = namekey(ref[1])
        if locals is not None and key in locals:
            require(not projection, "group-local projection unsupported")
            return [5, locals[key]]
        if key not in self.semantic:
            require(key in self.owners, "missing source dependency")
            self.compile(self.owners[key])
        result = self.semantic[key]
        if witness and result[0] == 2:
            require(key in self.instances, "source theorem instance missing")
            result = [7, self.instances[key]]
        if projection:
            require(result[0] == 0 or result[0] == 3 and result[2][0] == 0,
                    "projection does not name seed/group type")
        return result

    def term(self, dag, arity, witness=False, locals=None):
        return transform_dag(dag, arity,
                             lambda r, p: self.resolve(r, p, witness=witness, locals=locals), source=True)

    def compile(self, key):
        if key in self.done:
            return
        require(key not in self.active and len(self.active) < MAX_UNITS, "source dependency cycle/depth")
        self.active.add(key)
        unit = self.units[key]; d = unit["descriptor"]
        if d[0] == 3:
            arity = d[1]
            local = {namekey(t[0]): i for i, t in enumerate(d[3])}
            types = [[self.term(t[1], arity, locals=local),
                      [self.term(c[1], arity, locals=local) for c in t[2]]] for t in d[3]]
            gid = self.store.add(0x18, 2, [self.store.foundation, arity, d[2], types])
            for nk, selector in self.group_members[key].items():
                self.semantic[nk] = [3, gid, selector]
            def namer(n):
                r = self.resolve([6, n])
                return self.store.seed[2][r[1]] if r[0] == 0 else native_name(r)
            def raw_resolve(r, projection):
                mapped = self.resolve(r, projection)
                return [6, self.store.seed[2][mapped[1]] if mapped[0] == 0 else native_name(mapped)]
            inventory = normalize_inventory(unit["inventory"], raw_resolve, namer)
            # Every actual generated expression is traversed with the same resolver;
            # native reconstruction independently compares these diagnostic claims.
            for row in unit["inventory"]:
                for dag in inventory_dags(row):
                    self.term(dag, row[2])
            self.store.inventories[identity(gid)] = inventory
        else:
            arity = d[2]
            ty = self.term(d[3], arity)
            value = self.term(d[4], arity, witness=d[0] == 1)
            row = unit["inventory"][0]
            require(self.term(row[3], arity) == ty, "source descriptor/inventory type mismatch")
            require(self.term(row[4][0], arity, witness=d[0] == 1) == value,
                    "source descriptor/inventory body mismatch")
            type_id = self.store.add(0x10, 2, [self.store.foundation, arity, *ty])
            if d[0] == 1:
                j = make_judgment(self.store, arity, ty)
                witness_id = self.store.add(0x22, 1, [self.store.foundation, arity, *value])
                pi = self.store.add(0x23, 1, [j, witness_id])
                self.semantic[key] = [2, j]
                self.instances[key] = pi
                self.choices.setdefault(C.cidkey(j), pi)
            else:
                if d[0] == 2:
                    array(row[4], 3)
                    require(uint(row[4][1], 1) == 0, "unsafe opaque")
                else:
                    array(row[4], 3); uint(row[4][1])
                value_id = self.store.add(0x10, 2, [self.store.foundation, arity, *value])
                tag = 0x11 if d[0] == 0 else 0x19
                oid = self.store.add(tag, 2, [self.store.foundation, arity, type_id, value_id])
                self.semantic[key] = [1 if d[0] == 0 else 4, oid]
        self.active.remove(key); self.done.add(key)

    def all(self):
        for key in sorted(self.units):
            self.compile(key)
        for root in self.roots:
            require(namekey(root) in self.semantic, "uncaptured root")

    def replay(self, name):
        key = namekey(name)
        require(key in self.semantic, "unknown requested source root")
        r = self.semantic[key]
        require(r[0] != 0, "seed is not ordinary contribution root")
        typed_root = [4, self.instances[key]] if r[0] == 2 else [{1: 1, 3: 2, 4: 3}[r[0]], r[1]]
        # Plan once with available source choices, then commit only reached aliases.
        planner = Planner(self.store, self.choices)
        planner.root(typed_root)
        selected = {k: self.choices[k] for k in planner.required_aliases}
        return self.store.add(0x15, 3, [self.store.foundation, typed_root, trie(self.store, selected, True)])

    def mapping(self):
        return {"schema": 1, "foundation": C.to_projection(self.store.foundation),
                "names": [{"name": C.to_projection(self.names[k]),
                           "semantic": C.to_projection(r),
                           "instance": C.to_projection([1, self.instances[k]] if k in self.instances else [0])}
                          for k, r in sorted(self.semantic.items())]}


def direct_refs(dag):
    result = {}
    for n in dag[1]:
        if n[0] in (2, 8) and n[1][0] in (1, 2, 3, 4):
            result[C.cidkey(n[1][1])] = None
    return result


def make_judgment(store, arity, closed_type):
    type_id = store.add(0x10, 2, [store.foundation, arity, *closed_type])
    context = store.add(0x12, 2, [store.foundation, trie(store, direct_refs(closed_type))])
    return store.add(0x13, 2, [context, arity, [], type_id])


class Planner:
    def __init__(self, store, representatives):
        self.store, self.representatives = store, representatives
        self.batch, self.required_aliases = [], set()
        self.done, self.active, self.statements = set(), set(), {}
        self.bindings = {namekey(n): [0, i] for i, n in enumerate(store.seed[2])}
        for ref, payload in store.objects.values():
            if ref[1:3] in ([0x11, 2], [0x13, 2], [0x19, 2], [0x23, 1]):
                rt = {0x11: 1, 0x13: 2, 0x19: 4, 0x23: 7}[ref[1]]
                r = [rt, ref]; self.bindings[namekey(native_name(r))] = r
            elif ref[1:3] == [0x18, 2]:
                array(payload, 4)
                for i, desc in enumerate(array(payload[3])):
                    array(desc, 2)
                    selectors = [[0, i], [2, i]] + [[1, i, k] for k in range(len(array(desc[1])))]
                    for selector in selectors:
                        r = [3, ref, selector]; self.bindings[namekey(native_name(r))] = r

    def enter(self, kind, ref):
        key = (kind, identity(ref))
        require(key not in self.active, "selected semantic/evidence dependency cycle")
        if key in self.done:
            return False
        require(len(self.active) < 512, "selected dependency depth")
        self.active.add(key)
        return True

    def leave(self, kind, ref):
        key = (kind, identity(ref))
        self.active.remove(key); self.done.add(key)

    def reference(self, ref, projection=False, *, witness=False, locals=0, suppress_group=None):
        array(ref); require(ref, "empty constant reference")
        tag = uint(ref[0], 7)
        if tag == 0:
            array(ref, 2)
            require(uint(ref[1]) < len(self.store.seed[2]), "seed export index")
        elif tag == 5:
            array(ref, 2)
            require(not projection and uint(ref[1]) < locals, "escaped/invalid group-local type")
        elif tag in (1, 2, 4, 7):
            array(ref, 2)
            require(not projection and (tag != 7 or witness) and (tag != 2 or not witness),
                    "semantic/witness/projection reference grammar")
            if tag == 1:
                typed(ref[1], 0x11, 2); self.declaration(ref[1], False)
            elif tag == 4:
                typed(ref[1], 0x19, 2); self.declaration(ref[1], True)
            elif tag == 2:
                typed(ref[1], 0x13, 2); self.alias(ref[1])
            else:
                typed(ref[1], 0x23, 1); self.instance(ref[1])
        elif tag == 3:
            array(ref, 3)
            group = array(self.store.get(ref[1], 0x18, 2), 4)
            selector = array(ref[2]); require(selector, "group selector")
            st = uint(selector[0], 2)
            array(selector, 3 if st == 1 else 2)
            ti = uint(selector[1]); require(ti < len(group[3]), "group type selector")
            if st == 1:
                require(uint(selector[2]) < len(group[3][ti][1]), "constructor selector")
            require(not projection or st == 0, "projection structure selector")
            if suppress_group != ref[1]:
                self.group(ref[1])
        else:
            raise ValueError("unsupported external reference")
        return ref

    def dag(self, dag, arity, witness=False, locals=0, suppress_group=None):
        output = transform_dag(dag, arity,
                               lambda r, p: self.reference(r, p, witness=witness, locals=locals,
                                                           suppress_group=suppress_group))
        require(output == dag, "noncanonical semantic/witness DAG")
        # Exact native universe-vector arity is checked again by the native decoder.
        # For non-seed references the descriptor permits checking it here as well.
        for n in dag[1]:
            if n[0] != 2 or n[1][0] in (0, 5):
                continue
            r = n[1]
            if r[0] in (1, 4):
                u = self.store.get(r[1])[1]
            elif r[0] == 2:
                u = self.store.get(r[1], 0x13, 2)[1]
            elif r[0] == 7:
                u = self.store.get(self.store.get(r[1], 0x23, 1)[0], 0x13, 2)[1]
            elif r[2][0] != 2:
                u = self.store.get(r[1], 0x18, 2)[1]
            else:
                inventory = self.store.inventories.get(identity(r[1]))
                require(inventory is not None, "generated inventory unavailable")
                name = native_name(r)
                rows = [row for row in inventory if row[0] == name]
                require(len(rows) == 1 and rows[0][1] == 6, "recursor inventory selector")
                u = rows[0][2]
            require(len(n[2]) == u, "explicit universe instantiation arity")
        return dag

    def term(self, ref, arity, witness=False):
        payload = array(self.store.get(ref, 0x22 if witness else 0x10, 1 if witness else 2), 5)
        require(payload[0] == self.store.foundation and payload[1] == arity, "term foundation/universe arity")
        return self.dag(payload[2:], arity, witness)

    def statement(self, j):
        if not self.enter("S", j):
            return self.statements[identity(j)]
        payload = array(self.store.get(j, 0x13, 2), 4)
        arity = uint(payload[1], MAX_UNIVERSES)
        require(payload[2] == [], "this ordinary-source cut requires empty explicit telescope; full Pi type retained")
        ty = self.term(payload[3], arity)
        context = array(self.store.get(payload[0], 0x12, 2), 2)
        require(context[0] == self.store.foundation, "statement context foundation")
        actual_refs = parse_trie(self.store, context[1])
        require(actual_refs == direct_refs(ty), "statement exact direct semantic references")
        self.statements[identity(j)] = (arity, ty)
        self.leave("S", j)
        return arity, ty

    def instance(self, pi):
        if not self.enter("I", pi):
            return
        payload = array(self.store.get(pi, 0x23, 1), 2)
        arity, ty = self.statement(payload[0])
        value = self.term(payload[1], arity, True)
        self.batch.append({"kind": 1, "id": C.to_projection(pi), "u": arity,
                           "type": C.to_projection(ty), "value": C.to_projection(value)})
        self.leave("I", pi)

    def alias(self, j):
        key = C.cidkey(j)
        self.required_aliases.add(key)
        if not self.enter("A", j):
            return
        require(key in self.representatives, "missing exact semantic representative")
        pi = self.representatives[key]
        payload = array(self.store.get(pi, 0x23, 1), 2)
        require(payload[0] == j, "representative proves different judgment")
        arity, ty = self.statement(j)
        self.instance(pi)
        value = [[[4, i] for i in range(arity)], [[2, [7, pi], list(range(arity))]], 0]
        self.batch.append({"kind": 4, "id": C.to_projection(j), "u": arity,
                           "type": C.to_projection(ty), "value": C.to_projection(value)})
        self.leave("A", j)

    def declaration(self, ref, opaque):
        kind = "O" if opaque else "D"
        if not self.enter(kind, ref):
            return
        payload = array(self.store.get(ref, 0x19 if opaque else 0x11, 2), 4)
        require(payload[0] == self.store.foundation, "declaration foundation")
        arity = uint(payload[1], MAX_UNIVERSES)
        ty, value = self.term(payload[2], arity), self.term(payload[3], arity)
        self.batch.append({"kind": 2 if opaque else 0, "id": C.to_projection(ref), "u": arity,
                           "type": C.to_projection(ty), "value": C.to_projection(value)})
        self.leave(kind, ref)

    def group(self, gid):
        if not self.enter("G", gid):
            return
        payload = array(self.store.get(gid, 0x18, 2), 4)
        require(payload[0] == self.store.foundation, "group foundation")
        arity, np = uint(payload[1], MAX_UNIVERSES), uint(payload[2])
        types = array(payload[3]); require(0 < len(types) <= MAX_GROUP_TYPES, "group type count")
        expected_names, direct = set(), set()
        for i, desc in enumerate(types):
            array(desc, 2); array(desc[1])
            require(len(desc[1]) <= MAX_GROUP_CONSTRUCTORS, "group constructor count")
            for dag in [desc[0], *desc[1]]:
                self.dag(dag, arity, locals=len(types))
                direct.update(direct_refs(dag))
            selectors = [[0, i], [2, i]] + [[1, i, k] for k in range(len(desc[1]))]
            expected_names.update(namekey(native_name([3, gid, s])) for s in selectors)
        inventory = self.store.inventories.get(identity(gid))
        require(type(inventory) is list and len(inventory) <= MAX_EXPORTS, "required group inventory")
        require({namekey(r[0]) for r in inventory} == expected_names and len(inventory) == len(expected_names),
                "exact generated member names")
        observed = set()
        def resolve(raw, projection=False):
            array(raw, 2); require(raw[0] == 6, "inventory raw reference")
            nk = namekey(raw[1]); require(nk in self.bindings, "unbound inventory native name")
            r = self.bindings[nk]
            self.reference(r, projection, suppress_group=gid)
            if r[0] not in (0, 5) and not (r[0] == 3 and r[1] == gid):
                observed.add(C.cidkey(r[1]))
            return raw
        normalized = normalize_inventory(inventory, resolve, lambda n: n)
        require(normalized == inventory, "noncanonical normalized generated inventory")
        require(observed <= direct, "unexplained generated external dependency")
        by_name = {namekey(r[0]): r for r in inventory}
        all_names = [native_name([3, gid, [0, i]]) for i in range(len(types))]
        for i, desc in enumerate(types):
            tn = native_name([3, gid, [0, i]])
            tr = by_name[namekey(tn)]
            require(tr[1] == 4 and tr[2] == arity and tr[4][0] == np and tr[4][2] == all_names,
                    "generated type binding")
            ctors = [native_name([3, gid, [1, i, k]]) for k in range(len(desc[1]))]
            require(tr[4][3] == ctors, "generated constructor ordering")
            rr = by_name[namekey(native_name([3, gid, [2, i]]))]
            require(rr[1] == 6 and rr[4][0] == all_names and rr[4][1] == np, "generated recursor association")
            for k, cn in enumerate(ctors):
                cr = by_name[namekey(cn)]
                require(cr[1] == 5 and cr[2] == arity and cr[4][0] == tn
                        and cr[4][1] == k and cr[4][2] == np, "generated constructor binding")
        self.batch.append({"kind": 3, "id": C.to_projection(gid), "u": arity, "numParams": np,
                           "types": C.to_projection(types), "inventory": C.to_projection(inventory)})
        self.leave("G", gid)

    def root(self, root):
        array(root, 2); tag = uint(root[0], 4)
        if tag == 4:
            self.instance(root[1])
        elif tag == 1:
            self.declaration(root[1], False)
        elif tag == 2:
            self.group(root[1])
        elif tag == 3:
            self.declaration(root[1], True)
        else:
            raise ValueError("unsupported PI1 root")
        # The finite native reader counts checked alias declarations as batch rows.
        require(len(self.batch) <= MAX_UNITS, "selected native batch row allowance including aliases")
        require(sum(len(row["inventory"]) if row["kind"] == 3 else 1 for row in self.batch)
                <= MAX_EXPORTS, "selected native export allowance")


def make_plan(store, roots, presentation=None):
    require(0 < len(roots) <= MAX_UNITS, "finite nonempty root list")
    require(len({identity(r) for r in roots}) == len(roots), "duplicate replay root")
    choices, root_payloads = {}, []
    for root in roots:
        replay = array(store.get(root, 0x15, 3), 3)
        require(replay[0] == store.foundation, "replay foundation")
        selected = parse_trie(store, replay[2], True)
        individual = Planner(store, selected)
        individual.root(replay[1])
        require(individual.required_aliases == set(selected), "missing/extra representative-map entry")
        for k, pi in selected.items():
            require(k not in choices or choices[k] == pi, "incompatible representative contexts; rebuild required")
            choices[k] = pi
        root_payloads.append(replay)
    joined = Planner(store, choices)
    for replay in root_payloads:
        joined.root(replay[1])
    require(joined.required_aliases == set(choices), "joined exact representative context")
    result = {"seed": C.to_projection(store.seed), "foundation": C.to_projection(store.foundation),
              "replays": C.to_projection(roots), "batch": joined.batch}
    if presentation is not None:
        fields(presentation, ["subtype", "val", "injective", "a", "map", "law"])
        saved = len(joined.batch)
        for ref in presentation.values():
            joined.reference(C.from_projection(ref), witness=True)
        require(len(joined.batch) == saved, "presentation names an unchecked/unprepared contribution")
        result["presentation"] = presentation
    return result


def export_package(store, root, destination):
    make_plan(store, [root])
    selected = store.closure(root)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "objects").mkdir()
    for key in sorted(selected):
        (destination / "objects" / (key + ".cbor")).write_bytes(C.dumps(store.objects[key][1]))
    inventories = [[store.objects[key][0], store.inventories[key]] for key in sorted(selected)
                   if store.objects[key][0][1:3] == [0x18, 2]]
    manifest = {"foundation": C.to_projection(store.foundation), "root": C.to_projection(root),
                "objects": C.to_projection([store.objects[k][0] for k in sorted(selected)]),
                "inventories": C.to_projection(inventories)}
    (destination / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")


def read_package(path, seed):
    path = Path(path)
    manifest = strict_json(read_bytes(path / "manifest.json", 16 * 1024 * 1024))
    fields(manifest, ["foundation", "root", "objects", "inventories"])
    store = Store(seed)
    require(C.from_projection(manifest["foundation"]) == store.foundation, "unadopted foundation")
    ids = C.from_projection(manifest["objects"])
    require(type(ids) is list and 0 < len(ids) <= MAX_OBJECTS, "package object count")
    provided, total = set(), 0
    for ref in ids:
        key = identity(ref); require(key not in provided, "duplicate package object")
        raw = read_bytes(path / "objects" / (key + ".cbor"), MAX_BYTES - total)
        total += len(raw)
        payload = C.loads(raw)
        require(C.cid(ref[1], ref[2], payload) == ref, "misaddressed package object")
        store.add(ref[1], ref[2], payload); provided.add(key)
    for record in store.base.values():
        require(identity(record["id"]) in provided, "missing unchanged foundation component")
    invs = C.from_projection(manifest["inventories"])
    for pair in array(invs):
        array(pair, 2); typed(pair[0], 0x18, 2)
        key = identity(pair[0]); require(key in provided and key not in store.inventories, "group inventory binding")
        store.inventories[key] = pair[1]
    require(set(store.inventories) == {k for k in provided if store.objects[k][0][1:3] == [0x18, 2]},
            "missing/extra group inventory")
    root = C.from_projection(manifest["root"])
    require(store.closure(root) == provided, "package is not exact root closure")
    make_plan(store, [root])
    return store, root


def merge_packages(seed, paths):
    joined, roots = Store(seed), []
    for path in paths:
        store, root = read_package(path, seed)
        for ref, payload in store.objects.values():
            joined.add(ref[1], ref[2], payload)
        for key, inventory in store.inventories.items():
            require(key not in joined.inventories or same(joined.inventories[key], inventory),
                    "incompatible generated-inventory claims")
            joined.inventories[key] = inventory
        if root not in roots:
            roots.append(root)
    make_plan(joined, roots)
    return joined, roots


def reexport_actual(store, roots, actual):
    """Rebuild all nonfoundation mathematical objects from actual native rows.

    The caller must separately bind actual to its immutable native run, source,
    command and exact input plan. This function does not authenticate run logs.
    """
    fields(actual, ["foundation", "replays", "batch"])
    expected = make_plan(store, roots)
    expected_actual = {key: expected[key] for key in ("foundation", "replays", "batch")}
    require(same(actual, expected_actual), "incomplete/altered actual-native export")
    rebuilt = Store(store.seed)
    for row in actual["batch"]:
        kind, ref, arity = row["kind"], C.from_projection(row["id"]), row["u"]
        if kind == 3:
            types = C.from_projection(row["types"])
            result = rebuilt.add(0x18, 2, [rebuilt.foundation, arity, row["numParams"], types])
            rebuilt.inventories[identity(result)] = C.from_projection(row["inventory"])
        else:
            ty, value = C.from_projection(row["type"]), C.from_projection(row["value"])
            type_id = rebuilt.add(0x10, 2, [rebuilt.foundation, arity, *ty])
            if kind in (0, 2):
                value_id = rebuilt.add(0x10, 2, [rebuilt.foundation, arity, *value])
                result = rebuilt.add(0x11 if kind == 0 else 0x19, 2,
                                     [rebuilt.foundation, arity, type_id, value_id])
            else:
                j = make_judgment(rebuilt, arity, ty)
                if kind == 1:
                    value_id = rebuilt.add(0x22, 1, [rebuilt.foundation, arity, *value])
                    result = rebuilt.add(0x23, 1, [j, value_id])
                else:
                    result = j
                    require(len(value[1]) == 1 and value[1][0][0] == 2
                            and value[1][0][1][0] == 7, "actual semantic alias shape")
                    pi = value[1][0][1][1]
                    require(rebuilt.get(pi, 0x23, 1)[0] == j, "actual alias representative target")
                    canonical = [[[4, i] for i in range(arity)], [[2, [7, pi], list(range(arity))]], 0]
                    require(value == canonical, "actual semantic alias body")
        require(result == ref, "actual native re-export changed identity")
    for root in roots:
        original = store.get(root, 0x15, 3)
        selected = parse_trie(store, original[2], True)
        new_map = trie(rebuilt, selected, True)
        result = rebuilt.add(0x15, 3, [rebuilt.foundation, original[1], new_map])
        require(result == root, "actual replay identity changed")
    require(same(make_plan(rebuilt, roots), expected), "actual native reconstruction is incomplete")
    for root in roots:
        require(rebuilt.closure(root) == store.closure(root), "actual native closure changed")
        for key in rebuilt.closure(root):
            require(rebuilt.objects[key] == store.objects[key], "actual native canonical object changed")
    return rebuilt


def read_record(path, prefix):
    raw = read_bytes(path)
    if raw.lstrip().startswith(b"{"):
        return strict_json(raw)
    selected = [line[len(prefix):] for line in raw.splitlines() if line.startswith(prefix)]
    require(len(selected) == 1, "exactly one bound native JSON record required")
    return strict_json(selected[0])


def write_json(path, value):
    raw = json.dumps(value, separators=(",", ":"), ensure_ascii=False) + "\n"
    require(len(raw.encode("utf-8")) <= MAX_BYTES, "JSON output byte allowance")
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codec-path", required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    cap = commands.add_parser("capture")
    cap.add_argument("--seed", required=True)
    cap.add_argument("--capture", required=True)
    cap.add_argument("--root-name", required=True)
    cap.add_argument("--package", required=True)
    cap.add_argument("--plan", required=True)
    cap.add_argument("--mapping", required=True)
    cap.add_argument("--inherit", action="append", default=[])
    prep = commands.add_parser("prepare")
    prep.add_argument("--seed", required=True)
    prep.add_argument("--package", action="append", required=True)
    prep.add_argument("--plan", required=True)
    prep.add_argument("--presentation")
    inv = commands.add_parser("reexport")
    inv.add_argument("--seed", required=True)
    inv.add_argument("--package", action="append", required=True)
    inv.add_argument("--actual", required=True)
    inv.add_argument("--output", required=True)
    inv.add_argument("--plan", required=True)
    args = parser.parse_args()
    configure_codec(args.codec_path)
    seed = C.from_projection(strict_json(read_bytes(args.seed)))
    if args.command == "capture":
        inherited, inherited_roots = (merge_packages(seed, args.inherit) if args.inherit else (None, []))
        capture = read_record(args.capture, b"SOURCE_CAPTURE_JSON ")
        compiler = SourceCompiler(seed, capture, inherited, inherited_roots)
        compiler.all()
        root = compiler.replay(C.name_path(args.root_name))
        plan = make_plan(compiler.store, [root])
        export_package(compiler.store, root, args.package)
        write_json(args.plan, plan)
        write_json(args.mapping, compiler.mapping())
        result = {"status": "COMPLETE_CANDIDATE_EXPORTED_NOT_NATIVE_ACCEPTANCE",
                  "replay": C.to_projection(root), "objects": len(compiler.store.closure(root)),
                  "nativeUnits": len(plan["batch"])}
    elif args.command == "prepare":
        store, roots = merge_packages(seed, args.package)
        presentation = strict_json(read_bytes(args.presentation, 1024 * 1024)) if args.presentation else None
        plan = make_plan(store, roots, presentation)
        write_json(args.plan, plan)
        result = {"status": "EXACT_ROOT_UNION_PLAN_NOT_NATIVE_ACCEPTANCE", "roots": len(roots),
                  "nativeUnits": len(plan["batch"])}
    else:
        store, roots = merge_packages(seed, args.package)
        require(len(roots) == 1, "final independent re-export selects one exact successor root")
        actual = read_record(args.actual, b"ACTUAL_BATCH_JSON ")
        rebuilt = reexport_actual(store, roots, actual)
        export_package(rebuilt, roots[0], args.output)
        write_json(args.plan, make_plan(rebuilt, roots))
        result = {"status": "ACTUAL_ROWS_REENCODED_REQUIRES_BOUND_RUN_AND_FRESH_NATIVE_REPLAY",
                  "replay": C.to_projection(roots[0]), "objects": len(rebuilt.closure(roots[0]))}
    print(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    main()
