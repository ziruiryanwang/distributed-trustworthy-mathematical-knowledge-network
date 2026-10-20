# Efficient directory validation, not another memory campaign

2026-10-20, core_search. Source-only successor selected by root after build01
reached its original wall limit with 6,537 files/134 MB copied, no release
manifest, and about 38.7 MB peak Job memory. Preserve that partial directory and
all used predecessor bytes/evidence. No retry or budget increase is selected.

The exact predecessor distribution.py SHA256
`b6d4998462fe0f50d31b7e10f1d039c1bc8b0eef0067e02210fd0bab83ff69e9`
was read/hash-checked and copied unchanged to the fresh
`software/v5/distribution_efficient/distribution.py`; its copy hash matched
before editing. Only path validation and its operation scopes are changed.

## Mechanism and assumption

Previously every ordinary file visit performed full Path.resolve and lstat for
every ancestor. Selecting, copying, readback, census and final hash verification
repeat those visits for thousands of files. This is redundant metadata I/O,
not a byte-buffer or mathematical-verification issue.

The successor exposes `with path_scope():` backed by a ContextVar containing
only successfully checked directory strings. Canonical resolution, ordinary
directory type and nonreparse ancestry are checked once per distinct existing
directory within a scope. File names retain lexical checks; every existing
file retains a fresh lstat regular/nonreparse check. File freshness, content,
sizes, stream hashes, copy readbacks, destination exclusivity and final exact
census are not cached. A new directory is validated only after it exists.

Build, verify_release and launch each create/reset a scope. Nested final release
verification starts a new scope and restores the outer one on completion;
exception paths reset too. Standalone ordinary() outside a scope retains the
predecessor's uncached behavior. There is no cross-operation cache/adoption.

The explicit premise is owner-controlled local directories with no concurrent
filesystem mutation during an operation. This is not hostile-filesystem race
isolation. Canonical checked parent plus lexical component and fresh nonreparse
file type suffices for confinement under that premise; a file leaf no longer
re-resolves its parent chain. Exact output filename census and content pins
still bind the release independently.

For F leaf visits and D distinct existing directories, expensive directory
resolution occurs O(D) times per scope, rather than O(F); ancestor lstat work
likewise drops from repeated O(F * depth) to O(D). Small pure name checks/cache
lookups still traverse path components. Streamed payload work is unchanged.
This is a source-level mechanism argument, not a measured build-speed claim.

Root owns finite changed-boundary validation and any subsequent fresh build.
core_growth owns targeted directory-count/freshness/scope controls; reviewer
audits the successor. Do not repeat the seven unchanged distribution controls,
restart build01, widen its budgets, tune memory, regenerate proofs, or claim
that these source changes have already produced an installation.
