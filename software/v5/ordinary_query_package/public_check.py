"""Seven-call public query/discovery/export/use check; source-only until selected.

Requires root's exact package/profile selection and enclosing finite Windows Job.
Reopens only the retained synthetic owner. No admission, state copy, command
rebuild, proof campaign, automatic retry or useful-growth claim is authorized.
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
import threading

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OLD = ROOT/"experiments/v5-local-checks/ordinary-current-relocated-smoke-01-payload"
SAVED = ROOT/"experiments/v5-local-checks/ordinary-current-relocated-smoke-01/smoke"
OUTPUT = ROOT/"experiments/v5-local-checks/ordinary-query-public-01/public"
PYTHON = Path(r"D:\Python314\python.exe")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
HELPER = ROOT/"software/v5/ordinary_distribution/relocated_smoke.py"
HELPER_PIN = {"bytes": 38940, "sha256": "aaba6e2e30906414f539842fd7678aaaf3ab7f9c077b30c6f115db7407584831"}
INSTALLATION = "32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
CONTEXT = "94827b21912710d45d0a459d089b741d39a15caf9b60847b5f0553be7457cece"
PARENT = "8c74aadc460b8efdbfedfa4f6a2468c93dc8c7b617b65870040cbbe22a0c2e8e"
STORE = "c60f943f157cccf4c4be478cc2b600b609f79e81084fda3eca691ef0ccbddfeb"
UNITS = ["2951fcf2eb813a9c4472c8a58f6ff51d1389363f9c2d2cace207ca28319887ae",
         "6f0a5a17f40dbca4e4f0eabb86c6d6a2dfd0eeb0056d36e81373a2e185cd51c8"]
EXPORT = "ff50a5653b4cfd7c9ff2dac8c5403fcce66251bcabb5e05f9a8574871b51c093"
ANCHORS = {
    "IMMUTABLE-FILES.json": "c7f34a6b8b7303c239c38edef6362f49c332d14723e410d4ab0cd4aa388e092c",
    "SMOKE-RESULT.json": "e1d0aac60245722d73ffe21fc2961fc52bf5216931c09d8eccbfb7b18c37301f",
    "completion/RESULT.json": "60cf12bd8b954a2a61a7d8a2aeb006e4ea9bdee087a8846de3eec1e39224bf79",
    "complete/command.json": "6be77385211ca106a85af1cc1e2eec80d939e6d9fc2483aad6d27291ff192e7c",
    "catalog/ADOPTION.json": "6a1cbaf4edb1e74e1a27c34def157d64249c5a91eb822274c3bf5d4f11d399db",
    "fixtures/custody-limits.json": "abf5b2dc515a06691194c47e7a320a7fdeaedbbaa18ec45e074807649968ecbe",
}
BINDINGS = [
    ("Eq", "80b9689fa00451ea0cb456c6e822415c8ca66d4d0cd6a47c890c84371a59d6d5"),
    ("Nat.zero", "ea54d1998d3fd8cec06155ef7bdc70690bb898be6faea2ce18243c32cfab82c9"),
    ("Nat.add", "b6e338b03825275ae69439503bc2266eb3c691e511a0036b6ad92b696330a63b"),
    ("Nat", "ca48e6ac6a5c8bfe6df0d8156961a55a1f3aec59783b8f31b5fd2e0c151eace2"),
]
INDEX_LIMITS = {"max_objects": 32, "max_postings": 4096, "max_features": 512,
    "max_snapshots": 33, "max_logical_bytes": 16777216, "max_db_pages": 4096}
CAPS = {"01-query-local": (35, 15), "02-query": (45, 10), "03-publish": (45, 10),
        "04-serve": (45, 8), "05-find": (45, 8), "06-export": (75, 40), "07-consumer": (35, 10)}
MIB, CLEANUP_SECONDS, CONTROLLER_CPU_RESERVE = 1024**2, 25, 2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def helpers():
    # Only this retained test helper is imported outside the selected package.
    # Its pure functions are reused; Smoke.prepare/run are NEVER invoked.
    with HELPER.open("rb") as stream:
        raw = stream.read(HELPER_PIN["bytes"]+1)
    need(len(raw) == HELPER_PIN["bytes"] and hashlib.sha256(raw).hexdigest() == HELPER_PIN["sha256"],
         "PUBLIC_CHECK_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_query_check_helpers", HELPER)
    module = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(HELPER), "exec"), module.__dict__)
    module.ordinary(HELPER)
    return module


def lean_worker(values):
    need(len(values) == 4, "PUBLIC_CHECK_LEAN_WORKER_ARGUMENTS")
    h = helpers()
    runtime, modules, source = map(Path, values[:3])
    purpose = values[3]
    h.ordinary(runtime, directory=True); h.ordinary(modules, directory=True); h.ordinary(source)
    need(runtime == LEAN and purpose in ("query", "consumer") and
         source.name == ("NatRightIdentityQuery.lean" if purpose == "query" else "Consumer.lean"),
         "PUBLIC_CHECK_LEAN_WORKER_SCOPE")
    output = source.with_suffix(".olean"); h.ordinary(output, fresh=True)
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith(("LEAN", "PYTHON")) and k.upper() not in ("PATH", "VIRTUAL_ENV")}
    env["LEAN_PATH"] = os.pathsep.join((str(runtime/"lib/lean"), str(modules)))
    env["PATH"] = os.pathsep.join((str(PYTHON.parent), str(runtime/"bin")))
    return subprocess.call([str(runtime/"bin/lean.exe"), "-DElab.async=false", "-R", str(source.parent),
        "-o", str(output), str(source)], cwd=source.parent, env=env, stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW)


class Check:
    def __init__(self, args, h):
        self.args, self.h = args, h
        self.started, self.cpu_started = BOOT_WALL, BOOT_CPU
        self.deadline = self.started+args.wall_seconds
        self.charged, self.reserved, self.cpu_complete = 0.0, 0.0, True
        self.calls, self.held, self.threads = [], {}, {}
        self.output_created = False

    def check(self):
        need(time.monotonic() < self.deadline and time.process_time()-self.cpu_started+
             self.charged+self.reserved < self.args.cpu_seconds, "PUBLIC_CHECK_ORIGINAL_ALLOWANCE")

    def hold(self, path, expected=None):
        pin = self.h.pin(path, self.check)
        need(expected is None or pin == expected, "PUBLIC_CHECK_EXACT_PIN:"+str(path))
        need(self.held.setdefault(str(path), pin) == pin, "PUBLIC_CHECK_IMMUTABLE_CHANGED")
        return pin

    def document(self, path, maximum=8*MIB):
        self.check()
        return self.h.diagnostic_json(self.h.read(path, maximum))

    def save(self, path, value):
        return self.hold(path, self.h.save(path, value))

    def tree(self, root):
        # Reuse the bounded, redirect-refusing walk, not the smoke workflow.
        return self.h.Smoke.capture_tree(self, root)

    def prepare(self):
        h, args = self.h, self.args
        self.package = h.ordinary(args.package, directory=True)
        self.output = h.ordinary(args.output, directory=True, fresh=True)
        need(self.output == OUTPUT and Path(args.python_runtime) == PYTHON.parent and
             Path(args.lean_runtime) == LEAN, "PUBLIC_CHECK_SELECTED_PATHS")
        self.runtimes = {"python_runtime": h.ordinary(PYTHON.parent, directory=True),
                         "lean_runtime": h.ordinary(LEAN, directory=True)}
        roots = [self.package, self.output, OLD, SAVED, *self.runtimes.values()]
        need(all(not a.is_relative_to(b) and not b.is_relative_to(a)
                 for i, a in enumerate(roots) for b in roots[i+1:]), "PUBLIC_CHECK_DISJOINT_ROOTS")
        self.script = h.ordinary(Path(__file__).resolve())
        self.hold(self.script); self.hold(HELPER, HELPER_PIN)
        need(re.fullmatch(r"[0-9a-f]{64}", args.profile_sha256), "PUBLIC_CHECK_PROFILE_HASH")
        raw = h.read(self.package/"PROFILE.json", 2*MIB)
        need(h.sha(raw) == args.profile_sha256, "PUBLIC_CHECK_PROFILE_PIN")
        self.profile = h.diagnostic_json(raw)
        need(set(self.profile) == {"schema", "files", "installation_manifest_sha256", "helper_paths", "author_worker"}
             and self.profile["schema"] == "DMKN_ORDINARY_OWNER_PROFILE_V1" and
             self.profile["helper_paths"] == ["authoring/helpers"] and
             self.profile["author_worker"] == "author_worker.py" and
             self.profile["installation_manifest_sha256"] == INSTALLATION, "PUBLIC_CHECK_PROFILE_LAYOUT")
        old_raw = h.read(OLD/"installation/INSTALLATION.json", 2*MIB)
        manifest_raw = h.read(self.package/"installation/INSTALLATION.json", 2*MIB)
        need(manifest_raw == old_raw and h.sha(manifest_raw) == INSTALLATION, "PUBLIC_CHECK_UNCHANGED_INSTALLATION")
        self.manifest = h.diagnostic_json(manifest_raw)
        need(self.manifest["schema"] == "DMKN_ORDINARY_NATIVE_INSTALLATION_V1" and
             h.identity("DMKN-ORDINARY-IMPLEMENTATION-CLAIM-V1", h.canonical(self.manifest["implementation"])) == IMPLEMENTATION
             and self.manifest["implementation"]["semantic_id"] == SEMANTIC, "PUBLIC_CHECK_INSTALLATION_ID")
        self.package_pins = dict(self.profile["files"])
        installation_files = {"INSTALLATION.json"}
        for logical, expected in self.manifest["files"].items():
            parts = h.relative(logical).parts
            if parts[0] in self.runtimes:
                self.hold(self.runtimes[parts[0]].joinpath(*parts[1:]), expected)
            else:
                installation_files.add(logical)
                self.package_pins["installation/"+logical] = expected
                self.hold(OLD/"installation"/h.relative(logical), expected)
        self.package_pins["installation/INSTALLATION.json"] = {"bytes": len(manifest_raw), "sha256": INSTALLATION}
        self.package_pins["PROFILE.json"] = {"bytes": len(raw), "sha256": args.profile_sha256}
        need(1 <= len(self.package_pins) <= 512 and len({p.casefold() for p in self.package_pins}) == len(self.package_pins),
             "PUBLIC_CHECK_PACKAGE_CENSUS")
        for logical, expected in self.package_pins.items():
            self.hold(self.package/h.relative(logical), expected)
        need(self.tree(OLD/"installation") == installation_files and
             self.tree(self.package/"installation") == installation_files and
             self.tree(self.package) == set(self.package_pins), "PUBLIC_CHECK_EXACT_PACKAGE_TREES")
        for logical, digest in ANCHORS.items():
            need(self.hold(SAVED/h.relative(logical))["sha256"] == digest, "PUBLIC_CHECK_SAVED_ANCHOR")
        # This exact prior audited map excludes mutable catalog/custody databases
        # and locks. It includes accepted reports, evidence and native artifacts.
        retained = self.document(SAVED/"IMMUTABLE-FILES.json")
        need(type(retained) is dict and len(retained) <= 1024, "PUBLIC_CHECK_OLD_PIN_MAP")
        for path, pin in retained.items():
            self.hold(h.ordinary(path), pin)
        adoption = self.document(SAVED/"catalog/ADOPTION.json")
        need(adoption["store_id"] == STORE and adoption["implementation"] == self.manifest["implementation"],
             "PUBLIC_CHECK_EXISTING_ADOPTION")
        completed = self.document(SAVED/"completion/RESULT.json")
        self.target = {"name": h.name("CommonsLibraryExample.add_zero"), "unit_id": UNITS[1], "export_id": EXPORT}
        need(completed["targets"] == [self.target] and completed["local_root"] == CONTEXT and
             completed["parent_root"] == PARENT and [r["unit_id"] for r in completed["units"]] == UNITS,
             "PUBLIC_CHECK_ACCEPTED_CONTEXT")
        self.evidence = []
        for row in completed["units"]:
            path = SAVED/"completion/evidence"/(row["unit_id"]+".json")
            self.hold(path, {key: row[key] for key in ("bytes", "sha256")})
            raw = h.read(path)
            need(h.identity("DMKN-ORDINARY-EVIDENCE-V2", raw) == row["unit_id"], "PUBLIC_CHECK_EVIDENCE_ID")
            self.evidence.append(h.diagnostic_json(raw))
        self.bindings = [[h.name(n), symbol] for n, symbol in BINDINGS]
        imports = self.evidence[1]["imports"]
        need(all(row in imports for row in self.bindings), "PUBLIC_CHECK_KNOWN_BINDINGS")
        roles = self.manifest["roles"]
        def helper(role, module, digest):
            logical = roles[role]
            need(logical.startswith("supervisor/") and self.manifest["files"][logical]["sha256"] == digest,
                 "PUBLIC_CHECK_SUPERVISOR_PIN")
            return h.load_exact(self.package/"installation"/h.relative(logical), module,
                                self.manifest["files"][logical], self.check)
        self.supervisor = helper("supervisor", "_public_query_supervisor",
            "6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9")
        helper("domains", "domains", "651db5f6bb707159c0d29dd6092174bfcebd1dc17b833fdfdacf7e2a66d8522a")
        self.jobs = helper("job", "_public_query_job",
            "bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028")
        self.output.mkdir(); self.output_created = True
        for name in ("fixtures", "config", "calls", "query-local", "consumer"):
            (self.output/name).mkdir()
        self.save(self.output/"SELECTION.json", {"package": str(self.package), "profile_sha256": args.profile_sha256,
            "package_files": self.package_pins, "installation_manifest_sha256": INSTALLATION,
            "implementation_id": IMPLEMENTATION, "context_root": CONTEXT, "store_id": STORE,
            "original_allowance": vars(args), "call_caps": CAPS, "cleanup_seconds": CLEANUP_SECONDS,
            "scope": "REUSED_SYNTHETIC_OWNER_ONE_NEW_INDEX_NO_ADMISSION_OR_REBUILD"})
        self.save(self.output/"fixtures/known-bindings.json", self.bindings)

    def reserve(self, label):
        self.check()
        need(label in CAPS and not any(e["label"] == label for e in self.calls), "PUBLIC_CHECK_SINGLE_CALL")
        wall, cpu = CAPS[label]
        grant = self.supervisor.limits_checked({
            "wall_seconds": min(wall, math.floor(self.deadline-time.monotonic())-CLEANUP_SECONDS),
            "cpu_seconds": min(cpu, math.floor(self.args.cpu_seconds-self.charged-self.reserved-
                (time.process_time()-self.cpu_started))-CONTROLLER_CPU_RESERVE),
            "memory_mib": self.args.memory_mib, "active_processes": 8,
            "stdout_bytes": 8*MIB, "stderr_bytes": 8*MIB})
        need(grant["wall_seconds"] >= (15 if label in ("01-query-local", "07-consumer") else 40) and
             grant["cpu_seconds"] >= (2 if label in ("01-query-local", "07-consumer") else 5),
             "PUBLIC_CHECK_REMAINING_CHILD_GRANT")
        event = {"label": label, "limits": grant, "launched": False, "settled": False,
                 "cpu_complete": False, "charged_cpu_seconds": grant["cpu_seconds"]}
        self.calls.append(event); self.reserved += grant["cpu_seconds"]
        return event

    def launch(self, event, argv, *, asynchronous=False):
        self.check()
        need(not event["launched"], "PUBLIC_CHECK_NO_RELAUNCH")
        # The pre-reserved find grant may wait for READY. Narrow its wall grant
        # again at actual dispatch; neither its reservation nor lease is renewed.
        event["limits"]["wall_seconds"] = min(event["limits"]["wall_seconds"],
            math.floor(self.deadline-time.monotonic())-CLEANUP_SECONDS)
        native = event["label"] in ("01-query-local", "07-consumer")
        need(event["limits"]["wall_seconds"] >= (15 if native else 40), "PUBLIC_CHECK_DISPATCH_REMAINING_WALL")
        if not native:
            argv[argv.index("--wall-seconds")+1] = str(event["limits"]["wall_seconds"]-5)
        event.update(argv=argv, cwd=str(self.output), launched=True)
        def supervise():
            try:
                event["supervision"] = self.supervisor.supervise(argv, self.output,
                    self.output/"calls"/event["label"], event["limits"], self.jobs.Job)
            except BaseException as error:
                event["supervision_exception"] = {"type": type(error).__name__, "error": str(error)[:2000]}
        if asynchronous:
            thread = threading.Thread(target=supervise, name="query-check-finite-service", daemon=False)
            self.threads[event["label"]] = thread
            thread.start()
        else:
            supervise()

    def settle(self, event, *, validate=True, public=True):
        if event["settled"]:
            return event.get("public_result")
        thread = self.threads.get(event["label"])
        if thread is not None:
            # No renewed lease: await the already running finite supervisor.
            thread.join(timeout=max(0, self.deadline-time.monotonic()))
            if thread.is_alive():
                event["thread_not_closed"] = True
        report = event.get("supervision")
        final = report.get("final_job") if type(report) is dict else None
        observed = final.get("cpu_seconds") if type(final) is dict else None
        known = (not event.get("thread_not_closed") and type(observed) in (int, float) and
                 math.isfinite(observed) and observed >= 0)
        if not event["launched"]:
            observed, known = 0.0, True
        self.reserved -= event["limits"]["cpu_seconds"]
        charged = observed if known else event["limits"]["cpu_seconds"]
        self.charged += charged; self.cpu_complete = self.cpu_complete and known
        event.update(settled=True, cpu_complete=known, charged_cpu_seconds=charged)
        self.h.save(self.output/"calls"/(event["label"]+"-SUPERVISION.json"), event)
        if not validate:
            return None
        need(known, "PUBLIC_CHECK_UNKNOWN_CPU_FULL_GRANT_CHARGED")
        self.h.clean(report)
        path = self.output/"calls"/event["label"]
        need(self.h.read(path/"stderr.txt", MIB) == b"", "PUBLIC_CHECK_CHILD_STDERR")
        raw = self.h.read(path/"stdout.txt", 8*MIB)
        if public:
            event["public_result"] = self.h.diagnostic_json(raw)
            need(event["public_result"].get("ok") is True and not event["public_result"].get("close_errors"),
                 "PUBLIC_CHECK_PUBLIC_SUCCESS")
        else:
            need(raw == b"", "PUBLIC_CHECK_LEAN_STDOUT")
        self.check()
        return event.get("public_result")

    def cli(self, event, script, operation=None, *, state=False, extra=()):
        grant = event["limits"]
        argv = [str(PYTHON), "-I", "-S", "-B", str(self.package/script)]
        if operation is not None:
            argv.append(operation)
        argv += ["--profile-sha256", self.args.profile_sha256, "--python-runtime", str(PYTHON.parent),
                 "--lean-runtime", str(LEAN), "--wall-seconds", str(grant["wall_seconds"]-5),
                 "--cpu-seconds", str(grant["cpu_seconds"]-1), "--memory-mib", str(self.args.memory_mib)]
        if state:
            argv += ["--catalog", str(SAVED/"catalog"), "--custody", str(SAVED/"custody"),
                     "--store-id", STORE, "--custody-limits", str(SAVED/"fixtures/custody-limits.json")]
        return argv+list(map(str, extra))

    def peer(self, event, operation, config, *, asynchronous=False):
        path = self.output/"config"/(operation+".json")
        pin = self.save(path, config)
        self.launch(event, self.cli(event, "peer.py", operation, state=operation != "find",
            extra=("--config", path, "--config-sha256", pin["sha256"], "--output", self.output/operation)),
            asynchronous=asynchronous)
        if not asynchronous:
            return self.public_result(event, operation)

    def public_result(self, event, operation):
        result = self.settle(event)
        directory = self.output/("export" if operation == "export-module" else operation)
        need(result["operation"] == operation and result["profile_sha256"] == self.args.profile_sha256 and
             result["implementation_id"] == IMPLEMENTATION,
             "PUBLIC_CHECK_PUBLIC_IDENTITY")
        if operation != "find":
            need(result["store_id"] == STORE and result["catalog"] == str(SAVED/"catalog") and
                 result["custody"] == str(SAVED/"custody"), "PUBLIC_CHECK_PUBLIC_OWNER")
        else:
            need(all(result[k] is None for k in ("store_id", "catalog", "custody")), "PUBLIC_CHECK_FIND_NO_OWNER")
        if operation != "export-module":
            need(result["semantic_id"] == SEMANTIC and result == self.document(directory/"RESULT.json") and
                 result["result"]["cleanup_errors"] == [],
                 "PUBLIC_CHECK_PEER_SAVED_REPORT")
        return result["result"]

    def compile(self, label, source, modules, purpose):
        event = self.reserve(label)
        env = {"LEAN_PATH": os.pathsep.join((str(LEAN/"lib/lean"), str(modules))),
               "PATH": os.pathsep.join((str(PYTHON.parent), str(LEAN/"bin"))),
               "source": str(source), "purpose": purpose}
        self.save(self.output/"calls"/(label+"-ENVIRONMENT.json"), env)
        self.launch(event, [str(PYTHON), "-I", "-S", "-B", str(self.script), "--lean-worker",
                            str(LEAN), str(modules), str(source), purpose])
        self.settle(event, public=False)
        for suffix in self.h.PARTS:
            need(self.hold(source.parent/(source.stem+suffix))["bytes"] > 0, "PUBLIC_CHECK_FIVE_LEAN_PARTS")

    def ready(self, event):
        until = min(self.deadline-CLEANUP_SECONDS, time.monotonic()+15)
        path = self.output/"serve/READY.json"
        while time.monotonic() < until:
            self.check()
            if path.exists():
                try:
                    ready = self.document(path)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    ready = None  # A concurrently written incomplete file is not readiness.
                if ready is not None:
                    need(ready["status"] == "READY" and ready["host"] == "127.0.0.1" and
                         type(ready["port"]) is int and 0 < ready["port"] <= 65535 and
                         ready["tls"] is False and ready["shared_custody"] == str(SAVED/"custody") and
                         ready["index"] == str(self.output/"new-profile-index") and
                         ready["lease_seconds"] == 20 and ready["mathematical_acceptance"] is False,
                         "PUBLIC_CHECK_ACTUAL_READY")
                    self.hold(path)
                    return ready
            need(self.threads[event["label"]].is_alive(), "PUBLIC_CHECK_SERVICE_EXITED_BEFORE_READY")
            time.sleep(0.05)
        raise ValueError("PUBLIC_CHECK_READY_DEADLINE")

    def run(self, report):
        h, w = self.h, self.output
        report["phase"] = "QUERY_LOCAL"
        source = w/"query-local/NatRightIdentityQuery.lean"
        raw = ('module\npublic import Init\npublic meta import OwnerQueryCommand\n'
               'set_option autoImplicit false\n#ordinary_type_query [] '+
               json.dumps((w/"query-local/native-type.json").as_posix())+' :\n'
               '  forall n : Nat, Nat.add n Nat.zero = n\n').encode("ascii")
        self.save(source, raw)
        self.compile("01-query-local", source, self.package/"authoring/helpers", "query")
        native_pin = self.hold(w/"query-local/native-type.json")
        native_doc = self.document(w/"query-local/native-type.json")
        report["phase"] = "PUBLIC_QUERY"
        event = self.reserve("02-query")
        self.launch(event, self.cli(event, "query.py", extra=("--native-type", w/"query-local/native-type.json",
            "--bindings", w/"fixtures/known-bindings.json", "--output", w/"query-prepared")))
        query = self.settle(event)
        query_doc, specs = self.document(w/"query-prepared/QUERY.json"), self.document(w/"query-prepared/SPECS.json")
        need(query == self.document(w/"query-prepared/RESULT.json") and query["operation"] == "prepare-query" and
             query["mathematical_acceptance"] is False and query["profile_sha256"] == self.args.profile_sha256 and
             query_doc["schema"] == "DMKN_ORDINARY_FORMAL_TYPE_QUERY_V1" and query_doc["semantic_id"] == SEMANTIC and
             native_doc == ["DMKN_ORDINARY_LEAN_QUERY_TYPE_AST_V1", query_doc["universe_params"], query_doc["type"]] and
             query_doc["key_profile"] == query["key_profile"] and query_doc["type_bindings"] == self.bindings and
             query["native_type_sha256"] == native_pin["sha256"] and
             query["bindings_sha256"] == self.hold(w/"fixtures/known-bindings.json")["sha256"] and
             query["query_sha256"] == self.hold(w/"query-prepared/QUERY.json")["sha256"] and
             query["specs"] == specs and len(specs) == 1 and specs[0]["tag"] == "declared-type-key" and
             len(query["features"]) == 1, "PUBLIC_CHECK_ACTUAL_QUERY_OUTPUTS")
        self.tree(w/"query-prepared")
        report["query"] = query
        report["phase"] = "PUBLISH"
        index = {"path": str(w/"new-profile-index"), "limits": INDEX_LIMITS, "create": True}
        published = self.peer(self.reserve("03-publish"), "publish", {"index": index, "context_root": CONTEXT,
            "targets": [self.target], "max_unit_bytes": MIB, "max_total_bytes": 4*MIB})
        need(published["status"] == "INDEXED_LOCAL_TARGETS" and published["local_context"] == CONTEXT and
             published["mathematical_acceptance"] is False and len(published["publications"]) == 1,
             "PUBLIC_CHECK_ONE_PUBLICATION")
        publication = published["publications"][0]
        record = publication["record"]
        need(publication["new"] is True and publication["mathematical_acceptance"] is False and
             record["object_id"] == EXPORT and record["namespace"] == query["namespace"] and
             all(feature in record["features"] for feature in query["features"]), "PUBLIC_CHECK_PUBLICATION_NAMESPACE")
        report["publication"] = publication
        report["phase"] = "SERVE_AND_FIND"
        # Both grants are reserved BEFORE either concurrent command begins.
        service, search = self.reserve("04-serve"), self.reserve("05-find")
        self.peer(service, "serve", {"index": dict(index, create=False), "host": "127.0.0.1", "port": 0,
            "tls": None, "lease_seconds": 20, "cleanup_seconds": 10, "share_all_custody": True, "exclusive": True,
            "limits": {"max_connections": 2, "max_requests": 24, "max_reply_bytes": 8*MIB, "operation_ms": 5000}},
            asynchronous=True)
        ready = self.ready(service)
        found = self.peer(search, "find", {"contacts": {"selected": {"host": ready["host"], "port": ready["port"],
            "tls": False, "server_name": None, "ca_file": None, "ca_sha256": None}}, "providers": ["selected"],
            "specs": specs, "limits": {"providers": 1, "snapshots": 1, "requests": 4, "pages": 2,
                "examined": 32, "candidates": 8, "bytes": MIB, "wall_ms": 10000, "inflight": 1},
            "offer": {"max_bytes": 16384, "max_expanded_bytes": MIB, "max_age_ms": 10000},
            "page": {"scanned": 16, "matches": 8, "bytes": 131072, "timeout_ms": 1000,
                "record_probes": 256, "node_reads": 100000, "hash_calls": 2000000, "sql_vm_steps": 1000000}})
        need(found["status"] == "INCOMPLETE_SEARCH" and found["global_complete"] is False and
             found["mathematical_acceptance"] is False and found["namespace"] == query["namespace"] and
             found["features"] == query["features"] and
             found["termination"] == "SELECTED_CONTACTS_FINISHED_NO_COMPLETENESS_CLAIM" and
             found["search"]["http"]["failed_requests"] == 0 and
             found["search"]["session"]["last_refusal"] is None and
             found["search"]["session"]["pending_requests"] == 0 and len(found["matches"]) == 1,
             "PUBLIC_CHECK_INERT_DISCOVERY")
        match = found["matches"][0]
        need(match["provider"] == "selected" and match["record"] == record and
             match["snapshot_id"] == publication["snapshot_id"], "PUBLIC_CHECK_ACTUAL_DISCOVERED_RECORD")
        locator = match["record"]["locator"]
        discovered = {"name": locator["export_name"], "unit_id": locator["unit_id"], "export_id": match["record"]["object_id"]}
        need(discovered == self.target, "PUBLIC_CHECK_DISCOVERED_TARGET_IDENTITY")
        self.save(w/"fixtures/discovered-targets.json", [discovered])
        served = self.public_result(service, "serve")
        need(served["status"] == "LEASE_FINISHED" and served["quiescent"] is True and
             served["cleanup_errors"] == [] and served["ready"] == ready, "PUBLIC_CHECK_SERVICE_CLOSED_BEFORE_EXPORT")
        report.update(discovered_target=discovered, service=served, search=found)
        report["phase"] = "PUBLIC_EXPORT"
        event = self.reserve("06-export")
        self.launch(event, self.cli(event, "owner.py", "export-module", state=True,
            extra=("--parent-root", CONTEXT, "--module-targets", w/"fixtures/discovered-targets.json", "--output", w/"export")))
        exported = self.public_result(event, "export-module")
        module = self.export_check(exported, discovered)
        report["module_export"] = exported
        report["phase"] = "NORMAL_CONSUMER"
        consumer = w/"consumer/Consumer.lean"
        self.save(consumer, ("module\npublic import Init\npublic import "+module+"\npublic section\n"
            "theorem QueryPackageConsumer.useFound (n : Nat) :\n"
            "    Nat.add n Nat.zero = n :=\n  CommonsLibraryExample.add_zero n\n").encode("ascii"))
        self.compile("07-consumer", consumer, w/"export/modules", "consumer")
        report["phase"] = "FINAL_VERIFY"
        need([event["label"] for event in self.calls] == list(CAPS) and all(e["settled"] for e in self.calls) and
             self.reserved == 0 and self.cpu_complete, "PUBLIC_CHECK_EXACT_SEVEN_CLOSED_CALLS")
        for directory in ("query-local", "consumer", "publish", "serve", "find", "export", "calls"):
            self.tree(w/directory)
        for path, expected in list(self.held.items()):
            self.hold(Path(path), expected)
        need(self.tree(self.package) == set(self.package_pins), "PUBLIC_CHECK_FINAL_PACKAGE_CENSUS")
        self.save(w/"IMMUTABLE-FILES.json", self.held)
        self.check()
        report.update(status="PASS_PUBLIC_QUERY_DISCOVERY_MATCHED_EXPORT_USE", phase="COMPLETE",
                      immutable_preservation="VERIFIED_BEFORE_AND_AFTER")

    def export_check(self, exported, discovered):
        h, directory = self.h, self.output/"export"
        manifest = self.document(directory/"MODULE.json")
        need({k: v for k, v in exported.items() if k not in ("module_directory", "manifest_path", "supported_runtime")} == manifest and
             manifest["status"] == "CHECKED_LOCAL_MODULE_WITH_EXACT_INSTALLED_THEOREM_RELATION" and
             manifest["policy"] == "DMKN_ORDINARY_INIT_EXACT_THEOREM_MATCH_PUBLIC_MODULE_V2" and
             manifest["source_context_root"] == CONTEXT and manifest["semantic_id"] == SEMANTIC and
             manifest["targets"] == [discovered] and manifest["new_catalog_acceptance"] is False and
             manifest["ordered_unit_ids"] == UNITS and manifest["matched_unit_indices"] == [0] and
             manifest["units_matched"] == manifest["units_checked"] == 1 and
             manifest["matched_names"] == [h.name("Nat.add_zero")] and
             manifest["added_names"] == [discovered["name"]] and
             exported["module_directory"] == str(directory/"modules") and
             exported["manifest_path"] == str(directory/"MODULE.json"), "PUBLIC_CHECK_MIXED_EXPORT_RESULT")
        runtime = exported["supported_runtime"]
        need(runtime["implementation_id"] == IMPLEMENTATION and runtime["installation_manifest_sha256"] == INSTALLATION and
             runtime["lean_runtime"] == str(LEAN) and runtime["lean_executable"] == str(LEAN/"bin/lean.exe") and
             runtime["lean_executable_pin"] == self.manifest["files"][self.manifest["roles"]["lean"]], "PUBLIC_CHECK_EXPORT_RUNTIME")
        selection, request = self.document(directory/"SELECTION.json"), self.document(directory/"request.json")
        key_input = selection["key_input"]
        need(selection["cache_key"] == manifest["cache_key"] == h.identity("DMKN-ORDINARY-MODULE-CACHE-V1", h.canonical(key_input)) and
             manifest["module_name"] == "DMKNBridge_"+manifest["cache_key"] and
             key_input["semantic_id"] == SEMANTIC and key_input["foundation_id"] == manifest["foundation_id"] and
             key_input["implementation_id"] == IMPLEMENTATION and key_input["policy"] == manifest["policy"] and
             key_input["targets"] == [discovered], "PUBLIC_CHECK_ACTUAL_CACHE_KEY")
        sources = {"native": "module/OrdinaryModule.lean", "worker": "module_worker.py",
                   "controller": "authoring/py/module_export.py", "closure": "authoring/py/module_closure.py"}
        expected_sources = {role: [self.profile["files"][path]["bytes"], self.profile["files"][path]["sha256"]]
                            for role, path in sources.items()}
        expected_helpers = sorted([[0, path.removeprefix("authoring/helpers/"), pin["bytes"], pin["sha256"]]
            for path, pin in self.profile["files"].items() if path.startswith("authoring/helpers/")])
        need(key_input["sources"] == expected_sources and key_input["helpers"] == expected_helpers and
             selection["source_context_root"] == CONTEXT and selection["ordered_unit_ids"] == UNITS,
             "PUBLIC_CHECK_CACHE_SUPPORT_BINDING")
        for role in ("request", "inventory"):
            self.hold(directory/(role+".json"), selection["input_pins"][role])
        need(h.read(directory/"inventory.json", MIB) == h.read(self.package/"installation"/
             h.relative(self.manifest["roles"]["inventory"]), MIB), "PUBLIC_CHECK_EXACT_FIXED_INVENTORY")
        need(request["units"] == [doc["unit"] for doc in self.evidence] and request["unit_ids"] == UNITS and
             request["context_root"] == CONTEXT and request["targets"] == [discovered["name"]] and
             request["module_name"] == h.name(manifest["module_name"]), "PUBLIC_CHECK_EXACT_RETAINED_CLOSURE")
        native = self.document(directory/"SUPERVISION.json")
        h.clean(native)
        need(native["argv"][4] == str(self.package/"module_worker.py") and
             native["argv"][6] == str(self.package/"module/OrdinaryModule.lean") and
             native["final_job"]["cpu_seconds"] == manifest["native_cpu_seconds"] and
             h.read(directory/"supervision/stderr.txt", MIB) == b"", "PUBLIC_CHECK_INNER_NATIVE_CLOSURE")
        native_raw = h.read(directory/"native-report.json", 8*MIB)
        native_report = h.diagnostic_json(native_raw)
        rows = [row for doc in self.evidence for row in doc["unit"][2]]
        need(h.sha(native_raw) == manifest["report_sha256"] and native_report["schema"] == "DMKN_ORDINARY_MODULE_OUTPUT_V2" and
             native_report["checking_passes"] == 2 and native_report["basis_rows"] == 581 and
             all(native_report[k] == request[k] for k in ("semantic_id", "context_root", "foundation_id", "module_name", "targets", "unit_ids")) and
             native_report["inventories"] == rows and native_report["names"] == [row[0] for row in rows] and
             native_report["matched_inventories"] == self.evidence[0]["unit"][2] and
             native_report["added_inventories"] == self.evidence[1]["unit"][2] and
             all(native_report[k] == manifest[k] for k in ("matched_unit_indices", "units_matched", "units_checked", "matched_names", "added_names")),
             "PUBLIC_CHECK_NATIVE_MATCHED_ADDED_INVENTORIES")
        phases = [h.diagnostic_json(line) for line in h.read(directory/"native-report.json.phases.jsonl").splitlines()]
        need([(r["phase"], r["event"], r["exit_code"]) for r in phases] ==
             [(phase, event, code) for phase in ("build", "reread-private", "reread-exported")
              for event, code in (("STARTED", None), ("EXITED", 0))], "PUBLIC_CHECK_BOTH_REREADS")
        module = manifest["module_name"]
        need(re.fullmatch(r"DMKNBridge_[0-9a-f]{64}", module) and
             set(manifest["artifact_parts"]) == {module+suffix for suffix in h.PARTS} and
             {p.name for p in (directory/"modules").iterdir()} == set(manifest["artifact_parts"]), "PUBLIC_CHECK_MODULE_FIVE_PARTS")
        for filename, pin in manifest["artifact_parts"].items():
            self.hold(directory/"modules"/filename, pin)
        need(native_report["artifact_parts"] == [{"path": str(directory/"modules"/(module+suffix)),
             "bytes": manifest["artifact_parts"][module+suffix]["bytes"]} for suffix in h.PARTS],
             "PUBLIC_CHECK_NATIVE_ARTIFACT_PART_BINDING")
        return module


def main():
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize and Path(sys.executable).resolve() == PYTHON, "PUBLIC_CHECK_PYTHON_PROFILE")
    if sys.argv[1:2] == ["--lean-worker"]:
        return lean_worker(sys.argv[2:])
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for key in ("package", "profile-sha256", "python-runtime", "lean-runtime", "output"):
        parser.add_argument("--"+key, required=True)
    for key in ("wall-seconds", "cpu-seconds", "memory-mib"):
        parser.add_argument("--"+key, required=True, type=int)
    args = parser.parse_args()
    need(120 <= args.wall_seconds <= 180 and 60 <= args.cpu_seconds <= 110 and
         256 <= args.memory_mib <= 1536, "PUBLIC_CHECK_ORIGINAL_FINITE_ENVELOPE")
    check = Check(args, helpers())
    report = {"status": "FAILED", "phase": "PREFLIGHT", "calls": check.calls,
        "claim": "SAME_HOST_PUBLIC_COMPATIBILITY_NOT_NEW_ACCEPTANCE_OR_USEFUL_GROWTH_OR_FINAL_V5",
        "retention": "ALL_PRIOR_AND_PARTIAL_OUTPUTS_PRESERVED_NO_RETRY"}
    try:
        check.prepare()
        check.run(report)
    except BaseException as error:
        report.update(status="FAILED", error_type=type(error).__name__, error=str(error)[:2000],
            immutable_preservation="POST_FAILURE_SAVED_FILE_AUDIT_REQUIRED_NO_RENEWED_ALLOWANCE")
    finally:
        cleanup = []
        for event in check.calls:
            if not event["settled"]:
                try:
                    check.settle(event, validate=False)
                except BaseException as error:
                    cleanup.append({"label": event["label"], "error": str(error)[:2000]})
        report.update(wall_seconds=time.monotonic()-check.started,
            controller_cpu_seconds=time.process_time()-check.cpu_started,
            inclusive_child_job_cpu_charged=check.charged, outstanding_cpu_reserved=check.reserved,
            child_cpu_complete=check.cpu_complete, cleanup_errors=cleanup,
            accounting="CHILD_JOB_CPU_ONCE_NO_NESTED_DOUBLE_CHARGE_UNKNOWN_FULL_GRANT_THEN_STOP_OUTER_JOB_AUTHORITATIVE")
        if (cleanup or check.reserved or not check.cpu_complete or report["wall_seconds"] >= args.wall_seconds or
                report["controller_cpu_seconds"]+check.charged >= args.cpu_seconds):
            report.update(status="FAILED", budget_or_cleanup_error="PUBLIC_CHECK_ORIGINAL_ALLOWANCE_OR_CLOSURE")
        if check.output_created:
            check.h.save(check.output/"PUBLIC-CHECK-RESULT.json", report)
    print(json.dumps({"status": report["status"], "phase": report["phase"]}, sort_keys=True), flush=True)
    return 0 if report["status"] == "PASS_PUBLIC_QUERY_DISCOVERY_MATCHED_EXPORT_USE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
