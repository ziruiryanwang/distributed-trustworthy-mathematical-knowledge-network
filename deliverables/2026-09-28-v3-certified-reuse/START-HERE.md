# V3 continuation: certified reuse without ancestral proof replay

28 September 2026, Chicago. **Local certified-reuse checkpoint, not full-v3
completion.** The ordinary-source child now has an independently audited final
certificate and a downloadable sample accepted by the packaged receiver.
The authentic unresolved-premise control was refused. Installed preparation
has separate post-hoc compatibility evidence; its prospective byte-oracle test
remains failed. This is a separate continuation of the preserved
[02:43 tentative handoff](../2026-09-28-v3-tentative/START-HERE.md), not a
rewrite of what was available before 03:00. Nothing is published externally;
licensing remains undecided and native v2 is unchanged.

## The redesigned contract

The system must not require a recipient to download or replay all the proofs
behind an imported lemma. A content hash, signature, popularity score or entry
in a blockchain alone cannot establish that property together with mathematical
validity. The selected mechanism is an exact formal interface accompanied by
a recursively composed certificate of checking.

For a selected foundation and checking profile, the intended rule is:

```text
Each imported interface T_i has a valid certificate under that profile.
The new proof p checks as U with exactly those compatible premises.
Every imported-premise assumption is discharged in the new certificate.
------------------------------------------------------------------------
U has a certificate that a new recipient can check without replaying p
or any ancestor proof.
```

This implication is conditional on the adopted checker's fidelity, foundations,
interface interpretation and cryptographic soundness. The current experimental
implementation does not establish all of those assumptions for general Lean.
It does exercise real checking, real proof production and real verification;
an intermediate success record is never a substitute certificate.

| Role | Mandatory selected data | Not a mandatory input |
|---|---|---|
| Receiver | Trusted local profile, exact interface, application claim, final certificate | Ancestor proof bodies, global ledger, complete corpus |
| New contributor | New source/proof, immediate parent interfaces/certificates, needed authenticated computational support | Transitive parent proof archives |
| Search/index | Selected descriptors and retrieval metadata | Authority to declare a theorem valid |
| Archive/custodian | Whatever exact objects it undertakes to retain | A complete copy of all mathematics at every node |

The quantitative design target is selected interface/support/certificate work,
not work proportional to unrelated corpus size or ancestral proof bytes. That
is not a constant-time promise: statements, direct premise sets and necessary
definitions can themselves be large. If a computation requires unsupported
proof-body unfolding, the sealed profile must refuse or use an explicitly
different, separately costed path; it must not silently fetch the whole history.
No node can remain fully informed of unbounded new information for free.

Proof archives remain valuable for independent native audits and regeneration
after a checker or cryptographic-profile upgrade. Removing them from mandatory
receiving does not make those recovery tasks free: a certificate under an old
profile is not automatically a certificate under a new one. Selected archives
can be replicated by several holders without requiring every node to store all
mathematics.

## Actual mathematical example

The existing ordinary Lean child uses a certified equality-preservation lemma
twice:

```lean
theorem CommonsV3.compose_congr
    {alpha : Sort u} {beta : Sort v} {gamma : Sort w}
    (f : alpha -> beta) (g : beta -> gamma)
    {x y : alpha} (e : x = y) : g (f x) = g (f y) :=
  ScaleIface.L g (ScaleIface.L f e)
```

The conditional native import contains L's exact proposition but no L proof
body. The child's new packet is 6,983 bytes; its framed checking input is 7,639
bytes. Its completed research campaign has 31 segments and one distinct parent
assumption. A genuine resolve step discharges that assumption before final
receipt construction and fresh cold verification. This is a small ordinary
source example, not a novel discovery or evidence of useful knowledge growth.

The final receipt is 223,522 bytes, the same size as the parent receipt in
this sample. Its SHA-256 is
`14e0a6d6e0ffbfab9990d03c879bb24cf02dd176639e5c4e56011aa0fa3dde35`.
The claim is 148 bytes and the child interface capsule is 2,356 bytes.
Equal receipt size for two examples is supporting evidence, not by itself an
asymptotic theorem or a large-network benchmark.

The extracted packaged receiver accepted this final rank-one certificate.
It also rejected a second receipt containing the **unchanged cryptographic
payload** of the actual last join, which still had one unresolved premise.
The SDK reached its claim-digest comparison after integrity checking and
refused it. This control is not a broken-seal, malformed-file or mocked test.
It tests one causal boundary; it does not establish general recursive security.

## Try the genuine child sample

- [Existing qualified receiver ZIP](../../product-local/certified-verifier-package-01/mathematical-commons-v3-receiver.zip), 56,577,912 bytes.
- [New child sample ZIP](child-bundle.zip), 223,416 bytes; four flat files,
  226,706 bytes uncompressed. It contains the completed child, not a partial
  proof or the negative control.

Receiver SHA-256:
`db862cc0c0b86a53d7f9e47c9c5c32ba4cc4406f805d1f08d6fb37b78b4f9ec4`.
Child archive SHA-256:
`9953f6348903ff03f6f6e4c14ec2f5cc9143934cda01c3068590ef6d41b7eb18`.

Use the existing [Windows receiver instructions](../2026-09-28-v3-tentative/RECEIVER-USAGE.md)
with these three replacements in their first PowerShell block:

```powershell
$v3SampleArchive = Join-Path $v3Project 'deliverables\2026-09-28-v3-certified-reuse\child-bundle.zip'
$v3SampleSha = '9953f6348903ff03f6f6e4c14ec2f5cc9143934cda01c3068590ef6d41b7eb18'
$v3UseRoot = Join-Path $v3Project 'product-local\receiver-child-operator-01'
```

All checksum, fresh-directory, profile and invocation checks stay unchanged.
The old guide's extraction-folder name `lemma-L` may remain: it is only a local
folder label; with this archive it contains the child. The formal capsule and
claim, not that folder name, determine the theorem. No separate Python or Lean
installation is needed for receiving. Do not run into an existing output
directory or edit a retained result. These instructions are for an optional
operator check, not another research campaign run by this handoff.

## Costs and the claim we can make

The completed child research campaign took 3,847.79 seconds of sampled wall
time, about 64.13 minutes. New charged subprocess CPU was 34,315.109375 seconds,
plus 70.1875 seconds of outer controller CPU. Its declared cumulative charge
is 71,350.75 CPU seconds, including 36,965.453125 carried from parent production,
failures and the selected child preparation history. Earlier backend/build,
installation, model and audit work are separately retained, not zero.

The actual complete positive child receiver command took 6.6670 seconds wall
and 1.375 inclusive CPU seconds in this single shared-host observation. Its
inner cryptographic timer was 13 ms, **not** total receiver latency. Both
receiver controls and their supervisor together took 21.1237 seconds sampled
wall and 6.484375 known CPU seconds. These are not matched throughput trials.
The receiver's fixed roughly 97 MB installed closure is still hashed before
and after checking; no ancestor proof files are required by its call.

This is far too expensive to present as affordable certification of such a
small theorem. Cheap receiving and expensive production are both real facts.
The design removes compulsory ancestry replay; **net speedup and faster useful
accumulation are not established**. A matched resource comparison must include
new certification, discovery/import, repeated consumption, failures and setup.
Let R be matched full baseline consumption cost, V full certified consumption
cost (including wrapper/import), and G+F the incremental extra certification
and setup cost, all in one chosen resource measure. Break-even requires
m(R-V) > G+F; if R<=V and G+F is nonnegative, no finite m yields savings.
No measured break-even m is asserted here.

## Installed contributor: distinguish execution from test outcome

The public contributor exposes separate `prepare` and bounded `advance`
operations. Its source and twelve changed-boundary contract groups have been
independently reviewed; those tests used fake workers and are not proof
production. The copied installation passed its full file-identity audit.

The first real integration attempt stopped in its test launcher before any
public worker ran: the launcher requested an unsupported active-process bound.
The corrected launcher preserved the original finite deadline and budgets.
Its one public `prepare` then executed real parent verification, conditional
ordinary-Lean export and a fresh coherent snapshot, reaching closed READY.
No `advance` or new certificate was produced by that installed invocation.

The outer prospective test nevertheless **failed**: it expected the public
capsule to have the native serializer's final newline. Read-only diagnosis
shows exact equality of every preceding byte and unchanged proof packet,
checking input and journal; the two source writers intentionally differ in
that final LF. The failure is retained. A separately identified post-hoc
saved-output audit, not an edited result or rerun, **confirms the narrow
installed prepare compatibility**. It checked all remaining actual workers,
markers, limits, closed records, exact data, retained charges and pins after
the failed comparison. The fresh snapshot has 31 segments / one assumption;
the state has no completed proof stages and no bundle. This is post-hoc
qualification under the source-justified encoding relation, not a passing
prospective oracle trial. Full installed proof production is still unqualified.

The observed successful public process tree consumed 34.734375 inclusive CPU
seconds. The failed outer gate's final controller sample was 2.234375 CPU
seconds and 37.7145 wall seconds. The first prelaunch failure cost 3.5 controller
CPU seconds / 3.9440 wall seconds; its raw 2,000-second conservative worker
reservation is retained but is not measured execution. These costs are separate
from the earlier child-certification campaign, not hidden inside it.

- [Public contributor API](../../product-local/certified-companion-source-03/CONTRIBUTOR-API.md)
- [First actual launcher failure](../../experiments/certified-contributor-03/PREPARE-OUTCOME.md)
- [Exact encoding diagnosis](../../experiments/certified-contributor-03/PREPARE02-DIAGNOSIS.md)
- [Raw failure and independent saved-output compatibility audit](../../experiments/certified-contributor-03/PREPARE02-OUTCOME.md)

## Central remaining work

1. Affordable certification and a fully qualified installed contribution path.
   Do not reprove the completed example merely to gain a different label.
2. Broader authenticated definitions/inductives and demand-driven computational
   support. The current profile permits new Prop-valued theorems over only its
   fixed support vocabulary (43 records / 66 names); it is not a growing Lean
   library yet.
3. Assurance for the exact guest-to-Lean interpretation and the actual accepted
   recursive verifier suite. Finite tests are not a general correspondence or
   production cryptographic proof. The receiver reports native_admission=false.
4. Integrating certified objects into the decentralized discovery/custody loop,
   followed by meaningful costed reuse comparisons. The experimental receiver
   is separate from the native-v2 peer node; no global-scale deployment was run.

Independent agents still choose their own investigations. There is no network
task list, human-intention acceptance rule, mandatory author identity or central
consensus service. Validity, availability, usability and usefulness stay separate.

## Detailed evidence and specifications

- [Layered architecture](../2026-09-28-v3-tentative/SCALE-ARCHITECTURE.md)
- [Dataflow and scale contract](../../research/cycles/v3-2026-09-27/SCALE-DATAFLOW.md)
- [Implemented locality audit](../../research/cycles/v3-2026-09-27/IMPLEMENTED-LOCALITY-AUDIT.md)
- [Exact assurance boundary](../../research/cycles/v3-2026-09-27/CERTIFIED-PROFILE-ASSURANCE.md)
- [Actual ordinary-child certificate audit](../../experiments/certified-importer-probe-02/CHILD-CERTIFICATE-OUTCOME.md)
- [Actual child receiver audit](../../experiments/certified-child-receiver-01/OUTCOME.md)
- [Live research desk](../../research/NOW.md)

The earlier architecture's pending-status text is historical. This dated
continuation adopts only the explicitly scoped audited capabilities above;
it does not retroactively qualify an earlier deadline or the whole project.
