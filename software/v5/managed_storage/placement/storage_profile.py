"""Fixed managed data-stream calculations and a supplied-connection guard.

Unwired source helper: no directory/database creation, runtime adoption or
migration. Callers authenticate the supported runtime/VFS, ordinary paths and
same-profile hot-journal lineage BEFORE opening a writable connection.
"""
import sqlite3

from discovery import formal_features as F

PROFILE = "DMKN_V5_MANAGED_APPARENT_STREAMS_P4096_S65536_A1_V1"
PAGE_BYTES = 4096
SECTOR_BYTES = 65536
# A=1 bounds apparent stream lengths, not filesystem allocation or free space.
GENERATION_FILES_BYTES = 131072 + 1
RUN_FILES_BYTES = 2*1024 + 2*16384


def _at(value, *keys):
    for key in keys:
        F.need(type(value) is dict and key in value, "MANAGED_STORAGE_CONFIG_FIELD")
        value = value[key]
    return value


def _observation():
    return {"profile":PROFILE, "scope":"CONDITIONAL_APPARENT_MANAGED_DATA_STREAM_BYTES",
            "calculation_only":True, "physical_envelope_adopted":False,
            "mathematical_acceptance":False}


def database_envelope(pages):
    """Main plus possible rollback journal; fixed constants, no occupancy credit."""
    F.uint(pages,64,268435456,"MANAGED_STORAGE_PAGE_CAP")
    main = pages*PAGE_BYTES
    journal = pages*(PAGE_BYTES+8) + 2*SECTOR_BYTES*(pages+2) + SECTOR_BYTES
    return {"pages":pages,"main_bytes":main,"journal_bytes":journal,
            "total_bytes":main+journal}


def node_metadata(value):
    """New profile requires all five bounded nonnull integers; no JS defaults."""
    F.fields(value,("entries","bytes","valueBytes","providersPerKey","pages"))
    result = {}
    for key,lo,hi in (("entries",32,65536),("bytes",65536,134217728),
                      ("valueBytes",1024,65536),("providersPerKey",1,128),
                      ("pages",256,65536)):
        result[key] = F.uint(value[key],lo,hi,"MANAGED_STORAGE_METADATA:"+key)
    return result


def registry_envelope(manager):
    """Check registry and both charged slots before any manager filesystem write.

    This validates storage-bearing fields only. The caller must validate the
    complete fresh manager schema/profile/bindings; saved output is not authority.
    """
    pages = F.uint(_at(manager,"registry_pages"),64,4096,"MANAGED_STORAGE_REGISTRY_PAGES")
    reservations = {key:F.uint(_at(manager,key),1,2**50,"MANAGED_STORAGE_RESERVATION:"+key)
                    for key in ("owner_reserved_bytes","registry_reserved_bytes","cleanup_reserved_bytes")}
    slots = _at(manager,"slots")
    F.need(type(slots) is list and len(slots) == 2,"MANAGED_STORAGE_TWO_SLOTS")
    selected = []
    for index,slot in enumerate(slots):
        selected.append({"slot":index,
            "reserved_bytes":F.uint(_at(slot,"reserved_bytes"),1,2**50,"MANAGED_STORAGE_SLOT_BYTES"),
            "max_runs":F.uint(_at(slot,"max_runs"),1,4096,"MANAGED_STORAGE_SLOT_RUNS")})
    database = database_envelope(pages)
    registry = database["total_bytes"] + GENERATION_FILES_BYTES
    F.need(registry <= reservations["registry_reserved_bytes"],"MANAGED_STORAGE_REGISTRY_RESERVATION")
    charged = (reservations["registry_reserved_bytes"]+reservations["cleanup_reserved_bytes"]
               +sum(slot["reserved_bytes"] for slot in selected))
    F.need(charged <= reservations["owner_reserved_bytes"],"MANAGED_STORAGE_OWNER_RESERVATION")
    return {**_observation(),"registry_database":database,
            "registry_other_files_bytes":GENERATION_FILES_BYTES,
            "registry_bound_bytes":registry,"slot_reservations":selected,
            **reservations,"owner_charged_bytes":charged,
            "cleanup_progress_guaranteed":False}


def generation_envelope(manager, slot, generation):
    """Check every permitted run before sequence/PROVISIONING reservation.

    Call with the immutable validated configs, not remaining/active run counts.
    This does not validate mathematical, location or cross-role configuration.
    """
    F.uint(slot,0,1,"MANAGED_STORAGE_SLOT")
    owner = registry_envelope(manager)
    selected = owner["slot_reservations"][slot]
    runs = F.uint(_at(generation,"placement","max_runs"),1,4096,"MANAGED_STORAGE_RUNS")
    F.need(runs <= selected["max_runs"],"MANAGED_STORAGE_SLOT_RUN_CAP")
    metadata = node_metadata(_at(generation,"location","limits","metadata"))
    fields = (
        ("workspace/workspace.sqlite",("workspace","ledger_pages"),65536),
        ("workspace/modules/modules.sqlite",("workspace","module_limits","db_pages"),268435456),
        ("workspace/packets/evidence-packets.sqlite",("workspace","packet_limits","db_pages"),268435456),
        ("workspace/index/discovery.sqlite",("workspace","index_limits","max_db_pages"),268435456),
        ("workspace/placement.sqlite",("placement","ledger_pages"),65536),
        ("workspace/placement-routes.sqlite",("service_limits","journal_pages"),65536),
    )
    databases = {}
    for path,keys,maximum in fields:
        pages = F.uint(_at(generation,*keys),256,maximum,"MANAGED_STORAGE_GENERATION_PAGES")
        databases[path] = database_envelope(pages)
    persistent = sum(row["total_bytes"] for row in databases.values())
    node = database_envelope(metadata["pages"])
    per_run = node["total_bytes"] + RUN_FILES_BYTES
    total = persistent + runs*per_run + GENERATION_FILES_BYTES
    F.need(total <= selected["reserved_bytes"],"MANAGED_STORAGE_GENERATION_RESERVATION")
    return {**_observation(),"slot":slot,"reserved_bytes":selected["reserved_bytes"],
            "configured_runs":runs,"persistent_databases":databases,
            "persistent_databases_bytes":persistent,"node_metadata":metadata,
            "node_database_per_run":node,"other_files_per_run_bytes":RUN_FILES_BYTES,
            "all_run_bytes":runs*per_run,"generation_other_files_bytes":GENERATION_FILES_BYTES,
            "generation_bound_bytes":total,"possible_files":14+6*runs,
            "possible_directories":6+3*runs,"possible_entries":20+9*runs,
            "external_outputs_included":False,"shared_installation_included":False}


def configure_connection(connection, *, max_pages):
    """Configure/check one already supplied Python SQLite connection before DDL.

    Caller preconditions: fresh supported enrollment or authenticated same-
    profile reopen, original file bounds, no unknown hot journal/WAL/temp files,
    ordinary paths, supported exact runtime/default VFS, and no other writers.
    This function cannot establish those premises and accepts no adoption bool.
    On any error the caller must close/refuse, never continue schema writes.
    It does not own/close the connection or repair/migrate an existing database.
    """
    F.uint(max_pages,64,268435456,"MANAGED_STORAGE_PAGE_CAP")
    F.need(type(connection) is sqlite3.Connection and connection.isolation_level is None
           and not connection.in_transaction and connection.row_factory is None
           and connection.text_factory is str,"MANAGED_STORAGE_CONNECTION")
    def scalar(sql):
        rows = connection.execute(sql).fetchall()
        F.need(len(rows) == 1 and type(rows[0]) is tuple and len(rows[0]) == 1,
               "MANAGED_STORAGE_PRAGMA_SHAPE")
        return rows[0][0]
    attached = connection.execute("PRAGMA database_list").fetchall()
    F.need(len(attached) == 1 and len(attached[0]) == 3
           and attached[0][0:2] == (0,"main")
           and type(attached[0][2]) is str and bool(attached[0][2]),
           "MANAGED_STORAGE_SINGLE_FILE_DATABASE")
    options = connection.execute("PRAGMA compile_options").fetchall()
    F.need(("TEMP_STORE=1",) in options,"MANAGED_STORAGE_TEMP_BUILD")
    count = F.uint(scalar("PRAGMA page_count"),0,max_pages,"MANAGED_STORAGE_EXISTING_PAGES")
    F.need(scalar("PRAGMA journal_mode") == "delete","MANAGED_STORAGE_EXISTING_JOURNAL")
    if count:
        F.need(scalar("PRAGMA page_size") == PAGE_BYTES
               and scalar("PRAGMA auto_vacuum") == 0,"MANAGED_STORAGE_EXISTING_FORMAT")
    # Empty fresh connections can inherit DEFAULT_AUTOVACUUM; fix before DDL.
    # Existing nonempty format must already match; no VACUUM/migration path.
    for sql in ("PRAGMA page_size=4096","PRAGMA auto_vacuum=NONE",
                "PRAGMA journal_mode=DELETE","PRAGMA synchronous=FULL",
                "PRAGMA temp_store=MEMORY","PRAGMA cache_spill=ON"):
        connection.execute(sql).fetchall()
    F.need(scalar("PRAGMA max_page_count="+str(max_pages)) == max_pages,
           "MANAGED_STORAGE_PAGE_CAP_READBACK")
    readbacks = {}
    for key,expected in (("page_size",PAGE_BYTES),("auto_vacuum",0),
                         ("journal_mode","delete"),("synchronous",2),
                         ("temp_store",2),("max_page_count",max_pages)):
        actual = scalar("PRAGMA "+key)
        F.need(type(actual) is type(expected) and actual == expected,
               "MANAGED_STORAGE_READBACK:"+key)
        readbacks[key] = actual
    F.uint(scalar("PRAGMA cache_spill"),1,2**63-1,"MANAGED_STORAGE_CACHE_SPILL")
    F.need(not connection.in_transaction,"MANAGED_STORAGE_PRE_SCHEMA_TRANSACTION")
    return {"profile":PROFILE,"connection_readbacks":readbacks,
            "lineage_scope":"CALLER_PRECONDITION_NOT_ESTABLISHED_HERE",
            "runtime_profile_adopted":False,"physical_envelope_adopted":False,
            "mathematical_acceptance":False}

