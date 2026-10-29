# Standalone inert host: saved-outcome audit

2026-10-28. Reviewer: growth_design_audit. **PASS for the selected distribution,
eight focused control groups, and one public incremental-host lifecycle.**
This is a local Windows/Python storage-and-index result. Mathematical acceptance,
useful discovery, growth advantage, independent deployment and full v5 completion
are not established by these runs.

## Evidence and method

The controlling scope is [EXECUTION.md](EXECUTION.md), following source
[REVIEW.md](REVIEW.md), SHA-256
`7ea01e5585535ac6182736eedc0f38452b6461c628172d3c48da62bf3011e44d`.
The audit reads saved files and hashes only; it does not rerun product code, open
owner/custody/index databases, invoke Lean, create network traffic or change Git.
All paths below are relative to the canonical project root. Run directories are
under `experiments/v5-local-checks/`.

For each of the three runs, the actual `selection.json` hash equals the outer
report's selection pin. All 11 selected source rows across the three selections
match both their saved snapshots and current frozen files. Expanded selected
arguments, cwd and limits equal `command/command.json` and the outer report.
Captured stdout decodes to the corresponding inner BUILD/control/workflow report;
stdout/stderr lengths agree with the outer observations. Every outer result is
`COMMAND_EXITED_ZERO_AND_CLOSED`, exit zero, reaped, Job closed, with no active or
terminated processes, termination request, cleanup error or stderr.

| Run | Selection SHA-256 | Outer `RESULT.json` SHA-256 |
|---|---|---|
| `inert-host-pack01` | `547c441ef4bd431d12c59e5f036a2f14b7dd7018ba80c1b83751c97ae6aba091` | `e924c80884517082655e76d72408863425c6b9935ae41df404c50011866d351c` |
| `inert-host-controls01` | `03db8976d2bde3275e9ef8a775bd2a73f9899085d8f9c296ac943b8b0dba3d3c` | `e53e1dc674c49503d01d847b8c7a5ae9b2ff7959aa28d00baaaeccf5680b38ba` |
| `inert-host-public01` | `85bb50cc65503ae1376956cfca4a059910ac55c6c2ec61f7e56e7f96117d0b96` | `bfd1a9002fbafbe3e2c5dd4c9065ec367351eb665bc0ca7cb4ed425af108bf9c` |

## Actual standalone distribution

The used package is
`inert-host-pack01/packed/inert-host`, with profile `SOURCES.json` SHA-256
`d6c1f02949962d26a565910f7d2bf064987597aeb418446067c66fc8a107c4db`.
Its saved `packed/BUILD.json` hashes to
`775813d29406d8bd0a56fa1af6b90c1efd9589f283e2fabe4dffe9fb78e4af8f`.
It records 30 payload files / **477,704 bytes**, and a 482,330-byte stored ZIP
whose recorded SHA-256 is
`40405ae1cb7ce15b6d13143ddf26152266878ef6e7ca959704938e0191291cac`.

The 28 source payloads total 452,893 bytes: three new role files total 73,646
bytes, while 25 existing support files total 379,247 bytes. Source review already
independently hashed all 28 source rows with no mismatch. In this outcome audit,
the actual extracted profile hash and all 28 profile-to-BUILD metadata rows match;
the two guide/manifest rows reconcile the 30-file total. Exact archive contents,
manual fresh extraction, readback/census and final source checks use the reviewed
builder's executed assertions. This audit does not repeat the whole payload and
archive hash campaign.

The builder source is `6bb9bc34c221951ff55f9c7150df3dbdb38fe151d8cbd95de208628403f6bdf9`,
using the existing file helper `9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30`.
This is a Python role distribution, with no Lean/native payload or mathematical
owner requirement. It still requires the selected external Python runtime and
Windows facilities. Three executable/DLL runtime pins do not constitute hermetic
attestation of Python, stdlib, SQLite, TLS or the operating system.

The proper practical comparator is the already qualified Python-only static
`ordinary_inert_mirror02`. This change adds current sparse incremental custody
and indexing to that role separation. It does not newly invent Lean-free hosting.
[BURDEN.md](BURDEN.md) records the selected-file burden comparison; package sizes
alone are not comparative runtime, RAM, adoption or growth evidence.

## Eight focused control groups

The actual `checks/RESULT.json` SHA-256 is
`5824b3557e62f805833de6af2f94d2acc8819e020ecb23708abca97510c71293`.
It binds control source
`70ebfdceb9a86c11f22d78e13a4742a3af7db31308f5918a9eb55ae92a40eef7`
and the actual standalone profile. All eight groups passed:

| Group | Evidence within the reviewed test boundary |
|---|---|
| Profile/source/module binding | Changed profile/source, extra role and preloaded module refusals. |
| Actual pure role | Authentic closure and namespace load; original-budget refusal without renewal. |
| Sparse append | Two actual evidence units / 7,130 bytes retain a support-only unit without requiring global import closure. |
| Postcommit exception | Exception after a real index COMMIT preserves a supported, potentially unreported committed prefix. |
| Lock and old descriptor | Permanent lock contention refuses; the exact retained old descriptor refuses before database open. |
| Static preparation | Sparse static generation works and refuses incremental append. |
| Remote service preflight | Missing remote TLS refuses before listener creation. |
| Cleanup uncertainty | Injected provider start/stop failure drains its owned task while the permanent lock is held and remains a terminal failure. |

The sparse case includes `applyTwice` and `applyFour_eq`, omits `applyTwice_eq`,
and asserts that the omitted unit is a genuine non-foundation import of the
consumer. It therefore exercises actual sparse support, not merely omitted
foundation bytes. The old descriptor is copied into scratch from retained
`incremental-host-public01/suite/host/HOST.json`, pinned at
`45db32b2c53e86b03920ffab2d95fcc31700f40c2a76902899cc0f9ff75058e8`.

The runner records 21 scratch SQLite connections; its passing assertions require
their closure. Native calls, owner calls and application network calls are zero.
The postcommit fault is an injected exception, not a process kill or power-loss
experiment. Cleanup faults use controlled provider substitutes, not a claim about
all possible operating-system failures.

## Actual public lifecycle

The actual `workflow/RESULT.json` hashes to
`8c4dc47cbed3ea47946d7b0ebb0e0cd8f0dd7a07ca654c4c82704f35ca8c6ae8`.
Its runner is
`6786aaae4ae0cc4d5721c87023b414519bf7ad5ce01e42450ab122fac1e31c29`;
`PUBLIC-PLAN.md` is
`347b75f9af95b6f820360e3946a8ddc230e3adae08219c4a6069bd3bcf75d548`.

All four public calls completed once and are `CLOSED`:

| Call | Config SHA-256 | Worker `public/RESULT.json` SHA-256 |
|---|---|---|
| init | `cf49b693763595557cfb4e2e2771caf957a66d0de9517121a2785b9899b6e1cf` | `b77c86cb5144ceff5ba4e88a38877c1a8990bdf57bc01ee674d027a9ad73ef8a` |
| append contribution | `db5b14d4759d849983b75169cf02c10fd6c63406070140e5c3e27b4e080c1ee1` | `604dd2b76d6513c7a6d14972dacaa73cbcb1ccacadc0997bc01556fa34736e7a` |
| append completion | `09dafc9677fde2266536714481140d81feb9df0e818a9757298c07e0f206a4ad` | `fd4b9aa663b35db662b5ccc8e769022376d15903d4767b316bd67c95b30d581c` |
| serve | `176db5ac0b6bdb7797a7b095064f432c65910100456782b5617572adf1d593f5` | `bf77b90e32acba25a276a5ce60b05338ccb4be6af46af60666df8ba6baffa344` |

For each call, this audit compared the workflow's embedded launcher, worker and
supervisor reports with their separately saved files, checked the worker hash
in the launcher, and required equality of launcher/worker result objects and
captured public stdout. Actual config hashes, profile, operation, package path,
single-attempt command and cwd agree. Worker argv equals the original public
argv with the recorded worker/deadline fields; deadline minus original start
equals the original wall allowance. Each supervisor reports exit zero, reaped
child, closed Job, zero active/terminated processes, no forced termination,
cleanup error or stderr. The outer workflow confirms all four children reaped.

Inputs are retained contribution/completion bundles from
`contribution-bundle-controls01/checks/`, rather than new Lean exports:

| Bundle | Units / target exports | Evidence bytes | Manifest SHA-256 |
|---|---|---:|---|
| contribution | 21 / 11 | 379,701 | `78c2f5088d5140d9333d71b701ddd6c9c95bc257fa4d53c8bfdaf9e385c9ceb0` |
| completion | 3 / 1 | 10,700 | `0bd22da5351f0f46ee9ac51ed6b856e8f909a2ed9a00a2c80b50a987b60907c9` |

Both appends report `batch_complete=true`. Final custody has **36 objects**
(24 evidence units and 12 previews), 30 export locators and 453,184 logical bytes;
the index has **12 objects**. The stable descriptor's actual hash is
`7fe567ac310a877bf70f82d7fb9f2871f561b0d72206a8c361bcae35b6f082bb`.
Its identity describes configuration, not current content. The reviewed runner's
passing assertions establish unchanged descriptor bytes and permanent lock inode
through both appends and service. The final index snapshot is
`078406983b67131ccfd237f0ed5d3d9887861cf51509117bc3cb36cfd7da5090`,
distinct from both preceding snapshots.

The saved READY file hashes to
`9c3ab1525dbdbbe8965b67756dafe2e27ced8ad9f8bba32ad0e30fd6cab3b327`
and equals the workflow's READY object. It explicitly says
`prior_append_completion=NOT_ASSERTED_BY_SERVICE`; service readiness alone does
not promote a partial earlier append into a completed batch.

Actual service used `127.0.0.1:61229`, without TLS, for a natural 20-second lease
with a 10-second cleanup reserve. Final status is `LEASE_FINISHED`, quiescent,
not accepting, with no active requests, reserved reply bytes, pending cleanup,
cleanup failures, request failures, refusals or accept failures. Index, custody
and host lock report closed. No remote TLS handshake is exercised here.

Two discovery requests consumed 889 request bytes / 5,489 reply bytes. The
formal declared-type query used no export ID or snapshot in its initial offer,
but was selected from the known fixture. Its match is `CommonsProjectIntake.applyFour_eq`,
export ID `d0c7be50520d2b91b72e43308b8f1ec75022b32c37fe9561381f4aef879fff1a`.
This supports the configured typed discovery route, not independent useful
discovery, broad recall or global corpus completeness.

The four typed acquisitions are bound by the reviewed runner's exact-byte
comparisons to the retained inputs and generated preview:

| Returned object | Bytes | Raw SHA-256 |
|---|---:|---|
| New target preview | 1,351 | `362292c8237bd4cf0f9127ed5575723f188b51efa7ab0a784ac0bf1c1489193c` |
| New theorem | 4,997 | `53c957070a250ac49c9ec46d2fdb091d0967143852546238c4d21d08f7f1506e` |
| Support-only `applyTwice` | 2,133 | `c7266a3047afcf59059b7884853b4d6b9be4244509f260e78dd072973f9704aa` |
| Older contribution `fill` | 7,593 | `d376ec93a92e700a4823668706f06b8fed71b08f8a085bfd3ee18d8bee8ec943` |

Acquisition accounting is closed with four completed responses, zero failed
attempts, pending requests or reserved reply bytes. Its 811 request / 16,074 reply
bytes reconcile with discovery to the provider's **six requests, 1,700 request
bytes and 21,563 reply bytes**. All acquisition/host results retain
`mathematical_acceptance=false`; no native check or mathematical owner was opened.

## Costs and interpretation

| Selection | Outer wall seconds | Job CPU seconds | Outer wrapper CPU seconds | Known inclusive CPU seconds | Peak Job private commit bytes |
|---|---:|---:|---:|---:|---:|
| pack01 | 1.1203215 | 0.28125 | 0.109375 | 0.390625 | 19,255,296 |
| controls01 | 1.3256411 | 1.015625 | 0.078125 | 1.09375 | 27,799,552 |
| public01 | 25.4815222 | 5.546875 | 0.296875 | 5.84375 | 86,532,096 |

Combined known inclusive CPU is **7.328125 seconds**. Nested builder, harness,
worker, launcher and supervision CPU values are already included and must not
be added again. The public service's lease explains most wall time. Runs can
overlap; the wall figures are not an elapsed-project-time sum. Peak Job private
commit is neither a simultaneous whole-PC RAM census nor a comparative memory
benchmark. Audit/model/human effort and other external costs are not included.

The outer ceilings were respectively 60/30 seconds wall/CPU with 256 MiB and one
simultaneous process; 180/90 with 768 MiB and one; and 240/90 with 1,024 MiB and
four. The nested public `--cpu-seconds` budget applies to the worker Job. Its
trusted parent has a separate cooperative `min(60, cpu_seconds)` allowance;
there is **no standalone aggregate hard parent-plus-worker CPU cap**. The outer
test Jobs enclose these costs but do not strengthen that public contract.
Original deadlines persist through setup, worker execution, lease and cleanup;
sampled CPU/wall/log enforcement and trusted-host limitations remain as reviewed.

## Disposition

The selected standalone role has exact distribution evidence, focused refusal
and partial-prefix evidence, and actual public no-Lean incremental service
evidence. It removes a concrete operator dependency while preserving the current
wire protocol and keeping mathematical authority in the consumer's chosen
checking path. It is suitable for root's scoped adoption decision.

No new support for migration of old profile-pinned roots, Linux/macOS operation,
hostile-source sandboxing, independent hosting, custody permanence, broad search
quality or useful mathematical growth is inferred. Finite retained-fixture
operation is not a release-completion criterion for the whole commons. Root owns
adoption, integration and the next high-payoff decision; full v5 remains active,
local and unpublished.
