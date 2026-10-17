# Location portability: three-payload successor, not a new transport

2026-10-16. Independent source-only review for the fixture-free workspace/client
increment. No product source, used evidence, Git index, runtime, test, or proof
campaign was changed. Root owns the next implementation selection.

## Conclusion

The existing role-aware location service can be made independent of the research
directory with **three changed product payloads** in one fresh selected package:

1. `location/controller.py`;
2. `location/controller_services.py`;
3. `location/node_entry_services.mjs`, derived from the currently selected
   `node_entry_services_available.mjs` successor.

This is path portability for the existing Windows/Node/runtime profile, not
cross-platform support or completion of v5. Retain the exact runtime manifest,
source pins, peer protocol, private-pipe lifecycle, workflow tickets and finite
budgets. Do not change the frozen predecessors in place.

There is no `location/service.py`. The actual wrapper is
`controller_services.py`; its superclass and child entry contain separate path
assumptions. A facade or portable subclass alone cannot fix these assumptions.

## What is hard-coded, and what is already parameterized

| Boundary | Current source fact | Required consequence |
|---|---|---|
| Runtime adoption | `controller.py` fixes `ROOT`, v4 `BASE`, Node executable, source under `experiments/v5-local-checks`, and exact source path suffix | Explicit trusted-owner installation/source/workspace roots; preserve runtime identity |
| Runtime validation | Fixed manifest SHA, exact 5,896-file selected runtime census, all selected size/hash pins, 192 MiB total bound, bounded source pins | Move the root, not the trust check; the first successor still accepts only these exact runtime bytes |
| Evidence and child cwd | Base controller requires fresh evidence under the research experiments tree; service wrapper spawns at `B.ROOT` | Evidence under selected workspace; cwd exactly the selected workspace |
| Node bootstrap | Available-entry successor independently asserts research cwd, installed `node.exe` path, fixed manifest, source names and import allowlist | Matching path-bearing local launch map and independent validation in the child |
| Runtime loading | `runtime.mjs` takes a canonical absolute root; `services_composition.mjs` derives Ping from that root | No rewrite needed; pass selected installation's `overlay` |
| Channel consumers | `available_descriptor.py`, `observed_route.py`, `delta/transport.py`, and `transport/located_receipts.py` import exact service classes | All selected consumers must load the same successor package identity |
| State lifecycle | Node entry calls `locator.start({create: true})` | Initial portable increment has fresh per-operation location state; persistent location restart is not already implemented by relocating paths |

The latest selected source aliases must be retained: readiness source
`maintained_roles_ready.mjs` appears at runtime as `maintained_roles.mjs`, and the
available-descriptor entry appears as `node_entry_services.mjs`. Selecting the
older filenames' original bytes would regress adopted behavior.

## Owner adoption contract

Introduce required keyword parameters on the fresh `AdoptedLocationRuntime`
constructor, conceptually:

```text
AdoptedLocationRuntime(source_directory, source_pins,
                       installation_root=..., workspace_root=...)
```

This remains a **trusted local-owner API**, not a network descriptor schema.
The source digest map is adopted by the owner, not accepted from a provider.
The installation root locates one fixed release profile; there is no arbitrary
executable, command line, environment overlay, module resolver, or manifest
selection API. Retain the existing manifest digest constant:

```text
a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed
```

Required invariants:

- All roots are absolute, canonical ordinary directories, with no junction or
  symlink in their ancestry. Do not use textual prefix checks for containment.
- Workspace is disjoint from immutable installation and source trees: neither
  may contain the workspace, and workspace may not contain either. Source may
  be inside the installation if the selected packaging layout requires it.
- Node is derived as `installation_root/runtime/node/node.exe`; overlay and
  manifest locations are derived too. No independent executable parameter.
- Evidence is a fresh proper descendant of workspace, with an existing checked
  ordinary parent. Source and runtime roots are not output destinations.
- The owner-selected `configuration.state` is a fresh proper workspace descendant
  with an existing checked parent, disjoint from this operation's evidence path.
  This covers the current create-only location lifecycle; do not silently add
  resume or migration semantics.
- Copy and retain the owner selection without mutable aliases to caller maps.
  Read-only fields are preferable. Changing any selection requires a new adopted
  operation, not assignment to a live controller's roots.

Canonical-path checks and pre/post hashing retain the existing trusted-local-host
assumption. They do **not** eliminate filesystem time-of-check/time-of-use races
against a malicious local administrator. Ordinary remote peers cannot select or
mutate these local roots. Exact Python class checks are API-origin constraints,
not a sandbox against arbitrary hostile code in the owner interpreter.

## Concrete three-file responsibilities

### Fresh controller payload

Replace only the selected runtime/source/evidence root policy with the explicit
adoption above. Make `verify()` address `self.installation` everywhere it currently
addresses `BASE`. Preserve fixed manifest identity, exact census, size/hash and
tree bounds, nine base-source names, pre/post verification, and all IPC/lifecycle
code.

Provide a small shared launch-map constructor for the role-aware entry, with a
new local map version and exact fields:

```text
schema: DMKN_V5_LOCAL_NODE_SOURCE_MAP_V2
root: exact source directory
installation_root: exact adopted installation
workspace_root: exact adopted workspace
files: exact nine base plus five role source digests
manifest_sha256: unchanged supported manifest digest
```

The map is written exclusively to fresh evidence, hash-bound through the existing
fixed argv. It is not remote protocol state, a mathematical warrant, or a public
claim of runtime authority. Bound its serialized length before writing/spawning;
long owner paths must fail within the existing 16,384-byte bootstrap bound.

The three-file product surface must explicitly expose only the role-aware service
entry. The old bare `LocationProcess._start_core` and old role-only launcher target
different legacy entries. Do not accidentally advertise them as portable. The
clean narrow option is a clear refusal for direct bare-base launch in this fresh
product successor while retaining its shared lifecycle methods for the selected
service subclass. Supporting all historical launch variants would require more
entry successors and is unnecessary for the selected client.

### Fresh service-controller payload

Preserve `ServiceLocationProcess` and `ServiceLocatedWorkflow` names and exact
class-origin checks. Validate owner state/evidence scope, merge exactly the
existing nine-plus-five source pins, use the shared V2 map, and spawn with
`cwd=adoption.workspace`. Keep the fixed entry filename and sanitized environment.
Keep the existing role-aware READY check, deadlines, private pipes, cancellation,
teardown and posthash paths unchanged.

### Fresh Node service entry payload

Start from the available-descriptor entry, not the earlier service entry. Before
dynamic runtime import or networking:

1. Check unchanged fixed argv shape, no injected Node execution arguments,
   bounded config/map files and their exact argv hashes.
2. Require the V2 map's exact field set, canonical owner roots and fixed manifest
   identity. Require `mapping.root == dirname(import.meta.url)`.
3. Require `process.cwd() == workspace_root` and
   `process.execPath == installation_root/runtime/node/node.exe`.
4. Recheck evidence/config/map paths and fresh state scope under workspace.
5. Retain exact fourteen source names/hashes; construct the allowed import set
   solely from them and the fixed manifest's overlay entries under installation.
6. Retain the import hook (including no URL query/fragment), then load the same
   services composition using `installation_root/overlay`.

Keep the existing narrowly typed unavailable-dial response, same operation
deadline, frame/byte counts, command set and service teardown. No remote endpoint
can supply a local root or an executable path.

## Class identity and integration constraint

Use one fresh selected package snapshot in the isolated product process. Keep
unchanged consumer payloads importing `location.controller_services` from that
same package. In particular, `DeltaLocatedHandoff` requires exact
`ServiceLocationProcess`; `ServiceLocatedWorkflow`, `available_descriptor` and
`observed_route` repeat exact-origin checks. A subclass or second import of the
same text under a different package name will fail, correctly.

Do not monkeypatch `ROOT`, `BASE`, `sys.modules`, or imported class globals. Do not
replace exact-origin checks with `hasattr`, arbitrary callbacks or serialized
"authenticated peer" claims. If root chooses distinct package/module names
instead of a selected successor snapshot, consumer import changes enlarge the
patch surface and must be enumerated separately.

The I-only mixed custody profile change is a **separate coupled selection** owned
by the client-contract agent. It cannot be accomplished by giving a fake aggregate
image to the old constructor. This location seam does not alter packet or theorem
acceptance and does not manufacture the absent A certificate.

## Containment is still a launcher obligation

The current controller explicitly requires hard parent Job containment. Its
`included_in_parent_job: True` report is not a containment probe. Moving the
paths must not turn that inherited caller contract into claimed enforcement.

The public operation launcher must create/own the actual bounded Job before
adoption verification and launch; child inheritance, no breakaway, CPU/memory/
process/wall limits, output caps, and terminal descendant closure remain part
of the selected launcher contract. The existing private pipe does not replace
that Job. A user-facing entry which bypasses it is not supported by this seam.
Report verified Job evidence at the launcher layer, or label the controller's
containment status as required-but-not-independently-checked. Do not accept a
JSON boolean as containment evidence.

This design is therefore three location payloads **plus reuse of an actual
supported bounded launcher**; it is not a claim that three files deliver a
complete portable application. Source pin verification itself must stay charged
to the same finite operation, including its synchronous posthash.

## Minimal future changed-boundary controls

Only after root selects reviewed implementation and a finite test allocation:

- One fresh owner installation/source/workspace layout outside the experimental
  subtree starts the same role-aware channel; actual runtime bytes stay pinned.
- Refuse altered manifest, source or Node bytes; extra/missing runtime file;
  noncanonical/link paths; workspace overlap; escaped evidence/state; V1 map;
  wrong cwd/execPath; unknown map field; oversized bootstrap map; and wrong
  exact-class consumer composition. Use small pure controls where possible.
- One actual source-map/READY/channel closure exercises the changed launch
  boundary under the existing bounded Job. Couple it to the selected integrated
  client workflow rather than rerunning the historical location campaign.
- Preserve existing typed unavailability and readiness sources by exact input
  pin comparison; do not launch a new large campaign to reconfirm unchanged code.

No proof generation, higher cycle cap, broad network simulation, or certification
retry is needed to establish this path-portability seam. Independent-host reach,
other operating systems, persistent service reopening, secure updates, licensing,
and full v5 release acceptance remain separate obligations.

## Follow-up: exact package closure and handoff coupling

Root requested an explicit import strategy before selecting any source copy.
Recommendation: **a canonical-name `location` package overlay in a fresh isolated
owner process**, sharing the unchanged retained v5 packages. Do not introduce a
`portable_location` Python namespace. It is not necessary to duplicate the entire
v5 source tree merely to keep these class identities coherent.

The location-specific selected closure is exactly these 21 payloads:

```text
location/__init__.py
location/controller.py                         CHANGED
location/controller_services.py                CHANGED
location/protocol.py
location/workflow.py
location/available_descriptor.py
location/observed_route.py
location/protocol.mjs
location/framing.mjs
location/intent.mjs
location/runtime.mjs
location/maintained.mjs
location/transport.mjs
location/composition.mjs
location/ipc_wire.mjs
location/node_entry.mjs
location/maintained_roles.mjs                   exact readiness-successor alias
location/role_composition.mjs
location/node_entry_roles.mjs
location/services_composition.mjs
location/node_entry_services.mjs               CHANGED available-entry successor
```

Eighteen payloads are byte-preserved from their selected sources, with the
readiness alias mapping explicitly recorded; three are fresh successors. The
legacy Node entry payloads remain in the fixed adopted source-name set, not as
supported product launch commands. Tests, integration harnesses, the old
`controller_roles.py`, and campaign modules are not part of this location
product closure. This count is **not the full transitive Python dependency
count**: retained `discovery`, `transport`, `custody`, mathematical modules and
the selected frontier-network package still require their normal source pins.

The trusted launcher starts a fresh isolated interpreter and selects import roots
before importing any v5 package: selected overlay root first, one exact retained
v5 source root second. A normal `location/__init__.py` makes the selected location
package a single regular package; its submodules do not fall back piecemeal to the
old location directory. No untrusted cwd, `PYTHONPATH`, user site, caller search
path, or remote endpoint may select that precedence. Refuse an already loaded
`location` or `location.*`; do not delete/rebind loaded module entries to force a
transition. Record and check the selected modules' actual `__file__` origins.

The resulting identity chain is:

```text
location.protocol.OwnerEgressPolicy       one selected class
location.workflow.WorkflowBudget          one selected class
location.workflow._LocatedSearchClient    one selected class
location.controller_services.*            one selected service pair
                    |
                    +-- unchanged delta.transport.DeltaLocatedHandoff
                    +-- inherited DeltaAcquisition.from_search
                    +-- unchanged transport.located_receipts._ExpiringContact
                    +-- unchanged observed_route / available_descriptor
```

`DeltaLocatedHandoff` then checks the fresh portable service's **exact existing
canonical-name class**, constructs the same selected `ServiceLocatedWorkflow`,
and receives `_LocatedSearchClient` from that workflow. Its `begin_search` and
`DeltaAcquisition.from_search` see the same class objects, not merely equivalent
text. `OwnerEgressPolicy` remains shared with the workflow, handoff and endpoint
guards; `Endpoint` remains the retained `transport.http_provider.Endpoint`.

The new frontier transport can retain
`FrontierLocatedHandoff = delta.transport.DeltaLocatedHandoff` and inherit
`from_search`, provided its existing type/profile-specific constructor is the
selected frontier successor. No new handoff class, class-gate relaxation,
`_ExpiringContact` override, or search-budget copy is required for this strategy.

Alternative `portable_location` namespace: possible only with new explicit
handoff/from-search gates and careful imports of shared original policy/workflow
types, plus adapted observed/unavailable helpers. That enlarges the semantic
review surface without fixing a new requirement. Do not choose it merely to
avoid selecting a coherent package overlay. If the owner insists on concurrent
old/new location instances in one interpreter, that is a different requirement
and this minimal closure no longer suffices.

This recommendation does not itself authorize copying or execution. The root
must select the fresh overlay location, its exact retained-file map, the three
edit owners, launcher import-root contract and coupled frontier successor before
implementation. Existing used paths remain frozen.

### Root-selected copy preparation

Root selected `software/v5/portable_runtime/location` as the fresh overlay and
requested exact baseline mapping before copying. The machine-readable
[LOCATION-PORTABILITY-BASELINE.json](LOCATION-PORTABILITY-BASELINE.json) records
all 21 canonical source paths, destination names, byte counts and SHA-256 pins,
with only the three named successors marked editable after root copy confirmation.

Latest adopted actual anchor is `delta-network-continuation-01`, not a new test:

- Selection: `5699ded6dba1a6dc10e674b033248a3532dec2f4ba4650692b685f375097c5a3`.
- Configuration: `0cfa1763f6177adb0cd1ad196fddbae81b04229837227ced528e7d95697019b2`.
- Outer result: `70898a9f36f2540697d2008ee2ce3862e02f5e535c91d251b95e2e6d5aeca995`.

Six Python modules match that actual source snapshot; fourteen JS modules match
the same operation's adopted `delta-network-node-02` snapshot, including both
explicit aliases. The remaining 64-byte canonical `location/__init__.py` is a
docstring-only source selection, **not present in the actual namespace-package
snapshot and not claimed as previously executed evidence**. Its presence in the
new overlay intentionally makes package resolution closed, so retained old
`location` cannot fill missing submodules. That loader/package behavior is a new
boundary to check under the eventual selected source closure.

No source copy, product edit or test had been performed by this reviewer at this
mapping checkpoint. Root's copy confirmation is required before the three-file
implementation assignment begins.

### Three-payload source implementation

Root subsequently confirmed exact pre/post verification of the 21-file baseline
copy and authorized only the three named payload edits. They are implemented;
independent actual-source review is assigned to `v5_growth_decision`. No runtime,
import, compilation, tests, proof generation, or Git mutation was performed by
this author.

Public runtime adoption now has the exact signature:

```python
AdoptedLocationRuntime(source_directory, source_pins, *,
                       installation_root, workspace_root)
```

The role-aware service signatures are unchanged. Adoption is a frozen dataclass
with immutable copied source pins, derived fixed Node path, ordinary roots and
workspace/source/runtime disjointness. The service additionally validates fresh
state/evidence scope before launch, bounds the V2 map, and uses selected workspace
cwd. Old bare-base launch explicitly refuses; no `ROOT` or `BASE` variable remains
in the three successor payloads. Runtime posthash uses the original adopted
object and refuses an adoption substitution.

The child validates V2 exact fields, canonical roots, owner cwd/executable,
evidence/config/map relationship, fresh state scope, fixed manifest and original
import allowlist before loading runtime modules or starting networking. Existing
channel sequencing, finite transport limits and typed dial-unavailability remain.
The old declarative `included_in_parent_job` boolean is replaced with
`parent_job_containment: REQUIRED_CALLER_CONTRACT_NOT_CHECKED_HERE`; actual
containment belongs to the selected launcher.

Read-only post-edit comparison confirms exactly the three allowed files changed
and all 18 other selected payloads retain their baseline hashes. Initial review
targets (not yet test-qualified):

| Payload | Bytes | SHA-256 |
|---|---:|---|
| `controller.py` | 15,864 | `2d8eb0f8525684024e665c00de3bebd5ae23523e3e8e9347313522c46a678387` |
| `controller_services.py` | 5,502 | `8591c49dba300a84d1e4b60f3ee1550be5eefd06b22867cf84d5b1080497e595` |
| `node_entry_services.mjs` | 9,785 | `2eae8676469da5ef34fb88539d67774fc3dd115a6662cf24d169046e224fc346` |

The coupled frontier-network implementation and complete isolated-loader source
closure remain root/other-agent work. This source increment does not claim v5
release, an A certificate, persistent locator reopening, or public deployment.

Independent source review subsequently requested exact-string canonical-path
comparison in Python: Windows `Path` equality alone is case-insensitive, whereas
Node's `realpathSync` comparison is exact. The correction is adopted in
`ordinary` and `fresh_workspace_path`; no path policy is loosened. Corrected
controller is 15,884 bytes, SHA-256
`4dc0824d758e72fce591dbd9dddb9e487bcd0506cfaf4a71e894b0166b84e064`.
Other two edited payloads retain the hashes above. Independent actual-source
clearance is recorded in `PRODUCT-SOURCE-REVIEW.md`; this remains unexecuted.
