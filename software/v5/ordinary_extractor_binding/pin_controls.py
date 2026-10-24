"""Pure changed-boundary controls; inert bytes are never executed.

Exercise the exact selected_exporter function from the pinned source AST with
explicit narrow test doubles for its already-reviewed profile and path helpers.
This tests role/pin logic, not the real loader, filesystem defenses, extractor,
profile authentication or mathematical checking. The public smoke covers actual
integration. One original 25 wall / 15 CPU seconds, no subprocess or network.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import re
import time
from types import SimpleNamespace

START = time.monotonic(), time.process_time()
PIN = "28ff83c5a8561b9f5250e9be08b34744aedd23757765feb174e1504d700308aa"
MIB = 1024**2


def need(condition, code):
    if not condition:
        raise ValueError(code)


def check():
    need(time.monotonic()-START[0] < 25 and time.process_time()-START[1] < 15,
         "CONTROL_ALLOWANCE")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_bounded(path, maximum):
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) <= maximum, "CONTROL_READ_BOUND")
    return raw


def hexid(value):
    need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None,
         "CONTROL_HEXID")


class ProfileDouble:
    def __init__(self, pins, refusal=None):
        self.file_pins, self.refusal, self.calls = tuple(pins), refusal, 0

    def verify(self, callback):
        need(callback is check, "CONTROL_CALLBACK_IDENTITY")
        callback()
        self.calls += 1
        if self.refusal:
            raise ValueError(self.refusal)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    need(output.is_absolute() and output.is_dir(), "CONTROL_OUTPUT")
    source = Path(__file__).with_name("library_extraction.py")
    raw = read_bounded(source, MIB)
    need(sha(raw) == PIN, "CONTROL_HELPER_PIN")
    tree = ast.parse(raw, filename=str(source))
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "selected_exporter"]
    need(len(functions) == 1, "CONTROL_EXACT_FUNCTION")
    fixture = output/"fixture"
    helper = fixture/"authoring/py/library_extraction.py"
    binary = fixture/"authoring/bin/MissingImportExporter.exe"
    binary.parent.mkdir(parents=True)
    # Fake executable data; no native operation, loader or module import occurs.
    content = b"not executable: newly approved local binary identity\n"
    with binary.open("xb") as stream:
        stream.write(content)
    ordinary = lambda path: Path(path)
    core = SimpleNamespace(ordinary=ordinary, hexid=hexid, read_bounded=read_bounded)
    env = {"A": SimpleNamespace(C=core, need=need, sha=sha), "Path": Path,
           "__file__": str(helper), "EXPORTER_MAXIMUM_BYTES": 32*MIB}
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), "exec"), env)
    select = env["selected_exporter"]
    helper_pin = (helper, len(raw), PIN)
    binary_pin = (binary, len(content), sha(content))
    pins = (helper_pin, binary_pin)
    rows = []

    def case(name, profile, path=binary, expected=None):
        check()
        try:
            result = select(path, profile, check)
        except ValueError as error:
            need(expected is not None and str(error) == expected,
                 "CONTROL_WRONG_REFUSAL:"+name+":"+str(error))
        else:
            need(expected is None and result == (binary,
                 {"bytes": len(content), "sha256": sha(content)}),
                 "CONTROL_EXPECTED_RESULT:"+name)
        need(profile.calls == 1, "CONTROL_PROFILE_VERIFY_ONCE:"+name)
        rows.append(name)

    case("approved-new-pin-not-historical-binary", ProfileDouble(pins))
    case("profile-verification-first", ProfileDouble(pins, "PROFILE_REFUSAL"),
         expected="PROFILE_REFUSAL")
    case("helper-must-belong-to-profile", ProfileDouble((binary_pin,)),
         expected="EXTRACTION_LOCAL_PACKAGE_ROLE")
    case("executable-must-be-selected", ProfileDouble((helper_pin,)),
         expected="EXTRACTION_SELECTED_EXECUTABLE")
    case("duplicate-executable-refused", ProfileDouble((*pins, binary_pin)),
         expected="EXTRACTION_SELECTED_EXECUTABLE")
    case("wrong-package-role-refused", ProfileDouble(pins), binary.with_name("Other.exe"),
         expected="EXTRACTION_LOCAL_PACKAGE_ROLE")
    for size in (True, 0, -1, 1.5, 32*MIB+1):
        case("invalid-size-"+repr(size), ProfileDouble((helper_pin,
             (binary, size, sha(content)))), expected="EXTRACTION_EXECUTABLE_SIZE")
    case("invalid-hash-refused", ProfileDouble((helper_pin, (binary, len(content), "F"*64))),
         expected="CONTROL_HEXID")
    case("wrong-hash-refused", ProfileDouble((helper_pin, (binary, len(content), "0"*64))),
         expected="EXTRACTION_EXECUTABLE_PIN")
    case("truncated-bytes-refused", ProfileDouble((helper_pin,
         (binary, len(content)+1, sha(content)))), expected="EXTRACTION_EXECUTABLE_PIN")
    case("oversize-reread-refused", ProfileDouble((helper_pin,
         (binary, len(content)-1, sha(content)))), expected="CONTROL_READ_BOUND")
    need(len(rows) == 15 and read_bounded(source, MIB) == raw and
         read_bounded(binary, MIB) == content, "CONTROL_FINAL_BINDINGS")
    check()
    result = {"ok": True, "controls": rows, "helper_sha256": PIN,
              "claim": "EXACT_FUNCTION_WITH_EXPLICIT_TEST_DOUBLES_NOT_INTEGRATION_OR_MATH",
              "native_operations": 0, "wall_seconds": time.monotonic()-START[0],
              "cpu_seconds": time.process_time()-START[1]}
    encoded = json.dumps(result, sort_keys=True).encode("ascii")
    with (output/"PIN-CONTROLS.json").open("xb") as stream:
        stream.write(encoded)
    print(encoded.decode("ascii"), flush=True)


if __name__ == "__main__":
    main()
