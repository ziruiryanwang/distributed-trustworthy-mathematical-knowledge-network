"""Bounded advertised ordinary type metadata, never mathematical acceptance.

This is the semantic seam for a later index adapter, not an index, transport,
kernel or certificate protocol. A preview contains only an export's claimed
header and exact type-symbol bindings, never its proof/body or owner paths.
`resolve` binds that advertisement to exact inert evidence, still not to checked
mathematics. Native admission and warranted dependency matching remain required.

The internal syntax checks deliberately reuse ordinary_evidence's validators.
This module must be selected together with that exact API, not substituted for
the old certified-module adapter. No input chooses its own limits.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import hashlib

import ordinary_evidence as E


SCHEMA = "DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V1"
LOCATOR_SCHEMA = "DMKN_ORDINARY_LEAN_EXPORT_LOCATOR_V1"
PREVIEW_ASSURANCE = "ADVERTISED_TYPE_PREVIEW_NOT_EVIDENCE_BOUND"
BOUND_ASSURANCE = "EXACT_EVIDENCE_HEADER_BOUND_NOT_MATHEMATICAL_ACCEPTANCE"


class PreviewError(ValueError):
    """An indexing-profile refusal, not a verdict of mathematical invalidity."""


def _need(ok, code):
    if not ok:
        raise PreviewError(code)


@dataclass(frozen=True)
class Limits:
    """Trusted finite preview profile; evidence retains its separate defaults."""

    codec: E.Limits = field(default_factory=lambda: E.Limits(
        max_bytes=1024 * 1024, max_name_parts=256, max_name_bytes=65536,
        max_literal_bytes=65536, max_params=256, max_levels=8192,
        max_exprs=65536, max_names=4096, max_imports=4096))
    max_type_nodes: int = 65536
    max_type_bindings: int = 4096

    def __post_init__(self):
        _need(type(self.codec) is E.Limits, "PREVIEW_LIMIT_CODEC")
        _need(type(self.max_type_nodes) is int and
              1 <= self.max_type_nodes <= (1 << 32) - 1, "PREVIEW_NODE_CONFIGURATION")
        _need(type(self.max_type_bindings) is int and
              1 <= self.max_type_bindings <= self.codec.max_imports,
              "PREVIEW_BINDING_CONFIGURATION")


DEFAULT_LIMITS = Limits()


@dataclass(frozen=True)
class Preview:
    """Parsed advertisement. `document` is mutable data, not an authority token.

    At a changed boundary, reparse raw bytes. The public describe/resolve paths
    do so, rather than trusting an instance's fields or a saved success flag.
    """

    raw: bytes
    document: dict
    export_id: str
    type_reference_keys: tuple[bytes, ...]
    type_nodes: int

    @property
    def mathematical_acceptance(self):
        return False


def _type_census(header, limits):
    """Validate once with the existing grammar, then mark reachable DAG nodes.

    Reachability operates on indices, never recursively expands shared terms.
    Orphan expressions/levels are refused so the existing full-node reference
    census is exactly the root-reachable type census. This does not replace
    Lean's subsequent decode/re-encode and actual checking gates.
    """
    _need(type(limits) is Limits, "PREVIEW_LIMIT_CONFIGURATION")
    kind, raw_params, packet = E._array(header, 3)
    _need(1 <= E._uint(kind, 6), "PREVIEW_DECLARATION_KIND")
    params = E._names(raw_params, limits.codec.max_params, limits.codec, params=True)
    _, raw_levels, raw_nodes, _ = E._array(packet, 4)
    E._array(raw_levels, maximum=limits.codec.max_levels)
    E._array(raw_nodes, maximum=limits.codec.max_exprs)
    _need(len(raw_levels) + len(raw_nodes) <= limits.max_type_nodes,
          "PREVIEW_TYPE_NODE_BOUND")
    refs, count = E._dag_references(packet, params, limits.codec)
    _need(count <= limits.max_type_nodes, "PREVIEW_TYPE_NODE_BOUND")
    _need(len(refs) <= limits.max_type_bindings, "PREVIEW_TYPE_REFERENCE_BOUND")
    _, levels, nodes, root = packet
    expressions, universes = set(), set()
    todo_expr, todo_level = [root], []
    while todo_expr:
        index = todo_expr.pop()
        if index in expressions:
            continue
        expressions.add(index)
        node = nodes[index]
        tag = node[0]
        if tag == 1:
            todo_level.append(node[1])
        elif tag == 2:
            todo_level.extend(node[2])
        elif tag == 3:
            todo_expr.extend((node[1], node[2]))
        elif tag in (4, 5):
            todo_expr.extend((node[3], node[4]))
        elif tag == 6:
            todo_expr.extend((node[2], node[3], node[4]))
        elif tag == 8:
            todo_expr.append(node[3])
        # Bound variables and native Nat/String literals have no child edges.
    while todo_level:
        index = todo_level.pop()
        if index in universes:
            continue
        universes.add(index)
        node = levels[index]
        if node[0] == 1:
            todo_level.append(node[1])
        elif node[0] in (2, 3):
            todo_level.extend((node[1], node[2]))
    _need(len(expressions) == len(nodes) and len(universes) == len(levels),
          "PREVIEW_ORPHAN_TYPE_NODE")
    return tuple(sorted(refs)), count


def read_preview(raw, limits=DEFAULT_LIMITS):
    """Read canonical, bounded metadata; do not check a proof or fetch anything."""
    _need(type(limits) is Limits, "PREVIEW_LIMIT_CONFIGURATION")
    doc = E.strict_json(raw, limits.codec)
    _need(type(doc) is dict and set(doc) == {
        "schema", "profile_id", "unit_id", "export_name", "header", "type_bindings"},
        "PREVIEW_FIELDS")
    _need(doc["schema"] == SCHEMA, "PREVIEW_SCHEMA")
    E._hex(doc["profile_id"])
    E._hex(doc["unit_id"])
    E.name_key(doc["export_name"], limits.codec)
    refs, nodes = _type_census(doc["header"], limits)
    keys = []
    for row in E._array(doc["type_bindings"], maximum=limits.max_type_bindings):
        name, symbol = E._array(row, 2)
        keys.append(E.name_key(name, limits.codec))
        E._hex(symbol)
    _need(tuple(keys) == refs, "PREVIEW_TYPE_BINDING_CENSUS_OR_ORDER")
    export = E.export_id(doc["profile_id"], doc["unit_id"], doc["export_name"], limits.codec)
    return Preview(raw, doc, export, refs, nodes)


def _read_exact_evidence(evidence, expected_unit=None):
    # Evidence.document and Evidence.unit_id are mutable/caller-constructible
    # claims. Only bounded raw bytes enter the actual evidence reader again.
    raw = evidence.raw if type(evidence) is E.Evidence else evidence
    _need(type(raw) is bytes and 0 < len(raw) <= E.DEFAULT_LIMITS.max_bytes,
          "PREVIEW_EVIDENCE_BYTES")
    if expected_unit is not None:
        actual = hashlib.sha256(E.EVIDENCE_DOMAIN.encode("ascii") + b"\0" + raw).hexdigest()
        _need(actual == expected_unit, "PREVIEW_EVIDENCE_ID_MISMATCH")
    return E.read_evidence(raw)


def _from_checked_syntax(evidence, export_name, limits):
    """Private builder from freshly parsed inert syntax, not checked mathematics."""
    key = E.name_key(export_name, limits.codec)
    doc = evidence.document
    inventory = doc["unit"][2]
    selected = None
    for row in inventory:
        if E.name_key(row[0]) == key:
            selected = row
            break
    _need(selected is not None, "PREVIEW_EXPORT_NOT_IN_UNIT")
    header = [selected[1], selected[2], selected[3]]
    refs, _ = _type_census(header, limits)
    own_names = set(evidence.census.expected_names)
    imported = {E.name_key(name): symbol for name, symbol in doc["imports"]}
    bindings = []
    for reference in refs:
        name = E.strict_json(reference, limits.codec)
        if reference in own_names:
            symbol = E.export_id(doc["profile_id"], evidence.unit_id, name, limits.codec)
        else:
            _need(reference in imported, "PREVIEW_UNBOUND_TYPE_REFERENCE")
            symbol = imported[reference]
        bindings.append([name, symbol])
    raw = E.canonical_json({"schema": SCHEMA, "profile_id": doc["profile_id"],
        "unit_id": evidence.unit_id, "export_name": selected[0],
        "header": header, "type_bindings": bindings})
    # Enforce the total canonical byte bound and the same external read contract.
    read_preview(raw, limits)
    return raw


def preview_from_evidence(evidence, export_name, limits=DEFAULT_LIMITS):
    """Return proof-free canonical preview bytes from Evidence or raw evidence.

    The evidence reader checks bounded inert syntax (including body syntax), not
    mathematics. Only selected[1:4] and derived type bindings leave this function;
    proof/value bodies, other inventory rows and evidence imports are not emitted.
    A preview-profile refusal does not reject the underlying Lean declaration.
    """
    _need(type(limits) is Limits, "PREVIEW_LIMIT_CONFIGURATION")
    return _from_checked_syntax(_read_exact_evidence(evidence), export_name, limits)


def _description(preview, assurance, next_gate):
    doc = preview.document
    return {"assurance": assurance, "mathematical_acceptance": False,
        "next_gate": next_gate, "object_id": preview.export_id,
        "object_sha256": hashlib.sha256(preview.raw).hexdigest(),
        "object_bytes": len(preview.raw), "type_nodes": preview.type_nodes,
        "locator": {"schema": LOCATOR_SCHEMA, "profile_id": doc["profile_id"],
                    "unit_id": doc["unit_id"], "export_name": doc["export_name"]}}


def describe(raw, limits=DEFAULT_LIMITS):
    """Describe uncommitted advertised metadata, never a mathematical result.

    Authenticated-index membership is a later adapter's separate responsibility.
    This function therefore does not claim that any provider committed the bytes.
    """
    return _description(read_preview(raw, limits), PREVIEW_ASSURANCE,
                        "ACQUIRE_EXACT_ORDINARY_EVIDENCE")


def resolve(raw, evidence, limits=DEFAULT_LIMITS):
    """Bind the exact advertised header and type identities to inert evidence.

    This does not match dependency IDs to warranted local mathematics, reconstruct
    a basis, check Lean declarations, or promote a catalog entry. All those gates
    remain required even when this function returns successfully.
    """
    preview = read_preview(raw, limits)
    exact = _read_exact_evidence(evidence, preview.document["unit_id"])
    _need(exact.document["profile_id"] == preview.document["profile_id"],
          "PREVIEW_EVIDENCE_PROFILE_MISMATCH")
    expected = _from_checked_syntax(exact, preview.document["export_name"], limits)
    _need(expected == raw, "PREVIEW_EVIDENCE_HEADER_OR_BINDINGS_MISMATCH")
    return _description(preview, BOUND_ASSURANCE,
                        "MATCH_WARRANTED_DEPENDENCIES_AND_CHECK_ORDINARY_EXTENSION")
