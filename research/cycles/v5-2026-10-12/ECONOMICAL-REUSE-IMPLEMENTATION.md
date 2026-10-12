# Economical native deltas over real certified frontiers

## Status and selected problem

2026-10-12: post-guide implementation explicitly resumed. This is new source-led
work, not another base-production audit or a renewal of its proof budget. The
retained base receipt is available; producing a fresh succinct receipt for each
small theorem is not the default contribution route. Root owns execution,
adoption and Git. This worker owns only this checkpoint and fresh, unrun
`software/v5/delta/` sources.

The first consequence needed is a real receiver that can accept a bounded new
mathematical proof over that certified base, while downloading/checking neither
the base's theorem proofs nor an unbounded chain of uncertified descendants.
No empirical speedup, completed native build or positive delta is claimed here.

## Existing code establishes a useful seam

`modules/receipt/src/relation.rs::check_bytes` performs the actual module
correspondence/native local-proof checks and returns a computed journal and
the exact parent journal bytes. Its conclusion is conditional until every
parent journal is discharged. It must not itself be treated as admission.

`admission/verifier.py::ReceiptVerifier.receive` actually invokes the selected
non-dev cryptographic verifier and creates an instance-local `VerifiedModule`.
`describe` revalidates that handle's live owner and returns its exact journal,
receipt digest, module and summary. Its `close` invalidates its handles.

The older `receipt_native check` diagnostic omits the returned parent bytes;
it exposes only a parent count. The retained binary must not be assumed to
implement the current profile2 relation simply because a similarly named source
exists. A fresh driver can include the unchanged adopted relation and return
its exact conditional conclusion. It does not need a new guest image, new proof
production or changes to frozen host/checker sources.

## Proposed smallest implementation (root review requested)

Use two explicitly bound operations in one trusted owner session:

1. The exact existing `ReceiptVerifier` verifies each certified frontier from
   its real receipt, or revalidates a still-live matching handle it minted.
2. A freshly selected native driver checks each delta's full bounded witness.
   It returns the input digest, computed journal and exact parent journals.
   The controller admits a delta only if every returned parent journal is
   already in its private accepted set. It checks the delta's own image,
   foundation/policy and requested identity too, including a zero-parent delta.
3. The controller reconstructs the entire target dependency closure from those
   actual returned parent bytes, rejects unused/duplicate/forward references,
   and revalidates all real frontier handles and immutable input/runtime pins
   immediately before returning its own distinct `VerifiedDelta`.

This split invocation is sound under the same trusted-owner-process assumption
as the existing receipt API: no other participant can substitute a persisted
JSON result or fabricate an owner-local handle. The root must adopt the native
binary and its actual checker/runtime pins. The native report alone is never
accepted outside the bound invocation. Combining native and receipt checking in
one Rust executable remains possible, but is not required for this induction
argument and would add expensive crypto-host build plumbing now.

Let A initially contain exact verified frontier journals. Process deltas in
topological order. If the adopted native relation establishes
`parents => local_journal` and all exact parents belong to A, induction permits
adding that local journal to A. Checking its identity/profile prevents a valid
but different local conclusion from being substituted. Final closure reachability
and bounds prevent hidden or disconnected uncertified ancestry. This argument
assumes native checker correctness, receipt soundness and the trusted owner;
it is not a formal refinement proof of Lean or of native/guest machine targets.

## Full-cost and locality requirements

The receiver envelope bounds the whole packet, not depth alone: total wire and
decoded receipt/witness bytes, frontier and delta counts, parent edges, openings,
semantic bodies, parser nodes/depth, native/crypto calls, CPU reservations, wall
and peak memory. Failed and unused submitted material consumes budget; no retry
or below-frontier ancestry fetch occurs. Each shared delta is checked once in
that operation. Oversized closure reports `NEEDS_SEAL`/resource-incomplete,
not a false-theorem finding. Actual proof checking still can time out.

For packet cap B and finite owner envelope, a successful check has no mandatory
term proportional to proof history below real frontiers or network population.
This does not claim all Lean reduction is cheap, guarantee completion of any
true theorem, or eliminate semantic definition-body downloads. Growing chains
eventually require a funded seal, a different proof or a larger owner envelope.

Costs must include receipt verification, native deltas, acquisition/discovery,
frontier retention and failed work. Compare with an equally optimized warm
local library and ordinary shared checked packages. The existing selective-
sealing break-even inequality remains conditional; the base's measured proof
cost cannot be hidden as a free certificate in a claimed full-cost result.

## Integration boundaries that must not disappear

`VerifiedDelta` must never be passed off as `VerifiedModule`; existing crypto
parents still require real receipts. A self-contained onward packet retains
the complete uncertified closure, rather than exporting a local success handle.

Existing `ImportSession` and `SourceOperation` deliberately require their exact
receipt-backed classes. Therefore accepting a native delta does not by itself
integrate delta-backed ordinary Lean authoring. A separately reviewed fresh
authoring adapter/successor will be needed; frozen receipt-only APIs must not be
silently relaxed. Receiver implementation should expose authenticated group
openings and exact checked journals needed by that later adapter, without
inventing a receipt for a delta.

## Root-approved source implementation and exact build prerequisite

Root approved the fresh-driver/split-live-frontier design. New, unrun sources are
`software/v5/delta/native.rs`, `packet.py`, `receiver.py`, `__init__.py`, `API.md`
and `test_packet.py`. The receiver implements the full packet induction, distinct
live authority, complete onward packet retention, bounded resources and refusal
behavior described above. Nine test groups are structural/refusal controls only;
they have not run and do not fabricate positive mathematical authority.

The initial independent source review was requested at driver SHA-256
`66d5c58a99cccab4ffe1c53264fd1ae1eb0941c15dcadff0a54ef2844caa664e`, packet
`3ebd338998acefa7808695ec4a0f5320d15a6893b8c339243af21afad456c0f3`, receiver
`4ccc30212de07fdd84924bd463efbb3576125bf2ee2ebe044c23879316d4aef2` and tests
`f7b1279b6d9b34dac385b5b1bbb4eb9224eca7b71c3cb59d688006bcc425c27c`.
Root's telemetry finding was subsequently fixed before any use: local
`process.json` has fractional CPU/wall and is parsed by `production.producer.parse`,
not the integer-only mathematical parser. The receiver now also pins that parser's
two source files. Thus the receiver review hash above is historical, not a later
runtime selection. Clean nonzero worker rejection maps to invalid/unbound;
unclean closure or resource exhaustion maps to resource-incomplete. Neither is a
false-theorem assertion. A native missing-demand subtype is not yet generally
available; retained diagnostics remain necessary.

The source-loop agent now owns the disjoint ordinary-authoring successor design.
It has the concrete `describe/open_group/export_packet` API and original-frontier
lifetimes. This receiver is not being declared the final software scope.

The future build should compile only the new native driver, preserving the
`delta/` and `modules/receipt/src/` relative layout in a fresh source snapshot.
It includes these unchanged actual profile2 source pins:

| Included source | SHA-256 |
|---|---|
| `canonical.rs` | `23ca5fa1bfe536db08136bef9956426e4d43e90fa36d00a1886e97eef6892d9b` |
| `input.rs` | `4b5da4aefeef4ca7dc2ce3d2bd10cd0f270a3d5682f2ea16d8ea2e37c63bfa46` |
| `foundation_static.rs` | `1dd5bd98389d54d09dce554c6a9d82cf841254e3249dadf921360e154c5ebcd5` |
| `foundation_data.rs` | `ed450bccfc23fa613bb0c8a8bd3c9ba67ab8477c1d59bf5c1eb5c11cf05423ab` |
| `commitments.rs` | `ec77943fb15b15ec84c82a864c926536c1356b300cdd616fea93473202d9ed91` |
| `journal.rs` | `1a49bdf52fd38852dafb44ecbae772d0aad2456870ed046b15acabcc0c18dbe1` |
| `policy.rs` | `cd254a0a591d73d69f3e504bca75ac50f1962f5e61d730340db029970baae902` |
| `relation.rs` | `3625bc9c7708e5a03580e1e61bc7019f5b7cf6ad48ee37f6d749919d245e2eb8` |

The actual retained `native-library-01/libnanoda_lib.rlib` is 10,230,216 bytes,
hash `b52ee8efe8883b2b6025c08dbcc55a7032a6ec94e87a6adc9d202b0f8587a2c5`.
The prior `NATIVE-BUILD-PLAN.md` identifies the adopted rustc, serde, serde_json,
RISC0 SHA dependency, linker and retained dependency/library maps. Reuse those
only after exact fresh build selection verifies the relevant current bytes.
Required target is `x86_64-pc-windows-msvc`, edition 2021, overflow checks enabled,
panic unwind, optimization with final LTO/embedded bitcode matching retained
dependencies. Do not use the older native wrapper executable as profile2 by
name, rebuild dependencies unnecessarily, or invoke a guest/prover. The prior
failed-descendant build remains failed; future finite build supervision must
record actual closure rather than laundering its lifecycle as a pass.

No new compile, test, receipt verification or proof was run by this worker.
Independent source review, fresh finite native build and actual changed-boundary
integration remain root-owned next operations, not authorized by this note alone.

### Concrete build handoff and real workload reuse

`software/v5/delta/NATIVE-BUILD-PROPOSAL.json`, SHA-256
`bdd23d50c7e45906e84cda6167f1ea6bf73c25a6b4cfae31924674998258d021`,
now specifies the nine exact source inputs, 172 retained runtime/library pins
(all independently rehashed without mismatch), and all 65 compiler argv elements.
It proposes 240 worker CPU / 300 wall seconds, 3072 MiB, six processes and 1 MiB
per log. It explicitly authorizes no runtime. Direct compilation reuses native
checker/serde/RISC0 SHA libraries; no Cargo/network, guest or proof call is needed.

Important refinement to the earlier build discussion: actual
`receipt-native-build-01` itself already used `/DEBUG:NONE` and still required
descendant termination. Its recorded 43.03125 worker CPU / 50.659013 stage wall
is a size estimate, **not a clean lifecycle pass**. Do not simply repeat that
generic supervisor. The later genuine host03 build's reviewed owned-VCTIP cleanup
is the relevant successful supervision pattern. Root owns its fresh adapter and
finite selection; no unbounded process kill or global telemetry setting is implied.

Root's new actual receipt/source integration already supplies the real child
witness at `experiments/v5-local-checks/receipt-source-integration-01/evidence/`
`preparation/snapshot/child-input.json` and `parent-0.receipt`: 1355 rows and one
ordinary-source theorem group. Its subsequent guest snapshot exhausted the
selected cycle cap; that failed operation stays failed. The native-delta route
can check this retained child without repeating the successful receiving/authoring
prefix, increasing the snapshot cap or producing a new certificate. Independent
actual integration audit belongs to its existing reviewer, not this worker.

The root-approved closure-member API is now present: `members`, `describe_member`
and `open_member_group` use the actual established journal inventory retained
after the target-closure check. They do not create receipt handles or trust a
claimed packet inventory. This lets the separate ordinary-authoring adapter
authenticate the Tree/base interfaces occurring in a checked delta's theorem
types. The separate source-loop agent owns that adapter; work is nonduplicative.

The ninth structural test group now also covers finite fractional operational
telemetry versus the intentionally integer-only mathematical parser. All groups
remain unrun; exact latest test bytes must be selected afresh before any runtime.

## Source-only actual delta harness; build prerequisite failed

New `software/v5/delta/actual.py` is an unrun source draft. It selects the exact
retained child witness (113220 bytes, SHA-256
`88b71b8282afc99297bf6564d22616fce6211eed9a9e18afa1cb42a41d1206e1`),
184-byte expected journal
`07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da`
and genuine 223594-byte base receipt `850c33b2...`. Target module is
`4adbc049e4d1e29ec045d64c7dba9e27bdd506dfa6c7fb707f022be40439e742`.
The journal fixture is only an expected identity, never admission authority.

The proposed actual path spends one real cold receipt verification and two
native calls: real admission/open/member/export, then the same theorem row with
its proof expression reference changed from 1200 to its type term 770, requiring
a clean native refusal and revocation of the earlier handle. Packet-cap and
missing-frontier controls require zero worker calls. Actual source compilation,
host preparation, guest snapshot and certificate production are not repeated.
Root's outer selection should reserve at least one crypto plus two native
worker calls (suggested per-call 30 CPU seconds each), controller/finalization
headroom and a finite wall limit. Inner conservative reservation accounting
retains cache-hit and preflight reservations; it is not measured CPU consumed.

No direct original-frontier-close test is claimed: preserving the live frontier
allows a nonduplicative real native-negative control. The owner-failure lifetime
check and source argument cover distinct boundaries. Fresh ordinary delta
authoring remains the separate source-loop agent's assignment. The harness still
requires independent review and exact root runtime/configuration selection.

Root's first actual native-driver build now FAILED cleanly: retained
`native-library-01/libnanoda_lib.rlib` has no
`nanoda_lib::parser::decode_corresponded_owned_row`. Hash identity did not establish
API compatibility. The proposal, driver and failed build remain unchanged.
Harness work pauses temporarily for a read-only search for an already-built
compatible native checker; if none exists, a separately selected exact native
checker build is necessary. This does not relax any relation check or authorize
runtime. The independent reviewer owns the failed-build audit; this worker owns
the disjoint compatible-library search.

### Compatible native library search and source-only successor proposal

The full canonical-root filename census found 16 retained `*nanoda*.rlib` files:
ten RISC-V guest libraries and six native candidates. The only v5 native library
is `native-library-01`; five others belong to older general-checker, native-relation
and certified-typed-row builds. None of the six native candidates contains the
`decode_corresponded_owned_row` symbol string. That scan is corroborating evidence,
not by itself a universal Rust symbol-absence proof; no retained native artifact
with a matching current checker build map was found. The old selected01 library
has the actual compiler rejection as decisive incompatibility evidence.

All 25 current checker Rust files and its Cargo.toml (26 files) were compared to
`guest-build-05/project/modules/native/checker`: every SHA-256 matches. The parser
is `7a183a1c9e6ff3ee2c32ee6542ed85d3de0835b00e235f80f6982c3e7038d218`,
with the required public owned-row decoder at line 160; module correspondence is
`f37c855666480553ee9b95f59dc3ba7ad19316e8e707aacd47fecfa29f1d12e2`.
Guest05 selection SHA-256 is
`5da04eb9fa61bb667efa2afe35157a86a2bfde6be05a3c0f64f7fc99e27fb74a`;
its retained SOURCE-MAP is
`df3d2f881ad0b2460e2b39c45720147c157fadb1eb38646a2a4649202cf7f8f3`.
No checker sources need changing for the new native build.

Root requested source-only `software/v5/delta/NATIVE-LIBRARY02-PROPOSAL.json`.
It uses the exact Run-V5-Check schema, current 26-file checker pins plus its
unchanged runner (27 source pins), all 68 retained native-library01 runtime pins
(freshly rehashed, zero mismatch), and the same direct rlib-only compiler argv
and eight dependency externs. It selects fresh name `native-library-02`, 90 CPU
/120 wall seconds, 2048 MiB, four processes (the prior actual cap), 1 MiB logs.
It invokes neither Cargo nor a linker executable, no dependency rebuild, no guest,
no proof and no test. The predecessor library01 used 34.59375 measured Job CPU
and 11.800615 wall seconds with clean closure; this is an estimate, not a promise
for the changed checker. The proposal remains source only: root must separately
adopt/copy the exact selection under experiments, reviewer clear it, then launch.
The new driver's later link selection must bind the actual produced rlib hash,
not a predicted path or this proposal's mere existence.
