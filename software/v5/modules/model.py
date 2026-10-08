"""Conditional role/merge/demand bookkeeping. NEVER verifies mathematics.

An ImportClaim is deliberately not called VerifiedImport: hash openings and
serialized claims cannot grant certificate authority. The native/guest adapter
must authenticate every claim before it may skip imported checking.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from . import codec

STATUS = "CONDITIONAL_STRUCTURE_ONLY_NO_MATHEMATICAL_ADMISSION"


@dataclass(frozen=True)
class Address:
    module: str
    name_bytes: bytes

    @classmethod
    def of(cls, module: str, name: list) -> "Address":
        codec.digest_string(module)
        return cls(module, codec.name_key(name))

    @property
    def name(self) -> list:
        return codec.parse_json(self.name_bytes)


@dataclass(frozen=True)
class ImportClaim:
    """Unverified exact certificate premise, requiring separate real verification."""

    module: str
    foundation: str
    policy: str
    group_root: str
    group_count: int
    rank: int
    journal_hash: str
    receipt_hash: str

    def summary(self) -> dict:
        return {"schema": codec.SUMMARY_SCHEMA, "foundation": self.foundation,
                "policy": self.policy, "group_count": self.group_count, "group_root": self.group_root}

    def validate(self, limits: codec.Limits) -> None:
        codec.require(codec.summary_id(self.summary(), limits) == self.module, "CLAIM_MODULE_BINDING")
        codec.uint(self.rank, 2**64 - 1)
        codec.digest_string(self.journal_hash)
        codec.digest_string(self.receipt_hash)


@dataclass(frozen=True)
class Need:
    kind: str
    address: Address
    body_hash: str | None = None


class DemandRequired(Exception):
    def __init__(self, demand: Need):
        self.demand = demand
        super().__init__(demand.kind)


class NotVisible(codec.StructureError):
    pass


@dataclass(frozen=True)
class ConditionalDeclaration:
    address: Address
    group_index: int
    role: str
    descriptor_bytes: bytes

    @property
    def descriptor(self) -> dict:
        return codec.parse_json(self.descriptor_bytes)


class ConditionalEnvironment:
    """Pure monotone witness model; returned roles are NOT authentication tokens."""

    status = STATUS

    def __init__(self, local_spec: dict, limits: codec.Limits = codec.DEFAULT_LIMITS):
        codec.validate_spec(local_spec, limits)
        self.limits = limits
        self.spec = codec.parse_json(codec.canonical(local_spec, limits), limits)
        self.module = codec.module_id(self.spec, limits)
        self.claims: dict[str, ImportClaim] = {}
        self.groups: dict[tuple[str, int], bytes] = {}
        self.declarations: dict[Address, ConditionalDeclaration] = {}
        self.bodies: dict[tuple[int, str], bytes] = {}
        self.local_proofs: dict[Address, str] = {}
        self._header_bytes = len(codec.canonical(self.spec, limits))
        self._body_bytes = 0
        for index, group in enumerate(self.spec["groups"]):
            self._insert_group(self.module, index, group, "LOCAL_MUST_CHECK")

    def _insert_group(self, module: str, index: int, group: dict, role: str) -> None:
        encoded = codec.canonical(group, self.limits)
        key = module, index
        if key in self.groups:
            codec.require(self.groups[key] == encoded, "GROUP_MUTATION")
            return
        codec.require(len(self.groups) < self.limits.max_groups, "WITNESS_GROUP_LIMIT")
        pending: list[ConditionalDeclaration] = []
        for descriptor in group["declarations"]:
            address = Address.of(module, descriptor["name"])
            codec.require(address not in self.declarations, "DECLARATION_REDEFINITION_OR_ROLE_CHANGE")
            pending.append(ConditionalDeclaration(address, index, role,
                           codec.canonical(descriptor, self.limits)))
        codec.require(len(self.declarations) + len(pending) <= self.limits.max_declarations,
                      "WITNESS_DECLARATION_LIMIT")
        added_bytes = len(encoded) + sum(len(item.descriptor_bytes) for item in pending)
        codec.require(self._header_bytes + self._body_bytes + added_bytes <= self.limits.max_bytes,
                      "WITNESS_TOTAL_CANONICAL_BYTE_LIMIT")
        # No partial mutation on a failing census.
        self.groups[key] = encoded
        for declaration in pending:
            self.declarations[declaration.address] = declaration
        self._header_bytes += added_bytes

    def add_claim(self, claim: ImportClaim) -> None:
        codec.require(type(claim) is ImportClaim, "CLAIM_TYPE")
        claim.validate(self.limits)
        codec.require(claim.module != self.module, "IMPORT_CURRENT_LOCAL_MODULE")
        codec.require(claim.foundation == self.spec["foundation"] and claim.policy == self.spec["policy"],
                      "IMPORT_FOUNDATION_POLICY")
        previous = self.claims.get(claim.module)
        codec.require(previous is None or previous == claim, "CLAIM_MUTATION")
        codec.require(previous is not None or len(self.claims) < self.limits.max_groups,
                      "WITNESS_CLAIM_LIMIT")
        added_bytes = 0 if previous is not None else len(codec.canonical(asdict(claim), self.limits))
        codec.require(self._header_bytes + self._body_bytes + added_bytes <= self.limits.max_bytes,
                      "WITNESS_TOTAL_CANONICAL_BYTE_LIMIT")
        self.claims[claim.module] = claim
        self._header_bytes += added_bytes

    def add_import_opening(self, module: str, opening: dict) -> None:
        codec.require(module in self.claims, "MISSING_UNVERIFIED_IMPORT_PREMISE")
        claim = self.claims[module]
        group = codec.verify_group_opening(module, opening, self.limits)
        codec.require(opening["summary"] == claim.summary(), "OPENING_CLAIM_BINDING")
        self._insert_group(module, opening["index"], group,
                           "IMPORTED_ONLY_IF_REAL_CERTIFICATE_PREMISE_IS_DISCHARGED")

    def supply_body(self, expression: Any, universes: int) -> str:
        identifier = codec.body_id(expression, universes, self.limits)
        encoded = codec.canonical(expression, self.limits)
        key = universes, identifier
        previous = self.bodies.get(key)
        codec.require(previous is None or previous == encoded, "BODY_MUTATION")
        # Aggregate witness storage, not only per-body bounds.
        added_bytes = 0 if previous is not None else len(encoded)
        codec.require(self._header_bytes + self._body_bytes + added_bytes
                      <= self.limits.max_bytes, "WITNESS_TOTAL_CANONICAL_BYTE_LIMIT")
        self.bodies[key] = encoded
        self._body_bytes += added_bytes
        return identifier

    def supply_local_value(self, name: list, expression: Any) -> str:
        address = Address.of(self.module, name)
        codec.require(address in self.declarations, "LOCAL_VALUE_UNKNOWN_DECLARATION")
        declaration = self.declarations[address].descriptor
        codec.require(declaration["kind"] in ("theorem", "definition", "opaque"), "LOCAL_VALUE_KIND")
        identifier = codec.body_id(expression, declaration["universes"], self.limits)
        if declaration["kind"] != "theorem":
            codec.require(identifier == declaration["value_hash"], "LOCAL_VALUE_COMMITMENT")
        else:
            previous = self.local_proofs.get(address)
            codec.require(previous is None or previous == identifier, "LOCAL_PROOF_MUTATION")
        self.supply_body(expression, declaration["universes"])
        if declaration["kind"] == "theorem":
            self.local_proofs[address] = identifier
        return identifier

    def lookup(self, address: Address, local_cutoff: int,
               checking_inductive_group: int | None = None) -> ConditionalDeclaration:
        codec.uint(local_cutoff, len(self.spec["groups"]))
        if checking_inductive_group is not None:
            codec.require(checking_inductive_group == local_cutoff
                          and local_cutoff < len(self.spec["groups"])
                          and self.spec["groups"][local_cutoff]["kind"] == "inductive",
                          "MUTUAL_VISIBILITY_SCOPE")
        if address.module == self.module:
            codec.require(address in self.declarations, "UNDECLARED_LOCAL_REFERENCE")
            result = self.declarations[address]
            if result.group_index >= local_cutoff and result.group_index != checking_inductive_group:
                raise NotVisible("LOCAL_SELF_OR_FORWARD_REFERENCE")
            return result
        # Imported contexts are not subject to the consumer's insertion order.
        # They still require exact certificate discharge outside this pure model.
        if address not in self.declarations:
            raise DemandRequired(Need("NeedDeclaration", address))
        return self.declarations[address]

    def demand_definition_body(self, address: Address, local_cutoff: int,
                               checking_inductive_group: int | None = None) -> Any:
        declaration = self.lookup(address, local_cutoff, checking_inductive_group).descriptor
        codec.require(declaration["kind"] == "definition", "DELTA_REQUIRES_DEFINITION_KIND")
        key = declaration["universes"], declaration["value_hash"]
        if key not in self.bodies:
            raise DemandRequired(Need("NeedBody", address, declaration["value_hash"]))
        return codec.parse_json(self.bodies[key], self.limits)

    def new_local_obligations(self) -> list[dict]:
        """Every local group needs native checking, regardless of available imports."""
        obligations = []
        for index, group in enumerate(self.spec["groups"]):
            for declaration in group["declarations"]:
                address = Address.of(self.module, declaration["name"])
                kind = declaration["kind"]
                if kind in ("definition", "opaque", "theorem"):
                    identifier = (self.local_proofs.get(address) if kind == "theorem"
                                  else declaration["value_hash"])
                    codec.require(identifier is not None and (declaration["universes"], identifier)
                                  in self.bodies, "NEW_LOCAL_VALUE_MUST_BE_PRESENT")
                elif kind == "recursor":
                    for rule in declaration["meta"]["rules"]:
                        codec.require((declaration["universes"], rule["value_hash"]) in self.bodies,
                                      "NEW_LOCAL_RECURSOR_RULE_MUST_BE_PRESENT")
            obligations.append({"group_index": index, "kind": group["kind"],
                                "role": "LOCAL_MUST_CHECK", "mathematical_admission": False})
        return obligations

    def conditional_premises(self) -> dict:
        """Report unresolved external premises, never serialized acceptance flags."""
        ranks = [claim.rank for claim in self.claims.values()]
        rank = 0 if not ranks else max(ranks) + 1
        codec.uint(rank, 2**64 - 1)
        return {"status": STATUS, "module": self.module, "suggested_rank": rank,
                "mathematical_admission": False, "certificate_verification": "NOT_PERFORMED",
                "parent_receipts": [{"module": claim.module, "journal_hash": claim.journal_hash,
                                     "receipt_hash": claim.receipt_hash, "rank": claim.rank}
                                    for _, claim in sorted(self.claims.items())]}
