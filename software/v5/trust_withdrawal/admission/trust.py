"""Persisted local withdrawal of one immutable owner-adopted checking stack.

This is local policy, not mathematical evidence or a global revocation registry.
The owner, Python controller and filesystem/OS are trusted. Checks linearize at
their final read in the owner-serialized model; they do not cancel workers or
recall data already returned. Whole-directory rollback by the trusted owner/OS
and power-loss durability beyond the filesystem's guarantees are not claimed.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat
import weakref

from modules import codec as C

SUPPORT_SCHEMA = "DMKN_LOCAL_TRUST_SUPPORT_V1"
ADOPTION_SCHEMA = "DMKN_LOCAL_TRUST_ADOPTION_V1"
MAX_SUPPORT_BYTES = 128 * 1024
MAX_RECORD_BYTES = MAX_SUPPORT_BYTES + 1024
SUPPORT_LIMITS = C.Limits(max_bytes=MAX_SUPPORT_BYTES)
RECORD_LIMITS = C.Limits(max_bytes=MAX_RECORD_BYTES)


def _manifest(value):
    C.fields(value, {"schema", "identities", "roles"})
    C.require(value["schema"] == SUPPORT_SCHEMA, "TRUST_SUPPORT_SCHEMA")
    ids = C.fields(value["identities"], {"relation_image", "aggregate_image",
        "foundation", "policy", "receipt_scheme"})
    for name in ("relation_image", "foundation", "policy"):
        C.digest_string(ids[name])
    if ids["aggregate_image"] is not None:
        C.digest_string(ids["aggregate_image"])
    C.require(ids["receipt_scheme"] == "resolved-succinct-poseidon2",
              "TRUST_RECEIPT_SCHEME")
    roles = value["roles"]
    C.require(type(roles) is dict and 1 <= len(roles) <= 512, "TRUST_SUPPORT_ROLES")
    copied, total = {}, 0
    for name, row in roles.items():
        C.require(type(name) is str and 0 < len(name) < 256
            and all(" " <= ch <= "~" and ch not in "\\:" for ch in name)
            and all(part not in ("", ".", "..") for part in name.split("/")),
            "TRUST_SUPPORT_ROLE_NAME")
        C.fields(row, {"bytes", "sha256"})
        C.require(0 < C.uint(row["bytes"], 8 * 1024**3), "TRUST_SUPPORT_ROLE_BYTES")
        C.digest_string(row["sha256"])
        total += row["bytes"]
        C.require(total <= 8 * 1024**3, "TRUST_SUPPORT_TOTAL_BYTES")
        copied[name] = dict(row)
    result = {"schema": SUPPORT_SCHEMA, "identities": dict(ids), "roles": copied}
    C.canonical(result, SUPPORT_LIMITS)
    return result


def support_id(manifest):
    """Validate and name stable selected roles; this grants no trust authority."""
    return C.hash_value("local-trust-support-v1", _manifest(manifest), SUPPORT_LIMITS)


def _ordinary(path, *, directory):
    info = path.lstat()
    C.require(not stat.S_ISLNK(info.st_mode)
        and not (getattr(info, "st_file_attributes", 0)
                 & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)),
        "TRUST_REDIRECTED_PATH")
    C.require(stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode),
              "TRUST_PATH_KIND")
    return info


def _path(value):
    path = Path(value)
    C.require(path.is_absolute() and ".." not in path.parts
        and len(str(path)) <= 32768 and len(path.parts) <= 128, "TRUST_ABSOLUTE_PATH")
    return path


def _directory(path):
    for parent in reversed(path.parents):
        _ordinary(parent, directory=True)
    info = _ordinary(path, directory=True)
    return info.st_dev, info.st_ino


def _marker_exists(path):
    # lstat observes even a dangling redirect, partial file or directory marker.
    # No marker contents are interpreted as authority or read to decide denial.
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    return True


def _read(path):
    key = _directory(path)
    C.require(not _marker_exists(path / "WITHDRAWN"), "TRUST_WITHDRAWN")
    record = path / "ADOPTION.json"
    before = _ordinary(record, directory=False)
    C.require(0 < before.st_size <= MAX_RECORD_BYTES and before.st_nlink == 1,
              "TRUST_ADOPTION_BOUND_OR_LINK")
    with record.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        C.require((opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino),
                  "TRUST_ADOPTION_REPLACED")
        raw = stream.read(MAX_RECORD_BYTES + 1)
    after = _ordinary(record, directory=False)
    C.require(len(raw) == before.st_size == after.st_size
        and (before.st_dev, before.st_ino) == (after.st_dev, after.st_ino)
        and after.st_nlink == 1 and _directory(path) == key,
        "TRUST_ADOPTION_CHANGED_DURING_READ")
    C.require(not _marker_exists(path / "WITHDRAWN"), "TRUST_WITHDRAWN")
    return raw, key, (after.st_dev, after.st_ino)


class TrustBinding:
    """Opaque original-domain registration; constructing one grants nothing."""
    __slots__ = ("_domain", "__weakref__")

    def __init__(self):
        raise C.StructureError("TRUST_BIND_ONLY_THROUGH_DOMAIN")


class TrustDomain:
    """One existing local adoption, with sticky observed denial and no reset API."""
    __slots__ = ("_path", "_raw", "_directory_key", "_record_key", "_identity",
                 "_bindings", "_denied")

    def __init__(self):
        raise C.StructureError("TRUST_EXPLICIT_CREATE_OR_OPEN_REQUIRED")

    @classmethod
    def create(cls, fresh_directory, domain_id_hex64, manifest):
        """Explicit owner provisioning only; never replace an existing directory."""
        C.require(cls is TrustDomain, "TRUST_EXACT_DOMAIN_CLASS")
        C.digest_string(domain_id_hex64)
        selected = _manifest(manifest)
        selected_id = support_id(selected)
        raw = C.canonical({"schema": ADOPTION_SCHEMA, "domain_id": domain_id_hex64,
            "support_id": selected_id, "support": selected}, RECORD_LIMITS)
        path = _path(fresh_directory)
        _directory(path.parent)
        # A partial failed provisioning remains unusable and is never repaired
        # implicitly by create/open. No cleanup deletes retained operator state.
        path.mkdir()
        _directory(path)
        with (path / "ADOPTION.json").open("xb") as stream:
            C.require(stream.write(raw) == len(raw), "TRUST_ADOPTION_SHORT_WRITE")
            stream.flush()
            os.fsync(stream.fileno())
        return cls.open(path, domain_id_hex64, selected_id)

    @classmethod
    def open(cls, existing_directory, expected_domain_id_hex64, expected_support_id_hex64):
        """Ordinary startup: require the preexisting exact adoption, fail closed."""
        C.require(cls is TrustDomain, "TRUST_EXACT_DOMAIN_CLASS")
        C.digest_string(expected_domain_id_hex64)
        C.digest_string(expected_support_id_hex64)
        path = _path(existing_directory)
        raw, directory_key, record_key = _read(path)
        record = C.parse_json(raw, RECORD_LIMITS)
        C.fields(record, {"schema", "domain_id", "support_id", "support"})
        C.require(record["schema"] == ADOPTION_SCHEMA
            and record["domain_id"] == expected_domain_id_hex64
            and record["support_id"] == expected_support_id_hex64
            and support_id(record["support"]) == expected_support_id_hex64
            and C.canonical(record, RECORD_LIMITS) == raw, "TRUST_ADOPTION_MISMATCH")
        self = object.__new__(cls)
        self._path, self._raw = path, raw
        self._directory_key, self._record_key = directory_key, record_key
        self._identity = {"domain_id": expected_domain_id_hex64,
            "support_id": expected_support_id_hex64,
            "adoption_sha256": hashlib.sha256(raw).hexdigest()}
        # Registration should not retain every completed operation's binding.
        # Live profiles/issuers hold their own strong original binding reference.
        self._bindings, self._denied = weakref.WeakSet(), False
        self._current()
        return self

    def _current(self):
        try:
            C.require(type(self) is TrustDomain and not self._denied,
                      "TRUST_DENIAL_LATCHED")
            raw, directory_key, record_key = _read(self._path)
            C.require(raw == self._raw and directory_key == self._directory_key
                and record_key == self._record_key, "TRUST_ADOPTION_CHANGED")
        except BaseException:
            self._denied = True
            raise

    def identity(self):
        """Current checked policy identity, never a mathematical success flag."""
        self._current()
        return dict(self._identity)

    def bind(self):
        self._current()
        binding = object.__new__(TrustBinding)
        binding._domain = self
        self._bindings.add(binding)
        return binding

    def check(self, binding):
        self._current()
        C.require(type(binding) is TrustBinding and binding._domain is self
            and binding in self._bindings, "TRUST_UNREGISTERED_BINDING")
        return dict(self._identity)

    def withdraw(self, reason):
        """Flush a newly created marker, without clear/reinstate/overwrite.

        Failure is propagated, not acknowledged as persisted success. This live
        domain still denies; a partially created marker also denies on restart.
        An existing marker needs no rewrite and is already denial evidence;
        returning in that case does not claim it was freshly flushed.
        """
        C.require(type(self) is TrustDomain and type(reason) is str
            and len(reason) <= 2000, "TRUST_WITHDRAW_REASON")
        raw = C.canonical({"schema": "DMKN_LOCAL_TRUST_WITHDRAWN_V1",
            "adoption": dict(self._identity), "reason": reason}, C.Limits(max_bytes=16384))
        self._denied = True
        C.require(_directory(self._path) == self._directory_key,
                  "TRUST_DIRECTORY_CHANGED")
        marker = self._path / "WITHDRAWN"
        if _marker_exists(marker):
            return
        try:
            with marker.open("xb") as stream:
                C.require(stream.write(raw) == len(raw), "TRUST_WITHDRAW_SHORT_WRITE")
                stream.flush()
                os.fsync(stream.fileno())
        except FileExistsError:
            # An owner-serialized second withdrawal needs no update. Never
            # inspect/replace an existing marker, including incomplete content.
            C.require(_marker_exists(marker), "TRUST_WITHDRAW_MARKER_DISAPPEARED")


def check_binding(binding):
    C.require(type(binding) is TrustBinding
        and type(getattr(binding, "_domain", None)) is TrustDomain,
        "TRUST_EXACT_REGISTERED_BINDING")
    return binding._domain.check(binding)
