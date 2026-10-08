"""Bounded strict CBOR/CAS bridge. Byte identity is NOT foundation qualification.

Only the selected uint64/bytes/definite-array language is supported. JSON is a
diagnostic transport: each bytes value is exactly {"$bytes": [0..255, ...]}.
No Lean execution, imports, axiom-type acceptance, or local adoption occurs here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


UINT64_MAX = (1 << 64) - 1
MAX_BYTES = 64 * 1024 * 1024
MAX_NESTING = 64  # Physical CBOR/JSON nesting, NOT native expression DAG depth.
MAX_ITEMS = 8 * 1024 * 1024
SOURCE_COMMIT = bytes.fromhex("293d5d0c0c3f3dded4688b3ccd6a33939ac5102b")
DOMAIN = b"DTMKN-CAS\x00"
ALLOWED_AXIOMS = ("propext", "Classical.choice", "Quot.sound")
EXACT_FORBIDDEN = (
    "Lean.reduceBool", "Lean.reduceNat", "dontcare",
    "__expr_for_default_constructor__", "__local_decl_for_default_constructor",
    "sorryAx", "Lean.trustCompiler", "Lean.ofReduceBool", "Lean.ofReduceNat",
)
INTERNAL_PREFIXES = ("_kernel_fresh", "_ind_fresh", "_nested_fresh", "_uniq", "_nested")
REQUIRED_ROOTS = (
    "True", "False", "Eq", "Nat", "Bool", "List", "Iff", "Nonempty",
    "propext", "Classical.choice", "Quot.sound", "Quot", "Quot.mk", "Quot.lift", "Quot.ind",
    "Nat.zero", "Nat.succ", "Bool.false", "Bool.true", "Nat.add", "Nat.sub", "Nat.mul",
    "Nat.pow", "Nat.gcd", "Nat.div", "Nat.mod", "Nat.beq", "Nat.ble", "Nat.land", "Nat.lor",
    "Nat.xor", "Nat.shiftLeft", "Nat.shiftRight", "String", "String.ofByteArray", "String.ofList",
    "Char", "Char.ofNat", "List.nil", "List.cons", "outParam", "semiOutParam", "optParam",
    "autoParam", "eagerReduce",
)


class CodecError(ValueError):
    """Invalid selected bytes, projection, or bounded construction input."""


def _uint(value, maximum=UINT64_MAX):
    if type(value) is not int or not 0 <= value <= maximum:
        raise CodecError(f"expected unsigned integer <= {maximum}")
    return value


def _array(value, length=None):
    if type(value) is not list or (length is not None and len(value) != length):
        raise CodecError(f"expected array of length {length}")
    return value


def _header(major, value):
    _uint(value)
    if value < 24:
        return bytes([(major << 5) | value])
    for ai, width in ((24, 1), (25, 2), (26, 4), (27, 8)):
        if value < (1 << (8 * width)):
            return bytes([(major << 5) | ai]) + value.to_bytes(width, "big")
    raise CodecError("uint64 overflow")


def dumps(value):
    """Encode exact Python list/int/bytes values; bool and all coercions rejected."""
    output = bytearray()
    count = 0

    def visit(item, depth):
        nonlocal count
        count += 1
        if depth > MAX_NESTING or count > MAX_ITEMS:
            raise CodecError("local codec nesting/item envelope exceeded")
        if type(item) is int:
            output.extend(_header(0, item))
        elif type(item) is bytes:
            if len(item) > MAX_BYTES:
                raise CodecError("byte-string envelope exceeded")
            output.extend(_header(2, len(item)))
            output.extend(item)
        elif type(item) is list:
            if len(item) > MAX_ITEMS:
                raise CodecError("array item envelope exceeded")
            output.extend(_header(4, len(item)))
            for child in item:
                visit(child, depth + 1)
        else:
            raise CodecError("only exact list/int/bytes values are encodable")
        if len(output) > MAX_BYTES:
            raise CodecError("canonical object exceeds local 64 MiB envelope")

    visit(value, 0)
    return bytes(output)


def loads(data):
    """Strict shortest-form decode, with full consumption and exact re-encode check."""
    if type(data) is not bytes or len(data) > MAX_BYTES:
        raise CodecError("expected bytes within local object envelope")
    position = 0
    count = 0

    def take(length):
        nonlocal position
        if length > len(data) - position:
            raise CodecError("truncated CBOR")
        result = data[position:position + length]
        position += length
        return result

    def visit(depth):
        nonlocal count
        count += 1
        if depth > MAX_NESTING or count > MAX_ITEMS:
            raise CodecError("local codec nesting/item envelope exceeded")
        first = take(1)[0]
        major, ai = first >> 5, first & 31
        if major not in (0, 2, 4):
            raise CodecError("unsupported CBOR major type")
        if ai < 24:
            value = ai
        elif ai in (24, 25, 26, 27):
            width = 1 << (ai - 24)
            value = int.from_bytes(take(width), "big")
            minimum = {24: 24, 25: 256, 26: 65536, 27: 4294967296}[ai]
            if value < minimum:
                raise CodecError("nonshortest integer/length")
        else:
            raise CodecError("unsupported/reserved/indefinite additional information")
        if major == 0:
            return value
        if major == 2:
            return take(value)
        if value > MAX_ITEMS - count or value > len(data) - position:
            raise CodecError("impossible or excessive array length")
        return [visit(depth + 1) for _ in range(value)]

    result = visit(0)
    if position != len(data):
        raise CodecError("trailing bytes")
    if dumps(result) != data:
        raise CodecError("CBOR round-trip mismatch")
    return result


def to_projection(value):
    """Convert selected CBOR values to the exact JSON bridge, without coercions."""
    dumps(value)  # Enforce the same local envelope and primitive domain.

    def visit(item):
        if type(item) is bytes:
            return {"$bytes": list(item)}
        if type(item) is list:
            return [visit(child) for child in item]
        return item

    return visit(value)


def from_projection(value):
    """Reject text, floats, booleans, nulls and non-singleton bytes objects."""
    count = 0

    def visit(item, depth):
        nonlocal count
        count += 1
        if depth > MAX_NESTING or count > MAX_ITEMS:
            raise CodecError("local projection envelope exceeded")
        if type(item) is int:
            return _uint(item)
        if type(item) is list:
            return [visit(child, depth + 1) for child in item]
        if type(item) is dict and list(item) == ["$bytes"]:
            values = _array(item["$bytes"])
            if len(values) > MAX_BYTES:
                raise CodecError("projected bytes envelope exceeded")
            return bytes(_uint(v, 255) for v in values)
        raise CodecError("invalid JSON bridge value")

    result = visit(value, 0)
    dumps(result)
    return result


def projection_loads(text):
    """JSON parser rejects duplicate keys, nonfinite constants and fractions."""
    if type(text) is not str:
        raise CodecError("JSON bridge must be text")
    try:
        text_size = len(text.encode("utf-8", errors="strict"))
    except UnicodeEncodeError as error:
        raise CodecError("invalid Unicode in JSON bridge") from error
    if text_size > MAX_BYTES:
        raise CodecError("JSON bridge text exceeds local envelope")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise CodecError("duplicate JSON object key")
            result[key] = value
        return result

    def forbidden(_):
        raise CodecError("noninteger JSON number")

    try:
        projected = json.loads(text, object_pairs_hook=pairs,
                               parse_float=forbidden, parse_constant=forbidden)
        return from_projection(projected)
    except (json.JSONDecodeError, RecursionError) as error:
        raise CodecError("malformed or overnested JSON bridge") from error


def projection_dumps(value):
    return json.dumps(to_projection(value), separators=(",", ":"), ensure_ascii=True)


def cid(object_type, schema, payload):
    """Hash the canonical encoding of a VALUE, not pre-encoded payload bytes.

    A bytes payload intentionally means a CBOR byte string. To hash existing
    encoded bytes, first loads(bytes); this prevents ambiguous interpretation.
    """
    _uint(object_type, 65535)
    _uint(schema, 65535)
    encoded = dumps(payload)
    preimage = (DOMAIN + object_type.to_bytes(2, "big") + schema.to_bytes(2, "big")
                + len(encoded).to_bytes(8, "big") + encoded)
    return [1, object_type, schema, hashlib.sha256(preimage).digest()]


def cidkey(identifier):
    """Injective 37-byte lookup key, NOT canonical CBOR and NOT a second hash."""
    _array(identifier, 4)
    if _uint(identifier[0], 255) != 1:
        raise CodecError("unsupported ContentID algorithm")
    object_type, schema = _uint(identifier[1], 65535), _uint(identifier[2], 65535)
    digest = identifier[3]
    if type(digest) is not bytes or len(digest) != 32:
        raise CodecError("ContentID digest must be exactly 32 bytes")
    return b"\x01" + object_type.to_bytes(2, "big") + schema.to_bytes(2, "big") + digest


def name_path(dotted):
    """Convenience for the fixed ASCII source names in this local selection only."""
    return [[0, component.encode("utf-8")] for component in dotted.split(".")]


def _validate_name(path):
    _array(path)
    if not path:
        raise CodecError("anonymous declaration/reference name")
    for component in path:
        _array(component, 2)
        tag = _uint(component[0], 1)
        if tag == 0:
            if type(component[1]) is not bytes:
                raise CodecError("name string component must be bytes")
            try:
                component[1].decode("utf-8", errors="strict")
            except UnicodeDecodeError as error:
                raise CodecError("invalid scalar UTF-8 name component") from error
        else:
            _uint(component[1])
    if path[0][0] == 1:
        raise CodecError("numeric-root internal name prohibited")
    first = path[0][1].decode("utf-8")
    if first.startswith(INTERNAL_PREFIXES):
        raise CodecError("internal-name prefix prohibited")
    if any(path == name_path(name) for name in EXACT_FORBIDDEN):
        raise CodecError("exact forbidden declaration/reference name")
    return dumps(path)


def _validate_seed_envelope(seed):
    """Limited shape/inventory checks, deliberately NOT kernel/schema acceptance.

    DAG records remain primitive-validated data. Their node tags, scopes,
    canonical DAG order, declaration typing, axiom types, full closure and
    generated inventory must be independently checked by the receiver/audit.
    """
    _array(seed, 3)
    commit, descriptors, exports = seed
    if commit != SOURCE_COMMIT or type(commit) is not bytes:
        raise CodecError("not the locally selected 20-byte Lean source pin")
    _array(descriptors)
    _array(exports)
    if not descriptors or not exports:
        raise CodecError("empty selected seed candidate")
    export_keys = [_validate_name(path) for path in exports]
    if export_keys != sorted(set(export_keys)):
        raise CodecError("exports must be canonical-name-byte sorted and duplicate-free")
    available = set(export_keys)
    missing = [name for name in REQUIRED_ROOTS if dumps(name_path(name)) not in available]
    if missing:
        raise CodecError("missing mandatory BOOT1 root exports: " + ", ".join(missing))
    axiom_keys = []
    declared = set()
    quotients = 0

    def declared_name(path):
        key = _validate_name(path)
        if key not in available or key in declared:
            raise CodecError("declared name missing from exports or declared twice")
        declared.add(key)

    def dag(value):
        _array(value, 3)
        _array(value[0])
        _array(value[1])
        if not value[1] or _uint(value[2]) != len(value[1]) - 1:
            raise CodecError("DAG root must be final nonempty expression node")

    for descriptor in descriptors:
        _array(descriptor)
        if not descriptor:
            raise CodecError("empty bootstrap descriptor")
        tag = _uint(descriptor[0], 5)
        if tag in (0, 1, 2, 5):
            _array(descriptor, 4 if tag == 5 else 5)
            declared_name(descriptor[1])
            _uint(descriptor[2], 1024)
            dag(descriptor[3])
            if tag == 5:
                axiom_keys.append(dumps(descriptor[1]))
            else:
                dag(descriptor[4])
        elif tag == 3:
            _array(descriptor, 4)
            _uint(descriptor[1], 1024)
            _uint(descriptor[2])
            _array(descriptor[3])
            if not descriptor[3]:
                raise CodecError("empty inductive group")
            for item in descriptor[3]:
                _array(item, 3)
                declared_name(item[0])
                dag(item[1])
                _array(item[2])
                for ctor in item[2]:
                    _array(ctor, 2)
                    declared_name(ctor[0])
                    dag(ctor[1])
        else:
            _array(descriptor, 1)
            quotients += 1
            for name in ("Quot", "Quot.mk", "Quot.lift", "Quot.ind"):
                declared_name(name_path(name))
    if quotients != 1:
        raise CodecError("exactly one quotient descriptor is required")
    expected_axioms = sorted(dumps(name_path(name)) for name in ALLOWED_AXIOMS)
    if sorted(axiom_keys) != expected_axioms:
        raise CodecError("axiom descriptor names differ from exact selected three")
    dumps(seed)


def make_foundation(seedPayload):
    """Return named candidate records: {payload, cbor, id, cidkey}.

    Keys are seed, native_rules, reserved_names, foundation. This constructs
    commitments, not a qualified profile or permission to adopt one.
    """
    _validate_seed_envelope(seedPayload)

    def record(object_type, schema, payload):
        encoded = dumps(payload)
        if loads(encoded) != payload:
            raise CodecError("candidate payload round-trip mismatch")
        identifier = cid(object_type, schema, payload)
        return {"payload": payload, "cbor": encoded, "id": identifier, "cidkey": cidkey(identifier)}

    seed = record(2, 1, seedPayload)
    axioms = sorted((name_path(name) for name in ALLOWED_AXIOMS), key=dumps)
    rules = record(3, 1, [0, 4, [0, 1, 2, 3, 4, 5], axioms])
    entries = [[path, [index]] for index, path in enumerate(seedPayload[2])]
    entries += [[name_path(name), []] for name in EXACT_FORBIDDEN]
    entries.sort(key=lambda entry: dumps(entry[0]))
    if len({dumps(entry[0]) for entry in entries}) != len(entries):
        raise CodecError("duplicate ReservedNames entry")
    reserved = record(4, 1, [seed["id"], entries])
    foundation = record(1, 2, [0, SOURCE_COMMIT, seed["id"], rules["id"], reserved["id"]])
    return {"seed": seed, "native_rules": rules, "reserved_names": reserved, "foundation": foundation}


def self_test():
    """Finite deterministic vectors only; not fuzzing or security qualification."""
    positives = [
        (0, "00"), (23, "17"), (24, "1818"), (255, "18ff"),
        (256, "190100"), (65535, "19ffff"), (65536, "1a00010000"),
        (4294967295, "1affffffff"), (4294967296, "1b0000000100000000"),
        (UINT64_MAX, "1bffffffffffffffff"), (b"", "40"), (b"abc", "43616263"),
        ([], "80"), ([1, [2], b"\x00"], "830181024100"),
        (b"a" * 24, "5818" + "61" * 24), ([0] * 24, "9818" + "00" * 24),
    ]
    for value, expected in positives:
        encoded = bytes.fromhex(expected)
        assert dumps(value) == encoded and loads(encoded) == value
        assert from_projection(to_projection(value)) == value
        assert projection_loads(projection_dumps(value)) == value
    negatives = [
        "", "1800", "1817", "1900ff", "1a0000ffff", "1b00000000ffffffff",
        "5800", "590018", "5a0000ffff", "5b00000000ffffffff",
        "9800", "990018", "9a0000ffff", "9b00000000ffffffff", "20", "60", "a0", "c000", "f4", "f6",
        "fa00000000", "fb0000000000000000", "1c", "1d", "1e", "1f", "5f", "9f", "ff",
        "18", "1900", "1a00", "1b00", "4300", "8100ff", "8200", "0000",
        "9bffffffffffffffff", "5bffffffffffffffff", "81" * (MAX_NESTING + 1) + "00",
    ]
    rejected = 0

    def reject(action):
        nonlocal rejected
        try:
            action()
        except CodecError:
            rejected += 1
        else:
            raise AssertionError("negative vector unexpectedly accepted")

    for value in negatives:
        reject(lambda value=value: loads(bytes.fromhex(value)))
    for value in (True, False, None, -1, UINT64_MAX + 1, 1.5, "abc", {}, (1,), bytearray(b"x")):
        reject(lambda value=value: dumps(value))
    for value in (True, None, "abc", -1, 1.0, {"$bytes": [256]}, {"$bytes": [True]},
                  {"$bytes": [] , "x": 0}, {"$bytes": "00"}, {"other": []}):
        reject(lambda value=value: from_projection(value))
    for value in ('{"$bytes":[],"$bytes":[]}', "NaN", "1.0", "1e0", "Infinity", "[0]0",
                  "18446744073709551616", "\ud800"):
        reject(lambda value=value: projection_loads(value))
    reject(lambda: cid(True, 1, []))
    reject(lambda: cid(65536, 1, []))
    reject(lambda: cid(1, -1, []))
    reject(lambda: cidkey([2, 1, 1, bytes(32)]))
    reject(lambda: cidkey([1, 1, 1, bytes(31)]))
    reject(lambda: make_foundation([SOURCE_COMMIT, [], []]))
    # Explicit preimage vector, independent of the encoding/hash assembly helper.
    expected_digest = hashlib.sha256(bytes.fromhex(
        "44544d4b4e2d43415300" "0002" "0001" "0000000000000001" "80")).digest()
    identifier = cid(2, 1, [])
    assert identifier == [1, 2, 1, expected_digest]
    assert cidkey(identifier) == bytes.fromhex("0100020001") + expected_digest
    assert len(cidkey(identifier)) == 37
    assert cid(2, 1, []) != cid(2, 2, []) != cid(3, 2, [])
    assert cid(2, 1, []) != cid(2, 1, b"\x80")
    assert len(EXACT_FORBIDDEN) == len(set(EXACT_FORBIDDEN)) == 9
    return {"positive_encoding_vectors": len(positives), "negative_vectors_rejected": rejected,
            "hash_preimage_vector": "passed", "scope": "finite codec tests, not native qualification"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--seed-log", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "artifacts")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps(self_test(), sort_keys=True))
    if args.seed_log is None:
        if not args.self_test:
            parser.error("specify --self-test and/or --seed-log")
        return 0
    with args.seed_log.open("rb") as stream:
        log_bytes = stream.read(MAX_BYTES + 1)
    if len(log_bytes) > MAX_BYTES:
        raise CodecError("seed log exceeds local 64 MiB envelope")
    try:
        log_text = log_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise CodecError("seed log is not strict UTF-8") from error
    seed_lines = []
    diagnostics = {}
    for line in log_text.splitlines():
        if line.startswith("SEED_JSON "):
            seed_lines.append(line[len("SEED_JSON "):])
        for prefix in ("SEED_INVENTORY_JSON", "RECEIVED_INVENTORY_JSON"):
            if line.startswith(prefix + " "):
                if prefix in diagnostics:
                    raise CodecError("duplicate inventory diagnostic")
                # Inventory is separate and does not extend any committed schema.
                diagnostics[prefix] = projection_loads(line[len(prefix) + 1:])
    if len(seed_lines) != 1:
        raise CodecError("expected exactly one SEED_JSON record")
    candidate = make_foundation(projection_loads(seed_lines[0]))
    artifact_root = Path(__file__).resolve().parent / "artifacts"
    output = args.output_dir.resolve()
    if not output.is_relative_to(artifact_root.resolve()):
        raise CodecError("generated output must remain under experiments/lean-feasibility/artifacts")
    files = {}
    manifest = {
        "status": "UNQUALIFIED_FOUNDATION_CANDIDATE_BYTES",
        "local_adoption": False, "native_replay_performed_by_codec": False,
        "semantic_schema_validation": "NOT_PERFORMED; seed envelope checks only",
        "source_commit": SOURCE_COMMIT.hex(),
        "exact_forbidden_names": list(EXACT_FORBIDDEN),
        "internal_prefix_rule_is_not_a_table_wildcard": list(INTERNAL_PREFIXES),
        "codec_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "seed_log_sha256": hashlib.sha256(log_bytes).hexdigest(),
        "objects": {}, "files": {},
    }
    for name, record in candidate.items():
        filename = name.replace("_", "-") + ".cbor"
        files[filename] = record["cbor"]
        manifest["objects"][name] = {
            "filename": filename, "content_id": to_projection(record["id"]),
            "cidkey_hex": record["cidkey"].hex(), "canonical_content_id_hex": dumps(record["id"]).hex(),
            "bytes": len(record["cbor"]), "payload_sha256": hashlib.sha256(record["cbor"]).hexdigest(),
        }
    files["seed-verified.json"] = (projection_dumps(loads(candidate["seed"]["cbor"])) + "\n").encode("utf-8")
    for name, diagnostic in diagnostics.items():
        files[name.lower().replace("_", "-") + ".json"] = (projection_dumps(diagnostic) + "\n").encode("utf-8")
    for filename, data in files.items():
        manifest["files"][filename] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    files["manifest.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.mkdir(parents=True, exist_ok=True)
    if any((output / filename).exists() for filename in files):
        raise CodecError("output already exists; select a fresh artifacts subdirectory")
    for filename, data in files.items():
        with (output / filename).open("xb") as stream:
            stream.write(data)
    print(json.dumps({"status": manifest["status"], "output": str(output),
                      "seed_descriptors": len(candidate["seed"]["payload"][1]),
                      "seed_exports": len(candidate["seed"]["payload"][2]),
                      "foundation_cidkey": candidate["foundation"]["cidkey"].hex()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CodecError as error:
        raise SystemExit("CODEC_REJECTED " + str(error)) from error
