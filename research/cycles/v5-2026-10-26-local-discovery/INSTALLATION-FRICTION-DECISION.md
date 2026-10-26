# Installation friction: ship approved bytes before inventing an installer

2026-10-26. Source/metadata decision only. No packing, build, test, product import,
state access, publication or Git change. The adopted source handoff is not reopened.

## Recommendation

If root selects installation work next, prefer **one prebuilt exact package archive
with external approved runtimes**, alongside the already adopted source handoff.
Do not create an aggregate installer now. This removes real repeated setup work
without changing product bytes, mathematical trust or runtime selection.

This is a demonstrated **convenience/distribution gap**, not evidence that current
installation is impossible: the existing source-archive installation succeeded.
No independent new-user setup failure or need for automatic installation has been
demonstrated. Its marginal payoff must be weighed against a concrete real-library
obstruction; do not launch another broad installation campaign to find one.

## Evidence and the actual payload

The current README requires a native build, then fair/contact/sparse/transport/
exact-module/multi-source file overlays: seven deliberate stages with actual
intermediate receipts, fresh directories and selected PROFILE identities.
Keeping those choices explicit is sound, but manually reproducing them adds
operator work when the desired final bytes already exist.

The adopted package is
`experiments/v5-local-checks/multi-source-package01/suite/assembled/package`.
Its PROFILE is `ca257419f464c2e9d968011983673160377f743ebbe2a27e2399b510dce1ce67`;
its unchanged INSTALLATION is
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
Read-only metadata reconstruction gives:

| Included part | Files |
|---|---:|
| PROFILE-selected auxiliary payloads | 117 |
| Nonruntime INSTALLATION payloads | 27 |
| Exact selected documentation | 8 |
| PROFILE and INSTALLATION manifests | 2 |
| Total | 154 |

Declared payload size is **39,148,493 bytes**, excluding external runtimes. This
is a metadata sum, not a new whole-tree verification or existing ZIP size.
The package/preparer integration and later actual retained-context reopening are
adopted; neither alone establishes a newly archived/relocated final package.

`ordinary_archive_install/ADOPTION.md` records an actual source-only archive
installation through the earlier transport overlay: seven public calls,
144.5682446 wall seconds, 72.0 known CPU seconds and 941,723,648 bytes peak Job
commitment. These are observed costs, not new-user requirements or final-six-overlay
timing. `ORDINARY-PACKAGE-OUTCOME.md` separately records relocation of the original
111-file native package without `_build`, successful initialization, preserved
caller-source failure and later corrected contribution/reopen. Reuse those facts;
do not repeat them or transfer their narrow pass to an untested archive automatically.

## Three choices

| Choice | Actual benefit | Cost/risk | Decision |
|---|---|---|---|
| Existing manual recipe | Already documented; source build plus explicit immediate-predecessor checks; no new delivery component. | Repeated compilation, copies and seven-stage path/hash bookkeeping; build failures remain possible. | Keep as rebuild/customization fallback. |
| Exact prebuilt package archive | Recipients extract one unchanged final runtime payload; skip helper compilation and all six overlays. | Must approve executable artifacts and exact provenance; platform/runtime pins remain; archive identity/relocation needs a narrow gate. | Smallest practical setup improvement. |
| New aggregate installer | Could orchestrate those stages or runtime downloads and hide some manual choices. | Another executable/retry/partial-state/update surface; no current proof users need this; wrapping compilation does not remove its cost. | Defer; no demonstrated necessity. |

## Why an exact prebuilt package is plausible

`ordinary_multi_source_package/assemble.py` already reconstructs the whole package
map from PROFILE, INSTALLATION and its selected receipt's documentation rows.
`ordinary_fair_search/assemble.py` supplies bounded ordinary-path, pin and exact
census primitives suitable for native-sized files. Reuse their file-only boundary;
do not use a predecessor-specific assembler to reapply an already applied overlay.
The source-bundle utility's 2 MiB/file and 8 MiB/total caps are deliberately smaller
than this native payload; do not blindly widen them or pretend it is its packer.

The profile loader resolves package files relative to the supplied package root;
NativeInstallation resolves runtime-role paths under explicit caller-selected
runtime roots. The build directory and original absolute build paths are not
operation dependencies. Exact PROFILE/INSTALLATION remain unchanged by relocation.
The launcher checks bootstrap support; its child checks the full package and named
runtime attachments. The offline selector alone checks only its stated interface
and is **not** a native-artifact validator. `--help` is not a relocation gate.

An archive can therefore contain exactly those 154 files at their original relative
paths, with full-map/digest receipt and current quick-start **outside** the immutable
package. Keep ASSEMBLY evidence as evidence, not a rewritten receipt claiming the
archive was newly built. Exclude `_build`, owner data, diagnostics, secrets and
runtimes. Use the existing coherent source extraction for query companions,
mirror and current selector/guides; do not duplicate them into the package.

## External prerequisites remain explicit

Require independently approved Windows x86-64/little-endian/64-bit, Python 3.14.6
and Lean 4.34.0 distributions; use the actual selected Python with `-I -S -B`.
Nine named attachments are pinned: python.exe, python3.dll, python314.dll; Lean's
bin/lean.exe, libInit_shared.dll, libc++.dll and libleanshared{,_1,_2}.dll.
Complete ordinary runtime support is still needed: Python stdlib/SQLite/TLS and
Lean libraries/toolchain components used by the chosen operations. Nine pins do
not attest all dependencies. Do not advertise arbitrary newer runtimes, Linux/macOS,
hermeticity or that a mathematical investigator no longer needs Lean.

Users still select protected ordinary absolute Windows paths, fresh output leaves
with existing parents, finite resource allowances, actual data/contacts and local
execution approvals. Mathematical owners initialize their own fresh state; no
author's checked owner is shipped as portable trust. Existing owners retain their
approved exact identity/limits and recovery rules. A mirror needs only its existing
source/Python route and gains nothing from downloading native investigator bytes.
Hash selection does not authenticate a publisher or sandbox code. License, public
release authorization, release-signing and external runtime distribution remain
unsettled; local prebuilt convenience must not silently decide them.

## Cheapest validation if selected

Use one bounded file-only whole-map pack/readback and fresh extraction comparison,
preserving all 154 pins, original manifest identities and extra/alias refusal.
Use existing path/census/pin primitives and an ordinary ZIP container, not an
automatic download/update/install service. Then one state-free bounded **public
query preparation** from that relocated package can exercise full support/runtime
loading without native proof work or owner state. Reuse the existing inert query
form and check all terminal closure conditions; no fresh init/contribution/service
campaign is needed for a byte-preserving archive. Root selects any such execution
separately. Stop after exact archive/relocation/navigation adoption; do not repack
the source handoff or expand this into another installer project.
