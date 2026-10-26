"""Bounded advisory index contacts; no mathematical or connection authority.

Pure canonical parsing, immutable exact-key lookup and owner-selected egress.
No filesystem, clock, DNS, socket, referral following or source execution. A
reader must apply its own OwnerEgressPolicy and original monotonic contact lease
before every use. Registration metadata may be wrong, omitted or stale.

The egress predicate is adapted from portable_runtime/location/protocol.py;
there is deliberately no import of that DHT/controller/runtime closure.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import hashlib
import ipaddress
import json
import re
from types import MappingProxyType

from discovery import formal_features as F
from .http_provider import Endpoint

ROUTE = "/v5/ordinary/contacts"
MAP_SCHEMA = "DMKN_ORDINARY_CONTACT_MAP_V1"
REQUEST_SCHEMA = "DMKN_ORDINARY_CONTACT_REQUEST_V1"
REPLY_SCHEMA = "DMKN_ORDINARY_CONTACT_REPLY_V1"
STATUS = "ADVISORY_INDEX_CONTACTS"
ASSURANCE = "UNVERIFIED_SPECIALIST_REGISTRATION"
MAP_MAX, REPLY_MAX = 2*1024**2, 32768
MAX_KEYS, MAX_ENDPOINTS, MAX_CONTACTS = 2048, 16, 64
ENDPOINT_FIELDS = ("host", "port", "tls", "server_name")
REPLY_FIELDS = ("schema", "namespace", "features", "nonce", "status", "assurance",
                "contacts", "truncated", "global_complete", "mathematical_acceptance")


def _check(callback):
    F.need(callback is None or callable(callback), "CONTACT_BUDGET_CALLBACK")
    if callback is not None:
        callback()


def _ipv4(value):
    F.need(type(value) is str and 0 < len(value) <= 15, "CONTACT_NUMERIC_IPV4")
    try:
        address = ipaddress.IPv4Address(value)
    except ipaddress.AddressValueError as error:
        raise ValueError("CONTACT_NUMERIC_IPV4") from error
    F.need(str(address) == value, "CONTACT_CANONICAL_IPV4")
    return address


def _server_name(value):
    if value is None:
        return None
    F.need(type(value) is str and 1 <= len(value) <= 253 and value == value.lower(),
           "CONTACT_TLS_NAME")
    F.need(all(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
               for label in value.split(".")), "CONTACT_TLS_NAME")
    return value


def endpoint_spec(value):
    """Validate inert endpoint syntax only, NOT owner egress authorization."""
    F.fields(value, ENDPOINT_FIELDS)
    address = _ipv4(value["host"])
    port = F.uint(value["port"], 1, 65535, "CONTACT_PORT")
    F.need(type(value["tls"]) is bool, "CONTACT_TLS_BOOL")
    name = _server_name(value["server_name"])
    F.need(value["tls"] or name is None, "CONTACT_PLAINTEXT_HAS_NO_TLS_NAME")
    # This rejects nonsensical destinations, not all private addresses. Only
    # the independently adopted OwnerEgressPolicy may authorize a learned dial.
    Endpoint(str(address), port, value["tls"], name, None).validate()
    return {"host": str(address), "port": port, "tls": value["tls"], "server_name": name}


@dataclass(frozen=True, init=False, slots=True)
class OwnerEgressPolicy:
    """Immutable owner policy, never learned from a directory response."""
    _mode: str
    _ports: frozenset
    _tests: frozenset
    _config_bytes: bytes

    def __init__(self, config):
        F.fields(config, ("schema", "mode", "public_ports", "test_endpoints"))
        F.need(config["schema"] == "DMKN_V5_OWNER_EGRESS_V1" and
               config["mode"] in ("public-ipv4", "loopback-test"), "CONTACT_EGRESS_SCHEMA")
        ports, tests = config["public_ports"], config["test_endpoints"]
        F.need(type(ports) is list and len(ports) <= 16 and
               type(tests) is list and len(tests) <= 16, "CONTACT_EGRESS_ENTRIES")
        for port in ports:
            F.uint(port, 1, 65535, "CONTACT_PORT")
        F.need(ports == sorted(set(ports)), "CONTACT_CANONICAL_PORTS")
        pairs = []
        for item in tests:
            F.fields(item, ("host", "port"))
            F.need(str(_ipv4(item["host"])) == "127.0.0.1", "CONTACT_TEST_LOOPBACK_ONLY")
            pairs.append((item["host"], F.uint(item["port"], 1, 65535, "CONTACT_PORT")))
        F.need(pairs == sorted(set(pairs)), "CONTACT_CANONICAL_TEST_ENDPOINTS")
        F.need((config["mode"] == "public-ipv4" and ports and not pairs) or
               (config["mode"] == "loopback-test" and pairs and not ports), "CONTACT_EGRESS_MODE")
        object.__setattr__(self, "_mode", config["mode"])
        object.__setattr__(self, "_ports", frozenset(ports))
        object.__setattr__(self, "_tests", frozenset(pairs))
        object.__setattr__(self, "_config_bytes", F.compact(config))

    def endpoint(self, value):
        row = endpoint_spec(value)
        address, port = _ipv4(row["host"]), row["port"]
        if self._mode == "public-ipv4":
            F.need(address.is_global and not address.is_reserved and not address.is_multicast
                   and not address.is_loopback and not address.is_link_local and not address.is_unspecified,
                   "CONTACT_PUBLIC_ADDRESS_REQUIRED")
            F.need(port in self._ports and row["tls"] is True, "CONTACT_PUBLIC_TLS_PORT")
        else:
            F.need((str(address), port) in self._tests, "CONTACT_TEST_ENDPOINT_NOT_ALLOWED")
        return Endpoint(str(address), port, row["tls"], row["server_name"], None).validate()

    def report(self):
        return {"config": json.loads(self._config_bytes), "https_trust": "OWNER_SYSTEM_CA_ONLY",
                "ca_store_updates": "TRUSTED_OWNER_ENVIRONMENT_NOT_PINNED_ROOT_SET"}


def request_limit(request):
    F.fields(request, ("schema", "namespace", "features", "nonce", "max_contacts", "max_bytes"))
    F.need(request["schema"] == REQUEST_SCHEMA, "CONTACT_REQUEST_SCHEMA")
    F.hexid(request["namespace"]); F.validate_features(request["features"], 8)
    F.hexid(request["nonce"])
    F.uint(request["max_contacts"], 1, MAX_CONTACTS, "CONTACT_REQUEST_CONTACTS")
    return F.uint(request["max_bytes"], 1, REPLY_MAX, "CONTACT_REQUEST_BYTES")


def _envelope(request, contacts, truncated):
    return {"schema": REPLY_SCHEMA, "namespace": request["namespace"],
            "features": list(request["features"]), "nonce": request["nonce"],
            "status": STATUS, "assurance": ASSURANCE, "contacts": contacts,
            "truncated": truncated, "global_complete": False, "mathematical_acceptance": False}


@dataclass(frozen=True, init=False, slots=True)
class ContactMap:
    """A bounded immutable-byte map; exact route lookup, never a corpus scan."""
    namespace: str
    raw_sha256: str
    key_count: int
    contact_count: int
    _rows: object

    def __init__(self, raw, *, check_budget=None):
        _check(check_budget)
        document = F.strict(raw, MAP_MAX)
        F.fields(document, ("schema", "namespace", "entries"))
        F.need(document["schema"] == MAP_SCHEMA, "CONTACT_MAP_SCHEMA")
        namespace = F.hexid(document["namespace"])
        entries = document["entries"]
        F.need(type(entries) is list and len(entries) <= MAX_KEYS, "CONTACT_MAP_KEYS")
        rows, total = {}, 0
        for entry in entries:
            _check(check_budget)
            F.fields(entry, ("features", "endpoints"))
            key = tuple(F.validate_features(entry["features"], 8))
            F.need(key not in rows, "CONTACT_DUPLICATE_KEY")
            endpoints = entry["endpoints"]
            F.need(type(endpoints) is list and 1 <= len(endpoints) <= MAX_ENDPOINTS,
                   "CONTACT_MAP_ENDPOINTS")
            encoded, seen = [], set()
            for endpoint in endpoints:
                _check(check_budget)
                item = F.compact(endpoint_spec(endpoint))
                F.need(item not in seen, "CONTACT_DUPLICATE_ENDPOINT")
                seen.add(item); encoded.append(item)
            rows[key] = tuple(encoded); total += len(encoded)
        for name, value in (("namespace", namespace), ("raw_sha256", hashlib.sha256(raw).hexdigest()),
                            ("key_count", len(rows)), ("contact_count", total),
                            ("_rows", MappingProxyType(rows))):
            object.__setattr__(self, name, value)
        _check(check_budget)

    @classmethod
    def from_bytes(cls, raw, *, check_budget=None):
        F.need(cls is ContactMap, "CONTACT_MAP_TYPE")
        return cls(raw, check_budget=check_budget)

    def reply(self, request, *, check_budget=None):
        _check(check_budget)
        maximum = request_limit(request)
        # Bind even a different namespace's empty reply to the requested domain;
        # this is explicit advisory absence, never a claim about global coverage.
        rows = self._rows.get(tuple(request["features"]), ()) if request["namespace"] == self.namespace else ()
        retained = []
        raw = F.compact(_envelope(request, retained, bool(rows)))
        F.need(len(raw) <= maximum, "CONTACT_REPLY_MINIMUM")
        for row in rows[:request["max_contacts"]]:
            _check(check_budget)
            candidate = [*retained, json.loads(row)]
            encoded = F.compact(_envelope(request, candidate, len(candidate) < len(rows)))
            if len(encoded) > maximum:
                break
            retained, raw = candidate, encoded
        _check(check_budget)
        return raw


def reply(index, request, *, check_budget=None):
    F.need(type(index) is ContactMap, "CONTACT_MAP_TYPE")
    return index.reply(request, check_budget=check_budget)


def read_reply(raw, request):
    """Validate a bounded advisory claim, without authorizing any connection."""
    maximum = request_limit(request)
    result = F.strict(raw, maximum)
    F.fields(result, REPLY_FIELDS)
    F.need(result["schema"] == REPLY_SCHEMA and result["status"] == STATUS and
           result["assurance"] == ASSURANCE, "CONTACT_REPLY_SCHEMA")
    F.need(result["namespace"] == request["namespace"] and
           result["features"] == request["features"] and result["nonce"] == request["nonce"],
           "CONTACT_REPLY_BINDING")
    F.need(result["global_complete"] is False and result["mathematical_acceptance"] is False,
           "CONTACT_REPLY_ASSURANCE")
    F.need(type(result["truncated"]) is bool and type(result["contacts"]) is list and
           len(result["contacts"]) <= request["max_contacts"], "CONTACT_REPLY_CONTACTS")
    seen = set()
    for endpoint in result["contacts"]:
        encoded = F.compact(endpoint_spec(endpoint))
        F.need(encoded not in seen, "CONTACT_DUPLICATE_ENDPOINT")
        seen.add(encoded)
    return deepcopy(result)
