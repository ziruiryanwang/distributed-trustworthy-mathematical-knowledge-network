# Frozen advisory name directory: decision and minimum contract

2026-10-28, query_scaling. Source/theory only; no implementation, runtime, owner
database access, imports, schema change or Git operation. **The changed contract
is useful and materially simpler than a maintained current-root index. Select the
static authenticated directory as the candidate for separate implementation
selection and review.** It pays one full metadata export for many different exact
names discovered during investigation of a large installed library. It does not
merely cache the eight names already queried, and it does not solve natural-language
or unknown-spelling discovery.

## What this changes

POINT-QUERY-DECISION rejected cheap point lookup with the *same freshly validated
current-context contract*. This directory has a different contract: supplied
search inputs from one explicit historical export. Lookup never opens the owner,
checks its current activity, restores snapshots or asserts membership in a newer
root. Later growth, withdrawal or deletion does not silently change the selected
directory. Native mathematical acceptance remains wholly independent.

Let C_r be the exact binding map obtained by the approved exporter through the
existing complete advisory metadata validation at root r. A valid directory
contains every `(name_key, SymbolID)` in C_r exactly once. Its lookup returns the
restriction to requested exact names, or directory-local absence. The stronger
historical-projection claim assumes **an approved export actually constructed the
directory from C_r**. A pinned peer-authored descriptor merely naming a genuine
root cannot establish that premise. Hashes select bytes; the Merkle commitment
does not prove export origin, complete coverage, sortedness or mathematics.

## Existing mechanisms and the actual seam

No equivalent root-wide indexed advisory directory was found in the inspected
sources. Saved query BINDINGS/SPECS cover the requested names; prepared contribution
bindings and reference-continuation maps serve particular authoring/continuation
work. The fixed basis query covers the pinned basis, while anchor/received queries
still derive selected bindings through their own context or realization work.
Custody's `names(module,name)->group` index belongs to the separate module-object
representation; ordinary custody indexes ExportIDs, and provider discovery indexes
features. None supplies this complete selected ordinary-root name map.

The project-authoring descriptor lists module name, project cwd/search paths and
imports (`ordinary_report_selection/prepare.py:438-461`); it supplies no complete
exact-name-to-SymbolID inventory. Extracting all names from approved Lean modules
would add different loading/export work and would not establish this owner-root
association for free.

The actual source seam is `ordinary_advisory_query/advisory_context.py:133-148`:
its private reader already constructs the complete validated context before
discarding unrequested bindings. A fresh auxiliary successor can share that same
reader/policy between existing projection and a detached whole-map export. Do not
raise the ordinary eight-name request cap, duplicate the validator, or replace
admission's catalog reader. Keep all lineage/import/operation metadata checks,
snapshot-read omission, owner locking, recovery and close-before-publication.

Root's proposed additional `query.py` input mode `--directory-export v1`, through
the existing finite launcher, is a suitable public construction boundary. It
avoids a second unsupervised owner-opening utility. Package auxiliary/launcher
pins change; native/core support and existing root identities need not. Offline
lookup needs only the pinned inert name codec and directory/proof code, not a
full NativeInstallation or owner opening. A separately selected source contract
must make this dependency reduction concrete.

## Minimum format and construction

Use a fresh directory outside owner, custody and installation trees, containing
fixed names `ENTRIES.bin`, `TREE.bin`, and small canonical `DIRECTORY.json` published
last. No embedded path is followed. Root's proposed pure interfaces
`build(bindings, output, metadata, evidence, auth, check, final_check)` and
`lookup(root, manifest_sha256, names, evidence, auth, check)` fit this boundary; the
public exporter, not arbitrary supplied metadata, establishes the export premise.

- Capture the complete map while holding the existing owner lifecycle; verify
  exact canonical keys with existing `ordinary_evidence.name_key`, valid SymbolIDs
  and count. Close successfully before publishing a complete export. A failure
  retains incomplete files with no final descriptor; never overwrite a directory.
- Set `K = auth.H("NAME-DIRECTORY-KEY", name_key)` (decoded to 32 bytes) and store each
  64-byte row as `K[32] || SymbolID[32]`, sorted strictly by K. Reject any duplicate
  digest, including two different names mapping to the same SymbolID. Preserve
  all ordinary basis and extension names; SymbolID is not universally ExportID.
- Public whole-root export requires N in 1..1,048,576; zero is refused there.
  The pure codec may support zero as the existing empty-vector relation, without
  pretending that an approved ordinary root has no basis. Let P be the next power
  of two at least max(1,N). `ENTRIES.bin` is exactly 64N bytes. `TREE.bin` is a complete binary heap
  of exactly 32(2P-1) bytes. Bounds, arithmetic and file offsets are checked before
  allocation, seeking or reading. Build has explicit row/output/time/memory caps;
  it may fail rather than publish partial coverage.
- Reuse the existing domain-separated vector relation in
  `discovery/authenticated_index.py:53-66,89-97,182-188`, rather than introduce a
  mutable authenticated index. Inject the selected existing pure
  `discovery.authenticated_index` module as `auth`, with its existing
  `discovery.formal_features` dependency; only packed heap storage is new.
  `RID = auth.H("NAME-DIRECTORY-RECORD", row64)`. The vector context uses
  `auth.digest("DMKN-HISTORICAL-NAME-DIRECTORY-CONTEXT-V1", metadata)`.
  Leaves bind context, real ordinal and RID; internal nodes and padding use the
  existing NODE/PAD rules; `vector_commit` additionally binds count. Count one
  has height zero; ordinary exported roots
  normally contain at least the basis.
- The pinned descriptor includes format/schema, N (which uniquely determines P) and exact file lengths,
  vector context/root, source semantic/foundation/implementation/store/root IDs,
  historical source PROFILE, name-codec pin, export UTC, and explicit complete
  recorded-binding coverage. Current activity, snapshot integrity, load readiness
  and mathematical acceptance are not asserted. Source profile remains distinct
  from the current lookup tool's selection. Optional full-file digests are audit
  aids, not mandatory per-lookup scans.

Sorting and complete coverage must be checked during this one construction. A
Merkle tree over arbitrarily sorted or incomplete rows cannot provide the promised
directory absence. The final source/allowance checks and owner closure precede
the descriptor commit. The caller supplies `final_check` for package verification
and allowance before that commit. A later auxiliary RESULT-report failure cannot
undo a completed directory; report that distinction and preserve its bytes.
Export time is recorded provenance, not authenticated time.

## Bounded lookup and corruption behavior

Each lookup externally selects the descriptor's digest, checks its bounded schema
and file lengths, captures one through eight exact request names, and computes K
with the selected codec. It opens only the two selected data files. No whole-file
hash, `integrity_check`, full export enumeration, source profile reload or owner
state validation is hidden in the cold lookup path.

Binary-search midpoint rows may be unauthenticated. They only choose a bounded
route. Before returning a result, verify against the pinned vector root:

- A hit authenticates the exact ordinal and **captured 64-byte row**, with K equal
  to the query digest. Build the returned binding/spec from those captured bytes;
  do not authenticate one read then return an unverified reread.
- Interior absence authenticates real rows at consecutive ordinals j and j+1,
  with their strictly ordered keys bracketing K. Boundary absence authenticates
  ordinal 0 or N-1 with the corresponding strict inequality. Padding is never an
  absence endpoint. One-row hit/boundary cases use an empty authentication path.
- Invalid paths, offsets, counts, endpoint relations or final proofs return
  corruption/incomplete lookup, not absence. All requested names must resolve
  before emitting their conjunction; never silently drop a missing reference.

Under collision/second-preimage resistance and the approved sorted complete
export premise, corrupt midpoints can cause refusal but cannot produce an
incorrect authenticated hit or directory absence. Duplicate-digest rejection at
build does not eliminate the hash assumption for later queries. Merkle integrity
does not turn the resulting spec into acceptance authority or a current-root claim.

Emit a new directory-result schema plus ordinary direct `SPECS.json`; do not
impersonate the existing owner-query report. The existing preparer accepts direct
specs. Its `query_report` mode still requires the exact matching PROFILE. A miss
means only no row in this selected historical directory, never global absence or
absence from a newer root. Later replacement requires an explicitly selected new
immutable export; there is no automatic refresh, merge or latest-root alias.

## Why choose this over the simpler alternatives

An immutable SQLite name table would provide point reads, but adds SQLite schema,
page/journal handling and a local file-integrity premise. A sorted exact-key
offset file is simpler if entirely unverified hints suffice; its variable rows
also preserve names for later browsing. Both can be acceptable under a candid
local-immutable-bytes premise, but neither establishes exact historical lookup
after storage corruption without a full scan or extra commitment structure.

The fixed-row Merkle option earns its small extra proof mechanism by preserving
that historical projection at logarithmic cold-read cost. Existing vector proof
logic already supplies the relation. It needs no mutable catalog index, cache
invalidation, new checking authority, per-root append protocol, SQL migration or
native rebuild. Omitting full names intentionally excludes browsing/prefix search;
do not add those features without a separate practical need.

For Q fresh name selections from one stable root, current cost repeats the full
metadata/opening cost C each time. This candidate pays C once, O(N log N) sorting,
O(N) tree/write work and retained storage, then O(k log N) fixed-record/proof work
per request of k<=8 names, plus small inert startup. Full heap plus entries is
less than 192N bytes; at N=1,048,576 it is 128 MiB minus 32 bytes, excluding the
small descriptor/filesystem overhead. The exporter still inherits current large
context-memory and finite-limit constraints; lookup is the improved boundary.

This is justified for a grounded large library that investigators consult through
many different names over time. Reusing a few already known specs remains cheaper.
Rebuilding after every growing-root addition can reproduce the quadratic cost,
so retain a stable library directory and use ordinary fresh projection for names
outside its coverage until a new export is worth its full cost. No throughput,
growth-speedup or universal payoff is claimed from source analysis. The next gate
is a small independently reviewed implementation/finite boundary selection, not
another mathematical campaign or an expansion into general discovery indexing.
