# After guest03: diagnose structural representation cost before another build

Mechanism lane, source investigation only. No new implementation, build, VM,
proof allocation or larger ceiling is selected by this note. Frozen guest03,
image02 and failed snapshot01 remain unchanged. Root owns the new bounded trace.

## Actual boundary

Combined guest03/image02 still fails at the same selected session ceiling:
`33557665 >= 33554432`. No completed capsule or certificate resulted. The prior
frontend/constructor differential passes establish preserved behavior on their
selected boundaries, not a completed guest or sufficient performance. The old
guest02 partial trace cannot establish where guest03 now spends its budget.

Actual image02 has1,462,580bytes, file SHA256
`103e9fd4e80b6e6101feb89ebd0724a6010138708f169d9b9eba3b82c7e17f63`,
imageID `e44b00bbb1c675916d3060b782fec7d1eda742b5f1a4aae04b6a8554b20bbceb`.
Snapshot01 actual frame has91,387bytes including four-byte length; SHA256
`67e7485dc5167ffb75061a8bfae2afea79e7dd5efeca662896b0fad6b3a13ab1`.
Its payload is91,383UTF8bytes. The earlier zero-image held witness is91,311bytes;
only the eight image-word spellings account for this72byte difference.

## Source census: substantial immutable and multiply represented material

Read-only UTF8 parsing and recursive structural counting of the held base input
(`025d2ce3...`) gives the following. Canonical byte counting sorts object keys,
uses compact integer-only JSON and matches the complete91,311byte input. Nodes
count Values, not object keys. These are source-data counts, not measured VM
rows/instructions, allocation bytes or proof time.

| Component | Canonical UTF8 bytes | Value nodes |
|---|---:|---:|
|Whole zero-image witness|91,311|13,425|
|Native rows|56,868|6,468|
|Adopted foundation prefix within those rows|23,313|2,610|
|Eleven body openings|21,949|4,789|
|Local specification|12,376|2,155|
|Eleven body hash inputs (`expr,universes`)|21,035|4,777|
|Eleven group-leaf hash inputs (`group,index`)|12,387|2,172|

Native row census:1metadata,98names,22nonzero levels,928expressions,
6inductive blocks,3theorems,14definitions. Foundation is413rows. Local spec
contains11groups/14declarations. The last two table rows are extra hash-input
work over already represented data, not disjoint extra bytes in the witness.

The initial witness hash covers everything once. The foundation is additionally
canonicalized once and hashed twice (raw SHA and domain-framed SHA). Body and
group identities independently hash selected expanded trees. Local groups are
cloned into bindings; correspondence reconstructs type/body trees from native
DAG rows; native row decoding then constructs its typed arena. The new move
constructor removes repeated ancestor serialization but not this representational
multiplicity or DAG-to-tree expansion. The returned correspondence result also
clones every used BodyOpening although the guest uses only its census: a real
remaining copy, but not yet demonstrated as the budget-limiting cause.

The base has11group-leaf hashes and12binary Merkle branch hashes. Together with
witness, policy, foundation, body and repeated summary validation, the successful
source path contains40domain-hash calls plus one raw foundation SHA. This census
is not a claim that the failed execution reached all of them. Per-call overhead
matters: a redesign that replaces a few bulk hashes with thousands of per-node
hashes may be slower despite a better asymptotic representation.

## Kernel attribution, without another execution

The exact assembled kernel is:

```text
experiments/general-checker-guest-01/host-prepare-01/original/
risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0/zkos/v1compat/elfs/v1compat.elf
```

It is58,736bytes, SHA256
`9dd8af014a24db3752b9beda71c837f553ff361fc1bca83cc79584bd38ac9de5`.
Classify retained PCs against its load ranges in addition to user ELF symbols.
The SDK sha module chooses `guest::Impl` for target_os=zkvm, but that abstraction
does NOT establish accelerated execution. Exact retained candidate source fixes
`ExecutorImpl::circuit_version()` to `RV32IM_M3_CIRCUIT_VERSION=3`; resume writes3
to `RV32IM_VERSION_ADDR`. The exact v1compat kernel selects `sha_software`, hence
`sha2::compress256`, for that value. The earlier accelerated-SHA reading was
incorrect. New-image prefix01 attributes40,515 exclusive samples to kernel
`ecall_sha`, out of131,426 samples. This is instruction sampling, not wall time,
row share, inclusive cost or whole-execution cost. Windows9..12 contain only
sampled SHA PCs; later windows include further hashes and canonical work.

Changing the version register is not a supported proof-backend optimization:
retained `Segment::execute()` also fixes M3 and the proving preflight machine
ecall dispatcher does not support SHA. A different genuinely supported SHA
backend requires compatible execution, proving, recursion, verifier parameters,
images and actual integration evidence. Merely making execution faster by
forcing an unsupported path is not certificate soundness. No backend migration
or new hash primitive is selected.

## First structural candidate: specialize the immutable foundation

The relation already trusts one exact compiled semantic foundation with22
declarations. Every witness nonetheless transmits its same413rows, parses them,
copies the prefix, emits23,313canonical bytes and performs two SHA comparisons.
The immutable prefix is25.5% of the zero-image wire payload and40.99% of row bytes.

A concrete alternative is to embed exact foundation data in the new guest image,
omit the prefix from the new witness format, and prepend/construct those exact
native rows internally. Raw indexes in local rows can retain the existing global
offset convention; the internal environment still receives the complete prefix
before local rows. This is specialization of an already fixed assumption, not
trusting a downloaded cache or skipping checks of newly submitted mathematics.

Formal reduction: let F be the adopted prefix and R the old relation after all
hash assumptions are interpreted. Define the new relation on local input x by
running the same downstream checker on F concatenated with x. Image identity
binds F. The old input relation already requires both fixed hash equalities for
F before using it. Therefore substitution of compiled F preserves local module
admission under the same foundation and hash-collision assumptions; no new axiom
or admitted local declaration appears. The foundation has not become globally
complete or unconditionally sound merely because it is embedded.

Required conditions: the exact embedded bytes must be independently matched to
the adopted prefix; image/build manifests must bind them; native names/indexes
and all downstream correspondence/kernel checks remain; no unbound host cache
may supply F. A new wire-format/image contract is required. Old and new image
certificates cannot silently mix. The mathematical module/policy identities can
remain stable because their content semantics have not changed, but witness
identity needs an explicit decision below.

This can remove repeated foundation wire parsing and foundation hash checks.
It does not remove constructing the native foundation environment. If maintaining
the old whole-witness hash, reconstructed F still participates in that global
canonical hash; do not overclaim removal of every associated operation. The new
trace should determine whether this specialization addresses a dominant phase.

## Second structural candidate: exact wire witness binding

The journal's witness digest binds an execution witness; it is not a theorem or
module identity. Hashing the exact input payload instead of re-emitting its
canonical Value can remove one full canonical traversal/buffer. The host already
prepares canonical payloads, so those particular digest bytes would remain equal
if the same frame/domain is retained. But noncanonical JSON spellings currently
share a canonical witness digest; exact-wire binding would distinguish them.
That is an explicit contract change, not a purported byte-for-byte equivalence
over every formerly accepted byte string. Keep module/group/body identities
unchanged unless separately selecting a content-format migration.

The strict parser cannot simply lose its global checks. A DeserializeSeed with
shared remaining-node budget can count each Value once during parsing, before
large subtree allocation. Preserve duplicate-key, integer-only, trailing-input,
per-container and default serde depth restrictions. A useful lemma for this
strict domain is that compact canonical encoding never exceeds input byte length:
whitespace disappears, key permutation preserves length, u64 decimal spelling
is fixed, and valid string escapes canonicalize without increasing byte length.
That lemma requires careful UTF8/escape validation and exact encoder behavior;
it is not permission to omit a size guard on arbitrary Values. Alternatively
use a canonical-wire parser that checks canonical spelling directly, at the cost
of an explicit accepted-wire narrowing. Choose the contract transparently.

Safer API separation: keep public general parse/check unchanged; a new guest-only
wire entry performs bounded strict parsing and an internally computed exact-wire
witness hash. No public API may inject an arbitrary trusted witness digest.
Current canonical hash fixtures/native journals remain reference points, but
noncanonical-wire tests must explicitly test the new identity rule. No code is
selected here.

## Longer-term option: a canonical typed arena, not expanded trees

If the repaired trace demonstrates that descriptors/body canonical processing
remains central after fixed-context specialization, a compact typed arena can
remove both verbose JSON and DAG unfolding. Encode constructor tags, bounded
indices, literal names and topologically ordered references once. Construct
native rows/descriptor relations from that same authenticated arena, not an
independently trusted second description. Normalize universe parameters and
local/external/foundation references exactly as current correspondence does.

Do not assume a Merkle hash per term node is automatically the solution. It
introduces many short SHA calls. An alternative is a deterministic hash-consed,
postorder arena encoding with one bulk body/group commitment. Equivalent sharing
layouts then require a specified canonical node numbering/deduplication rule;
untrusted arena layout must not choose a different mathematical identity. Child
references must be strictly earlier, all roots/nodes accounted for, unused-node
and size policies explicit, and imported opaque/transparent/theorem roles retain
their present checks. Body demand still fetches the selected reachable arena,
not ancestral proof history. Group-level Merkle openings can continue providing
selective import authentication.

This is a real content-format/identity migration and a new compatibility proof,
not a minor optimization. At the present input,928expression DAG nodes versus
2,289expanded expression/level visits is a modest sharing factor, not proof of
an overwhelming arena speedup. Large shared structures create a stronger
asymptotic motivation, but a current cost decision still needs actual attribution.

## Decision rule

Use one new-image bounded trace, then choose one structural intervention tied
to its limiting phase. If fixed-prefix hashing/parsing dominates, prioritize
compiled foundation specialization and explicit wire binding. If native inference
dominates, neither will solve that central cost; analyze demanded reductions and
kernel work instead. If expanded descriptors dominate, evaluate the arena
contract and exact compatibility burden. Do not select another guest build,
increase the ceiling, or advertise useful growth merely because a source-level
optimization has been identified.

## Root-selected stronger repair: existential public conclusion

After new-image prefix01 and independent source challenge, root selects source
implementation of a NEW profile2 journal, not the exact-wire alternative above.
The new journal has magic DMKNM002, profile2,184bytes, and relation identifier
DMKN_CERTIFIED_MODULES_V2. It retains image, foundation, semantic policy,
ModuleID, group root/count and rank; it omits the whole-witness digest.

Let K(W,J) denote all old mathematical, correspondence, exact-parent verification
and rank checks, excluding assignment of the execution witness digest. The new
claim is existence of W such that K(W,J). A certificate for a theorem or module
needs existence of a checked proof, not the assertion that an arbitrary supplied
proof byte string was checked. Module/group/body identities still bind the
types and computational definitions. A parent certificate is verified against
its entire exact new journal. Induction on decreasing rank therefore remains:
each imported premise has a certified semantic conclusion; each local extension
is checked against those premises. No mathematical premise currently reads the
witness digest. Soundness assumptions of the native checker and proof system
are unchanged. This is not unconditional mathematical consistency.

New certificates deliberately do NOT certify exact source/proof provenance.
Distinct valid proofs and parent choices may produce the same conclusion at the
same rank. The host's session_binding already hashes exact image/input/expected
journal/limits/parent receipt bytes; capsule/checkpoint hashes continue binding
one local engineering run. That is reproducibility protection, not a new public
provenance guarantee. Parent journals may never be relabeled or cross-profile
mixed; new image/version/receiver migration must be explicit.

Predicted eliminated work for actual base frame: one91,383byte canonical output
and its framing/copy, plus one91,424byte SHA input (1,429SHA-256 compression
blocks including padding). This removes a whole-input linear pass and software
hash, not just its32byte public field. Node/depth/unsigned-number/canonical-byte
bounds MUST survive via independently justified validation. No measured speedup
or sufficient execution budget is claimed before a completed new guest.

Foundation specialization remains a later orthogonal option: it can remove
23,313wire bytes and its two hashes (365+366compression blocks), but not native
foundation environment construction. Exact-wire binding would eliminate only
canonical emission, not its1,429hash blocks. Shared canonical semantic DAGs
remain the asymptotic representation direction, requiring a genuine format
migration; their benefit is not replaced by this constant-factor repair.
