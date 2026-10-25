# Fixed-basis reuse: bounded source payoff decision

2026-10-24. SOURCE/THEORY ONLY; no code, state opening, new run or adoption.
Recommendation: keep ordinary native/batched admission as the default. A narrowly
bound fixed-basis snapshot is a credible next cut optimization, not a reason yet
to ship cuts publicly. Do not build a persistent worker or a new certificate lane.

## What the actual observation says

Root reports recursive01 worker CPU: basis 16.203125 s, 34-unit native batch
1.828125 s, first cut 20.5 s, second cut 20.21875 s. Cut parent CPU is
24.109375/26.65625 s under intrusive `sys.setprofile` instrumentation. These are
different operations, not matched alternatives: subtracting basis CPU from cut
CPU is NOT a measured optimization saving or a fair cut/native speed comparison.
The cut+diagnostic-reopen trace counts 324/420 source ADOPTION reads. Counts expose
repeated validation; instrumented parent time does not establish its ordinary cost.

Two independent source costs are real: `GroundedCut.check` calls `receiveSeed`
on every cut, repeating 456 kernel additions from empty; `SourceAnchor.check`
reopens identity bytes and reads fixed SQLite metadata at many inner checkpoints.
Neither cost depends on theorem ancestry, but both can defeat practical benefit.

## Existing primitive that can remove repeated basis construction

`ordinary_lean/BasisSnapshot.lean::checkAndWriteBasis` invokes the real empty
receiver, checks quotient state and all 581 names, and serializes actual returned
kernel records. Its ModuleData has zero imports, entries and extra names. The
ordinary controller promotes that artifact only after a bound clean live worker
event; `portable_catalog._commit_checked` records length/hash and native origin.
The current implementation support already names the snapshot helper and loader.

`LocalSnapshot.restoreLocal` can consume a ONE-module plan: basis=root, no parent.
It supplies exact artifact paths, empties the module search path, disables plugins
and extension loading, selects private records and supplies no IR artifacts.
`checkRestored` checks quotient state, the single module identity, zero imports/
entries/extra names and record counts. This is trusted native deserialization,
NOT verification of a downloaded `.olean` or re-kernel-checking stored proofs.

Thus a fixed cached basis can replace seed reconstruction without importing
arbitrary ancestors. It still reads/deserializes the FIXED basis proof bodies;
the claim is independence from growing application history, not zero proof reads.

## Necessary protected binding and semantic argument

At paid native-to-cut derivation, while holding the genuine native owner lock:

1. Authenticate the committed native-bootstrap basis root and its actual basis
   operation; derive only its first module, not the selected extension's snapshot.
   Existing validated context/basis-record APIs suffice at this one-time boundary.
2. Bind source store, foundation, implementation/support, basis root/module,
   zero-parent role, exact ordinary path, length/hash and the actual fixed seed/
   inventory identities into a protected local basis descriptor. The current
   SourceAnchor binds support identity but NOT this artifact, so it is insufficient.
3. Commit the descriptor only within the genuine derivation event; supplied hashes,
   saved PASS files, filenames or downloaded descriptors cannot establish origin.
   Use a distinct cut support/epoch; do not reinterpret existing used cut state.
4. On reuse hold source/cut locks, validate live support/withdrawal and exact basis
   bytes before unsafe deserialization; keep paths immutable through the event.
   Construct a singleton import plan internally, never accept a caller module list.
5. Check restored quotient state and all fixed-name/inventory rows, with
   no extra declarations or axioms, before acceptance. Preserve concrete checking,
   signature grounding, new-theorem checking, exact final census and atomic commit.

Conditional argument: the committed artifact is the selected serializer output
of the checked fixed basis; byte integrity and the adopted serializer/deserializer
correspondence recover that basis. Inventory equality includes types, bodies,
reduction heights and generated inductive/recursor metadata, not just statements.
It is NOT injective raw-record equality: inventoryRow normalizes def/theorem/opaque
`all` to `[name]`. Trusted origin and serializer correspondence remain essential.
The cut induction then proceeds over the same basis.
Native deserialization remains trusted/memory-sensitive even if a later census
would reject a malformed object. This uses the EXISTING ordinary native trust
premises, but adds that path to the cut primitive; document/review it explicitly.
Hash identity alone does not prove this correspondence or create cold public trust.

## Protected metadata: cheaper checks without a daemon

Under approved owner code, immutable support, no whole-state rollback and serialized
mutation through the held owner locks, repeated identity-file/PK comparisons inside
every trie operation need not be the mechanism enforcing mathematical grounding.
Separate cheap budget/sticky-denial checks (optionally sampling WITHDRAWN) from
repeated identity/SQLite validation: validate
at opening, before worker launch, after clean completion and immediately before
commit; resolve/reopen validates anew. A sticky observed withdrawal remains fatal.
Keep exact selected frontier/freshness checks and transactional invariants.

The premise must say who can withdraw: if writers honor the held lock, identity
cannot change mid-operation. If a trusted out-of-band marker can appear anyway,
the last eligibility check must refuse it; no sampled design guarantees detection
of a write after that check before COMMIT. Future use must recheck withdrawal.
Do not silently promise instantaneous revocation or weaken that policy by calling
a startup observation permanently current. These boundary checks are simpler than
long-lived worker state, but trace counts do not yet justify a wall-time claim.

## Alternatives, cost condition and next investment

Native batching already amortizes basis restoration and checks many new units;
ordinary Lean/Lake is the main route to creative theory development. Prefer it
when work is available together or selected native roots remain small. It does
not remove growing-history restoration for independently timed durable events.
A stable in-process worker could reuse basis and semantics, but adds lifetime,
resource renewal, state contamination, support changes and crash/commit coupling.
It is a larger investment than one authenticated immutable fixed snapshot.

Let R be repeated checked seed reconstruction; H+D fixed snapshot hashing/loading;
V the retained fixed census; S selected semantics/interface work; N the new proof;
P support/controller work; C initial capture/storage cost. The cached route is
beneficial after k uses only if k[R-(H+D)-DeltaV-DeltaP] > C, with all terms in one
stated resource measure. Concrete rechecking, failures, custody and original
migration still count. Neither R > H+D nor dominance of R has yet been measured.
Against native reuse, also compare avoided ancestral restoration with extra
concrete reconstruction, interface processing and cut-index/custody costs.

Next: finish current evidence/audit, then root may select ONE source successor
binding only the already checked fixed basis, with metadata checks rationalized
under the explicit lock/revocation model. A later small matched discriminator
must exclude intrusive profiling from timing and include setup/census/support
costs; do not repeat the creative episode or run a broad benchmark. If this fixed
cost repair still has no plausible useful region over native batching/small roots,
shelve the accelerator. Public productization is NO-GO on current cost evidence.
