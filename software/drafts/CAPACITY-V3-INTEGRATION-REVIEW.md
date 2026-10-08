# Independent source review of v3 integration

2026-09-21. Source review complete for the cut identified below. The three
integration findings were corrected; no further source-level integration blocker
was found. No Python import, compilation, native execution, database query or
product test was performed by this reviewer. This is not empirical qualification
or release/installation approval. Frozen v2 installations remain separate.

## Recovery pin-budget seam: verified disposition

The implemented split between recovery execution pins and original-public-
receipt authentication is sound within the native-free recovery profile. The
two sets remain explicit and separate.

Adding capacity makes the ordinary public receipt twelve pins: interpreter,
configuration and ten local modules. The recovery worker must independently
authenticate all twelve exact original pins, including checking and all peer
sources, their counters and relevant configuration pin bindings before any
state transition. The original receipt remains pinned as an outer input.

Recovery imports node only for its request/configuration helpers; the reviewed
node source loads checking through `Dispatcher.checking`, not at import time.
The recovery path never invokes that method or constructs a dispatcher. Thus
checking can be omitted from the recovery supervisor's execution-source tuple
without omitting executing code, while capacity remains included because storage
imports it. Do not reuse this reduced tuple for original-receipt authentication.

With nine execution-source modules, the owner-managed recovery envelope contains
fifteen input pins: interpreter, configuration, nine modules, worker, wrapper,
original receipt and owner entrypoint. The separately finalized grant is the
sixteenth pin. Standalone recovery has one fewer pin. Keep the supervisor's
sixteen-pin ceiling and byte ceilings unchanged; retain both owner entrypoint
and grant binding. Future recovery imports require revisiting this closure.

This source argument does not attest the complete Python runtime, protect against
hostile concurrent owner mutation, or qualify v3 recovery behavior.

## Configuration and stage-plan split

Configuration schema 3 and mathematical stage-plan schema 2 need distinct
readers. `run_stage.execute` must use the schema-2 reader. The support builder's
temporary schema-2 policy must use `Domains.from_stage_plan(policy)` or
`Domains.from_record(policy["domains"])`, not the schema-3 configuration reader.
The actual mathematical plan format and its pin/domain checks must remain intact.

## Integrated-cut findings and corrections

The initial integrated root cut was handed off and reviewed. These findings
were reported, corrected by root and re-read:

1. `recovery_worker.authenticate_pins` updates the original pin count to twelve
   but still requires `len(expected) == 11`. This rejects every valid v3
   recovery request at `RECOVERY_PIN_PATH_COLLISION` before authentication can
   complete. Corrected: both counts are twelve, and every expected path remains
   independently rehashed before state is opened.
2. A failed ordinary reservation COMMIT sets store uncertainty and raises
   `TRANSACTION_OUTCOME_UNKNOWN`. `Dispatcher.execute` re-raises that Refusal
   from its reservation block; the outer node handler maps only
   `PENDING_EXECUTION` to BLOCKED, so this uncertain reservation is labeled
   REFUSED. Corrected: the node's outer handler maps this code to BLOCKED with
   `state_outcome: UNKNOWN`, including constructor/initialization ambiguity.
   No uncertain transaction is converted into an ordinary terminal refusal.
3. Recovery interruption terminalization still uses the ordinary transaction
   tier. Its existing exact request, no-stage, attempt, active-key and unchanged
   charge checks must remain. Corrected: it uses the selected cap minus 1,024
   pages with the terminal tier, keeps all those checks inside the transaction,
   and writes only the fixed interruption response/phase and active-slot clear.
   It does not allocate grants, stages, mathematical records or acceptance.

Confirmed integration seams: configure/load use schema 3 and validate initial
capacity; build and mathematical execution use `from_stage_plan` with schema 2;
ordinary indexed prior lookup precedes reservation guards; node and recovery
pass scratch; known pre-COMMIT ordinary SQLITE_FULL with confirmed rollback
maps to METADATA_SPACE; the node uses terminal_refusal for quiescent failures;
administrative owner commands and pre-config error handling are wired; ordinary,
inspection and service execution pin sets include capacity. Capacity and both
administrative modules otherwise match the reviewed drafts apart from their
development-status docstrings. Storage adds the stated SQLITE_FULL mapping.

Additional confirmed boundaries: read-only inspection authenticates schema 3 and
the authorization singleton without invoking the writable store constructor;
status retains its read-only store path and bounded existing-lock behavior;
renewal replays exact successful bytes before fresh-grant/physical checks; and
the owner adapter preserves known CPU/cleanup before failure census. The
administrative profile is still finite and separate from ordinary credits.

The reviewed mathematical stage format remains schema 2; its source, native
checker and foundation are not revised by this integration. No native03 result
can qualify this v3 cut: native03 uses the preserved v2 installation.

## Reviewed SHA-256 identities

Paths are relative to `software/`. These identify development source, not a
deployed release or the separately authored qualification harness.

| Source | SHA-256 |
| --- | --- |
| `manage.py` | `df319f00dbcf29702a04d6151564896ae4d040998ac5859cace7cbe53580bb77` |
| `build.py` | `4e28d64fdfb936f5edd4fdb4531170b273ac6b48a5dfc0455149199849a82018` |
| `py/capacity.py` | `b32b19d8fbaeeb2a90561e7c57f5b16ccdd614b2d993ac5ba7e241eac02889cc` |
| `py/storage.py` | `e33e61df78984c60e60999d53db515487e41157f29475e0cbcaf12321968637d` |
| `py/admin_manage.py` | `984364e1dda0f4c666129187a30a8c6b89335fd49c50942b2199517cde080e2d` |
| `py/admin_worker.py` | `ceb61f18f2bf84de92146119089201b130a96bf9fedbb95f6a7f85bc92e77244` |
| `py/domains.py` | `1ff763737af54286b3c676dbb8cc4b30b8a34f87f48b9f4145b7ad0954a77ea7` |
| `py/run_stage.py` | `2b2a33de45490d124f0828f0e1de15e5c57c91facd326fd4ae054027c7952f4d` |
| `py/node.py` | `dc0b2e20c27290270b595122c33385d51ff629b67ef52b94b97dd8a3990f6977` |
| `py/inspect_context.py` | `7c29d1532453001abd361a1ebf1f449603517e8a8512ae858096967c9f2c225b` |
| `py/recovery_worker.py` | `d5bf6e09d7e3163e8025be59c818c6099ae537e3a3a952576b6fbf2dd7bc8c52` |
| `py/recovery_manage.py` | `99b0cd3438607fd1beffbb5bbf2b07eb1f82d3868c579efd97875437841fb7b6` |

## Qualification remains separate

Source reasoning is conditional on intact typed state, writer exclusion and
SQLite atomicity. It does not measure Windows supply queries, SQLite page/journal
margins, process cleanup, a real administrative CLI/output-loss path, a genuine
native continuation, or the 4,096-request/256-stage horizon. The separately
authored unit harness and any native-renewal launch require their own exact
source/launch and retained-outcome reviews. No indefinite-operation, usefulness,
discovery or usable-v1 completion claim follows from this integration review.
