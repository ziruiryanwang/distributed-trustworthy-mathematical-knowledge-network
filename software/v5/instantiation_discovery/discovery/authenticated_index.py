"""Pure, domain-separated commitments and ordinal proofs for discovery metadata.

Membership commits provider-selected metadata. It is not proof of truthful
feature extraction, complete indexing of a corpus, or mathematical validity.
The I/O object only supplies get_node(hash) and put_node(node).
"""
from __future__ import annotations

import hashlib
from contextlib import contextmanager
from contextvars import ContextVar
from functools import lru_cache
from .formal_features import (SCHEMA, EXPORT_SCHEMA, EXPORT_PAIR_SCHEMA, EXPORT_TYPE_PATTERN_SCHEMA,
                              EXPORT_CONCLUSION_FINGERPRINT_SCHEMA,
                              compact, digest as _digest, fields, hexid, need, uint)

MAX_VECTOR = 1048576
_HASH_METER = ContextVar("discovery_hash_meter", default=None)


@contextmanager
def hash_meter(callback):
    """Operation-scoped SHA invocation accounting; no persistent authority."""
    token = _HASH_METER.set(callback)
    try: yield
    finally: _HASH_METER.reset(token)


def _charge_hash():
    callback = _HASH_METER.get()
    if callback is not None: callback()


def digest(domain, value):
    _charge_hash()
    return _digest(domain, value)


def H(domain, *parts):
    _charge_hash()
    return hashlib.sha256(("DMKN-DISCOVERY-" + domain + "-V1").encode("ascii")
                          + b"\0" + b"".join(parts)).hexdigest()


def raw(value): return bytes.fromhex(hexid(value))
def number(value): return uint(value, 0, 2**64-1).to_bytes(8, "big")


def context(namespace, feature_id, partition):
    uint(partition, 0, 255, "PARTITION")
    return digest("DMKN-DISCOVERY-CONTEXT-V1", {
        "namespace": hexid(namespace), "feature_id": hexid(feature_id), "partition": partition})


def vector_empty(ctx, height=0):
    uint(height, 0, 20, "VECTOR_HEIGHT")
    value = H("PAD", raw(ctx))
    for _ in range(height): value = H("NODE", raw(value), raw(value))
    return value


def vector_height(count):
    return (max(1, uint(count, 0, MAX_VECTOR, "VECTOR_COUNT"))-1).bit_length()


def vector_commit(ctx, count, tree_root):
    uint(count, 0, MAX_VECTOR, "VECTOR_COUNT")
    return H("VECTOR", raw(ctx), number(count), raw(tree_root))


@lru_cache(maxsize=1)
def partition_empty():
    values = [H("PARTITION-EMPTY")]
    for _ in range(8): values.append(H("PARTITION-NODE", raw(values[-1]), raw(values[-1])))
    return tuple(values)


@lru_cache(maxsize=64)
def map_empty(namespace):
    # Immutable bounded cache: at most64 namespace/default chains, never nodes.
    hexid(namespace)
    values = [None] * 257
    values[256] = H("MAP-EMPTY-LEAF", raw(namespace))
    for depth in range(255, -1, -1):
        values[depth] = H("MAP-NODE", depth.to_bytes(2, "big"), raw(values[depth+1]), raw(values[depth+1]))
    return tuple(values)


def node_hash(node):
    need(type(node) is dict, "NODE_SHAPE")
    kind = node.get("kind")
    if kind == "vector-leaf":
        fields(node, ("kind", "context", "index", "record_id"))
        uint(node["index"], 0, MAX_VECTOR-1, "VECTOR_INDEX")
        return H("LEAF", raw(node["context"]), number(node["index"]), raw(node["record_id"]))
    if kind in ("vector-node", "partition-node"):
        fields(node, ("kind", "left", "right"))
        return H("NODE" if kind == "vector-node" else "PARTITION-NODE", raw(node["left"]), raw(node["right"]))
    if kind == "partition-leaf":
        fields(node, ("kind", "namespace", "feature_id", "partition", "count", "tree_root"))
        uint(node["count"], 1, MAX_VECTOR, "NONEMPTY_PARTITION")
        ctx = context(node["namespace"], node["feature_id"], node["partition"])
        committed = vector_commit(ctx, node["count"], node["tree_root"])
        return H("PARTITION-LEAF", raw(ctx), raw(committed))
    if kind == "map-leaf":
        fields(node, ("kind", "feature_id", "feature_root"))
        return H("MAP-LEAF", raw(node["feature_id"]), raw(node["feature_root"]))
    if kind == "map-node":
        fields(node, ("kind", "depth", "left", "right"))
        depth = uint(node["depth"], 0, 255, "MAP_DEPTH")
        return H("MAP-NODE", depth.to_bytes(2, "big"), raw(node["left"]), raw(node["right"]))
    if kind == "map-run":
        return _run_values(node)[0]
    raise ValueError("NODE_KIND")


def _path_mask(depth, end):
    return ((1 << (end-depth))-1) << (256-end)


def _run_values(node):
    fields(node, ("kind", "namespace", "depth", "end_depth", "path", "child"))
    need(node["kind"] == "map-run", "MAP_RUN_KIND")
    namespace = hexid(node["namespace"])
    depth = uint(node["depth"], 0, 255, "MAP_RUN_DEPTH")
    end = uint(node["end_depth"], depth+1, 256, "MAP_RUN_END")
    path = int(hexid(node["path"]), 16)
    need(path & ~_path_mask(depth, end) == 0, "MAP_RUN_PATH_MASK")
    empty = map_empty(namespace)
    value = hexid(node["child"])
    need(value != empty[end], "MAP_RUN_EMPTY_CHILD")
    values = [None] * (end-depth+1); values[-1] = value
    for level in range(end-1, depth-1, -1):
        left, right = (empty[level+1], value) if (path >> (255-level)) & 1 else (value, empty[level+1])
        value = H("MAP-NODE", level.to_bytes(2, "big"), raw(left), raw(right))
        values[level-depth] = value
    return values


def _get(io, expected, kind):
    node = io.get_node(expected)
    need(node.get("kind") == kind and node_hash(node) == expected, "AUTHENTICATED_NODE_BINDING")
    return node


def append_vector(io, ctx, count, tree_root, rid):
    uint(count, 0, MAX_VECTOR-1, "VECTOR_FULL"); hexid(rid)
    old_height, height = vector_height(count), vector_height(count+1)
    empty = [vector_empty(ctx)]
    for _ in range(height): empty.append(H("NODE", raw(empty[-1]), raw(empty[-1])))
    if count == 0:
        need(tree_root == empty[0], "EMPTY_VECTOR_ROOT")
    elif height > old_height:
        tree_root = io.put_node({"kind": "vector-node", "left": tree_root,
                                 "right": empty[old_height]})
    def insert(current, level):
        if level == 0:
            need(current == empty[0], "APPEND_OVERWRITE")
            return io.put_node({"kind": "vector-leaf", "context": ctx, "index": count, "record_id": rid})
        if current == empty[level]:
            left = right = empty[level-1]
        else:
            node = _get(io, current, "vector-node"); left, right = node["left"], node["right"]
        if (count >> (level-1)) & 1: right = insert(right, level-1)
        else: left = insert(left, level-1)
        return io.put_node({"kind": "vector-node", "left": left, "right": right})
    return insert(tree_root, height)


def vector_get(io, ctx, count, tree_root, index):
    uint(index, 0, uint(count, 1, MAX_VECTOR)-1, "VECTOR_INDEX")
    current, siblings = tree_root, []
    for level in range(vector_height(count), 0, -1):
        node = _get(io, current, "vector-node")
        bit = (index >> (level-1)) & 1
        siblings.append(node["left"] if bit else node["right"])
        current = node["right"] if bit else node["left"]
    leaf = _get(io, current, "vector-leaf")
    need(leaf["context"] == ctx and leaf["index"] == index, "VECTOR_LEAF_BINDING")
    return leaf["record_id"], list(reversed(siblings))


def verify_vector(ctx, count, tree_root, index, rid, siblings):
    uint(index, 0, uint(count, 1, MAX_VECTOR)-1, "VECTOR_INDEX")
    need(type(siblings) is list and len(siblings) == vector_height(count), "VECTOR_PROOF_LENGTH")
    value = node_hash({"kind": "vector-leaf", "context": ctx, "index": index, "record_id": rid})
    for level, sibling in enumerate(siblings):
        value = H("NODE", raw(sibling), raw(value)) if ((index >> level) & 1) else H("NODE", raw(value), raw(sibling))
    need(value == tree_root, "VECTOR_PROOF_ROOT")


def empty_descriptor(namespace, feature_id, partition):
    return {"partition": partition, "count": 0, "tree_root": vector_empty(context(namespace, feature_id, partition))}


def descriptor_hash(namespace, feature_id, desc):
    fields(desc, ("partition", "count", "tree_root"))
    p = uint(desc["partition"], 0, 255, "PARTITION")
    uint(desc["count"], 0, MAX_VECTOR, "PARTITION_COUNT"); hexid(desc["tree_root"])
    if desc["count"] == 0:
        need(desc == empty_descriptor(namespace, feature_id, p), "EMPTY_PARTITION_BINDING")
        return partition_empty()[0]
    return node_hash({"kind": "partition-leaf", "namespace": namespace, "feature_id": feature_id, **desc})


def partition_get(io, namespace, feature_id, root, partition):
    uint(partition, 0, 255, "PARTITION")
    empty, current, siblings = partition_empty(), root, []
    for height in range(8, 0, -1):
        if current == empty[height]: left = right = empty[height-1]
        else:
            node = _get(io, current, "partition-node"); left, right = node["left"], node["right"]
        bit = (partition >> (height-1)) & 1
        siblings.append(left if bit else right); current = right if bit else left
    if current == empty[0]: desc = empty_descriptor(namespace, feature_id, partition)
    else:
        node = _get(io, current, "partition-leaf")
        need(node["namespace"] == namespace and node["feature_id"] == feature_id
             and node["partition"] == partition, "PARTITION_LEAF_BINDING")
        desc = {k: node[k] for k in ("partition", "count", "tree_root")}
    return desc, list(reversed(siblings))


def partition_set(io, namespace, feature_id, root, desc):
    p = desc["partition"]; descriptor_hash(namespace, feature_id, desc)
    _, siblings = partition_get(io, namespace, feature_id, root, p)
    value = io.put_node({"kind": "partition-leaf", "namespace": namespace, "feature_id": feature_id, **desc})
    for level, sibling in enumerate(siblings):
        left, right = (sibling, value) if (p >> level) & 1 else (value, sibling)
        value = io.put_node({"kind": "partition-node", "left": left, "right": right})
    return value


def feature_root(namespace, feature_id, descriptors):
    need(type(descriptors) is list and len(descriptors) == 256, "PARTITION_SUMMARY_COUNT")
    level = []
    for p, desc in enumerate(descriptors):
        need(type(desc) is dict and desc.get("partition") == p, "PARTITION_SUMMARY_ORDER")
        level.append(descriptor_hash(namespace, feature_id, desc))
    while len(level) > 1:
        level = [H("PARTITION-NODE", raw(level[i]), raw(level[i+1])) for i in range(0, len(level), 2)]
    return level[0]


def _map_endpoint(node, namespace, depth):
    """V2 canonical endpoints: leaf or two-nonempty-child branch, never a run."""
    if depth == 256:
        need(node["kind"] == "map-leaf", "MAP_ENDPOINT_LEAF")
    else:
        need(node["kind"] == "map-node" and node["depth"] == depth, "MAP_ENDPOINT_BRANCH")
        empty = map_empty(namespace)[depth+1]
        need(node["left"] != empty and node["right"] != empty, "MAP_UNCOMPRESSED_UNARY")


def _map_read(io, namespace, current, depth):
    node = io.get_node(current)
    need(node_hash(node) == current, "AUTHENTICATED_NODE_BINDING")
    if node["kind"] != "map-run":
        _map_endpoint(node, namespace, depth)
        return node
    need(node["namespace"] == namespace and node["depth"] == depth, "MAP_RUN_CONTEXT")
    # Hash equality alone cannot establish maximal/canonical physical encoding.
    # Inspect its endpoint: an adjacent run or expanded unary branch refuses.
    child = io.get_node(node["child"])
    need(node_hash(child) == node["child"], "AUTHENTICATED_NODE_BINDING")
    _map_endpoint(child, namespace, node["end_depth"])
    return node


def validate_map_storage(io, namespace, node):
    """Fresh V2 CAS admission, after node_hash checked the exact fields."""
    if node["kind"] == "map-node":
        _map_endpoint(node, namespace, node["depth"])
    elif node["kind"] == "map-run":
        need(node["namespace"] == namespace, "MAP_RUN_CONTEXT")
        child = io.get_node(node["child"])
        need(node_hash(child) == node["child"], "AUTHENTICATED_NODE_BINDING")
        _map_endpoint(child, namespace, node["end_depth"])


def map_get(io, namespace, root, feature_id):
    key = int(hexid(feature_id), 16); empty = map_empty(namespace)
    current, siblings, depth = hexid(root), [], 0
    while depth < 256:
        if current == empty[depth]: return None, [*siblings, *empty[depth+1:]]
        node = _map_read(io, namespace, current, depth)
        if node["kind"] == "map-run":
            path = int(node["path"], 16); end = node["end_depth"]
            values = _run_values(node)
            for level in range(depth, end):
                if ((key ^ path) >> (255-level)) & 1:
                    return None, [*siblings, values[level-depth+1], *empty[level+2:]]
                siblings.append(empty[level+1])
            current, depth = node["child"], end
        else:
            bit = (key >> (255-depth)) & 1
            siblings.append(node["left"] if bit else node["right"])
            current = node["right"] if bit else node["left"]; depth += 1
    if current == empty[256]: return None, siblings
    leaf = _map_read(io, namespace, current, 256)
    need(leaf["feature_id"] == feature_id, "MAP_LEAF_KEY")
    return leaf["feature_root"], siblings


def _map_run(io, namespace, depth, end, key, child):
    if depth == end: return child
    endpoint = _map_read(io, namespace, child, end)
    if endpoint["kind"] == "map-run":
        key = (key & _path_mask(depth, end)) | int(endpoint["path"], 16)
        end, child = endpoint["end_depth"], endpoint["child"]
    return io.put_node({"kind": "map-run", "namespace": namespace, "depth": depth,
                        "end_depth": end, "path": f"{key & _path_mask(depth, end):064x}", "child": child})


def map_update(io, namespace, root, feature_id, update):
    """Single private traversal; update(old_feature_root_or_None) returns new root.

    The callback is local builder logic, never a network-supplied path token.
    New stores use maximal run encoding only; legacy expanded stores stay V1.
    """
    key = int(hexid(feature_id), 16); empty = map_empty(namespace); hexid(root)
    def new_leaf(old):
        value = hexid(update(old))
        return io.put_node({"kind": "map-leaf", "feature_id": feature_id, "feature_root": value})
    def visit(current, depth):
        if current == empty[depth]:
            return _map_run(io, namespace, depth, 256, key, new_leaf(None))
        node = _map_read(io, namespace, current, depth)
        if depth == 256:
            need(node["feature_id"] == feature_id, "MAP_LEAF_KEY")
            return new_leaf(node["feature_root"])
        if node["kind"] == "map-node":
            bit = (key >> (255-depth)) & 1
            changed = visit(node["right"] if bit else node["left"], depth+1)
            return io.put_node({"kind": "map-node", "depth": depth,
                "left": node["left"] if bit else changed, "right": changed if bit else node["right"]})
        end, path = node["end_depth"], int(node["path"], 16)
        mismatch = (key ^ path) & _path_mask(depth, end)
        if not mismatch:
            child = visit(node["child"], end)
            return _map_run(io, namespace, depth, end, path, child)
        split = 256-mismatch.bit_length()
        old_suffix = _map_run(io, namespace, split+1, end, path, node["child"])
        new_suffix = _map_run(io, namespace, split+1, 256, key, new_leaf(None))
        bit = (key >> (255-split)) & 1
        branch = io.put_node({"kind": "map-node", "depth": split,
            "left": old_suffix if bit else new_suffix, "right": new_suffix if bit else old_suffix})
        return _map_run(io, namespace, depth, split, path, branch)
    return visit(root, 0)


def map_set(io, namespace, root, feature_id, selected_root):
    hexid(selected_root)
    return map_update(io, namespace, root, feature_id, lambda old: selected_root)


def verify_map(namespace, root, feature_id, selected_root, siblings):
    need(type(siblings) is list and len(siblings) == 256, "MAP_PROOF_LENGTH")
    key = int(hexid(feature_id), 16)
    value = map_empty(namespace)[256] if selected_root is None else node_hash({
        "kind": "map-leaf", "feature_id": feature_id, "feature_root": selected_root})
    for depth in range(255, -1, -1):
        left, right = (siblings[depth], value) if (key >> (255-depth)) & 1 else (value, siblings[depth])
        value = H("MAP-NODE", depth.to_bytes(2, "big"), raw(left), raw(right))
    need(value == root, "MAP_PROOF_ROOT")


def validate_snapshot(value, namespace=None):
    fields(value, ("schema", "namespace", "feature_schema", "partition_bits", "feature_map_root",
                   "local_cut", "previous_snapshot", "coverage_claim"))
    need(value["schema"] == "DMKN_FORMAL_INDEX_SNAPSHOT_V1"
         and value["feature_schema"] in (SCHEMA, EXPORT_SCHEMA, EXPORT_PAIR_SCHEMA,
                                          EXPORT_TYPE_PATTERN_SCHEMA, EXPORT_CONCLUSION_FINGERPRINT_SCHEMA),
         "SNAPSHOT_SCHEMA")
    hexid(value["namespace"]); hexid(value["feature_map_root"])
    need(namespace is None or value["namespace"] == namespace, "SNAPSHOT_NAMESPACE")
    need(type(value["partition_bits"]) is int and value["partition_bits"] == 8, "PARTITION_PROFILE")
    uint(value["local_cut"], 0, 2**63-1, "LOCAL_CUT")
    if value["previous_snapshot"] is not None: hexid(value["previous_snapshot"])
    need(value["coverage_claim"] == "PROVIDER_SELECTED_FEATURE_RECORDS_NOT_GLOBAL_CORPUS", "SNAPSHOT_CLAIM")
    return value


def snapshot_id(value):
    return digest("DMKN-FORMAL-INDEX-SNAPSHOT-V1", validate_snapshot(value))
