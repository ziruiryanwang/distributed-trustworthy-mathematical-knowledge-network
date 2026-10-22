# Release-owned producer: independent design review

2026-10-22, storage_launch_review. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Disposition and exact scope

**The compact adoption boundary is sound in principle under explicit local
software-adoption assumptions. Source implementation and execution are not yet
accepted by this review.** The selected change removes a concrete impossible
input requirement: the old constructor requires315 distinct nonempty pins,
whereas the generic snapshot selection allows256 and additionally requires
operation documents. Raising a parser limit would not repair the requirement
to keep this workstation's build history online.

I reviewed the root's `RELEASE-PRODUCER-SELECTION.md`, the complete adapter
`TYPED-PRODUCER-DEPLOYMENT-SEAM.md`, the minimal control contract, and the relevant
unchanged production, aggregate-small, lifecycle, generic-snapshot and current
body-location distribution contracts. The earlier independent315-pin boundary
and prior actual lifecycle-control outcome remain retained; neither was rerun.
Only text/source inspection occurred. No Python import, syntax check, test,
database, native process, proof, source installation or Git mutation occurred.
The live heavy operation was not inspected or interrupted.

Root's final schema decision supersedes the seam's earlier provisional
`snapshot_artifacts` spelling. The author has been asked to reconcile the note
and implementation before their final source checkpoint. This review specifies
the final agreed boundary, not both alternatives.

## The small selected boundary

The implementation consists of new `release_production` init, adoption and
producer modules, with a separately root-owned operator entry. The class is
`ReleaseLifecycleProducer(aggregate_lifecycle.producer.LifecycleProducer)`.
It does not invoke the old lifecycle, aggregate-small or typed constructor;
it explicitly establishes their required state and reuses their operations.

The two profile schema tags and profile hash domain must be new. The exact
outer fields are:

```text
schema, base_profile, source_pins, snapshot_host_build, release
release = {root, manifest, descriptor}
```

The inner fields are:

```text
schema, support_profile, source_pins, relation_image,
stage_memory_ceiling_mib, host_build, image_adoption
```

`manifest` and `descriptor` are ordinary absolute pins. The descriptor has a
new fixed schema and exactly the adopted foundation, policy, individual
relation image, aggregate image, three relative artifact roles, and27 logical
core-source bindings. The release's operative files must all resolve below
the selected ordinary release root. Per-operation inputs are separate.

Three compatibility fields are **ordinary pin maps under the new schema**:

| Field | Exact pin roles |
|---|---|
| `base_profile.host_build` | `release`, `descriptor`, `stage_host` |
| `base_profile.image_adoption` | `release`, `descriptor`, `guest_image` |
| `snapshot_host_build` | `release`, `descriptor`, `snapshot_host` |

All copies of the release/descriptor pins must equal the selected outer pins;
host/image pins must equal the descriptor's materialized roles. The support
host must equal `stage_host`, `_image` must equal `guest_image`, and
`_snapshot_host` must equal `snapshot_host`. These are not success reports,
build attestations or substitute historical records. No `result`, `attempt`
or fabricated command may be added merely to appease an old adoption parser.

The selected containing manifest is the existing V3 directory file-map
container. This constructor validates only its **operative producer component**,
not every role and semantic condition of a full current distribution. Do not
call the full distribution validator and silently acquire its entire import,
wrapper, Lean-support or reader preparation closure. Conversely, a successful
component construction must never be labeled complete V3 distribution validation.
The manifest remains a bounded JSON input; unrelated entries are not mandatory
local payload reads. Required entries cannot be omitted from its selected map.

## Trust argument: identity is not mathematics

Let the local owner choose expected manifest digest `m`, exact descriptor pin
`d`, ordinary root `r`, and profile `p`. Let `R` be the finite operative closure
derived from those selections. The constructor can establish:

```text
hash(manifest bytes) = m
descriptor bytes match d and the manifest's descriptor row
the descriptor/profile roles and mathematical identity tuple agree
every required file and imported source in R has the selected path and bytes
the immutable new profile identity binds this installation and its roles
```

This establishes an adopted software configuration, **not** that its checker is
correct, its host was compiled from particular source, or a theorem is valid.
The source/artifact correspondence and actual aggregate execution-image identity
remain the maintainer's separately reviewed release-assembly obligations.
The operator's trust decision is external to the manifest and descriptor.
An unknown peer's self-consistent file map supplies no authority to choose
executables, image IDs, foundation, policy or trusted source code.

Mathematical acceptance remains the unchanged receipt relation with the actual
adopted image, foundation, policy and exact statement/capsule bindings. A guest
file SHA-256 is not its execution-image ID. A release descriptor is neither a
SNARK nor proof of the claimed host/image correspondence. A forged operation
report is still not a cryptographic receipt. Removing online build logs therefore
does not remove a mathematical premise; it changes where software assurance is
audited and requires the local owner to adopt that software explicitly.

The filesystem, interpreter, kernel and immutable local installation assumptions
remain. Hash checks do not defeat arbitrary concurrent hostile OS writes or a
compromised interpreter. The proposed file set is not a proof of hermetic native
loader closure. This design does not add signing, key distribution or global
revocation; those remain separate release obligations rather than hidden promises.

## Hash dependencies must be acyclic

Root selected one direction, not two interchangeable representations:

```text
payload code / hosts / guest -> descriptor -> containing manifest
containing manifest + descriptor + local paths -> operational profile
operational profile + packet -> configuration / selection
```

Here an arrow means the later object may contain the earlier object's digest.
The manifest pins the descriptor; **the descriptor never pins that manifest**.
The manifest must not contain its own file/hash. Code included in the descriptor
must not hardcode the digest of that same descriptor or containing manifest.
An absolute materialized profile that pins the manifest must not itself be a
payload hashed by that manifest. Materialize it separately or use a relative
template that has no reverse commitment. Configuration/selection must likewise
not become their own selected payload. A later receipt or result may bind prior
objects; it cannot repair a circular release specification.

Portable release identity is therefore distinct from path-bound operational
identity. The expected manifest digest enters through trusted owner input,
not a self-described digest field read from peer data.

## Required constructor and inherited invariants

All of the following must be evident in the actual source before launch:

1. Bound/parse/copy the new outer and inner profile, reject unknown fields and
   old/new schema mixing, establish new domain-separated lifecycle identity,
   and start `_lifecycle_ready = False`.
2. Establish all inherited state: `profile`, `_raw`, `profile_id`, `_closed`,
   `_busy`, `_attempt_open`, `_history`, `_last_call_failure`, lifecycle
   profile/raw/ID, then construct the unchanged support `production.Producer`
   from its ordinary exact support profile. No parent old-schema constructor
   or typed historical adoption is called.
3. Adopt `_A`, `_Job`, `_install`, the support pin map and exact aggregate/core
   source sets. Check the chosen stage memory ceiling against the actual
   adopted supervisor ceiling, not just a hardcoded nominal maximum.
4. Establish exact release/descriptor/role state, `_image`, `_snapshot_host`
   and `_snapshot_build_pins`; enforce finite file/count/byte bounds before
   readiness. Finish with `profile_id = _lifecycle_id`, readiness true and
   a full rebinding check.
5. On failure after a support owner was returned, close that owner. Preserve
   refusal and cleanup failure rather than reporting a usable instance. The
   caller must not claim to have cleaned an arbitrary support object whose
   own constructor never returned. No worker is started by the constructor.

Keep `LifecycleProducer._check` through the normal superclass chain. It checks
both aggregate and support profiles and, once ready, all three lifecycle
equalities:

```text
encoded(_lifecycle_profile) = _lifecycle_raw
profile_id = _lifecycle_id
encoded(profile) = encoded(_lifecycle_profile["base_profile"])
```

It also verifies the existing24 imported module origins and snapshot-role
finalization markers. The new checker must additionally verify its three core
module origins and the selected release/descriptor bindings. Effective cached
role members and pin maps must remain equal to their committed profile/descriptor
values; checking only the serialized public profile while dispatch uses a
separately mutable `_image` or `_snapshot_host` is insufficient.

Source paths must be exact ordinary paths, with no traversal, drive/ADS escape,
reparse target, case/directory alias or duplicate logical-source ambiguity.
All required support/runtime files must be members of the same adopted operative
manifest subset. Imported source names must resolve to the selected package tree;
preloaded conflicting product modules cannot be blessed after execution.
The command entry therefore validates the finite bootstrap source map before
product import. Direct in-process use assumes the owner already imported trusted
code; constructor checks cannot retroactively sandbox its import-time execution.

The new class must refuse legacy `_adopt_build`, `_adopt_host_build` and
`_adopt_image` paths, rather than retain an accidental fallback into historical
records. Its `_snapshot` remains the lifecycle's generic `snapshot.adopt`, never
the older aggregate-small retained snapshot grammar.

## No-override, funding and identity separation

The unchanged `_no_override` accepts ordinary pin-valued maps; it does not need
historical result-field names. Thus the new three-role maps satisfy the actual
consumer contract without manufacturing old evidence. Preserve checks over:

- release stage-host and guest-image maps;
- `_snapshot_build_pins`;
- actual session snapshot evidence;
- every retained prior-attempt record.

The release does not override a failed snapshot, failed stage, output sentinel,
unknown closure or finalization failure. If any later action fails while an
attempt is open, inherited fail-stop and resource-charge rules remain in force.

The existing `_request` requires every retained predecessor to match the exact
current profile ID, session ID, allowance, budget, prior prefix and carried
costs. A new release profile or relocation cannot relabel U's allowance, adopt
its checkpoint lineage as a newly funded session, or erase charges. Mathematical
reuse of a genuine accepted U result is a different operation from continuing
U's scheduler. A new V session needs its own explicit owner funding.

Four entry actions remain separate: snapshot, request, preflight, run. Request
construction calls the existing preflight once, not twice. Neither construction,
profile observation nor preflight starts proof stages. Snapshot is one separately
selected finite layout operation; it is not proof production. Only explicit run
invokes the unchanged finite scheduler. No automatic transition, retry, funding
increase or deferred daemon is selected.

## Closure and scalability argument

The proposed exact-layout arithmetic is plausible and must be independently
counted against the eventually selected files:

| Set | Expected size |
|---|---:|
| Existing lifecycle core plus new init/adoption/producer | 24 + 3 = 27 |
| Core, existing aggregate-small operator helper, new entry, Python auxiliary rows | 27 + 2 + 16 = 45 |
| Support union after manifest, three helpers, stage host, interpreter/DLL | 52 |
| Add containing manifest, descriptor, guest and snapshot host | 56 |

These are distinct-path counts with exact conflicting-pin refusal, not the sum
of every repeated role. The new constructor should enforce at most64 operative
installation pins and at most512MiB. The generic snapshot's configuration,
profile document and packet then need at most67 unique slots, before any other
explicitly selected rows. This fits256 without weakening any of its three
existing parsers. The final selector must count its **actual** union, including
entry/helper/output-operation bindings;56 is not a completed runtime inventory.

Historical build maps/logs are not recursively opened to populate `R`. Parent
receipts, demanded semantics and operation data retain their own unchanged
validation and envelopes; they are not silently dropped or declared constant
cost. Ordinary construction now depends on bounded release payloads rather
than unbounded release-production history. Rebinding those files still costs
their actual bytes and is not a measured startup or whole-workflow speedup.

The current130-source consumer distribution plus lifecycle's seven absent
logical files and the new four-file package reaches its141 logical-source cap.
This arithmetic does not prove source-version compatibility. Any same-named
consumer/producer difference requires an explicit reviewed common version or
isolated namespace; last-writer-wins replacement is not acceptable. This is a
later assembly check, not grounds to rerun unchanged proof algorithms now.

## Minimal subsequent checks and remaining integration gate

The four negative control groups and one real fresh relocated constructor,
profile observation and close are an appropriately small decision-changing
verification plan. They should exercise the actual new role/manifest/origin
functions, explicitly disclose doubles, and forbid host, proof and network
dispatch. No repeated scheduler, crypto, U receipt or completed lifecycle suite
is needed. A Python read monitor can detect unintended historical reads in that
test; it is not an OS sandbox or proof of all native I/O behavior.

The source-only design does **not** solve the installed-launch evidence mismatch:
the existing generic snapshot recognizes `DMKN_V5_LOCAL_CHECK_RESULT_V1`, while
the installed public launcher emits `DMKN_V5_CLIENT_LAUNCH_RESULT_V1`. That needs
one separately reviewed explicit adapter or schema branch. Do not fake an old
research result, package the canonical-root research wrapper as a portable
launcher, or silently fall back between failed evidence schemas. Reuse the
generic snapshot mathematics and adapt only the real supervisory evidence.

Source acceptance still requires the concrete three core files, entry review,
exact source/pin closure, constructor cleanup and all role-immutability guards.
Later assembly, independent artifact adoption, exact finite controls, public
installed evidence, genuine new snapshot/renewal and full release obligations
remain explicit. This principled constructor repair is central progress toward
deployability, not a final-v5 or mathematical-growth completion claim.
