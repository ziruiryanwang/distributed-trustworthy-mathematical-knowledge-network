# Local agent API — development cut

This document describes the extracted product interface. Build and transport
qualification are recorded in `CHECKPOINT.md`. The bounded same-host reciprocal
peer loop and narrow transfer recovery have passing independent audits. This
is not independent-host deployment or a v1 release.

An agent decides what to investigate. There is no system-wide root goal, task
list, natural-language intent field, reward claim, or mandatory proof strategy.
The node supplies formal information and checks submitted artifacts against its
selected Lean foundation. Usefulness/ranking and mathematical acceptance are
different questions.

## Invocation and identities

The operator initializes a node and assigns a local client label. Submit a UTF-8
JSON request file using the installation's command:

```powershell
& 'D:\Python314\python.exe' -B -E -s -S .\manage.py request --config 'ABS_NODE_STATE\config.json' --request 'ABS_REQUEST.json'
```

Every ordinary request has exactly these fields:

```json
{"client":"local","request_id":"unique-local-id","op":"info","args":{}}
```

Request bytes are capped at 128 KiB. IDs/client labels use 1–64 ASCII letters,
digits, underscores or hyphens. Handles are opaque local strings: do not build
them, borrow another client's handle, or send one to another node. Foundation,
definition and proof identities are typed content identifiers, not local handles.

For an existing request ID, exactly identical bytes replay its terminal result
without redoing work; different bytes conflict. Keep the original request file.
If the process/transport outcome is unknown, do not infer rejection and invent
another request ID. Inspect retained evidence and the recorded pending state.
General crash recovery is not implemented. The explicit ordinary-abort mode
below has a passing bounded native-interruption audit on its preserved cut;
peer recovery remains a separate, narrower mode. Frozen installations retain their
own code and supported operations.

## Formal local operations

| Operation | Arguments | Effect |
| --- | --- | --- |
| `info` | `{}` | Current client context, historical checked descriptions, current P1 candidate snapshot. |
| `select_context` | `{context, selected}` | Compare current head with `context`, then select this client's historical `selected` context; no new acceptance or live dependency check. |
| `find` | `{provider:"P1", snapshot?, cursor?, limit?, max_bytes?}` | Bounded candidate page; not acceptance. Default limit 2, maximum 4; reply allowance 1–16 KiB. |
| `preview` | `{candidate}` | The selected candidate's untrusted formal metadata; no fresh proof check. |
| `admit` | `{context, selected:[candidate,...]}` | Fresh local native check of 1–4 selected candidates and their dependency union with the current context; advances the head only on success. |
| `submit` | `{context, source, root}` | Checks locally authorized Lean source, captures the selected declaration, compiles canonical objects, replays natively, exports inversely and replays again. Returns a private checked artifact; does not publish or replace the current context. |
| `publish` | `{artifact, snapshot}` | Reauthenticates the checked artifact and publishes a candidate into P1 at the current snapshot. Does not grant acceptance to readers. |

For pagination, keep the same snapshot, limit and byte allowance with its
cursor. An old snapshot is a historical cut, not global freshness. If one row
cannot fit the selected reply budget, increase that budget within the supported
limit; an absent result is not proof that no matching mathematics exists.

`select_context` has passed 24 native-free metadata contract tests and an
independent outcome audit. Native01 failed during bootstrap on the test's
aggregate process limit; native02 passed bootstrap but rejected ordinary `def`
at code generation. Native03 now has a passing independent context-selection
and canonical-reuse audit with noncomputable source, on its preserved v2 cut;
see `qualification/context-native-03/OUTCOME.md`. Both earlier failures remain
preserved and charged. Retain
context handles from earlier successful replies. Selection authenticates the
owned historical record, not its present files: success explicitly returns
`mathematicalAcceptance:false` and `live_context_status:"UNCHECKED"`. Later
`admit`/`submit` still revalidate the selected evidence/packages and perform
their normal fresh checks. Missing or corrupt live bytes must refuse then.
Selection does not erase published knowledge, refund resources or create proofs.
A new no-op selection is charged normally. An exact retry returns its old bytes
without moving the head again; that historical response is not current status.
Use `info` to observe the current head. Pending selection is outside peer
recovery; the new ordinary-abort mode covers it prospectively.

For a fresh node, `manage.py configure --context-packages N` selects an initial
package-list ceiling from 5 through 16 (default 16); the five common packages
count toward it. This is an immutable configuration choice, not a way to change
an existing context's limit or enlarge one proof's genuine dependency closure.

`info`/admission descriptions expose exact receiving Lean names and formal
types. Use those names in agent-owned source. `source` is an inline string of
at most 65,536 UTF-8 bytes; `root` selects one declaration using supported dotted
Lean name syntax. Source is executable owner-authorized local input, **not a
sandbox for source supplied by arbitrary peers**. The peer protocol transfers
only inert canonical packages, never source or execution plans.

The 2026-09-23 development frontend elaborates source using the selected Lean
runtime's `Init` module, including its source syntax and macro extensions;
the pinned Lean executable supplies the built-in elaborators and tactics.
Every declaration shared with the checked context must match its complete
canonical type/body, declaration kind and structural inventory, with safe
declarations and the existing binder/universe normalization. Checked peer declarations are installed
under their exact receiving names before source elaboration. This change is
under integration testing; older frozen installations retain their narrower
declaration-only source environment.

The imported frontend is an authoring tool. Any library definition or theorem
used by the submitted proof outside the checked context must be captured with
its complete dependency closure and pass the same bounded canonical checks.
Additional axioms, unsafe declarations and unsupported constructs are refused.
Both fresh native replays still rebuild from the selected mathematical
foundation without importing the frontend. Successful source elaboration alone
does not create an accepted artifact.

Use `noncomputable def` when a mathematical definition needs no executable
code. Syntax support and capture support are separate: a valid Lean program
may still exceed the supported declaration, dependency or resource profile.
The conformance tests establish specific supported forms rather than all Lean
or mathlib programs. A parser failure says nothing about a proposition's truth.

When an ordinary admitted definition's body is needed, use the separate
historical read-only inspection command with an exact request:

```json
{"client":"local","context":"OPAQUE_CONTEXT","reference":[1,"EXACT_PUBLIC_DEFINITION_ID_PROJECTION"],"max_bytes":65536}
```

The strings above are placeholders, not valid identifiers. Copy the complete
public reference projection from the node; do not replace a typed ID with a
bare digest. Invoke `manage.py inspect --config ... --request ...`. This returns
the canonical type/body DAG and referenced exact names, authenticated against
historical native output. It supports ordinary external definitions only and
does not invent reduction metadata, supply a proof strategy, or grant new
mathematical acceptance.

## Peer operations — implementation under qualification

| Operation | Arguments | Meaning |
| --- | --- | --- |
| `peer_find` | `{peer:"configured-alias"}` | Fetch a bounded untrusted catalog and return receiver-owned remote selections. |
| `peer_acquire` | `{remote}` | Receive exact selected bytes, validate the complete canonical package, derive/compare metadata and register a local candidate. No native acceptance or head advance. |
| `expose` | `{selected:[candidate,...]}` | Build an immutable view from explicitly selected locally published entries. Acquired-only entries are ineligible. |
| `replica_expose` | `{acquisition}` | Explicitly build a one-entry view of the exact original bundle retained by this client's successful acquisition. No publication, admission, or new mathematical result. |

After acquisition, call ordinary `admit` with the receiver's own current context.
Neither the sender's checking result nor a transport digest replaces this step.
Exact duplicates can reuse a local candidate while still charging a new
acquisition request's actual allowance. Unsupported alternative packages under
one descriptor are refused, not silently selected as equivalent proofs.

Replica custody has fourteen partly synthetic state-contract passes and a scoped
genuine same-host outcome audit in `qualification/replica-native-02/OUTCOME.md`:
exact-byte serving after the original supplier stops, source-copy independence,
corruption refusal and fresh receiver-local proof reuse. This does not establish
independent-host availability or useful growth. Retain the `acquisition` handle returned by
`peer_acquire`. New-view preparation requires the original received package,
not merely its normalized analysis copy, and must reproduce every advertised
entry field and the exact bundle bytes. Legacy acquisitions without that
custody record refuse; there is no automatic backfill. The operation consumes
one request and the existing 80-MiB exposure reservation, with no native stage.
It does not make an acquired candidate eligible for ordinary `expose`.

A successfully committed replica view is separately retained. Its ledger
authority and frozen bytes can be used for service without reopening the old
incoming or normalized package copies. Neither possession nor service implies
mathematical acceptance: every receiving node still uses ordinary fresh `admit`.
Exact request replay returns the historical response; it does not guarantee
that a view's current files remain available.

An operator can serve a committed view using `manage.py serve`, an explicit
new session ID, local client/view, fixed loopback port and finite request/time
allowance. The session never restarts itself. This first profile uses literal
127.0.0.1 only; it is not public-network deployment. The detailed wire boundary
is in `PEER.md`.

## Interpretation of outcomes

### Owner capacity and status — bounded v3 continuation qualified

The current development cut requires fresh config/database version 3. Old
installed version-2 nodes retain their own code/state; there is no migration
or configuration-edit upgrade. Twelve native-free capacity contracts, four
integration controls and one seventeen-call native continuation have independent
scoped passing audits; see `qualification/capacity-native-01/OUTCOME.md`.
That finite result does not establish indefinite service or qualify later
ordinary-abort changes automatically.

Fresh `configure` accepts `--initial-requests` (1–4096, default 128),
`--initial-stages` (1–256, default 16), `--initial-reserved-mib`
(136–65536, default 4096), and `--initial-metadata-mib` (32/64/128/256,
default 32). The last two values are MiB. Per-operation grants remain unchanged.
State and scratch require the same fixed local NTFS volume and sufficient
sampled space; authorization is not an OS disk reservation.

`manage.py status --config ABS_CONFIG` uses no ordinary request/stage credit.
It reports used, authorized and remaining vectors; metadata pages/caps; pending
request and bounded heads/provider data; and a physical-supply sample. It reads
node state without mutation under the owner lock, but writes supervisory evidence
in scratch. It does not verify historical contexts' present mathematical files.
An active writer can return `BUSY`; absent state returns `NOT_INITIALIZED`.

To add supplied capacity, write an exact owner envelope and invoke
`manage.py renew --config ABS_CONFIG --request ABS_ENVELOPE`:

```json
{"schema":1,"op":"renew","grant_id":"grant-001","config":"CONFIG_SHA256_FROM_STATUS","add":{"requests":1,"stages":1,"reserved_bytes":142606336}}
```

The config text is a placeholder for the exact digest. `reserved_bytes` uses
bytes, not MiB. Additions are nonnegative exact integers; Boolean/decimal values
are invalid. Optional `metadata_cap_mib` raises the selected cap to 32/64/128/256;
a cap-only increase is allowed. The lifetime ceilings are 4096 requests, 256 stages,
64 GiB authorized reserved bytes and 64 successful grants. Other limits do not
increase. Initialized, nonpending state and physical supply are required for a
fresh grant; grants never clear uncertain work, refund usage or accept mathematics.

Keep the exact envelope. A successful repeated grant ID with identical bytes
returns its original response without incrementing capacity again; different
bytes conflict. Replay precedes new-work headroom/pending/supply checks. Response
vectors are historical; use status for the current values. A definite unrecorded
refusal may be retried after conditions change. `RENEWAL_OUTCOME_UNKNOWN` or lost
output requires checking/replaying the SAME envelope, not inventing a new ID.

Logical quota, metadata headroom and physical supply are separate constraints.
Renewal may increase one without fixing another. At the declared ceilings the
node stops accepting new work; this is bounded continuation, not indefinite
retention. See `drafts/OPERATING-ENVELOPE.md` for tier and failure assumptions.

### Owner recovery — qualified within a narrow interruption profile

This is a local operator command, not an ordinary agent or peer request. For an
interrupted `peer_find`, `peer_acquire` or `expose`, retain the exact original
request and its original supervised call directory. Write an owner envelope:

```json
{"op":"recover_peer","client":"owner","args":{"client":"local","request_id":"original-request-id","supervisor_receipt":"ABS_SCRATCH/calls/ORIGINAL_CALL/supervisor.json"}}
```

Invoke `manage.py recover --config ABS_CONFIG --request ABS_ENVELOPE` with the
same Python startup flags. Paths above are placeholders. The command checks
the selected installed source/configuration cut and original execution evidence.
An already-terminal request returns its exact stored bytes. A genuinely pending
request can be terminalized as `INTERRUPTED_PEER_OPERATION` only after its original
worker tree is authenticated quiescent, its reservation-bound attempt matches,
and no native stage belongs to it. A later equal-request retry receipt cannot
replace original-attempt evidence.

Recovery neither accepts mathematics nor refunds charges or deletes partial
files. Successful recovery permits a deliberate new request ID for new work;
it does not automatically retry the interrupted operation. Missing evidence,
nonempty SQLite journals or native-stage uncertainty remain blocked. Never
delete journal/evidence files or reset counters to force recovery. See
[RECOVERY](RECOVERY.md) and the current qualification checkpoint for the exact
supported scope; this is not arbitrary crash or power-loss recovery.
The retained `qualification/recovery-01/OUTCOME.md` audits one genuinely
interrupted acquisition, original-attempt recovery and exact terminal replays.
It does not qualify every operation or failure mode described by the source.
That result belongs to the preserved v2 cut; the v3 pin/schema integration
requires its own regression qualification.

### Owner ordinary abort — bounded native interruption qualified

Use the same `manage.py recover` command with owner operation
`recover_ordinary` and the same exact selection fields shown above. It supports
only `info`, `find`, `preview`, `select_context`, `admit`, `submit`, and `publish`.

The preserved `qualification/ordinary-abort-native-02/OUTCOME.md` independently
audits one genuine live-Lean interruption, original-tree quiescence, abort,
exact replays and fresh checked continuation. The eleven state contracts cover
additional synthetic cases; neither result qualifies arbitrary crash recovery
or automatically qualifies later replica changes.

It does not support bootstrap, renewals, arbitrary new operations, host reboot,
missing original evidence, damaged state or nonempty SQLite sidecars.

After authenticating the source/configuration cut and exact request, a terminal
row returns its original bytes, including an earlier successful response. That
is historical replay, not new checking or a current availability guarantee.
For a still-pending row, abort additionally requires the bound original attempt,
its authenticated whole public worker-tree quiescence, the existing owner lock
and matching active slot. Its fixed refusal is `INTERRUPTED_ORDINARY_OPERATION`.
Old native stages and incomplete output files may remain, but cannot be promoted
to accepted mathematics. Only the terminal response/phase and active slot change;
all charges and files remain. A later submission is a deliberate new request.

Recovery itself creates no ordinary request/stage charge and starts no checker.
Its bounded supervision/evidence costs still exist. If terminal persistence is
uncertain, retain the same selection for inspection/replay; never infer rollback
or retry the mathematics automatically. Persistent terminal-storage failure can
leave the node blocked, and renewal cannot clear that pending request. This is
not a general repair tool. Independent state contracts and a genuine native
interruption/continuation experiment are required before qualifying this mode.

### Mathematical and resource interpretation

`accepted:true` is local, foundation- and context-relative mathematical checking,
not usefulness, human-intention alignment, universal trust or permanent storage.
Candidate flags explicitly mean no receiving acceptance yet. A size/resource/
language-profile refusal is not a theorem being false. A transport failure with
`state_outcome:"UNKNOWN"` may follow a committed operation; preserve its request
and evidence instead of assuming rollback. Failed work remains charged.

The default finite configuration authorizes 128 requests and 16 native stages.
V3 renewal, historical context selection and ordinary abort have scoped native
qualifications on their preserved cuts; general crash recovery remains open.
Do not bypass limits by
editing an initialized configuration, deleting evidence or resetting counters.
