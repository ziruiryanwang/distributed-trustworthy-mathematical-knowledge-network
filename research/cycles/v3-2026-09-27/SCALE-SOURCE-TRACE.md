# Scale redesign: additional primary-source checks

2026-09-27. Root read-only network checks; no source checkout, compilation,
dependency installation, proof-generation service or external write.

The existing succinct bibliography is reused. New facts checked directly:

- Crossref metadata for DOI10.1145/3658644.3670322 names Evan Laufer,
  Alex Ozdemir and Dan Boneh and title *zkPi: Proving Lean Theorems in
  Zero-Knowledge*. This reconfirms metadata, not a fresh full-paper audit.
- The public repository [emlaufer/zkpi](https://github.com/emlaufer/zkpi)
  resolves at the inspected master revision
  `ff136f79ca5843cafed61bc1222a5dd85d7a8646`.
- Its [Lean example toolchain](https://github.com/emlaufer/zkpi/blob/ff136f79ca5843cafed61bc1222a5dd85d7a8646/Lean4Examples/lean-toolchain)
  explicitly selects `leanprover/lean4:v4.8.0-rc1`, not this project's4.34.0.
- Its root [Cargo manifest](https://github.com/emlaufer/zkpi/blob/ff136f79ca5843cafed61bc1222a5dd85d7a8646/Cargo.toml)
  names package `zkpi` version0.1.0, Rust edition2021. The root listing has
  no README.md; a direct README request returned404. No operational readiness,
  exact supported Lean fragment, recursive-composition support or compatible
  proof format can be inferred from the project title or manifest.

Conclusion: this is a relevant concrete research/code precedent, **not** a
drop-in verified backend for our current Lean runtime or canonical format.
Version alignment, supported typing/conversion rules, canonical binding,
recursive composition, security assumptions and actual prover/verifier costs
must be established before adoption. No measured performance is borrowed.

Local read-only command lookup found git, but no cargo/rustc on PATH. This is
not an exhaustive filesystem claim or authority to install another runtime.
