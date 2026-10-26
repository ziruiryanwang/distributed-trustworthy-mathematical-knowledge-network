# Fresh-build closure: independent source investigation

2026-10-25. Scope: source/data inspection only. No imports, compilation, test,
network, package mutation, existing-state access or Git action. The canonical
guard passed. This is not an independent-host execution result.

## Decision

**The historical generated-base pins in the bounded-transport assembler are
the demonstrated installation blocker.** The preceding bounded build -> fair ->
contact -> sparse chain already propagates independently generated native byte
identities. The newest selected-package preparer also accepts such identities.
No second hardcoded generated identity or old absolute path was found in those
selected installation/launch interfaces. Preserve their source-version and
supported-runtime pins; they are different from historical generated-output pins.

## Trace and source identities

| Stage | Actual source rule |
|---|---|
| `ordinary_bounded_operations/build.py` (`79a05693...`) | Builds through pinned `ordinary_package/build.py`; records actual receiver/authoring compiler outputs, both exporter executables and query companions. Installation support digests and final PROFILE are derived from those actual bytes, not historical binary pins. Source-map SHA `e9b7a873...` and toolchain pins select a supported source/runtime version. |
| `ordinary_fair_search/assemble.py` (`9acc1b24...`) | Accepts caller-selected PROFILE/build-receipt hashes, checks the pinned builder/source-map identities, computes the actual installation implementation ID and preserves native payload pins. Fixed owner/loader/overlay/document pins describe source versions. |
| `ordinary_contact_federation/assemble.py` (`77feac69...`) | Accepts caller-selected fair PROFILE/receipt; requires the fair assembler identity and role census. Reads the installation manifest bound by that PROFILE and carries actual native pins forward. |
| `ordinary_sparse_access/assemble.py` (`3c2a197e...`) | Accepts caller-selected contact PROFILE/receipt; requires the contact assembler identity and role census. Preserves the selected installation and native pins. |
| Current `ordinary_bounded_transport/assemble.py` (`1633315b...`) | Requires the historical PROFILE `97f93cc6...`, ASSEMBLY receipt `b138a640...` and installation manifest `32236aa3...`, in addition to the source assembler identity. These generated-instance restrictions block an otherwise compatible fresh build. |
| `ordinary_bounded_transport/prepare_selected.py` (`5a4b1e36...`) | Requires exact 45 noncompiled interface pins and 72 native role names, but only bounded well-formed pins for native bytes. The installation hash is caller-selected via the approved PROFILE; the private helper's PROFILE variable is explicitly rebound to it. |

The full source identities relevant to the last boundary remain in the existing
bounded-transport REVIEW.md. Builder/overlay source names above identify exact
unchanged files, not permission to edit them.

The current transport check fails immediately if either supplied historical
PROFILE/receipt hash differs (`TRANSPORT_EXACT_SPARSE_BASE_REQUIRED`), and its
layout check separately requires the historical installation hash. Even if
native compilation happened to be byte-identical, an independently generated
assembly receipt contains its own package path and measured times, so requiring
one historical receipt is not a valid fresh-install interface.

## Symbolic final interface closure

Without executing product code, the reviewer reconstructed noncompiled outputs
from the bounded builder's 64-copy source map and the exact fair/contact/sparse/
transport overlay maps. The result has **45 noncompiled auxiliary roles**, with
exactly the names, lengths and hashes in the newest compatibility map: zero
mismatches or extra roles. Native auxiliary roles are the fourteen five-file
helper groups plus two exporter executables: **72 roles**. The installation's
eight receiver objects are separately bound by its actual installation manifest.

Thus no compatibility-map rewrite is required merely because a fresh build
produces different native hashes. The source-build records and installation
assembler compute actual support commitments. `NativeInstallation.open` verifies
those selected bytes and commitments; it does not compare the implementation ID
with a historical instance. The fixed mathematical basis/semantic contract stays
fixed, which is intentional. A fresh implementation is not permission to reuse
another installation's protected native snapshots or silently migrate old state.

Source/runtime/package/output locations are explicit CLI arguments or relative
paths under the selected source/package roots. The public launcher derives its
package from its own location and accepts selected runtime roots and PROFILE.
The preparer requires the sibling `ordinary_network_kit/prepare.py`, already an
included source dependency. Historical example paths in guides are labelled
examples; they are not runtime path requirements. The fixed supported Windows
Python/Lean runtime bytes remain required, not a claim of generic platform support.

## Narrow existing convenience limitation, not a build blocker

`ordinary_network_kit/prepare.py:210-217` requires all convenience input reports
to match the selected local PROFILE. `producer` at 434-450 uses that method.
Consequently, `intake-baseline`/`publish` preparation using a producer report from
a *different* independently built PROFILE is refused, even when the portable
bundle has matching mathematical semantics. Changing `prepare_selected`'s local
PROFILE does not make foreign producer reports local.

This does not prevent installation, local producer/intake/publication, or the
ordinary network receive path (whose find/parent reports are receiver-local).
The underlying owner `intake-baseline` accepts an explicitly selected bundle and
manifest without requiring a producer report; the existing operator guide says
the producer-report route is optional. Do not promise cross-build producer-report
interchangeability or edit old reports to evade this check. It is not a reason
to expand the current installation repair into a new mechanism or experiment.

## Minimum consequence

Select a fresh transport assembler that preserves source/layout/actual-byte
checks while accepting the operator's actual compatible base PROFILE, receipt
and installation identity. The other agent owns that remedy invariant. Keep the
existing frozen assembler and evidence untouched. A later source handoff must
include that selected successor and the existing sibling helper; the earlier
136-payload ZIP explicitly does not contain the transport repair. No full native
rebuild, new compiler, new registry or unrelated audit campaign is justified by
this source finding alone. Actual source-build success remains separate evidence.
