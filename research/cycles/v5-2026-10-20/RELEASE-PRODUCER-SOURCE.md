# Release-owned producer: source checkpoint

2026-10-22; author storage_integration_adapter. Canonical root only.
Selection: `RELEASE-PRODUCER-SELECTION.md`.
Decision/derivation: `TYPED-PRODUCER-DEPLOYMENT-SEAM.md`.

## Authored boundary

Three new core files implement a27-source release-owned constructor over the
unchanged lifecycle24/scheduler. `README.md` specifies the final fields and
trust boundary. Root independently owns the new command entry; outcome_audit
owns changed-boundary controls; launch_review owns independent source review.

| Core file | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/release_production/__init__.py` | 169 | `56653258ec5e2b9e8d6abffa55e4f889b979daae05c81282a36cf65453b60717` |
| `software/v5/release_production/producer.py` | 7617 | `4396de095caf214559674e0fdd5188fcc52d10c3e4c8fe32e1d5b63259f397ce` |
| `software/v5/release_production/adoption.py` | 10675 | `62255a98879ed7162eb1a3414c937a29a70258b7396ae070d32fac1253ec5710` |

The independent boundary finding is315 mandatory installation pins versus the
existing256 snapshot limit. The implementation removes live historical build
evidence from this **new** profile by using externally adopted release roles;
it does not enlarge the limits or omit required operative files. Expected new
closure56 is a source-derived design count; hard bound64 is enforced, not an
already-executed count claim.
Here56 denotes the inherited constructor's repeated-rebind pin union, not the
entire Python/OS dependency closure. The test component separately copies and
verifies the complete584-file Python subtree; ordinary calls preserve the
existing selected-runtime and stable-local-installation assumptions.

## Contract now fixed

Outer exact fields are `schema`, `base_profile`, `source_pins`,
`snapshot_host_build`, `release`. The new inner schema retains the inherited
host/image map field names with explicitly new ordinary-artifact-reference
meaning. `release` is `{root,manifest,descriptor}`. The adopted container is
existing `DMKN_V5_DIRECTORY_RELEASE_V3`, checked only for this component's
operative subset. The descriptor has exact mathematical identities, three
relative runtime roles and27 exact source roles; it contains no manifest digest.

Constructor API is `ReleaseLifecycleProducer(profile)`.
`adoption.load(release, source_pins, support_profile)` returns
`root,pins,roles,descriptor,manifest_pin,descriptor_pin`.
The exact role bytes match the current selected stage host, snapshot host and
typed guest image; no new binary or image was built or adopted by this work.

The implementation initializes the required S/L state explicitly, calls only
the unchanged support constructor, and inherits lifecycle/scheduler methods.
It preserves `L._check`, including `_snapshot_build_pins` no-override checks,
and S/N's other ordinary pin-map rebinds. Legacy private build-adoption methods
explicitly refuse. The new constructor aggregates a primary and cleanup failure
instead of discarding either. No stage dispatch occurs during construction.

Independent review found that retaining the nested support base as `_install`
would let direct class callers place output elsewhere inside the release. The
selected correction sets the aggregate owner's `_install` to the whole adopted
release root and binds that field in `_check`; the support object retains its
own nested base. Every actual host/input/output argument is absolute. Inherited
S/N output protection now covers the complete release, and new command evidence
binds its changed working directory. Actual host-cwd portability still needs
the separately selected snapshot integration; no runtime claim is made here.

## Evidence status and remaining work

This is **authored source, pending independent review and selected controls**.
No product import, syntax check, constructor, test, snapshot, request, build,
proof, installation or Git operation was executed by this author. Root's
U64938 remains untouched; profile1242 and all used predecessors remain frozen.
The reviewed old lifecycle entry remains unchanged and must not be passed this
new profile. Root's separate new entry must use this exact contract.

Public installation still needs a selected producer-capability assembly and an
installed-launch evidence adapter; the research runner's canonical-root grammar
is not deployable merely because the artifact constructor can be relocated.
No source pass, small control result or snapshot alone establishes final v5.

On findings, amend only these new unexecuted assigned sources, refresh exact
pins, and obtain review before root selects any execution. Preserve all old
source/evidence and do not automatically renew or rerun any proof allowance.

## Separately delegated component-staging source

Root subsequently selected authorship, not execution, of
`Prepare-ReleaseProducerComponent01.ps1`. It takes four explicit reviewed source
digests (`InitSha`, `ProducerSha`, `AdoptionSha`, `EntrySha`) and plans only the
fixed fresh `experiments/v5-local-checks/release-producer-component-01` tree.
It copies620 exact selected files, including the complete584-file/30,459,330-byte
Python subtree, three support helpers, exact base manifest, retained lifecycle24,
one operator helper, four new sources and three retained runtime artifacts.

It then creates the descriptor and a clearly labeled operative-subset V3
file-map fixture (621 payload rows), plus the new profile and PREPARATION record
outside the immutable `installation` subdirectory. The fixture is not a valid
full directory distribution and expressly reports `full_distribution_validation`
false. The predicted constructor union is checked as56 rows without executing
the constructor. All selected input/copied bytes are rebound; failures preserve
partial output and attempt an overriding `PREPARATION-FAILED.json` marker.

This source does not import Python/product modules, instantiate owners, run
hosts, build, prove or select the subsequent controls. Root owns its independent
review and any actual invocation. No current installation or old evidence is
modified by preparation.
