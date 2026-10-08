# Paged peer discovery candidate - locally qualified

2026-09-22. This source package implements bounded wire-v2 peer catalog pages.
Fifteen native-free protocol/metadata contracts and the genuine Lean
receiving/contribution workflow passed independent outcome audits. This is the
latest locally qualified candidate, superseding but preserving the
[indexed-discovery candidate](../2026-09-22-indexed-discovery-candidate/START-HERE.md).
The full project goal is unfinished. No external publication is performed and
licensing remains undecided.

[Source ZIP](math-commons-source.zip), 112 payloads plus its
[manifest](SOURCE-MANIFEST.json), 3,662,316 ZIP bytes. SHA-256:

```text
01e141823fb3eb1a48d425586672d98a4b5ce10f69ae932d67f32cba3653dffb
```

Only fresh installation/state is supported. Extract into a new directory and
follow `QUICKSTART.md` and `AGENT-QUICKSTART.md`; do not modify the retained test
installations. Prerequisites remain Windows x64/local NTFS, Python 3.14.6 with
SQLite 3.50.4 and a complete Lean 4.34.0 Windows runtime, not bundled here.

Discovery requires wire version 2, without v1 fallback. Canonical bundle framing
remains version 1 and configuration/database schema remains 4. Peers advertise
up to 256 selected entries through immutable pages of at most 32 rows/64 KiB.
This is a finite capacity ceiling, not measured throughput for 256 genuine
theorems. The existing 64 MiB bundle cap remains. A page is an untrusted hint;
acquired mathematics still requires fresh local admission. Remote symbol
filtering is not implemented.

[Executed protocol results](../../experiments/peer-discovery-v2/PROTOCOL-RESULTS.md),
[native results](../../experiments/peer-discovery-v2/NATIVE-RESULTS.md), and the
[delivery support statement](RESULTS.md) state the exact evidence and limits.
Same-host tests do not establish
independent-host deployment, autonomous discovery or useful mathematical growth.
