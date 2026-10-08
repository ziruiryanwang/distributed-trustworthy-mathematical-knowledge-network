# Capacity renewal without resetting history

Root proposal, 2026-09-21. Not selected implementation, migration or runtime
evidence. This refines the first obstacle in [CONTINUED-OPERATION](CONTINUED-OPERATION.md).
Keep the recovery and reciprocal qualification cuts unchanged.

## Concrete obstacle and minimal boundary

The current node cannot perform new work after its initial 128 requests,
16 native stages or 4 GiB of conservative reservation are consumed. Even cheap
`info` calls consume requests and reserved bytes. Editing initialized config
changes its identity and is rejected. Starting over discards accessible local
history rather than supplying continued operation.

The minimal extension is an owner-local administrative **increase of cumulative
authorization**, distinct from ordinary agent requests and from service-session
grants. It must remain callable when ordinary request allowance is exhausted.
It is not a peer API, theorem acceptance operation, storage refund or automatic
renewal. The owner still supplies physical capacity and chooses the allowance.

The independent [design review](CAPACITY-RENEWAL-REVIEW.md) accepts the abstract
monotone transition but identifies a remaining implementation decision: bound
and supply administrative metadata headroom. Logical quota exhaustion is not
physical exhaustion; a full database may prevent the grant record or even an
ordinary terminal response from being stored. No unconditional administrative
availability claim is selected. Both request and stage byte charges must remain
included in `reserved_bytes`, which corresponds to current `meta.charged`.

## State and transition

For resource dimensions `requests`, `stages`, `reserved_bytes`, retain used
counters U and store cumulative authorization A. Initially A equals the selected
configuration's initial allowance. Never reinterpret U as remaining allowance.
The admission inequality is coordinatewise `U + charge <= A`.

An owner envelope contains a bounded fresh grant ID, the expected immutable
configuration identity and nonnegative increments d, with at least one positive
coordinate. Keep the exact original envelope bytes. Within the ordinary writer
lock and one transaction:

1. If the grant ID exists, exact byte equality returns its stored response;
   differing bytes refuse. This replay precedes remaining-capacity checks.
2. Require initialization, exact config binding and no pending active operation.
   Refuse uncertainty instead of turning a grant into recovery authority.
3. Require every integer, increment and resulting sum within the explicitly
   supported representation and deployment ceilings, without overflow.
4. Atomically append the grant record, replace A by A+d, and store the exact
   response. U, original requests/stages, heads, snapshots, candidates, proofs
   and publications remain byte-for-byte logically unchanged.

An interrupted caller cannot assume grant rollback. Identical retry must inspect
the stored grant under the same lock. If it committed, it must not add d twice.
A hot-journal state retains the existing explicit recovery limitation until a
separate database-recovery profile exists; do not delete sidecars to retry.

The administrative path needs its own finite input/time/process/output and
metadata-space allowance. It must not call ordinary `reserve`, consume a native
stage, require remaining agent request credits or accept remotely supplied
execution. Ordinary request accounting continues unchanged except that it reads
A from the local store. No signature/consensus/SNARK is needed in this owner-local
trust boundary; a future remote administrator would require a separate contract.

## Safety argument and representation obligations

Assume atomic store transactions, writer exclusion and trusted operator/runtime.
For a fresh grant, U'=U and A'=A+d with d nonnegative, so prior charged work is
preserved and authorization is monotone. For exact replay, U'=U and A'=A. These
transitions write no mathematical authority, hence a grant cannot admit a theorem
or select a new foundation. Later work still satisfies its normal checking path.
These are conditional invariants, not a verification of SQLite or the OS.

Implementation must select a versioned fresh-store schema or an explicit tested
migration; opportunistic table insertion on arbitrary old stores is not selected.
All persisted integers must stay within SQLite signed-64-bit exact integer range.
Smaller product ceilings may be necessary: the current stage directory recognizer
expects exactly four decimal digits, and the database has a 32 MiB page ceiling.
Changing a budget must not silently exceed those independent implementation
limits. A prospective ceiling of at most 10,000 lifetime stages fits IDs 0–9,999,
but is not selected or sufficient evidence of capacity by itself.

## Falsifiable qualification

Use a separately configured fresh node with deliberately small initial allowance,
not exhaustion of a large long-running test. Exercise, in order:

- Real bootstrap and ordinary work reach the chosen request/stage boundary;
  a further operation refuses with retained original charges and no promotion.
- An explicit owner grant remains usable at that boundary. Compare complete
  bounded ledger projections before/after: only authorization and grant records
  may change. No source/config identity is rewritten.
- Identical grant retry changes nothing; conflicting bytes, negative/Boolean/
  oversized integers and overflow refuse. A pending request blocks fresh grant
  mutation without clearing that request or refunding it.
- New ordinary work succeeds within the increased authorization, including one
  actual native-checked operation if stage renewal is claimed. A data-only store
  test cannot establish this part.
- An old exact ordinary request and an old exact grant replay their original
  bytes. Old snapshots/publications and consumed native stages remain intact.

Measure call latency, actual CPU, retained bytes and database pages. Include
failed work. Tests can use fabricated state to exercise pure guard branches only
if clearly separated from real initialization/native-operation evidence.

## What this does not solve

Renewal is not indefinite operation. Conservative reservation still grows even
when physical files are smaller; retained proofs/history and the database still
occupy space. A supported v1 envelope must specify storage supply and safe
exhaustion behavior. Physical expansion or later archival/garbage collection
requires an independent reachability/replay/availability contract; no such policy
is selected here. Likewise this does not fix oversized proof contexts, scalable
retrieval, public transport or measured mathematical usefulness.

The current implementation decision is context selection first, after preserving
the recovery cut. Renewal remains deferred until its supported physical/metadata
envelope and fresh-store version are specified. It must also distinguish replay
of committed grants from any unrecorded refusal, and expose a reviewed fresh-only
initial-allocation interface for realistic small-budget tests. Keep interventions
small and test actual saturation, not counts of grants or configuration resets.
