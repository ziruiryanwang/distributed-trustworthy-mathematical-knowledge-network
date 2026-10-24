# Ordinary Lean first, optional checked interchange

This directory contains a **source-only facade draft**, not an installed package
or final v5 release. Only `owner.py`, `profile.py` and this note are selected.
There is no build recipe or new runtime result yet. Do not run these standalone
files as if their required package payloads were present. The current installed
packages remain identified by `../ordinary_distribution/CURRENT.md`.

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

1. If a useful result is already in an approved compatible Lean project, import
   and use it normally. Existing Lean search/application can help; suggestions
   are not complete proof evidence. No commons conversion is required merely to
   use an already available lemma.
2. When independent inert admission is useful, share an existing exact bundle,
   or use `produce-baseline` on explicitly approved compiled local targets.
   Receiving `intake-baseline` independently checks that bundle above an explicit
   local parent. Production is not mathematical acceptance.
3. An eligible admitted closure can be locally realized by `export-module` and
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

Use the existing [producer contract](../ordinary_producer_package/README.md) for
production inputs and [approved-project completion contract](../ordinary_project_extraction_package/README.md)
for retained-candidate extraction/completion. Their installed-package examples
do not select this unbuilt draft. Configuration hashes bind selected paths and
modules, not every transitive binary. Approved source/plugins/artifacts remain
local trust premises; resource limits are not a hostile-input security sandbox.

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

The next decision is whether the growth/architecture review warrants a finite
clean-source recipe. Only after that separate selection should packaging or
changed-boundary checks begin. The detailed source map is in
[NATIVE-CONSOLIDATION-SOURCE.md](../../../research/cycles/v5-2026-10-22-native-library/NATIVE-CONSOLIDATION-SOURCE.md).
