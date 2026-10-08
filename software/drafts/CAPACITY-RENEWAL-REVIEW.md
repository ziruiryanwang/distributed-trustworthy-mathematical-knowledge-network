# Capacity renewal: bounded design review

2026-09-21. Read-only audit of `CAPACITY-RENEWAL.md` against current `storage.py`,
`node.py`, `manage.py` and selected checking/domain constraints. No execution,
migration or product changes. Verdict: the monotone-authorization transition is
sound under its stated trust/transaction assumptions, but its operable envelope
and administrative path are not yet specified sufficiently for implementation.

## Central findings and required decisions

### Administrative reachability is conditional, not physical inexhaustibility

`reserve` currently gates both request count and `meta.charged`; `stage` gates
stage count and that same charged counter. Grants must bypass both ordinary
paths, including wrapper-level checks, while retaining writer exclusion and
initialization/config binding. Existing `manage` has no grant command and the
ordinary dispatcher only permits owner `init`; a separate bounded owner command
is genuinely required, not merely a new ordinary operation name.

The shared control database has 8,192 pages of 4,096 bytes and no administrative
reserve. If ordinary rows consume the available pages, a fresh grant record may
not fit. Worse, an already-reserved ordinary operation may fail to persist its
terminal response and remain pending, which correctly blocks a fresh grant.
Therefore select a concrete metadata-headroom/exhaustion policy before claiming
renewal is reachable at logical quota exhaustion. At minimum scope that claim to
the supported envelope with sufficient DB/filesystem headroom; authorization is
not proof of space. Existing exact replay still needs readable storage, locking
and evidence-output capacity. There is no unconditional availability theorem.

### Preserve both reservation sites and exact replay semantics

The proposed transaction and replay-before-capacity-check order are correct.
Require a unique owner grant-ID index and store the complete bounded envelope
and exact response bytes atomically with A. Do not derive a replay response from
current A or rerun fresh-grant checks: an old successful grant must replay even
if later work exhausted allowance or left another operation pending. Only fresh
grant mutation needs `active = NULL`; ownership/config checks still apply.

Map `reserved_bytes` explicitly to existing `meta.charged`: it includes ordinary
request grants AND native-stage grants, not actual disk usage. Replace lifetime
authorization comparisons at both `reserve` and `stage`; preserve per-operation
8/64/80 MiB request and configured stage grants. A reservation refusal before
insertion leaves no new ledger request; a later stage-quota refusal preserves the
already-consumed request charge. Never relabel either result as refunded work.
Specify whether refused new grant IDs are remembered; otherwise exact replay is
defined only for committed grants, not every administrative refusal. The latter
minimal choice is acceptable if its response/retry contract says so explicitly.

### Integer and path ceilings must constrain authorization, not just increments

Use exact integers (`type(x) is int`, excluding Boolean values), validate stored
U/A as well as d, and check all proposed sums before SQL writes. SQLite arithmetic
can promote overflowing integer expressions to REAL; the intended signed-64-bit
invariant must not rely on SQL addition alone. Bound each coordinate and the
total grant-record count; a finite input size is not a finite lifetime ledger.

The proposed stage authorization ceiling 10,000 is arithmetically consistent:
`stage` uses the preincrement count as its ID, so the last permitted allocation
is `stage-9999`, after which U_stages is 10,000. Authorization above that must
refuse before creating a stage row/directory, unless every exact-four-digit
consumer is separately revised. This ceiling is a representability ceiling,
not evidence that 10,000 stages fit the selected DB/filesystem or cost envelope.

### Fresh schema first; no implicit migration or authorization reset

Current stores have no authorization/grant tables or explicit schema-version
check. Choose a new versioned fresh-store format before implementation, initialize
A exactly once from immutable configuration, and reject unsupported old stores.
Do not regenerate A from configuration on each open or infer it from grant
history using an unbounded scan. Existing installations/receipts remain frozen.
In-place migration would additionally need tested preservation of request bytes,
context identities, pin-bound old evidence and configuration identity; it is not
made safe simply by adding columns in a transaction. No migration is needed to
qualify a fresh bounded renewal cut.

### The proposed boundary experiment needs a real initial-allocation interface

`configure` hardcodes 128 requests, 16 stages and 4 GiB; no current public option
selects smaller initial allowances. Propose/validate normal fresh-only options
or an equivalent reviewed operator configuration path before using tiny grants.
Bootstrap itself costs one ordinary request plus one native stage and both byte
reservations. Test each exhausted dimension and their combined reachability;
renewing stages alone cannot make source work possible when request or byte
authorization is also exhausted. Include actual post-grant native work, exact
replays and a commit/output-loss discriminator, without fabricating successful
native evidence. Resource/DB measurements and failure records remain necessary.

## Order and limits

Keep grants deferred until a concrete supported envelope is selected. The draft's
last paragraph suggests pairing renewal with context selection; current root
direction instead selects the smaller context-pointer/initial-package-cap change
first. Neither action renews physical space, entry capacity, proof-context limits,
transport availability or mathematical usefulness. No further subsystem is
recommended by this review.
