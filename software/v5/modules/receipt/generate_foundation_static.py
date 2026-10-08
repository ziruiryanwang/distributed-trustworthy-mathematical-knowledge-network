"""Deterministically render the exact immutable foundation; stdout only.

Owner/source preparation, not a guest or a mathematical test. The generated
file is installed through apply_patch; this utility never writes project files.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
SOURCE = ROOT / "experiments/v5-local-checks/receipt-prepare-01/prepared/base/receipt-input.json"
SOURCE_SHA = "025d2ce3c42cf7eeab00d1e6626d22d59afe495c64232ad2687893eea278d4a8"
CANONICAL_SHA = "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"


def literal(text):
    assert type(text) is str
    return 'b"'+''.join(chr(b) if 32 <= b < 127 and b not in (34, 92)
                        else f'\\x{b:02x}' for b in text.encode("utf-8"))+'"'


def expression(value):
    if value is None:
        return "StaticValue::Null"
    if type(value) is bool:
        return "StaticValue::Bool("+str(value).lower()+")"
    if type(value) is int:
        assert 0 <= value < 2**64
        return f"StaticValue::U64({value})"
    if type(value) is str:
        return "StaticValue::String("+literal(value)+")"
    if type(value) is list:
        return "StaticValue::Array(&["+",".join(map(expression, value))+"])"
    assert type(value) is dict and all(type(key) is str for key in value)
    return "StaticValue::Object(&["+",".join("("+literal(key)+","+expression(value[key])+")"
                                            for key in sorted(value))+"])"


def render(rows):
    canonical = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    assert len(rows) == 413 and len(canonical) == 23313
    assert hashlib.sha256(canonical).hexdigest() == CANONICAL_SHA
    return ("// Generated immutable values; do not hand-edit.\n"
        "// Source: receipt-prepare-01/prepared/base/receipt-input.json SHA256\n"
        "// "+SOURCE_SHA+"\n"
        "// First413 rows canonical UTF8:23313bytes, SHA256\n"
        "// "+CANONICAL_SHA+"\n"
        "// Foundation ID:d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481\n"
        "pub(crate) const ADOPTED_FOUNDATION: StaticValue = StaticValue::Array(&[\n"
        +"\n".join("    "+expression(row)+"," for row in rows)+"\n]);\n")


if __name__ == "__main__":
    raw = SOURCE.read_bytes()
    assert len(raw) < 2**20 and hashlib.sha256(raw).hexdigest() == SOURCE_SHA
    print(render(json.loads(raw)["rows"][:413]), end="")
