# V5 cryptographic integration: smallest consequential path

Source-only feasibility selection, mechanism lane. Root owns implementation
selection, builds, finite execution/proving allocations and image adoption.
No new guest, host, proof or receipt is produced by this note. V4 images,
receipts, snapshots and used sources remain frozen and cannot be relabeled.

Root subsequently selected SOURCE implementation of this host/capsule route and
a finite guest build adapter. `src/bin/module_host.rs` is authored and passes
actual metadata compilation (metadata02) and independently reviewed executable
linking (host01, exact executable SHA256
`e3b357bb719db9c3e02fa65fde704e0cbd4dd73f48ee0157a6bf1e55dc5c9190`).
It shares canonical/commitments/journal/policy source,
supports prepare/execute/stage/verify/receive, admits only real fully resolved
succinct Poseidon2 receipts. That used profile1 host has capsule2/checkpoint4;
the newly selected mutable profile2 successor has capsule3/checkpoint5 and V2
session/snapshot domains and is not compiled/qualified by those old passes. Native
host compilation is by direct pinned retained-rllib linkage; Cargo auto-bin
discovery is disabled so guest selection does not inadvertently compile this
host-only file or add its backend dependencies to the guest graph.

Current build checkpoint: guest01 failed before compiler/source copying on an
inherited census metadata key; its failure/cost is preserved. Narrowly repaired
guest02 and retained-backend host-link01 have independently reviewed exact
selections and were launched by root. Host01 passes with clean process closure;
guest02 now passes final rebinding and yields the actual new 1,402,284-byte ELF.
See MODULE-RELATION for pins and limits. `assemble_guest.py` is independently
source-reviewed and exact actual selection01 is prepared from guest02's
successful result/ELF; root review/launch remains separate. Metadata compilation,
guest linking and image assembly
remain distinct from guest execution, proof production and public admission.

## Recommended route

Reuse the already built/pinned RISC0 SDK, cryptographic backend, toolchain and
incremental proof operations. Build ONE new mathematical guest and a small
new-profile host/receiver. First measure execution of the new relation; select
a finite proof only after that screen, not a blanket multi-module campaign.

The consequential first pair is the actual new-policy Tree/fold `base` module
and its `fusion` child. The first has no module parents; the second uses one
genuinely certified module, keeps imported theorem proofs absent and authenticates
the demanded computation bodies. This exercises actual module certification,
not a trivial synthetic proof or a new proof of the unchanged old relation.
The existing `project_summary`/`fusion_map` inputs are later options for a genuine
two-parent/depth-two receiving boundary; they are not automatically selected.

The sequence is:

1. Finish native wrapper hash/binding controls against actual repinned inputs.
2. Cross-build the new guest, assemble with the retained compatible kernel,
   independently adopt the resulting actual image ID and exact source manifest.
3. Adapt/build the host using retained native rlibs, then execute ONLY the base
   witness to obtain actual cycles, segments, rows, memory and journal.
4. If finite cost is justified, create one coherent base snapshot and its fully
   resolved receipt. Fresh cold verification adopts only that new-profile module.
5. Construct fusion witness with the actual adopted image and the actual base
   receipt journal. Execute fusion, then separately select its snapshot/proof.
6. Cold-receive fusion with no base receipt, witness, source or proof ancestry
   available to that receiver. Its own returned receipt must verify completely.
7. Integrate the same receipt gate into acquisition/custody/import, not a parallel
   experiment-only acceptance path. Root selects public reciprocal operation.

Step 6 verifies fusion's certificate alone. To use its statement/type and perform
new computation, a consumer may still demand authenticated semantic definitions,
groups or bodies. It obtains the corresponding owners' *resolved certificates*
without their proof ancestors. This is not constant-cost typechecking of all
possible mathematics or permission to omit computationally needed definitions.

## Exact guest build seam

Existing `receipt/Cargo.toml` uses the same four external dependencies and pinned
SDK source as the successfully built collection guest. The new checker must
replace the old checker source; reusing its old compiled guest library would
omit conditional roles, exact missing bodies and raw-row correspondence.

Retain the source topology `modules/receipt` and `modules/native/checker` in a
fresh immutable build snapshot, so the existing relative dependency resolves.
Use `--bin dmkn-module-guest` explicitly; do not compile the native diagnostic
adapter for the RISC-V guest target. Select the seven receipt source modules
plus checker source and manifests, not caches or old targets.

The retained build invocation is Cargo release, target
`riscv32im-risc0-zkvm-elf`, locked/offline, with
`-Z build-std=alloc,core,proc_macro,panic_abort,std` and
`-Z build-std-features=compiler-builtins-mem`. Inherit the exact adopted
guest03 preparation's compatible std source, cached archives, RUINT1.16.0 lock
adjustment, linker and environment. Its RISC-V flags include `passes=lower-atomic`,
`-Ttext=0x00200800`, fatal linker warnings, panic abort and the selected custom
getrandom backend. Fresh link-map paths are required.

The source manifest/package name now changes, and the wrapper adds a library
target. A whole old unit graph cannot therefore be asserted byte-identical.
Prepare a new lockfile/source map and require an explicit normalized graph delta:
only the new root library/binary and changed checker source/identity are allowed;
every external package version/checksum/feature/platform/dependency edge stays
bound unless separately reviewed. Copying an old root lock and blindly asserting
`--locked` suffices is not a plan. No dependency update or remote fetch is needed.

Retained build references:

- `experiments/general-checker-guest-03/prepare-03`: adopted locks, seed,
  compatible std/toolchain environment and graph.
- `experiments/certified-collection-01/build.py`: finite fresh source-copy and
  cross-build pattern; its old four-overlay scope is NOT reusable unchanged.
- `experiments/certified-collection-01/BUILD-OUTCOME.md`: actual comparison
  build cost, not a cost bound for the new larger relation.
- `experiments/certified-collection-01/ASSEMBLY-OUTCOME.md`: retained compatible
  kernel/image-assembly pattern. File SHA is not an image ID.

The guest receives `u32le(witness byte length) || strict JSON`, no trailing input.
After actual image adoption, update only witness.image and recompute the
expected journal; ModuleID does not change because image is not semantic
identity. Every parent journal must carry that same actual image. Zero-image
native diagnostic journals remain unusable as parent receipt statements.

## Host adaptation, no cryptographic backend rewrite

`experiments/certified-collection-01/host.rs` already implements bounded
`execute`, coherent `snapshot`, `segment`, `lift`, `join`, `resolve`, `finish`
and cold `verify` using the retained SDK. Its source supplies the proof algorithm,
not a compatible application protocol. A fresh host must replace these seams:

| Old seam | New required binding |
|---|---|
| collection vector codec and short journal limits | shared184-byte DMKNM002 profile2 journal, semantic policy and exact F |
| two-frame header/packet parser | one length frame plus the strict relation input |
| member-index parent selections | exact distinct parent journals already in the witness |
| old packet/interface/rank checks | existential module conclusion, ModuleID/summary, image/F/policy and exact rank |
| collection session/snapshot domains | fresh `DMKN-MODULE-SESSION-V2` and `DMKN-MODULE-SNAPSHOT-V2` domains |
| proof session snapshot v1/checkpoint v3 | fresh versions if snapshot payload semantics change |
| `members` telemetry | module/group count, selected parents, witness bytes and demanded-body bytes |

The host preflight need not rerun the kernel. Strictly parse the input, derive
its expected journal using actual image and authenticated module summary, bind
foundation/policy and every parent journal, and require one real parent receipt
per distinct selected journal before execution. The journal certifies existence
of a checked witness, not an exact proof/source identity. Exact host input hashes
remain local capsule bindings, not mathematical authority.

Preserve exact parent-set equality: no absent, duplicate or unselected parent
receipt, and no alternative receipt whose journal differs despite certifying
the same ModuleID. One arbitrary valid parent certificate is not authority for
another journal. Feed these real receipts to `ExecutorEnv::add_assumption`.
Actual session assumptions must match the selected parent count and statements;
each requires an actual `resolve` operation before finish.

Initially retain conservative operational limits, for example the old eight
immediate parents/128segments/64MiB binary object/512MiB aggregate read bounds.
Those are an explicitly narrower host deployment profile than the relation's
4096-parent format ceiling, not silent semantic changes. Raise none merely to
make an unbudgeted workload fit. The new JSON ceiling is16MiB; host framing adds
four bytes, which must not accidentally reduce or exceed the selected bound.

The native host links the existing backend rlibs with fat LTO; do not rebuild
the backend. Separate crate versions are selected by their actual retained
compiled origins, not by similar filenames. Sharing journal/canonical/policy
source can be done with `#[path]` modules and does not require linking native
Nanoda into the public receiver. The verifier does not execute the local proof.

## Public receipt acceptance: exact contract

```text
verify_module(receiptBytes, expectedModuleSummary, adoptedProfile, limits)
    -> private process-local VerifiedModule | refusal
```

`adoptedProfile` is locally adopted and binds the actual image ID, exact verifier
binary/SDK parameters, foundation, semantic policy, supported receipt kind,
hash suite and limits. It cannot be supplied by the untrusted offering peer.
It is distinct from the immutable mathematical ModuleID.

Required order/boundaries:

1. Bounded exact receipt bytes under supervised CPU/memory/output limits; strict
   fixed-integer bincode with trailing-byte refusal. Parser crash/timeout is
   refusal. Byte bounds alone are not hostile-parser process containment.
2. Accept only `InnerReceipt::Succinct` with `hashfn == "poseidon2"` for this
   first profile. Reject Fake, composite and other unselected kinds explicitly.
3. `VerifierContext::default().with_dev_mode(false)`, then actual
   `Receipt::verify_with_context(&context, adoptedImage)`.
4. Decode exact184-byte profile2 journal; validate recomputed ModuleID, group
   count, image equality, adopted F/policy and expected summary/ModuleID. Rank
   is an authenticated fact of this certificate, not identity of the theorem.
5. Return private evidence bound to exact receipt SHA, adopted profile and
   decoded summary. Only groups opened against this evidence gain imported
   roles. Arbitrary stored JSON `verified:true` has no authority.

SDK `receipt.rs:163` verifies inner cryptographic integrity AND equality to the
complete `ReceiptClaim::ok(image, journalDigest)`. This enforces successful halt,
exact image/journal and EMPTY assumptions. Integrity-only verification does not
enforce the last requirement and must never mint VerifiedModule. Final proof
creation must invoke the same full gate before writing a public receipt.

An in-process Rust capability can use a nonpublic constructor. A Python caller
must itself run the exact adopted verifier, bind exact input bytes and same-call
output under supervision, then mint its private capability. An external success
file is not transferable proof. Cold processes reverify the retained succinct
receipt; a process-local cache can reuse exact receipt/profile verification while
host integrity holds. Custody persists opaque receipts and unverified offers,
not a magically authoritative persistent success bit. Scale owns that integration.

## Avoiding repeated guest execution during proof stages

The retained host presently reexecutes the complete guest before EVERY stage
and compares against one saved coherent snapshot. With nsegments and pparents,
it uses `3n+p+1` proof/finish/cold-verify commands, plus the snapshot. That repeats
expensive witness parsing/checking many times. This is real avoidable producer
work, not proof-ancestry work at receivers.

A justified fresh host can execute ONCE to create an immutable operation capsule:
exact image/input/expected-journal hashes, actual complete session claim,
cycles/segment settings, parent receipt hashes, ordered assumption claims and
coherent ordered segment witnesses. Every checkpoint binds the exact capsule
and its operational key. Segment/lift/join/resolve stages then need no fresh
guest execution. They still verify their cryptographic inputs/outputs; final
finish still checks the complete exact adopted-image receipt and journal.

Reason: even if a capsule or claimed execution transcript is malicious, it is
only a prover witness. Successful final verification establishes existence of
a valid guest computation with the committed module conclusion.
A corrupted capsule can waste bounded work or fail, but cannot create an
accepted mathematical conclusion unless cryptographic/checker assumptions fail.
Profile2 intentionally does not attest which exact input was checked. Host
session/capsule binding still detects accidental run mixing but cannot make
transferable provenance claims. Mathematical soundness needs the existential
statement, whose types/computational definitions and exact parents remain bound.
No persisted capsule becomes mathematical authority. Resolve still uses genuine
verified parent receipts and final empty-assumption verification remains mandatory.

This optimization requires a new snapshot schema and independent review of
coherent segments, normalized Halted claims, parent-assumption ordering, replay
bindings and final verification. It must not modify/reuse old snapshots or
randomly mix new executions with old witnesses. It is a small host seam over
the existing prover; source/theory review can decide it before any proof run.

## Cost model and prospective allocation

Let E be one execution/snapshot CPU cost, n its actual segments and p its actual
parent assumptions. Let S_i,L_i,J_i,R_j be actual segment/lift/join/resolve costs.
The useful producer accounting target is:

```text
P = E + sum(S_i) + sum(L_i) + sum(J_i) + sum(R_j)
    + finish + coldVerify + allController + failedWork + setupAllocation.
```

Do not multiply one native-check timing by an assumed cryptographic factor.
No valid v5 cycles, segment count or proofCPU estimate exists before the actual
new-image execution screen. Its result fixes n and row padding; these permit
budget planning, not a proof of proportional CPU savings. Choose finite stage
and cumulative CPU/wall/memory/disk bounds from that screen and at most one
selected first-stage calibration, retaining that stage as part of the same
campaign rather than throwing it away and repeating it.

Useful retained planning observations, NOT v5 measurements:

- Prior fresh guest cross-build:167.859375 workerCPU +96.859375 controllerCPU,
  349.37allocation-wall seconds, peak~0.945GB private Job memory.
- Prior host link:57workerCPU +9.671875 controllerCPU,113.07outer-wall seconds.
- Prior image assembly:0.4375knownCPU. New source/checker/graph may differ.
- Prior66segment parent-free campaign:69,638.921875 known cumulativeCPU,
  including earlier failed/setup work; terminal campaign wall7690.78seconds.
  Cold inner verification was12ms, but full cold phase wall~0.400seconds.

These values show why a large speculative proof campaign is inappropriate even
though receipt verification can be cheap. The new proof cost must be amortized
against independent future uses. Growth accounting must include production,
search, receipt/body storage, replication, service and failures; succinctness
alone does not establish positive useful-growth advantage.

## Remaining central gates

No production claim until the exact new relation/image is built, independently
reviewed, produces actual resolved receipts, refuses invalid/Fake/wrong-image/
unresolved inputs through the public gate, and supports cold returned-module use.
Nanoda-to-Lean correspondence and supported declaration coverage remain explicit
trust obligations; certificates attest the selected program, not an unproved
equivalence to all Lean. Host parser/supervisor containment and public discovery/
custody interoperability remain real software work, not documentation waivers.

Next requested root decision: adopt the guest/host adaptation scope and the
single-execution capsule optimization after assurance review, then select ONLY
new guest preparation/build and host source. Proof authorization waits for the
actual execute-only work/cost screen.
