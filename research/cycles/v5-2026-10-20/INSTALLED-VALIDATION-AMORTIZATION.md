# Installed validation: eliminate unrelated work before adding persistence

2026-10-22; source-only investigation by `storage_launch_review`, assigned by
root after the completed distribution audit. Canonical root only. No product
edit, import, benchmark, test, constructor or native/proof call was selected or
performed. Counts below are read-only sums of the already bound release map,
not new runtime measurements.

## Recommendation

The smallest consequential next seam is **producer-only exclusion of unused
Lean content hashing**, not a new persistent service or broader cache. Keep
the existing complete physical census and every non-Lean validation unchanged.
Keep full hashing at build/explicit `verify` and in ordinary consumer paths;
only the `producer-profile` and `producer` paths omit the unused Lean hash loop.
Keep all current producer-owner, child-import, request, deadline and post-
operation checks. This is a proposal, not edit authority.

There is a real locality defect in the current public producer entry: a
producer-only action checks the ordinary Lean library even though that action
does not consume it. A first draft proposed dropping the global physical census
as well. Independent review correctly identified that census also rejects
extra import/DLL candidates, so that broader proposal is **not** recommended
without a separate namespace/dependency argument. Fixing the narrower hash
dependency does not require predicting a cache hit rate,
changing owner lifetimes or rerunning a large mathematical experiment.

The reported renewal cost (54.515625 full CPU versus 0.03125 verification and
1.59375 author CPU) motivates looking at setup, but does **not** identify its
cause or prove this seam speeds that different ordinary-client operation.
No savings percentage for that run is inferred here.

## Exact current source and what is already reused

Selection is the current130 input `25e7c849...`, now preserved unchanged inside
the full144 release `8a326340...`. Do not substitute similarly named historical
files in `software/`.

| Selected source | SHA-256 | Existing behavior |
|---|---|---|
| `standalone_validation/admission/pin_phase.py` | `ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881` | Successful pin/trust/origin observations reused only inside one synchronous validation phase; fresh exit sweep; records discarded. |
| `trust_withdrawal/client/runtime.py` | `70c52b5148c481ca840c6c55557c9bc5abf71f40d522365f0cb7b0398adbad39` | Stable role description and explicit persistent trust binding; fresh verifier/preparation owners for each new operation grant. |
| `candidate_admission/admission/verifier.py` | `ec6474cdd0580df89f9c646a41c0d909ec20e83da0a42274e0510a6e01bbbaea` | `_fresh_install_check` uses the existing pin phase, never borrows a pre-subprocess cache; withdrawal revokes handles. |
| `preparation/owner.py` | `a51482da62bffe4dabeb48c2a4fcb7842530a8543aa42ba287fc20c0d0cf3187` | One serialized finite owner permits multiple calls (at most16); checks profile/pins around stages and completion; failures close it. |
| `interface_views/authoring_atomic.py` | `081d9d18d16d1cd68b40a5f3cf52493bac7e2e2dbdfb9bd632b72d74de235dbc` | Reuses `OwnerPreparation`; repeated requests share its original allowance/owner, but each authoring stage remains supervised and produces untrusted material. |
| `authoring/worker.py` | `aeaad858c90da4f244801dc24f62a96550a6457381da5085a5bbc28939754137` | Rebinds selected worker/native/request/runtime before and after the actual native process. |

`production/producer.py` (`5555e944...`) also reuses already loaded, exactly
source-bound supervisor modules in the same process. Its `_check`, and the
preparation owner's `_check` that calls it, still freshly hash their selected
pin sets. They do not use the admission phase helper. That is a possible later
local optimization seam, not evidence that all duplicate reads are already gone.

The distribution `path_scope` (`afbea96b...`, lines414 onward) already coalesces
directory-ancestry validation. It does not cache file content, and nested scopes
start fresh. Adding the same directory cache again would duplicate existing work.

## The source-level avoidable term

In the installed distribution:

1. `installed_production_release` calls `verify_release(..., full=False)`.
2. `_verify_release` always performs `census(root, manifest["files"])` over
   the complete installation and hashes every non-base payload plus the base
   manifest. `full=False` means only some base hashes are omitted; it is not a
   producer-role filter.
3. `producer_profile` repeats that same verification before committing its
   output. It therefore has two complete physical censuses and two large main
   hash loops, in addition to its metadata/request checks.

Exact current manifest-derived quantities:

| Work set | Files | Bytes |
|---|---:|---:|
| Complete payload census | 9,894 | 919,541,411 |
| Each existing `full=False` main hash loop | 3,411 | 758,886,905 |
| Lean subtree included in that loop | 3,250 | 601,942,392 |
| Proposed first seam's retained main hash loop | 161 | 156,944,513 |
| Deferred producer bootstrap role union, not sufficient alone | 63 | 97,673,992 |
| Existing producer child full Python closure, separately retained | 584 | 30,459,330 |

The deferred 63-role union is operative60 plus `distribution.py`, the installed
`release_production/launch.py`, and `production/PROFILE-TEMPLATE.json`.
It includes the 2,375,023-byte release manifest. The existing main-loop byte
count does not include every repeated manifest/helper read, so these columns
are explicit work-set sizes, not matched total-I/O or elapsed-time benchmarks.
The first seam retains both complete censuses and removes exactly the selected
601,942,392-byte Lean subtree from each main hash sweep, not all physical work
outside the 63-role set.

Do not confuse support-runtime49 or operative60 with the full interpreter
closure. The installed operator (`f404f0ba...`, `_bootstrap` and
`verify_imports`) already performs a 584-file Python census/hash before imports
and again on final validation. It uses a guarded importer and held exact
product-source bytes. Those checks remain unchanged in the proposed seam.

## Minimal implementation contract

Introduce one closed internal producer-purpose validation branch, used only
at `installed_production_release` and the profile's final rebind. It is not a
caller-supplied exclusion list. Do not change `build`, explicit complete
`verify`, or ordinary consumer `launch` semantics.

Its acceptance obligations are:

- Read and hash the owner-supplied exact release manifest; keep its existing
  bounded grammar, case/path-alias exclusions and role relationships. The root
  digest is supplied by the owner, not inferred from arbitrary downloaded data.
- Retain the complete physical census, including checks for missing/extra
  paths, directory ancestry, symlinks/junctions and file-map spelling. Do not
  borrow the child's guarded import argument to remove parent/native namespace
  checks. A missing or extra Lean file still refuses this first version.
- Hold and execute the exactly manifest-pinned contract helper, as today.
  Validate exact descriptor/template mathematics, core31 and runtime roles.
  Keep all existing role checks; no caller-selected role list may omit
  inconvenient dependencies.
- Canonicalize/check ordinary ancestry for every selected path, verify its
  actual bytes against the manifest, except the fixed unused `assets/lean/`
  subtree in this producer-only branch, and bind the selected base manifest,
  supervisors, executable/DLL/runtime pins and native artifacts. Reading only
  metadata or trusting file size/mtime is not sufficient.
- Preserve fresh final checks and the pending-last-unlink commit. Profile
  creation repeats this same census/retained-byte check before success; producer launch
  leaves the existing launcher, guarded child importer, actual owner60 checks,
  live requests and output/cleanup validation intact.
- State the result's scope as **producer-role readiness**, not “all payloads
  in this directory were checked.” Complete-release inspection remains the
  explicit `verify` operation. No new mathematical trust, allowance or proof
  acceptance is created by either result.

For a pinned manifest M, full physical verification implies the proposed
producer-purpose verification. The converse intentionally does not hold:
content corruption of an existing unused Lean payload may block complete
verification without blocking producer readiness. Missing/extra paths still
block both because the complete census remains. This is an explicit separation
of capabilities, not an unnoticed weakening of the old global content-integrity
claim.

The soundness argument is conditional: the producer's executed/imported
product code, native inputs and selected runtime must not consume the omitted
Lean subtree except as separately explicit/pinned request inputs. Current
producer-role methods do not select Lean roles or invoke the Lean frontend;
native stage/snapshot commands use explicit executable/image/capsule paths and
the release root as cwd. The unchanged supervisor strips inherited language
variables and replaces PATH with its fixed receiver executable directories,
not `assets/lean`. Existing held-source imports and all current owner checks
remain. Any explicit request input still has its own original pin checks.

This does not prove a hermetic Windows loader. Parent imports before the child,
executable-directory/current-directory DLL search, SystemRoot and other host
OS configuration remain the existing trusted-local assumptions. In particular,
the child's 584-file Python check cannot be used as a proof of the parent's
already executed imports or every native DLL dependency. Retaining census
prevents newly added local candidates that the old path rejected. If a proposed
deployment intentionally makes `assets/lean` part of producer bootstrap/native
loader configuration, the unused-subtree premise fails and it must retain full
hashing or first change that explicitly selected environment. Root should adopt
this dependency/host-assumption boundary before selecting implementation.

This optimization does **not** remove the complete manifest's in-memory
parsing/grammar term or complete physical traversal. Its structural form remains
O(|M| + all-payload metadata + retained hash bytes); only the unrelated Lean
content term is removed. The stronger 63-file no-census design is deferred,
not proved safe by a small role count. No global-corpus-independent constant
time follows. A small separately committed role manifest is a possible later
design, not needed for this seam.

## Persistence and batching: useful, but not the first change

Existing multi-call owners already amortize construction within a finite
operation. Local agents can use those APIs under their original deadlines,
resource charges and single-client constraints. Do not add a second batching
framework simply to reproduce this capability.

A long-lived front end could reduce repeated process/import setup across
requests, but it cannot recycle spent grants, turn saved JSON into authority,
or ignore trust withdrawal. New grants still require fresh operation owners;
session handles retain their original owner identities. In particular, the
existing pin phase explicitly forbids spanning an await, subprocess, network
I/O or user callback. Broadening its lifetime is a security-contract change,
not a harmless cache-size increase.

The current assumption is an owner-controlled, stable local filesystem during
one validation/operation boundary; neither existing checks nor this proposal
provide a hostile-local-mutation sandbox. An across-operation hash cache would
need an additionally justified immutable-installation regime or fresh byte
checking. A digest file, mtime cache or previous successful launch alone does
not establish that regime. Warm process lifetime can be useful without taking
that shortcut, but its lifecycle/cleanup/withdrawal complexity makes the
role-scoped seam the higher-payoff first choice.

## Small discriminating evidence, only if root selects the change

Theoretical dependency review comes first. Then a small changed-boundary test
can require: selected-role corruption refuses; content corruption of an existing
unused Lean payload does not affect producer readiness but fails explicit
complete verification; missing/extra Lean or other files still refuse; incorrect
descriptor/template/role omission refuses; selected symlink/junction refuses;
and late selected-byte change preserves pending/nonadoption. Preserve both
consumer/producer image identities and existing consumer validation unchanged.
One genuine public profile path can validate integration. No new proof,
planet-scale run, broad benchmark or repeated existing campaign is necessary
to decide whether this locality seam is correctly implemented.
