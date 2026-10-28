# Independent source review: incremental inert host

2026-10-28, growth_design_audit. Canonical guard passed. Source and file metadata
only: no product import, execution, database access, network or Git operations.
Root owns integration, runtime selection and adoption. Review status below is
split by inspected boundary; no source-stage verdict is an executed result.

## Principle

The independent argument is
`../ordinary_connect_ownership/APPEND-RECOVERY-CHALLENGE.md`, SHA256
`b91a64f92c90aa28fa508f922843e369d28ca4120cc5cfec849c2ca490c35fe6`.
It supports the selected stable descriptor plus authorized committed-prefix
contract, under the documented lock/storage/transaction assumptions. It rejects
an unnecessary batch recovery journal for this role.

## Root integration seam: PASS at source stage

Reviewed stable source identities:

| File | SHA256 |
| --- | --- |
| host.py | `c7febeebe6a0ec0e49eb764215b68e9a87f9a3ec28719b69a3802940311ecf25` |
| run.py | `553f398b0c0f36fd06808d8be4f45998db1c66886b7ad9a2d3eb28f3cbb0a701` |
| HOSTING.md | `935a5759f88e178ffa37267e2b728d435c960f8eefcbf63444448024ef39fefe` |
| LAUNCHER.md | `c84a2948b978c3a1ef8eb4bc5f5d3053a8249e6fc27ac38dd0ce533e9774ea0a` |
| assemble.py | `79a13a5ef6e9989f432cdeeca0d4ee156fcd654b070e678de9967b21ee55ef89` |

The wrapper delta is additive: `init` and `append` dispatch to initialize/append;
prepare and serve retain their signatures. Init/prepare require fresh host roots;
append/serve require the exact descriptor/seal pin. Append receives the same
bounded pinned config, input/output disjointness checks, profile bootstrap,
allowance, final input/profile verification and failure-report behavior as the
existing dedicated entry. Only prepare/append parse bundle paths; only serve
parses TLS inputs. Init does not accidentally enter either path. No mathematical
owner or native call was added.

Compared to the selected predecessor, run.py changes only the host operation
allowlist. Its fixed option grammar, allocation containment, overlap protection,
dedicated-host exclusion and exact-host-root exception remain unchanged. The
exception remains unavailable to ordinary owner/peer operations.

HOSTING and LAUNCHER distinguish static V1 generations from fresh incremental
hosts, explain stable descriptor versus current snapshot, require explicit
partial disclosure, preserve finite cumulative limits, account for duplicate
inputs and possible repeated producer closure, and require completed process
cleanup before another invocation. No auto recovery/retry, owner proof checking,
whole-corpus completeness or end-to-end minimal-delta claim was introduced.

The file-only assembler pins the adopted connect kit manifest/receipt/map and
base PROFILE, validates the 160-file package, and requires an exact five-role
source-map replacement. It updates documentation-role mappings for both changed
Markdown files. Only the three code roles belong in PROFILE.files; the two docs
are outside that runtime allowlist but remain in the full package census. This
was checked against the retained base map and PROFILE as plain JSON data.
The resulting expected delta is those five roles plus PROFILE: 160 files,
154 unchanged, no additions and unchanged installation/native support. Source,
baseline and output pins are rechecked around copying and profile publication.

No blocking root-seam defect was found. Final source-map/build pins and the
custodian implementation are separate pending review sections, not presumed
passes from this wrapper review. The assembler has not run.

## Custodian implementation: PASS at source stage

Reviewed custodian.py SHA256
`510b922d18f42debaa3cffef5775db61121beccb4883cc352b5ee9d9350dac67`
and CONTRACT.md SHA256
`a92f716cee23da410c94336cb87149199f7a4d5f95b12e270f43fd00b096016e`.
The source hash was unchanged at the end of review.

Initialization checks the exact four-field config, affirmative partial policy
and existing limit ceilings before creating a fresh root. Under the permanent
lock it creates the two stores, verifies zero custody counts, zero index
sequence/objects/postings/features and one initial snapshot, and obtains its
exact snapshot identity. Both stores must close successfully before the bounded
canonical descriptor is written and renamed into place. Failure after rename
can honestly report initialized:true with overall failure; it does not pretend
the side effect was rolled back. No descriptor is installed after failed store
initialization/closure. The pending filename is only the preserved one-time
creation convention, not append recovery machinery.

Append validates its exact config, explicit share/partial flags, bounded bundle
limits, 1..64 unique exact target identities, pinned manifest and target-unit
membership. Inside the lock it validates the selected incremental descriptor
before opening stores, fixes both store limits to that descriptor and checks
semantic identity. Existing store constructors compare their persisted exact
configuration; append accepts no new cumulative capacity fields. Static V1
roots cannot take this path.

The unchanged batch reader verifies every supplied unit's manifest size/hash,
exact evidence identity and structural bounds before that batch is inserted.
Aggregate census checks precede each batch's mutation. Within the batch the new
code preserves evidence/all-locators -> exact evidence readback -> resolved
preview -> preview readback -> locator binding -> index admission -> record
readback. No new primitive bypasses the existing per-store transactions.
Conflict or index-capacity refusal can leave only the expressly authorized
unindexed custody or valid committed prefix.

Progress rows are saved after returned writes but before readback. The report
explicitly allows a committing call to take effect before throwing or losing
its response. batch_complete remains false until all selected targets, aggregate
census, metadata, input/descriptor/profile checks and store/lock closure finish.
No failure path deletes old objects, replaces the descriptor, resets capacity,
retries a unit or claims rollback. Later service does not claim an earlier
append completed. Runtime controls must still exercise these paths.

The V2 serve branch obtains current bounded metadata and one validated snapshot
under the shared lock. The provider reopens its index while the lock remains
held, so supported appends cannot race the reported snapshot. READY and final
service reports distinguish configuration identity/current content and carry
NOT_ASSERTED_BY_SERVICE for prior append completion. Empty initialized stores
are allowed. There is no historical snapshot walk or target census at startup.

Plain source comparison confirms prepare is text-identical to its predecessor;
the marker/lock/store-close/report helpers are also text-identical. V1 seal
parsing retains its complete field/target/counter checks, and the V1 serve branch
retains exact custody counts, latest snapshot and object-count comparisons.
Only explicitly parsed V2 descriptors enter the current-content branch.

No blocking defect was found in the changed custodian boundary under the stated
protected-storage, supported-command, completed-process-cleanup and SQLite
premises. This does not certify arbitrary power loss, unsupported concurrent SQL,
mathematical truth, complete dependency availability or final-v5 readiness.
Final mapping/build pins and executed controls remain separate gates.

## Final direct source selection: PASS at source stage

Reviewed source-map.json SHA256
`f5ea607c6774872113f404e2afcaf188b12a43e8839ac4ff5017b4edb02d8ab6`
and build.py SHA256
`d64ef13504564c86a527563aa66034ab19634311ea7f36e50ce45e175afd8426`.
Plain JSON comparison against the adopted connect map finds exactly the five
selected role/source replacements, the two corresponding documentation mapping
changes and no other top-level role/lane/tool/runtime changes. All 88 other
source pins are unchanged; counts remain 93 sources and 78 copies. The five new
source byte lengths/hashes match the actual reviewed files. Native selections
and outputs are unchanged. Builder source differs only in PREFIX and MAP_SHA.

Together these checks support the proposed bounded file-only assembly and
focused changed-boundary controls. No import, compiler, database, service or
assembly has been executed by this review. A later run requires root's finite
selection and an audit of actual output; full v5 remains unfinished.
