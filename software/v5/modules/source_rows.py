"""Producer-side Lean export decoding. This never establishes mathematical trust.

The exact local/foundation/external name partition is supplied explicitly. No
unknown symbol is silently promoted to the foundation, and no source namespace
is treated as an authentication credential. An independent relation must check
the resulting canonical descriptors and body commitments against native rows.
"""

from __future__ import annotations

from . import codec
from .model import ConditionalEnvironment


class SourceRows:
    def __init__(self, rows: list[dict], local_names: list[list],
                 foundation_names: list[list], external_names: list[dict] | None = None,
                 limits: codec.Limits = codec.DEFAULT_LIMITS):
        self.limits = limits
        codec.require(type(rows) is list and rows, "SOURCE_ROWS")
        codec.canonical(rows, limits)
        codec.require(type(rows[0]) is dict and set(rows[0]) == {"meta"}, "SOURCE_METADATA")
        self.names: list[list] = [[]]
        self.levels: list[dict] = [{"zero": None}]
        self.expressions: list[dict] = []
        self.declarations: list[dict] = []
        self.local = self._name_set(local_names)
        self.foundation = self._name_set(foundation_names)
        codec.require(not self.local & self.foundation, "SOURCE_NAME_ROLE_OVERLAP")
        self.external: dict[bytes, list] = {}
        for item in external_names or []:
            codec.fields(item, {"source_name", "module", "relative_name"})
            key = codec.name_key(item["source_name"], limits)
            codec.validate_name(item["relative_name"], limits)
            codec.digest_string(item["module"])
            codec.require(key not in self.local | self.foundation and key not in self.external,
                          "SOURCE_NAME_ROLE_OVERLAP")
            self.external[key] = ["external", item["module"], item["relative_name"]]
        self.work = 0
        self.bodies: dict[tuple[int, str], list] = {}
        self.proofs: dict[bytes, list] = {}
        for row in rows[1:]:
            codec.require(type(row) is dict, "SOURCE_ROW")
            domains = [tag for tag in ("in", "il", "ie") if tag in row]
            if not domains:
                codec.require(len(row) == 1, "SOURCE_DECLARATION_ROW")
                self.declarations.append(row)
                codec.require(len(self.declarations) <= limits.max_declarations,
                              "SOURCE_DECLARATION_LIMIT")
                continue
            codec.require(len(domains) == 1 and len(row) == 2, "SOURCE_DAG_ROW")
            domain = domains[0]
            index = codec.uint(row[domain], limits.max_nodes)
            item = {key: value for key, value in row.items() if key != domain}
            table = self.names if domain == "in" else self.levels if domain == "il" else self.expressions
            codec.require(index == len(table), "SOURCE_DAG_INDEX")
            if domain == "in":
                tag, value = next(iter(item.items()))
                codec.require(tag in ("str", "num"), "SOURCE_NAME_TAG")
                codec.fields(value, {"pre", "str"} if tag == "str" else {"pre", "i"})
                parent = self.name(value["pre"], allow_empty=True)
                name = parent + [["s", value["str"]] if tag == "str" else ["n", value["i"]]]
                codec.validate_name(name, limits)
                table.append(name)
            else:
                table.append(item)

    def _name_set(self, values: list[list]) -> set[bytes]:
        codec.require(type(values) is list and len(values) <= self.limits.max_declarations,
                      "SOURCE_NAME_CENSUS")
        keys = {codec.name_key(value, self.limits) for value in values}
        codec.require(len(keys) == len(values), "SOURCE_DUPLICATE_NAME")
        return keys

    def _visit(self, depth: int) -> None:
        # Count expansion, not merely input DAG nodes: a small shared DAG must
        # not materialize an exponentially larger expression tree unchecked.
        self.work += 1
        codec.require(depth <= self.limits.max_depth and self.work <= self.limits.max_nodes,
                      "SOURCE_EXPANSION_LIMIT")

    def name(self, index: int, allow_empty: bool = False) -> list:
        codec.uint(index)
        codec.require(index < len(self.names) and (allow_empty or index != 0), "SOURCE_NAME_INDEX")
        return self.names[index]

    def reference(self, index: int) -> list:
        name = self.name(index)
        key = codec.name_key(name, self.limits)
        if key in self.local:
            return ["local", name]
        if key in self.foundation:
            return ["foundation", name]
        codec.require(key in self.external, "SOURCE_UNMAPPED_REFERENCE")
        return self.external[key]

    def level(self, index: int, parameters: tuple[int, ...], depth: int) -> list:
        self._visit(depth)
        codec.uint(index)
        codec.require(index < len(self.levels), "SOURCE_LEVEL_INDEX")
        if index == 0:
            return ["zero"]
        tag, value = next(iter(self.levels[index].items()))
        if tag == "param":
            self.name(value)
            codec.require(value in parameters, "SOURCE_UNBOUND_LEVEL")
            return ["param", parameters.index(value)]
        if tag == "succ":
            codec.require(type(value) is int and value < index, "SOURCE_LEVEL_BACKREF")
            return [tag, self.level(value, parameters, depth + 1)]
        codec.require(tag in ("max", "imax") and type(value) is list and len(value) == 2,
                      "SOURCE_LEVEL_TAG")
        codec.require(all(type(x) is int and 0 <= x < index for x in value), "SOURCE_LEVEL_BACKREF")
        return [tag, *(self.level(x, parameters, depth + 1) for x in value)]

    def expression(self, index: int, parameters: tuple[int, ...], depth: int = 0) -> list:
        self._visit(depth)
        codec.uint(index)
        codec.require(index < len(self.expressions), "SOURCE_EXPRESSION_INDEX")
        tag, value = next(iter(self.expressions[index].items()))

        def sub(child: int) -> list:
            codec.require(type(child) is int and 0 <= child < index, "SOURCE_EXPR_BACKREF")
            return self.expression(child, parameters, depth + 1)

        if tag == "bvar":
            return ["bvar", codec.uint(value)]
        if tag == "sort":
            return ["sort", self.level(value, parameters, depth + 1)]
        if tag == "const":
            codec.fields(value, {"name", "us"})
            codec.require(type(value["us"]) is list and len(value["us"]) <= self.limits.max_universes,
                          "SOURCE_CONST_LEVELS")
            return ["const", self.reference(value["name"]),
                    [self.level(x, parameters, depth + 1) for x in value["us"]]]
        if tag == "app":
            codec.fields(value, {"fn", "arg"})
            return ["app", sub(value["fn"]), sub(value["arg"])]
        if tag in ("lam", "forallE"):
            codec.fields(value, {"name", "type", "body", "binderInfo"})
            self.name(value["name"], allow_empty=True)
            return ["lam" if tag == "lam" else "forall", value["binderInfo"],
                    sub(value["type"]), sub(value["body"])]
        if tag == "letE":
            codec.fields(value, {"name", "type", "value", "body", "nondep"})
            self.name(value["name"], allow_empty=True)
            codec.require(type(value["nondep"]) is bool, "SOURCE_NONDEP_FLAG")
            return ["let", sub(value["type"]), sub(value["value"]), sub(value["body"])]
        if tag == "proj":
            codec.fields(value, {"typeName", "idx", "struct"})
            return ["proj", self.reference(value["typeName"]), codec.uint(value["idx"]), sub(value["struct"])]
        if tag == "mdata":
            codec.fields(value, {"expr", "data"})
            return sub(value["expr"])
        # Literals need an explicitly specified native representation; do not
        # silently translate them via arbitrary numeral notation/instances.
        raise codec.StructureError("SOURCE_UNSUPPORTED_EXPRESSION:" + tag)

    def parameters(self, value: dict) -> tuple[int, ...]:
        params = value["levelParams"]
        codec.require(type(params) is list and len(params) <= self.limits.max_universes,
                      "SOURCE_UNIVERSE_PARAMETERS")
        for name in params:
            self.name(name)
        codec.require(len(set(params)) == len(params), "SOURCE_DUPLICATE_UNIVERSE")
        return tuple(params)

    def body(self, index: int, params: tuple[int, ...]) -> tuple[str, list]:
        expression = self.expression(index, params)
        digest = codec.body_id(expression, len(params), self.limits)
        self.bodies[len(params), digest] = expression
        return digest, expression

    def declaration(self, tag: str, value: dict) -> dict:
        required = {"name", "levelParams", "type"}
        extra = {"definition": {"value", "hints", "safety"},
                 "opaque": {"value", "isUnsafe"}, "theorem": {"value"},
                 "inductive": {"all", "ctors", "numParams", "numIndices", "numNested",
                               "isRec", "isReflexive", "isUnsafe"},
                 "constructor": {"induct", "cidx", "numParams", "numFields", "isUnsafe"},
                 "recursor": {"all", "numParams", "numIndices", "numMotives", "numMinors",
                              "rules", "k", "isUnsafe"}}[tag]
        optional = {"all"} if tag in ("definition", "opaque", "theorem") else set()
        codec.require(type(value) is dict and required | extra <= set(value)
                      and set(value) <= required | extra | optional, "SOURCE_DECLARATION_FIELDS")
        if "all" in optional and "all" in value:
            codec.require(type(value["all"]) is list, "SOURCE_ALL_NAMES")
            for item in value["all"]:
                self.name(item)
        params = self.parameters(value)
        name = self.name(value["name"])
        codec.require(codec.name_key(name, self.limits) in self.local, "SOURCE_NONLOCAL_DECLARATION")
        result = {"name": name, "kind": tag, "universes": len(params),
                  "type": self.expression(value["type"], params), "value_hash": None, "meta": {}}
        if tag in ("definition", "opaque", "theorem"):
            digest, expression = self.body(value["value"], params)
            if tag == "theorem":
                self.proofs[codec.name_key(name, self.limits)] = expression
            else:
                result["value_hash"] = digest
                result["meta"] = {"safety": "safe"}
                if tag == "definition":
                    codec.require(value["safety"] == "safe", "SOURCE_UNSAFE_DEFINITION")
                    result["meta"]["hint"] = value["hints"]
                else:
                    codec.require(value["isUnsafe"] is False, "SOURCE_UNSAFE_OPAQUE")
            return result
        codec.require(value["isUnsafe"] is False, "SOURCE_UNSAFE_INDUCTIVE")
        if tag == "inductive":
            result["meta"] = {"all": [self.name(n) for n in value["all"]],
                              "constructors": [self.name(n) for n in value["ctors"]],
                              "num_params": value["numParams"], "num_indices": value["numIndices"],
                              "num_nested": value["numNested"], "is_recursive": value["isRec"],
                              "is_reflexive": value["isReflexive"]}
        elif tag == "constructor":
            result["meta"] = {"inductive": self.name(value["induct"]),
                              "constructor_index": value["cidx"], "num_params": value["numParams"],
                              "num_fields": value["numFields"]}
        else:
            codec.require(tag == "recursor", "SOURCE_DECLARATION_KIND")
            codec.require(type(value["rules"]) is list
                          and len(value["rules"]) <= self.limits.max_declarations,
                          "SOURCE_RECURSOR_RULES")
            for rule in value["rules"]:
                codec.fields(rule, {"ctor", "nfields", "rhs"})
            result["meta"] = {"all": [self.name(n) for n in value["all"]],
                              "num_params": value["numParams"], "num_indices": value["numIndices"],
                              "num_motives": value["numMotives"], "num_minors": value["numMinors"],
                              "is_k": value["k"], "rules": [
                                  {"constructor": self.name(rule["ctor"]), "num_fields": rule["nfields"],
                                   "value_hash": self.body(rule["rhs"], params)[0]} for rule in value["rules"]]}
        return result

    def module(self, foundation: str, policy: str) -> ConditionalEnvironment:
        groups, seen = [], set()
        for row in self.declarations:
            tag, value = next(iter(row.items()))
            if tag == "inductive":
                codec.fields(value, {"types", "ctors", "recs"})
                records = [(kind, item) for source, kind in (("types", "inductive"),
                           ("ctors", "constructor"), ("recs", "recursor")) for item in value[source]]
            else:
                codec.require(tag in ("def", "thm", "opaque", "axiom", "quot"), "SOURCE_DECLARATION_TAG")
                records = [({"def": "definition", "thm": "theorem"}.get(tag, tag), value)]
            names = [codec.name_key(self.name(item["name"]), self.limits) for _, item in records]
            selected = [name in self.local for name in names]
            if not any(selected):
                codec.require(all(name in self.foundation or name in self.external for name in names),
                              "SOURCE_UNCLASSIFIED_DECLARATION")
                continue
            codec.require(all(selected), "SOURCE_PARTIAL_LOCAL_GROUP")
            codec.require(not seen.intersection(names) and len(set(names)) == len(names),
                          "SOURCE_DUPLICATE_DECLARATION")
            codec.require(all(kind not in ("axiom", "quot") for kind, _ in records), "SOURCE_LOCAL_AXIOM")
            seen.update(names)
            group = {"kind": "inductive" if tag == "inductive" else "ordinary",
                     "declarations": [self.declaration(kind, item) for kind, item in records]}
            codec.validate_group(group, self.limits)
            groups.append(group)
        codec.require(seen == self.local, "SOURCE_LOCAL_CENSUS_MISMATCH")
        environment = ConditionalEnvironment({"schema": codec.SPEC_SCHEMA, "foundation": foundation,
                                             "policy": policy, "groups": groups}, self.limits)
        for (universes, _), expression in self.bodies.items():
            environment.supply_body(expression, universes)
        for name, expression in self.proofs.items():
            environment.supply_local_value(codec.parse_json(name, self.limits), expression)
        return environment


def decode_source(rows: list[dict], local_names: list[list], foundation_names: list[list],
                  foundation: str, policy: str, external_names: list[dict] | None = None,
                  limits: codec.Limits = codec.DEFAULT_LIMITS) -> ConditionalEnvironment:
    return SourceRows(rows, local_names, foundation_names, external_names, limits).module(foundation, policy)
