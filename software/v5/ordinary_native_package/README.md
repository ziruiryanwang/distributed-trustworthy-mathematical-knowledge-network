# Ordinary Lean first, optional checked interchange

This directory contains a **source-only distribution candidate**, not a final v5
release. Its file-assembly recipe has not yet been executed. Do not run standalone
owner/loader files as if their required package payloads were present. Assembly
copies adopted artifacts; it is not a clean-source compiler build, mathematical
acceptance, security sandbox or general-library qualification.

## What this changes

The facade starts from the stable candidate-preview distribution and retains its
ordinary contribution, extraction/completion, module export, query and peer APIs.
It adds the already implemented owner-free producer and baseline intake paths.
It does not expose the parked `register-reference`, `export-reference-delta` or
`contribute-reference` commands, and does not load their matcher, registration,
snapshot-recovery, authoring or separate native-helper profile.

The logical `reference/` directory contains only unchanged `baseline_bundle.py`
and `baseline_intake.py`. Its historical name does not grant reference authority.
Keeping these paths avoids modifying the tested producer's exact role checks.

## Choose the smallest useful route

1. Work in an approved compatible ordinary Lean project, using its native
   notation, classes, tactics and libraries. Existing Lean search/application can
   help; suggestions and draft proofs are not independent acceptance evidence.
2. Select completed outputs (including a useful adaptation or bridge), then share
   an existing exact bundle or run `produce-baseline` on those compiled targets.
   `intake-baseline` independently checks the inert bundle above a receiver's
   explicit local parent. Keep ordinary package sharing available. There is no
   obligatory generated-module round trip or original-reference registration.
3. If independent assurance of an input is useful, intake it before relying on it.
   An eligible admitted closure can optionally be locally realized by `export-module` and
   imported into ordinary Lean. A new project proof can return through
   `contribute`; missing interpretations may be recovered with `extract-project`
   and then independently admitted by `complete` above the same retained parent.

All research choices remain local. None of these commands selects mathematical
tasks, promises usefulness, automatically publishes to indexes or creates a
global ledger. Existing peer interfaces can separately offer and receive exact
data. Ordinary approved package/repository sharing remains a valid default.

## Public surface and safety boundary

The selected command names are `init`, `status`, `contribute`, `complete`,
`extract-std`, `extract-project`, `export-module`, `intake-baseline` and
`produce-baseline`. Existing operation-specific pins and resource limits remain.
The source copies the tested producer argument gate and operation body exactly.
Production requires explicit local-project approval and a finite spool allowance;
it rejects owner-state and unrelated operation options before support loading.
All other commands still require their owner-state arguments and reject producer
options. Removed reference commands/options are not parser alternatives.

The included [producer contract](PRODUCER.md) specifies production inputs; its
source-stage wording is historical, not a new execution result. Production uses
the shared profile/runtime/resource options plus `--project-production`, its
`--project-production-sha256`, `--approve-local-project`, `--output-names`, fresh
`--output` and explicit `--spool-mib`. Receiving `intake-baseline` uses the shared
options plus the receiver's `--catalog`, `--custody`, `--store-id`,
`--custody-limits`, `--parent-root`, `--bundle-directory`, `--bundle-manifest` and
`--bundle-manifest-sha256`. Receiver state must already be initialized under its
own approved policy. Producer report target rows are locators, not warrants;
the actual accepted bindings/evidence determine what was checked.

Configuration hashes bind selected paths and
modules, not every transitive binary. Approved source/plugins/artifacts remain
local trust premises; resource limits are not a hostile-input security sandbox.
Checking final mathematics cannot undo harmful project execution or wasted draft
work. Intake neither endorses the original compiled artifacts nor registers their
frontend metadata. Existing checked-module/retained-candidate routes remain
optional, narrower capabilities, not prerequisites of ordinary package work.

## Limits that this consolidation does not solve

Baseline bundles can contain multiple admission batches. Generated-module export
and return completion are narrower: normally at most 32 new units and 4 MiB,
with further expression/name/edge limits. Local anchors cut exact previously
registered whole units, subject to finite chain bounds. They do not remove
installed-name conflicts, oversized indivisible groups or public-view conversion
requirements. Successful production/intake does not imply materialization fit.

Generated modules preserve supported checked kernel declarations, not the
original notation, tactics, simp/typeclass registrations or source layout.
Independent admission may therefore be useful without replacing ordinary
approved-package reuse. No new growth or global-scale claim follows from this
source cleanup.

## Compatibility and next gate

No core installation, native source, toolchain, peer protocol or state format is
changed. However, module-anchor support identity includes exact owner/loader
bytes: this facade necessarily creates a new support version. Old packages,
anchors and accepted state stay untouched; no migration or silent reinterpretation
is provided. Compatible core state and protected anchor reuse are different
questions. Use an old anchor only with its explicitly supported old package.

## File-assembly recipe

Run `assemble.py` only from the approved source tree with the selected Python
`-I -S -B`. Supply explicit `--source-root`, `--base-package`, `--exporter`,
`--python-runtime`, `--lean-runtime`, fresh `--output`, reviewed
`--source-map-sha256`, and finite `--wall-seconds`/`--cpu-seconds`.
The recipe accepts relocated inputs with the exact supported pins; it does not
search for a convenient historical installation or download dependencies.

The base is the adopted stable preview PROFILE
`ab04e72440bcd09381a81d4b721d1103fa2e62bc260fa6c0434e6c568419016f`.
The exporter is the retained 809,472-byte BaselineExporter executable
`2adcffad1ad4967f093e1acc6c31295c2519e7f9cbf35d04bee37d8580cc3c4f`.
Its source-build history is separate; file assembly does not reproduce it.

The complete package contains 132 unchanged base payloads, two facade
replacements, five baseline additions, and two documents: 141 payloads, plus
ASSEMBLY.json and the commit-last PROFILE.json. Exactly 111 helper roles are
profiled. No original-reference helper or new native checker is added.
Failures retain partial output and do not automatically retry. A new destination
requires a new explicit selection, not a resume flag. The caller supplies hard
outer process containment if required; controller bounds are cooperative.

Root must separately select and review any assembly or changed-boundary test.
The current source-only result does not supply an installed package or repeat any
previous producer, intake or theorem experiment.
