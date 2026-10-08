# One-pass peer service candidate - locally qualified

2026-09-22. This is the latest locally qualified source candidate. It keeps
the wire-v2 paged protocol and changes ordinary owner service startup to
authenticate a frozen view once per session. Its native-free differential,
fresh 20-step Lean receiving/contribution chain and two-slot product hosting
gate have separate scoped independent passing audits. Read the
[supported result and limits](RESULTS.md) before using it. The
[paged peer candidate](../2026-09-22-paged-peer-candidate/START-HERE.md)
remains a preserved predecessor.

[Source ZIP](math-commons-source.zip) and [manifest](SOURCE-MANIFEST.json):
112 payload files, 3,666,368 ZIP bytes, 3,621,056 payload bytes. SHA-256:

```text
6d406e1bd0f9d2e2c5757d99b448ae02e105236a5965a9de7a307f43fe6663c3
```

The manifest SHA-256 is
`1f3c345569bcb511fea67d62d42d457824d10567b08e926af0aa3b9f5779f9a6`.
The packager's `DEVELOPMENT_SOURCE_PACKAGED_UNQUALIFIED` marker is preserved as
a pre-audit machine record. Root verified every payload on a fresh extraction
at `product-local/onepass-native-01/install`, then completed the audited native
run there. A separate fresh extraction at
`product-local/onepass-hosting-01/install` was used for the product hosting
gate. Both are used evidence installations, not editable next-development
trees.

Relative to the paged predecessor, exactly `py/peer_service.py`,
`py/service_worker.py` and eight packaged Markdown documents changed. No
mathematical checker, canonical codec, Lean source, asset, wire schema,
database schema, peer route or bundle format changed. Fresh installation and
fresh state remain required; do not overwrite an existing node.

The archive's `QUICKSTART.md`, `AGENT-QUICKSTART.md`, `API.md`, `HOSTING.md`,
`PEER.md` and `RECOVERY.md` provide local commands and limits. The selected
environment remains Windows x64/local NTFS with Python 3.14.6/SQLite 3.50.4
and a complete Lean 4.34.0 Windows distribution. Runtime binaries are not
bundled. Direct service is loopback only; the authenticated SSH forwarding
recipe is documented but not independently hosted or qualified on a second
machine. Licensing remains undecided, and nothing was externally published.

The [one-pass contract](../../experiments/peer-service-onepass/CONTRACT.md)
and [audited outcomes](RESULTS.md) delimit the evidence. It does not establish
independent-host availability, useful mathematical growth, an end-to-end
speedup or a completed public v1.
