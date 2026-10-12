# Exact-warrant preparation and semantic growth accounting

Root-selected source-only successor, 2026-10-12. No runtime or certificate.
Rust relation is owned separately; this note covers Python preparation/binding
and the consequence for reciprocal accumulation. Old aggregate-v1 bytes stay
unchanged, including the unrun v1 admission helper. Namespace: aggregate_claims.

## Two identities serve different purposes

ModuleID commits to a mathematical interface. An exact legacy journal J also
binds the relation image, foundation, policy and rank. The same interface may
have different warranted ranks; proof bytes and derivation edges themselves
are not committed by J. A chosen witness must therefore retain its own exact
parent set even when another witness concludes the same J.

V2 graph keys, edges and targets are full J. Members are ordered by full-byte
lexicographic order, not numerical rank; little-endian rank ordering is not
numeric ordering. Multiple J for one ModuleID are legal. Duplicate exact J is
conservatively refused; preparation never unions proof edges or replaces a new
target by a certified frontier. A later deduplicator would need an explicit
derivation-selection contract and a fresh closure check, not a set union.

The finite-DAG argument is unchanged: exact authenticated frontiers establish
the induction base; each independently checked local extension names only
already-established exact parents of smaller rank. A reachable finite union
of these nodes is sound under the same checking/cryptographic assumptions.
Allowing several ranks for a semantic interface does not introduce a cycle or
authorize journal substitution. It repairs a completeness-of-composition
restriction, not a discovered false-acceptance vulnerability.

## Exact format consequences

- Header: 192 bytes, DMKNA002, version2; same field offsets.
- Input: DMKNAI02, version2; targets are184-byte J, not32-byte ModuleID.
- Merkle domains: DMKN-V5-AGGREGATE-V2 followed by NUL and LEAF/NODE/ROOT and NUL.
- Cap48 counts exact warranted claims. All other inherited caps remain.
- Old header/wire/path evidence cannot be relabeled as v2. New native evidence
  remains conditional until genuine matching boundary receipts are discharged.

Python bindings and preparation are deliberately inert. They can reject a
malformed graph encoding, but cannot certify the witnesses or the receipts.
The real relation checks witnesses and complete reachability; the real host
verifies every exact pending receipt and the actual adopted image.

## Why this advances growth without manufacturing it

Independent agents need not coordinate which proof rank of a shared lemma they
use. Supporting their compatible branches removes one artificial obstacle to
reuse. It does not establish positive net growth by itself.

Count semantic modules once across warrant variants. Useful growth remains an
increase in justified capability or lower full resource cost for specified
downstream work, against the equally optimized baseline. More proofs/ranks,
larger aggregate member_count or more receipts are costs or alternative support,
not automatically new mathematical knowledge. Arbitrary rank inflation remains
subject to exact proofs, per-operation caps and local service policy.

Public variant-aware delta/import remains a separate required repair: aggregate
support alone does not change the frozen receiver's ModuleID uniqueness or
ambiguous describe_member(module) selection. No release gate is closed here.

## Decisive checks selected in principle, not yet executed

Reuse retained genuine two-delta witness bytes and native expected J. Encode
only the changed v2 framing, compare actual Rust commitments/openings to Python,
and test same-ModuleID/different-J membership and exact-target refusal boundaries.
Use source-level graph controls for honest alternate-rank branches; do not call
synthetic frontiers actual mathematical admission. Keep parse-once differential
checks against the retained old census/parser semantics. No repeat authoring,
base proof, network loop or expensive guest run is needed for these boundaries.
