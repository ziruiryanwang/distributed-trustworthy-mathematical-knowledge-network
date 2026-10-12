# After bounded-parse: choose the next investment

2026-10-12. Source/retained-data decision memo only. No new implementation,
runtime, proof allocation or Git operation. This supplements, rather than
repeats, `COMPACT-WITNESS-FEASIBILITY.md` and `BOUNDED-PARSE-DECISION.md`.

## What the latest failure establishes

The adopted image `173255698c2bc9030e7528297b627c59d6d35a605ec3a16542b2ba73e5107ac2`
still failed its selected 2^25-cycle screen. Diagnostic SHA-256
`dca409e07e44f7647c2b248167cadcba6f5ad0827af83a3aa3173e0aee0bda72`
reports session-limit refusal and no complete accepted capsule. No proof stage
is justified from those partial segments. The failure gives neither full-run
cost nor remaining work; it is not evidence that doubling the cap will finish.

The current source has already removed duplicate canonical-size scans and
reused immutable structural counts. It already moves large input fields, and
the selected checker wrapper is `modules/native/proof_validation/lib.rs`, not
the older checker lib: local theorem syntax validation without materializing a
discarded proof tree is already implemented. Do not count these as new options.

The base lane is performing **one exact-current-image offline attribution**.
Reuse it; do not map the new PCs through the old ELF or run a second profiler.
The saved samples are saturated and cover only a failed prefix. The diagnostic
contains 131,614 stored and 22,960 omitted sample events; cumulative maximum
trace-cycle labels are not a denominator for the selected session-cycle cap.
Category counts can direct inspection, not establish causal or whole-run shares.

## Three choices, with their actual boundaries

| Choice | Work it can remove | Work it cannot remove | Main implementation cost |
|---|---|---|---|
| Lossless compact encoding into the existing Value algebra | JSON punctuation, escape and decimal-input parsing; some witness transport bytes | Value allocation/maps, most schema traversal, canonical semantic hashing, row correspondence/DAG construction, new mathematical checking, receipt verification | New decoder/bounds and wire version; native and guest integration; new guest image and compatible snapshot/stage hosts |
| One localized redundant-representation/commitment seam | Proven unnecessary copying, rebuilding or re-encoding of the **same authenticated immutable value** | Required checking of new proofs, required transparent semantics, reading new material, exact commitments not already established | Focused equality/invariant argument and source change; new image if guest source changes, with native correspondence preserved |
| Deliberately larger execution envelope | Nothing: buys completion information and potentially a reusable complete capsule | All existing guest/prover work; no efficiency or growth advantage by itself | Explicit joint cycle/segment/memory/storage/proof-cost decision, new fresh execution; no automatic renewal |

All three preserve certificate-based receiver independence from ancestral proof
replay **if** the accepted relation and recursive assumptions remain sound. They
change the producer's acquisition/certification cost, not the semantic search
guarantee. Lower producer cost improves the full-cost benefit region and service
capacity; a successful longer run alone does not establish either improvement.

## Compact transport is not just a decoder patch

Use the existing feasibility note's narrow round-trip target:
`decode(encode(V)) = V`, then unchanged mathematical acceptance of V and exact
canonical commitment bytes. Keep module semantic IDs and member Js unchanged;
aggregate H can retain the current **v2** layout/meaning, but its adopted image
slot changes to A'. No proof/header patching is allowed.

Two concrete prices must enter the decision:

1. The current `BoundedValue` raw-JSON length lemma does not apply to compact
   bytes. The decoder must establish the old canonical-JSON expansion envelope,
   global node/child-slot and depth limits, strict integer/string/map rules and
   exact EOF. Cheap-looking binary input can expand. Computing canonical lengths
   may reintroduce string classification and decimal-length work removed by
   bounded-parse; its net saving is not the entire old JSON parser cost.
2. The retained snapshot and proposed stage host call native aggregate
   `check_bytes` bound to the current v2 JSON-bearing wire. A new guest decoder
   alone is unusable through that path. The source must provide unambiguous
   version dispatch/new wire, matching native module/aggregate libraries, an
   encoder, compatible snapshot/stage host links and image/session bindings.
   A dual-representation shortcut would instead need a new rigorous binding
   argument; it is not free. The unchanged checker/backend can still be reused,
   but these native-library/host boundaries cannot simply be omitted.

Select this option only if exact-current evidence points to substantial lexical
input work that survives bounded-parse, and a source-based operation comparison
supports a net reduction after bounds. It will not solve a dominant checker or
canonical commitment bottleneck. Keep the initial representation lossless; a
typed arena, dictionary/backreference scheme or altered semantic hash is a
different, substantially larger change.

## What a smaller source seam would have to demonstrate

The current source still shows potentially avoidable work, but its magnitude is
unestablished. Examples for **inspection, not an implementation queue**:

- `module_relation::check_bound` clones selected group descriptors into bindings;
  correspondence clones used body openings into `body_hash_obligations`, while
  this relation consumes only that returned vector's length after checking each
  original body hash. Borrowing or a validated-count result could remove copies
  only if the same used-body set, exact comparisons and resource refusals remain.
- Commitment routines construct temporary `json!` Values, serialize canonical
  bytes, then copy those bytes into a second domain-framed buffer. Removing one
  copy can preserve the hash exactly. Replacing this with incremental hashing
  must retain the byte-length prefix, identical canonical bytes and bounds; a
  new counting pass or many tiny accelerated calls can erase the benefit.
- Foundation rows, imports and native DAGs are reconstructed per delta. A
  within-operation cache might save repeated work, but it must bind full immutable
  content, foundation/policy, owner/universe context and validated role. Caching
  by a short name or sender-claimed hash, or skipping a new local proof, is not
  an acceptable optimization. This is a larger seam than a removed copy.

Inspect the **selected** proof-validation wrapper/source map, not an older
source with similar function names. The retained group/body and row/native
representations serve different authenticity/correspondence obligations; two
passes are not redundant merely because both traverse expressions. A useful
candidate supplies an explicit equality/invariant and an exact removed-operation
count on the retained mathematical input. It must not rely on a borrowed theorem
being true without its certified premise or on opaque proofs being unfolded.

Prefer one such localized seam over compact transport if it addresses the
current hot path with substantially fewer changed trust/interop boundaries.
Do not collect many speculative micro-optimizations or redo the three seams
already adopted above. Unmapped allocator/memcpy samples alone do not identify
which Value construction is responsible; caller overlap and inlining matter.

## A higher cap needs more than a larger number

The failed current diagnostic already retains **128 segments**. Both the
snapshot custodian and staged host cap their segment vectors at 128; the
snapshot also caps the sum of retained serialized segments at 64 MiB. Raising
cycles alone with po2=18 cannot authorize a 129th segment. A larger-envelope
choice must jointly review at least:

- execution cap, po2 (supported 12..20), actual segment-count bound and final
  capsule size, not only elapsed runtime;
- larger proving-unit memory/CPU when po2 rises; fewer larger segments are not
  free, and no cost follows by linearly scaling this failed prefix;
- all segment proofs required by finish, complete capsule/parent/checkpoint
  reads within 512 MiB, and the full 3s+m stage graph/retention budget;
- one explicit terminal decision on another refusal, without an automatic
  cap ladder, unchanged retry or disposal of failed costs.

Changing cycle/po2 parameters need not change A if the same guest is used, but
it changes the host session binding and capsule. These partial segment files
are not an execution-resume API. A fresh successful run would be an information/
integration investment and could enable the existing genuine-A producer path;
it would not retrospectively pass the original efficiency gate.

## Recommended decision rule

Finish the exact-current offline attribution first, while pricing these three
bounded options from source. Then make **one** root decision:

1. If a clearly localized removable representation cost is supported, select
   that equality-preserving seam and its changed-boundary checks.
2. If lexical JSON work is the consequential remaining target and the expanded
   bounds/native-host migration still justify it, select the compact Value
   transport work as one coherent native/guest change, not guest-only work.
3. If neither small change has a defensible benefit argument, choose explicitly
   between a joint higher-envelope completion investment and holding proof
   funding pending a deeper representation decision. Do not silently convert
   absence of a cheap optimization into permission for another execution.

Do not force another image change merely to preserve the same failed cap, and
do not claim all options have been exhausted from symbol samples. The next
selection should minimize uncertainty about completing a genuinely reusable
certificate at justified total cost. None selects new experiments by this memo.
