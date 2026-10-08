"""Bounded inert peer framing. No mathematical acceptance or native imports."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re

MIB = 1024 * 1024
MAGIC = b"DTMKN-PEER-BUNDLE-1\n"
CATALOG_MAX = 65536
MANIFEST_MAX = MIB
OBJECT_MAX = 16 * MIB
PAYLOAD_MAX = 16 * MIB
BUNDLE_MAX = 18 * MIB
VIEW_MAX = 64 * MIB
OBJECT_COUNT = 8192
ENTRY_COUNT = 32
HEX = re.compile(r"[0-9a-f]{64}\Z")
KINDS = {(1, 2), (2, 1), (3, 1), (4, 1), (0x15, 3),
         *((tag, 2) for tag in (0x10, 0x11, 0x12, 0x13, 0x18, 0x19)),
         *((tag, 1) for tag in (0x20, 0x22, 0x23, 0x24))}
FORMAL_FIELDS = {"replay", "native_ref", "semantic_target", "universe_arity", "type_dag",
                 "descriptor", "descriptor_id", "symbols", "trace"}


class WireError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def require(ok, code="PEER_SCHEMA_REFUSED"):
    if not ok:
        raise WireError(code)


def uint(value, maximum=(1 << 64) - 1):
    require(type(value) is int and 0 <= value <= maximum)
    return value


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("utf-8")


def fields(value, names):
    require(type(value) is dict and set(value) == set(names))


def strict_json(raw, maximum):
    require(type(raw) is bytes and 0 < len(raw) <= maximum, "TRANSFER_LIMIT")
    # Bound physical nesting before the JSON decoder allocates nested objects.
    depth, quoted, escape = 0, False, False
    for byte in raw:
        if quoted:
            if escape:
                escape = False
            elif byte == 92:
                escape = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (91, 123):
            depth += 1
            require(depth <= 64)
        elif byte in (93, 125):
            depth -= 1
            require(depth >= 0)

    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value)
            value[key] = item
        return value

    def bad(_):
        raise WireError("PEER_SCHEMA_REFUSED")

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                           parse_float=bad, parse_constant=bad)
        pending, count = [value], 0
        while pending:
            item = pending.pop()
            count += 1
            require(count <= 262144)
            if type(item) is dict:
                pending.extend(item.keys())
                pending.extend(item.values())
            elif type(item) is list:
                pending.extend(item)
            elif type(item) is str:
                item.encode("utf-8", errors="strict")
            elif type(item) is int:
                uint(item)
            else:
                require(item is None or type(item) is bool)
        return value
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as error:
        if isinstance(error, WireError):
            raise
        raise WireError("PEER_SCHEMA_REFUSED") from None


def typed_id(value, kind=None):
    require(type(value) is list and len(value) == 4)
    require(uint(value[0], 1) == 1)
    uint(value[1], 65535)
    uint(value[2], 65535)
    fields(value[3], {"$bytes"})
    raw = value[3]["$bytes"]
    require(type(raw) is list and len(raw) == 32)
    for byte in raw:
        uint(byte, 255)
    require(kind is None or value[1:3] == list(kind))
    return value


def _header(major, number):
    uint(number)
    if number < 24:
        return bytes([(major << 5) | number])
    for width, tag in ((1, 24), (2, 25), (4, 26), (8, 27)):
        if number < (1 << (8 * width)):
            return bytes([(major << 5) | tag]) + number.to_bytes(width, "big")
    raise WireError("PEER_SCHEMA_REFUSED")


def object_name(identifier):
    """Exactly canonical CBOR(typed ID).hex(), matching existing identity()."""
    typed_id(identifier)
    return (b"\x84" + b"\x01" + _header(0, identifier[1]) +
            _header(0, identifier[2]) + b"\x58\x20" + bytes(identifier[3]["$bytes"])).hex() + ".cbor"


def canonical_payload(raw):
    """Bounded nonallocating syntax scan; uint/bytes/definite arrays only."""
    require(type(raw) is bytes and 0 < len(raw) <= OBJECT_MAX, "TRANSFER_LIMIT")
    offset, count, stack = 0, 0, [1]
    while stack:
        if stack[-1] == 0:
            stack.pop()
            continue
        stack[-1] -= 1
        count += 1
        require(count <= 8 * MIB and len(stack) <= 65, "OBJECT_ENCODING_REFUSED")
        require(offset < len(raw), "OBJECT_ENCODING_REFUSED")
        first = raw[offset]
        offset += 1
        major, info = first >> 5, first & 31
        require(major in (0, 2, 4), "OBJECT_ENCODING_REFUSED")
        if info < 24:
            size = info
        else:
            require(info in (24, 25, 26, 27), "OBJECT_ENCODING_REFUSED")
            width = 1 << (info - 24)
            require(offset + width <= len(raw), "OBJECT_ENCODING_REFUSED")
            size = int.from_bytes(raw[offset:offset + width], "big")
            offset += width
            require(size >= {24: 24, 25: 256, 26: 65536, 27: 4294967296}[info],
                    "OBJECT_ENCODING_REFUSED")
        if major == 2:
            require(size <= len(raw) - offset, "OBJECT_ENCODING_REFUSED")
            offset += size
        elif major == 4:
            require(size <= min(8 * MIB - count, len(raw) - offset), "OBJECT_ENCODING_REFUSED")
            stack.append(size)
    require(offset == len(raw), "OBJECT_ENCODING_REFUSED")


def verify_object(identifier, raw):
    typed_id(identifier)
    require(tuple(identifier[1:3]) in KINDS, "OBJECT_KIND_REFUSED")
    canonical_payload(raw)
    preimage = (b"DTMKN-CAS\0" + identifier[1].to_bytes(2, "big") +
                identifier[2].to_bytes(2, "big") + len(raw).to_bytes(8, "big") + raw)
    require(hashlib.sha256(preimage).digest() == bytes(identifier[3]["$bytes"]), "OBJECT_ID_MISMATCH")


def parse_manifest(raw, foundation):
    typed_id(foundation, (1, 2))
    value = strict_json(raw, MANIFEST_MAX)
    fields(value, {"foundation", "root", "objects", "inventories"})
    typed_id(value["foundation"], (1, 2))
    require(value["foundation"] == foundation, "FOUNDATION_MISMATCH")
    typed_id(value["root"], (0x15, 3))
    objects = value["objects"]
    require(type(objects) is list and 0 < len(objects) <= OBJECT_COUNT, "TRANSFER_LIMIT")
    names = set()
    for identifier in objects:
        typed_id(identifier)
        require(tuple(identifier[1:3]) in KINDS, "OBJECT_KIND_REFUSED")
        name = object_name(identifier)
        require(name not in names, "BUNDLE_FRAMING_REFUSED")
        names.add(name)
    require(object_name(value["root"]) in names, "BUNDLE_FRAMING_REFUSED")
    require(type(value["inventories"]) is list)
    # Full inventory semantics/exact root closure belong to local Checker.offer.
    return value


def validate_entry(entry):
    fields(entry, {"descriptor_id", "root", "manifest_sha256", "bundle_sha256", "bundle_bytes", "formal_metadata"})
    typed_id(entry["descriptor_id"], (0x8111, 3))
    typed_id(entry["root"], (0x15, 3))
    require(type(entry["bundle_bytes"]) is int and 0 < entry["bundle_bytes"] <= BUNDLE_MAX, "TRANSFER_LIMIT")
    for field in ("manifest_sha256", "bundle_sha256"):
        require(type(entry[field]) is str and HEX.fullmatch(entry[field]))
    formal = entry["formal_metadata"]
    fields(formal, FORMAL_FIELDS)
    require(formal["replay"] == entry["root"] and formal["descriptor_id"] == entry["descriptor_id"],
            "ADVERTISED_METADATA_MISMATCH")
    return entry


def parse_catalog(raw, expected_foundation):
    typed_id(expected_foundation, (1, 2))
    value = strict_json(raw, CATALOG_MAX)
    fields(value, {"schema", "foundation", "entries"})
    require(type(value["schema"]) is int and value["schema"] == 1)
    typed_id(value["foundation"], (1, 2))
    require(value["foundation"] == expected_foundation, "FOUNDATION_MISMATCH")
    require(type(value["entries"]) is list and len(value["entries"]) <= ENTRY_COUNT, "TRANSFER_LIMIT")
    seen = set()
    for entry in value["entries"]:
        validate_entry(entry)
        require(entry["bundle_sha256"] not in seen)
        seen.add(entry["bundle_sha256"])
    return value


def safe_path(path, *, directory=False):
    path = Path(path).absolute()
    for part in (path, *path.parents):
        stat = part.lstat()
        require(not part.is_symlink() and not (getattr(stat, "st_file_attributes", 0) & 0x400), "LOCAL_PATH_REFUSED")
    require(path.is_dir() if directory else path.is_file(), "LOCAL_PATH_REFUSED")
    return path.resolve(strict=True)


def read_local(path, maximum):
    path = safe_path(path)
    require(path.stat().st_size <= maximum, "TRANSFER_LIMIT")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    require(len(raw) <= maximum, "TRANSFER_LIMIT")
    return raw


def _new_directory(path):
    path = Path(path).absolute()
    parent = safe_path(path.parent, directory=True)
    require(path.name not in ("", ".", "..") and not path.exists(), "LOCAL_PATH_REFUSED")
    result = parent / path.name
    result.mkdir(exist_ok=False)
    return safe_path(result, directory=True)


def _save(path, raw):
    with Path(path).open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def make_bundle(package_dir):
    directory = safe_path(package_dir, directory=True)
    manifest_raw = read_local(directory / "manifest.json", MANIFEST_MAX)
    projection = strict_json(manifest_raw, MANIFEST_MAX)
    require(type(projection) is dict and "foundation" in projection)
    manifest = parse_manifest(manifest_raw, projection["foundation"])
    payloads, total = [], 0
    for identifier in manifest["objects"]:
        raw = read_local(directory / "objects" / object_name(identifier), min(OBJECT_MAX, PAYLOAD_MAX - total))
        require(raw, "BUNDLE_FRAMING_REFUSED")
        total += len(raw)
        verify_object(identifier, raw)
        payloads.append(len(raw).to_bytes(8, "big") + raw)
    bundle = MAGIC + len(manifest_raw).to_bytes(4, "big") + manifest_raw + b"".join(payloads)
    require(len(bundle) <= BUNDLE_MAX, "TRANSFER_LIMIT")
    return bundle


class _BoundedReader:
    def __init__(self, stream, size):
        self.stream, self.remaining = stream, size
        self.hasher = hashlib.sha256()

    def take(self, count):
        require(0 <= count <= self.remaining, "BUNDLE_FRAMING_REFUSED")
        output = bytearray()
        while len(output) < count:
            chunk = self.stream.read(min(65536, count - len(output)))
            require(type(chunk) is bytes and 0 < len(chunk) <= count - len(output), "BUNDLE_FRAMING_REFUSED")
            output.extend(chunk)
            self.hasher.update(chunk)
            self.remaining -= len(chunk)
        return bytes(output)

    def finish(self):
        require(self.remaining == 0 and self.stream.read(1) == b"", "BUNDLE_FRAMING_REFUSED")


def receive_bundle(stream, entry, expected_foundation, destination):
    """Materialize transport-checked bytes only. Failure leaves charged staging.

    Caller must reserve capacity/supervise/retain a quiescence-aware cleanup path.
    No candidate registry or acceptance is created here.
    """
    validate_entry(entry)
    typed_id(expected_foundation, (1, 2))
    source = _BoundedReader(stream, entry["bundle_bytes"])
    require(source.take(len(MAGIC)) == MAGIC, "BUNDLE_FRAMING_REFUSED")
    count = int.from_bytes(source.take(4), "big")
    require(0 < count <= MANIFEST_MAX, "TRANSFER_LIMIT")
    manifest_raw = source.take(count)
    manifest = parse_manifest(manifest_raw, expected_foundation)
    require(manifest["root"] == entry["root"], "ADVERTISED_METADATA_MISMATCH")
    directory = _new_directory(destination)
    objects_dir = directory / "objects"
    objects_dir.mkdir()
    _save(directory / "manifest.json", manifest_raw)
    total = 0
    for identifier in manifest["objects"]:
        length = int.from_bytes(source.take(8), "big")
        require(0 < length <= OBJECT_MAX and total + length <= PAYLOAD_MAX, "TRANSFER_LIMIT")
        require(length <= source.remaining, "BUNDLE_FRAMING_REFUSED")
        total += length
        with (objects_dir / object_name(identifier)).open("xb") as output:
            remaining = length
            while remaining:
                raw = source.take(min(65536, remaining))
                output.write(raw)
                remaining -= len(raw)
            output.flush()
            os.fsync(output.fileno())
    source.finish()
    require(source.hasher.hexdigest() == entry["bundle_sha256"], "BUNDLE_DIGEST_MISMATCH")
    require(digest(manifest_raw) == entry["manifest_sha256"], "MANIFEST_DIGEST_MISMATCH")
    for identifier in manifest["objects"]:
        verify_object(identifier, read_local(objects_dir / object_name(identifier), OBJECT_MAX))
    return {"package": {"path": str(directory), "manifest_sha256": digest(manifest_raw)},
            "root": manifest["root"], "descriptor_id": entry["descriptor_id"],
            "advertised_metadata": entry["formal_metadata"], "bundle_sha256": entry["bundle_sha256"],
            "mathematicalAcceptance": False, "native_stages": 0,
            "basis": "TRANSPORT_AND_OBJECT_IDENTITIES_ONLY"}


def build_view(destination, foundation, offers):
    """Caller authenticates explicit publication or replica-custody authority.

    This inert constructor grants neither sharing authority nor acceptance.
    """
    typed_id(foundation, (1, 2))
    require(type(offers) is list and len(offers) <= ENTRY_COUNT, "TRANSFER_LIMIT")
    directory = _new_directory(destination)
    (directory / "bundles").mkdir()
    entries, total, seen = [], 0, set()
    for offer in offers:
        require(type(offer) is dict and {"package", "descriptor_id", "formal_metadata"} <= set(offer))
        fields(offer["package"], {"path", "manifest_sha256"})
        require(type(offer["package"]["path"]) is str and type(offer["package"]["manifest_sha256"]) is str and
                re.fullmatch(r"[0-9a-fA-F]{64}", offer["package"]["manifest_sha256"]))
        manifest_raw = read_local(Path(offer["package"]["path"]) / "manifest.json", MANIFEST_MAX)
        require(digest(manifest_raw) == offer["package"]["manifest_sha256"].lower(), "MANIFEST_DIGEST_MISMATCH")
        manifest = parse_manifest(manifest_raw, foundation)
        bundle = make_bundle(offer["package"]["path"])
        # Owner-controlled files must remain stable between both reads.
        embedded = bundle[len(MAGIC) + 4:len(MAGIC) + 4 + len(manifest_raw)]
        require(embedded == manifest_raw, "MANIFEST_DIGEST_MISMATCH")
        sha = digest(bundle)
        require(sha not in seen)
        seen.add(sha)
        total += len(bundle)
        require(total <= VIEW_MAX, "LOCAL_QUOTA")
        entry = {"descriptor_id": offer["descriptor_id"], "root": manifest["root"],
                 "manifest_sha256": digest(manifest_raw), "bundle_sha256": sha,
                 "bundle_bytes": len(bundle), "formal_metadata": offer["formal_metadata"]}
        validate_entry(entry)
        entries.append(entry)
        _save(directory / "bundles" / (sha + ".bundle"), bundle)
    catalog = {"schema": 1, "foundation": foundation, "entries": entries}
    catalog_raw = encoded(catalog)
    parse_catalog(catalog_raw, foundation)
    _save(directory / "catalog.json", catalog_raw)
    _save(directory / "complete.json", encoded({"schema": 1, "foundation": foundation,
                                               "catalog_sha256": digest(catalog_raw)}))
    return catalog


def load_view(directory):
    directory = safe_path(directory, directory=True)
    complete = strict_json(read_local(directory / "complete.json", 4096), 4096)
    fields(complete, {"schema", "foundation", "catalog_sha256"})
    require(type(complete["schema"]) is int and complete["schema"] == 1)
    raw = read_local(directory / "catalog.json", CATALOG_MAX)
    require(digest(raw) == complete["catalog_sha256"], "BUNDLE_DIGEST_MISMATCH")
    catalog = parse_catalog(raw, complete["foundation"])
    total, mapping = 0, {}
    for entry in catalog["entries"]:
        path = directory / "bundles" / (entry["bundle_sha256"] + ".bundle")
        data = read_local(path, BUNDLE_MAX)
        require(len(data) == entry["bundle_bytes"] and digest(data) == entry["bundle_sha256"], "BUNDLE_DIGEST_MISMATCH")
        total += len(data)
        require(total <= VIEW_MAX, "LOCAL_QUOTA")
        mapping[entry["bundle_sha256"]] = (path, entry["bundle_bytes"])
    return {"catalog": catalog, "catalog_raw": raw, "bundles": mapping}
