"""Finite native-free controls for generic admission and parent-clock clamping.

Root must select execution. Synthetic inert units, a fake storage adapter and a
fake clock test new boundaries only. No installation, catalog, native process,
network, filesystem output or mathematical acceptance is performed.
"""
from pathlib import Path
from types import SimpleNamespace, MethodType
from unittest.mock import patch
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ordinary_admission as A
import ordinary_evidence as E
import ordinary_semantics as S
import portable_evidence as PE
import portable_catalog as P
import semantic_identity_checks as Fixtures


def ensure(ok, code):
    if not ok:
        raise AssertionError(code)


def refuses(marker, action):
    try:
        action()
    except ValueError as exc:
        ensure(str(exc) == marker, "WRONG_REFUSAL:" + str(exc))
    else:
        raise AssertionError("MISSING_REFUSAL:" + marker)


def report(label):
    print("ORDINARY_ADMISSION_CHECK " + label + " PASS mathematical_acceptance=false", flush=True)


NAME, SEMANTIC = Fixtures.name, S.semantic_id()
NAT = NAME("Nat")
NAT_ID = S.basis_symbol_id(SEMANTIC, S.foundation_id(), NAT)


def unit(label, dependency=None, *, value=0, semantic=SEMANTIC):
    own = NAME(label)
    typ = [E.EXPR_FORMAT, [], [[2, NAT, []]], 0]
    imports = [[NAT, NAT_ID]]
    if dependency is None:
        body = [E.EXPR_FORMAT, [], [[7, {"$bytes": [] if value == 0 else [value]}]], 0]
    else:
        dep_name, dep_id = dependency
        body = [E.EXPR_FORMAT, [], [[2, dep_name, []]], 0]
        imports.append([dep_name, dep_id])
    raw_unit = [E.UNIT_FORMAT, [0, own, [], typ, body, [2, 1], [own]],
                [[own, 1, [], typ, [body, [2, 1], [own]]]]]
    raw = E.canonical_json({"schema": PE.SCHEMA, "semantic_id": semantic,
        "imports": sorted(imports, key=lambda row: E.name_key(row[0])), "unit": raw_unit})
    parsed = PE.read_evidence(raw)
    return raw, (own, S.export_id(semantic, parsed.unit_id, own))


def context(extra=()):
    return {"local_root": "a" * 64, "semantic_id": SEMANTIC,
            "bindings": {E.name_key(n): identity for n, identity in [(NAT, NAT_ID), *extra]},
            "modules": []}


def plan(ctx, raws, limits=A.PreflightLimits()):
    return A._plan(ctx, raws, limits, lambda: None)


def preflight_controls():
    first, first_export = unit("AdmissionFirst")
    second, second_export = unit("AdmissionSecond", first_export)
    ordered = plan(context(), [second, first, first])
    ensure(ordered.status == "READY" and ordered.ordered_units == (first, second)
           and len(ordered.raw_units) == 2 and not ordered.missing, "DEDUP_OR_DEPENDENCY_ORDER")
    reused = plan(context([first_export]), [second, first])
    ensure(reused.ordered_units == (second,) and reused.reused_unit_ids == (PE.read_evidence(first).unit_id,),
           "ALREADY_KNOWN_UNIT_RECHECKED")
    all_known = plan(context([first_export, second_export]), [second, first])
    ensure(all_known.status == "READY" and not all_known.ordered_units, "EXACT_REUSE_NOT_EMPTY")
    report("exact_dedup_dependency_order_and_reuse")

    missing_a, pair_a = unit("NeedsFirst", (NAME("AbsentFirst"), "1" * 64))
    missing_b, pair_b = unit("NeedsSecond", (NAME("AbsentSecond"), "2" * 64))
    frontier = plan(context(), [missing_a, missing_b])
    ensure(frontier.status == "NEEDS" and frontier.missing == tuple(sorted([
        (E.name_key(NAME("AbsentFirst")), "1" * 64),
        (E.name_key(NAME("AbsentSecond")), "2" * 64)])), "WHOLE_FINITE_FRONTIER")
    differing, _ = unit("NeedsThird", (NAME("AbsentFirst"), "3" * 64))
    refuses("ADMISSION_MISSING_NAME_CONFLICT", lambda: plan(context(), [missing_a, differing]))
    # A forged public READY/status/order cannot skip revalidation in admit.
    owner = A.OrdinaryAdmission.__new__(A.OrdinaryAdmission)
    owner.catalog = SimpleNamespace(context=lambda root: context())
    owner._stage = lambda *args: (_ for _ in ()).throw(AssertionError("FORGED_PLAN_REACHED_CUSTODY"))
    forged = A.Preflight("READY", "a" * 64, (missing_a,), (), (), ())
    refuses("ADMISSION_MISSING_DEPENDENCIES",
            lambda: owner.admit("a" * 64, forged, A.OperationBudget(30, 2, 32)))
    report("whole_missing_frontier_and_forged_ready_refusal")

    alternate, _ = unit("AdmissionFirst", value=1)
    refuses("ADMISSION_SELECTED_NAME_CONFLICT", lambda: plan(context(), [first, alternate]))
    refuses("ADMISSION_PARENT_NAME_CONFLICT", lambda: plan(context([(first_export[0], "f" * 64)]), [first]))
    broken_import, _ = unit("BadImport", (first_export[0], "f" * 64))
    refuses("ADMISSION_SELECTED_IMPORT_CONFLICT", lambda: plan(context(), [first, broken_import]))
    refuses("ADMISSION_PARENT_IMPORT_CONFLICT", lambda: plan(context([first_export]), [broken_import]))
    other_semantics, _ = unit("WrongSemantics", semantic="0" * 64)
    refuses("ADMISSION_UNSUPPORTED_SEMANTICS", lambda: plan(context(), [other_semantics]))
    refuses("ADMISSION_BATCH_CENSUS_BOUND", lambda: plan(context(), [first, second], A.PreflightLimits(max_names=1)))
    refuses("ADMISSION_IMPORT_EDGE_BOUND", lambda: plan(context(), [second], A.PreflightLimits(max_edges=1)))
    report("exact_identity_name_semantics_and_aggregate_limits")


class FakeDB:
    """Only the reservation's read rows plus an observed INSERT; no real SQL."""
    def __init__(self):
        self.insertions = []

    def execute(self, sql, args=()):
        if sql.startswith("INSERT INTO operations"):
            self.insertions.append(args)
            result = None
        elif sql.startswith("SELECT count(*) FROM roots"):
            result = (1,)
        elif sql.startswith("SELECT count(*),COALESCE(sum(reserved_bytes),0) FROM operations"):
            result = (0, 0)
        elif sql.startswith("SELECT COALESCE(sum(reserved_bytes),0) FROM imports"):
            result = (0,)
        elif sql.startswith("SELECT 1 FROM roots WHERE id="):
            result = None
        else:
            raise AssertionError("UNEXPECTED_FAKE_SQL:" + sql)
        return SimpleNamespace(fetchone=lambda: result)


def reservation_controls():
    raw, _ = unit("DeadlineUnit")
    def reserve(clock, context_delay, parent_deadline):
        fake = SimpleNamespace(_active=lambda: None, _grant=None, _db=FakeDB(),
            _limits=P.Limits(), _implementation_raw=E.canonical_json(Fixtures.implementation()),
            _store_id="b" * 64, _root=Path(__file__).resolve().parent / "never-created-admission-control",
            semantic_id=SEMANTIC)
        def delayed_context(parent):
            clock[0] += context_delay
            return context()
        fake.context = delayed_context
        fake._reserve = MethodType(P.PortableCatalog._reserve, fake)
        made = []
        with patch.object(P.time, "monotonic", side_effect=lambda: clock[0]), \
             patch.object(Path, "mkdir", side_effect=lambda *args, **kwargs: made.append(True)):
            try:
                grant = P.PortableCatalog.reserve_extension(fake, "a" * 64, (raw,), seconds=28,
                    output_bytes=1024, parent_deadline=parent_deadline)
                return grant, fake, made
            except ValueError:
                ensure(not fake._db.insertions and not made and fake._grant is None,
                       "EXPIRED_PARENT_MUTATED_RESERVATION")
                raise
    grant, fake, made = reserve([0.0], 5.0, 30.0)
    ensure(grant.deadline == 30.0 and len(fake._db.insertions) == len(made) == 1,
           "SLOW_RESERVATION_RENEWED_PARENT_CLOCK")
    # The optional compatibility path remains relative if no parent is supplied.
    ordinary_grant, _, _ = reserve([0.0], 5.0, None)
    ensure(ordinary_grant.deadline == 33.0, "UNSELECTED_OLD_RELATIVE_API_CHANGED")
    refuses("CATALOG_PARENT_DEADLINE", lambda: reserve([0.0], 5.0, 3.0))
    refuses("CATALOG_PARENT_DEADLINE", lambda: reserve([0.0], 0.0, float("nan")))
    refuses("CATALOG_PARENT_DEADLINE", lambda: reserve([0.0], 0.0, True))
    report("delayed_absolute_deadline_clamp_and_premutation_refusal")


def main():
    preflight_controls()
    reservation_controls()
    print("ORDINARY_ADMISSION_ALL_PASS groups=4 native=false filesystem_writes=false mathematical_acceptance=false",
          flush=True)


if __name__ == "__main__":
    main()
