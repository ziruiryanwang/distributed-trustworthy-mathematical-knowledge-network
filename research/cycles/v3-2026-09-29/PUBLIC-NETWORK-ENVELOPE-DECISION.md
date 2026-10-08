# Smallest missing public network execution envelope

2026-09-30 UTC; `/root/census_review`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
**Source-only recommendation; no implementation/runtime/package change selected.**
Preempt this investigation for the actual prefix003 outcome when root supplies
its terminal evidence. No live proof output was inspected in this assessment.

## Decision in one paragraph

Ship a small **relocatable, one-command Windows supervisor for the two existing
peer CLIs**, using the already packaged, pinned Windows Job primitive. It
launches exactly one selected public peer command, owns its descendants and
finite lifetime, records its raw output and measured termination, and never
claims mathematical acceptance. A serving command is itself one supervised
command. No research scheduler, daemon manager, network orchestrator, new TLS
identity helper or alternative peer protocol is needed. The current sealed/
used base package remains unchanged; this requires a separately selected
small successor/add-on and qualification of that new seam before delivery.

## Why this is a central operability gap

The current `deliverables/2026-09-30-v3-tentative/OPERATING-GUIDE.md` lines113–119
requires an external finite supervisor and preserved output/cost records.
The packaged peer `CERTIFIED-NETWORK-API.md` lines50–58 and315–344 likewise
requires outside CPU/memory/wall/process containment; internal parsing/service
deadlines are sampled, not a complete process envelope. The experimental
adapters supplied it during qualification, but they are rooted in this project,
fixed allocations/topologies and retained evidence. A fresh downloader cannot
reproduce that boundary from the ordinary CLI examples alone.

This is neither a flaw in theorem acceptance nor evidence that current tests
were unsupervised. It is missing reusable public execution plumbing. Requiring
every operator to author a trusted launcher makes fresh-user operability
conditional on additional software not supplied by the product.

## Reuse exactly the useful existing primitive

The base archive already includes
`app/receiver/helpers/run_stage.py` (30037bytes/SHA
`bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028`),
its pinned `helpers/domains.py` dependency, packaged Python and DLLs.
Its `Job` class at208–275 supplies:

- Windows Job user-CPU limit, private-commit limit, active-process cap1..8
  and kill-on-last-handle-close;
- suspended-process assignment before resume;
- aggregate user+kernel CPU, cumulative/active/terminated counts and memory
  observations, explicit kill and close with surfaced failure.

Its **existing execute/main is not a drop-in peer launcher**. It requires
legacy `install/py/domains.py` and `install/py/run_stage.py` origins, schema2
stage domains, mandatory Lean runtime/executable pins, at most300seconds and
a one-active-process stage Job. The packaged receiver instead keeps helpers
under `helpers/`, and peer-only users need no Lean installation. Copying the
legacy plan format or changing its frozen paths would create needless coupling.
Use the pinned `Job` class, not that `execute` function or an old experiment's
main. Load its required `domains` module from its exact checked path; do not
make the legacy Domains object or add legacy directories merely to satisfy it.

The packaged `cert_verify.py` has reusable bounded `Controller` and exact-path/
pin utilities. Its `Installed` class intentionally adopts mathematical verifier
policy, loads capsule/bundle modules and resets controller limits to receiver
defaults. A network launcher should reuse only the needed checked primitives,
not instantiate `Installed` to accidentally impose verifier semantics/limits
or make peer launching a cryptographic verification operation. The existing
reviewed completion adapters demonstrate the primitive-loading/cleanup pattern;
their project-specific constants and main functions are not public interfaces.

Only `cert_peer.py` and `cert_route.py` have public entry points in this lane.
`cert_index.py` remains a library. No arbitrary executable, shell command,
`python -c`, new proof driver or imported peer module is needed in the outer
process. The child receives the normal installed public API unchanged.

## Minimum public contract

The operator adopts an immutable release manifest and supplies a bounded,
SHA-pinned run plan. Its essential information is the ordinary absolute package
root, entry-point enum (`peer` or `route`), exact peer config pin and optional
routing config pin, existing subcommand arguments, fresh result directory and
explicit finite limits. A package/profile pin is selected by the operator,
never by peer metadata. Relative executable/helper paths resolve against the
adopted extracted package, not cwd, this project or `D:\Python314`.

Construct the executable as packaged receiver Python plus fixed `-I -S -B`
and the chosen packaged entry point. Bind configuration arguments once;
reject duplicate/overriding reserved flags, unknown entry points, arbitrary
interpreter flags, nonfinite/invalid limits, escaped/reparse/overlapping paths
and reused output allocations before launching. Ordinary peer argument
validation remains with the public child CLI; the supervisor need not
reimplement proof, index or network protocol semantics.

The default operating shape is one foreground supervisor. Its child is hidden,
suspended, attached to one Job and only then resumed. Close inherited handles,
use DEVNULL stdin and a controlled child PATH containing adopted runtime/bin/
DLL directories plus System32; no host-runtime fallback. Child stdout/stderr
go directly to bounded owned files, not unbounded pipes. A flushed readiness
line can be inspected there; do not introduce an extra network readiness probe
that consumes a finite service's request allowance.

For a multi-process local example, each explicitly started command gets one
such envelope. A listener and client can therefore overlap without a new
multi-service orchestration API. **Per-command bounds do not imply a global
machine budget**: running m envelopes permits roughly m separate allowances.
This limitation must be visible. Root's finite multi-service test harness can
retain its own aggregate outer Job; no production Job16 change is implied.

The run record binds exact release/plan/config/helper/argv/cwd inputs, original
limits, child exit, raw log pins, observed totals and final cleanup. An outcome
such as `COMMAND_EXITED_ZERO_WITHIN_OBSERVED_ENVELOPE` means only that. An inert
peer result stays `receipt_verified:false`; a supervisor PASS never manufactures
proof acceptance, service availability after exit, or a successful transaction.
Even zero exit does not prove the caller's desired query/acquisition succeeded:
agents must inspect the preserved public result status.

## Safety and scalability boundary

Count one direct command, but measure all descendant Job processes. Preserve
the documented difference between active and cumulative limits: the actual
Windows runs can count two processes for one direct Python invocation. Use a
prospectively selected cap within the existing helper's1..8 active range and
an explicit cumulative cap; do not infer process identities from the counter.

The Job's configured time limit is **user CPU**. The controller must separately
sample total user+kernel CPU, wall deadline and output bounds, and refuse an
overrun even if the child later exits0. Memory/process containment and
kill-on-close are kernel mechanisms; total-CPU/wall/log observations may
overshoot and are not hard real-time enforcement. Controller CPU/memory are
separate bounded observations, not silently included in child Job totals.

Normal child completion is insufficient until the entire Job is quiescent.
On error, overrun, cancellation or attachment failure, retain evidence and
kill/wait the Job with direct-process fallback. Unknown launch or accounting
coverage is a failed/unknown outcome, conservatively reserved, not zero cost.
If final measurement, immutable binding, closure or result persistence fails,
do not emit success. Parent-process death should kill children through the
noninherited Job handle; that critical property needs an actual descendant
test, not just a source claim. This remains cooperative trusted-runtime/local
owner execution, not a sandbox against a hostile administrator or privileged
code escaping the platform's Job assumptions.

Do **not** add repeated recursive censuses of the persistent peer corpus,
catalog/history or proof ancestry. They would reintroduce a large-network
cost unrelated to the selected operation. The launcher needs bounded plan/
config/manifest/source checks, logs and a small fresh run directory; peer
state growth remains governed by existing transaction/frame/page/blob limits.
SQLite journals and transient disk usage are not magically covered by those
logical limits or the Job's memory cap. A hard disk quota remains an external
OS provisioning concern; disclose that rather than claiming complete physical
storage containment. No credential-file copy, plaintext logging or new identity
provisioning belongs in this launcher. Public config metadata suffices outside
the existing child TLS loader.

## Minimum qualification before calling it downloadable and usable

Use a fresh selected source/add-on, preserve current package and unchanged
proof/runtime bytes, then perform **one bounded changed-boundary campaign**.
Do not rerun the costly mathematical certificate or full routed corpus tests.

1. **Static selection review:** exact one-command construction and imported
   helper origins; no mutable cwd/peer-data code selection; suspend/attach/resume
   ordering; combined CPU versus user-CPU semantics; cleanup/direct fallback;
   strict path/plan/config/input/log handling and terminal-result precedence.
   Explain every source/manifest delta and reserve output accounting space.
2. **Native-free contract cases:** reject bad pins, duplicate keys/reserved
   args, invalid caps, wrong entry point, reused/reparse/overlapping output and
   package paths, and unsupported host before a child. Check zero exit without
   quiescence, nonzero child, late overrun, failed attach/measurement/close and
   result-persistence errors cannot yield PASS. Test seams must not add a public
   arbitrary-executable/test-mode escape to the shipped launcher.
3. **Real Windows containment controls:** small pinned disposable cooperative
   fixtures exercise actual normal child closure, descendant lifetime,
   parent-termination kill-on-close, wall overrun, CPU/memory/process limits and
   output overrun, with final no-survivor observations and honest overshoot/
   failure records. Reuse existing audited helper controls where bytes and
   binding are unchanged; execute only unresolved launcher-boundary cases.
   Fixtures are separate qualification code, not production allowlisted tools.
4. **Actual relocated public seam:** a fresh extraction/add-on at a different
   ordinary path, using only bundled Python/helpers, successfully runs a real
   harmless public peer initialization/query and one finite real service/client
   exchange under the launcher. Reuse an already adopted test identity when
   root selects it; no new credentials or theorem proof. An empty-shard query
   or retained valid bundle is sufficient—the changed claim is containment/
   relocation/output preservation, not new network mathematics. Verify real
   readiness logs, unchanged child JSON, exact selected interpreter/config,
   ordinary and forced-stop closure and no unowned survivors.
5. **Independent outcome/package handoff:** bind actual final launcher/maps/
   archive or add-on, saved successes and failures, measured costs and a short
   documented invocation runnable without experiment files or project paths.
   Unchanged peer protocol/theorem evidence is adopted by exact-byte identity,
   not declared re-proved. A source-only proposal cannot close this gate.

Tests in item3 must be chosen against existing evidence rather than becoming
a new exhaustive operating-system test suite. At minimum the new launcher
must demonstrate ordinary actual child execution and real forced descendant
cleanup, plus the actual public relocated service/client seam; failing or
unknown branches remain explicit. No global reliability, hostile-code disk
isolation or independently hosted deployment claim follows.

## Shipping choice and stop condition

The smallest releasable change is a separately pinned launcher/add-on plus
its finite plan example and public guide; it can refer to the already sealed
base archive rather than rewriting the2.35GB contributor distribution. A fresh
base-only successor is also possible if integration is simpler, but is not
selected here. Either way, final bytes must include the launcher and identify
the exact compatible base/profile/portable maps. Do not instruct users to copy
an unversioned research adapter or silently change a used package.

Close this issue only after the downloadable artifact and the above scoped
changed-boundary evidence exist. Until then the honest release statement is:
**peer commands are available, but fresh-user finite outer supervision still
requires externally supplied code**. This gap is central to usable network
operation, while cryptographic trust, proof-production cost and useful-growth
evidence remain separate open questions.
