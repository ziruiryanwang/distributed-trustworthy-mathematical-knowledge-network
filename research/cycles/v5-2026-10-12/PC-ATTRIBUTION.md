# Exact-image attribution of bounded instruction samples

Source-only plan, 2026-10-12. Owner: `v5_base_actual_audit`. Canonical project:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

This answers one concrete question for the already planned aggregate snapshot:
which machine-code ranges contain its recorded instruction samples? It does not
select another execution, test, compiler, proof or profiler campaign. No current
aggregate sample distribution is claimed here. Root owns execution and actual
result adoption; the root-owned `AGGREGATE-COST-SCREEN.md` is unchanged.

## Recommendation

Use a small offline, standard-library-only interval attribution helper after
actual snapshot diagnostics exist. Bind those diagnostics through the selected
assembled image to the exact user ELF and that ELF's actual linker map. Report
sample counts by exact machine-code symbol/range, with explicit unknown,
section-only and ambiguous buckets. Keep raw PCs, names and per-window counts.

Do not rebuild with debug symbols or rerun a successful guest for profiling.
Do not claim that the resulting sample fraction is a cycle fraction, proof-cost
fraction, caller-inclusive profile, or statistical confidence interval. This
is a bounded diagnostic for choosing the next source inspection, not a new
mathematical acceptance or growth criterion.

## Source-backed measurement convention

`software/v5/aggregate_host/aggregate_host.rs`, SHA-256
`7548e5b2092f3ece5d9ef93cef6c7ccd7d5e01ad123053f28e836558617857ca`, defines
`Samples::observe` at lines 152 onward. It observes only `InstructionStart`,
counts every such event, and retains event numbers

\[
1,\ 257,\ 513,\ldots
\]

because `SAMPLE_STRIDE = 256`. A retained cell is `(cycle >> 20, pc)`; its count
is incremented whenever that pair is sampled. At 131,072 distinct cells, a new
unseen pair is omitted and counted, while existing cells can still increase.
Therefore cell saturation biases the retained histogram toward already-seen
pairs; even a stable total omission fraction does not give uniform coverage.

The selected SDK tree is under
`experiments/general-checker-guest-01/host-prepare-01/candidate/` followed by
`risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8/risc0/`.
Its relevant source is:

| Source | Exact consequence |
|---|---|
| `circuit/rv32im/src/trace.rs:29` | `InstructionStart` carries a `u32` PC and `u64` reported cycle field. |
| `circuit/rv32im/src/execute/executor.rs:712` | The executor PC is a `ByteAddr`. |
| `circuit/rv32im/src/execute/executor.rs:741` | The callback emits `pc: self.pc.0` and `cycle: self.get_row_points()`. |
| `circuit/rv32im/src/execute/executor.rs:699` | Reported row points combine `row_info.row_points` with tracked block row points. |
| `binfmt/src/elf.rs:48` | ELF load segments are installed at their `p_vaddr` byte addresses. |
| `binfmt/src/elf.rs:398` | `ProgramBinary` packages the unchanged user and kernel ELFs; its loader combines their memory images without rebasing user code. |

Inspected executor SHA-256:
`d557a537e2b009977a13abf8313f2a0969ff691f02fc7c624078b2e3b6fad004`.
Inspected ELF loader SHA-256:
`7f52ff50c60e102efe7e61faae19b5be0427dccd1cafc3866981e3c9a24ed4d8`.
Actual attribution must retain the already adopted SDK/source-to-host binding;
these inspected sources do not independently requalify a different host binary.

Thus the address conversion is simply

\[
\text{link-map virtual byte address}=\text{recorded PC}.
\]

There is no factor of four, image-header offset, ASLR slide, or subtraction of
the user code's initial address. The `cycle` field's name does not make it an
instruction count or a timing measurement. Window `w` means only that the SDK
reported a row-point value in `[w*2^20, (w+1)*2^20)` at that sampled event.
The host separately reports backwards-cycle events. If any occur, window order
must not be advertised as a chronological execution-phase partition.

## Exact identity chain: two different meanings of ELF

The snapshot host names its combined input `elf`; its diagnostic `elf_sha256`
is the hash of the assembled `ProgramBinary` bytes, not the raw user ELF hash.
This distinction is necessary to avoid silently symbolizing the wrong image.

The offline input contract must bind:

1. An actual host diagnostic and its outer operation/source evidence.
2. `diagnostic.aggregate_image` and `diagnostic.elf_sha256` to the actual
   adopted assembly RESULT's image ID and `aggregate_image.bin` file hash.
3. Assembly COMMAND's pinned `user_elf` and actual successful compile RESULT's
   `artifact.user_elf` to exactly the same file, byte count and hash.
4. That compile RESULT's `artifact.link_map` to the exact map being parsed.
5. The actual user ELF's executable `PT_LOAD` ranges, which delimit possible
   user-code attribution. The pinned ELF summary is useful supporting evidence;
   a minimal ELF32 little-endian program-header parser can check the actual bytes.

The compile-only predecessor graph failure remains a failure. Its separate
successful graph prefix and new successful compile establish source/build
lineage; neither the map nor an execution capsule is a mathematical receipt.
An ordinary failed or cycle-capped snapshot can be analyzed as a labeled prefix
if it wrote complete diagnostics. Missing diagnostics after abrupt termination
mean no complete sample attribution, not a zero-cost execution.

## Exact retained linker-map grammar

The inspected format example is the old, retained
`experiments/v5-local-checks/guest-build-05/guest-link.map`, SHA-256
`9f18ef720922e6eaadcde4e8c820194ef3d39aaa5ba8a1fb55a21f0ffc8b1aeb`.
It demonstrates parsing only; its addresses must never label a new guest.

Its header is exactly:

```text
     VMA      LMA     Size Align Out     In      Symbol
```

VMA, LMA and Size are hexadecimal numbers without a required `0x`; Align is
decimal. Preserve the entire trailing text, including spaces and mangling.
In this exact format its first character is at zero-based column 33 for an
output section, 41 for an input section, and 49 for a symbol. Splitting the whole
line on whitespace would corrupt paths and Rust symbol names.

The useful record parser is:

```text
^\s*([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+([0-9]+)(\s+)(.*)$
```

Determine the trailing text's start position from the original line, then
classify it using the header's exact Out/In/Symbol columns. Track the current
output/input section so that a symbol in data is never treated as executable
code. Refuse an unsupported header or ambiguous record layout rather than
silently dropping records and claiming complete attribution. Check arithmetic
without 32-bit wraparound: `0 <= start < 2^32`, `0 <= size`, `start+size <= 2^32`.

For a positive-sized symbol row `s` with VMA `a_s` and size `n_s`, define

\[
I_s=[a_s,a_s+n_s),\qquad
A(p)=\{s:p\in I_s\text{ and }I_s\text{ is within executable user code}\}.
\]

Use VMA, not LMA. Require the symbol/input-section relation to be consistent,
and restrict candidate intervals to the exact ELF's executable ranges.
Do not infer a zero-sized symbol's extent by taking the next symbol address:
the retained map contains many `$x`, `.Lpcrel_hi*`, and zero-sized entry labels.

The retained format illustrates the distinction without a new execution:

- `memset`: `[0x200800, 0x2008f8)` from size `0xf8`.
- `memcpy`: `[0x2008f8, 0x200d04)` from size `0x40c`.
- `_start`: a zero-sized symbol at `0x200d04`, inside a positive-sized input
  section `(.text._start)` of size `0x1c`. That supports a section-only label,
  not an invented positive-sized function symbol.

For a sampled PC, the exclusive primary outcome is:

| Condition | Attribution outcome |
|---|---|
| Exactly one valid positive-sized symbol interval contains PC | Exact machine-code symbol/range. |
| Several intervals contain PC | Ambiguous; retain the full candidate set, never multiply the sample count. |
| No symbol, but a unique executable input section contains PC | Section-only label; do not silently promote it to a function. |
| PC is in user executable memory but lacks a supported range | Unknown user code. |
| PC is outside the user ELF executable ranges | Outside user executable; possibly kernel/runtime, not automatically a kernel function. |

Zero-sized labels can be attached as annotations but contribute no interval.
Equivalent aliases and LTO folding can create multiple names at one range;
retain their ambiguity. Never resolve it by choosing the first or nearest name.
The minimal helper does not need kernel symbolization. If later warranted, the
exact already-bound kernel ELF supplies a separate explicit address space/range
table; a broad numerical threshold alone is not function attribution.

## Function classes that can inform the next source decision

Keep exact raw symbol names and addresses as primary data. A small versioned
table may add coarse labels using anchored owner-namespace prefixes, not a
substring found inside a generic argument. For example, a destructor whose
type argument mentions a theorem checker remains a destructor, not a known
type-checker call. Unknown names stay unclassified.

| Anchored owner or exact runtime name | Coarse diagnostic class |
|---|---|
| `dmkn_aggregate_relation::relation::`, `::census::`, `::wire::` | Aggregate graph, input and size-census orchestration. |
| `dmkn_aggregate_relation::membership::`, `::header::` | Aggregate membership/header commitments and encoding. |
| `dmkn_module_relation::relation::` | Module orchestration; may contain inlined work from several phases. |
| `dmkn_module_relation::canonical::`, `::commitments::`, `::journal::`, `::policy::` | Canonicalization, commitments and policy/journal handling; preserve finer function names. |
| `nanoda_lib::parser::` | Native row parsing. |
| `nanoda_lib::module_correspondence::` | Canonical/native correspondence, including validation-only traversal. |
| `nanoda_lib::tc::`, `::inductive::`, `::quot::`, `::level::`, `::expr::` | Checker algorithms; owner names are not caller-inclusive costs. |
| `serde_json::`, `serde_core::` | Serialization/deserialization support. |
| `sha2::`, `risc0_zkvm::sha::` | Hashing support if these owners actually survive in the map. |
| `alloc::`, `core::`, `std::`, exact `memcpy`/`memset`/`memmove`/`memcmp` | General runtime, allocation, container or memory support. |
| `risc0_zkvm::guest::` | Guest SDK/runtime support, not proof-production work. |

The `::...` table abbreviations mean the same full crate prefix, not arbitrary
substring matches. Class labels are hypotheses for source inspection. LTO and
inlining mean that a PC inside `check_bound` can execute code originally written
in another function. Without debug inline stacks, caller attribution and
inline provenance remain unknown; do not report their absence as zero cost.

## Counts, consistency checks and honest output

Let diagnostic cells be `(w,p,c)` with integer count `c > 0`. Validate unique
cell keys, bounded u32 PCs, bounded counters, the declared stride/cell limit,
and agreement between cell sums and `samples_stored`. With no integer-counter
saturation, the callback implies

\[
S_{\mathrm{stored}}+S_{\mathrm{omitted}}
=\left\lceil\frac{N_{\mathrm{observed}}}{256}\right\rceil.
\]

For an exclusive attribution category `k`, report

\[
H_k=\sum_{(w,p,c):\operatorname{category}(p)=k}c,
\qquad f_k=H_k/S_{\mathrm{stored}},
\]

with `f_k` absent when the denominator is zero. Check that categories, including
unknown/ambiguous/outside-user, conserve all stored counts. Separately retain
the per-PC/per-window table and omissions. These are deterministic sampled
instruction fractions, not estimated CPU, guest cycles, padded rows, proof
time or full-workflow resource cost. Periodic sampling can alias a loop, even
when there are no omitted cells; do not manufacture confidence bounds.

The report should include all input hashes, executable ranges, parse counts,
zero-sized labels, interval ambiguities, unknown counts, complete/prefix status,
sample saturation and backwards-cycle flags. Sorted BTreeMap cells are not a
call stack or full execution trace. Host native preflight/receipt verification,
host-side serialization, segment custody and proof production are outside this
guest-PC histogram; their independently recorded costs remain separate.

## Minimum implementation, pending root selection

Proposed new helper: `software/v5/aggregate_host/attribute.py`, inert until
root selects exact retained inputs. It needs JSON, hashlib, struct and interval
search only; no SDK imports, Cargo, external symbolizer or guest invocation.
Bound map/ELF/diagnostic sizes and row counts before allocation. Build an interval
index once and process only distinct sampled PCs, retaining all overlaps.

First show root this principle plan. Implement only if the saved diagnostic
will change a central source decision and root confirms the small helper scope.
The single already-planned snapshot should supply both reusable execution data
and diagnostics; this plan adds no benchmark execution. An unknown/ambiguous
profile is an honest outcome, not automatic authority to rebuild or rerun.

## Source implementation checkpoint

Root adopted the source-only plan and assigned
`software/v5/aggregate_host/attribute.py`. The helper is written; independent
source review and root's exact execution selection are still required. This
author has not run the helper, a test, compiler, guest or prover.

The selected invocation is the immutable owner-job source snapshot with
`-I -S -B`, canonical working directory, followed by two arguments: absolute
selection JSON path and its exact SHA-256. The selection has this shape:

```json
{
  "schema": "DMKN_PC_ATTRIBUTION_SELECTION_V1",
  "diagnostic": {"path": "ABSOLUTE", "bytes": 1, "sha256": "EXACT"},
  "execution_result": {"path": "ABSOLUTE", "bytes": 1, "sha256": "EXACT"},
  "execution_command": {"path": "ABSOLUTE", "bytes": 1, "sha256": "EXACT"},
  "assembly_result": {"path": "ABSOLUTE", "bytes": 1, "sha256": "EXACT"},
  "assembly_command": {"path": "ABSOLUTE", "bytes": 1, "sha256": "EXACT"},
  "output": "FRESH_ABSOLUTE_CHILD_OF_SELECTED_OPERATION"
}
```

The illustrative placeholders above are not a runnable selection. Both assembly
records are pinned separately. The helper binds their adopted artifact validation
and compile-result/failure records, then checks actual ELF bytes/program headers,
actual map bytes and actual assembled image. It preserves the compile operation's
`FAIL_FINALIZATION` and `prior_budget_met:false`; artifact readoption is not a
resource-budget pass. Execution COMMAND/RESULT bind the actual diagnostic and
wire. Their outer source/host qualification is reused, not independently redone.

The algorithm sorts distinct sampled PCs and intervals, inserts each interval
once, and removes it at its exclusive endpoint with a heap. Runtime is
`O((intervals + distinct_PCs) log(intervals) + emitted_matches)` apart from
bounded ELF-segment checks, not a sample-cell-by-symbol nested scan. At most
100,000 map rows, 131,072 sample cells and 524,288 emitted candidate references
are accepted. Oversized ambiguity is refused rather than silently truncated.
Diagnostic/map input caps are 8 MiB each, total reads including final exact-file
rebinding are at most 128 MiB, and the sole JSON report is at most 64 MiB.
The outer operation still owns CPU/memory/time/process enforcement.

All retained cells are conserved in exclusive symbol, ambiguous-symbol,
section-only, ambiguous-section, unknown-user and outside-user categories.
Ambiguous symbols and sections retain their complete candidate IDs; only unique
symbol/section outcomes add to unique-range counts. Coarse namespace labels
never use substrings inside generic arguments. Zero-sized labels are separate
annotations with no invented extents. Invalid counts, duplicate JSON keys,
unrecognized map layouts, partial executable overlaps and mismatched pins refuse.

Root subsequently reported a saved, cycle-capped failed execution prefix with
sample-cell saturation (`aggregate-snapshot-01/evidence/diagnostic.json`, SHA-256
`ebd87c76cea9c321d1f64f5aee9ac5f1dc0c4aef0659c1937f0af84e4b259388`). Its ordinary
failure and omissions are preserved, not a reason to rerun/increase the guest
cap. No attribution fractions or hotspot claim have yet been computed by this
author. Particularly, saturated retained windows cannot characterize the omitted
later unseen window/PC pairs or the unexecuted remainder.

Independent source review requested two inexpensive consistency checks, now
included before source freeze: the command, diagnostic and wrapper result agree
on the guest cycle cap/segment size, and the header file equals the diagnostic's
exact 192 header bytes. Diagnostic failure requires a null result and cannot
coexist with a wrapper capsule-pass claim. Host source sets session statistics
before some finalization checks, so a failed diagnostic with statistics is
labeled a failure after execution, not falsely refused as impossible and not
promoted into acceptance. The current capped prefix has null session statistics.
The diagnostic's successful-capsule label similarly identifies only the host's
reported guest outcome, not wrapper acceptance or mathematical authority.

Source submitted for final review: 25,115 bytes, SHA-256
`0fc2ca9b35892cf86b3f8fdbf124db8cdb31f6cd20658125e2d6c23967c3a786`.
No runtime attribution result exists from this author.

## Adopted offline attribution and the next acceptance-preserving seam

Root executed the helper once after independent source/exact-selection clearance.
The resulting saved report is
`experiments/v5-local-checks/aggregate-pc-attribution-01/attribution/RESULT.json`,
SHA-256 `31b29b7a8888fbfa0337fbf3a72b3269d2facbf05513d0e27a23ac4ca91de84b`.
Root subsequently adopted its independent actual audit. The helper and its
used snapshot/evidence are now frozen. This author read that saved output only;
no attribution rerun or new guest execution was performed.

Exactly 118,429 retained samples map to unique user symbols and 13,025 lie outside
the user executable ranges. There are no ambiguous, section-only or unknown-user
outcomes in this particular report. This says nothing about the 23,898 omitted
samples. Among the exact named ranges:

| Machine-code range | Retained samples |
|---|---:|
| Serde deserializer trait implementation, `deserialize_any` | 13,496 |
| `memcpy` | 11,672 |
| `canonical_size::Census::visit` | 11,452 |
| `canonical_size::Census::string` | 10,772 |
| Serde `SliceRead` trait implementation, `parse_str` | 6,024 |
| Aggregate census `Census::charge::visit` | 3,414 |

The trait-implementation names start with encoded trait syntax, not the anchored
`serde_json::` prefix; the helper correctly leaves those coarse labels
unclassified. Therefore its `serialization` class is not the inclusive parser
cost. `memcpy` similarly gives no caller attribution. The two named canonical-size
ranges motivate inspecting this traversal, not a cycle-cost or speedup assertion.

For a retained category with count H, an exact accounting fact is that its count
among **all sampled events in this failed execution prefix** lies in
`[H, H + 23898]`, with denominator `131454 + 23898 = 155352`. These are bounds
over arbitrary missing labels, not statistical confidence bounds. They cannot
be transferred to all instructions, actual cycles, proof time or the unexecuted
remainder. Periodic sampling still aliases independently of cell saturation.

### Actual source chain and the redundant work

Read-only SHA-256 checks confirmed these currently inspected files equal the
frozen source pins of the compiled aggregate image:

| Selected source | SHA-256 |
|---|---|
| `software/v5/modules/receipt/src/canonical.rs` | `23ca5fa1bfe536db08136bef9956426e4d43e90fa36d00a1886e97eef6892d9b` |
| `software/v5/modules/receipt/src/relation.rs` | `3625bc9c7708e5a03580e1e61bc7019f5b7cf6ad48ee37f6d749919d245e2eb8` |
| `software/v5/aggregate_parse_once/census.rs` | `88e9796bbb5493187f541d40e7c777afa8bfd4059929a9a2a1f118cfae815b04` |
| `software/v5/aggregate_claims/relation.rs` | `698e0e1bfacdad37fe1720881b2034083b357a2fbeef7b233d83e2f7c1eb6a49` |

For each accepted aggregate delta, the current chain is:

```text
strict parse -> canonical_size -> aggregate tree census
             -> relation::check(Value) -> canonical_size -> check_bound(Value)
```

Parsing is already once, and native correspondence already has validation-only
traversal. Neither existing optimization is being reimplemented. The remaining
issue is that returning an ordinary mutable `Value` discards evidence of its
whole-input validation, so the public relation entry correctly validates again.
Removing that second check without replacing this lost invariant would be an
unsafe API shortcut.

### One opaque token, not a caller-supplied validation claim

The proposed token has an owned private value and exact structural metadata:

```text
ValidatedValue { private value, private node_count, private maximum_depth }
```

The name refers only to **JSON syntax/resource validation**. It is not evidence
of theorem correctness, receipt integrity or mathematical admission.

Its invariant is:

1. The owned value came from the existing strict complete byte parser, including
   duplicate-key rejection, unsigned-u64-only numbers, complete-input consumption
   and the unchanged parser nesting behavior.
2. The same value satisfies the current canonical byte, node and depth domain.
3. `node_count` equals the recursive count of `Value` nodes, excluding object
   keys, and `maximum_depth` equals the greatest value depth with root depth zero.
4. No caller has had mutable access since that invariant was established.

The minimal safe API should have a public parser returning this token and public
read-only access to `&Value` and structural counts. There must be no public
fields/constructor, `From<Value>`, `Deserialize`, mutable dereference, mutable
callback, replace operation or sender-supplied statistics. Do not derive `Clone`
unnecessarily. Moving the owned value out is crate-private, and the public
`relation::check_validated(token)` consumes the token before calling the unchanged
private `check_bound` function. Aggregate census may borrow it read-only and
return the same token; it cannot mint or mutate one. No cryptography or global
trusted cache is needed for this process-local ownership invariant.

Keep the existing public `relation::check(Value)` as a fully checked arbitrary-
value entry. It must not become an unchecked path. Existing `parse_validated`
callers that require a `Value` can remain compatible through an explicit checked
wrapper; avoid changing all unrelated callers or hashes. External unsafe Rust
can violate memory safety, but peer input cannot directly call private Rust
constructors; this is an API correctness argument under the existing trusted
compiled-program assumption, not a sandbox against injected native code.

### Stronger selected design: reuse structure counts too

Root is separately analyzing the lexical length lemma
`len(canonical(parse_syntax(b))) <= len(b)` for the selected strict JSON profile.
This checkpoint neither substitutes for that proof nor assumes it holds for
arbitrary caller-created `Value`s. Conditional on that lemma and unchanged strict
parsing, the existing 16 MiB raw-input bound already enforces the canonical byte
bound. A single cheap node/depth traversal can then mint the token without either
canonical-size string scan.

Aggregate census can update its cumulative node count with checked addition of
the token's exact node count, and its maximum depth with the exact maximum.
For finite trees this is equivalent to its current per-node traversal:

```text
old_nodes + node_count(value) <= MAX_AGGREGATE_NODES
maximum_depth(value) <= MAX_AGGREGATE_DEPTH
```

The remaining rows/bodies/parent/opening checks still read the exact same value
fields with unchanged object/array alternatives and limits. They are not dropped
or replaced by sender metadata. The current module-bound defaults, aggregate
bounds, graph/target checks, exact hashes, native correspondence/kernel checking,
parent obligations and receipt discharge are unchanged.

On accepted inputs, this preserves the entire `check_bound` input and output.
On rejected inputs, aggregate `charge` may discover a structural limit at a
different point. Its mutable counters are local to `check_reader`; every charge
failure propagates before a conclusion is returned, with no retry/recovery or
publication of those counters. Thus rejection remains rejection. Exact error
ordering and failed-prefix resource consumption are not claimed identical and
must be described if this optimization is selected. Do not export reusable
partially charged tokens/census state after failure.

### Acceptance proof and predicted operation reduction

Let P be the unchanged strict parser, V the current canonical-domain predicate,
C the current aggregate census, and K the unchanged `check_bound`. For an input
frame b, the old successful path is

```text
v = P(b); V(v); C(v); V(v); K(v).
```

The token constructor establishes `v = P(b)` and V(v), and ownership preserves
that value during C. Consequently the second V succeeds identically and can be
removed. If root's lexical lemma discharges the byte part of V, and the token
stores the exact node/depth census, the stronger path is

```text
token = strict_parse_and_structural_validate(b)
C_using_exact_token_counts(token.readonly_value, token.counts)
K(token.consume_owned_value()).
```

Equivalence of the census follows from finite-tree node-count addition and depth
maximum; equivalence of K follows from unchanged owned input bytes/values and
unchanged code. Receipt/guest obligations remain outside this syntactic argument
and must still be discharged exactly. The lexical lemma is a separate required
premise, not an unproved optimization flag.

For a successfully processed frame with N value nodes and S decoded UTF-8 bytes
in all string values and object keys, the old post-parse path makes three whole-
tree visits (two canonical-size traversals plus aggregate census) and scans the
S string bytes twice for canonical lengths. The stronger token path makes one
structural traversal and no canonical-length string scan. Therefore it removes
exactly 2N such node visits and 2S byte-classification iterations, plus the two
canonical-size decimal-digit loops and related byte-budget operations. It does
not remove parsing, allocation, byte reading, canonical hashing/serialization of
actual commitments, input extraction or mathematics checking. Overall input
processing remains linear; this is a concrete operation reduction, not an
asymptotic or measured whole-proof speedup. The failed prefix cannot predict the
full-run constant or whether the same execution cap would suffice.

The simpler fallback, if the lexical lemma fails, is the same opaque token
minted using existing strict parse plus `canonical_size`, removing only the
second traversal. Root has not selected a second-pass-only build: establishing
the stronger lemma first avoids an unnecessary intermediate guest rebuild.
No implementation, build, new execution or cap increase is authorized by this
source-analysis note.
