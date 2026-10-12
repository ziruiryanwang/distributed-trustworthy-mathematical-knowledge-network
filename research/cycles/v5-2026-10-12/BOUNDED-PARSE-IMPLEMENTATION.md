# Bounded-parse source implementation

2026-10-12. Owner: `v5_base_actual_audit`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

Root selected source-only implementation under
`software/v5/bounded_parse/`, following `BOUNDED-PARSE-DECISION.md` and its
independently reviewed K-infinity length lemma. Used predecessor bytes remain
unchanged. No build, runtime, dependency, wire-format or Git operation is included.
The independent control author owns `controls.rs` and its separate checkpoint.

## Exact file and API plan (before implementation)

| New file | Minimal change or explicit reuse |
|---|---|
| `canonical.rs` | Exact copy of `modules/receipt/src/canonical.rs`, plus opaque token and strict-parser/structural-census entry. Copying is necessary because `parse_syntax` is private. Existing functions, including arbitrary-value `canonical_size`, stay unchanged. |
| `module_relation.rs` | Exact copy of `modules/receipt/src/relation.rs`; add typed consuming entry and route byte entry through it. Arbitrary-value `check` and private `check_bound` stay unchanged. |
| `module_lib.rs` | Thin crate root: select the two files above; reuse existing input, foundation, commitments, journal and policy through explicit paths. |
| `census.rs` | Copy of `aggregate_parse_once/census.rs`; charge token's exact cached nodes/depth, retaining all tighter cumulative/global limits and field/row/body/opening/edge checks. |
| `aggregate_relation.rs` | Copy of `aggregate_claims/relation.rs`; change the single new-delta call from `check(Value)` to typed `check_validated(BoundedValue)`. All graph rules and mathematical paths remain unchanged. |
| `aggregate_lib.rs` | Thin crate root: select new census/relation; reuse exact-J header, membership and wire by explicit paths. Attach only new independent controls under `cfg(test)`. |

No new manifests or compiler/build adapters are owned by this author. Root can
later select these crate roots against retained dependencies, without rebuilding
the checker or running old complete suites. New image adoption remains separate.

The exact proposed API is:

```rust
// canonical module
pub struct BoundedValue { /* private owned Value, nodes, maximum_depth */ }
impl BoundedValue {
    pub fn as_value(&self) -> &serde_json::Value;
    pub fn nodes(&self) -> usize;
    pub fn maximum_depth(&self) -> usize;
    pub(crate) fn into_value(self) -> serde_json::Value;
}
pub fn parse_bounded(bytes: &[u8]) -> R<BoundedValue>;

// module relation
pub fn check_validated(input: BoundedValue) -> R<RelationConclusion>;

// aggregate census (not exported as a new public protocol)
pub(crate) fn charge(&mut self, bytes: &[u8]) -> R<BoundedValue>;
```

Only `parse_bounded` constructs tokens. It calls the unchanged private strict
parser, then one checked node/depth traversal with unchanged 1,000,000/256 bounds,
counting values but not keys at root depth zero. No string scans, integer
formatting, canonical serialization or hashing are needed for this resource
check, under root's length lemma and pinned serde feature assumptions.

No mutable borrow, public constructor, `From<Value>`, `Deserialize`, `Default`,
`DerefMut`, unchecked counts or clone is exposed. `into_value` is crate-private;
the external aggregate crate can only inspect and pass the token to the typed
relation entry. Existing `parse_validated` remains unchanged for API compatibility
and as a useful independently selected differential reference.

## Focused differential oracle and refusal boundary

The independent author receives this API before production implementation.
`aggregate_lib.rs` will use `#[cfg(test)] mod controls;`, so the new controls can
exercise its private `census::Census::charge`. They may include the preserved
`aggregate_parse_once/census.rs` as a test-only reference and call unchanged
`canonical::parse_validated`/`canonical_size` through the linked new module crate.
No production reference implementation or checker reimplementation is needed.

For fixed bytes b, compare new parse acceptance with unchanged `parse_validated`;
on success compare exact Values and independently counted node/depth metadata.
For aggregate fixtures, compare success/refusal and successful census fields
against old charge, preserving object/array record alternatives. Do not require
identical partial counters or error text on refusal. Seed existing public Census
counter fields near real aggregate limits to test cumulative rather than per-frame
accounting with small inputs. Root subsequently approved private scanner bound
parameters, called with fixed production limits, plus this counter-only seam:

```rust
#[cfg(test)]
pub(super) fn test_shape(value: &Value, node_limit: usize, depth_limit: usize)
    -> R<(usize, usize)>;
```

The aggregate test module includes the same `canonical.rs` by explicit path to
access this seam under `cfg(test)`; it calls only this copy's counters. All genuine
tokens still come from the linked production module crate. No test-only token
constructor or public parameterized parser exists. This needs only the existing
pinned serde/serde_json/RISC0 externs, not an extra dependency or module-test build.

Cover escapes/Unicode/u64 maxima and malformed number/duplicate/EOF/recursion
cases, a raw-size refusal, and the whole-value node limit that raw-size cannot
establish. Any large exact node-limit fixture must be bounded and separately
selected by root; syntax alone is not an authority to run it. Privacy/ownership
misuse checks must fail compilation if tested later; do not expose a test-only
unchecked token constructor. The existing arbitrary-value entry must still
refuse values outside the canonical domain.

Later native evidence should reuse the retained positive two-delta bytes and
recorded expected conclusion, plus the previously specified genuine invalid-proof
input, against the new roots. Compare exact public output and refusal without
replaying the old baseline. This is a proposal only; root owns all runtime and
finite selection. No guest execution or cap increase follows automatically.

## State

Plan sent to root, control author and assurance before source implementation.
Root adopted this plan before implementation. All six production files are now
written, source only. Independent assurance cleared all six production files at
the hashes below, including the full minimal diffs, reused module paths, immutable
token invariant and nonminting test seam. Control/build/runtime review remains
separate; no compiler, tests,
driver, guest, proof or network was invoked by this author. Root separately owns
new `bounded_parse/build.py` and future exact build selections; the control author
owns `controls.rs` and its checkpoint.

| Production file | Bytes | SHA-256 |
|---|---:|---|
| `canonical.rs` | 13804 | `f8356d9300f5436b3b6fb7a76b7d2d19e0b3dcedae0bfd00e1e10abea54de9c1` |
| `module_relation.rs` | 7523 | `0f78c1663673f291c7b612cc3bdef423124cc6cc47fd649b71e5bc13d4cd808a` |
| `census.rs` | 2508 | `48cad55b54d3cd233d760871308ccfdc54bb50711adb89651f7d2861caa5a1d5` |
| `aggregate_relation.rs` | 10246 | `6a2425aa6d26bf10ab6053d92f498d09b6c7bdde598efe118a5bc7bd2ceb0947` |
| `module_lib.rs` | 478 | `328692d04054f54bcb79ce316b14df6c472590160b39615942a027202d55be76` |
| `aggregate_lib.rs` | 355 | `4476115a65c03d5c81250017d4308b2dc8e3d64b8c2190f428c30ac03ed1098a` |

Read-only source-string comparison establishes: removing the new token/scanner
block from new `canonical.rs` reproduces the old file exactly; the complete
private `check_bound` and arbitrary-value `check` texts are identical; undoing
the sole aggregate call/comment replacement reproduces its predecessor exactly.
These are source identity checks, not compilation, behavioral tests or proof of
the source-level equivalence argument. The old sources were read, never edited.

The only census semantic change is replacing its tree walk with the token's
exact counts/max-depth; every existing field and arithmetic budget check remains.
Failure counter ordering may differ as allowed by the decision, while no failing
charge returns a token or aggregate conclusion. The test-only counter helper
cannot mint tokens and is absent from production builds. In particular, shape
counts on an arbitrary `Value` do not establish its numeric/canonical validity.
