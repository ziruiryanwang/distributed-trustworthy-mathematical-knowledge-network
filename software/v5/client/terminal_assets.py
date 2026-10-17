"""Exact retained assets and real owners for one genuine terminal integration.

No proof, guest, verifier call, fabricated receipt or ambient experiment import.
All inputs are selected by the outer owner plan. Profiles name the actual source
snapshot; retained data and successful construction confer no mathematics.
"""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

from aggregate_claims import bindings as B
from aggregate_claims.aggregate_admission import AggregateReceiptVerifier
from client.actual_assets_atomic import need, ordinary, read_pin, sha
from client.workspace_evidence import SCHEMA
from client.workspace_resilient import Workspace
from custody.module_store import BODY_SCHEMA, permitted_hashes
from evidence_network.custody import public_profile
from evidence_network.packet import pack_terminal
from mixed_claims.authoring_atomic import MixedOwnerPreparation
from mixed_claims.packet import Envelope
from mixed_claims.receiver import MixedDeltaVerifier
from modules import codec as C
from production.producer import parse

MIB = 1024**2
PARAMETERS = "DMKN_V5_TERMINAL_ACTUAL_OWNER_V1"
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
FIRST = "4adbc049e4d1e29ec045d64c7dba9e27bdd506dfa6c7fb707f022be40439e742"
SECOND = "52c564f87f31082468557df6eed0a04bc7adf9d28d9614fe6cf173f5633088bf"
AGGREGATE = "99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60"
MANIFEST = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
PORTS = {"bootstrap", "origin_location", "replica_location", "readerB", "readerC",
         "origin_http", "replica_http"}
RETAINED = {
    "base_bundle": (53769, "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"),
    "foundation": (23313, "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"),
    "first_input": (113220, "88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1"),
    "source": (1383, "a4e2d897f929e2e63c43c70f274a8f270d9bb783180a6677366ae50ad73df153"),
    "roots": (52, "7882f5358514ab6fbe98c212868e267cd9d0dc4a20561b2702d66530a868b2e9"),
    "reference_packet": (662480, "54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1"),
    "header": (192, "49dd845edaec83f5b0cba5af38653f768e51ed95a4bb6ea7824c10bdd1c3169e"),
    "derivation": (6350, "1750785cbde497cbd60f371203ce67cbf35844aaf9422782b65f03c2d1561941"),
    "aggregate_host": (6630400, "a9438205bbb091623f12bd10a7e9a0a2b437c873003fec3cb000c7d8dbbd7a05"),
    "preparation_host": (66652160, "74a58215351a641d9efbbffbc389b5faea350c46f5c1e1a48bf76cf77b99d6c9"),
    "native": (1713152, "37a0af1b08e7176fb0d387b3e8439266d7c2c0befe5b08bc3cdd4c90c62d3e40"),
    "image": (1681428, "d76f623bb1de5c840fd2ef9c1ac35fc6aba2de74cda0f62c11c161f6973da31f"),
    "frontend": (593408, "1f73b8b0ea20395a43202a3c155e6fd929a5ae0cef2a74a4c70d2625b9e3f69d"),
    "profile": (21137, "f03b591c6e9e40346028c35b663d4d2c5daaf9a58ec6eb890810f96c6c984a4b"),
}
JOURNAL_PINS = {
    BASE: "22fe722c57894cb192a6700954fb045a708431a1470e274440c7d60a5767b682",
    FIRST: "07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da",
    SECOND: "6317ca94965267295974ce571adc4ca3c7515a9efed819896592b75d73c14541",
}
ALLOCATION = {
    "B_wall_seconds": (1, 3600), "C_wall_seconds": (1, 3600),
    "controller_cpu_seconds": (1, 600), "receipt_cpu_seconds": (1, 600),
    "native_cpu_seconds": (1, 600), "author_cpu_seconds": (1, 600),
    "admission_wall_seconds": (1, 600), "author_wall_seconds": (1, 600),
    "admission_memory_mib": (64, 4096), "author_memory_mib": (64, 4096),
}


def _bytes(value, size):
    need(type(value) is list and len(value) == size
         and all(type(part) is int and 0 <= part <= 255 for part in value), "TERMINAL_EXACT_BYTES")
    return bytes(value)


def _runtime(rows):
    result = {}
    for row in rows:
        key = row["path"]; value = {name: row[name] for name in ("bytes", "sha256")}
        need(key not in result or result[key] == value, "TERMINAL_RUNTIME_CONFLICT")
        result[key] = value
    need(len(result) <= 128 and sum(row["bytes"] for row in result.values()) <= 512*MIB,
         "TERMINAL_OWNER_RUNTIME_BOUND")
    return result


class Assets:
    def __init__(self, context):
        self.context = context
        context.remaining_seconds()
        params = deepcopy(dict(context.parameters))
        C.fields(params, {"schema", "assets", "ports", "allocation"})
        need(params["schema"] == PARAMETERS, "TERMINAL_PARAMETERS_SCHEMA")
        C.fields(params["assets"], {*RETAINED, "receipt"})
        C.fields(params["ports"], PORTS); C.fields(params["allocation"], set(ALLOCATION))
        self.ports = params["ports"]
        need(all(type(port) is int and 1024 <= port <= 65535 for port in self.ports.values())
             and len(set(self.ports.values())) == len(PORTS), "TERMINAL_DISTINCT_PORTS")
        self._allocation = params["allocation"]
        for key, (lo, hi) in ALLOCATION.items():
            value = self._allocation[key]
            need(type(value) is int and lo <= value <= hi, "TERMINAL_ALLOCATION:"+key)
        a = self._allocation
        need(a["receipt_cpu_seconds"]+a["native_cpu_seconds"] <= 600,
             "TERMINAL_MIXED_SINGLE_VERIFICATION_CAP")
        need(2*a["receipt_cpu_seconds"]+a["native_cpu_seconds"]+a["author_cpu_seconds"]
             <= context.limits["cpu_seconds"], "TERMINAL_OUTER_WORKER_SUBALLOCATION")
        need(max(a["admission_memory_mib"], a["author_memory_mib"])
             <= context.limits["memory_mib"], "TERMINAL_OUTER_MEMORY_SUBALLOCATION")
        self.calls = {
            "admit": dict(native_cpu_seconds=a["native_cpu_seconds"],
                receipt_cpu_seconds=a["receipt_cpu_seconds"],
                wall_seconds=a["admission_wall_seconds"], memory_mib=a["admission_memory_mib"]),
            "author": dict(cpu_seconds=a["author_cpu_seconds"],
                wall_seconds=a["author_wall_seconds"], memory_mib=a["author_memory_mib"]),
        }
        self._pins = params["assets"]
        for name, row in self._pins.items():
            C.fields(row, {"path", "bytes", "sha256"}); ordinary(row["path"])
            C.digest_string(row["sha256"])
            need(type(row["bytes"]) is int and 0 < row["bytes"] <= 128*MIB,
                 "TERMINAL_INPUT_PIN_SIZE")
            if name in RETAINED:
                need((row["bytes"], row["sha256"]) == RETAINED[name], "TERMINAL_RETAINED_IDENTITY:"+name)
        # A receipt is mandatory, independently selected later, with no fixture,
        # capsule, I receipt or missing-file fallback. It is still untrusted here.
        self._receipt = read_pin(self._pins["receipt"], 8*MIB)
        self.receipt_identity = {"bytes": len(self._receipt), "sha256": sha(self._receipt)}
        self.aggregate_image = AGGREGATE
        self.header = read_pin(self._pins["header"], 192)
        B.decode_header(self.header, adopted_image=self.aggregate_image)
        derivation = C.parse_json(read_pin(self._pins["derivation"], MIB))
        need(derivation["schema"] == "DMKN_FIRST_FRONTIER_SELECTION_DERIVATION_V1"
             and _bytes(derivation["selected_header"], 192) == self.header
             and len(derivation["members"]) == 2, "TERMINAL_SELECTED_H2")
        self._members = {}
        for item in derivation["members"]:
            C.fields(item, {"journal", "index", "siblings"})
            exact = _bytes(item["journal"], 184)
            need(type(item["siblings"]) is list and len(item["siblings"]) == 1,
                 "TERMINAL_H2_SINGLE_SIBLING")
            siblings = [_bytes(part, 32) for part in item["siblings"]]
            live = B.bind_member(self.header, exact, item["index"], siblings,
                                 adopted_image=self.aggregate_image)
            module = live["module"]
            need(module in (BASE, FIRST) and module not in self._members
                 and sha(exact) == JOURNAL_PINS[module]
                 and item["index"] == (0 if module == BASE else 1), "TERMINAL_SELECTED_MEMBER")
            self._members[module] = dict(journal=exact, index=item["index"], siblings=siblings)
        need(set(self._members) == {BASE, FIRST}, "TERMINAL_MEMBER_SET")
        self._second = _bytes(derivation["omitted_descendant"], 184)
        need(sha(self._second) == JOURNAL_PINS[SECOND], "TERMINAL_SECOND_EXACT_J")
        self.foundation = read_pin(self._pins["foundation"], MIB)
        self.foundation_sha256 = self._pins["foundation"]["sha256"]
        self._terminal = {module: pack_terminal(self.header, row["journal"], row["index"],
            row["siblings"], self._receipt, aggregate_image=self.aggregate_image,
            envelope=Envelope(**self.configuration()["packet_envelope"]), terminal_receipt_bytes=8*MIB)
            for module, row in self._members.items()}
        self._prepare_profiles()
        context.remaining_seconds()

    def configuration(self):
        return {"schema": SCHEMA, "wire_profile": public_profile(self.aggregate_image),
            "module_limits": dict(modules=8, groups=32, declarations=128, bodies=32,
                                  logical_bytes=16*MIB, db_pages=8192),
            "packet_limits": dict(packets=4, offers=8, offers_per_module=2, packet_bytes=32*MIB,
                                  logical_bytes=128*MIB, db_pages=65536),
            "index_limits": dict(max_objects=32, max_postings=4096, max_features=1024,
                                 max_snapshots=64, max_logical_bytes=16*MIB, max_db_pages=8192),
            "packet_envelope": asdict(Envelope(packet_bytes=32*MIB, receipt_bytes=8*MIB,
                claims=1, frontiers=2, deltas=1, edges=2, openings=32, bodies=32)),
            "terminal_receipt_bytes": 8*MIB, "max_operations": 2,
            "max_report_bytes": MIB, "ledger_pages": 1024}

    def grant_limits(self, phase):
        need(phase in ("B", "C"), "TERMINAL_PHASE")
        a = self._allocation
        admission = a["receipt_cpu_seconds"]+(a["native_cpu_seconds"] if phase == "C" else 0)
        author = a["author_cpu_seconds"] if phase == "B" else 0
        return dict(wall_seconds=a[phase+"_wall_seconds"],
            controller_cpu_seconds=a["controller_cpu_seconds"], calls=256, input_bytes=256*MIB,
            worker_cpu_seconds=admission+author, output_bytes=512*MIB, output_entries=4096,
            acquisition=dict(requests=128, reply_bytes=128*MIB, verify_attempts=1,
                verification_input_bytes=32*MIB, worker_cpu_seconds=admission),
            imports=dict(max_sources=2 if phase == "B" else 1, max_members=3, max_receipts=1,
                max_calls=4096, submitted_bytes=256*MIB, data_bytes=16*MIB))

    def _prepare_profiles(self):
        context = self.context
        template = parse(read_pin(self._pins["profile"], MIB))
        producer = template["producer"]
        need((producer["image_id"], producer["foundation"], producer["policy"])
             == (B.RELATION_IMAGE, B.FOUNDATION, B.POLICY), "TERMINAL_PREPARATION_BASIS")
        old_install = Path(producer["supervisor_manifest"]["path"]).parent
        self._manifest = {"path": str(context.installation/"RELEASE-MANIFEST.json"),
            "bytes": producer["supervisor_manifest"]["bytes"], "sha256": MANIFEST}
        files = parse(read_pin(self._manifest, 8*MIB))["files"]

        def installed(row):
            path = Path(row["path"])
            need(path.is_relative_to(old_install), "TERMINAL_TEMPLATE_RUNTIME_ROOT")
            relative = path.relative_to(old_install).as_posix()
            need(files.get(relative) == {key: row[key] for key in ("bytes", "sha256")},
                 "TERMINAL_TEMPLATE_MANIFEST_ROLE")
            return {**row, "path": str(context.installation/relative)}

        sources = {}
        for key, digest in context.source_sha256.items():
            if not key.startswith("v5/") or not key.endswith(".py"): continue
            context.remaining_seconds()
            path = ordinary(context.sources_v5/key[3:]); size = path.stat().st_size
            need(0 < size <= 2*MIB, "TERMINAL_SOURCE_SIZE")
            row = {"path": str(path), "bytes": size, "sha256": digest}
            read_pin(row, 2*MIB)  # Authority is the selected digest, not a new hash.
            sources[key[3:]] = row
        need(len(sources) <= 120 and {"authoring/worker.py", "client/terminal_assets.py",
            "client/workspace_resilient.py", "transport/search_resilience.py"} <= set(sources),
            "TERMINAL_SOURCE_MAP")
        producer.update(supervisor_manifest=deepcopy(self._manifest),
            host=deepcopy(self._pins["preparation_host"]), python=installed(producer["python"]),
            python_dll=installed(producer["python_dll"]),
            runtime_pins=[installed(row) for row in producer["runtime_pins"]],
            source_pins=[sources["production/__init__.py"], sources["production/producer.py"]])
        template.update(image=deepcopy(self._pins["image"]), worker=sources["authoring/worker.py"],
            native_executable=deepcopy(self._pins["frontend"]), source_pins=list(sources.values()))
        self._preparation = template
        runtime = [producer["python"], producer["python_dll"], *producer["runtime_pins"]]
        self._aggregate_runtime = _runtime([self._pins["aggregate_host"], *runtime, *sources.values()])
        self._native_runtime = _runtime([self._pins["native"], *sources.values()])

    def owners(self, workspace, grant, phase):
        """Construct after reserve; transfer only on success, clean all failures."""
        need(type(workspace) is Workspace and workspace.config == self.configuration()
             and grant.limits == self.grant_limits(phase), "TERMINAL_EXACT_WORKSPACE_GRANT")
        aggregate = delta = preparation = None
        a = self._allocation; caps = grant.limits
        try:
            aggregate = AggregateReceiptVerifier(supervisor_manifest=self._manifest["path"],
                supervisor_manifest_sha256=MANIFEST, executable=self._pins["aggregate_host"]["path"],
                runtime_pins=self._aggregate_runtime, aggregate_image=self.aggregate_image,
                operations=1, submitted_bytes=8*MIB, reserved_cpu_seconds=a["receipt_cpu_seconds"],
                wall_seconds=grant.remaining_seconds(), member_calls=4096, member_storage=3,
                member_bytes=64*MIB, controller_cpu_seconds=a["controller_cpu_seconds"],
                output_bytes=64*MIB, output_entries=256)
            delta = MixedDeltaVerifier(legacy_verifier=None, aggregate_verifier=aggregate,
                native_executable=self._pins["native"]["path"], runtime_pins=self._native_runtime,
                output_directory=grant.directory/"delta", envelope=Envelope(**workspace.config["packet_envelope"]),
                operations=1, submitted_bytes=32*MIB,
                reserved_cpu_seconds=caps["acquisition"]["worker_cpu_seconds"],
                controller_cpu_seconds=a["controller_cpu_seconds"], wall_seconds=grant.remaining_seconds(),
                output_bytes=128*MIB, output_entries=1024)
            if phase == "B":
                preparation = MixedOwnerPreparation(self._preparation,
                    dict(allowance_id=C.hash_value("terminal-client-preparation", {"grant": grant.identifier}),
                        operations=1, worker_cpu_seconds=a["author_cpu_seconds"],
                        controller_cpu_seconds=a["controller_cpu_seconds"], wall_seconds=grant.remaining_seconds(),
                        output_bytes=256*MIB, output_entries=1024), grant.directory/"preparation")
            return workspace.operation(grant, receipt_owner=None, aggregate_owner=aggregate,
                delta_owner=delta, preparation_owner=preparation, foundation_bytes=self.foundation,
                foundation_sha256=self.foundation_sha256)
        except BaseException as error:
            failures = []
            for owner in (preparation, delta, aggregate):
                if owner is not None:
                    try: owner.close()
                    except BaseException as cleanup: failures.append(cleanup)
            if failures: raise BaseExceptionGroup("TERMINAL_OWNER_CONSTRUCTION_CLEANUP", [error, *failures])
            raise

    def origin_material(self):
        """Origin only: strip FIRST proof, retain bounded public semantic data."""
        self.context.remaining_seconds()
        base = C.parse_json(read_pin(self._pins["base_bundle"], MIB))
        first = C.parse_json(read_pin(self._pins["first_input"], MIB))
        need(C.module_id(base["spec"]) == BASE and C.module_id(first["local_spec"]) == FIRST
             and len(base["spec"]["groups"]) == 11 and len(first["local_spec"]["groups"]) == 1,
             "TERMINAL_ORIGIN_INTERFACE")
        first_opening = C.group_opening(first["local_spec"], 0)
        first_export = [["s", "OwnerV5"], ["s", "fold_map_received"]]
        need(first_opening["group"]["declarations"][0]["name"] == first_export,
             "TERMINAL_FIRST_EXPORT")
        groups = [{"module": BASE, "opening": C.group_opening(base["spec"], index)}
                  for index in range(11)]
        groups.append({"module": FIRST, "opening": first_opening})
        values = {}
        for row in base["bodies"]:
            key = row["universes"], row["digest"]
            need(key not in values and C.body_id(row["expression"], key[0]) == key[1],
                 "TERMINAL_ORIGIN_BODY_HASH")
            values[key] = row["expression"]
        bodies, seen = [], set()
        for item in groups:
            for declaration in item["opening"]["group"]["declarations"]:
                for digest in sorted(permitted_hashes(declaration)):
                    key = declaration["universes"], digest
                    need(item["module"] == BASE and key in values, "TERMINAL_ORIGIN_BODY_CLOSURE")
                    if key in seen: continue
                    seen.add(key)
                    bodies.append(dict(schema=BODY_SCHEMA, module_id=BASE,
                        relative_name=declaration["name"], universes=key[0], body_hash=key[1],
                        expression=values[key]))
        need(len(bodies) == len(values) == 11, "TERMINAL_ORIGIN_SEMANTIC_CENSUS")
        self.context.remaining_seconds()
        return {"terminals": [{"module": module, "packet": raw}
                for module, raw in sorted(self._terminal.items())],
            "groups": groups, "bodies": bodies, "first_export_name": first_export}

    def author_input(self):
        """Release only after actual B acquisition; trusted strategy phase rule."""
        self.context.remaining_seconds()
        roots = C.parse_json(read_pin(self._pins["roots"], 1024))
        need(roots == [[["s", "OwnerV5"], ["s", "fold_map_twice_received"]]], "TERMINAL_AUTHOR_ROOT")
        return read_pin(self._pins["source"], 65536).decode("utf-8"), roots

    def expected_journals(self):
        """Evaluator data only; never pass to the unknown-ID chooser."""
        return {"BASE": self._members[BASE]["journal"], "FIRST": self._members[FIRST]["journal"],
                "SECOND": self._second}

    def expected_second_spec(self):
        """Read only after author closes; compare interface, never proof bytes."""
        self.context.remaining_seconds()
        reference = C.parse_json(read_pin(self._pins["reference_packet"], MIB))
        spec = reference["deltas"][-1]["local_spec"]
        need(C.module_id(spec) == SECOND, "TERMINAL_REFERENCE_INTERFACE")
        return deepcopy(spec)
