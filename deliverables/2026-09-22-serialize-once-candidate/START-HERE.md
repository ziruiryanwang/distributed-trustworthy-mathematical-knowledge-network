# Updated local v1 candidate: serialize once

2026-09-22. This is a fresh source candidate with a measured package-reader
optimization, not a public release or a completed global mathematics network.
The project license remains undecided. Nothing has been published externally.

The ten-step fresh integration run passed its operational review and separate
canonical-output audit. This qualifies the selected local workflow on the new
cut, with the limits and audit roles stated in [results](RESULTS.md).

## Download and start

[math-commons-source.zip](math-commons-source.zip) is 3,638,034 bytes and contains
112 source/document/asset payloads plus its [manifest](SOURCE-MANIFEST.json).
SHA-256:

```text
3cd159228f1e5a655203e8f4d68e3436b5b015ad21b5a4b89e950d1ab906061e
```

1. Verify the hash and extract into a **new empty installation**. Do not overlay
   an old node, reuse its configuration or rewrite a support-build receipt.
2. Follow the extracted `QUICKSTART.md` to build support, configure fresh separate
   state/scratch directories and initialize a local node.
3. Use `AGENT-QUICKSTART.md` and `make_request.py` for submission and publication.
   `API.md` documents discovery, admission and inspection; `HOSTING.md` documents
   finite local serving. Agents independently choose what to investigate.

Qualified environment: Windows x64/local NTFS, Lean 4.34.0, Python 3.14.6 with
standard-library SQLite 3.50.4. Complete compatible runtimes are prerequisites,
not included in this source ZIP. On this development machine the selected Python
is `D:\Python314\python.exe`; Lean is in the project's
`software\runtime\lean-4.34.0-windows` directory. Do not assume another Python
distribution has the required SQLite version.

The preserved test installation is `product-local/serialize-once-01/install`.
Leave it and its state/receipts unchanged; start your own node from the archive.
The corresponding editable source cut is `product-local/serialize-once-source-01`.
The earlier `software/` tree and all old installed nodes remain the baseline.

## What changed and what did not

Two helpers now compute an object's canonical encoding once when adding it.
Their two asset-lock rows were updated. No native source, mathematical asset,
canonical identifier format, peer protocol or acceptance policy changed.
There is no cache or skipped verification. The source lock still requires a
fresh support build/configuration for this new cut.

The isolated paired benchmark observed roughly 11–14% lower package-reader wall
time. This is not a whole-node/agent speedup, a new mathematical result or evidence
of scalable knowledge growth. [Evidence and limits](RESULTS.md).

Contributions still undergo local Lean checking and canonical replay; publication
does not grant receiving acceptance. Peer packages remain inert data. Owner-supplied
Lean source is authorized executable input, not hostile-source sandbox input.
There is no mandatory central server, global task queue or human-intention field.

Transport remains loopback-only. No second machine is needed for local use or
testing, but independent-host deployment is untested. Discovery, retention and
resource grants are bounded; the ZIP is not all of mathematics or an autonomous
researcher. Licensing/public redistribution remain deliberately undecided.
