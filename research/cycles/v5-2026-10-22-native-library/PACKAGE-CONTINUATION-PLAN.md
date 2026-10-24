# Minimal package and public-workflow continuation

2026-10-24. Initial source-only assessment by `package_continuation`; no product
code, installation, accepted state or experiment was changed or executed during
that assessment. Root subsequently selected the narrow source continuation in
RETAINED-CONTINUATION-SELECTION; its authored adapters are recorded below.
Runtime requires a separate root selection. This note addresses the bounded
unfinished ordinary-reference integration, not a new growth campaign.

## Recommendation

Use a **file-only exact successor of the already assembled reference package**,
then run only the six remaining public operations against the existing owner.
Do not repeat initialization, library intake, helper compilation, the earlier
correspondence diagnostic, or the original snapshot copy.

The retained-snapshot continuation needs a small, separately reviewed product
change: the current store requires the snapshot to be under the newly reserved
operation. Merely shipping `reference_store02.py` fixes the census defect but
does not supply this continuation. Coordinate that seam with
`RETAINED-REGISTRATION-CONTINUATION.md`; do not pretend a file-only package change
has solved it.

## What can be retained exactly

The predecessor is
`experiments/v5-local-checks/ordinary-reference-assembly-01/package`.

| Identity | Exact value |
|---|---|
| PROFILE SHA-256 | `2d965cb67cb6729dfe42380146377bb1ab85ef42713c1de3f6668da09ba2fb13` |
| ASSEMBLY SHA-256 | `ae7ff57af40576ca2b7683baf188d366f3803b5c3e44f7a72f0f25540ef81671` |
| Installation manifest SHA-256 | `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2` |
| Implementation ID | `fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df` |

The assembly receipt records **165 payload files, 57,976,127 payload bytes and
137 profile entries**. With PROFILE and ASSEMBLY there are 167 installed files.
This is not the much larger protected library snapshot. A bounded exact package
copy is therefore a modest implementation cost; introducing overlay search paths,
symlinks or hard links would add a larger trust/layout change. Existing loaders
explicitly reject redirected paths and multiply linked files.

Preserve all installation payloads and all native helper/source bytes. No native
build is needed for a Python bookkeeping or retained-snapshot lifecycle repair.
Preserve the distinction between legacy `reference/helpers` and ordinary
`authoring/helpers`; overlapping module names are not interchangeable.

The current owner can reopen the same catalog after such an upgrade in principle:

- `owner.py` validates ADOPTION against the installation's implementation claim,
  store identity and stored limits, not the outer package directory or PROFILE
  digest.
- `reference_store.open_for_owner` binds STORE to adoption/activation, semantics,
  foundation, implementation and limits. The marker does not include support ID.
- Each reference record *does* bind support ID. The changed store source, and any
  changed registration/owner source, produce a new support ID. Do not retain the
  old support ID by relabeling changed source.
- The current records directory is empty. Thus there are no accepted reference
  records needing source-support migration. Closed failed operations may retain
  their old support ID: the store census checks its shape but does not demand it
  equal the current support ID.
- Accepted mathematics is already in the underlying owner catalog. It is not
  conferred by the new package, assembly receipt or old workflow report.

## Smallest file changes

For the census repair alone, the only changed installed payload is logical
`reference/reference_store.py`, selected from reviewed `reference_store02.py`.
`profile.py` need not change: it already recognizes that logical module, and its
exact pin belongs in the new PROFILE.

For retained-snapshot continuation, the likely minimal changed installed set is:

| Logical installed file | Necessary reason |
|---|---|
| `reference/reference_store.py` | Reviewed census repair plus explicit protected retained-snapshot binding, if selected |
| `reference/reference_registration.py` | Build a current warranted request and perform a new live match against the retained snapshot |
| `owner.py` | Expose an explicit owner-selected continuation argument/operation, if needed by that design |

Keep the existing logical names so the loader and module census remain unchanged.
The exact retained-snapshot API and record/path rules require the other source
assessment before these are treated as a selected edit list. In particular,
current `bind_reference_inputs` demands `snapshot.directory == grant.directory /
"snapshot"`, and current record parsing binds snapshot metadata paths to the
record's operation. A controller-only call substitution would not be sufficient.

Root-owned fresh assembly/selection adapters can derive from the existing
file-only patterns but should start at the **retained assembled package**, not
repeat `assemble.py`'s entire historical build-provenance chain. Preserve the old
receipt as pinned provenance. A new receipt should record the exact base,
overlays, changed/unchanged census, installation identity, copy bytes and
`ASSEMBLED_NOT_ADOPTED`; it must not claim a native build or mathematical check.
The package descriptor remains `DMKN_ORDINARY_OWNER_PROFILE_V1` if its schema and
payload set do not change. The new assembly receipt can use an explicit successor
schema rather than falsify the old assembler's fixed 31-added/132-unchanged claim.

Minimum file-only algorithm:

1. Pin the exact retained PROFILE, ASSEMBLY and all selected payloads; validate
   complete source census and no redirected/multiply linked paths.
2. Resolve the independently reviewed overlay map from logical names to fresh
   source successors; reject every unexpected addition, removal or change.
3. Copy retained/overlaid files to a fresh package with exclusive creation, bounded
   streaming and per-file destination verification. Do not touch the old package.
4. Keep the installation manifest bytes and installation map exact. Revalidate
   selected input pins after copying. Refresh only the overlay pin entries in
   PROFILE. Commit new assembly metadata and then PROFILE last.
5. Report the actual exact file delta. A completed copy establishes byte identity,
   not compatibility or acceptance; those belong to source review and the later
   public operation.

No product imports, catalog opens, native calls, project builds or snapshot copy
belong in this file-only step. It should fit the already modest assembly envelope;
root should select a finite cap from the actual finalized adapter, not renew the
old completed operation.

## Six-call continuation, not an eight-call restart

Use the catalog, custody, store identity and already created fixture files under
`experiments/v5-local-checks/ordinary-reference-public-workflow-01/workflow` in
place. Keep its failed WORKFLOW and original calls untouched. The old WORKFLOW
hash is `b99ae315a7f17cf5df9019d739f0d6577c65df929bdb8044bec42cbbd2a81734`.

The retained accepted roots are:

- Basis: `138c02d2de87fcc82cdfd11ac292ee9a9fb2ff41761f00174c6793337f1f8ee4`.
- Six-unit intake: `72b399a0e3ad4a1673ec369115c255dd0f3016ae2956572c5def4ce1081f96b1`.
- Store ID: `0096ade6422b06862c21d8f051a0c3d714ef65aec6f2607a2941443741c138c8`.

New logs and authoring outputs go in one fresh continuation directory. Do not
copy the catalog, derive a new store ID from the new output path, or run `init`.
The fixture paths and custody limits can be reused as explicit pinned inputs;
the new delta target list is produced only after A actually succeeds.

| Call | What it must establish |
|---|---|
| Registration continuation | Open current owner under lock; current request/support and actual new native correspondence; record-last registration of the retained snapshot |
| Author A | Existing notation/ordinary source works; A's two results are actually admitted over the retained intake root |
| Export delta A | Only A's new units are materialized; the original library is not replayed as a new mathematical contribution |
| Author B | B imports the generated delta and original library, actually uses A and the original checked law, then is admitted |
| Compiled-sorry refusal | The bad source really compiles; extraction rejects its `sorry` dependency before admission |
| Final status | Exactly the retained basis/intake plus A/B roots remain, including no root from the refusal |

This preserves the substantive original assertions. The controlled Flag example
still proves interoperability, **not growth or final-v5 deployment**.

The fresh harness must explicitly adapt the following old constants/invariants,
not merely rename its output:

- Package path and PROFILE/ASSEMBLY receipt schema/pins.
- Six-call CAPS and refusal index (old zero-based index 6 becomes 4).
- Separate retained state/fixture paths from fresh logs/output paths.
- Seed the expected root chain with the two retained roots; do not fabricate new
  init/intake public results. Current owner checks, not those constants, determine
  actual authority.
- Validate retained snapshots/failure provenance only as input identity/history.
  A saved correspondence result must not substitute for the live event.
- Retain `public_workflow02.py`'s distinction between clean process exit and
  expected exit code, including preservation of partial replies/accounting.
- Require exactly six current calls and four total roots at the end. Failed
  original costs remain charged historically; current inclusive Job CPU must not
  be double-counted with its nested controller/native reports.

There is no need for an extra status-only warmup: the first real owner operation
already validates catalog/context under lock. Add such a call only if finalized
continuation semantics uncover a specific unresolved state question.

## Decision boundary

Package relocation with identical underlying installation is source-supported.
The absent reference-record case makes a source-support upgrade particularly
simple. But snapshot retention is **not** already supported by the frozen product
API. Root must select and review that seam before assembly or execution.
If its implementation balloons, compare its maintenance cost against a simpler
explicit bounded alternative instead of turning one failure into a generalized
recovery framework. This note authorizes neither alternative and claims no
runtime success.

## Selected source authoring completed, not executed

Following root's explicit source selection, four fresh files were authored under
`software/v5/ordinary_reference_package`:

| File | SHA-256 |
|---|---|
| `assemble02.py` | `ad4a10722697308d3749d09465213b3d5ce17735a48980287f5216830c94e2ba` |
| `select_assembly02.py` | `950b038733233158849f99a2d85fa2f706c8e571fab22f98b6d53e54ed6cabb4` |
| `public_continuation.py` | `52314e90d362c4626187be0acced825e4622b9bf4708253f967e6c2a28be833a` |
| `select_public_continuation.py` | `0f328e7c0cecb06e92d240ae696559978bb2f1f29e994702119be6fbe26666c8` |

The assembler uses exactly the three selected overlays (`owner02.py`,
`reference_registration02.py`, `reference_store03.py`), keeps the 137-entry
profile layout, preserves the installation, and reports 3 changed/162 unchanged
payloads in `DMKN_ORDINARY_REFERENCE_SUCCESSOR_ASSEMBLY_V1`. Its fresh destination
is `ordinary-reference-assembly-02/package`. The selector's proposed enclosing
limit is 90 wall/50 CPU seconds, 512 MiB, two processes. No native build or
snapshot copy occurs.

The continuation targets `ordinary-reference-public-continuation-01/workflow`
for new evidence and new contribution outputs while using the old catalog and
custody in place. It explicitly supplies both `--retained-snapshot-operation`
and `--retained-snapshot-sha256`. It pins the old immutable failure/provenance,
ADOPTION/STORE markers, origin reservation/closure/manifest and fixture bytes;
it does **not** pin the mutable catalog/custody database files. Six public calls
share 480 wall/330 CPU seconds; the proposed outer limit is 540 wall/390 CPU,
1792 MiB/eight processes, with 1536 MiB child allocations. These are finite
proposed limits, not measured requirements or runtime authorization.

AST-only parsing passed for all four files without importing product code. One
earlier command-line quoting attempt failed before reading source; the corrected
stdin AST invocation then passed. No selector, assembler, public CLI, native
compiler, owner open or experiment was run by this agent. No Git mutation was
performed. Independent source reviews were requested separately for the assembly
pair and continuation pair. Later review corrections supersede these hashes and
must be recorded before use; no completed run exists here to repeat.
