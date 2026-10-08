"""Owner-only adapter: one 240-second session under the existing stage runner.

This is not a supervisor, sandbox, admission path, or mathematical checker.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import types


INSTALL = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\usefulness-vocabulary-01\install")
SOURCE_PINS = {
    "domains": (4934, "1ff763737af54286b3c676dbb8cc4b30b8a34f87f48b9f4145b7ad0954a77ea7"),
    "peer_wire": (16924, "bdf71281b0bcb81b762551ae33b502a9f75534774e11393a1b0b6131797e798c"),
    "peer_service": (13339, "58d355b183790e54c0bc5c96738e3ac0c2358aa1c65d0c1704d45e9ef8f28407"),
}
VIEW_PINS = {
    "complete.json": (245, "fca2e839d9c8953eb96585b7d069064603eda434e6128764237a20e5bac36865"),
    "catalog.json": (18550, "354a5f4be37454df38b48b70f49c35efb7522fc1595d8ba44bb80eadcf8735c4"),
}


def require(ok, code):
    if not ok:
        raise ValueError(code)


def pinned_bytes(path, expected):
    size, digest = expected
    with path.open("rb") as stream:
        raw = stream.read(size + 1)
    require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest,
            "FIXED_INPUT_PIN_MISMATCH")
    return raw


def source_module(name, path, raw):
    # Execute the authenticated source bytes, never a cached bytecode substitute.
    require(name not in sys.modules, "UNEXPECTED_PRELOADED_PRODUCT_MODULE")
    module = types.ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ""
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def main():
    require(sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_user_site and sys.flags.no_site,
            "PYTHON_ISOLATED_STARTUP_REQUIRED")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True, type=int)
    args = parser.parse_args()
    require(1 <= args.port <= 65535, "LOCAL_ENDPOINT_REFUSED")

    sources = {name: pinned_bytes(INSTALL / "py" / (name + ".py"), pin)
               for name, pin in SOURCE_PINS.items()}
    modules = {name: source_module(name, INSTALL / "py" / (name + ".py"), raw)
               for name, raw in sources.items()}
    D, W, service = (modules[name] for name in ("domains", "peer_wire", "peer_service"))

    helper = Path(__file__).resolve(strict=True)
    stage = helper.parent.parent
    require(helper == stage / "input" / "serve_usefulness_corpus.py"
            and Path.cwd().resolve(strict=True) == stage, "SELECTED_STAGE_LAYOUT")
    plan = W.strict_json(W.read_local(stage / "plan.json", 65536), 65536)
    domains = D.Domains.from_stage_plan(plan)
    require(domains.install == INSTALL and plan["seconds"] == 300,
            "FIXED_INSTALL_OR_STAGE_ENVELOPE")
    require(domains.require_stage(stage, plan["request_directory"]) == stage
            and str(stage) == plan["stage_directory"], "SELECTED_STAGE_BINDING")
    domains.require_read(helper)
    view = domains.require_read(stage / "input" / "view")
    W.safe_path(view, directory=True)
    for name, pin in VIEW_PINS.items():
        pinned_bytes(W.safe_path(view / name), pin)
    # The existing loader verifies all bundles against the pinned catalog.
    ready = domains.require_write(stage / "out" / "ready.json")
    require(ready == stage / "out" / "ready.json", "SELECTED_READY_PATH")
    W.safe_path(ready.parent, directory=True)
    require(not ready.exists() and not ready.is_symlink(), "READY_ALREADY_EXISTS")
    result = service.serve(view, args.port, ready, session_seconds=240,
                           max_requests=128, max_bytes=256 * 1024 * 1024)
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), allow_nan=False)
    require(len(raw.encode("utf-8")) <= 4096, "SERVICE_RESULT_BOUND")
    print(raw, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
