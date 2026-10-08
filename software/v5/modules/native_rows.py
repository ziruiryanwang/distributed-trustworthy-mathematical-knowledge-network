"""Deterministic codec -> native-row bridge, not a mathematical trust boundary.

The caller supplies exact adopted foundation rows; this builder neither adopts
their hash nor verifies module receipts. A Rust relation must independently bind
these rows back to the canonical descriptor openings before certified use.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from . import codec
from .model import Address, ConditionalEnvironment, DemandRequired, Need


class NativeRows:
    def __init__(self, foundation_rows: list[dict], limits: codec.Limits = codec.DEFAULT_LIMITS):
        codec.require(type(foundation_rows) is list and foundation_rows
                      and type(foundation_rows[0]) is dict and set(foundation_rows[0]) == {"meta"},
                      "FOUNDATION_NATIVE_METADATA")
        self.limits = limits
        # Relative names retain the protocol's original bound; native absolute
        # names gain exactly the three fixed module-prefix components.
        self.absolute_name_limits = replace(limits, max_name_parts=limits.max_name_parts + 3)
        encoded = codec.canonical(foundation_rows, limits)
        self.rows = codec.parse_json(encoded, limits)
        self.canonical_bytes = len(encoded)
        self.tables: dict[str, dict[bytes, int]] = {"in": {}, "il": {}, "ie": {}}
        self.next_index = {"in": 1, "il": 1, "ie": 0}
        self.names: dict[bytes, int] = {b"[]": 0}
        name_values: list[list] = [[]]
        for row in self.rows[1:]:
            index_fields = [key for key in self.tables if key in row]
            if not index_fields:
                codec.require(len(row) == 1, "FOUNDATION_DECLARATION_ROW")
                continue
            codec.require(len(index_fields) == 1 and len(row) == 2, "FOUNDATION_DAG_ROW")
            domain = index_fields[0]
            index = codec.uint(row[domain])
            codec.require(index == self.next_index[domain], "FOUNDATION_DAG_INDEX")
            item = {key: value for key, value in row.items() if key != domain}
            key = codec.canonical(item, limits)
            codec.require(key not in self.tables[domain], "DUPLICATE_FOUNDATION_DAG_NODE")
            self.tables[domain][key] = index
            self.next_index[domain] += 1
            if domain == "in":
                tag, value = next(iter(item.items()))
                codec.require(tag in ("str", "num") and type(value) is dict, "FOUNDATION_NAME_ROW")
                pre = codec.uint(value["pre"])
                codec.require(pre < len(name_values), "FOUNDATION_NAME_PREFIX")
                suffix = ["s", value["str"]] if tag == "str" else ["n", value["i"]]
                name = name_values[pre] + [suffix]
                codec.validate_name(name, limits)
                name_values.append(name)
                self.names[codec.canonical(name, limits)] = index

    def _append(self, row: dict) -> None:
        # Exact JSON array cost: its existing closing bracket is displaced by
        # one comma and one canonical row. Do not serialize the growing array
        # on every append (quadratic in total export length).
        size = len(codec.canonical(row, self.limits)) + (1 if self.rows else 0)
        codec.require(self.canonical_bytes + size <= self.limits.max_bytes,
                      "CANONICAL_BYTE_LIMIT")
        self.rows.append(row)
        self.canonical_bytes += size

    def intern(self, domain: str, item: dict) -> int:
        key = codec.canonical(item, self.limits)
        if key in self.tables[domain]:
            return self.tables[domain][key]
        index = self.next_index[domain]
        codec.require(index < self.limits.max_nodes, "NATIVE_DAG_NODE_LIMIT")
        self._append({domain: index, **item})
        self.tables[domain][key] = index
        self.next_index[domain] += 1
        return index

    def name(self, parts: list) -> int:
        if not parts:
            return 0
        codec.validate_name(parts, self.absolute_name_limits)
        key = codec.canonical(parts, self.limits)
        if key in self.names:
            return self.names[key]
        parent = self.name(parts[:-1])
        kind, value = parts[-1]
        item = {"str": {"pre": parent, "str": value}} if kind == "s" else {
            "num": {"pre": parent, "i": value}}
        index = self.intern("in", item)
        self.names[key] = index
        return index

    def relative_name(self, owner: str, name: list) -> int:
        return self.name(codec.relocated_name(owner, name, self.limits))

    def ref(self, owner: str, reference: list) -> int:
        if reference[0] == "foundation":
            return self.name(reference[1])
        if reference[0] == "local":
            return self.relative_name(owner, reference[1])
        codec.require(reference[0] == "external", "REFERENCE_TAG")
        return self.relative_name(reference[1], reference[2])

    def universe_name(self, index: int) -> int:
        return self.name([["s", "DMKN"], ["s", "Universe"], ["n", index]])

    def level(self, value: list) -> int:
        tag = value[0]
        if tag == "zero":
            return 0
        if tag == "param":
            return self.intern("il", {"param": self.universe_name(value[1])})
        if tag == "succ":
            return self.intern("il", {"succ": self.level(value[1])})
        codec.require(tag in ("max", "imax"), "LEVEL_TAG")
        return self.intern("il", {tag: [self.level(value[1]), self.level(value[2])]})

    def expression(self, owner: str, expression: list) -> int:
        tag = expression[0]
        if tag == "bvar":
            row = {"bvar": expression[1]}
        elif tag == "sort":
            row = {"sort": self.level(expression[1])}
        elif tag == "const":
            row = {"const": {"name": self.ref(owner, expression[1]),
                             "us": [self.level(x) for x in expression[2]]}}
        elif tag == "app":
            row = {"app": {"fn": self.expression(owner, expression[1]),
                           "arg": self.expression(owner, expression[2])}}
        elif tag in ("lam", "forall"):
            row = {"lam" if tag == "lam" else "forallE": {
                "name": 0, "type": self.expression(owner, expression[2]),
                "body": self.expression(owner, expression[3]), "binderInfo": expression[1]}}
        elif tag == "let":
            row = {"letE": {"name": 0, "type": self.expression(owner, expression[1]),
                            "value": self.expression(owner, expression[2]),
                            "body": self.expression(owner, expression[3]), "nondep": False}}
        elif tag == "proj":
            row = {"proj": {"typeName": self.ref(owner, expression[1]), "idx": expression[2],
                            "struct": self.expression(owner, expression[3])}}
        else:
            raise codec.StructureError("NATIVE_EXPRESSION_TAG")
        return self.intern("ie", row)

    def header(self, owner: str, declaration: dict) -> dict:
        universes = [self.universe_name(i) for i in range(declaration["universes"])]
        # The predecessor parser requires each parameter level to already exist.
        for index in range(declaration["universes"]):
            self.level(["param", index])
        return {"name": self.relative_name(owner, declaration["name"]),
                "levelParams": universes, "type": self.expression(owner, declaration["type"])}

    def _body(self, environment: ConditionalEnvironment, owner: str,
              declaration: dict, identifier: str) -> int:
        key = declaration["universes"], identifier
        if key not in environment.bodies:
            raise DemandRequired(Need("NeedBody", Address.of(owner, declaration["name"]), identifier))
        expression = codec.parse_json(environment.bodies[key], self.limits)
        codec.require(codec.body_id(expression, declaration["universes"], self.limits) == identifier,
                      "STORED_BODY_COMMITMENT")
        # Owner, not consumer: the same relative body bytes in two modules do not
        # denote the same absolute constants merely because they share a hash.
        return self.expression(owner, expression)

    def group(self, environment: ConditionalEnvironment, owner: str, group: dict,
              imported: bool) -> list[int]:
        codec.validate_group(group, self.limits)
        names = []
        if group["kind"] == "ordinary":
            declaration = group["declarations"][0]
            header = self.header(owner, declaration)
            names.append(header["name"])
            kind, commitment = declaration["kind"], declaration["value_hash"]
            present = (declaration["universes"], commitment) in environment.bodies
            if imported and kind == "theorem":
                self._append({"moduleImportTheorem": header})
            elif imported and not present:
                codec.require(kind in ("definition", "opaque"), "MISSING_IMPORTED_KIND")
                header["bodyHash"] = list(bytes.fromhex(commitment))
                if kind == "definition":
                    header["hints"] = declaration["meta"]["hint"]
                self._append({"moduleImportDef" if kind == "definition" else "moduleImportOpaque": header})
            else:
                if kind == "theorem":
                    commitment = environment.local_proofs.get(Address.of(owner, declaration["name"]))
                    codec.require(commitment is not None, "LOCAL_PROOF_MISSING")
                header["value"] = self._body(environment, owner, declaration, commitment)
                header["all"] = [header["name"]]
                if kind == "definition":
                    header.update(hints=declaration["meta"]["hint"], safety="safe")
                    self._append({"def": header})
                elif kind == "opaque":
                    header["isUnsafe"] = False
                    self._append({"opaque": header})
                else:
                    self._append({"thm": header})
            return names

        parts: dict[str, list] = {"types": [], "ctors": [], "recs": []}
        for declaration in group["declarations"]:
            header = self.header(owner, declaration)
            names.append(header["name"])
            meta, kind = declaration["meta"], declaration["kind"]
            header["isUnsafe"] = False
            if kind == "inductive":
                header.update(all=[self.relative_name(owner, n) for n in meta["all"]],
                              ctors=[self.relative_name(owner, n) for n in meta["constructors"]],
                              numParams=meta["num_params"], numIndices=meta["num_indices"],
                              numNested=meta["num_nested"], isRec=meta["is_recursive"],
                              isReflexive=meta["is_reflexive"])
                parts["types"].append(header)
            elif kind == "constructor":
                header.update(induct=self.relative_name(owner, meta["inductive"]),
                              cidx=meta["constructor_index"], numParams=meta["num_params"],
                              numFields=meta["num_fields"])
                parts["ctors"].append(header)
            else:
                header.update(all=[self.relative_name(owner, n) for n in meta["all"]],
                              numParams=meta["num_params"], numIndices=meta["num_indices"],
                              numMotives=meta["num_motives"], numMinors=meta["num_minors"], k=meta["is_k"],
                              rules=[{"ctor": self.relative_name(owner, rule["constructor"]),
                                      "nfields": rule["num_fields"],
                                      "rhs": self._body(environment, owner, declaration, rule["value_hash"])}
                                     for rule in meta["rules"]])
                parts["recs"].append(header)
        self._append({"inductive": parts})
        return names


def emit_conditional(environment: ConditionalEnvironment, foundation_rows: list[dict]) -> dict:
    """Build diagnostic input with unresolved exact foundation/module premises."""
    emitter = NativeRows(foundation_rows, environment.limits)
    premises = []
    for (owner, index), encoded in sorted(environment.groups.items()):
        if owner == environment.module:
            continue
        group = codec.parse_json(encoded, environment.limits)
        names = emitter.group(environment, owner, group, imported=True)
        claim = environment.claims[owner]
        premises.append({"module": owner, "group_index": index, "native_name_indices": names,
                         "descriptor_hash": codec.hash_value("group-descriptor", group, environment.limits),
                         "journal_hash": claim.journal_hash, "receipt_hash": claim.receipt_hash})
    for group in environment.spec["groups"]:
        emitter.group(environment, environment.module, group, imported=False)
    rows = codec.parse_json(codec.canonical(emitter.rows, environment.limits), environment.limits)
    return {"status": environment.status, "module": environment.module,
            "foundation": environment.spec["foundation"], "rows": rows,
            "unverified_module_premises": premises,
            "foundation_binding": "CALLER_MUST_AUTHENTICATE_EXACT_SEED_ROWS",
            "mathematical_admission": False, "certificate_verification": "NOT_PERFORMED"}
