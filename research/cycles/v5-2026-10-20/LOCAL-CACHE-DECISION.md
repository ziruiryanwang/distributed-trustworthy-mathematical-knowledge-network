# Restart-safe local admission cache: decision

2026-10-20, `core_release`. Source/theory inspection only. Canonical guard
passed. No implementation, imports, tests, native calls, memory investigation,
or Git mutation. This is a decision proposal, not new adoption authority.

## Decision

**A persistent, owner-controlled checked-fact cache is coherent and useful, but
it is not already implemented.** It should be a distinct local trust facility,
not a reinterpretation of workspace custody or saved success reports. It can
remove repeated checking of unchanged mathematics across finite sessions and
restarts. It cannot make an unfamiliar remote theorem trusted, replace a
transferable receipt, or by itself avoid checking ancestors of a new native
contribution.

**Defer implementation now.** Existing durable custody of untrusted proof and
semantic bytes, followed by the newly cheap native recheck where applicable, is
the simpler available route. A persistent authority cache adds a trust/type/update
boundary without yet supplying a missing public use/contribution path. The
native semantic-view investigation also warns that its outputs cannot directly
feed the present `client.author`; completing a second product path just to host
a cache is not a small optimization. Root should prioritize the existing actual
agent workflow, not either new framework for a comparator.

A future **native-only checked-fact store** is the simplest assurance case if
repeated-session checking actually becomes central and its public use seam is
already present. Keep I/A/mixed persistence out of that first scope; their
recursive implementation-support and revocation dependencies add obligations.
A warm ordinary library is already a legitimate comparator whether this
software implements its cache or not.

## What the current project actually does

| Existing boundary | Inspected evidence | Consequence |
|---|---|---|
| Workspace persistence | `software/v5/client/workspace.py`, `Workspace.open`, `reserve`, `read_record`; current `client/supplier_selected/workspace_evidence.py` retains the same model | Persisted packets, groups, bodies, indexes and historical operation records are untrusted. Old grants are interrupted, not resumed. |
| Same-live reuse | `client/workspace.py:admit_receipt`; `client/workspace_mixed.py:_admit_packet`, `admit_aggregate_member`, `close` | Receipt/packet hits reuse actual live issuer handles; close clears caches and closes issuers. Aggregate membership still binds exact J on a receipt hit. |
| Restarted local use | `client/supplier_selected/workspace_evidence.py:admit_local`, `_admit_evidence`; `client/API-EVIDENCE.md`, Lifetime and scope | Retained bytes pass through actual I/A/mixed admission again. No checked-fact row is restored. |
| Explicit cache policy | `software/v5/admission/README.md`; `software/v5/transport/RECEIPT-ACQUISITION-PLAN.md`, Minimal durable store | Saved-success JSON and custody rows cannot become acceptance; cold receivers verify again. This is intentional, not an overlooked current API. |
| Prior future design | `research/cycles/v5-2026-10-12/NEXT-AGGREGATE-COST-DECISION.md`, Persistence and minimum later controls | Explicitly says no durable verified-cache DB exists and requires exact profile/support binding plus current revocation policy for a future one. |
| CACHESEL1 | `notes/checkpoints/CP-001K-local-cache-feedback.md` | Concept-only optional retention selection for already checked proof families; not implemented admission persistence or permission to restore handles. |
| New native owner | `software/v5/native_closure/owner.py`, README | One complete-DAG native invocation yields exact owner-local members; closing revokes them. No persistent cache loader exists. |

The inspected v5 branches therefore deliberately reject the *present* saved-data
shortcut. They do not prove that all future locally controlled persistent
acceptance is unsound. Adding it requires an explicit new authority contract and
fresh source selection. The existing APIs and frozen evidence remain unchanged.

## The useful distinction: remembered local checking versus peer testimony

An existing peer packet, success JSON, Merkle opening, database `verified=1`
field, or copied report is not proof that the local adopted checker accepted J.
The proposed cache would instead be written only by a trusted local transition
that consumes an actually live accepted native member. Its origin is the
owner-controlled trust store, not the self-description of a downloaded file.

Let P be an exact adopted checking/trust profile, and let `Valid_P(J)` denote
derivability of J under its foundation and checker assumptions. The current
native owner supplies the conditional assurance

```text
live_native_member_P(J) => Valid_P(J).
```

A cache can preserve it across restart if these premises hold:

1. A committed row can be created only from that actual live member, with exact
   J, profile and original check binding copied from the owner, not from caller
   JSON. The cache writer rechecks owner validity at the commit boundary.
2. The locally controlled store preserves those committed bytes and their
   origin. Arbitrary custody imports cannot become cache writes or replacements.
3. A fresh reader uses current independently adopted P, not the profile advertised
   by the row. P remains permitted under the current local update policy.
4. A fresh finite cache-reader session validates the row and selected identity,
   then issues a distinct local token. It does not restore the old owner, grant,
   process, deadline, budget, or in-memory token.

Induction on committed insertions proves that every usable row denotes a fact
already checked under P. Restart changes resource authority, not mathematical
truth. The preservation/origin premise is substantial: this is a persistent
trusted local database, unlike the project's intentionally untrusted custody.

No new network identity, signing service, TPM, secret key or platform is needed
under the existing trusted local process/OS/install model. A local checksum is
useful for accidental corruption detection but **does not authenticate origin**
against an attacker who can rewrite the record and checksum. Directory ownership,
the trusted writer and independently configured store location supply that origin
premise. Protecting against hostile same-account software, root compromise or
arbitrary disk rollback would need a stronger trust design; do not claim it here.

## Smallest useful cache object

Begin with a closed, zero-assumption native check. Record exact accepted members,
not a vaguely named module or output status. A conservative identity comprises:

- Local cache namespace and schema, selected independently of remote input.
- Exact native acceptance profile: checker/relation image, foundation, policy,
  journal/interpretation schema, and actual adopted checker/controller/binder
  implementation identity and required support metadata.
- Exact 184-byte J. Equal semantic ModuleID with a different rank-bearing journal
  is not the same entry or a permissible expected-J substitution.
- The checked operation's immutable input digest/length, accepted member-set
  binding and check-origin locator for audit. These values describe a prior
  local check; they are not transferable proof and cannot mint a row themselves.

The present native `_profile_id` also binds paths and allowance values. Exact
equality is a safe conservative initial key, although relocation or budget
changes can cause unnecessary misses. Do not silently strip those fields for
hit rate. A stable mathematical/trust-profile key, separated from per-operation
resource accounting, needs a reviewed definition before using it instead.

Caching the fact `Valid_P(J)` need not keep or reread every ancestral proof
witness. It must retain enough identity/audit metadata to know exactly what was
checked; future invalidation or loss of local trust may require reacquiring
original evidence. Group openings and demanded transparent bodies remain
untrusted content and must still authenticate against J's module commitment at
use. A valid theorem whose required semantic data vanished is unavailable for
that use; the cache must not invent a body or treat a missing definition as
opaque. Packet custody/export remains a separate obligation.

## Atomicity, updates and bounded use

Use the existing single-owner, bounded-SQLite pattern if implementation is
selected. A separate schema/store prevents an old untrusted custody DB from
being silently upgraded into authority. Bootstrap it from fresh trusted local
configuration; never open a user/peer-supplied DB as authoritative because its
schema says `local-cache`.

One transaction commits the acceptance row, exact member bindings and quota
counters only after the successful check and final live/profile validation.
There is no externally visible PREPARED/unchecked row that a reader can promote.
Crash before commit leaves no accepted row; crash after durable commit may leave
a mathematically valid row even if the caller never received acknowledgment.
That uncertainty must not refund the old operation or resume its grant. A cache
failure may safely lose a hit; it must never reconstruct a success from logs.

Do not require a cross-database transaction with untrusted semantic custody:
cached validity and present semantic bytes are independent facets. Cache hit plus
missing data returns missing-data/unavailable, or performs separately charged
retrieval. Quota exhaustion refuses new cache rows. Eviction loses an
optimization, not mathematical validity or separately promised custody.

For an initial native-only implementation, exact profile mismatch means miss or
explicit refusal, followed only by a newly authorized ordinary check. A new
checker/foundation/policy/controller adoption uses a fresh namespace or excludes
all incompatible old rows. No automatic compatibility migration or rewrapping
of old accepted facts under the replacement profile.

Known revocation must affect existing cache-issued handles as well as future
lookups. The simplest trusted single-owner rule is: close/drain current use,
apply the new adopted profile/namespace, then permit fresh sessions. The current
profile must come from current trusted local configuration, not from an older
backup restored with the cache. If rollback or restore continuity is uncertain,
discard cache authority and recheck under the actually adopted current checker.
This is conservative recovery, not cryptographic anti-rollback protection.

I/A/mixed persistence is intentionally deferred. It would additionally need the
complete code-bound support graph already discussed in
`NEXT-AGGREGATE-COST-DECISION.md`: revoking a checker/image can invalidate outputs
of successor profiles that can depend on it. An exact top-level receipt image
alone is not a complete revocation policy.

Every cache session and lookup still has original finite input, metadata/I/O,
controller-time and output budgets. A hit spends its lookup/use resources; it
does not replenish an expired verification allocation. Database/profile checks
must be selected-row/indexed work, not a scan of the whole mathematical corpus.

## Product seam and one important nonconsequence

Use a separate `LocalCheckedNativeMember`-style origin behind a small reviewed
native semantic-view adapter. Do not fabricate `VerifiedNativeMember`, widen
I/A/mixed exact-type gates, or restore historical `LiveWarrant` objects. The
adapter authenticates selected group/body data just as a fresh native view does.
The pure context builder remains untrusted by itself. No cache-entry loader
should be callable through peer offer/custody/publication endpoints.

This provides repeated **local use of an already checked interface**. It does
not yet accelerate acceptance of a new child by omitting its parents from the
current zero-claim native closure. That owner correctly demands the full DAG.
Using cached facts as premises of new checks would require a separately reviewed
conditional-native owner: exact cached premises must discharge every returned
assumption and preserve the graph, rank, semantic-import and revocation rules.
That is a further design, not a side effect of adding a DB. Do not commission it
inside this small cache decision.

Likewise, no cache token travels to another participant. Export original witness
evidence or an actual supported certificate; the recipient establishes its own
authority. A first-time recipient still faces the unresolved large-ancestry
certification problem. Local memoization and succinct transferable verification
solve different cases.

## Concrete payoff and priority

The cheaper alternative already matches the durability requirement: retain exact
packets and committed semantic bytes in the existing bounded stores, load only
the selected items in a fresh finite session, and actually recheck them. That
avoids repeated network acquisition and permits corruption detection without
trusting durable acceptance flags. The existing I/A/mixed `admit_local` path
already does this for its evidence forms; the new standalone native owner can
cheaply recheck a supplied complete small DAG but is not yet a drop-in replacement
for that client path. Do not report it as integrated merely because both pieces
exist. Long enough admitted sessions also already amortize repeated receipt and
packet checks through real same-live handles, without changing persistence.

Let V be the cost of the presently repeated admission, H the complete cache-hit
cost, W the write cost, and M the storage/update/maintenance cost over k later
sessions. Against the same already-acquired semantics and the same local use,
the incremental saving is

```text
k * (V - H) - W - M.
```

This is a decision inequality, not a new growth theorem or measured speedup.
First checking and mathematics creation are common costs; a process kept live
already receives same-live hits, so it must not be charged V repeatedly in the
baseline. Count pin checks, DB reads, semantics authentication and any current
profile validation in H. Both ordinary and certified routes deserve legitimate
warm-cache treatment; it would be unfair to grant this optimization to only one.

The newly adopted three-member native operation used 1.3125 known whole CPU
seconds and 1.5337696 wall seconds. That is an observed component result, not a
per-hit saving or forecast for other graphs. It shows that this small workload
no longer needs an expensive campaign merely to make native rechecking viable.
It does not justify creating a second semantic-use/contribution path to save
roughly one such small check. Larger repeatedly used closures and many finite
agent sessions are the plausible high-payoff case, but they still require an
actual public cache-backed use seam and honest end-to-end accounting.

**Recommended sequence:** continue the existing core agent workflow and reuse
untrusted byte custody plus same-live caches. Reopen persistent acceptance only
when repeated rechecking is a demonstrated or convincingly modelled central cost
and a real supported consumer is already available. A native-only store would
then minimize its assurance scope; it is not commissioned now. Its eventual
changed-boundary controls can be cheap and inert (forged
saved data, wrong exact J/profile, torn commit, stale namespace, corruption,
closed/expired session, missing semantics and retained accounting), followed by
one actual check-close-reopen-use witness. Do not rerun kernel/proof campaigns
or create the cache solely to improve a benchmark. No cache runtime or
implementation is authorized by this note.
