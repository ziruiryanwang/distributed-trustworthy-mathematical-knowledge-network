"""Project owner-recorded names for search without reading proof snapshots.

This auxiliary helper does not replace the installed admission controller. Its
private reader retains that controller's catalog metadata validation and local
lifecycle, but never supplies a module loading plan or mathematical authority.
The caller must verify this helper's package pin before executing it.
"""
from __future__ import annotations

import sys

__all__ = ["project", "snapshot"]
MAX_NAMES = 8
MAX_INPUT_BYTES = 65536
MAX_DIRECTORY_NAMES = 1048576


def _need(condition, code):
    if not condition:
        raise ValueError(code)


def _read(installation, catalog_directory, store_id, local_root, names, *,
          limits, check, catalog_module, full=False):
    """Shared private metadata reader; never expose a native module plan."""
    P = catalog_module
    A = sys.modules.get("ordinary_admission")
    _need(A is not None and P is sys.modules.get("portable_catalog") and
          P is A.P, "ADVISORY_CATALOG_MODULE")
    C, E, S = P.L, P.E, P.S
    _need(A.C is C and A.E is E and A.S is S and
          type(installation) is A.NativeInstallation and type(limits) is P.Limits
          and callable(check), "ADVISORY_CONFIGURATION")
    check()
    P.hexid(store_id); P.hexid(local_root)
    _need(type(full) is bool, "ADVISORY_MODE")
    if full:
        _need(names is None, "ADVISORY_DIRECTORY_NO_NAME_SUBSET")
        captured, keys = [], []
    else:
        _need(type(names) is list and 1 <= len(names) <= MAX_NAMES,
              "ADVISORY_NAME_COUNT")
        # Detach the bounded request before opening protected state.
        names_raw = E.canonical_json(names)
        _need(0 < len(names_raw) <= MAX_INPUT_BYTES, "ADVISORY_NAME_BYTES")
        captured = E.strict_json(names_raw, E.Limits(max_bytes=MAX_INPUT_BYTES))
        keys = [E.name_key(name) for name in captured]
        _need(len(set(keys)) == len(keys), "ADVISORY_DUPLICATE_NAME")
    directory = C.ordinary(catalog_directory, directory=True)
    for support in (installation.root, *installation.runtime_roots.values()):
        _need(not directory.is_relative_to(support) and
              not support.is_relative_to(directory), "ADVISORY_STORAGE_SUPPORT_OVERLAP")

    class _AdvisoryCatalog(P.PortableCatalog):
        # The base opener uses cls.__new__, not __init__, and can call context
        # before returning. All override state therefore uses getattr defaults.
        @classmethod
        def _open(cls, directory, implementation_raw, store_id, *, create, limits, importing):
            _need(create is False and importing is None, "ADVISORY_EXISTING_ACTIVE_ONLY")
            return super()._open(directory, implementation_raw, store_id,
                                 create=False, limits=limits, importing=None)

        @classmethod
        def _create_importing(cls, *args, **kwargs):
            raise ValueError("ADVISORY_NO_ADMISSION_CAPABILITY")

        def _deny(self, *args, **kwargs):
            raise ValueError("ADVISORY_NO_ADMISSION_CAPABILITY")

        reserve_basis = reserve_extension = _reserve = _commit_checked = _deny
        _activate_import = _flush_import_tree = _import_active = abandon = _deny

        def _root_row(self, root):
            check()
            result = super()._root_row(root)
            check()
            return result

        def _validate_record(self, raw, row, import_doc, import_roots):
            check()
            _need(getattr(self, "_advisory_snapshot", None) is None,
                  "ADVISORY_NESTED_RECORD")
            P.fields(row.get("snapshot"), ("module_name", "parent_module", "relative_path",
                     "artifact_bytes", "artifact_sha256", "writer_origin"),
                     "ADVISORY_SNAPSHOT_FIELDS")
            snapshot = row["snapshot"]
            provenance = row.get("provenance")
            _need(type(provenance) is dict, "ADVISORY_SNAPSHOT_PROVENANCE")
            if row.get("origin") == "native-check":
                relative = "operations/"+P.hexid(provenance.get("operation_id"))+"/chunk.olean"
            elif row.get("origin") == "legacy-translation":
                import_id = P.hexid(provenance.get("import_id"))
                ordinal = P.uint(provenance.get("ordinal"), 0, self._limits.max_roots-1,
                                 "ADVISORY_IMPORT_ORDINAL")
                relative = "imports/"+import_id+"/"+str(ordinal)+"/chunk.olean"
            else:
                raise ValueError("ADVISORY_SNAPSHOT_ORIGIN")
            _need(snapshot["relative_path"] == relative, "ADVISORY_SNAPSHOT_PATH")
            size = P.uint(snapshot["artifact_bytes"], 1, self._limits.max_artifact_bytes,
                          "CATALOG_ARTIFACT_SIZE")
            expected = P.hexid(snapshot["artifact_sha256"])
            self._advisory_snapshot = (relative, size, expected)
            try:
                # The pinned base reaches its final _artifact only AFTER all
                # record, operation/import, source-record and path predicates.
                result = super()._validate_record(raw, row, import_doc, import_roots)
            finally:
                self._advisory_snapshot = None
            check()
            return result

        def _artifact(self, relative, size, expected, *, maximum=None):
            check()
            snapshot = getattr(self, "_advisory_snapshot", None)
            if snapshot is None:
                # In particular, imported audit.json retains its original byte
                # verification. Source-record/correspondence reads are unchanged.
                result = super()._artifact(relative, size, expected, maximum=maximum)
            else:
                _need(maximum is None and (relative, size, expected) == snapshot,
                      "ADVISORY_ARTIFACT_SCOPE")
                P.uint(size, 1, self._limits.max_artifact_bytes, "CATALOG_ARTIFACT_SIZE")
                P.hexid(expected)
                # Lexical internal value only: do not stat/open the snapshot or
                # add it to _verified_artifacts. No module plan escapes project.
                result = self._root.joinpath(*relative.split("/"))
            check()
            return result

    reader = None
    try:
        check()
        reader = _AdvisoryCatalog.open(directory, installation.implementation_raw,
                                      store_id, create=False, limits=limits)
        context = reader.context(local_root)
        check()
        _need(context["local_root"] == local_root and
              context["semantic_id"] == installation.semantic_id and
              context["foundation_id"] == S.foundation_id() and
              context["implementation_id"] == installation.implementation_id,
              "ADVISORY_CONTEXT_IDENTITY")
        bindings, missing = {}, []
        if full:
            _need(1 <= len(context["bindings"]) <= MAX_DIRECTORY_NAMES,
                  "ADVISORY_DIRECTORY_NAME_COUNT")
            # The inherited metadata validator produced canonical bytes keys and
            # hex IDs. Copy only these immutable values, never modules or handles.
            for key, symbol in context["bindings"].items():
                check()
                _need(type(key) is bytes, "ADVISORY_DIRECTORY_NAME_KEY")
                bindings[key] = P.hexid(symbol)
        else:
            for name, key in zip(captured, keys):
                check()
                if key in context["bindings"]:
                    bindings[key] = P.hexid(context["bindings"][key])
                else:
                    missing.append(name)
        result = {key: context[key] for key in
                  ("local_root", "semantic_id", "foundation_id", "implementation_id")}
        result.update(store_id=store_id, bindings=bindings, missing_names=missing,
                      snapshot_integrity="NOT_CHECKED", context_readiness="NOT_ASSERTED",
                      mathematical_acceptance=False)
        if full:
            result.update(binding_count=len(bindings),
                          coverage="COMPLETE_RECORDED_BINDINGS_AT_SELECTED_ROOT")
        reader._active()
        check()
    finally:
        if reader is not None:
            reader.close()
            _need(reader._closed and reader._db is None and reader._lock is None,
                  "ADVISORY_OWNER_CLOSURE")
    check()
    result["owner_closure"] = "CLOSED"
    return result


def project(installation, catalog_directory, store_id, local_root, names, *,
            limits, check, catalog_module):
    """Project one through eight names, preserving the original query contract."""
    return _read(installation, catalog_directory, store_id, local_root, names,
                 limits=limits, check=check, catalog_module=catalog_module)


def snapshot(installation, catalog_directory, store_id, local_root, *,
             limits, check, catalog_module):
    """Detach all recorded bindings after full metadata validation and close.

    This is one historical export input, never a current-state or load-readiness
    warrant. It opens no custody, reads no proof snapshots and executes no worker.
    The caller must preserve the exact root/provenance and publish only after
    checking its remaining allocation and selected software.
    """
    return _read(installation, catalog_directory, store_id, local_root, None,
                 limits=limits, check=check, catalog_module=catalog_module, full=True)
