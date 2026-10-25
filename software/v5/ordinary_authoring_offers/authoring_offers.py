"""Bounded advisory project associations, never mathematics or execution authority.

Pure parsing/indexing/selection only: no filesystem, DNS, HTTP, Git, Lean,
dependency resolution or owner state. Providers may lie or omit valid projects.
An accepted reply binds only a finite unverified claim to the requested key.
"""
from __future__ import annotations

import hashlib
import ipaddress
import json
import re
from types import MappingProxyType
from urllib.parse import urlsplit

import ordinary_evidence as E
from discovery import formal_features as F

ROUTE = "/v5/ordinary/authoring-offers"
MAP_SCHEMA = "DMKN_AUTHORING_OFFER_MAP_V1"
REQUEST_SCHEMA = "DMKN_AUTHORING_OFFERS_REQUEST_V1"
REPLY_SCHEMA = "DMKN_AUTHORING_OFFERS_REPLY_V1"
STATUS = "UNVERIFIED_AUTHORING_ASSOCIATIONS"
MAP_MAX, REPLY_MAX, OFFER_MAX = 2*1024**2, 32768, 8192
MAX_KEYS, MAX_OFFERS = 2048, 8
NAME_LIMITS = E.Limits(max_name_parts=64, max_name_bytes=1024)
OFFER_FIELDS = ("repository", "object_format", "commit", "project_dir",
                "module", "export_name", "toolchain")
REPLY_FIELDS = ("schema", "semantic_id", "export_id", "status", "offers",
                "truncated", "mathematical_acceptance", "source_availability",
                "correspondence", "execution_approved", "global_complete")
_RESERVED = frozenset(("CON", "PRN", "AUX", "NUL", "CLOCK$", "CONIN$", "CONOUT$",
    *(prefix+digit for prefix in ("COM", "LPT") for digit in "123456789\u00b9\u00b2\u00b3")))


def _check(callback):
    F.need(callback is None or callable(callback), "AUTHORING_BUDGET_CALLBACK")
    if callback is not None:
        callback()


def _text(value, maximum, code, *, empty=False):
    F.need(type(value) is str, code)
    try:
        size = len(value.encode("utf-8"))
    except UnicodeError as error:
        raise ValueError(code) from error
    F.need((0 if empty else 1) <= size <= maximum and
           all(ord(c) >= 32 and ord(c) != 127 for c in value), code)
    return value


def _repository(value):
    _text(value, 2048, "AUTHORING_REPOSITORY")
    F.need(value.startswith("https://") and all(32 < ord(c) < 127 for c in value)
           and not any(c in value for c in "\\?#"), "AUTHORING_REPOSITORY")
    try:
        parsed = urlsplit(value)
        host, port = parsed.hostname, parsed.port
        F.need(parsed.scheme == "https" and parsed.netloc and host and
               parsed.username is None and parsed.password is None and
               not parsed.query and not parsed.fragment and
               not any(c in parsed.netloc for c in "%@"), "AUTHORING_REPOSITORY")
        F.need(port is None or 1 <= port <= 65535, "AUTHORING_REPOSITORY")
        if ":" in host:
            ipaddress.IPv6Address(host)  # Syntax only; no lookup or connection.
            F.need("%" not in host, "AUTHORING_REPOSITORY")
        else:
            F.need(len(host) <= 253 and all(re.fullmatch(
                r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label)
                for label in host.split(".")), "AUTHORING_REPOSITORY")
        F.need(re.search(r"%(?![0-9A-Fa-f]{2})", parsed.path) is None,
               "AUTHORING_REPOSITORY")
        # Encoded controls are not useful repository locators in this profile.
        F.need(all(int(pair, 16) >= 32 and int(pair, 16) != 127
                   for pair in re.findall(r"%([0-9A-Fa-f]{2})", parsed.path)),
               "AUTHORING_REPOSITORY")
    except (ValueError, UnicodeError) as error:
        raise ValueError("AUTHORING_REPOSITORY") from error


def _directory(value):
    _text(value, 1024, "AUTHORING_PROJECT_DIRECTORY", empty=True)
    if value == "":  # The repository root, not an absolute filesystem root.
        return
    F.need(not value.startswith("/") and not value.endswith("/") and
           not any(c in value for c in '\\:*?"<>|'), "AUTHORING_PROJECT_DIRECTORY")
    for part in value.split("/"):
        F.need(part not in ("", ".", "..") and not part.endswith((".", " ")) and
               part.split(".", 1)[0].upper() not in _RESERVED,
               "AUTHORING_PROJECT_DIRECTORY")


def _offer_bytes(offer):
    F.fields(offer, OFFER_FIELDS)
    _repository(offer["repository"])
    F.need(offer["object_format"] in ("sha1", "sha256"), "AUTHORING_GIT_FORMAT")
    length = 40 if offer["object_format"] == "sha1" else 64
    F.need(type(offer["commit"]) is str and
           re.fullmatch("[0-9a-f]{"+str(length)+"}", offer["commit"]), "AUTHORING_COMMIT")
    _directory(offer["project_dir"])
    for field in ("module", "export_name"):
        F.need(len(E.name_key(offer[field], NAME_LIMITS)) <= 2048, "AUTHORING_NAME_BYTES")
    _text(offer["toolchain"], 256, "AUTHORING_TOOLCHAIN")
    F.need(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/@+-]*", offer["toolchain"]),
           "AUTHORING_TOOLCHAIN")
    raw = F.compact(offer)
    F.need(len(raw) <= OFFER_MAX, "AUTHORING_OFFER_BYTES")
    return raw


def offer_id(offer):
    """Canonical claim deduplication only; not a source/mathematics certificate."""
    return hashlib.sha256(b"DMKN-AUTHORING-OFFER-V1\0"+_offer_bytes(offer)).hexdigest()


def request_limit(request):
    F.fields(request, ("schema", "semantic_id", "export_id", "max_offers", "max_bytes"))
    F.need(request["schema"] == REQUEST_SCHEMA, "AUTHORING_REQUEST_SCHEMA")
    F.hexid(request["semantic_id"]); F.hexid(request["export_id"])
    F.uint(request["max_offers"], 1, MAX_OFFERS, "AUTHORING_REQUEST_OFFERS")
    return F.uint(request["max_bytes"], 1, REPLY_MAX, "AUTHORING_REQUEST_BYTES")


def _envelope(request, offers, truncated):
    return {"schema": REPLY_SCHEMA, "semantic_id": request["semantic_id"],
        "export_id": request["export_id"], "status": STATUS, "offers": offers,
        "truncated": truncated, "mathematical_acceptance": False,
        "source_availability": "NOT_CHECKED", "correspondence": "NOT_CHECKED",
        "execution_approved": False, "global_complete": False}


class OfferMap:
    """One bounded immutable-byte partial catalogue with direct exact-key lookup.

    Private in-memory integrity is an ordinary local-process premise. Mutable
    parsed caller objects are never retained; returned replies never expose rows.
    """
    __slots__ = ("_rows", "raw_sha256", "key_count", "offer_count")

    def __init__(self, raw, *, check_budget=None):
        _check(check_budget)
        document = F.strict(raw, MAP_MAX)
        F.fields(document, ("schema", "entries"))
        F.need(document["schema"] == MAP_SCHEMA, "AUTHORING_MAP_SCHEMA")
        entries = document["entries"]
        F.need(type(entries) is list and len(entries) <= MAX_KEYS, "AUTHORING_MAP_KEYS")
        rows, total = {}, 0
        for entry in entries:
            _check(check_budget)
            F.fields(entry, ("semantic_id", "export_id", "offers"))
            key = (F.hexid(entry["semantic_id"]), F.hexid(entry["export_id"]))
            F.need(key not in rows, "AUTHORING_DUPLICATE_KEY")
            offers = entry["offers"]
            F.need(type(offers) is list and 1 <= len(offers) <= MAX_OFFERS, "AUTHORING_MAP_OFFERS")
            encoded, seen = [], set()
            for offer in offers:
                _check(check_budget)
                item = _offer_bytes(offer)
                F.need(item not in seen, "AUTHORING_DUPLICATE_OFFER")
                seen.add(item); encoded.append(item)
            rows[key] = tuple(encoded); total += len(encoded)
        self._rows = MappingProxyType(rows)
        self.raw_sha256 = hashlib.sha256(raw).hexdigest()
        self.key_count, self.offer_count = len(rows), total
        _check(check_budget)

    @classmethod
    def from_bytes(cls, raw, *, check_budget=None):
        F.need(cls is OfferMap, "AUTHORING_MAP_TYPE")
        return cls(raw, check_budget=check_budget)

    def reply(self, request, *, check_budget=None):
        _check(check_budget)
        maximum = request_limit(request)
        rows = self._rows.get((request["semantic_id"], request["export_id"]), ())
        retained = []
        raw = F.compact(_envelope(request, retained, bool(rows)))
        F.need(len(raw) <= maximum, "AUTHORING_REPLY_MINIMUM")
        for row in rows[:request["max_offers"]]:
            _check(check_budget)
            candidate = [*retained, json.loads(row)]
            encoded = F.compact(_envelope(request, candidate, len(candidate) < len(rows)))
            if len(encoded) > maximum:
                break  # Deterministic prefix, not an unadvertised ranking policy.
            retained, raw = candidate, encoded
        _check(check_budget)
        return raw


def reply(index, request, *, check_budget=None):
    F.need(type(index) is OfferMap, "AUTHORING_MAP_TYPE")
    return index.reply(request, check_budget=check_budget)


def read_reply(raw, request):
    maximum = request_limit(request)
    result = F.strict(raw, maximum)
    F.fields(result, REPLY_FIELDS)
    F.need(result["schema"] == REPLY_SCHEMA and result["status"] == STATUS,
           "AUTHORING_REPLY_SCHEMA")
    F.need(result["semantic_id"] == request["semantic_id"] and
           result["export_id"] == request["export_id"], "AUTHORING_REPLY_BINDING")
    F.need(result["mathematical_acceptance"] is False and result["execution_approved"] is False
           and result["global_complete"] is False and result["source_availability"] == "NOT_CHECKED"
           and result["correspondence"] == "NOT_CHECKED", "AUTHORING_REPLY_ASSURANCE")
    F.need(type(result["truncated"]) is bool and type(result["offers"]) is list and
           len(result["offers"]) <= request["max_offers"], "AUTHORING_REPLY_OFFERS")
    seen = set()
    for offer in result["offers"]:
        encoded = _offer_bytes(offer)
        F.need(encoded not in seen, "AUTHORING_DUPLICATE_OFFER")
        seen.add(encoded)
    return result
