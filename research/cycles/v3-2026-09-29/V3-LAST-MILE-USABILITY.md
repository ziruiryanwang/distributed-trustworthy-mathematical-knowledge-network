# V3 last-mile usability: bounded source/document review

2026-09-30 UTC. Reviewer `/root/contributor_plan`; canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root owns the six mutable delivery documents. This review owns only this
checkpoint. No guide, installation, used source or evidence was edited.
No import, compilation, test, proof, network, credential operation or package
rehash campaign was performed.

Read all six documents under `deliverables/2026-09-30-v3-tentative`:
START-HERE, OPERATING-GUIDE, LAYERED-GUIDE, RESULTS, CORE-ISSUES and
ASSURANCE-AND-SCALE. Checked consequential syntax/support claims against
selected public contributor API, shipped workflow/importer, shipped receiver,
peer API and already-read peer sidecar. This is a source/document consistency
review, not a fresh-operator execution or release qualification.

## Highest priority: do not manufacture an external-supervisor prerequisite

OPERATING-GUIDE section2 currently says to use a separate process-tree
supervisor for network/owner-work operations, then says contributor/receiver
surrounding sequence and process supervision remain operator responsibility.
A new operator can reasonably infer that the base/contributor packages cannot
be used until they implement additional software. That is not what the public
interfaces require under their cooperative ownership assumptions.

Concrete source evidence:

- `app/receiver/cert_verify.py` has a Controller for wall/CPU/private-memory
  observations; it creates a finite Job for its one real verifier, launches
  hidden/suspended with attach-before-resume, samples job/log/storage bounds,
  and requires direct-child/Job quiescence and clean closure.
- Public `cert_workflow.py`/`cert_stages.py` retain the chosen operation CPU
  budget and deadline across invocations, precharge controller allowance,
  reserve each worker before launch, use finite suspended-start Jobs and
  fail on uncertain closure. The selected API's Cost and integrity policy
  explicitly describes this. A new wrapper is not a CLI prerequisite.
- The separate `peer_run.py` now supplies the peer/route per-command envelope.
  Its nine-group/one-client-init qualification does not qualify TLS serving,
  receipt checking, contributor completion or a shared sequence budget.

Recommended documentation correction: distinguish the three public launch
contracts. Run peer/route commands through the separately adopted sidecar (or
an equivalent intentionally selected owner supervisor). Run the shipped cold
receiver and contributor through their documented direct CLIs: their existing
per-operation controller/worker bounds apply. An additional enclosing supervisor
is optional when an operator wants an aggregate sequence budget or stronger
parent-process containment. Do not imply it is supplied by peer_run, a hostile
source sandbox, hard-real-time controller bound or combined-tree memory cap.
No new mechanism or runtime is needed to correct this wording.

## Concrete launch-template omission

The supplied-supervisor paragraph says to invoke the base Python with
`-I -S -B --plan ... --plan-sha256 ...` but omits the sidecar script position.
The linked frozen guide has the complete command, so this is not a product bug;
the main walkthrough should not force a novice to reconstruct it or suggest
that Python itself accepts `--plan`.

Use an explicit illustrative command, for example:

```powershell
& $mcPython -I -S -B '<absolute-peer_run.py>' --plan '<absolute-plan.json>' --plan-sha256 '<independently-adopted-plan-sha256>'
```

Also state that plan `argv` begins with `--config`, not the Python executable,
flags, script path, `&`, or a shell command string. The direct peer snippets
show inner syntax; that distinction already exists in prose but the complete
wrapper invocation makes it actionable. The main operating text correctly
restricts the sidecar to peer/route and gives source-only-guide-history versus
actual-qualification scope; retain that distinction.

## Scope the terminal-evidence wording to its actual API

START-HERE currently says “All saved PASS records require matching terminal
events and actual exit0” inside the peer-sidecar paragraph. In that local
context the intended point is correct, but “all” can be read across the whole
release. The peer envelope's final event contains definitive status/exit_code;
the shipped contributor and cold verifier final telemetry have different
schemas and do not carry those fields. Their public success predicates also
involve their own output/state/actual exit, not a fabricated peer-envelope
terminal object.

Recommend “For this peer launcher, saved RESULT/stdout are preliminary; require
the matching final event and actual exit0.” Keep the contributor's READY versus
COMPLETE record and cold receiver's actual verification predicates in their
own sections. This avoids asking users to find nonexistent status fields or
assuming the sidecar encloses contributor/cold commands.

## Bridge the central acquire-to-use step with existing material

The guide explains prepare/advance well, but gives only an owner-source path
placeholder. A new undergraduate reader cannot tell how a selected acquired
formal interface becomes a Lean declaration usable in that source. This is a
documentation gap in the central loop, not a request for a natural-language
interface, tactic framework or another experiment.

The existing, actually prepared `experiments/certified-collection-01/OwnerChild.lean`
is only479 bytes and directly applies `BatchProbe.left_inverse_injective`
twice to prove composition injectivity. The shipped importer installs each
selected capsule's exact declaration name/universes/type as a body-free premise,
then elaborates owner source in that environment and freshly checks its root.
It does not ask the owner to invent an axiom or copy parent proof source.

A short worked, **read-only explanatory** example or link to this already-used
source would show: the acquired parent's selected name is already available;
the owner theorem applies that name; `--root-name` selects the new theorem;
`--parent` supplies the exact acquired bundle; prepare is still not a final
certificate. Do not present this as a new runnable workload, novel discovery
or general mathlib support. If an operator wants to inspect unfamiliar capsule
encoding, cite the selected format/API rather than pretending a pretty-print
or semantic-search command exists. No new runtime campaign is warranted.

## Small claim/teaching corrections worth making before seal

1. LAYERED-GUIDE ends “A tentative v3 is a usable bounded release” while the
   central production/return gates are explicitly pending. Prefer “The intended
   tentative v3 is a bounded experimental release; the support report determines
   which paths are actually qualified.” This preserves real component usability
   without prematurely claiming a completed usable contribution loop.
2. Define `Prop` once as Lean's sort of propositions, and `same-image` as all
   recursive certificates using the same adopted checker executable identity.
   Explain that `journal.bin` is a small certificate's public claim, not the
   blockchain-like global ledger that the project deliberately avoids.
   These are short explanations of the existing design, not extra mechanisms.
3. At the final seal, synchronize the precise producer frontier and chosen
   return adapter in OPERATING-GUIDE/RESULTS. During this mutable review the
   first28/READY4 statements are historical current-text snapshots; root has
   newer raw005 evidence pending actual audit. Do not promote that raw progress
   until adoption, and do not present the old unrun prefix adapter review as
   review of the new enveloped adapter. No duplicated campaign is needed.

## What is already clear and should not be diluted

The documents correctly distinguish hash/custody/index metadata from real
receipt acceptance; disclose fixed-support Prop, no general new definitions/
mathlib, same-host evidence, undecided license, no exponential-growth evidence,
and unresolved construction-specific correspondence/recursive assurance.
They preserve routed FAIL plus same-copy cold completion as a composite rather
than a single passed allocation. They state bounded incomplete lookup and no
mandatory global ledger/ancestral proof download. Native v2 is a different
trust/replay lane; old TLS identity-helper guidance is explicitly not a v3
native-build or node migration instruction. No central server or hidden
all-corpus fallback is introduced by the operator examples.

No selected public CLI argument mismatch was found in the examined offer/find/
acquire/serve, routing or contributor templates. Paths are expressly
illustrative and require ordinary existing parents/fresh operation targets.
The priority corrections above concern real operator decisions and misleading
invocation/scope wording, not a peripheral feature wishlist.

Disposition: `DOCUMENT_SOURCE_REVIEW_WITH_ACTIONABLE_LAST_MILE_CLARIFICATIONS`.
Root must decide and edit mutable guides; this checkpoint does not seal them.
