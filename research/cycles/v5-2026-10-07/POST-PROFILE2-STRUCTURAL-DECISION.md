# After profile2 still reaches the same ceiling: structural alternatives

Source/data analysis only. No new image, hash suite, guest build, raised cap or
proof campaign is selected by this note. Root owns the next cost decision.

Snapshot02 actually FAILED at33557665>=33554432 with clean closure and no
capsule. Removing witness provenance hashing was justified and its relation
differentials passed, but sufficient execution improvement was not established.
Segment calibration therefore remains held with no selected runtime. Do not
use the failed execution as a timing estimate for the unseen complete workload.

## Actual-input static hash census

Read-only standard-library JSON/SHA calculation on
`experiments/v5-local-checks/module-base-snapshot-02/evidence/base.frame`,
91,383bytes, SHA256
`7f998807dc2f95e3f1e3b7fdbfa70aeb30b02c9075a00295a187591688b328b7`.
The4byte framing length was checked; native input has zero parents. No native
checker, VM, proof, network call or artifact was generated. Canonical spelling
is UTF8, sorted keys, compact separators, matching this already checked fixture.

For each call, SHA compression blocks are `ceil((input_bytes+9)/64)` including
standard SHA256 padding. Domain framing contributes14+4+len(domain)+8bytes.
Merkle branches follow actual odd duplication:11leaves ->6 ->3 ->2 ->1,
therefore12branch hashes, NOT10 as in a full unpadded binary-tree formula.

| Explicit source call | Calls | Canonical content bytes | SHA input bytes | Compression blocks |
|---|---:|---:|---:|---:|
| Fixed foundation raw canonical hash |1|23313|23313|365|
| Fixed foundation domain hash |1|23313|23375|366|
| Group leaves |11|12387|12794|207|
| Group internal branches |12|1620|2064|36|
| Module summary |1|288|326|6|
| Body openings |11|21035|21376|341|

The foundation's two hashes share one canonical encoding in current source;
the two table rows must NOT be counted as two emissions. Total explicit blocks
are1321; semantic-policy hashing and implicit SDK hashes are omitted, not free.
The table contains37calls (1+1+11+12+1+11).
These are source-operation counts, not sampled proportions, cycle costs or full
execution attribution. Foundation731blocks are55.3% of this count, not runtime.
Remaining dynamic commitments cost590blocks before policy/SDK/native work.

## Candidate A: specialize the actual immutable foundation

The guest already adopts exactly413rows/22declarations through two compile-time
hash constants. Compiling the SAME bytes/rows into the image replaces a costly
run-time assertion of fixed data by the image's existing immutable code/data
binding. For a valid witness `(F,x)`, substitute the adopted F before unchanged
correspondence/native checking. For every successful specialized run there is
an original relation witness with that same F. Conversely, an original accepted
witness uses that F under its existing collision-resistance assumption, so
specialization does not add mathematical premises or remove local checking.

Minimum implementation: a fresh wire contract supplies rows AFTER the exact
foundation prefix. A generated immutable representation supplies F, then the
current correspondence/native path sees the exact concatenation. All original
node/name/level indices remain: the suffix may reference foundation indices,
and foundation has no indices into the suffix. Build/source manifests bind the
generated data to the independently adopted canonical SHA and foundation ID.
Root selects the generated source and equivalence control, not an unbound local
cache. Native-only/general public legacy relation entry can remain available
for compatibility diagnostics; certified execution uses the explicit new entry.

Important cost distinction:

- Embedding a JSON string and parsing it every run removes repeated wire bytes,
  foundation cloning/canonicalization and731SHA blocks, but NOT foundation JSON
  parsing; it merely moves that parsing from input to embedded data.
- Generated typed/value constructors remove JSON tokenization for F but still
  allocate/reconstruct its representation. They require exact generated-value
  equivalence and executable-size accounting.
- Neither alternative removes native environment construction, foundation use
  during conversion, local proof checking or dynamic group/body commitments.

Foundation ID and semantic ModuleIDs can remain unchanged if exactly the same
semantic policy/content representation remains; image/input protocol changes
still require explicit version selection. No existing receipt is relabeled.
This is relatively low compatibility risk but a fixed tax removal, not a cure
for large semantic payloads. Do not launch another expensive build solely on
the55.3% block count: identify the residual phase from the current evidence.

## Candidate B: native proof-friendly semantic commitments

Current digest computation centralizes in Rust `canonical::hash` and Python
`codec.hash_value`. The native correspondence checker validates digest syntax
and returns exact body-hash obligations; it does not hardcode SHA arithmetic in
kernel judgments. Therefore a new content-commitment suite need not alter Lean
inference, declaration visibility, original kinds, exact parents or soundness
induction. It DOES change content identities and cryptographic assumptions.

A narrow hybrid could retain SHA256 for the SMALL final module summary and for
native host/session/artifact reproducibility, while using a native proof-friendly
commitment for group leaves/nodes and bodies. The current base's dynamic large
commitments account for584explicit SHA blocks. Combined with compiled F,1315
of1321listed explicit SHA blocks disappear; the6small-summary blocks remain.
This is a source-work reduction, not a predicted99.5% execution speedup. JSON
emission/copying, native work, SDK recursion/journal hashes and new hash costs
all remain. Current-image diagnostic and actual backend validation govern whether
this is the relevant next intervention.

No generic `Poseidon2HashSuite` call can be presumed accelerated in this guest.
Assurance independently checks the exact adopted M3 syscall, replay circuit,
prover and digest convention. Host software implementation must match guest
accelerated output, not just use an identically named primitive. The SDK's
`hash_elem_slice` delegates to an UNPADDED sponge, so direct variable-length
byte hashing without its own unambiguous encoding is not a valid construction.

Minimum cryptographic protocol obligations:

1. Version/domain/suite bind every commitment and semantic policy. Separate body,
   leaf, branch and summary roles; fixed unambiguous length framing; distinguish
   old identifiers from new ones. Old native fixtures/indexes remain old evidence.
2. Injectively encode bytes/integers as canonical field inputs: never reduce
   arbitrary32bit bytes modulo BabyBear, which creates trivial collisions. A
   three-byte limb encoding is injective below its modulus; exact padding/length,
   lane order, alignment and digest serialization still need specification.
3. Use exact adopted permutation constants and sponge mode with an independent
   native/Python/guest agreement vector. Test trailing zeros, empty payload,
   block boundaries, invalid field representatives and domain separation.
4. State actual capacity/output security. Eight BabyBear output cells contain
   about248bits, so their generic collision ceiling is about124bits, not a full
   SHA256128-bit collision claim. Do not silently advertise an unproved security
   target or forget the proof system's own soundness limits.
5. Rebuild only consequential new-policy module/body/opening/discovery records,
   not old proofs. There is not yet a real v5 receipt to migrate. A global dual
   identity resolver is unnecessary for this first new profile, but no in-place
   reinterpretation of retained artifacts is allowed.

An arena/content-format migration can additionally eliminate repeated expanded
term serialization, but it is orthogonal and has a larger semantics/canonical-
numbering burden. It is not necessary merely to change a central hash suite.

## Decision criterion

If the current-image failure is still dominated by pre-native SHA/serialization,
choose one architecture-sized combined intervention justified by exact retained
backend capability and identity migration, rather than serial micro-builds.
Foundation specialization alone leaves590listed SHA blocks and all native work;
hash migration alone can leave731fixed-prefix blocks if old F checks remain.
Their composition is coherent and worth considering together. If the new prefix
instead reaches expensive native inference, these frontend counts cannot justify
the next build: investigate the actual demanded checker work first. The unchanged
2^25screen is a diagnostic budget, not a permission to inflate caps until PASS.

## New evidence supersedes hash-count-only selection

Root independently adopts actual current-image prefix02. It reaches structural
correspondence, then owned-row decoding and native parser construction by
row-equivalent windows19..24. Windows21..23 contain Serde `flat_map_take_entry`,
`Content` destruction and Value/map deserialization; finalwindow24 contains
`Parser::apply_row`, indexmap/hashbrown insertion.21,342 of131,412exclusive
samples are kernel SHA (~16.2%); this is NOT a runtime share or full-run profile.
No completed execution or bound for later kernel checking follows. This evidence
means SHA-only migration must not be selected from the block census above.

Mechanism recommendation to root: ONE combined preserved-ID repair targeting
both observed overheads before considering a full content-format migration.

**Exact compiled foundation comparator.** Retain the current input shape and
all foundation rows. Generate an immutable `StaticValue` tree from exactly the
adopted F; leaves contain fixed booleans/u64/UTF8byte strings, arrays contain
fixed ordered children, objects contain canonical ordered key/value pairs.
Compare the parsed413-row input prefix directly against this static structure.
No runtime parse of an embedded JSON string, no new heap Value copy and no
canonical emission or foundation hash is needed. Source generation must bind
exact original canonical bytes/hash, and a standalone equality control must
recover that same value. Object/array lengths and every field/value compare;
the checker never accepts a caller-provided comparator hash or success flag.

This is exact equality to adopted F, stronger than the existing two-digest
condition under their collision assumption. ModuleID/policy/JSON input schema
remain unchanged. Native correspondence, row parsing and actual foundation use
still see the original input rows and are unchanged. A new image is required.
It removes731explicit SHA blocks plus one23,313byte canonical emission, not all
foundation parsing or construction. Fixed expected metadata remains part of F.

**Non-flattening owned-row entry.** Current parser.rs144..150 deserializes every
already-owned Value as `ExportJsonObject`, whose two outer fields are both
`#[serde(flatten)]`. Those flattened deserializers materialize/buffer Content
before constructing the actual row enum. Add a separate strict entry used only
AFTER the current correspondence checker: take the map, remove its sole optional
`in`/`il`/`ie` field, require exactly one remaining variant, deserialize that
singleton directly as the EXISTING `ExportJsonVal`, then construct the existing
`ExportJsonObject` and `OwnedExportRow`. The original general and text parsers
remain unchanged. Do not rewrite all variant payloads by hand.

On the relation's exact row domain, the old flattened decoder and this direct
split have the same variant key/payload and optional u32backreference. Their
inner deserializer is identical, including kinds, original hints, numeric bounds,
opaque/module-import variants, and metadata. The new entry's stricter outer
shape is already imposed by correspondence (and fixed F); it does not narrow
successful relation witnesses. `apply_row`, duplicate-node checks, continuous
backreferences, configuration and native checking remain the same. This avoids
Value-to-Content-to-enum copying on every row, a phase actually visible in02.

Focused validation should compare actual decoded old/new row objects across
all already retained five witnesses (no need to rerun their unchanged mathematical
checks) plus changed-boundary outer-shape/refusal controls. Compare generated F
exactly with its pinned adopted value and refuse altered leaves/census/metadata.
One standalone differential build can cover both; only after independent review
should one combined guest follow. No promise of same-cap completion is made.

A compact typed canonical DAG is the larger structural option: it could remove
JSON generic trees, repeated term expansion and flattened decoding together.
But it changes canonical node numbering, identity/commitment and correspondence
contracts, Python/Rust codec and migration, and requires fresh genuine closure
arguments. The current observed direct split/comparator is a much smaller
justifiable change per removed mechanism. Root decides; no source selected here.
