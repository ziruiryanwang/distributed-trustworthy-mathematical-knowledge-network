# Compact sealer closure: selected implementation disposition

2026-10-06. The exact closure analysis is retained in
[COMPACT-SEALER-DECISION.md](COMPACT-SEALER-DECISION.md); this is its implementation
index, not a second independent derivation or runtime pass.

The existing compact receiver has all 606 cryptographic closure files,
101,249,548 uncompressed bytes, including the exact same stage-capable driver
and guest as the full contributor. Therefore additional executable, runtime,
guest and formal-data payload is **zero bytes**. New source/profile/manifest
bytes are separate and must be measured after actual assembly.

Root selected `experiments/compact-sealer-01/CONTRACT.md`: source-free
`prepare-seal` and `advance`, explicit action-scoped worker permissions, full
cryptographic adoption for both, and unchanged relation, stage accounting and
same-completing-invocation cold verification. No `cert_stages.py` change is
needed. Full native authoring remains outside this closure. A definition
accepted by the native relation does not thereby gain a recursive certificate.

The source-level progress and pure test seam are in that directory's SOURCE.md.
Root alone selects assembly, tests and an actual finite preparation gate.
No preparation result, funded continuation or proof completion is asserted here.
