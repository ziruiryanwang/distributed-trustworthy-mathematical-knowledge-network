# Remove redundant witness scans without changing mathematical identities

2026-10-12. Root theory proposal, independently challenged and adopted in
principle after the encoder-domain correction below. A fresh source-only
implementation is selected at the end; no build, guest execution, proof,
new wire format or cap increase is selected here.
The full v5 objective remains active. This is the next cost decision, not a guide.

## Why this is central now

The independently audited aggregate execution failed at its original2^25 cap.
Its retained, saturated instruction samples were attributed offline once:
`aggregate-pc-attribution-01/attribution/RESULT.json`, SHA256
`31b29b7a8888fbfa0337fbf3a72b3269d2facbf05513d0e27a23ac4ca91de84b`.
The exact `canonical_size::Census::visit` and `::string` ranges hold11,452 and
10,772 retained samples. Parsing, allocation/copying and correspondence also
appear prominently. These observations select source inspection, not measured
cycle shares, whole-run bottleneck proportions or a causal speedup estimate.
There are23,898 omitted sample events and the execution is only a failed prefix.

Current successful per-delta flow is:

    strict JSON parse -> canonical_size -> aggregate tree/schema census
                      -> relation::check -> canonical_size -> check_bound

Parse-once and theorem validation without materializing its discarded output
tree are already implemented. Do not repeat either as a new optimization.
The next proposed change removes redundant resource-validation traversals,
not mathematical checking, canonical commitments, or receipt verification.

## Lemma: canonical serialization cannot lengthen accepted raw JSON

Let P be the actual pinned strict JSON parser, K the current bounded canonical
serializer, and K_infinity the total structural encoder with identical formatting
but without K's resource refusals. P rejects duplicate object keys, negative/nonintegral numbers,
out-of-range integers and malformed UTF-8/JSON strings, and requires exact EOF
apart from permitted whitespace. The selected serde features must continue to
exclude arbitrary-precision/raw-value semantics. If P(b)=V, then

    |K_infinity(V)| <= |b|.

This statement concerns byte lengths, not equality of encodings or hashes.
K need not yet be defined: a syntax-accepted V can exceed its global node limit.
The separate structural census below is indispensable. Once its node/depth
bounds also hold, K succeeds and equals K_infinity byte for byte.
Proof is structural over the parsed JSON syntax:

- Null and Boolean spellings have fixed lengths.
- Each admitted number is a u64 written in legal JSON integer syntax. Its
  canonical shortest decimal spelling is no longer than the accepted token.
  Exponents, fractions, overflow and negative zero must remain rejected by P.
- For a decoded string, canonical output includes two quote delimiters and
  emits UTF-8 scalars unchanged except quote/backslash and ASCII controls.
  Quote/backslash require at least two raw bytes. The five short control escapes
  use two bytes; other control scalars require six. Non-ASCII scalars encoded
  directly take their UTF-8 width; a JSON unicode escape takes six bytes, or
  twelve for a surrogate pair, never less than the resulting UTF-8 width.
  An optional escaped slash or longer control spelling cannot be shorter.
  The same argument applies to object keys. Neither parser nor serializer
  normalizes Unicode or replaces the string with a different one.
- Array/object punctuation has the same necessary count in each representation.
  Child values satisfy the induction hypothesis. Key reordering changes no
  lengths. Duplicate-key refusal prevents an unmodeled object transformation.
  Inter-token whitespace and trailing permitted whitespace only add raw bytes.

Independent source review confirms the serializer's exact escape behavior and
parser number callbacks against actual1.0.151/default,std, using the guest target
fingerprint and matching compile-cache sources, not an older retained1.0.143
registry copy. Exact source bindings are in ASSURANCE.md. The argument would need revision for
a canonicalizer that normalizes strings, escapes all non-ASCII characters,
expands numbers, or accepts general floating-point values.

Corollary: the existing raw16MiB bound already guarantees the canonical16MiB
bound for values created by P. Recomputing canonical string lengths is redundant
on THIS route. Arbitrary caller-created Values do not receive this corollary.

## One immutable validated parse value

Proposed new crate-private-invariant type `BoundedValue` contains:

    value: Value, nodes: usize, maximum_depth: usize

Only a strict byte parser plus one structural census constructs it. Fields stay
private; provide an immutable Value borrow and read-only counters. No unchecked
constructor, mutable borrow, deserializer, Default or caller-supplied counts.
Consumption into the relation is limited to the crate's implementation. This
token certifies representation bounds only; it is not mathematical authority.

The structural census counts Value nodes, not object keys, with root depth0.
It retains the existing1,000,000 node/256 depth bounds and checked arithmetic.
It need not scan key/string bytes, format integers, serialize, hash or allocate
a second expression tree. The original strict parser and its actual recursion
guard remain in place; a Value-depth bound alone does not replace that guard.

The aggregate census reads the cached node count/maximum depth, charges its
stricter500,000 cumulative node and128 depth limits, and retains every existing
row/body/opening/edge/schema budget. It only borrows the immutable Value.
The relation's new typed entry consumes that same token into unchanged
`check_bound`, omitting its second canonical-size pass. Existing arbitrary-Value
`check` and existing byte entry remain validated; callers cannot use the new
entry merely by asserting that their input is already checked.

The original module relation and exact-J aggregate graph rules, conditional
premises, imported interfaces, ranks, membership and mathematical checker are
unchanged. A new compiled guest has a new A and needs explicit adoption; this
is not authority to treat its receipt as the old A. No genuine old-A aggregate
receipt currently exists, but that fact must not become a hidden upgrade rule.

## Acceptance argument

For every fixed bounded input b, both pipelines invoke the identical strict
parser and obtain the identical Value V, or both reject parsing. For successful
parses the length lemma discharges the byte constraint. The one structural
census discharges exactly the remaining canonical-size node/depth constraints.
Aggregate totals are sums/maxima of the identical per-Value counts; its schema
and other budget checks are unchanged. Its read-only inspection cannot invalidate
the token. Thus the final unchanged `check_bound` sees exactly the same Value,
and returns identical journal and exact premises, or rejects mathematical input.

Consequently the non-resource-exhausted success domain and successful public
conclusion are equal. Intermediate error order/text, partial census values on
rejected inputs, allocation failures and exhaustion timing are not promised
equal. They must never yield a successful conditional conclusion or receipt.
Global caps are not enlarged or silently interpreted as per-delta caps.

## Cost consequence and implementation choice

Let n be the Value-node count, q the total key/string bytes examined by one old
canonical-size pass, and u the old integer-digit work. Existing wrapper work
includes three node traversals and two sets of q/u work. The proposed wrapper
uses one node traversal and cached aggregate addition/max, with zero q/u work
for size validation. JSON lexical parsing, Value construction/destruction,
semantic hashes, correspondence and kernel checking remain. This establishes
removed operation classes, not a numerical whole-program speedup or cap fit.

Prefer this small unchanged-wire intervention if independently justified.
A compact tagged witness codec is a separate alternative: it can remove JSON
lexical parsing but adds a format/decoder correspondence obligation and still
retains Value allocations and semantic work. Do not build both speculatively.

Minimum later implementation evidence: focused equivalence controls for Unicode
and escaped keys/values, unsigned-number refusals, duplicate keys/EOF/recursion,
node/depth/cumulative aggregate limits, private-token nonmutability, and exact
retained native conclusions plus real invalid-proof refusal. Test only changed
boundaries; do not rerun successful network/base-proof campaigns. A new guest
screen is a later decision after native/source review, never an automatic retry.

## Source-only implementation selection

Root adopts the independent principle review, including its distinction between
the unlimited formatting function and bounded K. Base agent owns fresh
`software/v5/bounded_parse/` only: the opaque token/structural census,
thin module/aggregate source successors, and changed-boundary controls. Reuse
unchanged source via explicit paths; where privacy requires a copied module,
keep and explain the minimal diff. All used canonical/relation/census/guest
sources remain untouched. No new dependency or wire schema is authorized.

The author must first show the exact file/API plan and differential oracle;
then implementation may proceed within this source-only scope. Assurance owns
independent review. Root owns future native/build selections and actual cost
decisions. Compact binary transport remains an unselected fallback, not a
parallel implementation. No mathematical theorem-checking shortcut is permitted.
