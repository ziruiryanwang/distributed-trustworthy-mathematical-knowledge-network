# Discovery distribution integration: saved-evidence audit

Reviewer: core_release. Only retained files and source were read; no build,
test, installed command, mathematical runtime or network operation was rerun.

## Build: PASS

The one selected build completed under its original limits. Actual installation:
`product-local/v5-distribution-discovery-01/Mathematical Commons v5`.

| Evidence | SHA-256 |
|---|---|
| selected input | `e0e22f412a6d276f172603ad11ff5217ea321b5a038921af2bd7f1b4b028e20b` |
| build selection | `a50cdd5ebdbeb1c9ff497eda8a992ee119ea4f65a48accacf7f88ef9c0688a68` |
| build `RESULT.json` | `b8cf950ca02ad8cb788d5433d173f60ed3f42cf96a229a0ba744b7ab6b64917d` |
| installed `V5-RELEASE.json` | `769506990ea10be5c6ce812e5cfd457922f4955ad4831bcdbc9d7a9ec9561108` |

The input and build evidence are under `experiments/v5-local-checks`, with run
name `distribution-discovery-build-01`. Independent comparison against input
basis `1903bb44` confirms 109 to 110 SDK entries: exactly the six replacements
and one helper in [source review](DISCOVERY-DISTRIBUTION-REVIEW.md), zero removals
and no other input-field changes. Both selected outer sources match their
retained snapshots and expected pins.

The new release binds that exact input hash. All 110 SDK records agree with the
selected input. Comparing old/new complete payload maps gives exactly the same
six changed files and one added file: 9,854 to 9,855 payloads, no other change
or removal. The builder, base, runtime assets, mathematical images, Lean
support and role bindings are unchanged. The generated preparation descriptor
changes only its derived source-pin list for those same six replacements and
one addition; all other preparation fields remain equal. This is expected
binding to the new SDK, not a changed preparation algorithm or checking policy.

Builder stdout records `DIRECTORY_CREATED_AND_EXACTLY_VERIFIED`, 9,855 files,
842,297,537 bytes and the release hash above, with mathematical acceptance false.
The enclosing result records exit zero, no cleanup errors, direct child reaped,
Job closed and zero active processes. Job CPU was 60.140625 seconds; outer
wrapper CPU was 1.453125, giving 61.59375 known CPU seconds without adding the
nested supervision field twice. Total wall time was 273.409226 seconds, within
the original 300-second bound; peak Job private commit was 57,085,952 bytes.
Unchanged large payloads were not independently rehashed a second time.

## Installed boundary 01: FAILED before owner invocation

The reviewed selector staged request SHA-256
`9f991f1be08f59489e31736e222c4084f9e5c740db7f029429d8e35771284228`
under the fresh installation parent's `integration-inputs`. The saved request
has exactly the four reviewed parameters, seven expected sources, the fixed
pattern workspace schema/profile, aggregate mode and original
60-CPU-second/120-wall-second/384-MiB allowance. No runtime adoption or foundation
parameter is supplied. Root's invocation returned `CLIENT_OUTPUT_LIMITS` from
`client/launch.py:141`; this is a failed request, not an installed success.

Independent source inspection identifies the exact cause: the unchanged
launcher defines `SOURCE_TOTAL = 64*MIB` and requires
`SOURCE_TOTAL <= output_limits.bytes`. The selector's 32 MiB is below that
minimum. The source review missed this existing launcher contract; no product
defect or exhausted RAM was implicated. The fail occurs during `read_plan`,
before Job construction, owner invocation or mathematical runtime work. Retained
request controls exist; the intended run and commons directories are absent.
There is no normal owner/Job result to claim as passing. The failed request and
its exact used selector remain preserved. Root's captured failure is retained
in [DISCOVERY-INSTALLED-PREFLIGHT-FAILURE.md](DISCOVERY-INSTALLED-PREFLIGHT-FAILURE.md),
SHA-256 `9d0c9b439249d9ae12bbfabe9249991cd0a814e4b9f50e79e608d7aa55c50b24`.
It records exit one and 5.126559 seconds tool wall time; failure CPU was not
measured and must not be counted as zero.

The remaining saved-plan bounds were inspected without execution: 111 sources
including the owner, 1,275,452 total source bytes, maximum source 50,509 bytes,
all required public sources, 21 portable closure entries and a small parameters
object. Process/CPU/wall/memory/log bounds meet the unchanged launcher. The
smallest source-supported correction is a fresh request with 64 MiB output,
1,024 entries unchanged and new names/paths; no product or adapter change is
needed. Any such successor still needs root's selection and actual outcome.

## Installed boundary 02: PASS

Reviewed `Select-DiscoveryInstalled02.ps1`, SHA-256
`c7f945d33234f11f9da7921b7b28cb51b20b46f0263a88c731e83d6a705c6f47`.
It pins the exact failed request, unchanged adapter, release and builder;
changes only the request name, fresh commons path and output byte allowance
to the legal 64 MiB minimum; and exclusively stages a new request. Existing
owner bytes are reused unchanged. The new request/control/run/commons paths
are checked absent. CPU, wall, memory, process and entry limits are unchanged.
This corrects the specific failed preflight contract without weakening product
checking or editing attempt 01. The actual saved successor request differs
from 01 in exactly those three fields.

The one selected successor ran under
`product-local/v5-distribution-discovery-01/integration-operations/installed-discovery-boundary-02`.

| Evidence | SHA-256 |
|---|---|
| successor request | `a763cfceee9ca1471da5091d25df9e5b4e1eb3d71001c5698b847462272888e0` |
| retained `plan.json` | `b7c2a6b05381aa620951244d0041e23b8ef987680cebd30c5e556fe2388615fc` |
| `RESULT.json` | `0e94883401a2e177ed82ca3f7d39cf69d69f022371419ca3d8c8ce48725fc599` |
| `BOOT-RESULT.json` | `bb9dd29ff0048789d25ed06769657703186fce4273b437a0f6485e476543cb43` |
| `work/discovery-installed-result.json` | `637a1c834bce418cebd8138496365e19c82a19e94dad6c82b75c6f21212cf3bc` |

Independent byte/length comparison of all 111 selected source originals and
retained snapshots passes. The unchanged adapter is `58b3c2b1` at its source,
staged owner and copied runtime origin. All seven changed modules' reported
origins are the selected copied files and agree with both the release map and
boot origin report. Boot records `OWNER_EXITED_ZERO` with 111 source files and
1,275,452 source bytes.

The adapter report is `COMPLETED`, stage `done`, no error or cleanup error,
workspace closed and finished before the original deadline. Its own local
involution syntax compiles into two sorted distinct keys under namespace
`9d8a2729497f2fc175a082de8ef3476d5a6135b537f3a1e29173863b53f06eb9`.
Create and reopen reports agree: pattern schema, same empty snapshot/namespace,
zero objects/postings/operations/modules/packets, no active client. Neither
query construction nor this structural store state is a mathematical warrant.
The reviewed adapter and saved report have zero RuntimeProfiles, issuers,
grants, native/proof/network calls; mathematical acceptance remains false.

The enclosing result separately confirms exit zero, direct child reaped, no
final/cleanup error, closed Job and zero active processes. Job CPU 2.234375 plus
outer wrapper CPU 5.171875 gives 7.40625 known CPU seconds; total wall time is
9.901229 seconds. Peak Job private commit is 42,209,280 bytes. Output census is
1,306,498 bytes / 141 entries within the original successor bounds. Build plus
successful installed check use 69 known CPU seconds; the failed preflight's
unmeasured CPU is additional. No passing component/native campaign was repeated.

## Claim boundary

The exact package now ships already-tested numeral import and optional
whole-type discovery together, with a passing changed installed origin/query/
workspace boundary. It preserves the prior trust/runtime stack. The retained
failure remains a failure. This does not establish new mathematics,
useful-growth benefit, worldwide deployment or completed final v5. Root owns
adoption and Git; no further runtime or rerun is selected by this audit.
