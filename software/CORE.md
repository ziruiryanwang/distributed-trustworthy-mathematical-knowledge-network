# Relocatable checking core

Current development delta (2026-09-21): configuration and control-store schema
are now version 3; mathematical stage plans remain version 2 and use the explicit
`Domains.from_stage_plan` reader. The original extraction description below
is historical where it refers to configuration version 2. V3 adds cumulative
resource authorization, owner status/renewal and reserved terminal metadata
space without changing the mathematical sources/codecs/checker. See
`drafts/CAPACITY-V3-INTEGRATION-REVIEW.md`, `API.md` and `CHECKPOINT.md` for the
current qualification boundary. No old installed state is automatically upgraded.

Implementation handoff, 2026-09-21. Authored and read-only inspected; this note
does not claim execution, test success, release qualification, or multi-host
operation. The experimental originals remain unchanged.

## Operator configuration and paths

The checker keeps its `Checker(config, work_dir, allocate_stage)` interface and
the existing bootstrap, offer, admit, submit, and publication gates. Schema 2
adds an exact `domains` record with absolute operator-selected directory paths:

| Domain | Contents and authority |
| --- | --- |
| `install` | Product sources in `py`, native sources/build products, immutable canonical assets in `assets`. |
| `state` | This node's database, packages, historical evidence; ordinary checking writes only below `state/work`. |
| `scratch` | Separate owner-selected staging and read-only inspection work; no state mutation is implied. |
| `lean_runtime` | The selected runtime directory; Lean must be exactly `bin/lean.exe` beneath it. |

State and scratch cannot overlap each other, installation, or runtime. Runtime
may be nested inside installation but cannot equal or contain installation.
Drive/share roots are refused. Work directories are strict descendants of
`state/work` or scratch; each stage is a new strict descendant of its selected
request directory. Read permission for pinned files is confined to these four
domains. Canonical packages must be under installation assets, state, or
scratch. The exact current Python executable has a separate pin-validation
exception; its containing directory is not a general input domain.

`domains.py` exposes `Domains.from_config`, `Domains.from_record`, `as_dict`,
`require_state`, `require_read`, `require_work`, `require_write`, `require_stage`,
`require_package`, and `require_lean`. `config.files.domains` is required and pins
the installed helper by exact path, byte length, and SHA-256. The checker and
runner must likewise reside in the configured installation's `py` directory.
Python launches use `-B -E -s -S`; the checker, runner, and internal worker reject
startup without the corresponding bytecode/environment/user-site/site flags.
Sibling imports remain available. This is not hostile-code isolation or whole
runtime attestation.

## Stage handoff

An owner-created execution plan retains the existing Lean/Python pins, input
snapshots, commands, and resource maxima. It additionally binds `schema: 2`,
normalized `domains`, the installed `domains_source` file pin,
`request_directory`, `stage_directory`, and the exact string `stage` identifier.
The inputs include `domains.py` with precisely that source pin. The plan file
itself must be inside the selected request directory.

The runner authenticates the expected plan hash, strict JSON, domain binding,
installed runner/helper pins, exact executables, and resource profile before
creating the stage directory. It writes the authenticated plan bytes into the
stage and snapshots inputs. Receipts bind the domains and request directory;
checker receipt validation compares these with current configuration as well
as authenticating input snapshots, actual commands, outputs, and quiescence.
Only `$RUN` and `$RUNTIME` substitutions remain; there is no project-root path.
Build stages may use a request directory under scratch and the same runner;
successful support compilation is not mathematical acceptance.

The source-to-canonical and inverse workers receive the domain binding through
their generated, snapshotted job record. Before helper loading or output
creation they bind their exact stage/input locations, plan/receipt hash, job,
checking/helper/codec/seed snapshots, and helper digest. Each action uses its
exact expected stage log and output directory. Inherited packages remain
manifest-authenticated inputs from permitted package domains.

## Preserved acceptance and failure rules

The canonical manifest/content/closure/inventory checks, selected context union,
fresh native receiving admission, all five contribution children, source
capture, native candidate/inverse replay, and publication reauthentication remain
the mathematical acceptance path. No SQL or global-history census was added to
the checker. Candidate offers are not accepted mathematical results.

Native stages retain the 300-second, 4096-MiB private-commit, 512-MiB selected
byte maxima and one-active-child Windows Job policy. Time/output polling can
overshoot; such stages cannot pass the envelope. Pre-authentication time remains
part of the runner's stage elapsed time. Missing or unauthenticated receipts do
not clear charged pending stages; startup failure may correctly leave no stage
directory at all. Source rejection is reported only through the existing
authenticated one-child diagnostic failure path.

All domains, configuration, and executable source belong to the cooperative
operator-local trust boundary. A peer may eventually supply canonical package
data, not these paths, source programs, or acceptance credentials. Filesystem
checks are not race-proof confinement against a hostile local account modifying
paths or runtime files. This extraction supports fresh-install relocation;
moving already-used state still requires a separate migration design because
historical receipts bind absolute paths.
