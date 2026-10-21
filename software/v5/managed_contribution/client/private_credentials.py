"""Explicit private-file provision for the existing placement bearer client.

Trusted same-host/current-clock cooperating owners only. Ordinary-file checks
do not establish Windows ACL confidentiality or isolation from same-user code.
No token belongs in ordinary request/plan/report/log output. Failed private
output is preserved, never overwritten/deleted/reissued by this helper.
"""
from copy import deepcopy
import hashlib
import ipaddress
import math
import os
from pathlib import Path
import time

from discovery import formal_features as F
from discovery.discovery_store import ordinary
from placement import codec as P
from placement.network import PlacementClient
from client.serve_placement import PlacementService

MAX_BYTES = 8192
CONFIDENTIALITY = "OWNER_PROVISIONED_PRIVATE_CREDENTIAL_DIRECTORY_V1"
SCOPE = "SAME_HOST_CURRENT_MONOTONIC_CLOCK_PRIVATE_OWNER_V1"
SCHEMA = "DMKN_V5_PRIVATE_PLACEMENT_CREDENTIAL_V1"
METADATA_SCHEMA = "DMKN_V5_PLACEMENT_CREDENTIAL_METADATA_V1"
READY_SCHEMA = "DMKN_V5_PRIVATE_HANDOFF_READY_V1"
SPEC_FIELDS = ("source", "write_until_ms", "retention_until_ms", "limits",
               "credential_path", "confidentiality")
METADATA_FIELDS = ("schema", "scope", "grant_id", "bindings", "read_endpoint", "intake_endpoint",
    "source", "write_until_ms", "retention_until_ms", "limits", "release_sha256", "profile_sha256",
    "operation", "session", "issuing_runtime", "service_until_ns")
STAGES = frozenset(("PREFLIGHT", "ISSUANCE_ATTEMPTED", "ISSUED", "WRITE_ATTEMPTED",
                    "FILE_CLOSED", "READBACK", "READY", "READ"))
CODES = frozenset(("PRIVATE_CREDENTIAL_PREFLIGHT_REFUSED", "PRIVATE_CREDENTIAL_HANDOFF_FAILED",
                   "PRIVATE_CREDENTIAL_READER_REFUSED"))


class CredentialError(ValueError):
    """Fixed code and whitelisted nonsecret stage only; no underlying payload."""
    def __init__(self, code, stage, grant_id=None):
        if code not in CODES or stage not in STAGES:
            code, stage, grant_id = "PRIVATE_CREDENTIAL_HANDOFF_FAILED", "PREFLIGHT", None
        if grant_id is not None and not (type(grant_id) is str and len(grant_id) == 64
                and all(c in "0123456789abcdef" for c in grant_id)):
            grant_id = None
        super().__init__(code)
        self.code, self.stage, self.grant_id = code, stage, grant_id

    def observation(self):
        return {"status": "FAILED", "code": self.code, "stage": self.stage,
                "grant_id": self.grant_id, "charge_refunded": False,
                "mathematical_acceptance": False}


def _endpoint(value):
    F.fields(value, ("host", "port", "tls", "server_name"))
    F.need(type(value["host"]) is str and str(ipaddress.IPv4Address(value["host"])) == value["host"],
           "CREDENTIAL_ENDPOINT")
    F.uint(value["port"], 1, 65535)
    F.need(type(value["tls"]) is bool and (value["server_name"] is None or
           type(value["server_name"]) is str and 1 <= len(value["server_name"]) <= 253),
           "CREDENTIAL_TLS")
    F.need(value["tls"] or value["server_name"] is None, "CREDENTIAL_TLS_NAME")


def _spec(value):
    F.fields(value, SPEC_FIELDS)
    F.need(value["confidentiality"] == CONFIDENTIALITY and type(value["credential_path"]) is str,
           "CREDENTIAL_PRIVATE_DIRECTORY_PREMISE")
    _endpoint(value["source"])
    F.uint(value["write_until_ms"], 1, 2**53-1)
    F.uint(value["retention_until_ms"], 1, 2**53-1)
    P.limits(value["limits"])


def _preflight(value, protected):
    _spec(value)
    path = ordinary(value["credential_path"], fresh=True, directory=False)
    F.need(type(protected) in (list, tuple) and 1 <= len(protected) <= 64,
           "CREDENTIAL_PROTECTED_ROOTS")
    for selected in protected:
        root = Path(selected)
        F.need(root.is_absolute() and root != Path(root.anchor), "CREDENTIAL_PROTECTED_PATH")
        F.need(not path.is_relative_to(root) and not root.is_relative_to(path), "CREDENTIAL_PATH_OVERLAP")
    return path


def preflight(specification, protected):
    """Nonsecret-only validation before launching; no files/grants are created."""
    try:
        _preflight(deepcopy(specification), protected)
    except BaseException:
        raise CredentialError("PRIVATE_CREDENTIAL_PREFLIGHT_REFUSED", "PREFLIGHT") from None


def _operation(value):
    F.fields(value, ("name", "run", "workspace_root", "plan_sha256"))
    name = value["name"]
    F.need(type(name) is str and 1 <= len(name) <= 64 and name[0] in "abcdefghijklmnopqrstuvwxyz0123456789"
           and all(c in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in name), "CREDENTIAL_OPERATION")
    F.hexid(value["plan_sha256"])
    for key in ("run", "workspace_root"):
        F.need(type(value[key]) is str and 1 <= len(value[key]) <= 2048, "CREDENTIAL_OPERATION_PATH")
        ordinary(value[key])
    F.need(Path(value["run"]) == Path(value["workspace_root"])/name, "CREDENTIAL_OPERATION_BINDING")


def _session(value):
    F.fields(value, ("number", "nonce", "worker"))
    F.uint(value["number"], 1, 4096); F.hexid(value["nonce"])
    F.fields(value["worker"], ("pid", "created"))
    F.uint(value["worker"]["pid"], 1, 2**32-1); F.uint(value["worker"]["created"], 1, 2**64-1)


def _metadata(value):
    F.fields(value, METADATA_FIELDS)
    F.need(value["schema"] == METADATA_SCHEMA and value["scope"] == SCOPE, "CREDENTIAL_SCOPE")
    for key in ("grant_id", "release_sha256", "profile_sha256", "issuing_runtime"): F.hexid(value[key])
    F.fields(value["bindings"], ("service_epoch", "generation", "namespace", "wire_profile_id"))
    for item in value["bindings"].values(): F.hexid(item)
    for key in ("read_endpoint", "intake_endpoint", "source"): _endpoint(value[key])
    for key in ("write_until_ms", "retention_until_ms"): F.uint(value[key], 1, 2**53-1)
    P.limits(value["limits"]); _operation(value["operation"]); _session(value["session"])
    F.uint(value["service_until_ns"], 1, 2**63-1)
    return deepcopy(value)


def _live(until_ns):
    F.uint(until_ns, 1, 2**63-1)
    F.need(time.monotonic_ns() < until_ns, "CREDENTIAL_ORIGINAL_SERVICE_INTERVAL")


def _file(path):
    path = ordinary(path, directory=False)
    info = path.stat()
    F.need(info.st_nlink == 1 and 0 < info.st_size <= MAX_BYTES, "CREDENTIAL_FILE_BOUND")
    with path.open("rb") as stream: raw = stream.read(MAX_BYTES+1)
    final = path.stat()
    F.need(len(raw) == info.st_size and (info.st_dev, info.st_ino, info.st_size) ==
           (final.st_dev, final.st_ino, final.st_size) and final.st_nlink == 1,
           "CREDENTIAL_FILE_CHANGED")
    return raw


def _envelope(raw):
    value = F.strict(raw, MAX_BYTES)
    F.fields(value, ("schema", "token", "metadata"))
    F.need(value["schema"] == SCHEMA, "CREDENTIAL_SCHEMA")
    token = value["token"]; F.hexid(token)
    metadata = _metadata(value["metadata"])
    F.need(hashlib.sha256(token.encode("ascii")).hexdigest() == metadata["grant_id"],
           "CREDENTIAL_TOKEN_IDENTIFIER")
    return value


def publish(service, specification, *, release_sha256, profile_sha256, operation,
            session, service_until_ns, protected):
    """Issue once and write only the explicitly selected private secret file.

    Return the nonsecret ready facet, never the issued credential dictionary.
    Any failure preserves the charged grant and partial private output.
    """
    stage, grant_id = "PREFLIGHT", None
    try:
        spec = deepcopy(specification); path = _preflight(spec, protected)
        F.need(type(service) is PlacementService, "CREDENTIAL_EXACT_SERVICE")
        _live(service_until_ns); ready = service.ready()
        numerator, denominator = service.deadline.as_integer_ratio()
        F.need(service_until_ns <= numerator*1000000000//denominator, "CREDENTIAL_SERVICE_BOUND")
        metadata = {"schema": METADATA_SCHEMA, "scope": SCOPE, "grant_id": "00"*32,
            "bindings": deepcopy(ready["bindings"]), "read_endpoint": deepcopy(ready["read_endpoint"]),
            "intake_endpoint": deepcopy(ready["intake_endpoint"]), "source": deepcopy(spec["source"]),
            "write_until_ms": spec["write_until_ms"], "retention_until_ms": spec["retention_until_ms"],
            "limits": deepcopy(spec["limits"]), "release_sha256": release_sha256,
            "profile_sha256": profile_sha256, "operation": deepcopy(operation),
            "session": deepcopy(session), "issuing_runtime": service.report()["route"]["runtime"],
            "service_until_ns": service_until_ns}
        _metadata(metadata)
        F.need(len(F.compact(metadata)) <= MAX_BYTES-512, "CREDENTIAL_METADATA_BOUND")
        _live(service_until_ns); stage = "ISSUANCE_ATTEMPTED"
        issued = service.issue_token(spec["source"], write_until_ms=spec["write_until_ms"],
            retention_until_ms=spec["retention_until_ms"], limits=spec["limits"])
        F.hexid(issued["grant_id"]); grant_id = issued["grant_id"]; stage = "ISSUED"
        F.need(issued["generation"] == metadata["bindings"]["generation"]
               and issued["write_until_ms"] == spec["write_until_ms"]
               and issued["retention_until_ms"] == spec["retention_until_ms"], "CREDENTIAL_ISSUED_BINDING")
        metadata["grant_id"] = grant_id
        raw = F.compact({"schema": SCHEMA, "token": issued["token"], "metadata": metadata})
        _envelope(raw); _live(service_until_ns)
        stage = "WRITE_ATTEMPTED"
        with path.open("xb") as stream:
            F.need(stream.write(raw) == len(raw), "CREDENTIAL_WRITE_INCOMPLETE")
            stream.flush(); os.fsync(stream.fileno())
        stage = "FILE_CLOSED"; _live(service_until_ns)
        saved = _file(path); stage = "READBACK"
        F.need(saved == raw, "CREDENTIAL_READBACK_CHANGED"); _envelope(saved)
        _live(service_until_ns); service.ready()
        return {"schema": READY_SCHEMA, "status": "READY", "stage": "READY",
                "metadata": _metadata(metadata),
                "credential": {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()},
                "recipient_receipt_confirmed": False, "mathematical_acceptance": False}
    except BaseException:
        raise CredentialError("PRIVATE_CREDENTIAL_HANDOFF_FAILED", stage, grant_id) from None


def read_client(pin, expected, *, egress, contact, deadline, requests,
                incoming_bytes, outgoing_bytes, operation_ms=60000):
    """Same-host/current-clock reader; returns existing client + public metadata.

    expected is the independently selected complete public metadata, not values
    taken from this unvalidated secret file. Contact/egress/caps stay independent.
    Caller must not persist/print the client's private attributes or wire bodies.
    """
    client = None
    try:
        F.fields(pin, ("path", "bytes", "sha256")); F.hexid(pin["sha256"])
        F.need(type(pin["path"]) is str, "CREDENTIAL_PIN_PATH")
        F.uint(pin["bytes"], 1, MAX_BYTES)
        wanted = _metadata(deepcopy(expected)); _live(wanted["service_until_ns"])
        F.need(type(deadline) in (int, float) and math.isfinite(deadline)
               and time.monotonic() < deadline <= time.monotonic()+3600, "CREDENTIAL_READER_DEADLINE")
        F.need(contact == wanted["intake_endpoint"], "CREDENTIAL_INDEPENDENT_CONTACT")
        raw = _file(pin["path"])
        F.need(len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"],
               "CREDENTIAL_FILE_PIN")
        value = _envelope(raw)
        F.need(value["metadata"] == wanted, "CREDENTIAL_EXPECTED_METADATA")
        _live(wanted["service_until_ns"])
        # nextafter avoids rounding a nanosecond cutoff up when adapting to the
        # unchanged client's float-deadline API. It never grants another duration.
        cutoff = math.nextafter(wanted["service_until_ns"]/1000000000, -math.inf)
        client = PlacementClient(egress, contact, wanted["bindings"], value["token"],
            deadline=min(deadline, cutoff), requests=requests, incoming_bytes=incoming_bytes,
            outgoing_bytes=outgoing_bytes, operation_ms=operation_ms)
        _live(wanted["service_until_ns"])
        return client, _metadata(wanted)
    except BaseException:
        if client is not None:
            try: client.close()
            except BaseException: pass
        raise CredentialError("PRIVATE_CREDENTIAL_READER_REFUSED", "READ") from None
