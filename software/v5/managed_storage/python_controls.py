"""Seven finite storage-helper controls; root selects execution separately.

Actual pinned SP/SF and full formal_features execute. Only the exact ordinary
function is AST-extracted from pinned discovery_store; no store/manager module
is imported. Static caller order checks are labeled separately from actual
tiny named-file SQLite tests. Every synthetic fixture remains; no deletion.
"""
import argparse
import ast
from copy import deepcopy
import hashlib
import os
from pathlib import Path
import sqlite3
import stat
import sys
import time
from types import ModuleType
import unittest


PROJECT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OUTPUT = PROJECT / "experiments/v5-local-checks/managed-storage-python-controls-01"
RELATIVE = Path("software/v5/managed_storage/python_controls.py")
PREFIX = "software/v5/managed_storage/"
FEATURE = "software/v5/instantiation_discovery/discovery/formal_features.py"
PROFILE = PREFIX + "placement/storage_profile.py"
PATHS = PREFIX + "placement/storage_paths.py"
ORDINARY = PREFIX + "discovery/discovery_store.py"
MANAGER = PREFIX + "placement/lifecycle.py"
PINS = {
    "software/v5/instantiation_discovery/discovery/formal_features.py": (10826, "8822c8186ba120da9c8b72abe6d0c905eeaced5af46ef19600e463904a6d1b0c"),
    "software/v5/managed_storage/placement/storage_profile.py": (9331, "3b535a337c1731ead3b9930c7cbe1f7c340a17152bd8b57e32981552ec061c90"),
    "software/v5/managed_storage/placement/storage_paths.py": (7490, "e1bcba2730e432b4dfc428d9c56ebb2e5b7bc0f4d8a9bfa0751b8818557eb9da"),
    "software/v5/managed_storage/placement/lifecycle.py": (39828, "0fa3dcc4285aa4afc87dfda5741e5c68334f8c0398138c3f218351e705a1f427"),
    "software/v5/managed_storage/client/workspace_evidence.py": (51821, "d94e38257444da3bda04e4d9b298d422280a573becc27eaa063fdbc01f9c02a2"),
    "software/v5/managed_storage/custody/module_store.py": (10754, "580515e461c95b424bc59011b8bf87e4776039f7d6cb87c27599f295c602dcbb"),
    "software/v5/managed_storage/evidence_network/custody.py": (8385, "4264841e55ebc21899d8967ef9ac439d0682da5ea4a0d1c2097eddc930f1300e"),
    "software/v5/managed_storage/discovery/discovery_store.py": (20113, "7f3c884b3ef3455e51563d233a2ca4a19087bc8097186e6b43e949abededa2c5"),
    "software/v5/managed_storage/placement/ledger.py": (12758, "59f87b9334c44a8a9f8feb236084f419081d2484582917aded55eaac15f8351d"),
    "software/v5/managed_storage/placement/advertisement.py": (23475, "13b0ef1ae400990f237e5e1957a77008d7f2ac51fb96758560152cfda3ecdf28"),
}
OPENERS = (
    ("placement/lifecycle.py", "ManagedGenerations", "open"),
    ("client/workspace_evidence.py", "Workspace", "open"),
    ("custody/module_store.py", "ModuleStore", "__init__"),
    ("evidence_network/custody.py", "PacketStore", "__init__"),
    ("discovery/discovery_store.py", "Store", "__init__"),
    ("placement/ledger.py", "PlacementLedger", "open"),
    ("placement/advertisement.py", "PlacementAdvertisement", "open"),
)
F = SP = SF = FIXTURES = None
RAW = {}
OBSERVED = {"refusals": 0, "static_openers": []}
STARTED = None


def need(ok, code):
    if not ok:
        raise ValueError(code)


def runner_path(path):
    need(path.is_absolute() and path.resolve() == path and all(
        not item.is_symlink() and not item.is_junction() for item in (path, *path.parents)),
        "CONTROL_ORDINARY_RUNNER_PATH")
    return path


def pin(path, size, digest):
    runner_path(path)
    need(path.is_file() and path.stat().st_size == size, "CONTROL_SOURCE_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(size + 1)
    need(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, "CONTROL_SOURCE_PIN")
    return raw


def module(name, path, raw=None, package=False):
    need(name not in sys.modules, "CONTROL_MODULE_ALREADY_PRESENT")
    value = ModuleType(name)
    value.__file__ = str(path)
    value.__package__ = name if package else name.rpartition(".")[0]
    if package:
        value.__path__ = []  # No implicit SDK imports from the filesystem.
    sys.modules[name] = value
    if raw is not None:
        exec(compile(raw, str(path), "exec", dont_inherit=True), value.__dict__)
    return value


def adopt(sources):
    global F, SP, SF, RAW
    RAW = {name: pin(sources / name, *row) for name, row in PINS.items()}
    discovery = module("discovery", sources / ORDINARY, package=True)
    F = module("discovery.formal_features", sources / FEATURE, RAW[FEATURE])
    discovery.formal_features = F
    tree = ast.parse(RAW[ORDINARY], filename=str(sources / ORDINARY))
    definitions = [node for node in tree.body
                   if isinstance(node, ast.FunctionDef) and node.name == "ordinary"]
    need(len(definitions) == 1 and not definitions[0].decorator_list,
         "CONTROL_EXACT_ORDINARY_EXTRACTION")
    selected = module("discovery.discovery_store", sources / ORDINARY)
    selected.__dict__.update(os=os, stat=stat, Path=Path, need=F.need)
    exec(compile(ast.Module(body=definitions, type_ignores=[]), str(sources / ORDINARY),
                 "exec", dont_inherit=True), selected.__dict__)
    discovery.discovery_store = selected
    placement = module("placement", sources / PROFILE, package=True)
    SP = module("placement.storage_profile", sources / PROFILE, RAW[PROFILE])
    placement.storage_profile = SP
    SF = module("placement.storage_paths", sources / PATHS, RAW[PATHS])
    placement.storage_paths = SF
    # The lazy dependency resolves to the exact extracted function, not a clone.
    need(SF._ordinary.__globals__["SP"] is SP and SP.F is SF.F is F,
         "CONTROL_ACTUAL_HELPER_BINDING")


def guard():
    need(STARTED is not None and time.monotonic() - STARTED < 35,
         "CONTROL_ORIGINAL_INTERNAL_DEADLINE")


def directory(name):
    guard()
    path = FIXTURES / name
    need(path.parent == FIXTURES and not os.path.lexists(path), "CONTROL_FRESH_FIXTURE")
    path.mkdir()
    return path


def write_new(path, raw):
    guard()
    need(type(raw) is bytes and len(raw) <= 300000 and path.is_relative_to(FIXTURES),
         "CONTROL_FIXTURE_WRITE_BOUND")
    need(not os.path.lexists(path), "CONTROL_FRESH_FILE")
    with path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "CONTROL_FIXTURE_WRITE")


def census(root):
    """Bounded, test-owned tree only. Capture contents to prove refusal preservation."""
    pending, files, directories, total = [root], {}, [], 0
    while pending:
        parent = pending.pop()
        runner_path(parent)
        directories.append(parent.relative_to(root).as_posix())
        with os.scandir(parent) as entries:
            for entry in entries:
                need(len(files) + len(directories) + len(pending) < 128,
                     "CONTROL_FIXTURE_ENTRY_CAP")
                path = parent / entry.name
                runner_path(path)
                info = path.lstat()
                if stat.S_ISDIR(info.st_mode):
                    pending.append(path)
                else:
                    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
                         "CONTROL_FIXTURE_FILE_KIND")
                    need(0 <= info.st_size <= 1024**2, "CONTROL_FIXTURE_FILE_CAP")
                    total += info.st_size
                    need(total <= 1024**2, "CONTROL_TOTAL_FIXTURE_CAP")
                    with path.open("rb") as stream:
                        raw = stream.read(info.st_size + 1)
                    need(len(raw) == info.st_size, "CONTROL_FIXTURE_CHANGED")
                    files[path.relative_to(root).as_posix()] = {
                        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    return {"files": files, "directories": sorted(directories), "bytes": total}


def configs(runs=2):
    """Storage-bearing synthetic inputs only, not a complete service configuration."""
    database = 139272 * 256 + 327680
    generation_bytes = 6 * database + runs * (database + 34816) + 131073
    registry_bytes = 139272 * 64 + 327680 + 131073
    manager = {
        "registry_pages": 64, "registry_reserved_bytes": registry_bytes,
        "cleanup_reserved_bytes": 1, "owner_reserved_bytes": 2 * generation_bytes + registry_bytes + 1,
        "slots": [{"reserved_bytes": generation_bytes, "max_runs": runs} for unused in range(2)]}
    generation = {
        "workspace": {"ledger_pages": 256, "module_limits": {"db_pages": 256},
                      "packet_limits": {"db_pages": 256}, "index_limits": {"max_db_pages": 256}},
        "placement": {"ledger_pages": 256, "max_runs": runs},
        "service_limits": {"journal_pages": 256},
        "location": {"limits": {"metadata": {
            "entries": 32, "bytes": 65536, "valueBytes": 1024, "providersPerKey": 1, "pages": 256}}}}
    return manager, generation


def set_at(value, keys, replacement):
    for key in keys[:-1]:
        value = value[key]
    value[keys[-1]] = replacement


def qualified(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = qualified(node.value)
        return base + "." + node.attr if base else node.attr
    return ""


def calls(node, name):
    return sorted((child for child in ast.walk(node)
                   if isinstance(child, ast.Call) and qualified(child.func) == name),
                  key=lambda child: (child.lineno, child.col_offset))


def method(tree, class_name, name):
    owners = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == class_name]
    need(len(owners) == 1, "CONTROL_AST_CLASS")
    functions = [node for node in owners[0].body
                 if isinstance(node, ast.FunctionDef) and node.name == name]
    need(len(functions) == 1, "CONTROL_AST_METHOD")
    return functions[0]


def keyword(call, name):
    values = [item.value for item in call.keywords if item.arg == name]
    need(len(values) == 1, "CONTROL_AST_KEYWORD")
    return ast.dump(values[0], include_attributes=False)


class Controls(unittest.TestCase):
    def refused(self, expected, action):
        with self.assertRaises(ValueError) as captured:
            action()
        self.assertEqual(str(captured.exception), expected)
        OBSERVED["refusals"] += 1

    def preserved_refusal(self, root, expected, action):
        before = census(root)
        self.refused(expected, action)
        self.assertEqual(census(root), before)

    def test_01_strict_arithmetic_exact_fit_all_runs(self):
        for count in (64, 256, 4096, 268435456):
            bound = SP.database_envelope(count)
            self.assertEqual(bound["main_bytes"], 4096 * count)
            self.assertEqual(bound["total_bytes"], 139272 * count + 327680)
            self.assertEqual(bound["main_bytes"] + bound["journal_bytes"], bound["total_bytes"])
        for bad in (True, False, 64.0, "64", None, 63, 268435457):
            self.refused("MANAGED_STORAGE_PAGE_CAP", lambda bad=bad: SP.database_envelope(bad))
        manager, generation = configs()
        registry = SP.registry_envelope(manager)
        envelope = SP.generation_envelope(manager, 0, generation)
        self.assertEqual(registry["registry_bound_bytes"], manager["registry_reserved_bytes"])
        self.assertEqual(registry["owner_charged_bytes"], manager["owner_reserved_bytes"])
        self.assertEqual(envelope["generation_bound_bytes"], manager["slots"][0]["reserved_bytes"])
        self.assertEqual(envelope["configured_runs"], 2)
        self.assertEqual(envelope["possible_files"], 26)
        self.assertEqual(envelope["possible_directories"], 12)
        self.assertEqual(envelope["possible_entries"], 38)
        self.assertFalse(envelope["physical_envelope_adopted"])
        self.assertFalse(registry["cleanup_progress_guaranteed"])
        for bad_value in (True, 64.0, "64", None, 63, 4097):
            bad = deepcopy(manager)
            bad["registry_pages"] = bad_value
            self.refused("MANAGED_STORAGE_REGISTRY_PAGES", lambda bad=bad: SP.registry_envelope(bad))
        for key in ("owner_reserved_bytes", "registry_reserved_bytes", "cleanup_reserved_bytes"):
            bad = deepcopy(manager)
            bad[key] = True
            self.refused("MANAGED_STORAGE_RESERVATION:" + key,
                         lambda bad=bad: SP.registry_envelope(bad))
        self.refused("MANAGED_STORAGE_SLOT", lambda: SP.generation_envelope(manager, True, generation))
        bad = deepcopy(generation)
        bad["placement"]["max_runs"] = True
        self.refused("MANAGED_STORAGE_RUNS", lambda: SP.generation_envelope(manager, 0, bad))
        for key, code in (("registry_reserved_bytes", "MANAGED_STORAGE_REGISTRY_RESERVATION"),
                          ("owner_reserved_bytes", "MANAGED_STORAGE_OWNER_RESERVATION")):
            bad = deepcopy(manager)
            bad[key] -= 1
            self.refused(code, lambda bad=bad: SP.registry_envelope(bad))
        bad = deepcopy(manager)
        bad["slots"][0]["reserved_bytes"] -= 1
        self.refused("MANAGED_STORAGE_GENERATION_RESERVATION",
                     lambda: SP.generation_envelope(bad, 0, generation))
        bad = deepcopy(manager)
        bad["slots"][0]["max_runs"] = 1
        self.refused("MANAGED_STORAGE_SLOT_RUN_CAP",
                     lambda: SP.generation_envelope(bad, 0, generation))
        # Each configured run is charged even though there is no active-run field.
        three, third = configs(3)
        extra = SP.generation_envelope(three, 0, third)["generation_bound_bytes"]
        self.assertEqual(extra - envelope["generation_bound_bytes"], 139272 * 256 + 327680 + 34816)
        # Both slots, including an entirely unused one, remain charged.
        bad = deepcopy(manager)
        bad["slots"][1]["reserved_bytes"] += 1
        self.refused("MANAGED_STORAGE_OWNER_RESERVATION", lambda: SP.registry_envelope(bad))
        cap_paths = (
            (("workspace", "ledger_pages"), 65536),
            (("workspace", "module_limits", "db_pages"), 268435456),
            (("workspace", "packet_limits", "db_pages"), 268435456),
            (("workspace", "index_limits", "max_db_pages"), 268435456),
            (("placement", "ledger_pages"), 65536),
            (("service_limits", "journal_pages"), 65536))
        for keys, maximum in cap_paths:
            for bad_value in (True, 256.0, "256", None, 255, maximum + 1):
                bad = deepcopy(generation)
                set_at(bad, keys, bad_value)
                self.refused("MANAGED_STORAGE_GENERATION_PAGES",
                             lambda bad=bad: SP.generation_envelope(manager, 0, bad))
        metadata = generation["location"]["limits"]["metadata"]
        for key, low, high in (("entries", 32, 65536), ("bytes", 65536, 134217728),
                               ("valueBytes", 1024, 65536), ("providersPerKey", 1, 128),
                               ("pages", 256, 65536)):
            edge = {**metadata, key: high}
            self.assertEqual(SP.node_metadata(edge), edge)
            for bad_value in (True, float(low), str(low), None, low - 1, high + 1):
                bad = {**metadata, key: bad_value}
                self.refused("MANAGED_STORAGE_METADATA:" + key, lambda bad=bad: SP.node_metadata(bad))
            missing = dict(metadata)
            del missing[key]
            self.refused("EXACT_FIELDS", lambda missing=missing: SP.node_metadata(missing))
        self.refused("EXACT_FIELDS", lambda: SP.node_metadata({**metadata, "other": 0}))
        self.assertEqual(configs(), (manager, generation))

    def test_02_fresh_paths_and_exact_lock_refusal(self):
        root = directory("fresh-and-locks")
        lock, database = root / "fresh.lock", root / "fresh.sqlite"
        before = census(root)
        SF.preopen_lock(lock, create=True)
        SF.preopen_database(database, max_pages=64, create=True)
        self.assertEqual(census(root), before)
        for name, raw, valid in (("empty.lock", b"", False), ("large.lock", b"xx", False),
                                 ("one.lock", b"\0", True)):
            path = root / name
            write_new(path, raw)
            if valid:
                SF.preopen_lock(path, create=False)
            else:
                self.preserved_refusal(root, "MANAGED_STORAGE_FILE_BOUND",
                                       lambda path=path: SF.preopen_lock(path, create=False))
            self.preserved_refusal(root, "FRESH_PATH",
                                   lambda path=path: SF.preopen_lock(path, create=True))
        self.preserved_refusal(root, "MANAGED_STORAGE_CREATE_FLAG",
                               lambda: SF.preopen_database(database, max_pages=64, create=1))
        write_new(root / "fresh.sqlite-journal", b"x")
        self.preserved_refusal(root, "MANAGED_STORAGE_FRESH_JOURNAL",
                               lambda: SF.preopen_database(database, max_pages=64, create=True))

    def test_03_metadata_overcap_and_unknown_grammar_preserved(self):
        root = directory("overcap")
        main = root / "over.sqlite"
        write_new(main, b"x" * (64 * 4096 + 1))
        self.preserved_refusal(root, "MANAGED_STORAGE_FILE_BOUND",
                               lambda: SF.preopen_database(main, max_pages=64, create=False))
        for suffix in ("-wal", "-shm"):
            case = directory("sidecar" + suffix)
            path = case / "data.sqlite"
            write_new(path, b"")
            write_new(case / ("data.sqlite" + suffix), b"x")
            self.preserved_refusal(case, "MANAGED_STORAGE_UNSUPPORTED_SIDECAR",
                                   lambda path=path: SF.preopen_database(path, max_pages=64, create=False))
        unused, generation = configs()
        partial = directory("partial-generation")
        write_new(partial / "generation.json", b"{}")
        before = census(partial)
        observed = SF.generation_preopen(partial, generation, 0, guard=guard)
        self.assertEqual(observed["observed_entries"], 1)
        self.assertEqual(observed["possible_entries"], 20)
        self.assertEqual(census(partial), before)
        unknown = directory("unknown-generation-entry")
        write_new(unknown / "generation.json", b"{}")
        write_new(unknown / "not-in-layout", b"preserve")
        self.preserved_refusal(unknown, "MANAGED_STORAGE_UNEXPECTED_ENTRY",
                               lambda: SF.generation_preopen(unknown, generation, 0, guard=guard))
        operation = directory("nonempty-operations")
        write_new(operation / "generation.json", b"{}")
        (operation / "workspace").mkdir()
        (operation / "workspace/operations").mkdir()
        write_new(operation / "workspace/operations/proof.tmp", b"preserve")
        self.preserved_refusal(operation, "MANAGED_STORAGE_UNEXPECTED_ENTRY",
                               lambda: SF.generation_preopen(operation, generation, 0, guard=guard))
        identity = directory("oversize-identity")
        write_new(identity / "generation.json", b"{}")
        (identity / "run-0001").mkdir()
        (identity / "run-0001/location-state").mkdir()
        write_new(identity / "run-0001/location-state/identity.key", b"x" * 1025)
        self.preserved_refusal(identity, "MANAGED_STORAGE_FILE_BOUND",
                               lambda: SF.generation_preopen(identity, generation, 1, guard=guard))

    def test_04_actual_named_sqlite_fresh_then_reopen(self):
        root = directory("sqlite-fresh-reopen")
        path = root / "tiny.sqlite"
        SF.preopen_database(path, max_pages=64, create=True)
        connection = sqlite3.connect(path, timeout=1, isolation_level=None)
        try:
            first = SP.configure_connection(connection, max_pages=64)
            self.assertEqual(first["connection_readbacks"]["auto_vacuum"], 0)
            self.assertLessEqual(connection.execute("PRAGMA page_count").fetchone()[0], 64)
            self.assertEqual(connection.execute("SELECT name FROM sqlite_schema").fetchall(), [])
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("CREATE TABLE tiny(id INTEGER PRIMARY KEY, payload BLOB NOT NULL)")
            connection.execute("INSERT INTO tiny VALUES(1,?)", (b"synthetic-storage-control",))
            connection.execute("COMMIT")
            self.assertEqual(connection.execute("PRAGMA auto_vacuum").fetchone(), (0,))
            OBSERVED["python_sqlite"] = {
                "version": sqlite3.sqlite_version,
                "source_id": connection.execute("SELECT sqlite_source_id()").fetchone()[0]}
        finally:
            connection.close()
        SF.preopen_database(path, max_pages=64, create=False)
        connection = sqlite3.connect(path, timeout=1, isolation_level=None)
        try:
            second = SP.configure_connection(connection, max_pages=64)
            self.assertEqual(second["connection_readbacks"], first["connection_readbacks"])
            self.assertEqual(connection.execute("SELECT * FROM tiny").fetchall(),
                             [(1, b"synthetic-storage-control")])
            self.assertFalse(second["runtime_profile_adopted"])
            self.assertFalse(second["physical_envelope_adopted"])
            self.assertFalse(connection.in_transaction)
        finally:
            connection.close()
        self.assertLessEqual(census(root)["bytes"], 65536)
        OBSERVED["actual_fresh_reopen"] = {
            "scope": "TINY_NAMED_FILE_CONNECTION_NOT_PAGER_BOUND_PROOF",
            "connection_readbacks": first["connection_readbacks"]}

    def test_05_actual_incompatible_auto_vacuum_refuses_preserved(self):
        root = directory("sqlite-incompatible")
        path = root / "auto-vacuum-full.sqlite"
        SF.preopen_database(path, max_pages=64, create=True)
        connection = sqlite3.connect(path, timeout=1, isolation_level=None)
        try:
            # Deliberately incompatible synthetic fixture, never an old product DB.
            for pragma in ("page_size=4096", "auto_vacuum=FULL", "journal_mode=DELETE",
                           "synchronous=FULL", "temp_store=MEMORY", "max_page_count=64"):
                connection.execute("PRAGMA " + pragma).fetchall()
            connection.execute("CREATE TABLE incompatible(id INTEGER PRIMARY KEY)")
            self.assertGreater(connection.execute("PRAGMA page_count").fetchone()[0], 0)
            self.assertEqual(connection.execute("PRAGMA auto_vacuum").fetchone(), (1,))
        finally:
            connection.close()
        before = census(root)
        SF.preopen_database(path, max_pages=64, create=False)
        connection = sqlite3.connect(path, timeout=1, isolation_level=None)
        try:
            self.refused("MANAGED_STORAGE_EXISTING_FORMAT",
                         lambda: SP.configure_connection(connection, max_pages=64))
            self.assertEqual(connection.execute("PRAGMA auto_vacuum").fetchone(), (1,))
        finally:
            connection.close()
        self.assertEqual(census(root), before)
        self.assertLessEqual(before["bytes"], 65536)
        OBSERVED["incompatible_fixture_preserved"] = True

    def test_06_registry_marker_preopen_negative_preserved(self):
        root = directory("registry-marker")
        (root / "slot-0").mkdir()
        (root / "slot-1").mkdir()
        write_new(root / "manager.json", b"AAAA")
        write_new(root / "owner.lock", b"\0")
        # Inert non-SQLite bytes prove this test is metadata only; never connected.
        write_new(root / "generations.sqlite", b"NOT-A-DATABASE")
        self.preserved_refusal(root, "MANAGED_STORAGE_REGISTRY_LINEAGE",
                               lambda: SF.registry_preopen(root, b"BBBB", max_pages=64))
        before = census(root)
        SF.registry_preopen(root, b"AAAA", max_pages=64)
        self.assertEqual(census(root), before)
        write_new(root / "unexpected", b"preserve")
        self.preserved_refusal(root, "MANAGED_STORAGE_REGISTRY_ENTRY",
                               lambda: SF.registry_preopen(root, b"AAAA", max_pages=64))
        tree = ast.parse(RAW[PATHS])
        self.assertFalse(calls(tree, "sqlite3.connect"))
        OBSERVED["registry_marker_scope"] = "ACTUAL_READ_ONLY_HELPER_NO_DATABASE_OPEN"

    def test_07_static_ast_seven_seams_and_allocation_order(self):
        for relative, owner, method_name in OPENERS:
            tree = ast.parse(RAW[PREFIX + relative], filename=relative)
            target = method(tree, owner, method_name)
            pre = calls(target, "SF.preopen_database")
            opened = calls(target, "sqlite3.connect")
            configured = calls(target, "SP.configure_connection")
            self.assertEqual((len(pre), len(opened), len(configured)), (1, 1, 1))
            pre, opened, configured = pre[0], opened[0], configured[0]
            self.assertLess(pre.lineno, opened.lineno)
            self.assertLess(opened.lineno, configured.lineno)
            self.assertEqual(keyword(pre, "max_pages"), keyword(configured, "max_pages"))
            self.assertEqual(ast.dump(pre.args[0], include_attributes=False),
                             ast.dump(opened.args[0], include_attributes=False))
            self.assertEqual(qualified(configured.args[0]), "self.db")
            sql = calls(target, "self.db.execute") + calls(target, "self.db.executescript")
            self.assertTrue(sql)
            self.assertTrue(all(configured.lineno < node.lineno for node in sql))
            OBSERVED["static_openers"].append({
                "file": relative, "preopen": pre.lineno, "connect": opened.lineno,
                "configure": configured.lineno, "first_sql": min(node.lineno for node in sql)})
        tree = ast.parse(RAW[MANAGER])
        target = method(tree, "ManagedGenerations", "open")
        envelope = calls(target, "SP.registry_envelope")
        self.assertEqual(len(envelope), 1)
        mkdir = [node for node in ast.walk(target)
                 if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                 and node.func.attr == "mkdir"]
        self.assertTrue(mkdir)
        self.assertTrue(all(envelope[0].lineno < node.lineno for node in mkdir))
        registry = calls(target, "SF.registry_preopen")
        self.assertEqual(len(registry), 1)
        self.assertLess(registry[0].lineno, calls(target, "sqlite3.connect")[0].lineno)
        allocation = method(tree, "ManagedGenerations", "allocate")
        envelope = calls(allocation, "SP.generation_envelope")
        reserve = [node for node in allocation.body
                   if isinstance(node, ast.FunctionDef) and node.name == "reserve"]
        transaction = calls(allocation, "self._transaction")
        self.assertEqual((len(envelope), len(reserve), len(transaction)), (1, 1, 1))
        self.assertLess(envelope[0].lineno, reserve[0].lineno)
        self.assertLess(reserve[0].lineno, transaction[0].lineno)
        self.assertEqual(qualified(transaction[0].args[0]), "reserve")
        OBSERVED["static_order_scope"] = "PINNED_AST_SOURCE_ORDER_NOT_EXECUTED_LIFECYCLE"


SELECTED = (
    "test_01_strict_arithmetic_exact_fit_all_runs",
    "test_02_fresh_paths_and_exact_lock_refusal",
    "test_03_metadata_overcap_and_unknown_grammar_preserved",
    "test_04_actual_named_sqlite_fresh_then_reopen",
    "test_05_actual_incompatible_auto_vacuum_refuses_preserved",
    "test_06_registry_marker_preopen_negative_preserved",
    "test_07_static_ast_seven_seams_and_allocation_order",
)


def main():
    global FIXTURES, STARTED
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = runner_path(Path(args.output))
    need(os.name == "nt" and output == OUTPUT and output.is_dir(), "CONTROL_SELECTED_OUTPUT")
    sources = output / "sources"
    need(Path(__file__).resolve() == sources / RELATIVE, "CONTROL_SNAPSHOT_EXECUTION_REQUIRED")
    result_path = output / "python-controls-result.json"
    FIXTURES = output / "fixtures"
    need(not os.path.lexists(result_path) and not os.path.lexists(FIXTURES),
         "CONTROL_FRESH_OUTPUT_REQUIRED")
    STARTED = time.monotonic()
    adopt(sources)
    FIXTURES.mkdir()
    suite = unittest.TestSuite(Controls(name) for name in SELECTED)
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    for name, row in PINS.items():
        pin(sources / name, *row)
    inventory = census(FIXTURES)
    success = result.wasSuccessful() and result.testsRun == len(SELECTED) and not result.skipped
    summary = {
        "schema": "DMKN_V5_MANAGED_STORAGE_PYTHON_CONTROLS_V1",
        "status": "PASS" if success else "FAIL", "tests_run": result.testsRun,
        "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
        "selected": list(SELECTED), "sources": {
            name: {"bytes": row[0], "sha256": row[1]} for name, row in PINS.items()},
        "actual_modules": [FEATURE, PROFILE, PATHS],
        "extracted": [{"source": ORDINARY, "definitions": ["ordinary"]}],
        "full_sdk_imported": False, "actual_store_or_manager_opened": False,
        "actual_named_sqlite_fixtures": {
            "fresh_reopen_completed": "actual_fresh_reopen" in OBSERVED,
            "incompatible_refusal_completed": OBSERVED.get("incompatible_fixture_preserved") is True},
        "hot_journal_recovery_exercised": False,
        "observed": OBSERVED, "fixture_inventory": inventory,
        "fixture_preservation": "ALL_RETAINED_NO_DELETION",
        "physical_envelope_adopted": False, "runtime_profile_adopted": False,
        "mathematical_acceptance": False,
        "scope": "FINITE_HELPER_AND_STATIC_WIRING_CONTROLS_NOT_FULL_MANAGED_LIFECYCLE"}
    raw = F.compact(summary)
    need(len(raw) <= 32768, "CONTROL_RESULT_BOUND")
    with result_path.open("xb") as stream:
        need(stream.write(raw) == len(raw), "CONTROL_RESULT_WRITE")
    print(raw.decode("utf-8"))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
