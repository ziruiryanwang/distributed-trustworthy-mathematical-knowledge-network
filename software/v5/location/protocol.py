"""Exact v5 rendezvous keys and bounded service descriptors.

Only an adopted local transport supplies authenticated_peer. A peer-supplied
JSON field is not channel authentication. Hints never confer mathematical,
availability, index-build, freshness or global-completeness authority.
"""
from copy import deepcopy
import ipaddress
import re

from discovery import formal_features as F
from transport.http_provider import Endpoint

ROLE = "formal-index-v1"
REQUEST_SCHEMA = "DMKN_V5_LOCATION_DESCRIPTOR_REQUEST_V1"
REPLY_SCHEMA = "DMKN_V5_LOCATION_DESCRIPTOR_V1"
ASSURANCE = "ADVISORY_SERVICE_HINT_ONLY"
MAX_DESCRIPTOR = 4096
_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def peer_id(value):
    """Canonical identity-multihash Ed25519 PeerID; no signature claim.

    This initial location profile matches the retained overlay's generated
    Ed25519 identities. Other libp2p key/PeerID representations require a new
    explicit profile, not a permissive arbitrary label.
    """
    F.need(type(value) is str and len(value) == 52, "LOCATION_PEER_ID")
    integer = 0
    for char in value:
        F.need(char in _B58, "LOCATION_PEER_ID")
        integer = integer * 58 + _B58.index(char)
    raw = integer.to_bytes((integer.bit_length() + 7) // 8, "big")
    raw = b"\0" * (len(value) - len(value.lstrip("1"))) + raw
    F.need(len(raw) == 38 and raw[:6] == b"\0\x24\x08\x01\x12\x20", "LOCATION_ED25519_PEER_ID")
    return value


def route_spec(namespace, features, stripe=0):
    return {"namespace": F.hexid(namespace), "role": ROLE,
            "predicate": {"all": list(F.validate_features(features, 8))},
            "stripe": F.uint(stripe, 0, 255, "LOCATION_STRIPE")}


def route_key(namespace, features, stripe=0):
    return F.digest("DMKN-V5-INDEX-RENDEZVOUS-V1", route_spec(namespace, features, stripe))


def descriptor_request(namespace, features, stripe, nonce, max_bytes):
    spec = route_spec(namespace, features, stripe)
    F.uint(max_bytes, 1024, MAX_DESCRIPTOR, "LOCATION_DESCRIPTOR_BYTES")
    return {"schema": REQUEST_SCHEMA, **spec,
            "route_key": route_key(namespace, features, stripe), "nonce": F.hexid(nonce),
            "max_bytes": max_bytes}


def validate_request(value):
    F.fields(value, ("schema", "namespace", "role", "predicate", "stripe", "route_key", "nonce", "max_bytes"))
    F.fields(value["predicate"], ("all",))
    F.need(value == descriptor_request(value["namespace"], value["predicate"]["all"],
        value["stripe"], value["nonce"], value["max_bytes"]), "LOCATION_REQUEST_BINDING")
    return value


def _ipv4(value):
    F.need(type(value) is str and 0 < len(value) <= 15, "LOCATION_NUMERIC_IPV4")
    address = ipaddress.IPv4Address(value)
    F.need(str(address) == value, "LOCATION_CANONICAL_IPV4")
    return address


def _server_name(value):
    if value is None:
        return None
    F.need(type(value) is str and 1 <= len(value) <= 253 and value == value.lower(),
           "LOCATION_TLS_NAME")
    labels = value.split(".")
    F.need(all(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
               for label in labels), "LOCATION_TLS_NAME")
    return value


class OwnerEgressPolicy:
    """Adopted owner data, never taken from a remote descriptor.

    Public mode uses numeric IPv4 + TLS with the owner's/system CA trust only.
    Loopback test mode lists exact allowed127.0.0.1 ports; it is not a remotely
    enabled downgrade and does not grant access to arbitrary local services.
    """
    def __init__(self, config):
        F.fields(config, ("schema", "mode", "public_ports", "test_endpoints"))
        F.need(config["schema"] == "DMKN_V5_OWNER_EGRESS_V1"
               and config["mode"] in ("public-ipv4", "loopback-test"), "LOCATION_EGRESS_SCHEMA")
        ports, tests = config["public_ports"], config["test_endpoints"]
        F.need(type(ports) is list and len(ports) <= 16 and type(tests) is list and len(tests) <= 16,
               "LOCATION_EGRESS_ENTRIES")
        for port in ports:
            F.uint(port, 1, 65535, "LOCATION_PORT")
        F.need(ports == sorted(set(ports)), "LOCATION_CANONICAL_PORTS")
        pairs = []
        for item in tests:
            F.fields(item, ("host", "port"))
            F.need(str(_ipv4(item["host"])) == "127.0.0.1", "LOCATION_TEST_LOOPBACK_ONLY")
            pairs.append((item["host"], F.uint(item["port"], 1, 65535, "LOCATION_PORT")))
        F.need(pairs == sorted(set(pairs)), "LOCATION_CANONICAL_TEST_ENDPOINTS")
        F.need((config["mode"] == "public-ipv4" and ports and not pairs)
               or (config["mode"] == "loopback-test" and pairs and not ports), "LOCATION_EGRESS_MODE")
        self._mode, self._ports, self._tests = config["mode"], frozenset(ports), frozenset(pairs)
        self._config = deepcopy(config)

    def endpoint(self, value):
        F.fields(value, ("host", "port", "tls", "server_name"))
        address, port = _ipv4(value["host"]), F.uint(value["port"], 1, 65535, "LOCATION_PORT")
        F.need(type(value["tls"]) is bool, "LOCATION_TLS_BOOL")
        name = _server_name(value["server_name"])
        if self._mode == "public-ipv4":
            F.need(address.is_global and not address.is_reserved and not address.is_multicast
                   and not address.is_loopback and not address.is_link_local and not address.is_unspecified,
                   "LOCATION_PUBLIC_ADDRESS_REQUIRED")
            F.need(port in self._ports and value["tls"] is True, "LOCATION_PUBLIC_TLS_PORT")
        else:
            F.need((str(address), port) in self._tests, "LOCATION_TEST_ENDPOINT_NOT_ALLOWED")
        F.need(value["tls"] or name is None, "LOCATION_PLAINTEXT_HAS_NO_TLS_NAME")
        return Endpoint(str(address), port, value["tls"], name, None).validate()

    def peer_address(self, value, expected_peer=None):
        """Canonical direct TCP dial hint; authenticated identity is still Noise.

        The future Node adapter must apply equivalent policy at connectionGater,
        including automatically learned/referral addresses, not only this API.
        """
        F.need(type(value) is str and len(value) <= 256, "LOCATION_PEER_ADDRESS")
        match = re.fullmatch(r"/ip4/([0-9.]+)/tcp/([1-9][0-9]{0,4})(?:/p2p/([^/]+))?", value)
        F.need(match is not None, "LOCATION_DIRECT_TCP_ONLY")
        host, raw_port, embedded = match.groups()
        address, port = _ipv4(host), F.uint(int(raw_port), 1, 65535, "LOCATION_PORT")
        if embedded is not None:
            peer_id(embedded)
        if expected_peer is not None:
            peer_id(expected_peer)
            F.need(embedded is None or embedded == expected_peer, "LOCATION_ADDRESS_PEER_BINDING")
        if self._mode == "public-ipv4":
            F.need(address.is_global and not address.is_reserved and not address.is_multicast
                   and not address.is_loopback and not address.is_link_local and not address.is_unspecified
                   and port in self._ports, "LOCATION_PEER_EGRESS")
        else:
            F.need((str(address), port) in self._tests, "LOCATION_TEST_ENDPOINT_NOT_ALLOWED")
        return value

    def report(self):
        return {"config": deepcopy(self._config), "https_trust": "OWNER_SYSTEM_CA_ONLY",
                "ca_store_updates": "TRUSTED_OWNER_ENVIRONMENT_NOT_PINNED_ROOT_SET"}


def verify_descriptor(raw, request, authenticated_peer, policy):
    validate_request(request)
    peer = peer_id(authenticated_peer)
    F.need(type(policy) is OwnerEgressPolicy, "LOCATION_OWNER_POLICY_REQUIRED")
    reply = F.strict(raw, request["max_bytes"])
    F.fields(reply, ("schema", "namespace", "role", "route_key", "nonce", "peer_id", "endpoints",
                     "assurance", "global_complete", "mathematical_acceptance"))
    F.need(reply["schema"] == REPLY_SCHEMA and reply["namespace"] == request["namespace"]
           and reply["role"] == ROLE and reply["route_key"] == request["route_key"]
           and reply["nonce"] == request["nonce"] and reply["peer_id"] == peer,
           "LOCATION_DESCRIPTOR_BINDING")
    F.need(reply["assurance"] == ASSURANCE and reply["global_complete"] is False
           and reply["mathematical_acceptance"] is False, "LOCATION_DESCRIPTOR_ASSURANCE")
    F.need(type(reply["endpoints"]) is list and 1 <= len(reply["endpoints"]) <= 4,
           "LOCATION_ENDPOINT_COUNT")
    endpoints = tuple(policy.endpoint(value) for value in reply["endpoints"])
    F.need(len(set(endpoints)) == len(endpoints), "LOCATION_DUPLICATE_ENDPOINT")
    return endpoints
