# Offline directory lookup: independent source review

2026-10-28. growth_design_audit. **GO for bounded changed-boundary controls and
later coherent package selection; no runtime outcome or product adoption is
asserted.** Reviewed root's lookup_directory.py and its use of directory_index.py,
the four selected codec sources, and SELECTION.md. No owner/database, service,
runtime or Git operation was performed. The separate directory-core review is
not repeated here. No source blocker was found in the wrapper's stated contract.

## Executed-code boundary

The supported main entry requires Windows, isolated Python, disabled site and
bytecode writing, and no optimization. Package location comes from this selected
script's own file, not from the directory manifest. A caller-approved exact
PROFILE hash binds the entry and directory helper bytes. The four codec sources
also have hardcoded exact hashes; they are read and checked before execution.
The loaded directory_index is the PROFILE-selected trusted local helper, not
code selected by the historical directory's metadata.

`modules()` executes the captured bytes, avoiding a source-file reread between
hashing and compile. It creates a fresh discovery namespace with an empty search
path and loads only the specified source closure. Its actual codec imports are
standard-library dependencies and the already selected ordinary/formal modules;
no owner, native worker, provider or arbitrary adjacent plugin is imported.
The prior sys.modules entries are restored on normal or exceptional exit.
This is source pinning inside an approved interpreter, not a sandbox for an
arbitrary malicious Python PROFILE or script. Script/runtime approval remains
the caller's premise.

## Filesystem and trust boundary

All selected paths must be absolute and canonical, with no parent traversal.
Every existing path component is checked with lstat; symbolic links and Windows
reparse points refuse. Input files must be ordinary single-link regular files.
Fresh output is checked for overlap with the package, directory and names file;
the directory cannot be inside or above the package. These rules preserve the
supported protected-local-storage premise; they do not claim race-proof access
against a concurrent same-account attacker replacing files after the checks.

Manifest, query-name and selected source reads have explicit byte bounds. Profile
and JSON objects reject duplicate keys. Name input then passes the exact existing
bounded evidence parser and structured-name checks. The directory descriptor
checks its approved SHA, schema, canonical encoding, exact metadata/count/size
commitments and vector root. Wrapper additionally checks selected semantics,
foundation and name-codec identity, plus exact entries/tree logical lengths.

An approved directory SHA must come from the completed approved exporter. A
random peer's self-consistent hash does not prove complete sorting or historical
owner correspondence. Neither the script nor the Merkle membership machinery
creates that exporter premise. The module docstring and selection state this
explicitly. Current PROFILE and historical source_profile_sha256 need not be
equal: the result preserves their separate roles rather than pretending a new
package retroactively created the export.

## Point access and output semantics

The wrapper opens only the two fixed binary files and supplies range-checked
seek/read callbacks. It performs no whole-file digest, directory enumeration,
owner context reconstruction, snapshot load or proof replay. Manifest and input
files are reread at the end, but have fixed independent caps. For 1..8 requested
names, the directory helper performs binary-search probes followed by ordinal
authentication of the selected hit or adjacent absence endpoints. The fixed
record/path access is logarithmic in the selected directory count, with the
hash-collision and complete-sorted-export premises of the core contract.

Unauthenticated middle probes can cause refusal or misrouting but cannot by
themselves authorize a hit/absence. The final authenticated captured row is the
one used. Selected-file mutation is not promised to be globally detected: damage
outside the selected authenticated paths need not affect this lookup. This is
the deliberate point-verification contract, not full corpus integrity checking.

Mixed present/missing names produce DIRECTORY_NAMES_MISSING with diagnostic
bindings and missing_names, but **no specs and no SPECS.json**. Only a complete
successful conjunction produces the explicit search specs. No weaker partial
query is generated. RESULT.json can retain diagnostic partial bindings without
conferring mathematical authority. Output-directory creation happens after
lookup and selected-input checks; ordinary write failures can leave partial
files, so callers still require clean CLI completion before consuming a result.

Returned metadata identifies only the historical export. The wrapper says
mathematical_acceptance:false, unchanged recipient checking, and explicit
find-spec inputs rather than a current-owner query report. It neither checks
current support validity nor claims absence after a later root extension.

The 30-wall/20-CPU allowances are cooperative and checked around the bounded
reads/steps; they are not hard process or physical-disk containment. Path/open
and bounded parser/system-call delays can exceed a deadline before the next
check. This limitation is correctly named in the returned cost field.

## Focused validation still needed

In addition to the separately authored core controls, one relocated wrapper
boundary should exercise an approved complete historical directory, all-present
and mixed-name queries, wrong PROFILE/manifest and changed helper/codec rejection,
output overlap/reparse or hardlink rejection, and historical-source/current-
package separation. No Lean, service or theorem episode is needed. Reuse the
core's fixed-read/logarithmic and corrupt-path controls rather than duplicate them.
