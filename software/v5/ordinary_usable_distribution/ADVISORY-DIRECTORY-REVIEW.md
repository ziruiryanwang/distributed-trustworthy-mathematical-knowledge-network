# Independent advisory-directory design review

The source follow-up at the end reviews the implemented core/exporter and
supersedes the earlier design's zero-entry statement. No control has been run.

2026-10-28. Source/theory only; no owner/database access, product import, runtime,
code execution or Git mutation. The canonical guard passed. This reviews the
design, not the not-yet-reviewed implementation or an executed performance claim.

**SOURCE DESIGN GO under its explicit approved-export premise.** No blocking
authentication or absence defect found in the final contract. Root separately
selected source implementation in `ordinary_name_directory/SELECTION.md`.

Reviewed identities:

- `ADVISORY-DIRECTORY-DECISION.md`:
  `4e052a96b4d5fce7ac94f3e8db5b9c5338ff813dc493924f8e8105ebe0dcec85`.
- `ordinary_name_directory/SELECTION.md`:
  `41c0cf52400062cabb08a1d1baaaae19cf018a899ad72d81ec9a01c3da0e0b54`.
- Reused `discovery/authenticated_index.py`:
  `77a12cda9dd4a303153b59d00998de8aa6bf08bb572af10136e21dfa9c96cc95`.
- Existing `ordinary_advisory_query/advisory_context.py`:
  `58e20183a71a58877a34e8c8ebd9fb384afe188bfced43d4e1b9c9eb1b66a47c`.

## Authentication and absence argument

Let C be the complete exact binding map produced by the approved full-context
advisory exporter. It validates canonical structured-name keys and SymbolIDs,
emits every key exactly once, rejects duplicate key digests, and sorts the fixed
records strictly by that digest. The small externally pinned descriptor binds
the complete count, historical identities, codec, layout and vector root.

The descriptor pin proves byte selection, not origin or completeness. The argument
requires that approved export actually occurred. A peer-authored descriptor naming
a genuine historical root cannot establish that relationship. The final decision
now states this necessary qualification; the old root ID does not authenticate
arbitrary binding records by itself.

Existing `verify_vector` binds each real ordinal, context and record digest, checks
the exact path height derived from the selected count, and reconstructs the pinned
root. The new key and row domains are distinct; fixed 32/64-byte fields avoid
ambiguous concatenation. Header-derived context isolates root/profile/semantic
generations. Reusing the existing NODE/PAD domains is safe within that context;
this does not require a second Merkle protocol.

Binary-search probes need not be authenticated. They determine only which final
certificate to attempt:

- A hit proves the captured row at its real ordinal and equality of its key digest
  to the requested digest. Under collision/second-preimage resistance, that row
  gives C's exact binding. Return the authenticated captured bytes, not a reread.
- Interior absence proves two real **consecutive** ordinals j and j+1 and strict
  `left_key < requested_key < right_key`. Complete global ordering from the approved
  export excludes the key everywhere else.
- Boundary absence proves the first or last real ordinal and the corresponding
  strict inequality. Padding, nonconsecutive bounds and equality are insufficient.

Thus malicious midpoints can cause refusal, but cannot produce a false accepted
hit or absence. Invalid final proofs must be corruption/unknown, never a miss.
Duplicate-digest rejection includes distinct names that happen to share a SymbolID;
it does not remove the cryptographic assumption for future requested names.
Count one correctly has a zero-length path. Count zero is explicitly unsupported,
consistent with the selected complete owner-root export containing its basis.

## Scope and lifecycle

The inherited advisory reader still performs complete lineage/import/operation
metadata checks under the normal owner lifecycle. That lifecycle can settle old
reservations; construction is not a database-read-only promise. It omits proof
snapshot reads and gives no module plan or mathematical authority. Export captures
the map, closes successfully, then publishes the final descriptor only after its
output and source/allowance checks. Incomplete outputs have no successful manifest.

Offline lookup loads bounded inert files only. Source withdrawal, growth or
deletion does not change the old directory; the report must clearly retain
historical coverage and no current-activity/readiness/acceptance assertion. Names
absent from this directory can exist in a newer root. Historical source PROFILE
and current lookup-tool PROFILE remain different roles.

One through eight names are a conjunction. Capture and validate the whole request;
any missing name suppresses all specs. A separate directory-result schema plus
existing direct SPECS is correct. Do not impersonate or relabel the existing
owner-query report to bypass its exact-PROFILE checks. Mathematical receiving and
contribution keep their current independent gates.

## Complexity and simpler alternatives

The cold path can make O(log N) unauthenticated fixed-size probes plus at most two
O(log N) final proof paths per requested name: O(log N), not O(log² N). Count and
arithmetic bounds must precede allocation/seeking; exact file sizes detect
truncation. No whole-file hash or owner open may be hidden in lookup. The heap
cost is linear: total payload is `64N + 32(2P-1) < 192N` bytes, with P the next
power of two. At the maximum supported count it is 128 MiB minus 32 bytes.

A plain sorted advisory index is simpler when caller-selected unverified hints
are enough, or when immutable local bytes are an accepted integrity premise.
Merkle authentication earns its added storage/mechanism only for the selected
stronger contract: exact historical projection despite later data corruption,
without an O(N) integrity scan at each cold lookup. This is an integrity/lookup
choice, not stronger mathematical acceptance. Reuse of existing vector code
keeps the additional implementation to packed storage and final-result checks.

The useful region is one export of a large stable library followed by many new
name selections. Existing saved specs remain cheaper for repeated known names.
Rebuilding on every root addition can recreate the original lifetime cost; no
automatic refresh, merge or latest-root alias should enter this implementation.
Sorting, full initial context validation, memory and storage remain paid costs.
The source argument establishes the changed cost boundary, not measured speedup,
universal benefit or worldwide discovery coverage.

## Next gate

Review the actual pure builder/reader and exporter integration, then use focused
synthetic controls for final certificates, corrupted hints, layout/domain isolation,
collision refusal, non-ASCII/numeric name encoding and all-or-nothing specs. A
bounded read-count assertion is sufficient for this access-path claim; no large
growth benchmark, native theorem run or repeated owner assurance campaign is
needed. Root owns any later execution selection.

## Source follow-up: core and export callers

2026-10-28, next_value. **SOURCE GO for the selected core and changed export
callers under the approved-export and protected-local-storage premises.** This
is static review, not an execution result. The current canonical guard passed;
no product import, syntax compilation, control execution, native process,
owner/database access, network operation or Git mutation was performed.

Reviewed current bytes:

| Source | SHA-256 |
|---|---|
| `ADVISORY-DIRECTORY-DECISION.md` | `db8695ccf25f1a644319204dbf52d25ea3ccb754971bce706505c2b32b1dfb29` |
| `ordinary_name_directory/directory_index.py` | `bd0a1fcced90c694943dc902a61cae7220c3bdf7ad0ed6c0bd464b9fbe992447` |
| `ordinary_name_directory/query.py` | `322f6d4202c0aca09e7ccb6d33b1bd7c2651776474bbfefeccfc8ab88e8781dd` |
| `ordinary_name_directory/advisory_context.py` | `42a4b204e8a2a579d49b70981b539feb7a2417bb9bc40b2b47d5883d0b4e6193` |
| `ordinary_lean/ordinary_evidence.py` | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `discovery/formal_features.py` | `f1f53ee40ce32126085f7f776c47d9d0ab2c5b7c679d40f018f6bff70f6430e5` |
| `discovery/authenticated_index.py` | `77a12cda9dd4a303153b59d00998de8aa6bf08bb572af10136e21dfa9c96cc95` |

The generic codec supports a correctly committed empty vector, using its
context-specific empty root and no entry/proof reads. The public owner exporter
requires 1..1,048,576 bindings. This distinction supersedes the earlier blanket
zero-entry exclusion; singleton proofs still have zero height. Context hashes
the exact historical metadata; count is separately bound by `vector_commit`
and the externally pinned descriptor. Actual key/record domains are
`auth.H("NAME-DIRECTORY-KEY", key)` and
`auth.H("NAME-DIRECTORY-RECORD", row)`. Storage names are `ENTRIES.bin`,
`TREE.bin`, and final `DIRECTORY.json`.

The implementation checks canonical name bytes and exact SymbolIDs before any
payload writes, sorts fixed records, rejects repeated digests even when symbols
agree, bounds count before tree allocation, and checks the canonical descriptor.
The reader authenticates a freshly captured final row at its actual ordinal,
uses those bytes directly, and proves misses only at consecutive real ordinals
or exact boundaries with strict comparisons. Hints do not authorize results.
The one-through-eight request bound, exact structured-name codec and all-or-none
spec generation are present. Initial construction remains O(N log N) sorting
and O(N) fixed-size storage/hashing plus full metadata validation. Lookup has
only fixed-width binary probes and at most two vector paths per name.

The advisory successor retains the existing private metadata-validating reader
and old one-through-eight projection. Its full-map branch copies canonical
immutable keys and valid IDs, exposes no module plan, checks activity, closes in
`finally`, and verifies closed/database/lock state before returning. The inherited
opener's reservation handling remains part of the lifecycle; no read-only database
claim is made. `run_directory` checks the exact returned identities, complete
coverage, count and closed status. It derives the name-codec pin through the
installation's evidence role, so that pin does not depend on a guessed filename.

The query caller validates its shared selected evidence/vector helpers and uses
captured, profile-pinned directory source. It checks profile/allocation after the
owner closes, creates the fresh output, and passes the same final gate to the
builder. The builder invokes that gate after writing payloads and before publishing
the descriptor. A failure retains partial files without a new valid descriptor;
the caller reports publication as UNKNOWN once build has begun. A later auxiliary
RESULT write failure does not erase or silently retry a committed directory.
No new source blocker was found in these changed paths.

The filesystem wrapper has its own independent review in
`ordinary_name_directory/LOOKUP-REVIEW.md` (`6a4a2a6cfadc54273bd4c0ddbf3437252c8988da0972f90d7d1a4e0099f835f2`)
for `lookup_directory.py` (`a7a2b63a4b815ef9c317d8da7e9bcb244f31fbd3b7d6e327071fee9f75912703`).
That review covers selected-source execution, inert filesystem/size checks,
historical semantics and direct-spec output. It still calls for a relocated
wrapper boundary; this core/exporter review does not substitute for it.

## Authored controls awaiting selected execution

`ordinary_name_directory/controls.py` is authored here and therefore is not
independently qualified by this review. Its current SHA-256 is
`831b897d5b12fd396c65e3c79a29bc3b0c816698cdd0eaefc5668bd61ab7aefb`.
Root's separate static review caught an invalid test-only use of the generic
feature validator, which accepts an older named-symbol format. That call was
removed before any execution; exact expected ordinary portable-symbol specs
remain checked. Neither implementation nor evidence was changed to fit the test.

The file contains fourteen groups: eleven pure codec/vector groups and three
caller groups. Core cases cover exact hits, each absence boundary, corrupt
midpoint steering, changed entries/siblings, truncated reads, descriptor/count/
context/size binding, cross-metadata tree separation, Unicode/numeric name
distinctions, conjunction behavior, singleton/empty vectors, deliberate digest
collision, and the final-publication gate. A 257-record synthetic case counts
every actual fixed-width read for eight names against logarithmic bounds and
less than full payload bytes. This is a small access-path control, not a speed
benchmark or full-scale measurement.

Caller cases exercise actual argument dispatch, actual `snapshot`/`project`
with explicit inert catalog/installation doubles, and actual `run_directory`
orchestration with named loader/owner doubles plus the real builder. They check
detachment, successful close before publication, empty public export refusal,
old projection compatibility, wrong-root/closure rejection and exact final-profile
failure after payload writes but before the descriptor. No real owner state,
locking, metadata lineage or mathematical grounding is established by those
doubles. Prior advisory-reader qualification is not relabeled as a new run.

Execution requires six explicit path/SHA pairs (`candidate`, `evidence`,
`features`, `auth`, `query`, `advisory`) selecting the reviewed sources above,
Windows isolated Python with `-I -S -B`, and a fresh output beneath canonical
`experiments/v5-local-checks`. The harness blocks subprocess/network/database
entrypoints, captures source bytes before loading, rechecks pins afterward, and
uses cooperative 45-wall/25-process-CPU-second bounds. An external containment
selection remains root's responsibility. No controls, imports or syntax checks
have been executed. Root owns independent control review and any later finite
execution/adoption; no native or broad assurance campaign follows from this GO.
