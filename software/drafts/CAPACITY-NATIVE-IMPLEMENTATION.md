# Native-renewal implementation: source-only handoff

2026-09-21. Implements the finite sequence in
[CAPACITY-NATIVE-DISCRIMINATOR](CAPACITY-NATIVE-DISCRIMINATOR.md) as a transparent
adaptation of the frozen native03 coordinator/worker. The author wrote only
`tests/capacity_native_worker.py`, `tests/run_capacity_native.py` and this note.
No previous driver, frozen installation, product module, launch JSON or outcome
was edited. No import, compilation, SQLite query or Python/Lean execution was
performed by the author. Source readiness is not source/launch approval.

Independent pre-execution review corrected one test expectation: the existing
checker emits `SELECTED_CHECK_FAILED:Refusal:STAGE_QUOTA`, not the bare store
code `STAGE_QUOTA`. The worker now checks that exact wrapped code. This is a
prospective harness/specification correction only; product bytes and required
state/charge behavior remain unchanged, and no native allocation was run.

## Selected inputs and exact sequence

`PRODUCT = SOURCE = software`, selecting the integrated version-3 product,
not native03's preserved version-2 installation. Read-only enumeration found
exactly 101 selected files: four root files (`API.md`, `manage.py`, `build.py`,
`assets-lock.json`), direct `py/*.py`, and recursive regular `native/` and
`assets/` files. This is the former 98-file inventory plus `capacity.py`,
`admin_worker.py` and `admin_manage.py`. Both new programs require exactly 101,
ordinal POSIX-relative ordering and exact path/length/SHA-256 identity. There
is no fallback inventory or inclusion of old build outputs/databases.

The worker copies those bytes to a fresh installation and builds support
through its public CLI. It then configures initial authorization `(2,1,144 MiB)`
and 32-MiB metadata, bootstraps, observes one real `STAGE_QUOTA` refusal, checks
readonly exhausted status, probes a pre-reservation `REQUEST_QUOTA`, grants G1,
checks the fixed noncomputable composition source, observes exhaustion again,
replays G1, grants G2, completes ordinary info, replays init/refusal/source/G2,
and observes final readonly status. No publish, admission, network, recovery,
inspection or unlisted status call is added.

Exactly 17 installed CLI calls: two preparation, eight ordinary and seven
administrative. Four ordinary requests are actually reserved; the rejected
new request and the three ordinary replays add zero. Two fresh owner grants
and two exact grant replays are administrative, not ordinary requests.
Receiver stages are bootstrap ID 0 and source-submit ID 1, with respectively
one and five native pipeline commands. Fresh support building separately has
one stage/two compilation commands. Final charged bytes are
`4*8 MiB + 2*128 MiB = 288 MiB = 301989888`; charges are not actual file sizes.

## Receipt roles are deliberately distinct

Ordinary calls use new `scratch/calls` entries. Their twelve ordered pins are
Python, config, then `node`, `run_stage`, `storage`, `capacity`, `checking`,
`domains`, `supervise`, `peer_wire`, `peer_service`, `peer_node`. Bind the exact
installed command, bytes, five recorded files, source pins, request/response
digests and ordinary event `origin_directory`. Preserve the public
450-second/450-CPU-second/6144-MiB/eight-process profile and output bounds.

Administrative calls use new `scratch/administration` entries. Their eleven
ordered pins are Python, config, installed `manage.py`, then `admin_worker`,
`node`, `capacity`, `storage`, `domains`, `run_stage`, `supervise`, `admin_manage`.
Bind the actual administrative command and event: status/renew operation,
checker not loaded, zero stages, no ordinary origin field. Verify the actual
10-second wall/5-second CPU/128-MiB/eight-process profile, 16-KiB request,
64-KiB output/event bounds and 1-MiB administrative diagnostic endpoint.
Status's expected envelope is generated exactly as its real owner CLI does;
the worker does not pass a fabricated status response or event.

Every interpreted successful call needs an actual clean supervisor receipt
with reaped direct child, zero final descendants, closed Job, no termination,
and no cleanup/output/evidence errors. The worker saves each direct-process
observation and available nested CPU/cleanup observation before validating
expected replies. Outer containment, not direct `wait()` alone, is responsible
for the complete tree if an inner wrapper fails or hangs.

## State observations and preservation

The worker imports only the authenticated installed `storage`/`capacity`
modules to obtain the existing `owner_lock(create=False)` implementation.
It does not construct a ControlStore, dispatcher or checker. Public installed
CLIs remain the only state writers. Each SQLite snapshot holds the existing
owner lock and uses `mode=ro`, query-only, memory temporary storage and no mmap,
with schema 3/4096-byte pages/SQLite 3.50.4, a 32-MiB database ceiling,
100,000 VM steps and at most 128 rows per each of ten fixed tables. Snapshots
retain exact BLOB bytes as hex, plus page/freelist observations and source pins.

Exact grant deltas are reconstructed independently: only authorization and one
new exact owner-grant row change. No consumed counter is decreased. The worker
checks the complete expected grant response, including historical used values,
no refund and no mathematical acceptance. Both grant replays return original
bytes, change no table and perform no new-grant supply observation; G1 replay
occurs after source submission has exhausted its added capacity.

The original stage refusal and renewed info have exact ordinary metadata-delta
checks. The unreserved quota probe has unchanged table and state-file maps.
All three ordinary replays preserve all ten tables, use original bytes and
allocate no stages. Three status calls preserve both tables and complete
state-file length/hash maps, and match actual usage/authorization/head/provider
and database-page observations. File maps are taken between quiescent calls,
outside the byte lock so the lock file can itself be read; the premise is an
otherwise idle trusted fixture domain, not adversarial concurrent owner writes.

All original work-file bytes and original mathematical/request/stage records
are checked for preservation at the end. The head remains C0, provider P1 cut
zero, and no entry is published. The renewed source result is a private checked
artifact. Actual native stage receipts/plans, commands, source root/digest and
returned definition profile are bound. Independent canonical/native outcome
audit must still establish the concrete capture/replay/body/dependency binding;
worker assertions and a readable fixture are not a substitute.

Actual product supply checks remain enabled and their NTFS/free-space samples
are checked at configuration, fresh store, admissions and fresh grants. Status
samples are observational and may report insufficient free space; they are not
treated as reservations. No physical-supply mock or synthetic accepted state
exists in this experiment.

## Launch and resource contract

Both roots must be absent: `product-local/capacity-native-01` and
`software/qualification/capacity-native-01`. The former holds installation,
state, scratch, driver and support-build data; the latter holds coordinator,
outer supervision, source snapshots, census and result evidence. Existing or
failed roots are never overwritten, cleaned or automatically retried.

Root must supply and independently review the exact launch. Fields are exactly
`schema`, `pins`, `product`, `limits`, `retained`, with schema integer 1. Eight
ordered pins are Python, new coordinator, new worker, existing
`tests/scenario_profile.py`, current product `run_stage.py`, `supervise.py`,
`domains.py`, and `runtime/lean-4.34.0-windows/bin/lean.exe`. The launch itself
is the ninth outer supervisor pin. Both programs reauthenticate selected pins
and product inventory; coordinator retains its selected source bytes before
importing helpers. The copied installation is the complete product snapshot.

Use the unchanged qualified test-only `scenario_profile.Transport` adapter
for the outer-sixteen shape, without importing/patching any previous driver.
Config schema 3 is not a change to native/support stage-plan schema 2. Keep
product ordinary-eight and native-one profiles unchanged. Fixed outer limits:
450 seconds wall, 450 Job CPU seconds, 6144 MiB private commit, sixteen requested
active processes, 64 KiB each worker stdout/stderr/event. Inner product limits
remain independently checked. The exact outer request is UTF-8
`{"op":"test-capacity-native"}` followed by one LF byte.

Combined retained endpoint ceilings remain 1 GiB, 16384 files and 32768 entries,
including copied source/support/work and final report overhead. The externally
pinned runtime is excluded explicitly. Worker preservation maps have their own
512-MiB/8192-file/16384-entry bound, and persisted individual snapshots/read
inputs have finite byte bounds. These are endpoint checks, not hard transient
disk quotas. No fill loop, repair loop or additional native attempt exists.

Outer Job CPU includes worker, wrappers and nested Jobs once; do not add nested
CPU again. Coordinator process CPU is separately observed up to its stated
endpoint; interpreter startup/final persistence remain explicitly outside that
complete-accounting claim. Preserve actual outer cleanup/CPU before interpreting
the worker result. Census both roots only after genuine worker-tree quiescence,
also on retained failures. Unknown cleanup forbids a live-tree census.

## Outcome boundary

The immediate intended label is `PASS_PENDING_INDEPENDENT_OUTCOME_AUDIT`.
Unexpected refusal, source failure, state mismatch, output ambiguity or cleanup
failure stops the sequence and preserves the failed prefix. Planned byte-exact
replays are the five listed operations, not authority to retry unexpected
failures. No launch exists by virtue of this note. A later independently audited
pass establishes this finite continuation only, not indefinite service, useful
knowledge growth, independent-host collaboration or completion of usable v1.
