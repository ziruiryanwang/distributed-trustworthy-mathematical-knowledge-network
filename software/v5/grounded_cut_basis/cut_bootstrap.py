"""Approved exact-source loader; no peer code, native run or mathematical state.

The caller first uses the approved ordinary profile loader in an isolated owner
process. This entrypoint, interpreter and immutable owner storage are premises.
Hash equality does not establish initial adoption or defeat in-process tampering.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

MIB = 1024**2
SCHEMA = "DMKN_GROUNDED_CUT_BASIS_SUPPORT_V1"
SOURCES = {"GroundedCut.lean", "GroundedCutDriver.lean", "cut_worker.py",
           "cut_bootstrap.py", "cut_runtime.py", "cut_controller.py",
           "source_anchor.py", "cut_map.py", "cut_summary.py", "cut_catalog.py"}
OBJECTS = {"lean-lib/GroundedCut" + suffix for suffix in
           (".olean", ".olean.private", ".olean.server", ".ir", ".ir.sig")}
ORDER = ("cut_map", "cut_summary", "source_anchor", "cut_catalog", "cut_runtime", "cut_controller")


def need(ok, code):
    if not ok:
        raise ValueError("GROUNDED_BOOTSTRAP_" + code)


def _pin(raw, pin, C, maximum):
    need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
         type(pin["bytes"]) is int and 0 < pin["bytes"] <= maximum, "FILE_PIN")
    need(type(raw) is bytes and len(raw) == pin["bytes"] and
         hashlib.sha256(raw).hexdigest() == C.hexid(pin["sha256"]), "FILE_CHANGED")


def _read(C, path, maximum, check):
    check()
    raw = C.read_bounded(path, maximum)
    check()
    return raw


def _base(base, check):
    """Bind the already-adopted ordinary graph, not a caller's replacement core."""
    need(type(base) is SimpleNamespace and type(base.A) is ModuleType and
         sys.modules.get("ordinary_admission") is base.A, "BASE_ADMISSION_MODULE")
    A = base.A
    E, S, C, P, PE = A.E, A.S, A.C, A.P, A.PE
    shared = {"ordinary_admission": A, "ordinary_evidence": E,
              "ordinary_semantics": S, "local_catalog": C,
              "portable_catalog": P, "portable_evidence": PE}
    need(all(type(module) is ModuleType and sys.modules.get(name) is module
             for name, module in shared.items()), "BASE_SHARED_MODULES")
    need(S.E is E and C.E is E and PE.E is E and PE.S is S and
         P.E is E and P.S is S and P.PE is PE and P.L is C, "BASE_CORE_GRAPH")
    need(type(base.installation) is A.NativeInstallation, "BASE_INSTALLATION_TYPE")
    installation = base.installation
    root = C.ordinary(base.root, directory=True)
    need(installation.root == root / "installation", "BASE_INSTALLATION_PATH")
    raw = _read(C, root / "PROFILE.json", 2 * MIB, check)
    descriptor = E.strict_json(raw, E.Limits(max_bytes=2 * MIB))
    need(type(descriptor) is dict and set(descriptor) == {"schema", "installation_manifest_sha256",
         "helper_paths", "author_worker", "files"} and
         descriptor["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
         descriptor == base.descriptor, "BASE_PROFILE_DESCRIPTOR")
    manifest = _read(C, root / "installation/INSTALLATION.json", 2 * MIB, check)
    need(manifest == installation.manifest_raw and
         hashlib.sha256(manifest).hexdigest() == C.hexid(descriptor["installation_manifest_sha256"])
         == installation.manifest_sha256 and
         E.strict_json(manifest, E.Limits(max_bytes=2 * MIB)) == installation.doc,
         "BASE_INSTALLATION_BINDING")
    for role, module in (("core", A), ("evidence", E), ("semantics", S),
                         ("legacy_catalog", C), ("catalog", P), ("portable_evidence", PE)):
        path = installation.path(role)
        need(Path(module.__file__).absolute() == path, "BASE_RUNNING_CORE")
        pin = installation.doc["files"][installation.doc["roles"][role]]
        _pin(_read(C, path, 2 * MIB, check), pin, C, 2 * MIB)
    G = base.G
    need(type(G) is ModuleType and sys.modules.get("ordinary_contribution") is G and
         G.A is A and G.E is E and G.S is S and G.PE is PE and G.P is P and
         Path(G.__file__).absolute() == root / "authoring/py/ordinary_contribution.py" and
         type(base.profile) is G.AuthoringProfile, "BASE_AUTHORING_GRAPH")
    files = descriptor["files"]
    need(type(files) is dict and 1 <= len(files) <= 512, "BASE_PROFILE_CENSUS")
    pins = []
    for name, pin in files.items():
        check()
        path = root.joinpath(*A.relative(name).parts)
        need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
             type(pin["bytes"]) is int and 0 < pin["bytes"] <= 128 * MIB, "BASE_PROFILE_PIN")
        pins.append((path, pin["bytes"], C.hexid(pin["sha256"])))
    profile = base.profile
    need(descriptor["helper_paths"] == ["authoring/helpers"] and
         descriptor["author_worker"] == "author_worker.py" and
         profile.installation_manifest_sha256 == installation.manifest_sha256 and
         profile.helper_paths == (root / "authoring/helpers",) and
         profile.author_worker_script == root / "author_worker.py" and
         type(profile.file_pins) is tuple and len(profile.file_pins) == len(pins) and
         set(profile.file_pins) == set(pins), "BASE_AUTHORING_PROFILE")
    _pin(_read(C, root / "authoring/py/ordinary_contribution.py", 2 * MIB, check),
         files["authoring/py/ordinary_contribution.py"], C, 2 * MIB)
    # CutRuntime.open calls the exact profile.verify once for remaining payloads.
    return A, E, S, C, P, PE, raw


def _graph(modules, A, E, S, C, P, PE):
    M, Q, H, K, R, T = (modules[name] for name in ORDER)
    need(Q.E is E and Q.S is S and Q.PE is PE and H.E is E and H.S is S and H.P is P and
         K.E is E and K.P is P and K.M is M and K.A is H and
         R.E is E and R.S is S and R.A is A and R.C is C and R.H is H and
         T.E is E and T.S is S and T.A is A and T.PE is PE and T.P is P and
         T.M is M and T.Q is Q and T.K is K and T.H is H and T.R is R,
         "LOADED_GRAPH_IDENTITY")


def load(addition_root, expected_manifest_sha256, base, *, check):
    """Return exact runtime/controller modules and their one opened support object.

    Only an approved ordinary-base namespace is accepted. No sys.path addition,
    automatic import of cut modules, retry, native invocation or catalog open.
    """
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize and callable(check), "OWNER_PROCESS")
    check()
    forbidden = (*ORDER, "cut_worker")
    need(not any(name == selected or name.startswith(selected + ".")
                 for name in sys.modules for selected in forbidden), "PRELOADED_CUT_MODULE")
    A, E, S, C, P, PE, base_raw = _base(base, check)
    root = C.ordinary(addition_root, directory=True)
    need(Path(__file__).absolute() == root / "cut_bootstrap.py", "RUNNING_BOOTSTRAP")
    for other in (base.root, *base.installation.runtime_roots.values()):
        need(not root.is_relative_to(other) and not other.is_relative_to(root), "SUPPORT_OVERLAP")
    raw = _read(C, root / "CUT-SUPPORT.json", 2 * MIB, check)
    need(hashlib.sha256(raw).hexdigest() == C.hexid(expected_manifest_sha256), "SUPPORT_PIN")
    doc = E.strict_json(raw, E.Limits(max_bytes=2 * MIB))
    need(type(doc) is dict and set(doc) == {"schema", "base_profile_sha256", "files"} and
         doc["schema"] == SCHEMA and hashlib.sha256(base_raw).hexdigest() ==
         C.hexid(doc["base_profile_sha256"]), "SUPPORT_BASE_BINDING")
    files = doc["files"]
    need(type(files) is dict and SOURCES | {"lean-lib/GroundedCut.olean"} <= set(files)
         <= SOURCES | OBJECTS, "SUPPORT_CENSUS")
    total = 0
    for pin in files.values():
        need(type(pin) is dict and set(pin) == {"bytes", "sha256"} and
             type(pin["bytes"]) is int and 0 < pin["bytes"] <= 64 * MIB, "PAYLOAD_PIN")
        C.hexid(pin["sha256"])
        total += pin["bytes"]
    need(total <= 512 * MIB, "SUPPORT_TOTAL_BOUND")
    verified = {}
    for name in ("cut_bootstrap", *ORDER):
        source = _read(C, root / (name + ".py"), 2 * MIB, check)
        _pin(source, files[name + ".py"], C, 2 * MIB)
        verified[name] = source
    modules = {}
    try:
        for name in ORDER:
            check()
            need(name not in sys.modules, "LATE_PRELOADED_CUT_MODULE")
            path = root / (name + ".py")
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            modules[name] = module
            sys.modules[name] = module
            exec(compile(verified[name], str(path), "exec", dont_inherit=True), module.__dict__)
            need(sys.modules.get(name) is module and Path(module.__file__).absolute() == path,
                 "LOADED_SOURCE_BINDING")
        _graph(modules, A, E, S, C, P, PE)
        runtime, controller = modules["cut_runtime"], modules["cut_controller"]
        need(runtime.SCHEMA == SCHEMA and runtime.SOURCES == SOURCES and runtime.OBJECTS == OBJECTS,
             "RUNTIME_MANIFEST_CONTRACT")
        support = runtime.CutRuntime.open(root, expected_manifest_sha256, base, check=check)
        need(type(support) is runtime.CutRuntime and support.root == root and support.base is base and
             support.manifest_raw == raw and support.manifest_sha == expected_manifest_sha256 and
             support.support_id == hashlib.sha256(runtime.DOMAIN + raw).hexdigest(), "RUNTIME_BINDING")
        _graph(modules, A, E, S, C, P, PE)
        check()
        return SimpleNamespace(runtime=runtime, controller=controller, support=support)
    except BaseException:
        # Failed loading never leaves a superficially usable partial cut graph.
        for name, module in reversed(tuple(modules.items())):
            if sys.modules.get(name) is module:
                del sys.modules[name]
        raise
