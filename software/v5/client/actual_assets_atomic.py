"""Pinned data/adoption for one ordinary real-I client strategy, not authority.

No experiment module is imported. Source pins are selected by the outer launch
plan and rebased to its immutable snapshot; hashes read now cannot authorize new
code. The retained preparation profile supplies installed asset identities only.
"""
from copy import deepcopy
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

from admission.verifier import ReceiptVerifier
from aggregate_claims import bindings as B
from client.workspace_atomic import SCHEMA
from frontier_network.custody import public_profile
from mixed_claims.authoring_atomic import MixedOwnerPreparation
from mixed_claims.packet import Envelope
from mixed_claims.receiver import MixedDeltaVerifier
from modules import codec as C
from production.producer import parse

MIB = 1024**2
PARAMETERS = "DMKN_V5_CLIENT_ACTUAL_OWNER_V1"
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
MANIFEST = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
RETAINED = {
    "receipt": (223594, "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47"),
    "bundle": (53769, "09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926"),
    "foundation": (23313, "736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c"),
    "host": (66652160, "74a58215351a641d9efbbffbc389b5faea350c46f5c1e1a48bf76cf77b99d6c9"),
    "native": (1713152, "37a0af1b08e7176fb0d387b3e8439266d7c2c0befe5b08bc3cdd4c90c62d3e40"),
    "image": (1681428, "d76f623bb1de5c840fd2ef9c1ac35fc6aba2de74cda0f62c11c161f6973da31f"),
    "frontend": (593408, "1f73b8b0ea20395a43202a3c155e6fd929a5ae0cef2a74a4c70d2625b9e3f69d"),
    "profile": (21137, "f03b591c6e9e40346028c35b663d4d2c5daaf9a58ec6eb890810f96c6c984a4b"),
}


def need(condition, reason):
    if not condition: raise ValueError(reason)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def ordinary(value):
    path = Path(value)
    need(path.is_absolute() and str(path.resolve()) == str(path), "ACTUAL_CANONICAL_FILE")
    need(path.is_file() and all(not p.is_symlink() and not p.is_junction()
                               for p in (path, *path.parents)), "ACTUAL_ORDINARY_FILE")
    return path


def read_pin(row, maximum=128*MIB):
    C.fields(row, {"path", "bytes", "sha256"}); C.digest_string(row["sha256"])
    need(type(row["bytes"]) is int and 0 < row["bytes"] <= maximum, "ACTUAL_PIN_SIZE")
    path = ordinary(row["path"])
    need(path.stat().st_size == row["bytes"], "ACTUAL_INPUT_SIZE")
    with path.open("rb") as stream: raw = stream.read(row["bytes"]+1)
    need(len(raw) == row["bytes"] and sha(raw) == row["sha256"], "ACTUAL_INPUT_PIN")
    return raw


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    need(len(raw) <= 4*MIB, "ACTUAL_REPORT_SIZE")
    with path.open("xb") as stream: stream.write(raw)


def configuration():
    return {"schema": SCHEMA, "wire_profile": public_profile(),
        "module_limits": dict(modules=32, groups=128, declarations=512, bodies=256,
                              logical_bytes=32*MIB, db_pages=16384),
        "packet_limits": dict(packets=4, offers=8, offers_per_module=2, packet_bytes=16*MIB,
                              logical_bytes=64*MIB, db_pages=32768),
        "index_limits": dict(max_objects=128, max_postings=8192, max_features=1024,
                             max_snapshots=256, max_logical_bytes=32*MIB, max_db_pages=16384),
        "packet_envelope": asdict(Envelope(packet_bytes=16*MIB, claims=1, frontiers=1,
                                           deltas=2, edges=3)),
        "max_operations": 4, "max_report_bytes": MIB, "ledger_pages": 1024}


def grant_limits(phase):
    # Worker reservations are DISJOINT across these three nonrenewable grants:
    # 90 seed + 120 consumer + 90 cold = 300 CPU seconds, within outer 600.
    # Controller lifetime caps are inclusive observations, not additional hard
    # Job reservations. The unchanged outer Job meters the complete process tree.
    need(phase in ("seed", "consumer", "cold"), "ACTUAL_PHASE")
    admission = {"seed": 30, "consumer": 60, "cold": 90}[phase]
    author = 0 if phase == "cold" else 60
    return dict(wall_seconds={"seed": 180, "consumer": 480, "cold": 180}[phase],
        controller_cpu_seconds=90, calls=128, input_bytes=64*MIB,
        worker_cpu_seconds=admission+author, output_bytes=512*MIB, output_entries=4096,
        acquisition=dict(requests=32, reply_bytes=32*MIB, verify_attempts=1,
                         verification_input_bytes=16*MIB, worker_cpu_seconds=admission),
        imports=dict(max_sources=2, max_members=3, max_receipts=1, max_calls=4096,
                     submitted_bytes=64*MIB, data_bytes=16*MIB))


class Assets:
    def __init__(self, context):
        self.context = context
        params = deepcopy(dict(context.parameters)); C.fields(params, {"schema", "assets", "ports"})
        need(params["schema"] == PARAMETERS, "ACTUAL_PARAMETERS_SCHEMA")
        C.fields(params["assets"], set(RETAINED)); C.fields(params["ports"], {"router", "provider", "reader", "http"})
        ports = params["ports"]
        need(all(type(p) is int and 1024 <= p <= 65535 for p in ports.values())
             and len(set(ports.values())) == 4, "ACTUAL_DISTINCT_PORTS")
        self.ports, self.pins = ports, params["assets"]
        for name, row in self.pins.items():
            C.fields(row, {"path", "bytes", "sha256"}); ordinary(row["path"])
            need((row["bytes"], row["sha256"]) == RETAINED[name], "ACTUAL_RETAINED_IDENTITY:"+name)
        self.receipt = read_pin(self.pins["receipt"], MIB)
        self.bundle = C.parse_json(read_pin(self.pins["bundle"], MIB))
        self.foundation = read_pin(self.pins["foundation"], MIB)
        self.summary = C.summarize(self.bundle["spec"])
        need(C.summary_id(self.summary) == BASE, "ACTUAL_BASE_SUMMARY")
        template = parse(read_pin(self.pins["profile"], MIB))
        producer = template["producer"]
        need((producer["image_id"], producer["foundation"], producer["policy"])
             == (B.RELATION_IMAGE, B.FOUNDATION, B.POLICY), "ACTUAL_RETAINED_RELATION")
        old_install = Path(producer["supervisor_manifest"]["path"]).parent
        manifest_pin = {"path": str(context.installation/"RELEASE-MANIFEST.json"),
                        "bytes": producer["supervisor_manifest"]["bytes"], "sha256": MANIFEST}
        files = parse(read_pin(manifest_pin, 8*MIB))["files"]

        def installed(row):
            path = Path(row["path"])
            need(path.is_relative_to(old_install), "ACTUAL_TEMPLATE_RUNTIME_ROOT")
            relative = path.relative_to(old_install).as_posix()
            need(files.get(relative) == {k: row[k] for k in ("bytes", "sha256")},
                 "ACTUAL_TEMPLATE_MANIFEST_ROLE")
            return {**row, "path": str(context.installation/relative)}

        self.sources = {}
        for key, digest in context.source_sha256.items():
            if not key.startswith("v5/") or not key.endswith(".py"): continue
            path = context.sources_v5/key[3:]
            ordinary(path); size = path.stat().st_size
            need(0 < size <= 2*MIB, "ACTUAL_SOURCE_SIZE")
            row = {"path": str(path), "bytes": size, "sha256": digest}
            read_pin(row, 2*MIB)  # digest came from the selected plan, not this read.
            self.sources[key[3:]] = row
        need(len(self.sources) <= 120, "ACTUAL_SOURCE_MAP_CAP")
        need("authoring/worker.py" in self.sources, "ACTUAL_WORKER_MUST_BE_SELECTED")
        producer.update(supervisor_manifest=manifest_pin, host=deepcopy(self.pins["host"]),
            python=installed(producer["python"]), python_dll=installed(producer["python_dll"]),
            runtime_pins=[installed(row) for row in producer["runtime_pins"]],
            source_pins=[self.sources["production/__init__.py"], self.sources["production/producer.py"]])
        template.update(image=deepcopy(self.pins["image"]), worker=self.sources["authoring/worker.py"],
            native_executable=deepcopy(self.pins["frontend"]), source_pins=list(self.sources.values()))
        self.preparation = template
        self.producer = producer
        self.receipt_runtime = {row["path"]: {k: row[k] for k in ("bytes", "sha256")}
            for row in (producer["host"], producer["python"], producer["python_dll"], *producer["runtime_pins"])}
        self.native_runtime = {row["path"]: {k: row[k] for k in ("bytes", "sha256")}
            for row in (self.pins["native"], *self.sources.values())}

    def owners(self, workspace, grant, phase):
        """Return transferred client, or close every constructed owner on failure."""
        receipt = delta = preparation = None
        try:
            receipt = ReceiptVerifier(supervisor_manifest=self.producer["supervisor_manifest"]["path"],
                supervisor_manifest_sha256=MANIFEST, executable=self.pins["host"]["path"],
                runtime_pins=self.receipt_runtime, image_id=B.RELATION_IMAGE,
                foundation=B.FOUNDATION, policy=B.POLICY, operations=1, submitted_bytes=8*MIB,
                reserved_cpu_seconds=30, wall_seconds=grant.remaining_seconds())
            delta = MixedDeltaVerifier(legacy_verifier=receipt, aggregate_verifier=None,
                native_executable=self.pins["native"]["path"], runtime_pins=self.native_runtime,
                output_directory=grant.directory/"delta", envelope=Envelope(**workspace.config["packet_envelope"]),
                operations=1, submitted_bytes=16*MIB,
                reserved_cpu_seconds=grant.limits["acquisition"]["worker_cpu_seconds"],
                controller_cpu_seconds=90, wall_seconds=grant.remaining_seconds(),
                output_bytes=128*MIB, output_entries=1024)
            if phase != "cold":
                preparation = MixedOwnerPreparation(self.preparation,
                    dict(allowance_id=C.hash_value("ordinary-client-preparation", {"grant": grant.identifier}),
                        operations=1, worker_cpu_seconds=60, controller_cpu_seconds=90,
                        wall_seconds=grant.remaining_seconds(), output_bytes=256*MIB, output_entries=1024),
                    grant.directory/"preparation")
            return workspace.operation(grant, receipt_owner=receipt, delta_owner=delta,
                preparation_owner=preparation, foundation_bytes=self.foundation,
                foundation_sha256=self.pins["foundation"]["sha256"])
        except BaseException:
            for value in (preparation, delta, receipt):
                if value is not None: value.close()
            raise
