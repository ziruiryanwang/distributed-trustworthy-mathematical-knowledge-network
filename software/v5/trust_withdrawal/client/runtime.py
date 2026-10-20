"""Owner-adopted client construction, independent of any mathematical fixture.

This is trusted local configuration, not remote input or an authority loader.
All mathematical work remains in the existing exact owners and public client.
"""
from copy import deepcopy
import hashlib
import sys
from importlib import import_module
from pathlib import Path, PurePosixPath

from admission.verifier import ReceiptVerifier
from admission import trust as T
from aggregate_claims import bindings as B
from aggregate_claims.aggregate_admission import AggregateReceiptVerifier
from mixed_claims.authoring_atomic import MixedOwnerPreparation
from mixed_claims.packet import Envelope
from mixed_claims.receiver import MixedDeltaVerifier
from modules import codec as C
from production.producer import parse
from .workspace_atomic import OperationGrant

MIB = 1024**2
SCHEMA = "DMKN_V5_CLIENT_RUNTIME_V1"
MODES = {
    "atomic": "client.workspace_atomic",
    "mixed": "client.workspace_mixed",
    "evidence": "client.workspace_evidence",
    "staged": "client.workspace_staged",
    "validated": "client.workspace_validated",
}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def _ordinary(value, *, directory=False):
    path = Path(value)
    need(path.is_absolute() and str(path.resolve()) == str(path),
         "RUNTIME_CANONICAL_PATH")
    need((path.is_dir() if directory else path.is_file())
         and all(not item.is_symlink() and not item.is_junction()
                 for item in (path, *path.parents)), "RUNTIME_ORDINARY_PATH")
    return path


def _pin(row, maximum=128*MIB):
    C.fields(row, {"path", "bytes", "sha256"})
    C.digest_string(row["sha256"])
    need(type(row["path"]) is str and Path(row["path"]).is_absolute()
         and type(row["bytes"]) is int and 0 < row["bytes"] <= maximum,
         "RUNTIME_PIN_FIELDS")
    return Path(row["path"])


def read_pin(row, maximum=128*MIB):
    path = _ordinary(_pin(row, maximum))
    need(path.stat().st_size == row["bytes"], "RUNTIME_PIN_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(row["bytes"]+1)
    need(len(raw) == row["bytes"]
         and hashlib.sha256(raw).hexdigest() == row["sha256"],
         "RUNTIME_PIN_CHANGED")
    return raw


def _runtime(rows):
    result = {}
    for row in rows:
        _pin(row)
        key = row["path"]
        value = {name: row[name] for name in ("bytes", "sha256")}
        need(key not in result or result[key] == value, "RUNTIME_CONFLICTING_PIN")
        result[key] = value
    need(1 <= len(result) <= 128
         and sum(row["bytes"] for row in result.values()) <= 512*MIB,
         "RUNTIME_MAP_BOUND")
    return result


def _workspace_type(mode):
    need(type(mode) is str and mode in MODES, "RUNTIME_EXPLICIT_MODE")
    # A closed local mapping, never a peer-provided module or class name.
    return import_module(MODES[mode]).Workspace


def _support(configuration):
    """Stable selected-role identity, not a claim of a hermetic OS/DLL closure.

    Raw generated preparation-profile bytes and operation/source-root paths are
    intentionally excluded. Their actual selected role contents are included.
    Executable pins remain freshly checked by the original owners before use.
    """
    context = configuration["_context"]
    profile = configuration["_preparation"]
    adoption = configuration["_adoption"]
    installation = Path(configuration["_manifest"]["path"]).parent
    files = configuration["_files"]
    roles = {}

    def add(name, row):
        _pin(row)
        value = {key: row[key] for key in ("bytes", "sha256")}
        need(name not in roles or roles[name] == value, "RUNTIME_SUPPORT_ROLE_CONFLICT")
        roles[name] = value

    add("supervisor/manifest", configuration["_manifest"])
    for relative in ("operator/commons.py", "receiver/helpers/domains.py",
                     "receiver/helpers/run_stage.py"):
        row = {"path": str(installation/relative), **files[relative]}
        read_pin(row, 4*MIB)
        add("supervisor/"+relative, row)
    # The exact manifest commitment above includes the launcher's full Python
    # census (584 files in the current installation). Do not duplicate that
    # committed table into flat support roles. Its worker subset appears below.
    for relative, row in configuration["_sources"].items():
        add("source/v5/"+relative, row)
    source_root = _ordinary(context.sources_v5, directory=True)
    for name, digest in context.source_sha256.items():
        if not name.startswith("v5/") or name.endswith(".py"):
            continue
        relative = PurePosixPath(name[3:])
        need(not relative.is_absolute() and relative.as_posix() == name[3:]
             and all(part not in ("", ".", "..") and "\\" not in part
                     for part in relative.parts), "RUNTIME_SUPPORT_SOURCE_RELATIVE")
        path = _ordinary(source_root.joinpath(*relative.parts))
        need(path.is_relative_to(source_root), "RUNTIME_SUPPORT_SOURCE_ROOT")
        row = {"path": str(path), "bytes": path.stat().st_size, "sha256": digest}
        read_pin(row, 2*MIB)
        add("source/"+name, row)
    portable_root = _ordinary(context.sources_portable, directory=True)
    portable = 0
    for name, digest in context.source_sha256.items():
        if not name.startswith("portable/"):
            continue
        relative = PurePosixPath(name[len("portable/"):])
        need(not relative.is_absolute() and relative.as_posix() == name[len("portable/"):]
             and all(part not in ("", ".", "..") and "\\" not in part
                     for part in relative.parts), "RUNTIME_SUPPORT_SOURCE_RELATIVE")
        path = _ordinary(portable_root.joinpath(*relative.parts))
        need(path.is_relative_to(portable_root), "RUNTIME_SUPPORT_SOURCE_ROOT")
        row = {"path": str(path), "bytes": path.stat().st_size, "sha256": digest}
        read_pin(row, 2*MIB)
        add("source/"+name, row)
        portable += 1
        need(portable <= 128, "RUNTIME_SUPPORT_PORTABLE_BOUND")
    need(portable > 0, "RUNTIME_SUPPORT_PORTABLE_REQUIRED")
    producer = profile["producer"]
    for name in ("host", "python", "python_dll"):
        add("producer/"+name, producer[name])
    for row in producer["runtime_pins"]:
        path = _pin(row)
        need(path.is_relative_to(installation), "RUNTIME_SUPPORT_RUNTIME_ROOT")
        add("producer/runtime/"+path.relative_to(installation).as_posix(), row)
    for name in ("image", "native_executable", "worker"):
        add("author/"+name, profile[name])
    lean = _ordinary(profile["lean_root"], directory=True)
    rows = profile["lean_runtime_pins"]
    need(type(rows) is list and 1 <= len(rows) <= 128, "RUNTIME_SUPPORT_LEAN_COUNT")
    paths = set()
    for row in rows:
        path = _pin(row)
        need(path.is_relative_to(lean) and path not in paths, "RUNTIME_SUPPORT_LEAN_ROOT")
        paths.add(path)
        add("author/lean/"+path.relative_to(lean).as_posix(), row)
    add("verifier/native", adoption["native"])
    if adoption["receipt"] is not None:
        add("verifier/individual", adoption["receipt"])
    if adoption["aggregate"] is not None:
        add("verifier/aggregate", adoption["aggregate"]["executable"])
    result = {
        "schema": "DMKN_LOCAL_TRUST_SUPPORT_V1",
        "identities": {
            "relation_image": B.RELATION_IMAGE,
            "aggregate_image": (None if adoption["aggregate"] is None else
                                adoption["aggregate"]["image"]),
            "foundation": B.FOUNDATION, "policy": B.POLICY,
            "receipt_scheme": "resolved-succinct-poseidon2",
        },
        "roles": roles,
    }
    T.support_id(result)
    return result


class RuntimeProfile:
    """Pinned configuration only; contains no receipt, warrant or chosen theorem."""

    @staticmethod
    def _configuration(context, adoption):
        context.remaining_seconds()
        value = deepcopy(adoption)
        C.fields(value, {"schema", "preparation_profile", "native", "receipt", "aggregate"})
        need(value["schema"] == SCHEMA, "RUNTIME_SCHEMA")
        _pin(value["native"])
        if value["receipt"] is not None:
            _pin(value["receipt"])
        if value["aggregate"] is not None:
            C.fields(value["aggregate"], {"executable", "image"})
            _pin(value["aggregate"]["executable"])
            B._adopted_image(value["aggregate"]["image"])
        need(value["receipt"] is not None or value["aggregate"] is not None,
             "RUNTIME_ISSUER_REQUIRED")

        profile = parse(read_pin(value["preparation_profile"], MIB))
        C.fields(profile, {"schema", "producer", "image", "worker", "native_executable",
                           "lean_root", "lean_runtime_pins", "source_pins"})
        need(profile["schema"] == "DMKN_V5_PREPARATION_PROFILE_V1",
             "RUNTIME_PREPARATION_PROFILE")
        producer = profile["producer"]
        C.fields(producer, {"schema", "supervisor_manifest", "host", "python", "python_dll",
                           "source_pins", "runtime_pins", "image_id", "foundation", "policy"})
        need(producer["schema"] == "DMKN_V5_PRODUCER_PROFILE_V1"
             and (producer["image_id"], producer["foundation"], producer["policy"])
             == (B.RELATION_IMAGE, B.FOUNDATION, B.POLICY), "RUNTIME_RELATION_POLICY")
        for key in ("supervisor_manifest", "host", "python", "python_dll"):
            _pin(producer[key])
        need(type(producer["runtime_pins"]) is list and len(producer["runtime_pins"]) <= 128,
             "RUNTIME_TEMPLATE_RUNTIME_COUNT")
        old_install = Path(producer["supervisor_manifest"]["path"]).parent
        installation = _ordinary(context.installation, directory=True)
        manifest = {**producer["supervisor_manifest"],
                    "path": str(installation/"RELEASE-MANIFEST.json")}
        files = parse(read_pin(manifest, 8*MIB))["files"]
        need(type(files) is dict and len(files) <= 20000, "RUNTIME_MANIFEST_FILES")

        def installed(row):
            path = _pin(row)
            need(path.is_relative_to(old_install), "RUNTIME_TEMPLATE_INSTALL_ROOT")
            relative = path.relative_to(old_install).as_posix()
            need(files.get(relative) == {key: row[key] for key in ("bytes", "sha256")},
                 "RUNTIME_TEMPLATE_MANIFEST_ROLE")
            return {**row, "path": str(installation/relative)}

        root = _ordinary(context.sources_v5, directory=True)
        need(root/"client/runtime.py" == Path(__file__).resolve(),
             "RUNTIME_LOADED_SOURCE_ORIGIN")
        sources = {}
        for key, digest in context.source_sha256.items():
            if not key.startswith("v5/") or not key.endswith(".py"):
                continue
            relative = PurePosixPath(key[3:])
            need(not relative.is_absolute() and relative.as_posix() == key[3:]
                 and all(part not in ("", ".", "..") and "\\" not in part
                         for part in relative.parts), "RUNTIME_SOURCE_RELATIVE_PATH")
            path = _ordinary(root.joinpath(*relative.parts))
            need(path.is_relative_to(root), "RUNTIME_SOURCE_ROOT")
            C.digest_string(digest)
            row = {"path": str(path), "bytes": path.stat().st_size, "sha256": digest}
            # Digest authority is the selected launcher map, not this file read.
            read_pin(row, 2*MIB)
            sources[relative.as_posix()] = row
            need(len(sources) <= 120, "RUNTIME_SOURCE_MAP_BOUND")
        need({"client/runtime.py", "production/producer.py", "production/__init__.py",
              "authoring/worker.py", "admission/trust.py"} <= set(sources),
             "RUNTIME_SOURCE_CLOSURE")
        need(T is sys.modules.get("admission.trust")
             and Path(T.__file__).resolve() == root/"admission/trust.py",
             "RUNTIME_TRUST_SOURCE_ORIGIN")
        producer.update(supervisor_manifest=manifest,
            python=installed(producer["python"]), python_dll=installed(producer["python_dll"]),
            runtime_pins=[installed(row) for row in producer["runtime_pins"]],
            source_pins=[sources["production/__init__.py"], sources["production/producer.py"]])
        # External host, Lean, image and frontend roles retain the owner's exact
        # pins. Relocation of those assets requires an explicitly adopted profile.
        profile.update(worker=sources["authoring/worker.py"], source_pins=list(sources.values()))
        runtime = [producer["python"], producer["python_dll"], *producer["runtime_pins"]]
        configuration = {
            "_context": context, "_adoption": value, "_preparation": profile,
            "_sources": sources, "_manifest": manifest, "_files": files,
            "_receipt_runtime": (None if value["receipt"] is None else
                                 _runtime([value["receipt"], *runtime, *sources.values()])),
            "_aggregate_runtime": (None if value["aggregate"] is None else
                                   _runtime([value["aggregate"]["executable"], *runtime, *sources.values()])),
            "_native_runtime": _runtime([value["native"], *sources.values()]),
        }
        context.remaining_seconds()
        return configuration

    @classmethod
    def support_manifest(cls, context, adoption):
        """Inert source-validated selection for explicit owner adoption.

        Creates no domain, verifier, allowance or acceptance authority. A fresh
        description never replaces missing/withdrawn persisted policy state.
        """
        need(cls is RuntimeProfile, "RUNTIME_EXACT_PROFILE")
        result = _support(cls._configuration(context, adoption))
        context.remaining_seconds()
        return result

    @classmethod
    def from_context(cls, context, adoption, *, trust_domain):
        """Bind ordinary startup to an explicitly opened persistent domain."""
        need(cls is RuntimeProfile and type(trust_domain) is T.TrustDomain,
             "RUNTIME_EXACT_TRUST_DOMAIN")
        binding = trust_domain.bind()
        identity = T.check_binding(binding)
        configuration = cls._configuration(context, adoption)
        support = _support(configuration)
        need(T.support_id(support) == identity["support_id"],
             "RUNTIME_ADOPTED_SUPPORT_MISMATCH")
        self = cls.__new__(cls)
        self.__dict__.update(configuration)
        self._trust_domain, self._trust_binding = trust_domain, binding
        self._trust_original = (trust_domain, binding)
        self._trust_identity, self._support = deepcopy(identity), support
        self._selection = C.canonical(self.describe())
        context.remaining_seconds()
        self._check_trust()
        return self

    def _check_trust(self):
        need(type(self._trust_domain) is T.TrustDomain
             and type(self._trust_binding) is T.TrustBinding
             and self._trust_original[0] is self._trust_domain
             and self._trust_original[1] is self._trust_binding
             and self._trust_binding._domain is self._trust_domain,
             "RUNTIME_ORIGINAL_TRUST_BINDING")
        need(T is sys.modules.get("admission.trust")
             and Path(T.__file__).resolve() == Path(self._sources["admission/trust.py"]["path"]),
             "RUNTIME_TRUST_SOURCE_ORIGIN")
        need(T.check_binding(self._trust_binding) == self._trust_identity,
             "RUNTIME_TRUST_IDENTITY_CHANGED")

    def describe(self):
        """Copied configuration, not mathematical or execution authority."""
        return deepcopy({"manifest": self._manifest, "preparation": self._preparation, "sources": self._sources,
            "receipt_runtime": self._receipt_runtime, "aggregate_runtime": self._aggregate_runtime,
            "native_runtime": self._native_runtime, "adoption": self._adoption,
            "trust": self._trust_identity, "support": self._support})

    def open_operation(self, workspace, grant, *, mode, foundation_bytes,
                       foundation_sha256, authoring=False):
        """Construct after reserve; transfer only on success; never launch a proof."""
        self._check_trust()
        need(type(authoring) is bool, "RUNTIME_AUTHORING_FLAG")
        need(C.canonical(self.describe()) == self._selection, "RUNTIME_PROFILE_CHANGED")
        self._context.remaining_seconds()
        need(type(workspace) is _workspace_type(mode), "RUNTIME_EXACT_WORKSPACE_MODE")
        workspace._active()
        workspace._grant_active(grant)
        need(type(grant) is OperationGrant and grant._workspace is workspace
             and not grant._used and workspace._client is None and not workspace._poisoned,
             "RUNTIME_UNUSED_OWN_GRANT")
        need(grant.deadline <= self._context.deadline, "RUNTIME_ORIGINAL_OUTER_DEADLINE")
        use_a = mode != "atomic"
        need((not use_a and self._adoption["receipt"] is not None
              and self._adoption["aggregate"] is None)
             or (use_a and self._adoption["aggregate"] is not None),
             "RUNTIME_NO_ISSUER_DOWNGRADE")
        if use_a:
            need(workspace.config["wire_profile"]["aggregate_image"]
                 == self._adoption["aggregate"]["image"], "RUNTIME_WORKSPACE_IMAGE")
        need(type(foundation_bytes) is bytes and 0 < len(foundation_bytes) <= 16*MIB
             and hashlib.sha256(foundation_bytes).hexdigest() == foundation_sha256,
             "RUNTIME_FOUNDATION_PIN")
        caps = grant.limits
        acq = caps["acquisition"]
        need(len(foundation_bytes) <= caps["input_bytes"], "RUNTIME_FOUNDATION_LIMIT")
        envelope = Envelope(**workspace.config["packet_envelope"])
        envelope.validate()
        author_cpu = caps["worker_cpu_seconds"]-acq["worker_cpu_seconds"]
        need(not authoring or author_cpu >= 1, "RUNTIME_AUTHOR_SUBALLOCATION")
        receipt = aggregate = delta = preparation = None
        common = dict(trust_binding=self._trust_binding,
            supervisor_manifest=self._manifest["path"],
            supervisor_manifest_sha256=self._manifest["sha256"],
            # One public packet admission may consume several receipt claims.
            # CPU and bytes stay within the SAME acquisition suballocation.
            operations=min(acq["verify_attempts"]*envelope.claims, 4096),
            submitted_bytes=acq["verification_input_bytes"],
            reserved_cpu_seconds=acq["worker_cpu_seconds"])
        try:
            if self._adoption["receipt"] is not None:
                receipt = ReceiptVerifier(**common, executable=self._adoption["receipt"]["path"],
                    runtime_pins=deepcopy(self._receipt_runtime), image_id=B.RELATION_IMAGE,
                    foundation=B.FOUNDATION, policy=B.POLICY, wall_seconds=grant.remaining_seconds())
            if use_a:
                aggregate = AggregateReceiptVerifier(**common,
                    executable=self._adoption["aggregate"]["executable"]["path"],
                    aggregate_image=self._adoption["aggregate"]["image"],
                    runtime_pins=deepcopy(self._aggregate_runtime), wall_seconds=grant.remaining_seconds(),
                    member_calls=caps["imports"]["max_calls"], member_storage=caps["imports"]["max_members"],
                    member_bytes=min(caps["input_bytes"], 256*MIB),
                    controller_cpu_seconds=caps["controller_cpu_seconds"],
                    output_bytes=caps["output_bytes"], output_entries=caps["output_entries"])
            delta = MixedDeltaVerifier(legacy_verifier=receipt, aggregate_verifier=aggregate,
                native_executable=self._adoption["native"]["path"],
                runtime_pins=deepcopy(self._native_runtime), output_directory=grant.directory/"delta",
                envelope=envelope,
                operations=min(acq["verify_attempts"], 128), submitted_bytes=common["submitted_bytes"],
                reserved_cpu_seconds=common["reserved_cpu_seconds"],
                controller_cpu_seconds=caps["controller_cpu_seconds"],
                wall_seconds=grant.remaining_seconds(),
                output_bytes=caps["output_bytes"], output_entries=caps["output_entries"])
            if authoring:
                preparation = MixedOwnerPreparation(deepcopy(self._preparation),
                    dict(allowance_id=C.hash_value("ordinary-runtime-preparation", {"grant": grant.identifier}),
                        operations=min(caps["calls"], 16), worker_cpu_seconds=min(author_cpu, 3600),
                        controller_cpu_seconds=min(caps["controller_cpu_seconds"], 600),
                        wall_seconds=grant.remaining_seconds(), output_bytes=min(caps["output_bytes"], 1024*MIB),
                        output_entries=min(caps["output_entries"], 4096)), grant.directory/"preparation")
            kwargs = dict(receipt_owner=receipt, delta_owner=delta, preparation_owner=preparation,
                          foundation_bytes=foundation_bytes, foundation_sha256=foundation_sha256)
            if use_a:
                kwargs["aggregate_owner"] = aggregate
            # Construction linearizes at this final live check. No owner callback
            # or await occurs before transfer. A later external-process withdrawal
            # is observed at the next issuer gate; no atomic cross-process recall
            # is claimed. Preserve workspace's original transfer/cleanup contract.
            self._check_trust()
            return workspace.operation(grant, **kwargs)
        except BaseException as error:
            failures = []
            for owner in (preparation, delta, aggregate, receipt):
                if owner is not None:
                    try:
                        owner.close()
                    except BaseException as cleanup:
                        failures.append(cleanup)
            if failures:
                workspace._poisoned = True
                raise BaseExceptionGroup("RUNTIME_OWNER_CONSTRUCTION_CLEANUP", [error, *failures])
            raise

