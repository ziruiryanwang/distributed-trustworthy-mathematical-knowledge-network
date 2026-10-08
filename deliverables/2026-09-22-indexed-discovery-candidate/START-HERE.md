# Local candidate: indexed formal discovery

2026-09-22. The updated local candidate passes the scoped native workflow,
independent operational review and canonical audit. It supersedes the earlier
serialize-once candidate for this local profile; all older artifacts are
preserved. It is not an external release or an independently hosted network.
Licensing is undecided.

## Source package and setup

[math-commons-source.zip](math-commons-source.zip) contains 112 source/document/
asset payloads plus its [manifest](SOURCE-MANIFEST.json); 3,647,576 ZIP bytes.
SHA-256:

```text
0f8c7d3fd853abf09fd8eecf5fa6920df948be2aae1c9bcc50cca3edb7835f74
```

1. Verify the hash and extract into a new, empty installation directory.
2. Follow the extracted `QUICKSTART.md` to build support, configure fresh
   separate state/scratch directories and initialize a local node.
3. Follow `AGENT-QUICKSTART.md` for ordinary request generation, contribution,
   exact-symbol search and local admission; `API.md` defines the full interface.

This cut requires **fresh schema-4 configuration and storage**. Do not overwrite
an old installation, edit its version number, reuse its database, or rewrite a
support-build receipt. There is no in-place schema-3 migration. Canonical
mathematical identities and the native stage-plan format are unchanged.

Qualified test environment: Windows x64/local NTFS, Lean 4.34.0, Python 3.14.6
with SQLite 3.50.4. Compatible complete runtimes are prerequisites, not bundled
in the ZIP. The selected development runtimes are `D:\Python314\python.exe`
and the project's `software/runtime/lean-4.34.0-windows` directory. Leave the
preserved test installation `product-local/indexed-discovery-01/install` and its
state/receipts unchanged. Start your own node from the archive.

## What this adds

The ordinary find helper/API now accepts one optional exact formal type-symbol
key. A persistent transactional index selects matching local candidates without
scanning every stored result. Returned metadata exposes those keys; snapshots,
bounded pages and client-owned cursors keep queries reproducible within a local
catalog. A hit is a candidate, not a trusted proof: use separate local admission.

The cut retains the earlier serialize-once package-reader improvement. No Lean
source, mathematical asset, canonical codec, checker or wire protocol changed
in this indexing integration. The editable cut is
`product-local/indexed-discovery-source-01`, not the older root `software/` tree.

The [results and limitations](RESULTS.md) distinguish sixteen metadata contracts
from the fresh real-Lean reciprocal workflow. This is exact local type-symbol
membership, not semantic theorem search or a global synchronized index. Remote
catalogs still have a separate 32-entry ceiling, and transport is loopback-only.
No second machine is necessary for this local use/test profile; independent-host
operation remains unqualified. No autonomous research or useful-growth claim
follows from the deliberately tiny proof fixture.

There is no mandatory central server, global mathematical task queue, or human-
intention acceptance field. Agents choose investigations outside the core.
Owner-supplied Lean source is trusted executable local input; peers exchange
inert packages and cannot supply executable source through the peer protocol.
Nothing has been published externally, and public redistribution licensing
remains deliberately undecided.
