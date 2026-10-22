# Typed reusable-frontier production

This package joins the selected typed aggregate image to the existing bounded
production lifecycle. It does not implement a new proof system or scheduler.
Its purpose is to make the already retained general36 execution producible, then
allow a later generic execution to depend on the resulting aggregate receipt.

The intended chain is `base receipt -> A*(U) -> A*(V)`. Here U is the polymorphic
`context_transport` method; V genuinely applies U and equality transitivity.
The final arrow requires V's new packet to supply the actual first aggregate
receipt and U's membership opening, without replaying U's witness. This package
does not claim either receipt already exists and does not itself enforce that
one research workload is every caller's mathematical agenda.

## What changes, and what does not

`TypedLifecycleProducer` inherits `aggregate_lifecycle.producer.LifecycleProducer`.
It has a fresh profile schema and explicitly initializes the parent's small
installation state. It never temporarily lies about its image or profile schema.

| Boundary | Implementation |
|---|---|
| Corrected stage executable | `host_adoption.adopt_build(owner, pins, table)` |
| Actual typed image and build/assembly chain | `image_adoption.adopt_image(owner)` |
| One historical successful general arm | `snapshot_adoption.adopt(owner, session, expected, inputs)` |
| Future mixed-claim preparation and snapshot | Existing lifecycle `prepare` and `snapshot` |
| Complete-graph quotes, checkpoints, proof stages and allowance accounting | Existing `aggregate_small` scheduler |
| Final mathematical acceptance | Existing independent receipt/semantic receiver, outside this package |

The failed support optimization screen remains failed. Its actual general arm
completed with 36 segments and one genuine parent. Its enclosing command exited1
because the comparison missed its prospective investment threshold, not because
the general execution failed. Only the exact retained, independently audited
record bytes are accepted through this exception. This is not a generic rule
that nonzero process exits are safe to adopt.

## Stable owner profile

The outer profile contains exactly:

```text
schema = DMKN_TYPED_AGGREGATE_LIFECYCLE_PROFILE_V1
base_profile
source_pins
snapshot_host_build
```

`base_profile` retains the existing `aggregate_small` profile grammar. Its
`support_profile.image_id` is the actual typed image:

```text
9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865
```

Its `host_build` uses the exact selected corrected-stage build records, adopted
by `host_adoption`. That build's old-image provenance is not relabeled as the
current runtime image. Its `image_adoption` has ten file-pin roles:

```text
result, outer, selection, guest_build, guest_selection, guest_source_map,
artifact, guest_attempt, guest_recipes, assembly_command
```

`image_adoption.RECORDS` provides each role's canonical-root-relative path,
byte count and digest. `snapshot_host_build` remains the existing five-role
snapshot-host build dictionary: `result`, `attempt`, `selection`, `source_map`,
`command`. The retained snapshot host is image-parametric; its build provenance
is validated without compiling it again.

`source_pins` must cover exactly `producer.source_paths()`: the existing24
lifecycle modules plus these five modules,29 total:

```text
typed_production
typed_production.producer
typed_production.snapshot_adoption
typed_production.host_adoption
typed_production.image_adoption
```

These same29 source pins must also be present in the underlying support runtime
map. All existing runtime count/byte limits remain in force. The package does
not join or expand the separately installed consumer's runtime closure.

The composite profile identity is SHA-256 of the fresh domain
`DMKN-TYPED-AGGREGATE-LIFECYCLE-PROFILE-V1\0` followed by the existing canonical
profile encoding. Use `profile_document()` for a fresh value of that exact
document. Source/profile mutation or a changed installation path changes the
identity and cannot silently continue an old allowance. Keep the selected source
snapshot fixed across subsequent production prefixes.

## Retained execution evidence

`snapshot_adoption.evidence_pins(run_directory)` constructs the following exact
file pins without I/O. The actual directory is
`experiments/v5-local-checks/restricted-support-matched-execution-01`.

| Role | Relative path |
|---|---|
| result | `pair/RESULT.json` |
| outer | `RESULT.json` |
| selection | `selection.json` |
| configuration | `../restricted-support-matched-execution-01-configuration.json` |
| derivation | `pair/derivation.json` |
| arm | `pair/general/arm-result.json` |
| command | `pair/general/command/command.json` |
| job | `pair/general/host-job.json` |
| diagnostic | `pair/general/diagnostic.json` |
| stdout | `pair/general/command/stdout.txt` |

`snapshot_adoption.RECORDS` stores `(relative_path, bytes, sha256)` for these
roles. Every dictionary value is a file pin, not a string schema tag: the
unchanged scheduler incorporates each file's content identity into the session.

`production_request(evidence, allowance_id=..., budget=..., checkpoints=...,
prior_attempts=..., output_directory=..., stage_limit=...,
carried_external_costs=...)` reads the pinned records and derives the complete
general session. It then runs inherited preflight. This creates no directory,
executes no host, funds no proof and renews no allowance.

The derived session contains the selected typed image, exact wire/header/capsule,
the original genuine base receipt, exact session/capsule bindings, cycle cap2^26,
po18 layout,36 segments and one assumption. Adoption checks:

- Fixed audited record identities and the intended comparison failure.
- Actual outer exit1 with closed/reaped Job, no cleanup error or termination.
- Exact original selected arguments, input pins and all17 retained source files.
- Matching selected snapshot host and typed-image assembly/build lineage.
- Exact successful general arm, native stdout, diagnostic and derivation.
- Exact ordered parent, header, wire, image, complete capsule and segment census.
- Empty selected stderr logs and absence of finalization-failure overrides.

The complete capsule is self-contained for resumed segment production. Individual
historical segment-custody files are not stage inputs and are not re-read; the
actual capsule's full hash and session prefix are still checked. Historical
compiler-runtime trees are not repeatedly hashed as session inputs.

## Later generic snapshots

After separately funded receipt production and independent acceptance, use the
ordinary mixed-claim packet and `prepare`/`snapshot` lifecycle. Its completed
snapshot evidence retains the existing five roles:

```text
result, outer, selection, configuration, command
```

Dispatch is determined by the exact ten-role versus five-role key set before
validation. Each branch requires its own real schema. A failed validation never
falls back to the other branch. Generic snapshots bind the full typed profile
document, actual prepared packet, staged parent order, command and final closure.

## Funding and acceptance remain separate

`preflight` quotes the entire missing graph even if `stage_limit=1`. With no
checkpoints the retained36-segment/one-parent graph contains109 host calls. A
quote reports `full_path_fits_requested_envelopes`; an insufficient full-path
allowance makes that flag false, but does not itself make inherited preflight
or run reject the request. Requiring the flag to be true even for a one-stage
prefix is this campaign's root selection policy, not an inherited scheduler
enforcement rule. Actual dispatch still enforces its existing per-stage and
remaining-allowance reservations. Prior failures and charges remain in the same
lineage. Quotes are conservative bounds, not forecasts of actual running time.

`run` is the unchanged stage orchestration and requires a separately selected
finite owner. No owner is automatically launched by construction, preparation,
request generation, preflight or this document. The source bridge does not
prove a cryptographic receipt valid, establish net growth benefit, qualify
worldwide deployment or complete v5. Actual linked receipts and their independent
semantic use remain the central downstream capability test.
