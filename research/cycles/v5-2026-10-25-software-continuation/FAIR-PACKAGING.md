# Fair-search file-only package integration

Source implementation selected by root; no assembly, native execution, product
adoption or state migration is selected by this note. Preserve the used baseline
and all existing evidence. Another owner reviews integration before root selects
any bounded file-only smoke.

## Decision and complete map

Reuse a separately approved bounded ordinary-investigator package. Its selected
PROFILE, selected BUILD-RESULT receipt and installation manifest jointly identify
the complete input map. PROFILE alone is insufficient: it omits four documents.
The package has exactly 146 files: one PROFILE, 113 auxiliary files, 28
installation payloads including INSTALLATION.json, and four documents. External
Python/Lean runtime attachments listed in INSTALLATION.json are not package
payloads and are not traversed or copied.

The overlay replaces only profile.py, peer_api.py and README.md; it adds only
support/transport/fair_exchange.py and support/discovery/fair_search.py. Output
therefore has exactly 148 files, 115 profiled auxiliary files, the identical 28
installation payloads and four documents. LAUNCHER.md, PRODUCER.md and
RECEIVE-POLICY.md remain byte-identical. The new README explicitly describes the
remaining ordinary workflow and the fairness tradeoff. No native compiler runs.

The adopted input PROFILE is
`9c41b9a3fe36f7283af130ac6ef290e82c2a78c432980b2bea75ccdcf197a6d4`;
its BUILD-RESULT is
`483dcb2e318617107892df15f804c64073bbaa2144915c0717f3e5c38a5cfbd3`.
An explicitly selected compatible source build may have different native bytes.
The assembler accepts its actual manifests, not a fixed historical binary hash;
owner approval and compatibility of that build remain separate obligations.
Fixed builder/source-map identity, owner/loader version, exact role sets, exact
documentation pins and receipt-to-manifest links prevent accidental older-layout
assembly. A receipt's claim is not independent build authentication.

## Failure and trust boundary

The stdlib-only assembler requires a fresh output parent with a package child.
Receipts and failure diagnostics live outside the package. Every input role is
length/hash checked, the complete base census is exact, paths refuse redirection
and hard-linked files, copied bytes are streamed in bounded chunks, and inputs
and outputs are rechecked. PROFILE commits last inside the package. A pass needs
both successful process completion and its matching external assembly receipt;
PROFILE presence alone is not a pass. Partial output remains; no overwrite,
automatic retry, deletion, network access, package import or state access occurs.

Wall/CPU checks are cooperative; slow filesystem operations are not preempted.
An enclosing owner Job supplies whole-process containment when required.
Owner-approved immutable local storage is a premise, not hostile-writer locking.
Exact bytes demonstrate preservation, not mathematical validity, runtime
compatibility, fair global discovery, useful growth or completed v5 deployment.

The existing operator kit remains pinned to the old PROFILE. Root owns a fresh
selected integration; do not silently change its used bytes or claim it already
accepts the overlay. The common public launcher itself accepts an explicitly
selected compatible PROFILE. Its immutable run.py and native checking remain
unchanged.
