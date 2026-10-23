"""Selected source-only controls; run only after root's finite execution selection.

Catalog artifacts below are deliberately FAKE_BYTES_NOT_LEAN. Calls to the
private commit seam exercise storage transitions ONLY, never mathematical
admission, fixed-basis reconstruction, or native artifact safety.
"""
from pathlib import Path
import copy
import sqlite3
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_evidence as E
import local_catalog as C

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
STORE_ID = "1" * 64
DUMMY = b"FAKE_BYTES_NOT_LEAN_STORAGE_CONTROL"


def ensure(condition, message):
    if not condition:
        raise AssertionError(message)


def rejects(error_type, marker, action):
    try:
        action()
    except error_type as error:
        ensure(marker in str(error), f"wrong rejection: {error}")
    else:
        raise AssertionError(f"expected rejection {marker}")


def name(text):
    return [[0, {"$bytes": list(part.encode("utf-8"))}] for part in text.split(".")]


def profile():
    return {
        "schema": C.PROFILE,
        "kernel_support": "2" * 64,
        "adapter_support": "3" * 64,
        "basis_receiver_support": "4" * 64,
        "basis_seed": C.SEED,
        "basis_inventory": C.INVENTORY,
        "expression_format": E.EXPR_FORMAT,
        "declaration_format": E.UNIT_FORMAT,
        "axiom_policy": "FIXED_BASIS_NO_NEW_AXIOM_UNSAFE_SORRY",
        "snapshot_format": "LEAN_4_34_MODULEDATA_NO_EXTENSIONS_NO_IR",
    }


def fixture_names():
    # Not the real fixed inventory. This probes an internal storage helper's
    # caller-owned name census; no basis warrant is claimed or created for Lean.
    return [name("Nat")] + [name(f"SyntheticBasis.n{i}") for i in range(580)]


def packet(profile_id, own, dependency, symbol):
    type_dag = [E.EXPR_FORMAT, [], [[2, name("Nat"), []]], 0]
    body_dag = ([E.EXPR_FORMAT, [], [[7, {"$bytes": []}]], 0]
                if dependency == "Nat" else
                [E.EXPR_FORMAT, [], [[2, name(dependency), []]], 0])
    own_name = name(own)
    descriptor = [0, own_name, [], type_dag, body_dag, [2, 1], [own_name]]
    inventory = [[own_name, 1, [], type_dag, [body_dag, [2, 1], [own_name]]]]
    imports = [[name("Nat"), symbol]]
    if dependency != "Nat":
        raise AssertionError("use packet_with_prior for two dependencies")
    return E.canonical_json({"schema": E.SCHEMA, "profile_id": profile_id,
                             "imports": imports, "unit": [E.UNIT_FORMAT, descriptor, inventory]})


def packet_with_prior(profile_id, own, nat_symbol, prior, prior_symbol):
    doc = E.read_evidence(packet(profile_id, own, "Nat", nat_symbol)).document
    body = [E.EXPR_FORMAT, [], [[2, name(prior), []]], 0]
    doc["unit"][1][4] = body
    doc["unit"][2][0][4][0] = body
    doc["imports"].append([name(prior), prior_symbol])
    doc["imports"].sort(key=lambda row: E.name_key(row[0]))
    return E.canonical_json(doc)


def raw_for(catalog, own="SyntheticWork.first", *, symbol=None):
    nat_symbol = symbol or E.basis_symbol_id(catalog.profile_id, catalog.basis_id, name("Nat"))
    return packet(catalog.profile_id, own, "Nat", nat_symbol)


def fake_commit(catalog, grant):
    (grant.directory / "chunk.olean").write_bytes(DUMMY)
    return catalog._commit_checked(grant)


def open_store(directory, limits=None):
    options = {} if limits is None else {"limits": limits}
    catalog = C.LocalCatalog.open(directory, profile(), STORE_ID, create=True, **options)
    grant = catalog.reserve_basis(fixture_names(), output_bytes=1024)
    ensure(fake_commit(catalog, grant) == catalog.basis_id, "synthetic basis root")
    return catalog


def reader_controls():
    for raw, marker in [
        (b"1e999999999", "JSON_LEXICAL_TOKEN"),
        (b"-1", "JSON_LEXICAL_TOKEN"),
        (b"0.5", "JSON_LEXICAL_TOKEN"),
        (b"18446744073709551616", "JSON_UINT64"),
        (b"999999999999999999999", "JSON_INTEGER_DIGITS"),
        (b'{"x":0,"x":0}', "JSON_DUPLICATE_KEY"),
        (b'{"z":0,"a":0}', "JSON_NONCANONICAL"),
        (b"[[[0]]]", "JSON_DEPTH_BOUND"),
    ]:
        limits = E.Limits(max_json_depth=2) if marker == "JSON_DEPTH_BOUND" else E.DEFAULT_LIMITS
        rejects(E.EvidenceError, marker, lambda raw=raw, limits=limits: E.strict_json(raw, limits))
    raw = packet("a" * 64, "SyntheticWork.first", "Nat", "b" * 64)
    result = E.read_evidence(raw)
    ensure(result.raw == raw and result.census.external_names == (E.name_key(name("Nat")),),
           "exact evidence references")
    ensure(E.read_evidence(raw).unit_id == result.unit_id, "stable exact evidence identity")
    changed = copy.deepcopy(result.document)
    changed["imports"][0][1] = "c" * 64
    ensure(E.read_evidence(E.canonical_json(changed)).unit_id != result.unit_id,
           "dependency identity not bound")
    changed = copy.deepcopy(result.document)
    changed["imports"] = []
    rejects(E.EvidenceError, "IMPORT_REFERENCE_CENSUS",
            lambda: E.read_evidence(E.canonical_json(changed)))
    changed = copy.deepcopy(result.document)
    changed["imports"] *= 2
    rejects(E.EvidenceError, "IMPORT_ORDER_OR_DUPLICATE",
            lambda: E.read_evidence(E.canonical_json(changed)))
    changed = copy.deepcopy(result.document)
    changed["unit"][2] *= 2
    rejects(E.EvidenceError, "INVENTORY_DUPLICATE_NAME",
            lambda: E.read_evidence(E.canonical_json(changed)))


def lifecycle(directory):
    catalog = open_store(directory)
    try:
        first_raw = raw_for(catalog)
        first = E.read_evidence(first_raw)
        first_symbol = E.export_id(catalog.profile_id, first.unit_id, name("SyntheticWork.first"))
        nat_symbol = E.basis_symbol_id(catalog.profile_id, catalog.basis_id, name("Nat"))
        second_raw = packet_with_prior(catalog.profile_id, "SyntheticWork.second", nat_symbol,
                                       "SyntheticWork.first", first_symbol)
        grant = catalog.reserve_extension(catalog.basis_id, [first_raw, second_raw], output_bytes=1024)
        rejects(C.CatalogError, "CATALOG_UNCOMMITTED_ROOT", lambda: catalog.context(grant.root))
        root = fake_commit(catalog, grant)
        context = catalog.context(root)
        ensure(len(context["bindings"]) == 583 and len(context["modules"]) == 2,
               "exact synthetic context census")
        rejects(C.CatalogError, "CATALOG_LIVE_GRANT_REQUIRED", lambda: catalog._commit_checked(grant))
    finally:
        catalog.close()
    reopened = C.LocalCatalog.open(directory, profile(), STORE_ID)
    try:
        ensure(reopened.context(root)["bindings"] == context["bindings"], "reopen binding drift")
        rejects(C.CatalogError, "CATALOG_OVERWRITE",
                lambda: reopened.reserve_extension(root, [first_raw], output_bytes=1024))
    finally:
        reopened.close()


def binding_refusals(directory):
    catalog = open_store(directory)
    try:
        rejects(C.CatalogError, "CATALOG_DEPENDENCY_BINDING",
                lambda: catalog.reserve_extension(catalog.basis_id,
                                                   [raw_for(catalog, symbol="f" * 64)]))
        wrong = E.read_evidence(raw_for(catalog)).document
        wrong["profile_id"] = "e" * 64
        rejects(C.CatalogError, "CATALOG_EVIDENCE_PROFILE",
                lambda: catalog.reserve_extension(catalog.basis_id, [E.canonical_json(wrong)]))
        rejects(C.CatalogError, "CATALOG_UNCOMMITTED_ROOT", lambda: catalog.context("d" * 64))
    finally:
        catalog.close()
    wrong_profile = profile()
    wrong_profile["adapter_support"] = "d" * 64
    rejects(C.CatalogError, "CATALOG_ADOPTION",
            lambda: C.LocalCatalog.open(directory, wrong_profile, STORE_ID))


def grants_and_interruption(directory):
    catalog = open_store(directory)
    grant = catalog.reserve_extension(catalog.basis_id, [raw_for(catalog)], output_bytes=1024)
    old_deadline = grant.deadline
    grant.deadline += 1
    rejects(C.CatalogError, "CATALOG_LIVE_GRANT_REQUIRED", lambda: catalog._commit_checked(grant))
    grant.deadline = old_deadline
    real_clock = C.time.monotonic
    try:
        C.time.monotonic = lambda: old_deadline + 1
        rejects(C.CatalogError, "CATALOG_GRANT_EXPIRED", lambda: catalog._commit_checked(grant))
    finally:
        C.time.monotonic = real_clock
    (grant.directory / "chunk.olean").write_bytes(DUMMY)
    catalog.close()
    reopened = C.LocalCatalog.open(directory, profile(), STORE_ID)
    try:
        state = reopened._db.execute("SELECT state FROM operations WHERE id=?",
                                     (grant.identifier,)).fetchone()
        ensure(state == ("INTERRUPTED",), "reserved operation was resurrected")
        rejects(C.CatalogError, "CATALOG_LIVE_GRANT_REQUIRED", lambda: reopened._commit_checked(grant))
        rejects(C.CatalogError, "CATALOG_UNCOMMITTED_ROOT", lambda: reopened.context(grant.root))
        ensure((grant.directory / "chunk.olean").read_bytes() == DUMMY, "interrupted bytes lost")
    finally:
        reopened.close()


def corrupt_before_restore(directory):
    catalog = open_store(directory)
    root = catalog.basis_id
    path = Path(catalog.context(root)["modules"][0]["path"])
    catalog.close()
    path.write_bytes(b"X" * len(DUMMY))
    reopened = C.LocalCatalog.open(directory, profile(), STORE_ID)
    try:
        rejects(C.CatalogError, "CATALOG_ARTIFACT_DIGEST", lambda: reopened.context(root))
    finally:
        reopened.close()


def output_census_and_quota(directory):
    limits = C.Limits(max_artifact_bytes=4096, max_total_artifact_bytes=8192)
    catalog = open_store(directory, limits)
    try:
        grant = catalog.reserve_extension(catalog.basis_id, [raw_for(catalog)], output_bytes=4096)
        (grant.directory / "chunk.olean").write_bytes(DUMMY)
        (grant.directory / "unaccounted.log").write_bytes(b"retained")
        rejects(C.CatalogError, "CATALOG_OUTPUT_CENSUS", lambda: catalog._commit_checked(grant))
        catalog.abandon(grant)
        rejects(C.CatalogError, "CATALOG_OPERATION_OR_STORAGE_LIMIT",
                lambda: catalog.reserve_extension(catalog.basis_id,
                                                   [raw_for(catalog, "SyntheticWork.other")],
                                                   output_bytes=4096))
        rejects(C.CatalogError, "CATALOG_UNCOMMITTED_ROOT", lambda: catalog.context(grant.root))
    finally:
        catalog.close()


def withdrawal(directory):
    catalog = open_store(directory)
    try:
        grant = catalog.reserve_extension(catalog.basis_id, [raw_for(catalog)], output_bytes=1024)
        (grant.directory / "chunk.olean").write_bytes(DUMMY)
        (directory / "WITHDRAWN").write_bytes(b"local test withdrawal")
        rejects(C.CatalogError, "CATALOG_WITHDRAWN", lambda: catalog._commit_checked(grant))
        rejects(C.CatalogError, "CATALOG_WITHDRAWN", lambda: catalog.context(catalog.basis_id))
    finally:
        catalog.close()
    rejects(C.CatalogError, "CATALOG_WITHDRAWN",
            lambda: C.LocalCatalog.open(directory, profile(), STORE_ID))


class CommitFault:
    """Inject precisely before/after the real SQLite COMMIT, not fake success."""
    def __init__(self, connection, after):
        self.connection, self.after = connection, after

    def __getattr__(self, name):
        return getattr(self.connection, name)

    def execute(self, statement, *args):
        if statement == "COMMIT":
            if self.after:
                self.connection.execute(statement, *args)
            raise sqlite3.OperationalError("injected commit acknowledgment fault")
        return self.connection.execute(statement, *args)


def uncertain_commit(directory, after):
    catalog = open_store(directory)
    grant = catalog.reserve_extension(catalog.basis_id, [raw_for(catalog)], output_bytes=1024)
    (grant.directory / "chunk.olean").write_bytes(DUMMY)
    catalog._db = CommitFault(catalog._db, after)
    rejects(C.CatalogError, "CATALOG_TRANSACTION_UNCERTAIN_REOPEN_REQUIRED",
            lambda: catalog._commit_checked(grant))
    ensure(catalog._closed, "uncertain owner remained live")
    rejects(C.CatalogError, "CATALOG_CLOSED", lambda: catalog._commit_checked(grant))
    reopened = C.LocalCatalog.open(directory, profile(), STORE_ID)
    try:
        if after:
            ensure(reopened.context(grant.root)["root"] == grant.root, "committed root not recovered")
        else:
            rejects(C.CatalogError, "CATALOG_UNCOMMITTED_ROOT", lambda: reopened.context(grant.root))
        state = reopened._db.execute("SELECT state FROM operations WHERE id=?",
                                     (grant.identifier,)).fetchone()[0]
        ensure(state == ("COMMITTED" if after else "INTERRUPTED"), "uncertain operation state")
        rejects(C.CatalogError, "CATALOG_LIVE_GRANT_REQUIRED", lambda: reopened._commit_checked(grant))
        ensure((grant.directory / "chunk.olean").read_bytes() == DUMMY, "uncertain bytes lost")
    finally:
        reopened.close()


def main():
    ensure(len(sys.argv) == 2, "one selected output directory required")
    selected = Path(sys.argv[1]).resolve()
    ensure(selected.is_relative_to(ROOT / "experiments/v5-local-checks"), "selected local output")
    output = selected / "evidence-catalog-state"
    output.mkdir()
    reader_controls()
    print("EVIDENCE_CATALOG_PASS bounded-reader-identity-census", flush=True)
    cases = [
        ("synthetic-storage-lifecycle", lifecycle),
        ("dependency-profile-refusals", binding_refusals),
        ("fresh-grants-interruption", grants_and_interruption),
        ("artifact-digest-before-restore", corrupt_before_restore),
        ("output-census-retained-quota", output_census_and_quota),
        ("withdrawal-refusal", withdrawal),
        ("commit-fault-before", lambda path: uncertain_commit(path, False)),
        ("commit-fault-after", lambda path: uncertain_commit(path, True)),
    ]
    for label, case in cases:
        case(output / label)
        print("EVIDENCE_CATALOG_PASS " + label, flush=True)
    print("EVIDENCE_CATALOG_COMPLETE groups=9 storageOnly=true nativeAdmission=false", flush=True)


if __name__ == "__main__":
    main()
