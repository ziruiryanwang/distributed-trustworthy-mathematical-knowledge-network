# Source handoff: friction and the remaining installation evidence

2026-10-26. Reviewer: `owner_concurrency_boundary`. Source and saved-report
inspection only. No product import, build, test, network, state access, Git
mutation, installer implementation or source-package change was performed.
The canonical workspace guard passed. Full v5 remains unfinished and unpublished.

## Decision

The declared default installation route has **no demonstrated remaining
historical-generated-identity obstruction**. Its five stages accept the actual
selected preceding output identities while retaining fixed supported source,
runtime, role and interface checks. The main visible friction is manual staging,
receipt/hash handoff and navigation past historical instructions.

That does not close the release-evidence question. The exact 143-payload source
archive has **not been shown by the retained evidence to complete a fresh native
build and all four overlays as one archive-only installation**. One such bounded
installation, followed by a cheap final public manual-query smoke, is a meaningful
unperformed release gate. It is not a reason to invent another installer, repeat
mathematical campaigns or add a new overlay.

## Authoritative route and source contract

Start from `software/v5/ordinary_release_bundle/ADOPTION.md` and `README.md`.
The latter explicitly overrides included historical instructions. The source
ZIP is:

`experiments/v5-local-checks/transport-release-handoff01/suite/packed/source.zip`

- ZIP SHA-256: `897a6eb57056b911b200551413c65ce7788ba3d448ff8b6b8c143d883180ebd0`.
- Manifest SHA-256: `f1beab01d43e4b5fc6d7b9999ff2795598e3f2ee77c0dc85f1d99e82a15b31f1`.
- 143 payloads plus SOURCE-MANIFEST; 3,789,448 ZIP bytes.
- Supported runtime profile: Windows x86-64, Python 3.14.6 and Lean 4.34.0,
  with the declared exact named-runtime pins. Arbitrary custom builds carrying
  those version labels are not thereby supported or approved.

| Stage | Identity rule relevant to a fresh source installation |
|---|---|
| `ordinary_bounded_operations/build.py` | Explicit source/runtime roots and fresh output; produces actual package/PROFILE/installation identities and `_build/BUILD-RESULT.json`, status `BUILT_NOT_ADOPTED`. No historical native output is an input. |
| `ordinary_fair_search/assemble.py` | Takes actual base PROFILE and `--base-build-receipt` plus their selected hashes; validates fixed builder/source-map/layout and actual complete bytes. Newly generated native pins are permitted. |
| `ordinary_contact_federation/assemble.py` | Takes actual fair package/PROFILE and immediate `--base-receipt`; validates the fair source/role/layout contract and actual byte map. |
| `ordinary_sparse_access/assemble.py` | Takes actual contact package/PROFILE and immediate receipt; preserves the actual generated installation/native identities. |
| `ordinary_transport_release/assemble.py` | Takes actual sparse package/PROFILE/receipt. Its `validate_base_interface` binds 45 fixed noncompiled auxiliary roles, 72 generated native auxiliary roles, 19 fixed installation sources, eight receiver objects and nine fixed runtime pins. Generated identities may differ while source/layout/support commitments remain coherent. |

All four overlays copy existing native outputs; none recompiles them. Final
offline operation preparation uses `ordinary_bounded_transport/prepare_selected.py`
with the **actual final PROFILE hash**. Its known-layout check binds the selected
noncompiled interfaces and native role names, rather than historical native hashes.
Its in-memory helper PROFILE rebinding does not edit a frozen source file.

Do not substitute historical `ordinary_bounded_transport/assemble.py`, which
was locked to an old generated base, or `ordinary_network_kit/prepare_selected.py`,
which rejects the repaired final provider identity. Neither is the selected final
route. Contact/sparse guides retain some historical surrounding examples, but
their current CLI argument names and immediate-predecessor contract are present.
This is navigation complexity, not an established missing interface.

## What has actually run

The closest evidence is complementary, not a complete fresh-archive installation:

1. **Actual fresh native source build:**
   `experiments/v5-local-checks/bounded-investigator-src01`. The independent
   saved-output audit is in `software/v5/ordinary_bounded_operations/REVIEW.md`,
   section "Actual clean-source build". It used the same selected builder
   (`79a056932d5720e9ab964ee50a01d1b04569a60a5e6445df0070a2b6556b42f9`)
   and source map
   (`e9b7a873c8e509651833de51e5bd6beda130c74fdf7391859a8661c08426396a`).
   Its explicit source root was the **full canonical checkout**, not the later
   compact source extraction. The builder staged 86 inputs, generated a fresh
   146-file package and recorded fresh actual receipts. Native generation and
   complete package integrity passed; this is not an archive-only closure test.
2. **Actual successive file-only overlays:** fair, contact and sparse used that
   existing generated native package. Contact/sparse saved audits are in
   `research/cycles/v5-2026-10-25-software-continuation/CONTACT-ASSEMBLY-OUTCOME.md`
   and `SPARSE-ASSEMBLY-OUTCOME.md`. They establish actual selected byte
   preservation and package/receipt coherence, not new native generation.
3. **Exact current ZIP and relocated final handoff:**
   `software/v5/ordinary_transport_release/OUTCOME.md` audits
   `transport-release-handoff01`: exact 143-payload pack/extraction, relocated
   verifier, relocated final transport assembler and final offline selector.
   The assembler input was the **retained actual sparse package**, not a newly
   built package from that ZIP. The changed generated-identity control used
   synthetic parsed metadata, not newly compiled artifacts. The relocation is
   under the canonical project's `experiments` tree, not outside the project.

Thus neither a complete fresh archive-to-final-package chain nor an independently
performed installation follows by combining those reports. Conversely, the native
implementation is not untested: the missing boundary is **source-distribution
closure and complete actual fresh-generated chain integration**, not a mandate
to redo all correctness tests.

## Cost evidence and limits

The retained bounded native build reports:

| Quantity | Actual value or selected limit |
|---|---:|
| Total outer elapsed time | 60.078679 seconds |
| Inclusive Job CPU | 52.0 seconds |
| Separate outer wrapper CPU | 1.328125 seconds |
| Known CPU total | 53.328125 seconds |
| Peak Job private commitment | 925,749,248 bytes, about 882.863 MiB |
| Selected inner build limits | 480 wall / 360 CPU seconds / 2048 MiB |
| Selected outer limits | 540 wall / 440 CPU seconds / 2304 MiB / eight active processes |

Inner native/child CPU is included in the outer Job CPU and must not be added
again. The saved build closed all reported Jobs with no active processes or
cleanup errors. These figures are one local observation, not a success promise,
minimum RAM requirement, hard disk cap or hostile-code sandbox.

The builder's declared valid bounds are 120-3600 wall seconds, 100-3600 aggregate
CPU seconds and 256-8192 MiB. Its guide's 600/600/2048 example is an allowance,
not an observed need. Contact and sparse file-only assemblies took about 5.03
and 4.71 wall seconds respectively, with 1.578125 and 1.296875 Job CPU seconds.
The current transport handoff suite took 15.883160 wall / 8.078125 known CPU
seconds and about 145 MiB peak commitment, but included several controls and
packing/relocation in addition to assembly. These are not additive predictions
for a new driver. The retained costs make one finite full-chain check plausible
on this PC; a 60-90 CPU-second expectation remains an estimate, not a guarantee.

## Highest-payoff next action and challenge

The root's proposed one-time release check is justified if its selection enforces:

- Use the **exact approved ZIP**, freshly extracted, with no missing source
  supplied from the full checkout. All product stages select that extracted
  source root. A fresh canonical-root leaf preserves the workspace invariant;
  physical placement outside the project is not necessary for this gate.
- Compile once using existing supported runtimes, then run the four public
  overlays in order with actual new immediate receipts/PROFILE hashes. No old
  generated package or installation may substitute for a stage output.
- Require each actual terminal receipt and complete final package binding,
  not mere presence of PROFILE. Keep partial failures and stop on a failed stage;
  do not silently repair the archive or renew the operation.
- Finish with one cheap state-free public manual-query operation against the
  actual final package/profile. This checks launcher/loader coherence, not
  mathematics, network service, peer independence or theoretical growth.
- Reuse existing bounded execution and saved-output review mechanisms. Do not
  implement a new general installer or expand the run into old test campaigns.

An archive-only input contract plus source inspection reduces accidental
dependence on the full checkout; it does not establish OS-level hidden-read
isolation. Shared approved external runtimes remain explicit dependencies.
Any claim of independent-user or independent-host deployment still needs its
own evidence. Passing this gate would close a concrete local release obligation,
not the entire v5 objective.

New companion utilities/documentation outside the frozen archive are separate
deliverables, not corruption of the old closure. Do not automatically repack the
archive or fold them into this gate. A future orchestration helper may reduce
manual friction, but it should respond to an actual operator failure or measured
repeated cost; no such helper is selected by this audit.
