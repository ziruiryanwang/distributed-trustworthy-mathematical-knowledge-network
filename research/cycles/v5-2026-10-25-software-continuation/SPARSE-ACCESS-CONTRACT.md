# Sparse access: implementation contract

2026-10-25, source/theory only. Root selects implementation separately. Motivation,
cost argument and investigator workflow are in [NEXT-PAYOFF-REVIEW](NEXT-PAYOFF-REVIEW.md)
and [SEARCH-LOCALITY-DECISION](SEARCH-LOCALITY-DECISION.md). No test/code/state/Git
change or global-scale/growth claim follows from this contract.

## Decision and source

Adopt **fresh opt-in static pair indexes maintained in the same Store admission
transaction**, not namespace-changing pair features or a catch-up subsystem.
Keep canonical records, feature IDs, namespace, atomic commitments and snapshots
unchanged. V1 readers/stores remain the default. Sparse traversal requires an
explicit V2 protocol because V1 requires `next-start <= charged.scanned`.

Source basis is `experiments/v5-local-checks/contact-federation-assembly01/assembled/package`,
PROFILE `3d127796190ca3d049bd956288025c10c4ac7e383a15685aca6ea8d2fbc61479`.
Existing Store, candidate_query, SearchSession, FairSearch, HTTP provider and
peer_api were inspected. Their used bytes stay frozen; changes belong in a fresh
root-selected successor.

## Exact local configuration and helper interface

Add `Store(..., access_pairs=None)`. None retains the old physical config/schema
and behavior. Enabled configuration has exactly:

```text
access_pairs = {
  "pairs": [[atom_a, atom_b], ...],
  "limits": {"max_rows": R, "max_logical_bytes": B}
}
```

Require 1..8 pairs, each two distinct 64-hex atomic IDs in ascending order;
the pair list is lexicographically sorted with no duplicates. R is an integer
1..16000000; B is an integer 1024..2^40. Booleans are not integers. Atoms may be
absent from the current corpus. Configuration is owner-selected, immutable and
bound with the namespace in persisted Store config; enabled local schema is
`DMKN_DISCOVERY_STORE_V3`. Exact matching config is required on reopen.
Old stores are not migrated, repaired or rebuilt implicitly.

New `discovery/pair_access.py` has these narrow seams:

| Helper | Contract |
|---|---|
| `validate_config(value)` | Validate and return a detached canonical config. |
| `create(store, config)` | Create auxiliary tables/seq-zero metadata inside the fresh Store creation transaction. |
| `open_config(store, config)` | Check persisted config, bounded counters and readiness against base sequence; no full-table audit. |
| `append(store, record, ordinals, admitted_seq)` | In caller's admission transaction, charge/insert matching pairs and update completion sequence; never commit independently. |
| `plan(store, features, anchor, io)` | Meter readiness/config lookup; return lexicographically first eligible companion or None; corruption raises. |
| `next_row(store, anchor, companion, partition, start, stop, io)` | Meter one indexed seek; return `(anchor_ordinal, companion_ordinal, object_id, admitted_seq)` or None. |

Store retains detached `self.access_pairs`; default None needs no auxiliary SQL.
Tables live in the same SQLite database, not an independently movable sidecar:

```text
access_rows(anchor, companion, partition, anchor_ordinal,
            companion_ordinal, object_id, admitted_seq,
            PRIMARY KEY(anchor, companion, partition, anchor_ordinal))
access_meta(id=1, completed_seq, oriented_rows, logical_bytes)
```

Use object foreign-key binding and bounded nonnegative integer checks. Each
matching pair inserts **two** orientation rows; no arbitrary ORDER BY or extra
sort is needed for either atomic anchor. Quotas count both rows.

## Atomic maintenance and costs

The committed invariant is: each configured pair's rows are exactly its admitted
atomic intersection with original ordinals, both orientations agree, and
`access_meta.completed_seq == Store.meta.seq`. Initialize at zero. During new
admission, retain the existing per-feature ordinals in a bounded dictionary;
check at most eight pairs; insert both rows for each match; advance completion
sequence in the **same** object/postings/CAS/snapshot transaction. Duplicate
admission is a no-op. Rollback restores every base/access table and counter.

Charge each oriented row's canonical serialized tuple bytes once to global
Store logical usage and once against the independent access logical allowance
(two constraints, not double global usage). Bound/config-charge configuration
bytes too. Maintain row/byte counters transactionally, without repeated COUNT
scans. Add report counters `access_checks`, `access_inserts` and
`access_logical_bytes` for the enabled profile; count attempted work before its
SQL even if the transaction rolls back. The existing operation deadline and
outer CPU/memory envelope still apply; no per-pair allowance renewal.

At most `2*k*N` oriented rows and O(k) membership checks plus at most 2k B-tree
inserts per object arise for k<=8. Initial population still costs N ordinary
admissions plus pair work. No first-query build, migration, new maintenance
command, partial cache or automatic backfill is part of this version.

Pair row/byte/time/physical-DB quota failure rolls back **metadata admission**;
it must not silently omit rows or disable a pair. Shared `max_db_pages` includes
auxiliary indexes, so this optional investment competes with base index capacity.
Logical bytes are not exact SQLite physical size. Public `publish` already saves
custody preview before index admission: preserve that preview, accepted Lean
mathematics and earlier successful targets; do not claim whole-call rollback.
If an optional pair blocks indexing, atomic-profile/fresh-index choices are
operator decisions, not an automatic repair.

Identical successful admissions while quotas permit yield identical plain/pair
RecordIDs and snapshot IDs. Different capacity-induced admitted prefixes need
not yield identical roots. The invariant follows by empty-store initialization,
duplicate no-op and atomic insertion of precisely the new record's pairs.

## Ready access, exact old cuts and fallback

An enabled store is ready only when config/counters are valid and completion
sequence equals base sequence. Missing tables/config mismatch/watermark mismatch
fail; they are not legitimate absent caches. This constant-size check does not
detect arbitrary deletion of an unvisited row. Such omission remains unverified;
encountered inconsistent rows must fail the retained binding checks.

Only choose a configured pair contained in query features and containing the
existing authenticated minimum-count atomic anchor. Never reanchor on a third
feature. For old snapshot t, with original anchor count N, seek by the declared
primary key:

```text
anchor=a AND companion=b AND partition=p
AND anchor_ordinal>=start AND anchor_ordinal<N
ORDER BY anchor_ordinal LIMIT 1
```

The SQL upper bound is mandatory: do not filter an arbitrarily large later
suffix only by admission sequence. Recheck companion ordinal against its old
count, `admitted_seq<=t`, object/posting correspondence, canonical record, all
query features, and the original atomic-vector proof at the returned ordinal.
Extra query conjuncts may legitimately reject a correctly bound pair candidate;
cache/posting/old-cut inconsistencies raise instead of becoming false negatives.

Disabled access or no eligible pair chooses **atomic fallback before traversal**
under the same V2 request, `_ReadIO`, deadline and allowance. Do not call V1.page
with a fresh meter after spending planning work. Enabled corrupt state fails,
not fallback. Unsupported legacy remote route is charged incomplete/refused;
no automatic network V1 retry or negotiation is introduced.

## Exact V2 wire and accounting

Route: `/v5/discovery/sparse-candidates`.
Request/Page/Cursor schemas: `DMKN_FORMAL_CANDIDATE_REQUEST_V2`,
`DMKN_FORMAL_CANDIDATE_PAGE_V2`, `DMKN_FORMAL_CANDIDATE_CURSOR_V2`.
Request fields/limits equal V1 except schema. Cursor fields equal V1 except
schema, retaining `ADVISORY_POSITION_NOT_VERIFIED_COVERAGE` assurance.
Response fields equal V1 except schema plus `access_used`:

- `null` only for an unplanned resource refusal with `anchor_count=null`, no
  hits and unchanged next position;
- `{"kind":"atomic"}` for the sequential fallback;
- `{"kind":"pair","companion": atom}` for sparse access; companion must be a
  different requested atom. The request already binds the original anchor.

Plan before assigning a non-null response anchor_count. Access diagnostics are
provider claims, not authenticated intersection completeness. Existing finite
termination names may be reused; `anchor_boundary` remains advisory in V2.

In V2, `limits.scanned`/`charged.scanned` mean **attempted driver seeks**, including
an empty terminal seek. Charge one scanned unit before each seek, plus SQL/probe
work even when empty. Thus full traversal costs r nonempty visits plus at most
one empty end seek, not necessarily r total charges. Stopping at hit/byte caps
does not perform an extra free seek. No counter refunds the client's prepaid
maximum. Output diagnostics must state the selected mode; skipped ordinal
distance is neither charged work nor verified coverage.

A hit at original ordinal j advances next to j+1 only after proof/record/byte
checks succeed. A legitimate nonmatching row may advance after its checks.
An interrupted seek or unreported byte-exhausted hit must not advance past the
pending candidate. A successful empty seek may set next to old anchor count.

V2 verifier preserves strict request/summary/schema binding, bounded counters,
bytes, canonical record+all atomic features, partition, duplicate/order checks,
original vector proofs, exact cursor, and
`hits <= proofs <= record_loads <= charged.scanned`. It requires
`start <= next <= old_anchor_count`, with each hit in `[start,next)`.
Only V2 omits V1's `next-start <= charged.scanned` condition. V1 remains unchanged.
All mathematical-acceptance/global-completeness/verified-coverage flags remain
false. Never feed V2 into the authenticated contiguous `Coverage` path.

Positive soundness is unchanged: every accepted hit proves the same canonical
record's membership in the same atomic committed vector and satisfies the same
feature conjunction. Cache correctness affects efficiency/omission, not that
implication. It does not prove feature extraction or mathematical validity.

## Required public integration and ownership

| Seam | Exact required behavior |
|---|---|
| SearchSession.begin_candidates | Optional `mode="atomic-v1"`; `sparse-v2` constructs V2. Keep ticket operation exactly `candidates` and all existing reservations. |
| SearchSession.accept | Dispatch verifier from **held request schema**, never reply schema. Preserve full examined/scanned charge on all outcomes and existing dedup. |
| FairSearch | Constructor binds immutable `candidate_mode="atomic-v1"`; select one explicit route accordingly. Existing fair scheduling and settlement remain. |
| peer_api.find | Optional local `candidate_mode`; absence means V1. Report mode. |
| directory_find | Nested `search` forwards optional candidate_mode unchanged; directory hints cannot select it or renew a grant. |
| _index/publish/serve | Optional `index.access_pairs` passes exact config; existing state-open/create/path rules unchanged. Update exact-field validation wherever repeated, including CLI. |
| HTTP provider | Validate V2, reserve its bounded reply, narrow original timeout, dispatch one local plan; V1 route unchanged. |
| profile/package/docs | Pin/include pair_access and changed sources; document mode, capacity and incomplete outcomes. |

Root proposed ownership: this author pair_access/Store; independent reviewer
candidate_query/HTTP; root session/fair/API/profile; concept agent tests. This
table is a coordination proposal, not source-edit authority before root selects.

Reject any implementation requiring changed canonical identities, query-time
backfill, weakened positive proofs, hidden partial cache, renewed grants or
unbounded ordering. The prospective finite test plan should exercise tiny
tail-hit selectivity, both orientations, exact old cuts, rollback/quotas,
disabled/no-eligible fallback, wrong mode/schema/proof, charged failures and
public forwarding. No native proof or large-corpus rerun is needed for this
boundary. A cache is worthwhile only if repeated query savings exceed its
population/maintenance/storage/service cost; no universal benefit is asserted.
