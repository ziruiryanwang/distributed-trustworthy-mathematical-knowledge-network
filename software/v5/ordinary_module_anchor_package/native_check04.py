"""Five-call native-path successor integration; source-only until separately selected.

Reuse the retained synthetic owner and unchanged native installation in place.
No admission, extraction, helper build, peer binary or artifact corruption.
The old A and all three closed operations stay immutable; new support realizes fresh A.
Requires an enclosing finite Windows Job. Existing immutable evidence is retained.
"""
from __future__ import annotations

import time
BOOT_WALL, BOOT_CPU = time.monotonic(), time.process_time()
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OLD = ROOT/"experiments/v5-local-checks/ordinary-current-relocated-smoke-01-payload"
SAVED = ROOT/"experiments/v5-local-checks/ordinary-current-relocated-smoke-01/smoke"
REGISTRY = SAVED/"catalog/module-anchors-v1"
PYTHON = Path(r"D:\Python314\python.exe")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
HELPER = ROOT/"software/v5/ordinary_distribution/relocated_smoke.py"
HELPER_PIN = {"bytes": 38940, "sha256": "aaba6e2e30906414f539842fd7678aaaf3ab7f9c077b30c6f115db7407584831"}
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
CONTEXT = "03cb53c1e4f134e8acc404f2d92edb7f77a30810df74e9039f9fb59a6e92124f"
PARENT = "8c74aadc460b8efdbfedfa4f6a2468c93dc8c7b617b65870040cbbe22a0c2e8e"
STORE = "c60f943f157cccf4c4be478cc2b600b609f79e81084fda3eca691ef0ccbddfeb"
UNITS = ["25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3",
         "c4639e6e5f70e259ea1611adba8e168aa74dbfb91f98e2512cd465f82705e61e"]
EXPORTS = ["b5054e3c29436f1fe8d175b47df405405f76683d7c1e27531d9e597f2e55ee02",
           "bb47ce4786c4f5c22505952133e5220c0650452fb0006c83a395de131fee1355"]
PINS = {
    "IMMUTABLE-FILES.json": "c7f34a6b8b7303c239c38edef6362f49c332d14723e410d4ab0cd4aa388e092c",
    "catalog/ADOPTION.json": "6a1cbaf4edb1e74e1a27c34def157d64249c5a91eb822274c3bf5d4f11d399db",
    "fixtures/custody-limits.json": "abf5b2dc515a06691194c47e7a320a7fdeaedbbaa18ec45e074807649968ecbe",
    "module-contribution/RESULT.json": "c77d19c9c0035e7155db626d6234337396863ee6124a5adf1c5eee09a81b8b14",
}
CAPS = {"01-cold-A": (90, 50), "02-warm-B": (90, 50), "03-consumer": (35, 10),
        "04-reopen-reuse": (45, 8), "05-wrong-context": (45, 8)}
PRESERVED_ANCHOR = "08744de1cce786beec313017da1dea24921319a8996737d02a89c3dabc40bc55"
PRESERVED_SUPPORT = "6db6843068d2fcb3f15511f2e5ca2b79f94aeee00d19fa7b8d9764d37cb16596"
PRESERVED_OPERATIONS = {
    "f08b3ae81225416bbdbfe37f0ebeeea20e3628cf31696ee558622b2ed6b6733b",
    "2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b",
    "646b63d08513431d642eb8a73dc2724b7f4f59c3b2f7c588296034c26c990058",
}
PRESERVED_SIDECAR = {
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/CLOSED.json": {
        "bytes": 262,
        "sha256": "9ea0b40b9252a914799d1bc54bf53a33fca717229c2a7f42da139292565020ad"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/events/anchor-plan.json": {
        "bytes": 167,
        "sha256": "8d0d22b0d914a49b854b2962d6da5c8898b45d1f4032229722bff0fd4b787e6c"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/events/inventory.json": {
        "bytes": 823690,
        "sha256": "c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/events/native-report.json": {
        "bytes": 4836,
        "sha256": "686c6b53b6c2a174569d9d377158ad285dda6cb1a91ce5bc6fbdca236c4e5a24"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/events/native-report.json.pending": {
        "bytes": 4825,
        "sha256": "739a820815029600c0f71d0870a34a7864f120f627120930d9339b4588b59e02"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/events/native-report.json.phases.jsonl": {
        "bytes": 626,
        "sha256": "b08d7c398f68a2ea091dc174d0dc5f7a71c88df00be88bf3043a301a33327c53"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/events/request.json": {
        "bytes": 2911,
        "sha256": "c5cb5294bb812fa3587c82b8507b7a3f01e1169194e6f870e36d0721478dd47e"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/events/SUPERVISION.json": {
        "bytes": 2929,
        "sha256": "e6ee2772895febabc4af904c32cc93a673fe899135b4ac70b93ba94847c8bb1c"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/modules/DMKNBridge_1705759ee440d55396e5bdf0c78e153a64c9275453f61e5ef92f5c908946ef4c.ir": {
        "bytes": 1152,
        "sha256": "9f174435bb2bb65c1575996e4f385c79c52ba66a351e0cb77e1c9e9df22b1255"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/modules/DMKNBridge_1705759ee440d55396e5bdf0c78e153a64c9275453f61e5ef92f5c908946ef4c.ir.sig": {
        "bytes": 176,
        "sha256": "8b4cb3a33bdcc82c6845a42e83626d8b0d5806202d01ccd8e22f27a5bdca695c"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/modules/DMKNBridge_1705759ee440d55396e5bdf0c78e153a64c9275453f61e5ef92f5c908946ef4c.olean": {
        "bytes": 3128,
        "sha256": "f45fbd7ba0e5d6f5d0f7d9f247190bb73f13a9cb6314aa99dfa1d07ae830fbc7"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/modules/DMKNBridge_1705759ee440d55396e5bdf0c78e153a64c9275453f61e5ef92f5c908946ef4c.olean.private": {
        "bytes": 96,
        "sha256": "49a8c513f584222cc634eda9aa1c3b1fae8f16b28ee5464de3d42cd1fd394ae7"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/modules/DMKNBridge_1705759ee440d55396e5bdf0c78e153a64c9275453f61e5ef92f5c908946ef4c.olean.server": {
        "bytes": 96,
        "sha256": "92ed38256ea9b810d804c4e8feec6d472f23dc67167e4b19f2beeb9a81bef6e9"
    },
    "operations/2960f88a98821c1d0f5254364417442115c0df3587f1f72bf936dbe368358e2b/RESERVATION.json": {
        "bytes": 1141,
        "sha256": "944969854c405e50c8981355753efdfd3efdfbb850e2e1d8a9c82aa120dcea7e"
    },
    "operations/646b63d08513431d642eb8a73dc2724b7f4f59c3b2f7c588296034c26c990058/CLOSED.json": {
        "bytes": 246,
        "sha256": "19abb76522feb91713f530f9b3ff89ac74a4b9baa40e89f30ca35e5b33705154"
    },
    "operations/646b63d08513431d642eb8a73dc2724b7f4f59c3b2f7c588296034c26c990058/RESERVATION.json": {
        "bytes": 1217,
        "sha256": "5ea7ec72fbddd51c94858c722f33fd55e2e6a43989f9a62dff88d436945f4734"
    },
    "operations/f08b3ae81225416bbdbfe37f0ebeeea20e3628cf31696ee558622b2ed6b6733b/CLOSED.json": {
        "bytes": 246,
        "sha256": "707bbda28e33c83cb8cff88e994ebf82708d2f1afd203a5b15a244637c90ee2f"
    },
    "operations/f08b3ae81225416bbdbfe37f0ebeeea20e3628cf31696ee558622b2ed6b6733b/RESERVATION.json": {
        "bytes": 1141,
        "sha256": "f35d6f7775c7d583fd53b59216d465db30c018450f5beb610f3c80836a1ae560"
    },
    "records/08744de1cce786beec313017da1dea24921319a8996737d02a89c3dabc40bc55.json": {
        "bytes": 4771,
        "sha256": "045a9bffb24465aca3f42e68e993d200590140a4e8cd64af27b57bdc5421d313"
    },
    "STORE.json": {
        "bytes": 859,
        "sha256": "9a0b4e65b7e05b0d875d64f8b7d17a1519a02631aa4494902359db7299b2b513"
    }
}
MIB, CLEANUP_SECONDS, CONTROLLER_CPU_RESERVE = 1024**2, 20, 2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def helpers():
    with HELPER.open("rb") as stream:
        raw = stream.read(HELPER_PIN["bytes"]+1)
    need(len(raw) == HELPER_PIN["bytes"] and hashlib.sha256(raw).hexdigest() == HELPER_PIN["sha256"],
         "ANCHOR_CHECK_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_anchor_check_helpers", HELPER)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(HELPER), "exec"), module.__dict__)
    module.ordinary(HELPER)
    return module


def lean_worker(values):
    need(len(values) == 2, "ANCHOR_CHECK_LEAN_ARGUMENTS")
    h = helpers()
    source, imports = map(Path, values)
    h.ordinary(source); h.ordinary(imports)
    need(source.name == "Consumer.lean", "ANCHOR_CHECK_CONSUMER_SOURCE")
    directories = h.diagnostic_json(h.read(imports, 65536))
    need(type(directories) is list and len(directories) == 2 and
         len(set(directories)) == 2, "ANCHOR_CHECK_CONSUMER_IMPORTS")
    for value in directories:
        path = h.ordinary(value, directory=True)
        need(path.is_relative_to(REGISTRY/"operations") and path.name == "modules",
             "ANCHOR_CHECK_OWNED_IMPORTS")
    output = source.with_suffix(".olean"); h.ordinary(output, fresh=True)
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith(("LEAN", "PYTHON")) and k.upper() not in ("PATH", "VIRTUAL_ENV")}
    # Native path spelling only; returned directories and saved imports stay raw.
    need(all(re.match(r"^[A-Za-z]:\\", value) is not None for value in directories),
         "ANCHOR_CHECK_DRIVE_IMPORTS")
    env["LEAN_PATH"] = os.pathsep.join([str(LEAN/"lib/lean"), *("\\\\?\\"+value for value in directories)])
    env["PATH"] = os.pathsep.join((str(PYTHON.parent), str(LEAN/"bin")))
    return subprocess.call([str(LEAN/"bin/lean.exe"), "-DElab.async=false", "-R", str(source.parent),
        "-o", str(output), str(source)], cwd=source.parent, env=env, stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW)


class Check:
    def __init__(self, args, h):
        self.args, self.h = args, h
        self.started, self.cpu_started = BOOT_WALL, BOOT_CPU
        self.deadline = self.started+args.wall_seconds
        self.charged, self.cpu_complete = 0.0, True
        self.calls, self.held = [], {}
        self.output_created = False

    def check(self):
        need(time.monotonic() < self.deadline and time.process_time()-self.cpu_started+
             self.charged < self.args.cpu_seconds, "ANCHOR_CHECK_ORIGINAL_ALLOWANCE")

    def hold(self, path, expected=None):
        pin = self.h.pin(path, self.check)
        need(expected is None or pin == expected, "ANCHOR_CHECK_EXACT_PIN:"+str(path))
        need(self.held.setdefault(str(path), pin) == pin, "ANCHOR_CHECK_IMMUTABLE_CHANGED")
        return pin

    def document(self, path, maximum=8*MIB):
        self.check()
        return self.h.diagnostic_json(self.h.read(path, maximum))

    def save(self, path, value):
        return self.hold(path, self.h.save(path, value))

    def tree(self, root):
        # Only the frozen bounded walk is reused, not its campaign or preparation.
        return self.h.Smoke.capture_tree(self, root)

    def prepare(self):
        h, args = self.h, self.args
        self.package = h.ordinary(args.package, directory=True)
        self.output = h.ordinary(args.output, directory=True, fresh=True)
        need(self.output.is_relative_to(ROOT/"experiments/v5-local-checks") and
             Path(args.python_runtime) == PYTHON.parent and Path(args.lean_runtime) == LEAN,
             "ANCHOR_CHECK_SELECTED_PATHS")
        self.runtimes = {"python_runtime": h.ordinary(PYTHON.parent, directory=True),
                         "lean_runtime": h.ordinary(LEAN, directory=True)}
        roots = [self.package, self.output, OLD, SAVED, *self.runtimes.values()]
        need(all(not a.is_relative_to(b) and not b.is_relative_to(a)
                 for i, a in enumerate(roots) for b in roots[i+1:]), "ANCHOR_CHECK_DISJOINT_ROOTS")
        self.script = h.ordinary(Path(__file__).resolve())
        self.hold(self.script); self.hold(HELPER, HELPER_PIN)
        need(re.fullmatch(r"[0-9a-f]{64}", args.profile_sha256), "ANCHOR_CHECK_PROFILE_HASH")
        raw = h.read(self.package/"PROFILE.json", 2*MIB)
        need(h.sha(raw) == args.profile_sha256, "ANCHOR_CHECK_PROFILE_PIN")
        self.profile = h.diagnostic_json(raw)
        need(set(self.profile) == {"schema", "files", "installation_manifest_sha256", "helper_paths", "author_worker"}
             and self.profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
             self.profile["helper_paths"] == ["authoring/helpers"] and
             self.profile["author_worker"] == "author_worker.py" and
             self.profile["installation_manifest_sha256"] == INSTALLATION, "ANCHOR_CHECK_PROFILE_LAYOUT")
        manifest_raw = h.read(self.package/"installation/INSTALLATION.json", 2*MIB)
        need(manifest_raw == h.read(OLD/"installation/INSTALLATION.json", 2*MIB) and
             h.sha(manifest_raw) == INSTALLATION, "ANCHOR_CHECK_UNCHANGED_INSTALLATION")
        self.manifest = h.diagnostic_json(manifest_raw)
        need(self.manifest["schema"] == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1" and
             h.identity("DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1", h.canonical(self.manifest["implementation"])) == IMPLEMENTATION
             and self.manifest["implementation"]["semantic_id"] == SEMANTIC, "ANCHOR_CHECK_IMPLEMENTATION")
        package_pins = dict(self.profile["files"])
        installation_files = {"INSTALLATION.json"}
        for logical, expected in self.manifest["files"].items():
            parts = h.relative(logical).parts
            if parts[0] in self.runtimes:
                self.hold(self.runtimes[parts[0]].joinpath(*parts[1:]), expected)
            else:
                installation_files.add(logical)
                package_pins["installation/"+logical] = expected
                self.hold(OLD/"installation"/h.relative(logical), expected)
        package_pins["installation/INSTALLATION.json"] = {"bytes": len(manifest_raw), "sha256": INSTALLATION}
        package_pins["PROFILE.json"] = {"bytes": len(raw), "sha256": args.profile_sha256}
        # This assembler places its non-imported receipt beside PROFILE. Bind
        # exactly the selected receipt; do not ignore arbitrary extra files.
        need(re.fullmatch(r"[0-9a-f]{64}", args.assembly_sha256), "ANCHOR_CHECK_ASSEMBLY_HASH")
        assembly_raw = h.read(self.package/"ASSEMBLY.json", 2*MIB)
        need(h.sha(assembly_raw) == args.assembly_sha256, "ANCHOR_CHECK_ASSEMBLY_PIN")
        assembly = h.diagnostic_json(assembly_raw)
        changed, added = {"module/OrdinaryModule.lean"}, set()
        need(assembly["status"] == "ASSEMBLED_NOT_ADOPTED" and
             assembly["profile_sha256"] == args.profile_sha256 and
             assembly["claim"] == "ONE_PAYLOAD_NATIVE_PATH_GUARD_NO_NATIVE_OWNER_OR_STATE_OPERATION" and
             assembly["base_profile_sha256"] == "68fbcb5c5edba0be55e236a561af0fe2a6d1a1df7229e95ca8af75d09d0f4de0" and
             assembly["installation_manifest_sha256"] == INSTALLATION and
             assembly["implementation_id"] == IMPLEMENTATION and assembly["files_excluding_profile"] == 134 and
             set(assembly["changed"]) == changed and set(assembly["added"]) == added and
             assembly["changed_or_added"] == {name: package_pins[name] for name in changed | added},
             "ANCHOR_CHECK_ASSEMBLY_BINDING")
        package_pins["ASSEMBLY.json"] = {"bytes": len(assembly_raw), "sha256": args.assembly_sha256}
        need(1 <= len(package_pins) <= 512 and len({p.casefold() for p in package_pins}) == len(package_pins),
             "ANCHOR_CHECK_PACKAGE_CENSUS")
        for logical, expected in package_pins.items():
            self.hold(self.package/h.relative(logical), expected)
        need(self.tree(OLD/"installation") == installation_files and
             self.tree(self.package/"installation") == installation_files and
             self.tree(self.package) == set(package_pins), "ANCHOR_CHECK_EXACT_PACKAGE_TREES")
        for logical, digest in PINS.items():
            need(self.hold(SAVED/h.relative(logical))["sha256"] == digest, "ANCHOR_CHECK_RETAINED_PIN")
        retained = self.document(SAVED/"IMMUTABLE-FILES.json")
        need(type(retained) is dict and len(retained) == 252, "ANCHOR_CHECK_PRIOR_IMMUTABLE_CENSUS")
        for path, pin in retained.items():
            self.hold(h.ordinary(path), pin)
        adoption = self.document(SAVED/"catalog/ADOPTION.json")
        need(adoption["store_id"] == STORE and adoption["implementation"] == self.manifest["implementation"],
             "ANCHOR_CHECK_EXISTING_ADOPTION")
        names = ["CommonsPackageExample.applyTwice", "CommonsPackageExample.applyTwice_eq"]
        self.targets = [{"name": h.name(n), "unit_id": u, "export_id": e} for n, u, e in zip(names, UNITS, EXPORTS)]
        result = self.document(SAVED/"module-contribution/RESULT.json")
        need(result["local_root"] == CONTEXT and result["parent_root"] == PARENT and
             result["targets"] == self.targets and [r["unit_id"] for r in result["units"]] == UNITS,
             "ANCHOR_CHECK_RETAINED_ACCEPTANCE")
        self.evidence = []
        for row in result["units"]:
            path = SAVED/"module-contribution/evidence"/(row["unit_id"]+".json")
            self.hold(path, {k: row[k] for k in ("bytes", "sha256")})
            evidence_raw = h.read(path)
            need(h.identity("DMKN-ORDINARY-EVIDENCE-V2", evidence_raw) == row["unit_id"], "ANCHOR_CHECK_EVIDENCE_ID")
            self.evidence.append(h.diagnostic_json(evidence_raw))
        # Preserve exact audited native01/native02 state, including successful A,
        # all three closed operations, reservations, artifacts and diagnostics.
        # The old support's A is NOT reused across the changed importer boundary.
        for logical, pin in PRESERVED_SIDECAR.items():
            self.hold(REGISTRY/h.relative(logical), pin)
        need(self.tree(REGISTRY) == set(PRESERVED_SIDECAR) and
             {p.name for p in (REGISTRY/"records").iterdir()} == {PRESERVED_ANCHOR+".json"} and
             {p.name for p in (REGISTRY/"operations").iterdir()} == PRESERVED_OPERATIONS,
             "ANCHOR_CHECK_EXACT_PRESERVED_SIDECAR")
        roles = self.manifest["roles"]
        def helper(role, module, digest):
            logical = roles[role]
            need(logical.startswith("supervisor/") and self.manifest["files"][logical]["sha256"] == digest,
                 "ANCHOR_CHECK_SUPERVISOR_PIN")
            return h.load_exact(self.package/"installation"/h.relative(logical), module,
                                self.manifest["files"][logical], self.check)
        self.supervisor = helper("supervisor", "_anchor_check_supervisor",
            "6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9")
        helper("domains", "domains", "651db5f6bb707159c0d29dd6092174bfcebd1dc17b833fdfdacf7e2a66d8522a")
        self.jobs = helper("job", "_anchor_check_job", "bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028")
        self.output.mkdir(); self.output_created = True
        for directory in ("fixtures", "calls", "consumer"):
            (self.output/directory).mkdir()
        self.save(self.output/"SELECTION.json", {"package": str(self.package), "profile_sha256": args.profile_sha256,
            "installation_manifest_sha256": INSTALLATION, "context_root": CONTEXT, "store_id": STORE,
            "original_allowance": vars(args), "call_caps": CAPS, "cleanup_seconds": CLEANUP_SECONDS,
            "scope": "REUSED_SYNTHETIC_OWNER_TWO_LOCAL_MODULES_NO_ADMISSION_OR_REBUILD",
            "preserved_anchor": PRESERVED_ANCHOR, "preserved_operations": sorted(PRESERVED_OPERATIONS),
            "preserved_sidecar": PRESERVED_SIDECAR})
        for i, label in enumerate(("A", "B")):
            self.save(self.output/"fixtures"/(label+".json"), [self.targets[i]])

    def call(self, label, argv_for_grant, *, expected_exit=0, public=True):
        self.check()
        need(label in CAPS and not any(e["label"] == label for e in self.calls), "ANCHOR_CHECK_SINGLE_CALL")
        wall, cpu = CAPS[label]
        grant = self.supervisor.limits_checked({
            "wall_seconds": min(wall, math.floor(self.deadline-time.monotonic())-CLEANUP_SECONDS),
            "cpu_seconds": min(cpu, math.floor(self.args.cpu_seconds-self.charged-
                (time.process_time()-self.cpu_started))-CONTROLLER_CPU_RESERVE),
            "memory_mib": self.args.memory_mib, "active_processes": 8,
            "stdout_bytes": 8*MIB, "stderr_bytes": 8*MIB})
        need(grant["wall_seconds"] >= (15 if not public else 40) and grant["cpu_seconds"] >= 3,
             "ANCHOR_CHECK_REMAINING_GRANT")
        argv = argv_for_grant(grant)
        event = {"label": label, "argv": argv, "cwd": str(self.output), "limits": grant,
                 "expected_exit": expected_exit, "cpu_complete": False, "charged_cpu_seconds": grant["cpu_seconds"]}
        self.calls.append(event)
        supervision = None
        try:
            supervision = self.supervisor.supervise(argv, self.output, self.output/"calls"/label, grant, self.jobs.Job)
            event["supervision"] = supervision
        except BaseException as error:
            event["supervision_exception"] = {"type": type(error).__name__, "error": str(error)[:2000]}
            raise
        finally:
            final = supervision.get("final_job") if type(supervision) is dict else None
            observed = final.get("cpu_seconds") if type(final) is dict else None
            known = type(observed) in (int, float) and math.isfinite(observed) and observed >= 0
            charged = observed if known else grant["cpu_seconds"]
            self.charged += charged; self.cpu_complete = self.cpu_complete and known
            event.update(cpu_complete=known, charged_cpu_seconds=charged)
            self.h.save(self.output/"calls"/(label+"-SUPERVISION.json"), event)
        need(known, "ANCHOR_CHECK_UNKNOWN_CPU_FULL_GRANT_CHARGED")
        self.h.clean(supervision, exit_code=expected_exit)
        need(self.h.read(self.output/"calls"/label/"stderr.txt", MIB) == b"", "ANCHOR_CHECK_CHILD_STDERR")
        raw = self.h.read(self.output/"calls"/label/"stdout.txt", 8*MIB)
        self.check()
        if not public:
            need(raw == b"", "ANCHOR_CHECK_CONSUMER_STDOUT")
            return None
        result = self.h.diagnostic_json(raw)
        need(result.get("ok") is (expected_exit == 0) and not result.get("close_errors"), "ANCHOR_CHECK_PUBLIC_STATUS")
        return result

    def export(self, label, target, *, anchor="", context=CONTEXT, reject=False):
        directory = self.output/label
        def argv(grant):
            values = [str(PYTHON), "-I", "-S", "-B", str(self.package/"owner.py"), "export-module",
                "--profile-sha256", self.args.profile_sha256, "--python-runtime", str(PYTHON.parent),
                "--lean-runtime", str(LEAN), "--wall-seconds", str(grant["wall_seconds"]-5),
                "--cpu-seconds", str(grant["cpu_seconds"]-1), "--memory-mib", str(self.args.memory_mib),
                "--catalog", str(SAVED/"catalog"), "--custody", str(SAVED/"custody"), "--store-id", STORE,
                "--custody-limits", str(SAVED/"fixtures/custody-limits.json"), "--parent-root", context,
                "--module-targets", str(self.output/"fixtures"/(target+".json")), "--output", str(directory)]
            return values+(["--module-anchor", anchor] if anchor else [])
        public = self.call(label, argv, expected_exit=1 if reject else 0)
        need(public["operation"] == "export-module", "ANCHOR_CHECK_OPERATION")
        if reject:
            need(public["phase"] == "EXPORT_MODULE" and public["detail"]["phase"] == "ANCHOR" and
                 public["detail"]["error"] == "ANCHOR_CURRENT_CONTEXT_MISMATCH" and
                 public["detail"]["native_cpu_seconds"] == 0 and public["cost"]["worker_cpu_seconds"] == 0 and
                 public["accepted"] is None and not directory.exists(), "ANCHOR_CHECK_EARLY_CONTEXT_REFUSAL")
            return public
        need(public["profile_sha256"] == self.args.profile_sha256 and public["implementation_id"] == IMPLEMENTATION and
             public["store_id"] == STORE and public["catalog"] == str(SAVED/"catalog") and
             public["custody"] == str(SAVED/"custody"), "ANCHOR_CHECK_PUBLIC_OWNER")
        result = public["result"]
        manifest = self.document(directory/"MODULE.json")
        need({k: v for k, v in result.items() if k not in ("manifest_path", "supported_runtime")} == manifest and
             result["manifest_path"] == str(directory/"MODULE.json") and
             result["source_context_root"] == context and result["semantic_id"] == SEMANTIC and
             result["targets"] == [self.targets[0 if target == "A" else 1]] and
             result["new_catalog_acceptance"] is False, "ANCHOR_CHECK_SAVED_RESULT")
        runtime = result["supported_runtime"]
        need(runtime["implementation_id"] == IMPLEMENTATION and runtime["installation_manifest_sha256"] == INSTALLATION and
             runtime["lean_runtime"] == str(LEAN) and runtime["lean_executable"] == str(LEAN/"bin/lean.exe") and
             runtime["lean_executable_pin"] == self.manifest["files"][self.manifest["roles"]["lean"]],
             "ANCHOR_CHECK_RETURNED_RUNTIME")
        return result

    def checked(self, result, label, index, parent=None):
        h, directory = self.h, self.output/label
        expected_cut = [] if parent is None else [UNITS[0]]
        parent_id = "" if parent is None else parent["anchor_id"]
        need(result["status"] == "CHECKED_AND_REGISTERED_LOCAL_MODULE_ANCHOR" and
             result["parent_anchor_id"] == parent_id and result["ordered_unit_ids"] == [UNITS[index]] and
             result["cut_unit_ids"] == expected_cut and result["fetch_calls"] == result["native_calls"] == 1 and
             result["units_checked"] == 1 and result["units_matched"] == 0 and result["matched_names"] == [] and
             result["added_names"] == [self.targets[index]["name"]], "ANCHOR_CHECK_RESIDUAL_DELTA")
        request, selection = self.document(directory/"request.json"), self.document(directory/"SELECTION.json")
        plan_raw = h.read(directory/"anchor-plan.json", 4*MIB)
        plan = h.diagnostic_json(plan_raw)
        need(request["schema"] == "DMKN_ORDINARY_MODULE_REQUEST_V2" and request["anchor_id"] == parent_id and
             request["anchor_plan_sha256"] == h.sha(plan_raw) and request["unit_ids"] == [UNITS[index]] and
             request["units"] == [self.evidence[index]["unit"]] and request["context_root"] == CONTEXT and
             request["targets"] == [self.targets[index]["name"]] and
             selection["fetch_calls"] == 1 and selection["cut_unit_ids"] == expected_cut,
             "ANCHOR_CHECK_OLD_INVENTORY_NOT_IN_DELTA")
        for role in ("request", "inventory", "anchor_plan"):
            filename = "anchor-plan.json" if role == "anchor_plan" else role+".json"
            self.hold(directory/filename, selection["input_pins"][role])
        need(plan["schema"] == "DMKN_LOCAL_MODULE_ANCHOR_PLAN_V1" and plan["anchor_id"] == parent_id and
             len(plan["modules"]) == index and [r["unit_id"] for r in plan["bindings"]] == UNITS[:index],
             "ANCHOR_CHECK_PARENT_PLAN")
        direct = [h.name("Init" if parent is None else parent["module_name"])]
        if parent is not None:
            row = plan["modules"][0]
            need(row["anchor_id"] == parent_id and row["module_name"] == h.name(parent["module_name"]) and
                 row["direct_imports"] == [h.name("Init")] and row["added_names"] == [self.targets[0]["name"]] and
                 [p["path"] for p in row["artifact_parts"]] ==
                 [str(Path(parent["module_directory"])/(parent["module_name"]+s)) for s in h.PARTS],
                 "ANCHOR_CHECK_EXACT_PARENT_ARTIFACT_PLAN")
        support_id = selection["key_input"]["support_id"]
        need(re.fullmatch(r"[0-9a-f]{64}", support_id) and support_id != PRESERVED_SUPPORT and
             result["anchor_id"] != PRESERVED_ANCHOR, "ANCHOR_CHECK_FRESH_IMPORTER_SUPPORT")
        if parent is None:
            self.new_support = support_id
        else:
            need(support_id == self.new_support, "ANCHOR_CHECK_SAME_NEW_SUPPORT")
        key = h.identity("DMKN-ORDINARY-ANCHORED-MODULE-V1", h.canonical(selection["key_input"]))
        need(result["cache_key"] == selection["cache_key"] == key and result["module_name"] == "DMKNBridge_"+key,
             "ANCHOR_CHECK_MATERIALIZATION_KEY")
        native = self.document(directory/"SUPERVISION.json"); h.clean(native)
        need(native["argv"][4] == str(self.package/"module_worker.py") and
             native["argv"][6] == str(self.package/"module/OrdinaryModule.lean") and
             native["final_job"]["cpu_seconds"] == result["native_cpu_seconds"] and
             h.read(directory/"supervision/stderr.txt", MIB) == b"", "ANCHOR_CHECK_NATIVE_CLOSURE")
        report_raw = h.read(directory/"native-report.json", 8*MIB)
        report = h.diagnostic_json(report_raw)
        rows = self.evidence[index]["unit"][2]
        need(h.sha(report_raw) == result["report_sha256"] and report["schema"] == "DMKN_ORDINARY_MODULE_OUTPUT_V3" and
             report["checking_passes"] == 2 and report["basis_rows"] == 581 and
             all(report[k] == request[k] for k in ("semantic_id", "context_root", "foundation_id", "module_name",
                 "targets", "unit_ids", "anchor_id", "anchor_plan_sha256")) and report["direct_imports"] == direct and
             report["anchor_names"] == [t["name"] for t in self.targets[:index]] and
             report["inventories"] == report["added_inventories"] == rows and report["matched_inventories"] == [],
             "ANCHOR_CHECK_BOTH_VIEWS_EXACT_DELTA")
        phases = [h.diagnostic_json(line) for line in h.read(directory/"native-report.json.phases.jsonl").splitlines()]
        need([(r["phase"], r["event"], r["exit_code"]) for r in phases] ==
             [(phase, event, code) for phase in ("build", "reread-private", "reread-exported")
              for event, code in (("STARTED", None), ("EXITED", 0))], "ANCHOR_CHECK_FRESH_TWO_VIEW_REREADS")
        owned = h.ordinary(result["module_directory"], directory=True)
        expected_imports = ([] if parent is None else parent["import_directories"])+[str(owned)]
        need(owned.is_relative_to(REGISTRY/"operations") and owned.name == "modules" and
             owned != directory/"modules" and result["import_directories"] == expected_imports and
             set(result["artifact_parts"]) == {result["module_name"]+suffix for suffix in h.PARTS},
             "ANCHOR_CHECK_OWNED_RETURNED_DIRECTORIES")
        for filename, pin in result["artifact_parts"].items():
            self.hold(directory/"modules"/filename, pin); self.hold(owned/filename, pin)
        record_path = REGISTRY/"records"/(result["anchor_id"]+".json")
        record_raw = h.read(record_path)
        need(h.identity("DMKN-LOCAL-MODULE-ANCHOR-V1", record_raw) == result["anchor_id"], "ANCHOR_CHECK_REGISTERED_ADDRESS")
        record = h.diagnostic_json(record_raw)
        need(record["parent_anchor_id"] == parent_id and record["direct_imports"] == direct and
             record["module_name"] == request["module_name"] and
             [u["unit_id"] for u in record["units"]] == [UNITS[index]], "ANCHOR_CHECK_REGISTERED_DELTA")
        self.hold(record_path)

    def run(self, report):
        report["phase"] = "COLD_A"
        a = self.export("01-cold-A", "A"); self.checked(a, "01-cold-A", 0)
        report["phase"] = "WARM_B"
        b = self.export("02-warm-B", "B", anchor=a["anchor_id"]); self.checked(b, "02-warm-B", 1, a)
        report.update(anchor_a=a["anchor_id"], anchor_b=b["anchor_id"])
        report["phase"] = "ORDINARY_CONSUMER"
        source, imports = self.output/"consumer/Consumer.lean", self.output/"consumer/imports.json"
        self.save(source, self.h.consumer_source(b["module_name"]))
        self.save(imports, b["import_directories"])
        self.call("03-consumer", lambda grant: [str(PYTHON), "-I", "-S", "-B", str(self.script),
            "--lean-worker", str(source), str(imports)], public=False)
        for suffix in self.h.PARTS:
            need(self.hold(source.parent/(source.stem+suffix))["bytes"] > 0, "ANCHOR_CHECK_CONSUMER_FIVE_PARTS")
        registry_files = self.tree(REGISTRY)
        need({p.name for p in (REGISTRY/"records").iterdir()} ==
             {PRESERVED_ANCHOR+".json", a["anchor_id"]+".json", b["anchor_id"]+".json"} and
             {p.name for p in (REGISTRY/"operations").iterdir()} == PRESERVED_OPERATIONS |
             {Path(a["module_directory"]).parent.name, Path(b["module_directory"]).parent.name},
             "ANCHOR_CHECK_EXACT_TWO_NEW_REGISTRATIONS")
        report["phase"] = "REOPEN_ALL_ANCHORED"
        reused = self.export("04-reopen-reuse", "B", anchor=b["anchor_id"])
        need(reused["status"] == "REUSED_LOCAL_MODULE_ANCHOR" and
             all(reused[k] == b[k] for k in ("anchor_id", "cache_key", "module_name", "module_directory", "import_directories")) and
             reused["ordered_unit_ids"] == [] and reused["cut_unit_ids"] == [UNITS[1]] and
             reused["fetch_calls"] == reused["native_calls"] == reused["native_cpu_seconds"] == 0 and
             {p.name for p in (self.output/"04-reopen-reuse").iterdir()} == {"MODULE.json"},
             "ANCHOR_CHECK_ZERO_NATIVE_REOPEN_REUSE")
        need(self.tree(REGISTRY) == registry_files, "ANCHOR_CHECK_NO_REUSE_REGISTRATION_OR_MUTATION")
        report["phase"] = "WRONG_CONTEXT"
        self.export("05-wrong-context", "B", anchor=b["anchor_id"], context=PARENT, reject=True)
        need(self.tree(REGISTRY) == registry_files, "ANCHOR_CHECK_REFUSAL_PRESERVES_REGISTRY")
        report["phase"] = "FINAL_PRESERVATION"
        for path, expected in tuple(self.held.items()):
            self.hold(Path(path), expected)
        need(len(self.calls) == 5 and all(c["cpu_complete"] for c in self.calls), "ANCHOR_CHECK_FINITE_CALL_CENSUS")
        self.h.save(self.output/"IMMUTABLE-FILES.json", self.held)
        report.update(status="PASS_LOCAL_MODULE_ANCHOR_DELTA_USE_REOPEN", phase="COMPLETE",
            immutable_files=len(self.held), registry_files=len(registry_files),
            old_inventory_replayed_in_warm_request=False, warm_evidence_fetches=1,
            native_module_calls=2, ordinary_consumer_calls=1, reused_native_calls=0)


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize and Path(sys.executable).resolve() == PYTHON, "ANCHOR_CHECK_PYTHON_PROFILE")
    if sys.argv[1:2] == ["--lean-worker"]:
        return lean_worker(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "profile-sha256", "assembly-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+key, required=True)
    for key in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+key, required=True, type=int)
    args = parser.parse_args()
    need(180 <= args.wall_seconds <= 260 and 100 <= args.cpu_seconds <= 160 and
         256 <= args.memory_mib <= 1536, "ANCHOR_CHECK_ORIGINAL_FINITE_ENVELOPE")
    check = Check(args, helpers())
    report = {"status": "FAILED", "phase": "PREFLIGHT", "calls": check.calls,
        "claim": "LOCAL_INCREMENTAL_REUSE_NOT_COLD_SUCCINCT_VERIFICATION_OR_GROWTH_OR_FINAL_V5",
        "retention": "ALL_PRIOR_AND_PARTIAL_OUTPUTS_PRESERVED_NO_RETRY"}
    try:
        check.prepare(); check.run(report)
    except BaseException as error:
        report.update(status="FAILED", error_type=type(error).__name__, error=str(error)[:2000],
            immutable_preservation="POST_FAILURE_SAVED_FILE_AUDIT_REQUIRED_NO_RENEWED_ALLOWANCE")
    finally:
        report.update(wall_seconds=time.monotonic()-check.started,
            controller_cpu_seconds=time.process_time()-check.cpu_started,
            inclusive_child_job_cpu_charged=check.charged, child_cpu_complete=check.cpu_complete,
            accounting="CHILD_JOB_CPU_ONCE_NO_NESTED_DOUBLE_CHARGE_UNKNOWN_FULL_GRANT_THEN_STOP_OUTER_JOB_AUTHORITATIVE")
        if (not check.cpu_complete or report["wall_seconds"] >= args.wall_seconds or
                report["controller_cpu_seconds"]+check.charged >= args.cpu_seconds):
            report.update(status="FAILED", budget_or_cleanup_error="ANCHOR_CHECK_ORIGINAL_ALLOWANCE_OR_CLOSURE")
        if check.output_created:
            check.h.save(check.output/"NATIVE-CHECK-RESULT.json", report)
    print(json.dumps({"status": report["status"], "phase": report["phase"]}, sort_keys=True), flush=True)
    return 0 if report["status"] == "PASS_LOCAL_MODULE_ANCHOR_DELTA_USE_REOPEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
