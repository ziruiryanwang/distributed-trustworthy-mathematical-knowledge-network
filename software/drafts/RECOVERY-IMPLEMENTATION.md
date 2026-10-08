# Draft native-free pending recovery

Status: authored for source review only. Not integrated into `manage.py`, not
executed, and not qualification evidence. This draft is outside the current
installed source cut and must not consume the current experiment's allocation.
It implements the narrow contract in [RECOVERY.md](../RECOVERY.md), not native
stage recovery, migration, quota renewal, database repair, or power-loss repair.

## Selected command and ownership

The future supervised worker accepts exactly `--config`, `--state`, `--request`
and `--event`, using the installed interpreter with `-B -E -s -S`. Its request is:

```json
{
  "op": "recover_peer",
  "client": "owner",
  "args": {
    "client": "local",
    "request_id": "interrupted-acquisition-01",
    "supervisor_receipt": "E:\\operator-scratch\\calls\\call-selected\\supervisor.json"
  }
}
```

This is a separate owner-local control envelope, not a node/peer request. It
does not reserve another request, consume a stage, or allocate peer work. The
literal `owner` field is scope separation, not authentication against an attacker
who can already modify owner files or launch owner processes. The assumed owner
filesystem and local execution authority must remain trusted.

The original selected operation must be `peer_find`, `peer_acquire`, or `expose`.
The selected client must already occur in the configuration. Recovery never
loads the checker, peer implementation, runner, supervisor, or native runtime.
Their source bytes are hashed as evidence; hashing is not execution.

## Identity of the execution being recovered

Equal request bytes do **not** identify an execution attempt. A later retry can
have identical bytes and a clean supervisor receipt while the original request
remains pending. Using that retry receipt as cleanup evidence would be unsound.

The ordinary reservation transaction therefore needs the root-authored additive
record in the existing records table:

```text
data = {request: request_key, call_directory: original_absolute_call_directory}
raw = encode({config: config_id, kind: "attempt", client: "owner", data: data})
handle = "attempt:" ++ SHA256(raw)
```

The request key is the existing SHA-256 of the encoded client/request-ID pair.
The marker is inserted in the **same transaction** that reserves charges and
creates the pending request. A dispatcher retry returns or blocks at the prior
request lookup before reservation; it cannot mint an additional origin marker.
The pending recovery transition requires the exact marker for the selected
receipt's parent directory, including exact record bytes and kind/client columns.
There is no operator-attestation bypass and no fabricated-marker fallback.

Requests launched without an original supervised event/origin marker cannot use
this transition. An event directory supplied by an owner is not itself evidence
of supervision: the original command, receipt, pins and cleanup must also bind.

## Evidence authentication and limits

The original receipt must be a direct child `supervisor.json` of exactly one
call directory immediately below the configured `scratch/calls`. The directory
name and receipt name must agree. This intentionally supports the ordinary
`manage request` layout, not arbitrary nested qualification evidence locations.
Paths resolve before comparison; the config/state/install must match the current
selected domains. The recovery event must be new, under scratch, and outside the
original call directory. Recovery never overwrites the original evidence.

| Input | Bound and binding |
| --- | --- |
| Owner recovery envelope | 16,384 bytes; exact fields and configured client |
| Original supervisor receipt | 65,536 bytes; schema 1; known final transport status |
| Original adjacent request | 131,072 bytes; receipt file pin, request digest, exact ledger bytes |
| Original adjacent command | 65,536 bytes; receipt file pin and exact normal node command |
| Source/config/interpreter pins | Exactly 11 current ordinary node-call pins; at most 16 MiB each and 64 MiB total |
| Terminal reply | At most 1 MiB; replayed bytes are never parsed or reformatted |
| Recovery event | At most 65,536 bytes; fresh file, flush and fsync before stdout |
| Database work | Existing 100,000-step SQL ceiling; indexed request/record reads; stage table capped at 64 |

Receipt parsing accepts finite timing floats but rejects duplicate keys,
nonfinite constants, overflow-to-infinity and malformed JSON. Exact command
comparison uses the canonical encoding, which distinguishes booleans from
integers and integers from floats. It binds interpreter, startup flags, node,
config, state, request, event, working directory, non-shell launch, creation
flags and the declared bytecode environment override.

The 11 expected source pins are the current interpreter and selected config,
plus `node.py`, `run_stage.py`, `storage.py`, `checking.py`, `domains.py`,
`supervise.py`, `peer_wire.py`, `peer_service.py` and `peer_node.py`. All must
match current bytes. Configured checking/domains/peer pins must also agree.
An upgraded source cut blocks this first recovery profile; upgrade/migration
support requires a separate design. Pin equality does not independently verify
the correctness of the installed sources or Python standard library.

The original receipt's own size/hash is included in the new event. The receipt
is trusted owner-local retained evidence, not a signature, remotely verifiable
certificate, or protection against an owner rewriting their own evidence.

Original stdout/stderr/event are not used as recovery premises. They may be
absent, empty, partial or unparsable following interruption. The indispensable
inputs are the adjacent authenticated request and command. A receipt reporting
output-record or evidence-persistence errors nevertheless blocks a pending
transition, because the selected cleanup record is then incomplete/uncertain.

## Transition and replay

Let `k` be the selected request key, `r` the authenticated original request bytes,
`d` the original call directory, and `R[k]` the existing request row.

For both replay and transition, require exact `(client, request_id, key, raw)`
binding, initialized matching configuration and no native stage assigned to `k`.
The normal OS writer lock covers ledger selection, transition and close.

If `R[k].phase = terminal`, return `R[k].response` exactly. No cleanup or attempt
marker premise is required because replay changes no request state. In
particular, the stored response can be successful, and an unrelated active
request does not prevent replay when the writer lock can be acquired. Exact
authenticated request/command/current-pin binding remains mandatory.

For a pending transition, additionally require:

- `R[k].phase = pending`, `R[k].response = NULL`, and `meta.active = k`.
- The exact original-attempt marker for `(k, d)` exists.
- The receipt records a Job created before launch, completed attach/resume, a
  reaped direct child, initial active count zero, final active count zero, a
  nonempty assigned process history and a closed Job. Required booleans use
  exact boolean checks; counts and process IDs use exact integer checks.
- Cleanup errors are absent/empty, and output-record/evidence-persistence errors
  are absent. A deliberately terminated process is allowed: terminated-process
  count zero is **not** a premise for recovery.

Re-read all ledger transition guards in one immediate transaction. Change only
the selected pending row to the encoded response
`{"code":"INTERRUPTED_PEER_OPERATION","status":"REFUSED"}` and clear its active
slot. Assert that every other meta field is unchanged and the terminal row
contains exactly those bytes before commit. Never create candidate/context/head
records, reconstruct results from files, change counters, refund charges, or
delete anything. All retained/orphan files and original evidence remain intact.

This proves only a conditional recovery safety argument: under trusted source
and evidence integrity, origin binding plus completed process-tree cleanup and
writer exclusion prevent the old worker from later promoting its retained
artifacts. Native-stage absence restricts the transition to the supported case.
It is not a theorem that arbitrary Windows crashes or hostile owners are safe.

## Uncertainty and availability

Missing premises produce bounded `BLOCKED` diagnostics, not invented mathematical
refusals or automatic database resets. A failure after attempting the terminal
write reports `RECOVERY_PERSISTENCE_UNCERTAIN` and `UNKNOWN_REPLAY_REQUIRED` unless
commit completion was observed. Even if rollback probably succeeded, an outer
exception is not asserted to prove rollback.

Event-output failure suppresses stdout and exits nonzero. It never rolls back a
completed terminal transaction. A future supervised recovery invocation must
re-read the ledger; it may find the original response already terminal and replay
it exactly. Recovery's own event explicitly denies mathematical acceptance
authority and records whether it replayed or committed an interruption refusal.

The lock is necessary writer exclusion, not substitute process-tree evidence.
Lack of a PID or lock by itself does not permit recovery. No current request,
stage or storage allocation is renewed by recovery; sustained operation still
requires the separate capacity policy.

## Required independent review and fresh qualification

No execution result is claimed for this draft. Root alone may integrate and run
a separately approved fresh test allocation after source review. Qualification
must preserve the test's actual supervisor evidence, request bytes, source pins,
selected state observations, counters and retained-file census.

1. Interrupt an actual supervised slow loopback `peer_acquire` before its
   terminal visibility transaction. Require a genuine pending ledger row, the
   reservation-bound origin marker, quiescent original process tree, no new
   candidate/provider entry and unchanged client head.
2. Recover it using its real original receipt. Require the exact interruption
   refusal, cleared selected active slot, unchanged counters and retained files,
   no stage allocations and no mathematical promotions.
3. Replay the original request and recover again; both must return the exact
   stored terminal bytes without new charges. Use a fresh request ID for an
   ordinary acquisition and require success afterward.
4. Produce a real supervised retry while the original is pending. Its receipt
   has the same request bytes but a different call directory. Recovery selected
   with that receipt must block on the absent original-attempt marker.
5. Replay an already-successful terminal peer request. Require its successful
   response byte-for-byte, not an interruption refusal. Exercise a terminal
   replay with an unrelated pending request and verify that active slot remains.
6. Negative controls: wrong client/ID/raw/config/state/source cut; altered command
   or request pin; unsupported native operation; selected native stage row;
   absent/wrong origin marker; wrong active request; nonquiescent Job; incomplete
   cleanup; cleanup/persistence/output-record error; duplicate-key/nonfinite JSON;
   boolean count masquerading as zero; preexisting/out-of-domain event path.
7. Inject bounded commit/output failure and kill recovery after commit before
   stdout. Require conservative uncertainty and correct subsequent exact replay,
   never a second charge, candidate, stage or terminal rewrite.

Fabricated pending rows and fabricated receipts may exercise negative guards;
they do not qualify genuine interruption, quiescence, commit recovery, or restart
operability. Positive results do not extend to native-stage recovery or power
loss without a separate argument and evidence.
