# Preserve the module relation while removing repeated frontend work

Owner: mechanism lane. Source-plan only; receipt sources remain root-owned and
unchanged by this note. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision and evidence

Prioritize a combined frontend repair before rebuilding a move-constructor-only
guest. The actual retained trace prefix supports this priority; it does not
establish full-execution dominance or a speedup. Root's offline
`module-trace-analysis-01/evidence/RESULT.json` maps 131,491 deterministic samples
from 33,661,697 observed instructions. The run stopped at the diagnostic sample
cell cap, not successful VM completion. The SDK field named cycle is weighted
row points; the analysis uses 5,040 points per row, not instruction cycles.

Exclusive sample counts include 28,782 `write_all`, 20,170 `memcpy`, 15,462
canonical `emit`, 11,775 JSON `deserialize_any`, and 7,169 string emission.
22,680 samples are unattributed/overlapping. Windows18/19 contain substantial
`Value::deserialize`/copy samples. No correspondence or kernel attribution is
established in this retained prefix. No percentages here estimate proving time.

Source independently identifies three redundant mechanisms: full canonical
emission in `parse`, followed by immediate full witness-hash canonical emission;
owned `Value` deserialization into `Input`, recursively rebuilding already
parsed arbitrary `Value` fields; and two canonical emissions of the same
foundation-prefix `Value`. Constructor copying is a fourth, separately
source-reviewed repair with its differential check already selected.

## Invariant to preserve

For every finite byte input that reaches the existing guest relation, ignoring
resource exhaustion and permitted diagnostic-text differences, preserve its
accept/refuse outcome. On success preserve every journal byte, every exact
pending parent journal, every canonical body/descriptor/hash input, and every
native checking obligation. Native or frontend success is still not authority
for parent assumptions: guest `env::verify` and receipt resolution remain.

The new binary necessarily has a new image identity. Existing certificates do
not automatically become certificates for it. A new adopted image and separately
selected actual execution/proof remain required even under source equivalence.

## Repair A: move large fields; retain scalar deserializers

Replace only the whole-tree `serde_json::from_value::<Input>` with a typed
move-extractor. Keep serde conversions for genuinely typed leaves (`String`,
`u64`, `[u32;8]`, `usize`, `Vec<u8>`), avoiding reimplementation of their detailed
numeric/type behavior. Move arbitrary `Value` and `Vec<Value>` contents without
recursive serde reconstruction. Keep the old derives for the independent
reference test if convenient; production need not invoke them.

An important discovered compatibility condition: serde struct deserialization
is not object-only. Pinned serde_json1.0.151 `src/value/de.rs:482` accepts both a
map and an array for `deserialize_struct`; `visit_array` rejects leftover
elements. The extractor must preserve exact positional sequence alternatives:

| Struct | Exact object fields and positional sequence order |
|---|---|
| Input | schema, image, rank, local_spec, rows, parents, bodies |
| Parent | journal, openings |
| BodyOpening | universes, digest, expression |

For map input require exactly the named required fields; no unknown or missing
field. Move fields by `Map::remove` only after the census. For sequence input
require exactly7/2/3 elements respectively, then consume in declaration order.
The input `Value` cannot itself contain duplicate object keys; the unchanged
Strict raw parser remains responsible for refusing duplicate bytes.

Fields and remaining requirements:

| Field | Extraction preserving the old typed boundary |
|---|---|
| schema, body.digest | existing serde String conversion |
| image | existing serde `[u32;8]` conversion, exact length8 |
| rank | existing serde u64 conversion |
| body.universes | existing serde usize conversion on the same target |
| parent.journal | existing serde Vec<u8> conversion |
| local_spec, body.expression | move the arbitrary Value unchanged |
| rows, parent.openings | require Value::Array, move its entire Vec unchanged |
| parents, bodies | require Value::Array, map shallow struct extraction |

Do not tighten universes to host-size limits or assume native usize is the
guest's usize. The common later `universes <=256` check remains. All original
relation row/group/body/parent limits and semantic checks stay in their original
post-extraction position. An empty array may pass shape conversion and still
fail later semantics; do not confuse shape validity with admission.

The actual held guest graph selects serde_json features only `default,std`,
without arbitrary_precision/raw_value/preserve_order. Thus nested Value
deserialization is structurally the identity on this strict integer-only domain;
there are no feature-specific private-key reinterpretations to reproduce.
Record/check this graph assumption on the successor build, not just Cargo.toml.

Proof sketch: prove shallow struct extraction equivalent separately for exact
maps and exact positional arrays. Typed leaf conversions use the old operation.
For untouched Value fields, induction on scalar/array/map syntax establishes
old Value-deserialization identity under the selected feature set. Composition
gives the same Input/Parent/BodyOpening values. Error strings may differ for
manual shape refusal; the contract is acceptance and successful-value equality,
not identical diagnostic wording or malformed-input refusal order.

## Repair B: one checked canonical traversal at the guest boundary

Do not remove validation from public `canonical::parse`. Native diagnostic
hash/journal/opening actions and host preparation also call it and must retain
its current contract. Do not introduce an externally usable API that accepts a
caller-supplied witness digest or an unchecked Value as authoritative.

Preferred minimal internal factoring:

1. A private syntax parser performs the unchanged MAX_BYTES, duplicate-key,
   integer-only, trailing-input, container and serde nesting checks.
2. Public `parse(bytes)` calls it and then `canonical(value)` exactly as before.
3. A crate-private `parse_hashed(domain,bytes)` calls the same syntax parser and
   immediately `hash(domain,value)`, whose canonical traversal enforces all the
   existing global node/depth/canonical-byte/unsigned-number bounds, returning
   the validated Value and its computed digest together.
4. Public `relation::check(value)` retains its first witness hash, then calls a
   private common relation body with `(value,witness)`.
5. Public `relation::check_bytes(bytes)` calls the crate-private parse-and-hash
   helper for the fixed `module-witness` domain and the same private body.
   Guest `main` calls this new byte entry. No public arbitrary-prehash entry.

This removes one canonical traversal only in the explicitly jointly validated
guest path. The returned Value is not modified before its hash is computed.
Every non-resource syntax/structure failure formerly rejected by parse remains
rejected before Input extraction or native checking. On success the witness
equals `H_frame("module-witness", canonical(Value))` exactly. Hashing raw input
bytes instead would be wrong: whitespace or key order can differ legitimately.

An alternative is a nonforgeable module-private validated-encoding token, but
that adds interface surface without a benefit for this seam. Prefer the private
common-body factoring above.

## Repair C: reuse already checked foundation encoding

The relation currently computes `canonical(foundation_rows)` for a direct SHA
comparison, then `hash(domain,foundation_rows)`, which encodes the same immutable
Value again. Factor exact domain/length framing into a module-private helper
over a canonical byte slice. Expose only a safe combined operation that first
calls the existing canonical encoder once and returns both the encoded bytes
(or raw SHA) and the framed digest. Existing `hash(domain,value)` should use the
same framing helper. Never let external witness input assert that arbitrary
bytes are canonical or provide an authoritative precomputed digest.

The frame remains byte-for-byte:

```text
"DMKN-V5-MODULE\0" || u32be(domain.len) || domain
                   || u64be(encoded.len) || encoded
```

Domain ASCII/128-byte guard stays. The byte slice is exactly the unchanged
encoder result. Holding/reusing it cannot change either hash. Existing
foundation-id and foundation-canonical-SHA comparisons both remain mandatory.

## Changed-boundary verification, not a repeated campaign

First independently review the small extractor/call-graph changes. A standalone
serde-only differential should compare all extracted fields against the old
derived representation on the five held witnesses and focused shape cases:
top/parent/body map and sequence forms, missing/extra fields, sequence arity,
image length/range, rank type/range, byte range, universe target-size handling,
wrong container types and arbitrary nested Value retention. Do not claim its
hostusize limit proves the guestusize limit; source typing covers that difference.

For canonical factoring, reuse the held domain/hash vectors and add focused
duplicate keys, trailing input, noninteger/negative numbers and structure limits
to show the original public parse contract survives, and compare the two entry
paths' exact witness hashes. A complete new native check should use all five
held valid relation witnesses with exact old/new journals and pending parents;
only changed-entry malformed cases need new controls. This test does not replace
native soundness review or parent receipt verification.

After those boundaries pass, build one combined successor guest (frontend repair
plus independently qualified constructor move), assemble its new image, and
select one same-input bounded completion/cost screen. A second proof campaign,
unrelated peer tests, or a larger cycle budget has not been selected here. If the
screen still fails, retain it and diagnose its new limiting phase before paying
for proving. Do not label source-operation savings as measured VM/prover savings.

## Cost statement

For canonical input V with n Value nodes and encoded length b, remove one full
O(n+b) canonical traversal and one associated buffer allocation at the entry.
Move extraction visits top/container metadata plus typed small fields instead
of rebuilding every nested Value node in rows/spec/body expressions. Let m be
the number of structured parent/body records and j the parent journal bytes;
its extraction work is O(m+j) plus bounded-map operations and scalar conversion,
while it reuses the preexisting owned rows/opening vectors. Deallocation of
discarded metadata is still charged; this is not zero-cost parsing. Foundation
reuse removes one further O(n_f+b_f) traversal. SHA framing, strict parsing,
remaining correspondence, native inference, recursive verification and proof
generation remain. The retained prefix suggests these savings matter; it does
not quantify total success cost, certification break-even or useful growth.
