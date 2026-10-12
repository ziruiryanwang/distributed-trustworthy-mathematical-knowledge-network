# From an aggregate execution capsule to a real reusable receipt

**Later source selection:** root adopts this seam in principle and authorizes only
fresh `software/v5/aggregate_production/stage_host.rs` and `API.md`. No Python
producer, build, guest, proof, runtime or Git operation is selected. The earlier
proposal below remains the design basis; no successful A capsule is presumed.

### Pre-implementation deserializer assessment

Inspected the retained host's bincode1.3.3 `de/mod.rs` and `de/read.rs`,
serde_core1.0.228 `de/impls.rs` and `private/size_hint.rs`, and actual SDK Segment
definition before writing the new host. Bincode's `with_limit` charges decoded
bytes, **not total heap allocation**. General sequence/map lengths become size
hints; serde's normal Vec cautious preallocation caps one initial reservation
at1MiB, not all nested allocations or retained object overhead. Slice-backed byte/
string decoding checks the requested byte slice before copying, but arbitrary
nested SDK records still do not have a proven global allocation bound here.

The fresh host will add preallocation count bounds for the capsule's outer
assumption and segment vectors through custom deserialize visitors, preserving
their existing serialization layout. Its own checkpoint envelope will check fixed
fields, kind length and exact payload extent before copying/deserializing payload.
Selected SDK receipt/segment/claim internals remain decoded by the pinned library;
the64MiB file/encoded-byte limits do not prove a64MiB heap bound. The enclosing
owner must enforce finite process memory/CPU/wall limits and treat exhaustion,
panic, malformed data or failed cleanup as nonacceptance. That resource Job is
not a hostile-code sandbox. No SDK replacement or broad decoder rewrite is
selected; this residual must remain in the API/support statement.

2026-10-12. Source-only feasibility and proposed implementation seam. Root owns
source selection, builds, actual capsule adoption, proof funding and execution.
This note selects none of them. No base proof is restarted, SDK tree rehashed,
guest reexecuted, or source outside this checkpoint changed. Existing artifacts
and failures remain preserved. A successful aggregate capsule is a prerequisite
for later production, not an artifact presumed to exist by this document.

### Source implementation checkpoint

The authorized fresh `software/v5/aggregate_production/stage_host.rs` and `API.md`
now exist. This is source implementation only: no compilation, control execution,
guest execution, proof or successful A capsule has been established. The existing
module producer and aggregate snapshot host remain byte-for-byte outside this
assignment; there is still no aggregate Python producer or build adapter.

The host preserves the exact `DMKNAS01` capsule ABI and S/B binding domains,
performs actual conditional-relation preflight and full typed I/A parent receipt
verification, and reuses the pinned SDK segment/lift/join/resolve operations.
Each outer capsule count is rejected before allocation when excessive. Dedicated
`DMKNAP01` checkpoints check fixed framing and exact payload extent before copy;
their actual SDK payloads are verified, not trusted as saved status. Finish checks
all segment receipts as a complete composite with actual assumptions, compares
the composite and final succinct claims to exact `ReceiptClaim::ok(A,H)`, and
fully verifies the serialized application receipt before fresh output. The exact
existing six-field aggregate `verify` JSON contract is retained.

The self-review compared these operations against the existing two host sources
and actual retained SDK signatures. It does not replace compilation or an
independent source review. Nested SDK allocation/depth residuals above remain;
the enclosing owner must meter every call and reject unclean completion. Existing
I receipt bytes remain reusable premises; no old proof production is repeated.

Independent review requested one accounting clarification: the SDK's
`prove_segment` performs segment preflight/witness reconstruction. The host's
`guest_execute_calls=0` means no new whole-session ExecutorImpl acquisition,
not zero segment computation. API and source comments now say so; stage logic,
wire/capsule/report schemas and full-cost charging are unchanged.

## Decision

Implement a **fresh aggregate stage host and narrowly adapted producer**, reusing
the retained SDK's existing segment/lift/join/resolve operations and the successful
I-production controller's resource/accounting structure. Do not teach the old
module host to treat a 192-byte aggregate header as its 184-byte module journal.
Do not create a new mathematical guest just to add host-side staged proving.

The critical new boundary is real recursive assumption resolution. The base I
production had zero assumptions. The aggregate fixture has a genuine I frontier;
its receipt may be reused, but its mathematical premise must actually be resolved
inside the final succinct proof. Native checking, a successful execution report,
a capsule hash and a completed join do not accomplish that resolution.

The minimum decisive capability endpoint is one real final A receipt, accepted
through the existing exact aggregate receiver and bound to one selected member.
This is sealer operability, not an economic-benefit claim or final v5 release.
The separate [investment decision](NEXT-AGGREGATE-COST-DECISION.md) remains in force.

## The existing reusable pieces and the incompatible ones

Paths in this note are relative to the sole canonical project root.

| Actual source | Reusable part | Aggregate-specific boundary required |
|---|---|---|
| `software/v5/aggregate_host/aggregate_host.rs` | Actual A/ELF binding, exact native preflight, typed receipt verification, complete capsule definition/bindings, hardened fresh ordinary-path helpers | It currently offers only `snapshot` and `verify`; it does not prove stages |
| `software/v5/aggregate/receipt.rs` | Full non-dev succinct-Poseidon2 I/A application verification and exact H binding | Preserve independently adopted A; do not substitute I or permit arbitrary images |
| `software/v5/modules/receipt/src/bin/module_host.rs` | `take_segment`, `take_succinct`, `prefix_key`, supported SDK stage operations and final composite cross-check | Its module input parser, application validator, 184-byte limit and module binding domains are wrong for A |
| `software/v5/production/producer.py` | Deterministic dependency graph, missing-prefix reuse, per-stage reservations, clean closure checks, prior-attempt accounting, fresh output, first-failure stop | Profile/request/report schemas, expected-journal validation, capsule schema, stage argv/checkpoint envelope and finish marker are I-specific |
| Actual retained cryptographic SDK | The same `Segment`, `SegmentReceipt`, `SuccinctReceipt`, `ReceiptClaim`, `CompositeReceipt`, prover/verification APIs | Exact source/dependency feature and serialization compatibility must stay bound; no backend rebuild or new proof system is implied |

The old producer literally checks `DMKNM002`, expected length 184, capsule's
first u32 = 3 and schema-5 checkpoint offsets; its finish parser reads module
rank/group-count fields. It therefore must reject aggregate inputs unchanged.
The old stage host likewise cannot be invoked with a relabeled A header.

## Exact successful-capsule contract

The current aggregate snapshot serializes the following fields, in this order,
using fixed-integer bounded bincode and the pinned SDK types:

    AggregateSnapshot {
      magic: [u8; 8] = "DMKNAS01",
      version: u32 = 1,
      session_binding: Digest,
      session_claim: ReceiptClaim,
      assumption_order: Vec<Digest>,
      segments: Vec<Segment>
    }

Its exact bindings are:

    S = Hash(encode(("DMKN-AGGREGATE-SESSION-V1",
        Hash(ELF), A, I, foundation, policy,
        Hash(wire), Hash(H), cycles, po2, ordered_receipt_byte_hashes)))

    B = Hash(encode(("DMKN-AGGREGATE-SNAPSHOT-V1", S, Hash(capsule_bytes))))

H is exactly the selected 192-byte `DMKNA002`/version-2 header. A stage reader
must decode these existing formats **exactly**, reject trailing bytes, recompute
S and B, and require the capsule's target claim digest to equal
`ReceiptClaim::ok(A, exact H bytes).digest()`. It must enforce nonempty consecutive
segments, s <= 128, each segment's po2 <= selected po2, m <= 8, and exact count/
membership of the verified assumption order. File, total-read, memory, wall and
output limits remain additional obligations; a bounded file is not by itself a
proof that arbitrary deserializer length hints cannot allocate excessive memory.

The snapshot host already verifies:

- `compute_image_id(ELF) == independently adopted A`;
- actual aggregate native relation derives exactly H and the pending claims;
- one exact genuine receipt for every pending `(image, journal)` claim, in the
  relation's returned order, with no duplicate/unused claim;
- successful halted guest and exact H, no unsupported MMR/PoVW or queued Keccak;
- the actual assumption set/order corresponds exactly to the preverified parents,
  each using the selected Poseidon2 suite and default zero assumption control root;
- complete `session.segments()` materialization, not just callback-prefix files.

For the smallest new stage host, reuse that deterministic preflight and typed
parent verification before consuming a capsule. This repeats bounded native
preflight/parent verification across separate stage processes, **not** guest
execution or base proof production. Include that overhead in the quote; do not
credit repeated native checking as new mathematical evidence. If it later becomes
consequential, a bind-only stage preflight is a separate source/security argument,
not permission to trust a saved native success flag.

The complete capsule and its accepted operational evidence must be adopted by
the owner before funding. A structurally parseable capsule is still untrusted
proving material: an attacker can rewrite a capsule and its unkeyed checksums.
Those bindings prevent unnoticed substitution relative to the owner's selected
bytes; final mathematical authority still comes only from real cryptographic
verification under independently adopted A and exact H.

## Why a successful capsule still needs resolve stages

This point follows from the retained SDK source, not from an inference about
names in a JSON report. The inspected SDK is the retained checkout
`risc0-3bbcd44d6459b9ef6ac0df3846dc9215514934e8` below
`experiments/general-checker-host-05/build-01/source/`.

- `risc0/zkvm/src/host/server/session.rs::Session::claim` constructs session output
  using **unresolved** assumptions. With supplied proven parents, its target claim
  can already equal `ReceiptClaim::ok(A,H)`.
- `Session::segments` merges the actual journal and **all actual assumptions**
  into the final execution segment's output. Its cryptographic segment proof
  still carries these obligations.
- `risc0/zkvm/src/receipt/composite.rs::verify_integrity_with_context` checks every
  segment's integrity and continuation, then requires exactly one supplied proof
  per assumption in order and verifies matching claim digests. Its `claim()`
  removes those assumptions only on the convention that verification discharged
  them. Calling `claim()` without the preceding successful verification is not
  a valid discharge.
- `host/server/prove/prover_impl.rs` exposes the already used `lift`, `join` and
  `resolve` operations and verifies the returned recursion receipts.

Thus `session_claim` is the exact final **target**, not evidence that the needed
cryptographic resolve calls have already run. A staged implementation that stops
at a joined conditional proof would not supply the intended application receipt.

## Proposed minimum source and API scope

These are prospective fresh paths, not an authorization to create them now:

1. `software/v5/aggregate_production/stage_host.rs`: a thin new executable with
   `stage` and the unchanged aggregate `verify` result contract. Reuse exact
   `aggregate/receipt.rs`, the selected aggregate relation and the retained SDK;
   reproduce the existing aggregate capsule field order without editing the used
   snapshot host. No `snapshot`, `execute`, arbitrary verifier callback or alternate
   backend command belongs to this staged executable.
2. `software/v5/aggregate_production/producer.py` and `__init__.py`: fresh narrowly
   adapted controller with aggregate-specific exact schemas. Preserve the old
   graph/missing-plan, per-call accounting and recovery refusal rules. Compare
   unchanged blocks against the predecessor; do not refactor frozen production.
3. One concise `API.md` and independent small stage-envelope/controller controls.
   Root separately owns any exact link recipe, finite qualification adapter and
   input/resource selection. Build only the new host against the already adopted
   native relation/SDK artifacts; adding host commands need not change guest A.

Suggested stage CLI:

    stage ADOPTED_A ELF WIRE EXPECTED_HEADER CYCLES PO2
          KIND INDEX FRESH_OUTPUT RECEIPT_COUNT [RECEIPTS...]
          CAPSULE [REQUIRED_CHECKPOINTS...]

Only `segment`, `lift`, `join`, `resolve`, `finish` are permitted. The independently
adopted A is explicit; the ELF must match it. Header and parent decoders retain the
currently selected one-A profile. Cross-image compatibility remains a separate
later selection; this seam does not silently relax `verify_pending`.

The new producer's immutable session identity must bind actual A, fixed I/foundation/
policy, exact ELF/wire/H/capsule pins, S/B, cycles, po2, actual s/m and the ordered
exact receipt-byte pins. Parent order is significant in S even when the actual
execution uses a different assumption order. Keep both orders distinct. Profile
identity binds the exact stage host, controller/supervisor and relevant runtime
pins. Old module requests, profiles, attempt reports and checkpoints refuse.

Use an explicitly domain-separated aggregate checkpoint envelope. One minimal
proposed shape is fixed-integer bincode:

    (magic[8] = "DMKNAP01", version:u32 = 1,
     capsule_binding:Digest, kind:String, index:u32, proof_payload:Vec<u8>)

The payload remains the same supported SDK segment/succinct receipt type. The
new framing merely gives early cross-lane refusal and exact bounded parsing; it
does not certify a payload. Validate each consumed checkpoint cryptographically,
under exact supported verifier parameters, with no duplicate or unused key.
The unkeyed B field binds capsule bytes, not host/controller source-profile
identity. Rewriting framing supplies no authority. Selection of exact production
profiles and permission to reuse compatible checkpoints are owner/controller
obligations, separate from final exact A/H mathematical verification.
The controller's header parser and markers must change coherently with this
envelope. Do not reuse schema-5 numeric offsets or infer compatibility from a
shared string such as `join`.

A structured stage report should identify schema, kind/index, B, A, exact H hash,
s/m, exact output bytes/hash and whether it is a checkpoint or a final receipt.
Only a clean supervised same-call host result binds these operational fields.
Saved reports remain non-authoritative; the producer emits receipt artifacts,
not the receiver's private mathematical handles.

## Stage graph and required checks

For actual capsule segment count s >= 1 and actual assumption count m >= 0:

| Stage | Exact dependencies | Required cryptographic/result checks |
|---|---|---|
| `segment:i`, 0 <= i < s | Selected complete capsule only | `prove_segment(ctx, segments[i])`; exact index/hash suite; integrity and exact selected segment-verifier parameters |
| `lift:i` | `segment:i` only | Verify segment; `lift`; verify result; output claim digest equals input segment claim digest |
| `join:i`, 1 <= i < s | Prefix through i-1 and `lift:i` | Verify both; supported `join`; verify result; preserve SDK continuation/claim composition checks |
| `resolve:j`, 0 <= j < m | Full joined prefix if j=0, otherwise `resolve:j-1`; actual verified assumption j | Verify prior; use exact receipt selected by capsule claim-digest order; supported `resolve`; verify result |
| `finish:0` | All s segment checkpoints plus last resolve, or joined prefix when m=0 | Verify full segment composite with all actual assumptions; verify final succinct claim; exact final application verification |

For s=1 the prefix is `lift:0`; otherwise the old left-prefix sequence ends in
`join:s-1`. For each assumption, map the already fully verified I/A receipt's
claim digest to its intact succinct proof, then perform the SDK's `into_unknown()`
claim-type erasure. Assert unchanged digest and retain seal, suite and verifier
parameter fields. This operation is not conversion to a different mathematical
statement. Require a bijection between exact verified parent claims and the
capsule order: no missing, extra, repeated or ambiguous claim. Receipt-byte hashes
bind selection; they are not substitutes for claim digests.

The full fresh graph has

    s + s + (s - 1) + m + 1 = 3s + m

stage calls, at most 392 under the current bounds. There are at most 391
non-final checkpoints. The controller can retain completed exact checkpoints
and run only the missing graph suffix/dependencies under an explicitly funded
continuation. An old final prefix may allow intermediate lifts/joins to be skipped,
but finish still needs the complete segment vector. Never reexecute the guest to
recreate already retained successful capsule data or rerun the base I proof.

Independent segment/lift branches can in principle be scheduled concurrently.
The minimal successor should preserve the known sequential controller first;
parallelism needs an explicit shared CPU/memory/output allowance and dependency
scheduler, not one full-machine budget per child. It is not required to close
the execution-to-receipt boundary.

### Finalization is the authority boundary

Preserve the predecessor's deliberately redundant final check:

1. Consume every segment proof and verify the exact supported parameter profile.
2. Construct the SDK `CompositeReceipt` with those ordered segments and exact
   ordered real assumptions. Its retained non-exhaustive struct has no public
   constructor; the predecessor's fixed serde tuple is `(segments,
   assumption_receipts, verifier_parameters)`. If reused, require exact pinned
   SDK field layout and encode/decode round trip, then actual composite verification.
3. Require the verified composite claim digest to equal both capsule target claim
   and `ReceiptClaim::ok(A,H)`. Require the final succinct claim digest to equal
   that same value. This catches incomplete/extra resolution and wrong execution.
4. Construct `Receipt::new(InnerReceipt::Succinct(final), exact H)`, serialize its
   actual bytes and call the existing full `receipt::verify_aggregate(raw,H,A)`.
   Keep non-dev mode and exact succinct-Poseidon2 restriction. Integrity-only
   verification is insufficient. Require exact journal equality and header A
   binding before durable fresh output and the successful final marker.
5. A receiving consumer subsequently uses `AggregateReceiptVerifier.receive`
   under its own finite owner profile; exact member selection uses the existing
   membership path. Do not hand it a producer report in place of receipt bytes.

Under the existing cryptographic and checker assumptions, the final step proves
the selected aggregate guest's exact successful H claim with all assumptions
resolved. The already specified aggregate relation then supplies member validity.
Host/checkpoint correctness supports reliable production and accounting; it does
not create an additional unchecked mathematical import mechanism.

## Compatibility and assurance obligations before implementation adoption

- **Capsule ABI:** exact magic/version, field order, bincode options, SDK types/
  features and both aggregate binding domains. Same logical Rust field names do
  not establish binary compatibility across different SDK builds.
- **Guest/host relation match:** exact selected relation source or independently
  justified equivalence; host-native preflight must derive the same H and exact
  pending typed claims as the guest. Wrong A/header/policy refuses before funding.
- **Assumptions:** preserve actual capsule order and full parent application
  verification; no I-receipt-to-A relabeling or integrity-only parent admission.
  The source code's generic `resolve` branch is reusable, but zero-parent base
  production did not experimentally qualify this new I-to-A resolution path.
- **Final claim:** compare against independently selected A/H, never the capsule's
  own claim alone. No stage marker or raw capsule digest grants receiver authority.
- **Domain separation:** new control schemas and checkpoint framing reject old I
  material; retain all existing I artifacts and used source bytes unchanged.
- **Unsupported work:** no dev mode, proof of guest errors, external proving
  service, MMR/PoVW or coprocessor work is introduced. The staged host consumes
  the supported capsule profile, not an arbitrary SDK session.
- **Finite operation safety:** per-stage and whole-operation CPU/wall/memory,
  aggregate reads, output/entry reservation, ordinary fresh paths, input rebind,
  failure override and clean closure remain enforced. These are resource guards,
  not hostile-source isolation or a proof that every allowed shape can finish.

## A finite cost quote, not a blanket production allocation

For each still-missing stage t, record an explicit worker CPU cap c_t, wall cap
q_t, memory cap r_t and output reservation o_t. Also reserve controller work,
pinning/native preflight/parent rechecks, final receipt verification/report tails
and retained storage. With no existing A checkpoints, worker attempt allowance
must cover the selected subset of the 3s+m stage graph, not an imagined average:

    C_worker,cap = sum_selected_segment c_t
                 + sum_selected_lift c_t
                 + sum_selected_join c_t
                 + sum_selected_resolve c_t
                 + selected_finish_cap.

A uniform full-graph quote would have form

    s*c_segment + s*c_lift + (s-1)*c_join + m*c_resolve + c_finish.

These are finite **attempt ceilings**, not guaranteed successful-production costs.
Use the actual complete capsule's s, po2 distribution and m. I-production's
observed 1500/300 segment, 250/120 lift/join and 30/120 finish CPU/wall selections
are historical references, not inherited authority. The generic controller's
larger format ceilings likewise authorize no allocation. In particular m real
resolve calls are nonzero work; the base's m=0 total supplies no measured resolve
price. A source-reviewed finite qualification may fund that boundary for its
information value without claiming a profitable seal.

Quote separately:

- Actual prior capsule/build/failure and carried checkpoint costs, with scope;
- the proposed finite subset and remaining graph, including exact dependencies;
- this attempt's worker reservations, disjoint controller allowance and tails;
- per-process peak memory plus the enclosing concurrency budget;
- total retained checkpoint/receipt/log bytes and entries, and finish's read set;
- actual cold final receiving/member-binding cost, if a receiving gate is selected.

Individual 64 MiB file limits do not imply all 128 segment proofs plus the capsule,
parents and final proof fit the 512 MiB host read envelope or the controller's
aggregate output budget. Check those actual/set upper bounds before each stage,
especially finish. Do not silently enlarge caps to make a selected shape finish.
Reserve final reporting/closure work rather than repeating the earlier pattern
where successful computation was followed by failed resource finalization.

Retain first-failure stop and unknown-closure conservative reservations. No
automatic retry, allowance reset or discarded failure. A later explicit
continuation may use exact valid checkpoints without repeating them, while
carrying the old charges and actual failure disposition. The I receipt is reused
as a genuine premise. Unmodified old proving checkpoints refuse in the new
envelope. Renaming files or rewriting their unkeyed bindings cannot establish
a final A application claim; valid payload reuse, if ever appropriate, still
requires explicit owner selection and all final cryptographic checks.

## Decisive minimal negatives and qualification order

Source/control preparation can happen before a successful A capsule, but actual
production cannot. Prefer cheap structural/controller negatives first:

1. Reject old module capsule/schema3, wrong aggregate magic/version, trailing data,
   changed S/B, wrong H length or A, altered wire/ELF/parent-byte pins.
2. Reject missing/extra/duplicate typed parents, wrong exact journal and malformed
   assumption order; a genuine I receipt must never be accepted as an A receipt.
3. Reject duplicate/unused/wrong-kind/wrong-index checkpoints, an unchanged
   checkpoint with another capsule binding, truncated or forged payload and
   altered verifier parameters. Separately, the owner/controller rejects an
   unselected source profile. Envelopes are rewritable and do not authenticate
   either provenance or payload; actual payload and final A/H checks matter.
4. Reject a final joined proof with a remaining assumption, a wrong resolve order,
   a missing resolution, a non-contiguous segment vector, an incorrect final image
   or journal, fake/dev-mode and unsupported receipt forms.
5. Refuse stage selection without all exact dependencies and remaining total
   resource reservation; refuse continuation that drops prior costs or successful
   checkpoints. Retain clean failure evidence and all used sources.

Small synthetic controls establish controller/format transitions, not genuine
resolution soundness. The eventual positive gate must use the actual adopted
capsule and existing genuine I receipt, run the missing real graph under a
separately reviewed finite allowance, finish with full A verification, then
exercise actual same-call public receiver/member admission. Derive negative
verification cases from those retained artifacts where possible; do not produce
an unrelated second proof merely to exercise refusal paths.

No broader network campaign, new mathematical workload, compact witness migration,
image-upgrade mechanism or full SDK rebuild is needed to expose this seam. It
prepares the central missing production capability while preserving the stronger
ordinary-library economic comparator and the full deployable-v5 destination.

## Exact one-link feasibility and proposed finite build (2026-10-12)

Receipt/source-loop review: **a single fresh rustc link is feasible in principle**.
No adapter has been implemented or runtime selected by this note. Compile success
is still required. The stage host needs only the already retained SDK libraries,
the unchanged aggregate-host01 native relation libraries, and two direct Rust sources.
It does not require Cargo, backend/checker/relation rebuilds, a guest ELF or a
successful execution capsule merely to compile.

### Exact source and command delta

The two compiler-read project source files are:

| Source | Bytes | SHA-256 |
|---|---:|---|
|software/v5/aggregate_production/stage_host.rs|22515|5865e6afb30bd81adb79d6fe04e09ac8bb7238b40956284fa3bcd2d4da4fe102|
|software/v5/aggregate/receipt.rs|3631|41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254|

The sole path module is `../aggregate/receipt.rs`; there are no additional
project include files. If root selects a fresh `aggregate_production/build.py`
adapter, its exact source snapshot would contain **three files**: these two
Rust files and that new adapter. API.md is not a compiler input. The later
comments-only source/API clarification about segment witness reconstruction
does not change this closure or require a dependency rebuild.

Use the exact retained `aggregate-host-build-01/compile-command.json`
(5072B, SHA `acc215837499107a01bfe60544dceeb40ff19ad4d67f93252867bbf30f3de96b`).
Each following substitution must match exactly once; no other argv changes:

1. Crate name `aggregate_host` becomes `aggregate_stage_host`.
2. Snapshot source becomes the new snapshot's
   `software/v5/aggregate_production/stage_host.rs`.
3. Output becomes fresh `aggregate_stage_host.exe` under the new run.
All seven direct extern names and paths stay unchanged: anyhow, bincode, risc0_zkvm,
serde, serde_json, dmkn_module_relation, dmkn_aggregate_relation. Keep the
general-checker dependency directory for nanoda's transitive dependencies.
The profile remains edition2021, bin, x86_64-pc-windows-msvc, opt3, fatLTO,
embedded bitcode, overflow checks and panic unwind, using the same MSVC linker.
The retained module-host-build-03 already compiled the same
get_prover_server/prove_segment/lift/join/resolve APIs against this SDK. Thus
the new calls do not justify new SDK features or cryptographic backend builds.

The three retained native libraries under proof-validation-integration-build-01
remain the same ones pinned in the successful aggregate-host01 selection and
RESULT (`4cdb12b5e3aeaebcfef5e0370bd445f24ff6779b196ca69cbab60f9d57002a75`);
bind its clean attempt marker and absence of a finalization override:

| Library | Bytes | SHA-256 |
|---|---:|---|
|libdmkn_aggregate_relation.rlib|916696|829d68c1a2c51138785394e19bcb35692902144d7be19f1dbfc9c9742f1952b4|
|libdmkn_module_relation.rlib|4217412|10efaf57720635b0c347487194283117599ecb3be326b4c51b3c9dbcc144a4bf|
|libnanoda_lib.rlib|11339020|c0c0b10ba18adf5c20496d751cc9cbbc911677fafe64461d963dadc53a37c4a2|

The third library is transitively loaded. The new stage source needs only
canonical::{R,sha,hex,unhex}, the unchanged Header/Journal interfaces and
relation::{MAX_ASSUMPTIONS,check_bytes}, all available in the existing host
libraries. Root prefers this narrower choice: a host command addition does
not need to import the bounded-parse optimization or add an equivalence
boundary. It preserves the snapshot host's exact native preflight behavior
and cost; the optimized guest is independent. Repeated native preflight cost
remains chargeable in later production, not silently credited as optimized.
No old successful compilation needs repeating.

### Finite retained runtime selection, not a whole SDK census

Start from the pinned3142-entry runtime map in the old aggregate-host selection
`b8c64994f64c66eaa8a90612d5fa0f3ebcad4ce053e86f4f8fe485408cadbb8b`.
Retain only this deterministic subset:

- Immediate files in the exact14 retained `-L` directories with extensions
  `.rlib`, `.rmeta`, `.dll`, `.lib` or `.a`.
- The same98 C: host-tool/link-library entries already selected there.
- The selected rustc.exe, DLLs immediately in its bin directory, and immediate
  x86_64-pc-windows-msvc sysroot library files with those link/runtime extensions.

These are map-key filters, not recursive filesystem discovery. Read-only file
size inspection gives **1071 files /2,320,491,997B**, including25 Rust
compiler/sysroot entries and the98 C: entries. No library path or digest is
replaced. All seven direct extern paths and
the compiler/linker are covered. The set retains required proc-macro DLLs and
native static/import archives; it excludes `.d`, `.pdb`, generated source and
object files not referenced by this direct command. It is a conservative
linkable-artifact set, not a claim that every selected file is actually read.

Bind the small build/supervisor helper chain, Python executable/DLL, selection,
old command/result/selection/attempt and owned telemetry-tool
pin separately. Reuse the existing owner-controlled environment construction
with a fresh output/TEMP/profile. Hash these explicit inputs before and after;
inspect only the new run tree for output accounting. Do not call the old
full-SDK/runtime/history census routines. No retained library or cache is
modified. Implicit Windows system DLLs remain a declared trusted-build boundary;
this finite pin map is not a hermeticity or hostile-build sandbox proof.

### Proposed finite envelope and completion condition

Reference costs are actual retained successful links, not fresh measurements:
aggregate-host01 used65.375 workerCPU +6.640625 controllerCPU /72.2037113wall,
with987,435,008B peak Job memory and a6,626,304B executable. The more comparable
module-stage host03 used105.625 workerCPU +19.1875 controllerCPU /213.1983675wall,
with1,103,548,416B peak Job memory and a66,652,160B executable. Stage methods
can make substantially more backend code live than snapshot/verify alone;
therefore the smaller aggregate-host executable is not a justified size cap.

Propose one shared240s **inclusive kernel+user CPU** /300s worker-wall Job,
3072MiB, six active processes;40s ordinary controllerCPU /60s total including
finalization reserve;420s total wall;512MiB /8192 fresh output entries;1MiB
combined command logs. All clocks retain one initial origin. The native Job's
user-time limit must be supplemented by live inclusive polling and final
inclusive checks, as in the reviewed guest successor. Stop on the first
unexpected command exit, budget failure or changed pin; no retry or renewal.

Fresh name proposed: `aggregate-stage-host-build-01`. Root selects the exact
source/runtime map before any adapter execution. A future success would mean
one compiler command completed, the exact sources/inputs stayed unchanged,
the Job is cleanly closed, and a fresh executable pin was saved. RESULT/attempt
must be exclusive writes with a late overriding FINALIZATION-FAILED marker.
No host invocation, proof, image execution, network command or mathematical
admission belongs to this build. The adopted prior command's phase and recipe
are reusable; its old controller is not reused unchanged because it expects
the snapshot-host source set and uses an overbroad runtime pin set. Per root's
current scheduling choice, even this one-link compile is deferred until the
current guest-build/screen outcome; this feasibility note does not renew it.

## One-link controller ready for independent source review

The earlier statement that no adapter exists is superseded by this source-only
checkpoint. `software/v5/aggregate_production/build.py` is now 17,828 bytes,
SHA-256 `a1d2c22427ffa9f8293813ac76359f9cdde6a3f73870c75a209dad2310bc781a`.
The two reviewed Rust files and API remain unchanged. No Python project import,
test, compiler, host, guest or proof was run by this author. Root still holds
compilation until successful execution-screen adoption and exact selection.

The implementation follows the preceding one-link contract: three exact argv
substitutions only, seven unchanged externs, the same 1,071 retained compile/link
files (2,320,491,997 bytes), fresh three-source snapshot and private output/TEMP,
one shared finite Job, and no backend/checker/relation compilation. Its exact
success is `PASS_AGGREGATE_STAGE_HOST_ONE_LINK_ONLY` in
`DMKN_V5_AGGREGATE_STAGE_HOST_BUILD_RESULT_V1`; final adoption additionally
requires the matching attempt marker and no overriding finalization failure.

Source self-review made three concrete pre-use corrections:

- Check the original controller/wall envelope **after** every output census as
  well as before. A late scan crossing the limit therefore fails or writes the
  final override; it cannot silently leave a passing record.
- Hash the full 2.32 GB runtime map once before preparation and once during
  finalization. The intermediate precompile rebind checks small records,
  helpers and sources, avoiding a third redundant read of unchanged runtime
  bytes. No whole retained-directory census is introduced.
- Record the complete explicit environment, not merely its key names. The
  reused environment helper constructs it from fixed values rather than
  inherited credentials. It points TEMP/TMP/profile/cache to fresh directories,
  preserves the old MSVC/SDK LIB/INCLUDE/PATH values and telemetry opt-out, and
  contains no consumer Cargo package variables required by these source files.

The environment helper also hashes cl.exe and rc.exe for metadata, even though
this direct Rust command executes neither. The 1,071-entry runtime set remains
unchanged; the old environment record is now separately pinned:

`aggregate-host-build-01/environment-profile.json`, 2,241 bytes,
`34525808d26848e9582ad5ada38ff66fae2205f79ae0421a33f72fbd67af4e18`.

Its exact three host-tool observations (cl/link/rc) enter the small helper pin
map, and the freshly generated observations must match them. Thus those two
additional reads are neither invisible nor mislabeled compiler executions.
The stage source has only its reviewed receipt path module; it adds no
compile-time env/include input. Its serde/json and builtin macro use retains
the same selected host dependency versions and environment as the old host
recipe. General host runtime/system-DLL trust remains explicit, not hermetic.

### Exact root selection construction

Root can prepare one fresh `aggregate-stage-host-build-01-selection.json` with
exactly six fields:

1. `schema`: `DMKN_V5_AGGREGATE_STAGE_HOST_BUILD_V1`.
2. `name`: `aggregate-stage-host-build-01`.
3. `authorizes_compile_only`: true.
4. `sources`: the three relative paths in `SOURCE_SET`, each with exactly
   `bytes` and `sha256`; use the builder pin above and the unchanged Rust pins
   in the preceding table.
5. `runtime_pins`: filter the pinned old 3,142-entry selection map by the exact
   deterministic predicate above; retain its original path-to-digest values,
   require 1,071 entries, including 98 C: and 25 Rust-toolchain entries, and
   reject missing direct extern/compiler/linker paths. Do not reselect versions
   or import any bounded-native replacement. The controller independently
   reconstructs and compares this entire map and its byte total.
6. `limits`: exactly the unchanged proposed limits: worker CPU 240, worker wall
   300, memory MiB 3,072, active processes six, ordinary/total controller CPU
   40/60, total wall 420, fresh bytes 536,870,912, fresh entries 8,192 and combined
   command-log bytes 1,048,576. Use the keys in the controller's `LIMITS` map.

Require selection/run/attempt absence, an exact reviewed source hash and old
selection/command/result/attempt pins before exclusive selection creation.
Root's separate PowerShell selector owns that preparation; this lane has not
written one or launched it. The new controller takes the selection's absolute
path and SHA-256 under the pinned isolated Python (`-I -S -B`), explicitly in
the canonical workspace. No runtime follows automatically from this note.

Remaining uncertainty is actual compile/link success and resource sufficiency,
not a known source-contract mismatch. The independent reviewer must still
check the new controller and exact selection. Even a passing host build proves
neither a completed A receipt nor final software readiness: the successful
adopted capsule, separately budgeted missing proof stages, final exact A/H
verification, public member admission and reciprocal useful reuse remain
separate gates. Failed and successful earlier costs remain chargeable.

## Independent aggregate-producer plan challenge

Receipt/source-loop independently read the proposed aggregate producer plan,
the complete retained Python producer, current staged-host/API, snapshot
producer and actual `aggregate_claims` header bindings. This was read-only,
with no source execution or changes to the plan author's files.

Beyond root's separately identified legacy-header/version citation (which the
plan author is correcting), one concrete consistency issue was reported:
`missing_plan` can compute regeneration of a lost segment while preserving a
surviving higher prefix, but routine same-allowance continuation requires every
prior successful checkpoint's exact pin. A missing or replaced prior-success
file therefore refuses before that graph can run. The minimal safe resolution
is to distinguish the graph's mathematical reuse capability from authorized
routine continuation: intact checkpoints resume normally; lost/corrupted prior
success requires a separate owner recovery decision carrying the previous
charges. Automatic lost-file recovery need not enter the first controller.

The remaining proposed composition boundary matches inspected source: the old
constructor exposes the pinned supervisor/Job and file-check helpers without
launching a module workflow; graph/missing-plan are statement-independent. The
new loop must own the aggregate argv, full 192-byte current header, two capsule
bindings, new checkpoint prefix and exact JSON, and must never call old
`_request`, `_checkpoint` or `_run`. The checkpoint offsets, 3s+m graph count,
finish dependency on all segment proofs, and stage JSON fields match the current
host. The plan correctly treats nested Job/outer accounting as overlapping and
saved framing/reports as unauthenticated bookkeeping, not admission.

No other concrete source-level implementation blocker was found in this scoped
challenge. Runtime size/funding/closure checks remain essential and unobserved;
this is not approval of a proof budget, source implementation, actual resumed
production, cryptographic soundness or release completeness.

