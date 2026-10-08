# Source09 support and evidence report

2026-09-23. **Locally qualified Windows v1 source candidate.** The selected
source09 support build and installed mixed publication/custody workflow have
the independent disposition
`PASS_SELECTED_SOURCE09_INSTALLED_MIXED_ROLE_NOT_WHOLE_V1`.
This report binds the actual archive, focused tests, build and installed outcome;
it does not claim a perfect/public release or completion of the global goal.
The source08 first preparation remains a retained failure. The separate final
delivery gate is [HANDOFF-INTEGRITY.md](HANDOFF-INTEGRITY.md): consult its exact
checked scope and disposition. A missing, failed or mismatched report leaves
the handoff incomplete; no integrity success is assumed here.

## Exact candidate and change boundary

Selected source: `product-local/stage-census-source-09` in the canonical
Trustworthy project. Independent static review compared all 114 actual payloads
against the frozen source08 manifest: 113 unchanged, exactly one changed,
no additions or removals. The changed `py/run_stage.py` is 30,037 bytes,
SHA-256 `bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028`.
It repairs comparison of already OS-resolved ordinary/extended Windows path
spellings in live/output censuses, preserving original paths for I/O, and adds
bounded count/path/namespace refusal diagnostics. The 4096-entry ceiling,
byte/resource limits and narrow missing-file behavior stay unchanged. This is
not a hostile-local-filesystem isolation claim or proof of the old failure cause.

The inherited source07-to-source08 change remains separately reviewed:
114 payloads, 101 unchanged and thirteen changed (`py/peer_node.py`,
`py/service_worker.py`, `make_request.py` and ten public documents).
Mathematical checking/native sources, canonical codecs/assets, wire/TLS,
config/database schema, capacity/recovery, hosting controller and packaging
logic are unchanged across those cuts. The stage runner is now expressly a
changed component; its focused tests do not qualify all native-stage behavior.

| Delivered or tested object | Final binding |
| --- | --- |
| [math-commons-source.zip](math-commons-source.zip) | 3,782,752 bytes; SHA-256 `015894dea22164802b9683cf6545a6c9ab04ec2098c9fd9684b8fff34e9014ed` |
| [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json) | 20,300 bytes; SHA-256 `7d1aa2c3dd6a6592c79e522857cd684576c6a1308167f44c02e183744499306a` |
| [PACKAGE-RESULT.json](PACKAGE-RESULT.json) | 455 bytes; SHA-256 `41022e5cbd834c179e8a18dc0f6b778a6759601f6bfb21e30e21a551bcd2eb62` |
| Source09 preparation result | 4,389 bytes; SHA-256 `4d952125c444c398e6333d5ebc0e509fea3eae70c6d9659b917bdcd852d0c807` |
| Fresh installed build receipt | 3,194 bytes; SHA-256 `01b8f8bdf74555e3562974dcd8923c5e90ac192c5df4510dda0d0eed004a9813` |
| Independent census outcome audit | 4,938 bytes; SHA-256 `6a6ae28a918b45f9e3f0dbbb154d44b76f766ccde671fa9f73ba20edd8234d4e` |
| Installed mixed-workflow result | 140,099 bytes; SHA-256 `10b97df03b92aa69f6cad0f8f46e01610f65a8affaecb8b902e0850a5c9f5a3f` |
| Installed-workflow inputs | 69,106 bytes; SHA-256 `99109766046811bede1576053fd8481b5deb9cd51d8f26b86d625d4025f9d7a1` |
| Independent installed outcome audit | `PASS_SELECTED_SOURCE09_INSTALLED_MIXED_ROLE_NOT_WHOLE_V1`; 8,982 bytes; SHA-256 `af13f02267092713628e5930ed5203c3e38ba095503360001be96fd94be164d7` |

Both original packaging records retain `DEVELOPMENT_SOURCE_PACKAGED_UNQUALIFIED`:
source08 later failed its build, while source09 subsequently built successfully.
A later qualified disposition belongs in this companion report; frozen source,
package, installation, node state and machine results must not be rewritten.

## What the selected software implements

Independent local agents may discover candidates, acquire exact inert packages,
freshly admit them under a selected Lean foundation, reuse receiving declarations
in owner-authorized source, and submit/publish checked contributions. No mandatory
central server, shared research agenda, human-intention acceptance field or global
task queue is part of this workflow.

The inherited mixed-catalog feature extends `expose` with optional acquisition handles alongside
required local-publication candidates. Its catalog preserves publication rows
first, custody rows second, with each row's own authority. Whole-view count,
canonical-byte, bundle-byte and duplicate constraints apply jointly. Custody
does not manufacture publication; a bad selection prevents the whole view from
committing. Serving uses committed copied bytes and ledger authority without
granting mathematical acceptance. Every receiver still performs fresh `admit`.
Old pure publication and singular/plural custody envelopes remain available.

## Current gates and preserved failed attempt

| Gate | Actual disposition |
| --- | --- |
| Source08 complete source/harness prelaunch review | `PASS_STATIC_PRELAUNCH_ONLY`; thirteen changed files reviewed, full map checked. Not behavior or mathematics. |
| Source08 native-free `mixed-01` | Runner completed 12 tests, zero failures/errors/skips, clean termination. Independent outcome audit: `PASS_SELECTED_NATIVE_FREE_MIXED_EXPOSURE_NOT_INSTALLED_QUALIFICATION`. Not rerun on source09. |
| Source08 preparation-01 | Packaging succeeded; support build failed in the inherited census before node initialization/network. Independent disposition: `FAIL_PREPARATION_RETAINED; INSTALLED_MATHEMATICAL_GATE_NOT_RUN`. |
| Deterministic standard-library probe | Six simulated groups passed; independent audit: `PASS_SIMULATED_NAMESPACE_MECHANISM_ONLY_NOT_ACTUAL_CAUSE_OR_PRODUCT_GATE`. |
| Source09 complete source and focused-harness review | `PASS_STATIC_SOURCE09_CENSUS_GATE_ONLY`; all 114 payloads compared, one explained runner change. |
| Source09 native-free `contracts-01` | 12 tests, zero failures/errors/skips, quiescent. Independent audit: `PASS_SELECTED_NATIVE_FREE_STAGE_CENSUS_NOT_INSTALLED_BUILD`; the raw pending-audit label is preserved. |
| Source09 fresh package/extraction/support build | `PASS_PREPARATION_NOT_MATHEMATICAL_ACCEPTANCE`; package and two support compilations completed, exact 114 payloads bound, clean outer Job. No node initialization or network in preparation. |
| Source09 actual installed mixed-role workflow | Historical raw status `PASS_MIXED_EXPOSURE_PENDING_INDEPENDENT_AUDIT`; the completed independent audit below supplies qualification. Twelve charged ordinary requests, five native stages, one fresh publication, one no-charge exact replay, no renewed grants; cleanup is quiescent. |
| Independent mathematical/operational outcome audit | `PASS_SELECTED_SOURCE09_INSTALLED_MIXED_ROLE_NOT_WHOLE_V1`; exact package/build, proof-body reuse, distinct publication/custody authority, both fresh receiver admissions and cleanup checked. |
| Final delivered-artifact integrity check | Separate required [HANDOFF-INTEGRITY.md](HANDOFF-INTEGRITY.md); consult its exact checked scope and disposition. Missing/failed/mismatched report means incomplete handoff. |

The source08 native-free suite uses actual SQLite, request/authority/commit/replay and
wire/view paths. Initialization, publication/acquisition history and mathematical
package semantics are synthetic; semantic checking and supply are mocked, as is
the service transport body. No native stages or network connections occur.
Its raw runner pass is not evidence of Lean admission or live service.

Source09's focused suite imports the actual repaired runner and unchanged
domains module. It exercises real normal-tree bytes/output paths, one real
outside file with OS resolution, actual stdlib retry branches with scripted
WinError 2/3, mixed namespace operands, synthetic outside/unsupported names,
4096/4097 entry boundaries, narrow missing-file behavior, error propagation and
bounded diagnostics. Entry-count streams and namespace transitions are
simulated; there is no real compiler, deletion, reparse attack, UNC access,
network or mathematical acceptance. The reused outer supervisor is the frozen
source08 implementation in a separate snapshot.

Source08's failed stage reported `SELECTED_STAGE_ENTRY_OR_PATH_LIMIT`; its
combined guard recorded neither the offending entry nor which disjunct fired.
The final retained tree does not identify the transient trigger. The separate
stdlib probe demonstrates a reachable namespace false refusal, not historical
causation. A produced `.olean` file did not establish a successful build;
that failed installation is not reused for node initialization.

The independently audited installed result records a fresh producer acquiring/admitting audited
D1, submitting unchanged prior Beta source, publishing that freshly checked
artifact, and exposing Beta plus acquired-only D1. Actual owner service then
supplied both distinct catalog entries after the original supplier stopped;
a fresh receiver acquired and admitted both together. Recorded Beta body node
148 depends on D1, which is absent from Beta's type: this is substantive proof
reuse, not merely a type mention. It is a rerun of known source, **not new
mathematical authorship**. The audit separately traversed the canonical proof
body and checked both receiver theorem types, universe arities and foundation;
the service itself did not grant mathematical acceptance.

Producer usage was seven requests, three stages and 568 MiB reserved against
768 MiB authorized; receiver usage was five requests, two stages and 408 MiB
against 512 MiB. One exact exposure replay added no charge; no grant was renewed.
Both final statuses report no active/pending request. Recorded Jobs closed,
direct service children were reaped, and service threads ended; root's separate
current read-only check found no selected listeners/workers. These observations
do not promise future availability.

The frozen driver's legacy raw scope `SAME_HOST_FRESH_SOURCE08_MIXED_ROLE`
names the inherited workload, not the installed version. Exact source09
archive/manifest/build/input pins bind the actual run. That legacy string and
the raw pending-audit status remain unchanged in the original machine record;
the completed independent audit supplies the actual source09 qualification.

## Preserved evidence and its transfer limits

These predecessor results supply context, not a claim that all their tests were
rerun on source09. An unchanged-code comparison supports focused delta testing;
it is not automatic whole-release qualification.

| Capability | Preserved independently reviewed evidence |
| --- | --- |
| Agent-operated reciprocal contribution | Operator05: a no-history operator built/configured two nodes, reused D1 for Beta's homomorphic theorem, returned it for Alpha's product corollary, and freshly admitted both downstream. One agent operated both same-host nodes; one shell correction was disclosed. |
| Owner-controlled authenticated exchange | Remote04: bounded pinned-TLS controls, installed owner service and genuine surviving-holder/fresh-receiver return. No independent host or exhaustive TLS-security claim. |
| Evolving suppliers on retained state | Source06: added a third contact, replay/conflict controls, old-handle retrieval and fresh admission of another theorem, preserving earlier checked state. Suppliers were static audited views. |
| Several retained roots served together | Source07: actual exhausted-holder service of two acquired roots after both original suppliers stopped; fresh receiver admission of both, with independent scoped audit. No new publication or authoring. |
| Bounded useful discovery | Earlier matched consumers selected and substantively reused a theorem among seven entries without its target ID; both direct and retrieval arms published the same target. This did not establish causal speedup or general retrieval quality. |

Preserved failures remain part of the record: the first operator setup failed
under PowerShell 5.1 stderr handling; one source submission was refused and
independently repaired. Source06's two harness failures remain retained, including
its successful initial work and consumed allowance. Earlier U1 noncompletion
was not reclassified by later successful runs. No old state, failures or charges
are erased to obtain this candidate. Source08's failed support-build allocation,
partial installation, incomplete first-child receipt and all observed charges
also remain preserved; the source09 pass does not reclassify that failure.

## Costs: report measurements, not an efficiency claim

| Selected work | Observed cost and scope |
| --- | --- |
| Source08 native-free `mixed-01` | 1.90625 worker Job CPU s; 3.035936900007073 worker wall s; 78,528,512-byte peak private commit; 3.499370599980466 coordinator wall s. |
| Failed source08 preparation-01 | 32.625 inclusive outer Job CPU s; 46.622 outer wall s; 2,340,724,736-byte peak private commit. Includes successful packaging and failed support build; no initialization/network. |
| Deterministic stdlib probe | 0.140625 process CPU s; 0.017742700001690537 s for its case loop. No Job receipt; this is not the command's entire elapsed time. |
| Source09 native-free `contracts-01` | Independently audited: 1.265625 worker Job CPU s; 1.508981799997855 worker wall s; 38,662,144-byte peak private commit; 1.7695189000223763 coordinator wall s. |
| Source09 fresh preparation-01 | 15.578125 inclusive outer Job CPU s; 16.299610499991104 outer wall s; 2,343,305,216-byte peak private commit. Successful packaging and support build only. |
| Source09 installed mixed-role workflow | Independently audited disjoint Job CPU: 390.90625 s main + 0.265625 s original D1 supplier + 0.640625 s inclusive producer service = 391.8125 s. Integration wall 375.5965235999902 s; main Job peak private commit 2,763,730,944 bytes. |

The failed source08 first child also reports 21.875 CPU s; it is nested inside
the 32.625-s outer total and must not be added again. Known disjoint costs may
be reported together only with their explicit scopes; none establish speedup.

Source09 preparation plus runtime totals 407.390625 observed Job CPU seconds;
including its census suite gives 408.65625 s. Including the separately retained
failed source08 preparation (32.625 s) and its mixed unit suite (1.90625 s)
gives **443.1875 s** across those five non-overlapping workload groups. The
probe's 0.140625 process-CPU seconds remain separately reported because its
measurement is not a Job receipt. Nested service/native receipts are not added
again. These sums exclude earlier theorem production, model/controller/reviewer
work and whole-machine costs; they are not per-theorem or efficiency estimates.

For context, independently scoped earlier observed Job CPU totals were
372.03125 s for the operator05 workflow including its failed setup/source,
204.28125 s for source06 preparation/runtime plus unit tests, and 195.71875 s
for source07 preparation/runtime plus unit tests. These different workloads
must not be summed into a per-theorem cost or compared as a speedup estimate.
Nested Job/native CPU is not added twice. Model/controller/reviewer work and
whole-machine costs are not comprehensively measured; conservative reserved
bytes are not measured retained disk usage or physical reservations.

## Supported environment and trust premises

Windows x64, PowerShell 7, fixed local NTFS and stable cooperative-owner files
are required. The selected Python executable is `D:\Python314\python.exe`,
SHA-256 `03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38`.
Root's actual standard-library observation reports Python 3.14.6 (`c63aec6`,
June 10 2026, MSC v1944 AMD64), SQLite 3.50.4, OpenSSL 3.5.7 (June 9 2026),
and TLS 1.3/ALPN availability. The complete Lean 4.34.0 Windows runtime is
supplied separately. Read-only local inspection reports its `bin/lean.exe`
at 83,456 bytes and SHA-256
`a8040e2cab341c12116ab591fed9f761816f5f6b08554f6cc1680e86dfbba0a2`;
the actual source09 build receipt binds that same executable and Python pin.
These are executable pins, not whole-runtime attestation or a clean-machine test.
`Get-Command pwsh` resolves to the supplied PowerShell 7.6.5.0 application at
`C:\Users\Uisjs\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe`.
The walkthrough's `C:\Program Files\PowerShell\7\pwsh.exe` is an illustrative
path, absent here, and must be replaced with the actual resolved application.

The selected OS/filesystem, runtimes, implementation, foundational axioms and
cooperative local owner remain trusted. Local Lean source is executable input,
not isolated hostile code. Peers send bounded inert canonical data, not checking
plans or inherited acceptance credentials. Certificate pinning authenticates an
owner-selected endpoint, not theorem truth, completeness or availability.

Config 6 / physical database 5, wire/catalog 2 and stage-plan 2 are selected.
Fresh bound installations/state are required. Runtimes and test credentials
are excluded from the source package; no dependency downloader, automatic
agent, public listener or permanent service is installed by extraction.

## Mathematical coverage and practical limits

This is a bounded, extensible mathematical software profile, not a fixed replay
list and not a claim to represent all mathematics already. Independent agent
contributions demonstrate new checked declarations using earlier acquired work.
A preserved `Fin.castLE_castLE` case captured one real Init/private-helper closure
and supported a checked successor. Neither proves general mathlib compatibility.

The selected `Init` frontend supplies syntax/macros/tactics, matches shared
bindings to the checked inventory and captures required dependencies. Fresh
replays reconstruct from the selected foundation. Additional axioms, unsafe or
unsupported declarations and oversized closures refuse; syntactic Lean validity
does not guarantee canonical capture. New external inductive/recursive families,
class/instance registration and notation reconstruction are not comprehensively
qualified. The archive's `assets-lock.json`, foundation seed/inventory and five
common packages identify the supplied mathematical basis.

Contexts contain at most sixteen packages, including those five common packages;
admission selects at most four candidates. Views have at most 256 entries with
combined 64-MiB canonical and bundle limits plus page/SQL/time/memory bounds.
These ceilings do not promise that arbitrary selections at the maximum will fit.
There are at most sixteen initial-plus-added immutable peer contacts. Local
search is bounded enumeration or exact type-symbol filtering; remote discovery
is paged enumeration of one selected peer snapshot, not global completeness.

Nodes and hosting grants are finite. Renewal does not remove lifetime ceilings;
committed views can support deliberate compatible fresh-node transfer. General
backup/restore, used-state/profile migration, damaged-state recovery and salvage
of unexposed material after irreversible exhaustion are not provided. Narrow
recovery has scoped predecessor evidence, not qualification of every new
interruption. Conditional custody is not permanent retention.

No independent second host was available. This does not block a local candidate,
but prevents claiming independently administered deployment, public routing or
Internet availability. Licensing is explicitly undecided; no redistribution
permission or external publication/deployment follows from this handoff.
Sustained useful growth, broad-library interoperability, large-network scaling
and whole-agent comparative efficiency remain unestablished. The overall global
mathematical-commons goal remains unfinished.

## Maintainer provenance, not runtime dependencies

Basic installation and use require only the delivered package, supplied runtimes
and its extracted documents. The following preserved project records supply
additional audit detail; their relative links require the full project tree:

- [Source08 complete reviewed map](../../experiments/mixed-exposure-01/SOURCE-MAP.md)
  and [static review](../../experiments/mixed-exposure-01/SOURCE-REVIEW.md), plus
  [independent native-free outcome audit](../../experiments/mixed-exposure-01/OUTCOME-AUDIT.md).
- [Source08 preparation failure audit](../../experiments/mixed-exposure-01/PREPARATION-FAILURE-AUDIT.md),
  [independent simulated-mechanism audit](../../experiments/stage-path-census-01/PROBE-OUTCOME.md),
  [source09 complete source/harness review](../../experiments/stage-path-census-01/SOURCE-REVIEW.md)
  and [raw focused result](../../experiments/stage-path-census-01/runs/contracts-01/RESULT.json).
- [Source09 independent census outcome audit](../../experiments/stage-path-census-01/OUTCOME-AUDIT.md),
  [actual preparation result](../../experiments/stage-path-census-01/preparation-01/RESULT.json)
  and [fresh support-build receipt](../../product-local/stage-census-integration-09/install/build/build-receipt.json).
- [Source09 raw installed result](../../experiments/stage-path-census-01/integration-01/RESULT.json)
  and [exact installed-workflow inputs](../../experiments/stage-path-census-01/integration-01/INPUTS.json),
  with the [completed independent installed outcome audit](../../experiments/stage-path-census-01/INTEGRATION-OUTCOME-AUDIT.md).
- [Operator05 qualification](../../experiments/operator-onboarding-01/QUALIFICATION.md),
  [remote04 qualification](../../experiments/remote-transport-01/QUALIFICATION.md),
  [source06 qualification](../../experiments/peer-contacts-01/QUALIFICATION.md),
  [source07 qualification](../../experiments/aggregate-custody-01/QUALIFICATION.md).
- [Matched consumer comparison](../../software/qualification/usefulness-consumers-01/COMPARISON.md)
  and [existing-library result](../../experiments/lean-library-interop/RESULTS.md).

The installed audit qualifies the selected same-host capability, not every
release property. The adjacent [HANDOFF-INTEGRITY.md](HANDOFF-INTEGRITY.md)
separately decides the exact file-delivery gate; consult its checked scope.
Neither report authorizes external publication/deployment or grants a license.
