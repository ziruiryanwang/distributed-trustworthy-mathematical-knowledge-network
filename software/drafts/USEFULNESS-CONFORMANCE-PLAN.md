# Smallest vocabulary conformance discriminator

2026-09-21. Source-only plan; no imports, compilation, SQL, network or test
execution. This does not commission consumers or change the matched trial.

## Selected next action

Use the existing public product commands on **one fresh installation and node**:
build, configure, initialize, submit the exact vocabulary, publish. Five commands,
three ordinary requests, two mathematical stages. No service, peer transfer,
new scenario framework, extra theorem, inspection request or synthetic acceptance
is needed to answer this particular question.

`submit` already executes source elaboration/capture, canonical capture, fresh
candidate replay, inverse export and fresh inverse replay. Its returned
`description.rows[0].leanName` is the actual canonical receiving name, not the
source name `Reduction`. Publication reauthenticates that complete five-child
pipeline and commits a portable candidate. This is stronger than a standalone
`lean UsefulnessVocabulary.lean` test and uses the actual agent interface.

This minimal run does **not** claim independent-node admission. Both eventual
consumers still need separately checked onboarding with the identical published
vocabulary, and the producer/corpus/catalog readiness gates remain outstanding.

## Exact input and source-supported risk

Submit the current `drafts/UsefulnessVocabulary.lean` unchanged: **207 bytes**, SHA-256
`B3D65406FA204268F74BB3CBDCD623991127AA5D3CCC06595C63890F9FD9E48A`.
It has five LF characters, no CR/BOM, root `Reduction`, and no lemma/target proof.

Read-only decoding of the selected seed/inventory establishes these seed indices:

| Name | Index | Inventory kind |
| --- | ---: | ---: |
| List | 31 | 4: inductive |
| List.map | 317 | 1: definition |
| List.nil | 318 | 5: constructor |
| List.rec | 319 | 6: recursor |
| List.cons | 320 | 5: constructor |
| List.append | 322 | 1: definition |
| List.flatten | 327 | 1: definition |

`List.rec` has universe arity 2, one parameter, no indices, one motive, two
minors/two rules, `k=0`, `unsafe=0`. `SourceCompiler` initially maps every seed
name to `[0,index]`; its resolver uses that binding directly. The unsupported
nested-auxiliary-recursion selector concerns new exported groups, not this
ordinary reference to an existing seed recursor. `AgentReplayCore.receive`
reconstructs/checks the seed and installs those same bindings before source
elaboration or replay. Thus **no List.rec kernel/codec blocker is established
by source inspection**.

Execution is nevertheless essential: the reconstructed environment is not a
normal imported Lean project. Binder names, named argument `(motive := ...)`,
universe inference and parser support must work in this exact frontend.
Canonical DAG encoding omits user binder names, and generated recursors are
reconstructed by the kernel; presence in the seed does not by itself certify
this source spelling. Preserve the first failure; do not silently switch to a
positional-recursion spelling during the allocation.

Relevant immutable inputs: seed 724174 bytes, SHA-256
`A0ACDC706F5E42DCA21950C14DB2307A18955C63FF953019AAFF413D0A976001`;
inventory 823690 bytes, SHA-256
`C81800ABBE3F421B2E3D3687E864946E9C0DD43A97A118034C79376F7CDBA1B0`.
These are supporting read-only observations, not a new acceptance certificate.

## Allocation and exact public commands

Prospective roots, absent at this source inspection:

- `E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\usefulness-vocabulary-01`
- `E:\Distributed Trustworthy Mathematical Knowledge Network\software\qualification\usefulness-vocabulary-01`

Preferred combined path: after source-package contract qualification, root runs
the existing `release/package_source.py` CLI once, retains its actual archive/
manifest/result evidence, and verifies fresh extraction into this `install`
child against every manifest member. The currently intended package has 108
source/document files; use the actual selected manifest, not that count alone.
No installer qualification is presumed merely because a ZIP was made. This
lets the same five product commands test package-to-build-to-portable-vocabulary
operation while keeping packaging/extraction evidence distinct from mathematics.
The builder/extraction are separately accounted preparation, not extra ordinary
requests or mathematical stages, and are not included in the five-product-command
count. The retained endpoint census includes any new package/extraction evidence
charged to this preparation; do not silently exclude an external output root.

Root freezes the source/package manifest, this input and runtime pins before
using the fresh installation. Copy/extract only selected raw product sources,
assets and documentation; no support binaries, databases, prepared contexts or
old experiment outputs. If packaging readiness is not yet established, the
existing reviewed source-copy checks remain an alternative preparation route,
not a reason to execute/import an old scenario driver. Revalidate absence and
non-reparse/disjoint exact paths before allocation. Neither route changes the
mathematical source, acceptance pipeline or matched consumer trial.

The following variables name **selected future paths**, not existing results:

```powershell
$vocabRoot = 'E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\usefulness-vocabulary-01'
$vocabInstall = "$vocabRoot\install"
$vocabRuntime = 'E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows'
$vocabPython = 'D:\Python314\python.exe'

& $vocabPython -B -E -s -S "$vocabInstall\build.py" --lean-runtime $vocabRuntime --work "$vocabRoot\build-work"
& $vocabPython -B -E -s -S "$vocabInstall\manage.py" configure --state "$vocabRoot\state" --scratch "$vocabRoot\scratch" --lean-runtime $vocabRuntime --client local --initial-requests 3 --initial-stages 2 --initial-reserved-mib 280 --initial-metadata-mib 32
& $vocabPython -B -E -s -S "$vocabInstall\manage.py" request --config "$vocabRoot\state\config.json" --request "$vocabRoot\requests\init.json"
& $vocabPython -B -E -s -S "$vocabInstall\manage.py" request --config "$vocabRoot\state\config.json" --request "$vocabRoot\requests\submit.json"
& $vocabPython -B -E -s -S "$vocabInstall\manage.py" request --config "$vocabRoot\state\config.json" --request "$vocabRoot\requests\publish.json"
```

Issue them sequentially with the gates below; do not paste-run past a refusal.
Root authors each immutable UTF-8 JSON request before its invocation, replacing
only the response-bound handles shown below. No handle is guessed. The JSON
`source` value must decode to the exact 207-byte input above.

```json
{"client":"owner","request_id":"vocab-init","op":"init","args":{}}
```

```json
{"client":"local","request_id":"vocab-submit","op":"submit","args":{"context":"INIT_REPLY.contexts.local","source":"universe u\nnoncomputable def Reduction (A : Type u) (op : A -> A -> A)\n    (e : A) (xs : List A) : A :=\n  List.rec (motive := fun (_ : List A) => A) e\n    (fun (a : A) (_ : List A) (acc : A) => op a acc) xs\n","root":"Reduction"}}
```

```json
{"client":"local","request_id":"vocab-publish","op":"publish","args":{"artifact":"SUBMIT_REPLY.artifact","snapshot":"INIT_REPLY.snapshots.P1"}}
```

`submit` does not advance the head or P1, so the initial snapshot is still the
right publication snapshot in this fixed sequence. The placeholders above are
specifications for copying actual returned strings, not literal requests.

## Bounds and accounting without another scenario harness

The existing commands provide the needed execution containment. Each ordinary
worker retains its actual public Windows Job receipt: 450 wall/CPU seconds,
6144 MiB and eight processes; nested mathematical stages are 300 wall/CPU
seconds, 4096 MiB, one active child and 128 MiB charged stage storage. Build uses
its existing 300-second/4096-MiB/128-MiB support stage with two compilations.
Do not wrap these CLIs in `run_stage`: its one-active-child Job is unsuitable
for nested product workers. No product limits are changed.

Exact full-success node charges are `init:136 + submit:136 + publish:8 = 280 MiB`.
The node has 3/3 requests, 2/2 stages, no pending request and no renewal. Native
success means bootstrap one child plus submit five children; support's two
compilations are separate. A source refusal may use fewer than five children
while retaining the full already-reserved stage charge. Initial physical supply
must genuinely pass: 280 MiB + twice 32 MiB metadata + 1 GiB margin = 1368 MiB.

Root records per-command elapsed time/stdout/stderr, pins actual request and
response files, and checks each terminal receipt before the next command. Sum
the three **disjoint public Job** CPU totals and the separate build-stage Job
CPU once; do not add their nested native totals again. Record trusted wrapper/
root preparation/copy/audit costs separately when observed. This direct recipe
does **not** invent an enclosing aggregate Job CPU/wall bound: wrapper work is
outside those per-command Jobs. Public Job CPU ceilings sum to 1350 seconds,
plus build's 300-second stage ceiling, not a practical-efficiency result.

Prospective retained endpoint cap: 512 MiB, 8192 regular files, 16384 directory
entries across the new data/evidence roots, excluding shared runtimes. Check
at quiescent command boundaries and after final reports; this is an observed
endpoint allowance, not a transient disk quota. Stop and retain any overrun;
do not enlarge the allocation live. No retries, services, second source attempt,
extra proof or automatic recovery is part of these five commands.

## Evidence and stop interpretation

Require actual support build success and matching source/output/receipt pins;
build stderr is the expected stage-status JSON, not necessarily empty. Configure
must select exactly the chosen fresh domains/grants, zero offers and five common
packages. Init must genuinely accept the checked bootstrap. Before interpreting
any request, bind its adjacent request/command/stdout/stderr/event/supervisor
files, pins, response digest and whole-tree quiescence; a returned handle alone
does not prove a clean execution.

For the vocabulary require `accepted:true`, `source_root:"Reduction"`, the exact
source hash, one ordinary-definition row of universe arity 1, all five bound
submission steps with zero exits, and the actual candidate/inverse packages with
equal root/plans and fresh receiver outputs. Preserve `owner-source.lean`, staged
source/job/plan, all stage logs and canonical objects. Publication must point
to that artifact's checked package and produce the corresponding candidate,
descriptor and publication marker. Record exact receiving name/reference and
canonical manifest/root/descriptor pins for later identical onboarding. Audit
the actual definition body as the seeded List.rec right fold, not just its name.

On elaboration failure, retain diagnostics and classify source-interface refusal,
not mathematical falsity or unsupported List.rec in general. On codec/inventory/
replay failure, retain that exact boundary; on timeout, missing receipt, pending
or uncertain state, stop without another request ID. Do not repair source inside
this allocation. A success qualifies this vocabulary's exact source-to-portable
boundary only. It is not the append-law producer, target theorem, matched
consumer comparison, usefulness evidence or v1 completion.

Source basis: `API.md`, `drafts/OPERATOR-QUICKSTART.md`, `build.py`, `manage.py`,
`py/node.py`, `py/checking.py` (especially `submission_steps`, `submit`,
`publication`), `py/source_codec.py` (`SourceCompiler` seed bindings/resolver),
`native/AgentClient.lean` (`checkSource`, `describe`),
`native/AgentReplayCore.lean` (`referenceName`, `receive`), and
`native/BootstrapSupport.lean` (`decodeDag`, `receiveSeed`).
