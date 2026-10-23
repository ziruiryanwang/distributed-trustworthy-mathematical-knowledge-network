# Protected local mathematical state: concrete restart boundary

2026-10-22. `lean_persistence_boundary`. Source/theory only; no test, build,
runtime import, product edit or Git mutation. Canonical project root only.

## Decision

Use **checker-generated local Lean module snapshots plus a protected local
acceptance catalog**, not serialized operational handles, arbitrary peer `.olean`
files, or an always-on daemon as a prerequisite. The pinned Lean runtime already
has the relevant serialization/import APIs. A daemon may later amortize measured
startup cost, but is not needed to avoid repeated mathematical proof checking.

This recommendation is conditional on the acceptance lane's separately reviewed
canonical initialized basis and checked declaration adapter. The exact missing
software is a small local persistence owner and Lean snapshot wrapper; this note
does not claim those components already exist or have been qualified.

The practical compromise is explicit: restarting loads the selected environment
and its local imports. It does not re-prove them. This is not constant-time
restart, zero disk traffic, or free first-time library onboarding. An unrelated
fresh reader cannot inherit this local acceptance merely by copying the files.

## Actual implementation seams

The authoritative ordinary-source map is
`experiments/v5-local-checks/distribution-candidate-preflight-01-input.json`.
The following three selected paths were compared against its SHA-256 fields;
all match. Later producer assembly preserves this ordinary source set.

| Existing seam | What it actually does; consequence |
|---|---|
| `software/v5/continuing_context/client/workspace_atomic.py:163` | `Workspace` owns an OS lock and SQLite operation ledger. At open it marks old `GRANTED`, `OPEN` and `FAILED_PENDING_CLOSE` operations interrupted. `reserve` creates a fresh process-local `OperationGrant`. Reuse this separation and transaction pattern; do not make its historical records into mathematical authority. |
| Same file, `:304`, `:329`, `:447` | Saved record reads explicitly grant no authority. Closing removes grants; live warrants bind current client handles. A new persistent judgment API is required, not a flag that makes historical operation results authoritative. |
| `software/v5/incremental_native/mixed_claims/receiver.py:78`, `:118` | `_native_memo` is a private same-owner observation cache; `_revoke` clears it with handles and receipts. It records conditional checker observations, not independently established premises. Persisting this dictionary would not establish unconditional facts. |
| `software/v5/validation_phase/admission/trust.py:170` | `TrustDomain` persists exact local stack adoption and a sticky `WITHDRAWN` marker. Its docstring explicitly trusts the owner/controller/OS/filesystem and does not claim protection against whole-directory rollback. It stores no accepted mathematics. |
| Same file, `:65` | The support schema is specifically coupled to relation/aggregate images, a foundation, policy and `resolved-succinct-poseidon2`. A broad native-Lean profile must have a distinct adoption schema; do not invent irrelevant zk identities to pass this validator. Reuse the withdrawal pattern, not the wrong profile vocabulary. |

Selected source hashes:

- workspace: `32e3b95ea2e6d3f8dc35d63000728e9e075a16de3e13fb1a0b718bce45e11773`.
- receiver: `5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b`.
- trust: `c997d2a83ae5246dec9ff30eeca72e405ec0f66c0a307e53e0521eef66fae6d0`.

## The existing Lean APIs and their limits

Source below is the retained
`software/runtime/lean-4.34.0-windows/src/lean/Lean/Environment.lean`.

1. `Environment.addDeclCore ... (doCheck := true)` at line701 enters the
   checked constructor. `Kernel.Environment` has a private constructor; this
   is not a license to manufacture constants through arbitrary `ConstantInfo`.
2. `Environment.setMainModule` at1183 changes the local module identifier.
   Snapshot module identifiers can be unique storage names while mathematical
   declaration names remain unchanged. There is no need to rewrite ordinary
   theorem namespaces into content-hash namespaces merely for persistence.
3. `mkModuleData` at1857 serializes the stage2/current module's constants, with
   private-level output preserving kernel constants, including hidden generated
   auxiliaries. It obtains the completed checked kernel environment through
   `toKernelEnv`, rather than merely the asynchronous frontend signature map.
4. `saveModuleData` at1792 and `readModuleData` at1795 use the native compacted
   representation. `writeModule` at1901 is the standard higher-level writer;
   its module-system mode may produce several `.olean*` parts. These are real
   available APIs, not a proposed new binary serializer.
5. `importModules` at2438 accepts `plugins := #[]`, `loadExts := false` and
   explicit `arts : NameMap ImportArtifacts`. `Lean/Setup.lean:69` defines
   `ImportArtifacts`; its two arrays enumerate `.olean*` parts and IR parts.
   A checker-local legacy/non-`module` snapshot can use one `.olean` part and
   an empty IR array. This is a local storage representation, not a requirement
   that users abandon Lean's module system in their authoring projects.
6. `finalizeImport` at2307 builds the constant map directly from module data.
   **It does not kernel-check every imported theorem even at trust level0.**
   `loadExts := false` prevents extension initialization but does not turn the
   unsafe binary loader into an untrusted-data verifier.

Consequently the restore API is admissible only for bytes created by our own
trusted snapshot writer after successful checked admission, authenticated to
our protected local catalog, and loaded with the matching pinned runtime.
An upstream compiler's successful exit, a peer's manifest, a matching public
content hash, or an ordinary source project's `.olean` directory is insufficient.

### Concrete quotient hazard, not a generic caveat

`finalizeImport` sets `quotInit := !imports.isEmpty`, assuming the import closure
includes Lean's proper quotient initialization. Therefore a prelude-free local
environment with `quotInit = false` must **not** be serialized and restored via
this ordinary import route as though nothing had changed.

The selected broad profile must start from the exact canonical initialized
basis, with the quotient quartet generated by the checked `.quotDecl` operation,
and record `quotInit = true`. The acceptance agent located the existing
`BootstrapSupport.receiveSeed` route and
`software/assets/foundation/seed-verified.json`, SHA-256
`a0acdc706f5e42dca21950c14db2307a18955c63ff953019aaff413d0a976001`.
Root must select and review reuse of that basis; this cross-agent pointer is not
new execution evidence. Canonical builtin meanings also matter, since Lean
reduction recognizes certain builtin names. Do not use a policy that merely
allowlists those names while permitting their definitions to change.

On this initialized profile, restoration's quotient bit matches the warranted
pre-save state. Supporting genuinely prelude-free profiles requires a different
restore constructor or a separately justified adapter, not a permissive default.

### Keep authoring and acceptance state separate

Only the checked admission process creates snapshot data. Do not snapshot the
ordinary source frontend environment: it may contain unchecked declarations,
authoring assumptions, arbitrary extensions or executable metadata.

The local writer should retain the accepted kernel declaration data and exact
imports, with no peer extension entries, plugin list, IR or initializers. Use
private constant data, not exported theorem-as-axiom approximations. An explicit
empty extension-entry argument to `mkModuleData` can avoid exporting elaborator
convenience state; final wrapper review must verify the produced `ModuleData`
census and imports. Preserve proof values in the initial implementation. Local
proof-body elision may be possible, but requires a new assurance bridge and is
not needed to stop replay.

There is one incremental-writer detail to implement deliberately: stage2 is
"since import", not automatically "since the previous catalog commit". Calling
`writeModule` after every commit in one still-live environment could duplicate
earlier local declarations. For each chunk, the trusted wrapper must use the
exact new kernel-name census from successful checked insertion (including
generated auxiliaries), obtain those `ConstantInfo` values from that checked
environment, and construct a `ModuleData` with exactly those constants, the
protected parent-module imports, empty extension entries and empty extra IR
names. `ModuleData` is the existing public data structure at lines108-129;
`saveModuleData` can persist it. Alternatively, restore the last committed
module before using the standard stage2 writer, but that incurs a new import
and is not the recommended per-commit path. In neither case may caller-supplied
constant values substitute for the values obtained from the checked environment.
The snapshot wrapper is therefore small but not a one-line `writeModule` call.

On restore, provide the complete selected import closure in `arts`, with exact
locally recorded artifact paths and empty IR arrays. Missing entries must cause
our wrapper to refuse before calling Lean. The upstream import loader otherwise
falls back to `findOLean`/the search path when a module is absent from `arts`.
An accidentally omitted binding could therefore load an unrelated project file.
Generate the closure from protected local records, not peer-provided filenames.

Elaborator instances, notation and tactics stay in the ordinary owner-controlled
authoring project. They are not mathematical authority. The separate workflow
adapter must bind the exported proof data to the exact checked semantic
environment; these persistence snapshots need not recreate all editor state.

## Small public contract

The preservation argument is an induction, conditional on the selected Lean
kernel and serializer/runtime behaving as specified. Let `Valid(P,E)` mean that
E's declarations are warranted under the stated basis and support assumptions.
Checked insertion establishes `Valid(P,E) -> Valid(P,E+D)`. The local writer
serializes precisely the new accepted constants D and the protected E import
bindings; the restore wrapper reconstructs those same constant bindings and
quotient state without admitting other constants. Therefore restore preserves
the already established judgment. It is not a fresh proof of `Valid(P,E+D)`
from peer bytes. The trusted serializer's round-trip property is an explicit
implementation assumption to target with focused checks, not a theorem proved
in this note.

Lean's ordinary importer allows some overlapping theorem declarations through
`subsumesInfo`, without requiring identical proof values. Our initial snapshot
writer should not rely on this broader merging policy: imports must share
already identical parent module identities, and newly persisted names must not
overwrite any parent binding. Independent incompatible branches are isolated
until a separate compatible-merge operation is justified. This avoids silently
using importer conveniences as a proof of environment identity.

The following API names are proposals, not implemented claims:

- `open_library(profile, basis, store)`: acquire the local owner lock; open the
  exact protected catalog; validate the selected profile/basis adoption and any
  dependency support withdrawals. Do not resume any old operation grant.
- `restore(root, new_grant)`: select the finite accepted snapshot closure;
  validate its files and support lineage; import only those protected artifacts;
  return a fresh `LocalEnvironment` handle owned by this live process/grant.
- `check_extension(environment, inert_declarations, new_grant)`: perform the
  separately specified checked Lean extension. Neither decoding nor existence
  of a file in custody is sufficient. Reject overwrites/incompatible identities.
- `commit(environment, checked_extension)`: serialize only the accepted delta,
  publish its local catalog record atomically, then return its durable root ID.
- `close`: destroy live handles/grants; retain committed mathematical artifacts.

The durable catalog minimally binds:

`root ID, native profile ID, exact basis ID, parent/import root IDs, mathematical
declaration binding, snapshot module name, ordered artifact lengths/digests,
quotient state, assurance support set, writer/format version, committed status`.

Artifact digest identity and mathematical identity remain distinct: serializer
version changes need not create a new theorem, but old native snapshots must not
be loaded under a new runtime merely because their theorem names match.

The catalog has exclusive trusted local write authority. Network custody files
and ordinary research logs are never this catalog. A copied `PASS.json` cannot
be promoted through a public `restore` endpoint. There is no endpoint accepting
arbitrary `ConstantInfo`, raw module bytes or a user-asserted `verified=true` as
authority. Accepted inert proof data remains exchangeable through the network;
local snapshots are acceleration state, not transferable mathematical evidence.

## Transaction and crash state machine

Reuse the existing single-owner OS lock and SQLite `synchronous=FULL` transaction
pattern; no second database engine or distributed commit protocol is necessary.

1. **Reserved:** obtain a fresh finite operation grant and reserve disk quota.
   Parent roots must be committed and eligible under current local policy.
2. **Checked, uncommitted:** the checked extension exists only in memory.
   No public accepted root refers to it yet. Failure here loses optional work,
   not soundness or an already committed parent.
3. **Materialized, uncommitted:** write fresh immutable artifact paths, flush
   them, record exact lengths/digests, and verify the writer's finite manifest.
   Paths are not reused or overwritten. These files remain unreachable as
   accepted mathematics if the process fails before catalog commit.
4. **Committed:** after final support/policy eligibility checks, insert artifact
   and parent bindings plus the accepted root in one SQLite transaction. Only
   after commit return the root as durable. Do not serialize the current grant.
5. **Restored:** a later operation with a new grant loads the committed root;
   it never renews old budgets, deadlines, handles or network capabilities.

At restart an absent catalog record means staged files have no authority. A
committed record whose selected files are absent, partial, corrupted or
incompatible is unavailable and must refuse before unsafe import. It is not
silently repaired from a peer `.olean`. The controller may later regenerate
the cache by checking the preserved inert evidence through a fresh operation.
An acknowledgment lost after commit is handled idempotently by the exact root
ID: inspect the existing complete record, not re-run checking automatically.

Store admission and publication are distinct transactions. A failed network
advertisement does not undo a local mathematical fact or justify repeating its
proof. Store quotas can refuse new commits without invalidating old facts.
No garbage collection is selected here; later deletion must retain or explicitly
retire dependents and never silently break accepted-root restoration.

## Realistic trust, integrity and cost

The trusted computing base includes the pinned Lean kernel/runtime, bounded
decoder and controller, snapshot writer/reader, the local owner account and OS,
and protected storage integrity. The adversary controls peer data and replies,
not arbitrary writes to the trusted catalog or snapshot directory. Parent path,
ordinary-file and no-redirection checks follow existing local patterns. The
owner lock serializes supported writers; it is not a defense against an already
compromised owner account. Do not turn this feature into a machine-attestation
or anti-administrator project.

Before first mapping a selected snapshot into a fresh process, check its length
and digest against the protected catalog; do not parse unverified native binary
data first. Keep immutable selected artifacts stable during validation/use.
This catches accidental corruption under the cryptographic hash assumption,
while trusted storage excludes hostile concurrent replacement after the check.
If that exclusion is unavailable, path checks alone are insufficient: a stronger
handle/locking/mapping boundary is needed before calling the unsafe loader.

Hash selected local modules **once per process acquisition**, not once for every
lemma application or every `_active` guard. The process can retain a map of
verified immutable loaded artifacts. Do not rehash every unrelated file in an
entire compiler/distribution installation on each mathematical operation. The
exact installed checker profile is adopted at installation/startup, and local
withdrawal remains a small policy check. This changes the operational pinning
contract and must be deliberately selected; it is not an in-place relaxation
of already frozen guards.

For a fresh process using local closure C and new declarations D, the intended
cost is `read/hash(C) + import_metadata(C) + check(D) + persist(D)`, not
`check(all ancestor proofs in C) + check(D)`. Existing Lean import constructs
the selected constant map and retains proof/body representation; it is not a
proof of O(new declarations) restart. Within one process, repeated operations
may reuse its already loaded immutable environment. If measured restart cost
dominates ordinary use, a bounded process-level service is a justified next
optimization: it keeps the same durable roots but issues fresh per-request
grants. It should not become a prerequisite before the simple route is usable.

Power-loss guarantees are limited to the selected filesystem and SQLite flush
semantics. File-before-catalog ordering plus validation gives fail-closed
recovery, not a claim of perfect hardware durability. Whole-store rollback by
the trusted owner/OS, loss of every copy, and host compromise are not solved by
these local records. Those exclusions match the existing TrustDomain model.

## Withdrawal and cross-profile soundness

Each accepted root retains the **actual assurance support set**, not just the
current writer's native profile. A root obtained by locally checking a theorem
against a certified imported premise still depends on that premise's certificate
checker, relation/semantic bridge and foundation policy. Saving the resulting
Lean environment does not erase those assumptions.

At commit, compute the union of parent supports and the new checking supports;
store this immutable union in protected state. At restore/action boundaries,
require every member eligible. This checks distinct support profiles, not every
ancestor proof. Start conservatively at snapshot granularity: withdrawing any
support used by a snapshot blocks it and dependent snapshots. Independent
unrelated roots with no such support remain usable. Fine-grained declaration
salvage can follow only if it becomes a measured need.

The first broad-native persistence implementation should support the fully
native checked-basis lane only. A certificate-to-broad-native bridge is a
separate reviewed input adapter. It may later introduce conditional interface
assumptions only with preserved warrant correspondence and lineage. Conversely,
an ordinary local snapshot must never produce an old exact-J receipt claim.

Merely recompiling the new theorem does not remove a withdrawn support if it
still assumes the same imported premise. A fresh independent proof/check of
the relevant closure can produce a new lineage; a change of labels cannot.
Kernel or policy upgrades require explicit revalidation/migration, or an
audited compatibility argument, before old binary snapshots become eligible.

## Minimum implementation decision for root

Select one fresh native-library source seam after acceptance and workflow notes
agree: exact checked basis; inert checked extension; local snapshot writer;
catalog commit and fresh restore. Use an existing useful Lean development, close
the first process, restore in a second, check a substantive new extension, and
test the specific negative boundaries (foreign `.olean`, wrong basis/profile,
missing import binding, corruption, incomplete commit, withdrawn support,
expired grant). These are future selection criteria, not permission to launch
now and not a reason to rerun a cryptographic campaign.

The crucial design issue is resolved in principle: persistence does not need
another prover, arbitrary peer binary trust, an always-running service, or a new
universal theorem checker. It needs a narrowly trusted writer/restore path that
preserves the judgment already established locally, with explicit startup and
lineage costs. Final v5 and broad compatibility remain unproved until integrated
software and the representative reciprocal workflow actually satisfy them.
