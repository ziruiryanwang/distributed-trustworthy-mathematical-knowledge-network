# Ordinary checking cost: source model and safe reduction

2026-10-06. Source/evidence analysis only. No product import, copied product,
execution, timing campaign or source mutation was performed. The previous
October 6 distribution is a **frozen baseline**, not a satisfactory or completed
v4. The resumed user milestone is October 6, 10:00 Chicago / 15:00 UTC.

## Decision in brief

The final receiving operation spent 18.25 encompassing child-Job CPU seconds,
but its actual guest worker spent 1.703125 seconds and the parent-receipt
verifier spent 0.015625 seconds. The recorded workflow controller spent
16.453125 seconds. Source identifies a concrete large avoidable term:
**seven installed-tree validations, hashing 5,185,224,379 asset bytes**, for a
269,356-byte received fragment. Five of those validations already restrict
hashing to the cryptographic runtime, but nevertheless walk the entire
12,398-file installation. Two other validations hash the entire 2.345 GB
installation, including unused native Lean authoring support.

This identifies a cost mechanism, not a measured attribution of every CPU
second. We have no phase profiler, so cannot claim that hashing alone caused
16.453125 seconds, or translate an eliminated byte fraction into the same
elapsed-time or CPU reduction.

Recommend first implementing an explicit **receiving-operation asset closure**,
not a theorem-success cache. Preserve fresh initial/final exact validation,
pre/post worker checks and all mathematical checks, but validate precisely the
installation files executable or readable by this operation. Refuse any native
worker in that mode. The largest reduction comes from making unused Lean
authoring assets nondependencies of receiving, not from trusting unchanged
timestamps. This requires a fresh source selection and independent review of
the closure/noninterference argument below; it is not yet implemented.

## Evidence and immutable baseline

Inspected actual files under
`product-local/v4-operator-integration-01/commons-v4/contributor/`:

- `cert_workflow.py`: Installed initialization/rebinding; check_fragment;
  group_parents; main/finalization.
- `cert_stages.py`: crypto_assets; Session rebind/invoke/write/observe;
  storage census.
- `cert_fragments.py`: load/bind/snapshot/export_plan/execute/export.
- `cert_bundle.py`: immutable byte containers and structural binding.
- `cert_capsule.py`: canonical inspection/schema loading.
- `profile.json`: exact immutable asset membership and byte counts.

Also inspected public `operator/commons_run.py`, retained inner command records,
and the already adopted `experiments/v4-package-01/RECEIVER-OUTCOME.md` and
`OPERATOR-OUTCOME.md`. The profile pin is
`298d790ec380f50ca45307069fd577908131a0622e57a3aa455813268213bfc7`;
the public result pin is
`bbaad539e4e84a4e11eb442d270d66ba7848f81ae713ade0ded4fa48d02d3752`.
All saved successes and failures stay frozen; this is not a request to rerun
them. Source identities are preserved by the baseline release manifest.

## Exact selected execution graph

The actual selected input has one certified frontier bundle. Its fresh
`check-fragment` path runs:

1. Parse externally pinned installed profile; allocate the durable invocation.
2. `Installed.initialize()` calls full `Installed.rebind()`.
3. `Session.rebind()` calls `Installed.rebind(crypto=True)`; the fresh state
   has no input/output pins yet.
4. Load and structurally bind the eight-file fragment; write its eight-file
   operation snapshot. Group and separately stage the parent capsule/journal/
   receipt (three more files).
5. Parent `verify` invokes one worker, with crypto installation rebinding and
   operation-pin rebinding both before and after it.
6. Construct and bind an export plan from the exact saved child bytes.
7. Full guest `execute-fragment` invokes one worker, again with crypto
   installation/operation rebinding before and after it.
8. Only after actual guest success, export the eight-file inert fragment.
9. The `finally` block calls full `Installed.rebind()` before reporting success.

Thus the exact installed rebind sequence is
`full, crypto, crypto, crypto, crypto, crypto, full`.
There are two real inner commands, not seven proof executions. The guest itself
authenticates the supplied receipt assumption; that security boundary is not
removed by the proposal. No new certificate was produced.

The public wrapper separately checks selected code/profile identities. Its
recorded 0.8125 seconds CPU is **outside** the 18.25-second public child Job;
it is not controller or guest work. The controller/worker sum is 18.171875
seconds, leaving 0.078125 seconds relative to the enclosing Job figure. Do not
silently attribute this small remainder or sum nested measurements twice.

## Byte/pass model

Let `N` be installed payload-file count; `B` their total bytes; `Nc,Bc` the
cryptographic subset count/bytes; `P` profile bytes; `k` selected parent
journal groups. These are installation quantities, not global-corpus size.
For the fresh checking path with one guest execution:

\[
  r_{full}=2,\qquad r_{crypto}=1+2(k+1),\qquad
  H=2B+(2k+3)B_c.
\]

Each rebind separately reads/hashes the profile; each currently traverses the
full installation. `Installed.__init__` additionally reads/parses the profile
and constructs its full path map once. Module loads re-read and hash their own
small source files, so `H` is deliberately the asset-rebind term, not every
byte read by the complete process.

Actual immutable-profile values:

| Quantity | Count/bytes |
|---|---:|
| All installed payloads `N` | 12,398 |
| Full installed asset bytes `B` | 2,345,416,272 |
| Ancestor directories implied by those paths | 343 |
| Existing crypto subset `Nc` | 602 |
| Crypto asset bytes `Bc` | 98,878,367 |
| Ancestor directories implied by crypto paths | 51 |
| Profile `P` | 1,881,622 |
| Two full-pass hash bytes | 4,690,832,544 |
| Five crypto-pass hash bytes | 494,391,835 |
| Sum `H` | 5,185,224,379 |
| Per-file hashing operations | 27,806 |
| Full-tree payload visits, seven traversals | at least 86,786 |

The walk also visits directories/profile and rejects special/reparse entries.
Every selected file hash additionally resolves/checks its path and stats it;
therefore the metadata term is substantial independently of byte throughput.
The two full passes are **90.4654%** of `H`. Removing only the five repeated
crypto hashes saves at most 9.5346% of this byte term and leaves both full-tree
hashes. Such a cache alone is not the central remedy.

The largest crypto assets include the 66,458,624-byte checker executable,
6,778,592-byte Python DLL, 6,242,552-byte libcrypto DLL and 1,418,472-byte guest
image. The selection deliberately retains the full bundled Python runtime;
this proposal does not attempt fragile per-import standard-library pruning.

An explicit crypto-only scope at all seven boundaries would give:

\[
  H' = 7B_c = 692,148,569\ \text{bytes},\qquad
  1-H'/H = 0.8665152135\ldots
\]

That is an **86.6515% source-derived reduction in asset bytes hashed**, not an
86.6515% measured runtime speedup. A matching projected tree walk could reduce
each walk from the full tree to 602 files/51 required ancestor directories,
plus the profile and explicit excluded-subtree boundary checks. Actual entries
remain a checked quantity, not assumed equal to a formula in hostile storage.

A transparent cost model is

\[
 C = C_{bootstrap}(P,N) + \alpha H + \beta M
     + C_{data}(S,R) + C_{workers} + C_{supervision},
\]

where `M` counts path/metadata checks, `S` is operation data size, `R` repeated
pure transforms, and nonnegative coefficients depend on the host/filesystem.
The source proof reduces `H` and `M`; it supplies no calibrated values of
`alpha,beta` and therefore no experimentally established end-to-end speed ratio.

## Smaller repeated data work

The source received fragment is 269,356 bytes. Its eight-file snapshot plus
the three separately staged parent files totals 498,733 bytes. The parent
worker's four records add 1,891 bytes, and the guest worker's records add
2,474 bytes. The operation-pin rebind passes therefore hash

`0 + 498733 + 500624 + 500624 + 503098 = 2,003,079 bytes`.

There are 19 snapshot/export writes (eight input, three staged parent, eight
export), each flushed/fsynced, pinned and followed by an operation storage
census. There are 28 statically required `observe` calls on this path, plus
live-worker polling observations. The final report becomes the 28th state pin.
Storage polling is sampled cooperative accounting, not a hard disk quota.

At the top-level binding call graph, the single parent undergoes structural
bundle binding twice during `load` (the outer load and then fragment binding),
ordinary capsule/journal validation again in `group_parents`, and structural
bundle binding again in `export_plan`. The child capsule/packet binding occurs
both at load and export-plan construction. Each canonical capsule inspection
can recurse over its two definition capsules, reconstruct graphs, load schema
bytes and serialize commitments. These are genuine pure duplicates, but they
operate on kilobytes here; do not prioritize them above multi-gigabyte asset
rehashing without stronger evidence.

Input snapshotting, fresh guest execution, exact export equality and durable
failure records are essential boundaries. Eliminating snapshot/export copies
would be a different protocol change and is not selected by this analysis.

## Proposed minimal source change: explicit action-scoped adoption

The existing `crypto_assets` predicate already excludes `runtime/lean/**`,
`native/**`, the support-plan file and seed-inventory file, while retaining
all other assets and required cryptographic roles. Reuse that reviewed set
definition rather than inventing a per-example list. However, membership alone
is insufficient: its current walker still inspects the whole installation.

The smallest useful successor should:

1. Give `Installed` a fixed invocation scope selected by the public action,
   initially only `check-fragment -> crypto`; all authoring/advance modes
   remain full. Extending to source-free `prepare-seal` is an independent
   mechanically similar candidate, not necessary for the first change.
2. Validate the adopted profile schema/digest/full map as before, then derive
   the exact selected asset names and permitted directory projection once.
   Persist neither a success token nor a disk hash cache.
3. Perform fresh initial and final exact byte/path validation of that complete
   selected closure. Keep its per-worker pre/post validation too initially.
   Prune only explicitly excluded subtrees after checking their boundary is an
   ordinary directory. Never follow a symlink/reparse point to bypass selection.
4. Reject unknown files/directories in the executable/readable projection;
   distinguish deliberately uninspected native subtrees from approved input
   files. Document that a crypto-only operation no longer certifies health of
   unused authoring files. The full action still detects their corruption.
5. In the receiving scope, forbid `Session.invoke(native=True)` before any
   worker creation and forbid expansion to a broader asset scope later in the
   same invocation. Worker PATH must retain its existing native-directory
   exclusion. All direct module/data loads must lie in the selected closure.
6. Preserve all input bindings, receipt checks, full guest execution, exact
   output checks, finite allowances, lifecycle cleanup and status semantics.

Likely changed product files: `contributor/cert_workflow.py` for scope and
projected installation adoption; `contributor/cert_stages.py` for explicit
native/scope guard and sharing the derived closure; `CONTRIBUTOR-API.md` for
the acceptance/installation-health distinction. The selected successor profile,
manifest and public launcher's embedded profile binding must be regenerated
by the normal root-owned packaging process, not patched in the frozen baseline.
`cert_capsule.py`, `cert_bundle.py`, `cert_fragments.py`, the checker executable,
guest image, foundation and Lean semantics need not change for this first seam.

### Conditional noninterference theorem

Let `E` be the action's complete executable/readable installed-asset closure,
`I` its immutable candidate inputs, and `O` the trusted OS/runtime behavior.
Assume the selected program can obtain installed data/code only through `E`,
all accesses to `E` use the externally selected pins at the existing adoption
boundaries, and no native/wider action is callable in this scope. Then two
installations equal on `E` and `O`, with equal `I`, have the same program
transition relation and mathematical acceptance outcomes regardless of their
bytes outside `E`.

Proof: induction on program transitions. Ordinary computation depends only on
the previous state. Each installed read/load has its path in `E` by closure
and yields the same selected bytes; candidate reads are equal by `I`;
OS-mediated steps have the same modeled behavior by `O`. Therefore corresponding
states and acceptance predicates coincide. No statement says omitted files
are correct or even healthy. That stronger installation-health property is
intentionally not a precondition for this receiving-only operation.

The remaining engineering obligation is to establish that `E` is actually
closed for this program/platform, not merely to assert the theorem. In source,
the receiving branch uses no native code path; all explicit local modules,
registry/schema/foundation witness, Python runtime, checker and image are in
the existing crypto subset. The worker's nonnative PATH excludes Lean/native.
Windows DLL resolution and trusted OS behavior remain explicit assumptions,
as in the baseline. This report is not a binary dependency-closure proof.

## Safe operation-local reuse invariant

This is useful for the smaller pure duplicate transforms, but should not be
confused with an installed-file cache or receipt-verification cache.

Define an operation-local context `K=(profile_digest, schema_bytes,
registry_bytes, input_bytes...)`. A memo entry may be reused only when:

- every component read by the pure deterministic transform is in the key;
- key bytes are immutable captured values, not a pathname/stat/mtime surrogate;
- the fresh call compares complete bytes to the key, or uses the project's
  already stated collision-resistance assumption explicitly;
- outputs are immutable bytes/frozen values, or returned as fresh decoded
  objects so caller mutation cannot poison a later result;
- the cache is bounded/charged and dies with the invocation;
- a later process, resumed invocation or changed profile cannot import it as
  authority; it never suppresses actual receipt or guest checking.

For deterministic `f`, if `x=y` as complete immutable inputs, `f(x)=f(y)`.
Replacing the second computation by the first immutable result is therefore
observationally equivalent at that call site. Induction permits finitely many
such replacements. This is a local computation-sharing theorem, not a theorem
that a path still contains the same bytes, that a mutable Python dictionary is
unchanged, or that another node must trust a local execution result.

A possible later implementation can cache structurally bound bundle/capsule
results on retained exact byte tuples in `Session`, while keeping `LoadedBundle`
public constructors untrusted. A caller-supplied `binding_bytes` must never
qualify as a trusted memo entry. Do not add this optional cache merely to make
the patch look broader; first remove the identified dominant installation term.

## Mutation, failure detection and TOCTOU

Do **not** replace rehashing of mutable path-backed executables by a dictionary
of path/size/mtime or by an in-memory “already verified” set. Equal metadata
does not imply equal bytes. Initial and final checks alone also cannot detect
a malicious edit-and-restore between checks. The current baseline itself is
not an atomic filesystem snapshot or a hostile-owner sandbox; repeated hashes
do not prove continuous immutability.

This proposal preserves fresh checks for every selected byte at existing
boundaries. It changes the declared dependency set, not the strength of checking
selected mutable bytes. Same-user hostile mutation, OS/DLL compromise and
atomic snapshot semantics remain outside the existing cooperative-host threat
model. If stronger continuous immutability is desired, a separately designed
read-only snapshot/lease or handle-based access mechanism is required; no
unproved security claim may be borrowed from a stat cache.

All refusal paths must close workers, retain charged work and record the
original failure. A final selected-file mismatch must prevent a success status
even after a guest ran successfully. A changed omitted Lean file is irrelevant
to crypto-only acceptance **only** under the closure guard; it must still be
detected by a full/native invocation.

## Required changed-boundary tests before adoption

Use native-free fixtures/mocks for the new source first; do not rerun old proof
campaigns. Test the distinct obligations:

1. Exact scope derivation agrees with existing `crypto_assets`; required roles,
   schema, registry, foundation witness and full Python runtime are included.
2. Initial/final selected code, image, registry, DLL and profile corruption is
   rejected, including same-length modifications; no metadata-only cache hit.
3. Missing/extra selected files, unexpected directory entries, reparse/symlink
   boundaries and path escapes are refused before worker execution.
4. Omitted Lean/native bytes are not read/hashed/walked in receiving scope;
   change there does not invalidate that explicitly scoped operation. Full
   authoring mode still validates them and refuses their corruption.
5. Native invocation or late scope escalation from a receiving context fails
   before a subprocess; arbitrary candidate bytes cannot select native scope.
6. Count exact installation passes and byte sums with reader instrumentation
   in tests. Assert unchanged input/receipt/guest calls, not merely lower counts.
7. Selected mutation after an initial pass and before worker/final adoption is
   detected; completed guest work cannot override final failure. Preserve
   cleanup/accounting and all original errors.
8. If pure memoization is separately selected: changed profile/schema/registry/
   member/input never hits; mutable outputs cannot poison future calls; public
   caller-forged bound containers do not confer cached authority.

Only after source review should root select one fresh public receiving operation
for unchanged exact mathematical bytes through the successor. It qualifies
the changed real path, not a universal performance ratio. Static pass/byte
reduction is already theoretically quantifiable; a broad timing campaign is
unnecessary for deciding whether to implement this seam.

## Release consequence and limits

Ordinary users should pay for the checking machinery and exact selected proof
frontier, not repeatedly read an unrelated authoring distribution. Making that
dependency boundary explicit advances scalable reuse without weakening proof
trust or introducing human-intention criteria. It does not solve global
discovery, compositional-definition limits, proof-frontier growth, sustained
custody economics or net useful-growth justification. Those remain distinct
central workstreams; this analysis does not relabel the frozen baseline as v4
success or claim the broader goal complete.
