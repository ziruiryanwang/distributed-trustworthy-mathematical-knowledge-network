"""Recover an original bounded authoring map from retained inert bytes.

No file/network access, native import, reauthoring, protected-state mutation or
mathematical acceptance. The caller selects and pins REQUEST.json, acquires the
exact files it names, and supplies a stable lookup in the eligible real parent.
A forged REQUEST hash is not evidence of historical execution or authority.
The returned identities are warranted only by that protected lookup premise;
new declarations still require the unchanged candidate/completion/admission path.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

import ordinary_evidence as E
import ordinary_semantics as S
import portable_owner_request as R

MIB = 1024**2
REQUEST_FIELDS = frozenset((
    "parent_root", "acquired_targets", "output_names", "output_targets",
    "request_files", "groups", "fetched", "payload_bytes", "acquired_bytes",
    "source_body_sha256", "generated_source", "authoring_profile",
    "mathematical_acceptance"))
HEADER_FIELDS = frozenset(("schema", "semantic_id", "foundation_id",
    "context_root", "basis_rows", "targets", "group_count"))
FRONTIER_HEADER_FIELDS = HEADER_FIELDS | {"frontier_root", "frontier_labels"}


def need(condition, code):
    if not condition:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _metadata_json(raw, check):
    """Bounded retained controller metadata; booleans are needed here only.

    Native request/group/target bytes use the unchanged canonical evidence
    reader. This metadata reader rejects duplicate keys, large numeric tokens,
    noninteger numbers and excessive nesting before metadata is inspected.
    """
    need(type(raw) is bytes and 0 < len(raw) <= MIB, "RETAINED_REQUEST_BYTES")
    stack, quoted, escaped = [], False, False
    for index, byte in enumerate(raw):
        if index % 4096 == 0:
            check()
        if quoted:
            need(byte >= 32, "RETAINED_REQUEST_STRING_CONTROL")
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (91, 123):
            stack.append(byte)
            need(len(stack) <= 64, "RETAINED_REQUEST_DEPTH")
        elif byte in (93, 125):
            need(stack and stack.pop() == (91 if byte == 93 else 123),
                 "RETAINED_REQUEST_BRACKETS")
    need(not quoted and not escaped and not stack, "RETAINED_REQUEST_UNTERMINATED")

    def integer(token):
        need(token.isascii() and token.isdecimal() and len(token) <= 20 and
             (len(token) == 1 or token[0] != "0") and
             (len(token) < 20 or token <= "18446744073709551615"),
             "RETAINED_REQUEST_INTEGER")
        return int(token)

    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "RETAINED_REQUEST_DUPLICATE_KEY")
            result[key] = value
        return result

    def reject(_):
        raise ValueError("RETAINED_REQUEST_NONINTEGER")

    check()
    try:
        result = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
            parse_int=integer, parse_float=reject, parse_constant=reject)
    except (UnicodeError, RecursionError, json.JSONDecodeError) as error:
        raise ValueError("RETAINED_REQUEST_JSON") from error
    check()
    return result


@dataclass(frozen=True)
class RetainedPreparation:
    status: str
    semantic_id: str
    foundation_id: str
    context_root: str
    bindings: tuple[tuple[bytes, str], ...]
    output_names: tuple[bytes, ...]
    request_sha256: str
    header_sha256: str
    group_sha256s: tuple[str, ...]
    targets_sha256: str
    input_bytes: int
    parent_lookups: int

    @property
    def mathematical_acceptance(self):
        return False


def reconstruct_preparation(request_raw, header_raw, group_raws, targets_raw, *,
                            semantic_id, foundation_id, context_root,
                            warranted_symbol, check_budget):
    """Recover exactly the selected retained map, not a fabricated new parent.

    REQUEST byte-hash authorization and fresh bounded file acquisition belong
    to the caller. All requested names/IDs are checked against the original
    selected protected parent. Metadata does not prove that a compiler ran or
    that its projected types/proofs are valid. Only names/IDs are recovered;
    no projected body or saved acceptance flag is adopted as mathematics.

    Fixed public limits match ordinary contribution: 32 groups/outputs, 4096
    bindings, 1 MiB/header or group, 4 MiB combined header/groups, 64 KiB targets.
    One required callback carries the original caller allowance; failures and
    cancellation propagate, and no fresh allowance/retry is created here.
    """
    need(callable(warranted_symbol) and callable(check_budget), "RETAINED_CALLBACKS")
    check = check_budget
    check()
    for identity in (semantic_id, foundation_id, context_root):
        E._hex(identity)
    need(semantic_id == S.semantic_id() and foundation_id == S.foundation_id(),
         "RETAINED_PORTABLE_SEMANTICS")
    need(type(group_raws) is tuple and len(group_raws) <= 32 and
         type(header_raw) is bytes and 0 < len(header_raw) <= MIB and
         all(type(raw) is bytes and 0 < len(raw) <= MIB for raw in group_raws) and
         type(targets_raw) is bytes and 0 < len(targets_raw) <= 65536,
         "RETAINED_INPUT_BOUNDS")
    payload_bytes = len(header_raw)+sum(map(len, group_raws))
    need(payload_bytes <= 4*MIB, "RETAINED_PAYLOAD_BOUND")
    request = _metadata_json(request_raw, check)
    need(type(request) is dict and set(request) in
         (REQUEST_FIELDS, REQUEST_FIELDS | {"project_authoring"}), "RETAINED_REQUEST_FIELDS")
    need(request["parent_root"] == context_root and
         request["mathematical_acceptance"] is False, "RETAINED_REQUEST_PARENT")
    need(type(request["groups"]) is int and request["groups"] == len(group_raws) and
         type(request["payload_bytes"]) is int and request["payload_bytes"] == payload_bytes,
         "RETAINED_REQUEST_CENSUS")
    pin_map = request["request_files"]
    filenames = ("header.json", *(f"group-{index:05d}.json" for index in range(len(group_raws))))
    need(type(pin_map) is dict and set(pin_map) == set(filenames), "RETAINED_EXACT_FILE_MAP")

    def pinned(raw, pin):
        check()
        need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
             type(pin["bytes"]) is int and pin["bytes"] == len(raw), "RETAINED_FILE_PIN")
        E._hex(pin["sha256"])
        digest = sha(raw)
        need(digest == pin["sha256"], "RETAINED_FILE_CHANGED")
        check()
        return digest

    header_hash = pinned(header_raw, pin_map["header.json"])
    group_hashes = tuple(pinned(raw, pin_map[filename]) for filename, raw in
                         zip(filenames[1:], group_raws, strict=True))
    target_hash = pinned(targets_raw, request["output_targets"])
    check()
    header = E.strict_json(header_raw, E.Limits(max_bytes=MIB))
    need(type(header) is dict, "RETAINED_HEADER_FIELDS")
    frontier_mode = header.get("schema") == R.FRONTIER_REQUEST_FORMAT
    need(set(header) == (FRONTIER_HEADER_FIELDS if frontier_mode else HEADER_FIELDS),
         "RETAINED_HEADER_FIELDS")
    need(header["schema"] == (R.FRONTIER_REQUEST_FORMAT if frontier_mode else R.REQUEST_FORMAT) and
         header["semantic_id"] == semantic_id and
         header["foundation_id"] == foundation_id and header["context_root"] == context_root,
         "RETAINED_HEADER_CONTEXT")
    if frontier_mode:
        E._hex(header["frontier_root"])
        project = request.get("project_authoring")
        need(type(project) is dict and project.get("frontier_root") == header["frontier_root"],
             "RETAINED_FRONTIER_ROOT_BINDING")
    need(type(header["group_count"]) is int and header["group_count"] == len(group_raws),
         "RETAINED_HEADER_GROUP_COUNT")
    bindings, lookups = {}, {}
    name_limits = E.Limits(max_name_bytes=65536)

    def lookup(name):
        check()
        key = E.name_key(name, name_limits)
        need(len(key) <= 65536, "RETAINED_CANONICAL_NAME_BYTES")
        if key not in lookups:
            need(len(lookups) < 4096+32, "RETAINED_LOOKUP_BOUND")
            value = warranted_symbol(name)
            need(value is None or type(value) is str, "RETAINED_LOOKUP_TYPE")
            lookups[key] = None if value is None else E._hex(value)
            check()
        return key, lookups[key]

    def binding(name, identity, *, basis=False):
        check()
        E._hex(identity)
        key, current = lookup(name)
        need(key not in bindings and len(bindings) < 4096, "RETAINED_DUPLICATE_OR_NAME_BOUND")
        need(current == identity, "RETAINED_UNWARRANTED_BINDING")
        if basis:
            need(identity == S.basis_symbol_id(semantic_id, foundation_id, name),
                 "RETAINED_BASIS_IDENTITY")
        bindings[key] = identity

    basis_rows = E._array(header["basis_rows"], 581)
    for selected in basis_rows:
        check()
        identity, row = E._array(selected, 2)
        E._array(row, 5)
        E._uint(row[1], 7)
        binding(row[0], identity, basis=True)
    if frontier_mode:
        previous_key = None
        for selected in E._array(header["frontier_labels"], maximum=4096):
            name, identity = E._array(selected, 2)
            key = E.name_key(name, name_limits)
            need(previous_key is None or previous_key < key, "RETAINED_FRONTIER_LABEL_ORDER")
            binding(name, identity)
            previous_key = key
    for raw in group_raws:
        check()
        marker, rows, units = E._array(E.strict_json(raw, E.Limits(max_bytes=MIB)), 3)
        need(marker == R.GROUP_FORMAT, "RETAINED_GROUP_FORMAT")
        E._array(rows, maximum=4096)
        need(bool(rows), "RETAINED_GROUP_EMPTY")
        E._array(units, maximum=1)
        for unit in units:
            need(E._array(unit, 3)[0] == E.UNIT_FORMAT, "RETAINED_GROUP_UNIT_FORMAT")
        for selected in rows:
            check()
            name, mode, identity, body = E._array(selected, 4)
            E._uint(mode, 1)
            E._array(body, 2 if mode == 0 else 5)
            if mode == 1:
                need(E.name_key(body[0], name_limits) == E.name_key(name, name_limits),
                     "RETAINED_GROUP_ROW_NAME")
            binding(name, identity)

    targets = E._array(header["targets"], maximum=32)
    need(bool(targets), "RETAINED_PREPARED_TARGETS_EMPTY")
    selected_keys = set()
    for selected in targets:
        check()
        name, identity = E._array(selected, 2)
        key = E.name_key(name, name_limits)
        E._hex(identity)
        need(key not in selected_keys and bindings.get(key) == identity,
             "RETAINED_PREPARED_TARGET_BINDING")
        selected_keys.add(key)
    check()
    names = E._array(E.strict_json(targets_raw, E.Limits(max_bytes=65536)), maximum=32)
    need(bool(names) and E.canonical_json(request["output_names"]) == targets_raw,
         "RETAINED_OUTPUT_TARGETS")
    output_names = []
    for name in names:
        check()
        key, identity = lookup(name)
        need(key not in output_names and identity is None, "RETAINED_OUTPUT_COLLISION")
        output_names.append(key)
    need(len(E.canonical_json([[E.strict_json(key), identity] for key, identity in bindings.items()])) <= MIB,
         "RETAINED_PREPARED_BYTES")
    result = RetainedPreparation("READY", semantic_id, foundation_id, context_root,
        tuple(bindings.items()), tuple(output_names), sha(request_raw), header_hash,
        group_hashes, target_hash, len(request_raw)+payload_bytes+len(targets_raw), len(lookups))
    check()
    return result
