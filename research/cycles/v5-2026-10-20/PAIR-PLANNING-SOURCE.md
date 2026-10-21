# Pair planning: selected three-file source implementation

2026-10-20, core_release. Root adopted POST-CUSTODY-DISCOVERY-DECISION
`8f22aa5b4742108b99b96c0d87b8d30a036b96f9e24962faa559ba08af87f098` and selected
these fresh successors. No code import, compilation, test, build, network,
native/proof execution or Git action was performed. Used predecessors remain
unchanged. Independent review and root's separate execution selection follow.

## Sources

All successor paths below are under `software/v5/pair_planning/`.

| File | SHA-256 |
|---|---|
| `discovery/module_export_adapter.py` | `c7fde37659753a9238506d399e0be5c44ebb5e3a012b5a681dfa1a1551884fd1` |
| `client/direct_contacts.py` | `1f4224808ceb65feff3fd80353a3dbea3923e2ad091e7c435193fd82f4dc54c8` |
| `client/located_queries.py` | `4ffb84789deefb524f7f290b2a8879e3b9a1eadc0febf53ad2f5e1a3e168c66a` |

Exact current-114 predecessors and hashes are listed in the adopted decision.
The adapter adds only `plan_query`. Direct/located successors change only the
adaptive next-query boundary: optional Boolean, plan selection, copied local
diagnostics. Legacy `bind`, `compile_query`, all extraction and validators,
envelope classes and allocations remain unchanged.

## Exact ABI

`ModuleExportAdapter.plan_query(specs)` returns a fresh dictionary:

- `schema`: `DMKN_MODULE_EXPORT_PAIR_QUERY_PLAN_V1`;
- `namespace`: the unchanged selected profile namespace;
- `status`: `WIRE_CAP` if any eligible key was omitted, otherwise
  `ALL_ELIGIBLE` if an extra pair was added, otherwise `NO_EXTRA_PAIR`;
- `legacy_features`: unchanged `compile_query(specs)` result;
- `features`: sorted legacy keys plus selected extra keys, at most eight;
- `eligible_pair_features`, `added_pair_features`, `omitted_pair_features`:
  sorted key arrays; eligibility is checked against the original atomic keys,
  not the already compressed legacy set;
- `global_complete` and `mathematical_acceptance`: both false.

The first pass uses the old compiler, retaining all profile/fingerprint checks.
Eligible additions are chosen in canonical profile order; sorted output does
not change that cap-selection order. The planner cannot accept raw feature keys
or another profile. Its output contains no stored statistics or mutable profile
objects. Every returned array is newly constructed.

The existing adaptive helper signatures gain keyword-only `plan_pairs=False`:

    next_query(..., contact_lifetime_ms=60000, plan_pairs=False)
    next_located_query(..., descriptor_bytes=4096,
                       descriptor_age_ms=60000, plan_pairs=False)

Any non-Boolean refuses with `PAIR_QUERY_PLAN_OPTION`; integers are not accepted
as Booleans. Defaults retain the legacy feature computation and report shape.
Opt-in uses the planner exactly once before the allocated session is created;
one planned feature list flows into the existing session, generation identity,
route-subset validation and acquisition binding. There is no mutation of an
active session.

For opted-in callers, `query_plan` is deep-copied into the allocated generation
row and separately into the ordinary returned result. It is also present in
`NO_CONTACTS_IN_SELECTED_ROUTE_PLAN`. Existing envelope reports deep-copy their
generation rows. Caller mutation of a returned plan therefore cannot change
the recorded plan or live query. Existing controllers still charge original
specs/routes; original search reservation and all network charges remain.

## Assurance and review focus

Both independent decision challenges supported `L subset F`, the exact-query
argument under correct extraction, the eight-feature bound, and unchanged
legacy routes. The implementation has not yet passed independent source review.
The discriminating controls should use realizable nonexclusive export features;
fabricated metadata counts alone are not a source-to-index test.

More summary keys can require more bytes/authentication work and can refuse
under unchanged caps despite the legacy query succeeding. This is intentional
bounded behavior, not an implicit fallback or total-cost/availability theorem.
The planner does not provide global recall, correct-index-build assurance,
mathematical acceptance, useful-growth evidence or final-v5 completion.

Root owns the control selection; core_growth owns fresh focused controls. No
old passing campaign or proof-production operation is restarted by this source
checkpoint. The README documents opt-in use and the explicit limitation.
