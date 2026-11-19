# Fair-search package and selected operator kit: independent source review

Reviewer: `/root/onboarding_controls`. Disposition: **SOURCE GO for root's
separately selected file assembly and bounded integration controls**, not an
execution result, mathematical qualification or full-v5 release decision.

I did not author the fair-search implementation, assembler, package smoke,
selected-package wrapper or selected-package tests. I previously authored the
frozen operator-kit controls/review and audited their actual results; that prior
work is identified rather than presented as independent review of my own tests.
This review used source reads, metadata comparison and hashes only: no product
imports, syntax compilation, native processes, sockets, test runs, existing
mathematical state or Git mutations.

## Exact reviewed inputs

Paths in this section are relative to `software/v5/` in the canonical root.

| Input | SHA-256 |
|---|---|
| ordinary_fair_search/assemble.py | `9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30` |
| ordinary_fair_search/README.md | `c3d8642b6fe9ece1b12c3a313910d14c52442b78a94c8af1b44dbe0901115aa5` |
| ordinary_fair_search/test_package.py | `491445c71029f4ac40d9d9754b8061119114a092acd8d287096a5a0216ff69f4` |
| ordinary_operator_kit/prepare_selected.py | `9a2436210a869d815ec3c353250345424d540c6f1b4e765a20c4f8af86bcc6cc` |
| ordinary_operator_kit/compatibility.json | `b5a812c90a8edc930a3a1b2859a7f77e5799772a516e1478bb04ae7add7abfe2` |
| ordinary_operator_kit/test_selected.py | `702a95365cef7c4a8dd5f9ea6927ef5fadc86b3f696809a06e07b018b37102b6` |
| ordinary_operator_kit/SELECTED-PACKAGE.md | `365a6d76a36e338cd6dfb7d71daddb8136e63743fb1e395afb169cc89167b63c` |

The implementation inputs already reviewed and used in the sixteen-control run
remain frozen: fair_exchange `3fe626b2...`, fair_search `2567fcb2...`, peer_api
`06663bcd...`, profile `828031e8...`. Their full identities are fixed by the
assembler and compatibility map. Earlier controls establish their disclosed
native-free boundary, not the new public-package execution path.

The proposed current baseline is
`experiments/v5-local-checks/bounded-investigator-src01/distribution/package`:
PROFILE `9c41b9a3fe36f7283af130ac6ef290e82c2a78c432980b2bea75ccdcf197a6d4`,
installation manifest
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
The saved external build receipt was read and its builder/source-map/documentation
and implementation fields agree with the assembler's requirements. The wrapper's
41 baseline source-role pins were separately compared to that saved PROFILE:
no mismatches. Root still selects the exact receipt hash and output paths.

## File-only assembly

The selected baseline map is not merely the PROFILE auxiliary subset. The
assembler reconstructs 113 auxiliary files, 27 local installation payloads,
INSTALLATION.json, four documents and PROFILE.json: 146 files. Nine external
runtime attachments are validated as manifest pin data but never opened or
copied by assembly. Their later runtime verification remains the loader's job.

It checks the exact named layouts, explicit PROFILE/receipt hashes, expected
owner/loader versions, documentation pins, implementation-identity binding,
bounded file sizes, ordinary local paths and complete baseline file census.
Every selected baseline file is hashed before copying. The receipt's assertion
about a source build remains an operator-selected assertion; hashes are byte
identity, not authentication or a proof of compiler/source correspondence.

Only profile.py, peer_api.py and README.md replace existing payloads. Two support
modules are added. Thus 145 old non-PROFILE files minus three replacements gives
142 unchanged payloads, plus five selected overlay files gives 147 non-PROFILE
files. The new PROFILE has 115 auxiliary roles; final package count is 148.
No native file, installation manifest, launcher or other document changes.

Fresh output is required. Copying verifies source lengths/digests, flushes files,
and rechecks both original inputs and copied output before committing PROFILE.
The exact final census rejects extra files. PROFILE is written to a pending file
and renamed last inside the package. A separate ASSEMBLY.json records success;
zero exit and the matching receipt are required, since a late failure can leave
PROFILE or even a success-shaped receipt without a successful operation. Partial
output is preserved, never automatically removed, overwritten or retried.

Cooperative wall/CPU checks belong to one original allowance. They do not replace
an enclosing Job or protect against concurrent hostile local writers. The source
root may contain the fresh output under a disjoint experiments directory; actual
base/receipt/overlay inputs cannot be inside or overwritten by that output.

## One actual public-find discriminator

The package smoke's useful question is narrow: does the installed public launcher
load the new modules and reach later provider B after a settled stall at provider
A, without reopening the aggregate grant or treating discovery as acceptance?

The harness loads the selected package once in its own clean process through the
actual pinned loader, then uses the installed adapter/store/provider to create a
fresh one-object V3 index. The preview is deliberately synthetic and proof-free.
No Lean process or mathematical result is created. The actual public command runs
in a separate clean process, avoiding preloaded-module interference.

Provider A parses and binds the exact offer, sends nothing and observes client
EOF. B subclasses only to observe entry/closure around the unchanged real
Provider._serve. No protocol replies, matching checks, budget objects or verifier
are replaced. Exactly one public `run.py peer find` uses two loopback contacts.
The expected result binds the exact B record and snapshot, A's sole
`SettledRefusal/ATTEMPT_TIMEOUT`, one page/three actual requests, zero outstanding
session reservations, and the original eight-request/one-MiB outer prepayment.
Incomplete/global/coverage/acceptance flags must remain explicit and false where
appropriate; a returned record is not a theorem-admission claim.

All setup and the child share the original 80-wall/45-harness-CPU envelope. Launch
is refused unless at least 66 wall seconds remain for the fixed 60-wall/30-CPU
public call plus closure. The parent waits no later than its original deadline
minus five seconds. Root's proposed outer 90-wall/60-inclusive-CPU Job is the
whole-tree hard boundary; the harness's process_time alone excludes child CPU.
There is no fallback, second call or renewed original allowance.

Pass requires the public Job's successful closed/reaped state and zero cleanup
errors, parent child reaping, closed listeners, completed connection observers,
all writers' observed wait_closed, closed index, exact A/B connection counts and
settled B request/reservation counters. Cleanup failures cannot produce PASS.
An outer termination before the report still has to be interpreted through outer
evidence, not as absence of cost or a clean successful smoke.

This is deliberately same-host plain loopback and synthetic discovery metadata.
It does not qualify TLS, independent hosting, relevance/recall, hostility of local
source code, mathematical checking, latency under arbitrary CPU interference or
large-network growth. The actual loader/public-command boundary is new enough to
justify this one small test without repeating native mathematics campaigns.

## Explicit selected-package operator wrapper

The frozen preparer is loaded only after exact helper-byte verification, into a
fresh private module. No product code is imported, no global import path is
changed, and its PROFILE is set once to the explicitly selected per-call value.
The pinned compatibility map admits precisely the known baseline or coherent
fair-search auxiliary layout, rejects hybrids/extra roles/unknown source pins,
and checks actual bytes of all 41 or 43 known auxiliary noncompiled roles.

The map's own hash was independently recomputed. Native role sizes/hashes and the
installation-manifest identity are shape-checked but not approved by this helper.
In particular, installation core Python, supervisor, foundation and native
payloads are outside these 41/43 auxiliary-source checks. Explicit package/build
and runtime approval must cover them; the product loader retains its actual full
pin verification. The wrapper is interface preparation, not package authentication,
semantic/native equivalence or mathematical acceptance.

Original request/report bindings, duplicate/nonfinite/depth checks, ordinary path
restrictions, fresh outputs and explicit manual approval gates remain delegated
to the unchanged helper. Report-contained producer paths are never followed;
legitimately relocated input bundles remain possible through exact byte/semantic
bindings. No existing owner/index state is opened. A final cooperative timeout can
leave generated files; absence of the wrapper's successful return must not be
turned into an automatic rerun or silently adopted result.

The twelve selected tests cover coherent original/fair layouts, explicit native
identity variability without approval, hybrid/extra/unknown/boolean/schema
refusals, actual original 41-role and assembled fair 43-role selections, wrong
PROFILE refusal before writes, and same-length changed-source refusal before
writes. Subprocess/socket/SQLite entrypoints are trapped. These controls exercise
only inert preparation and are not a second version of the earlier 74-case suite.

## Disposition and next evidence

No consequential source blocker remains for these exact bytes. Root may select
file-only assembly, inspect its actual receipt/payload identities, then select
the twelve controls and one public loopback smoke in parallel under separate
finite envelopes. Execution results require their own saved-output audits;
this document does not predict PASS. Used implementation/evidence remain frozen.

The one requested documentation clarification is resolved in the reviewed guide
revision above: package approval covers the entire installation, including its
core Python/supervisor/foundation, not only generated native binaries. Its edited
paragraph explicitly limits the wrapper to auxiliary-interface compatibility and
leaves installed-component approval/checking to the operator and product loader.
No source change, second product loader or native mathematics retest was needed.
