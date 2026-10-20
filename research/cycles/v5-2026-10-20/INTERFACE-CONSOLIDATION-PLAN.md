# Consolidate tested interfaces into one installable candidate

Source-only bounded payoff decision, 2026-10-20; owner `core_search`.
No implementation, build, runtime invocation, binary copying, experiment or
Git mutation was performed. This plan is conditional on the genuine interface
integration passing its independent saved-outcome audit.

## Minimal delta, using the existing system

The current builder is
`software/v5/distribution_connected/distribution.py`, 46,634 bytes,
SHA `8e34df2a98fc3bf017f3d57ea2f92211bbcf156ee801479cbfaf9261f76763a6`.
Its current exact input is
`experiments/v5-local-checks/distribution-connected-01-input.json`,
SHA `557269158f76933177eae962cb97c2862a8512709dbee9842051649552573309`.
The installed baseline manifest is
`product-local/v5-distribution-connected-01/Mathematical Commons v5/V5-RELEASE.json`,
SHA `69d9456eb53135061bc68a8d657ae0f25bc71013cd9c8d2cd5f571c4c7996ef5`.

Make one fresh successor input from this current input, not an older generic
software-tree census. Exactly six existing SDK mappings change and two are
added:

| Logical SDK path | Fresh selected source |
|---|---|
| `v5/mixed_claims/imports_atomic.py` | `software/v5/interface_views/imports_atomic.py` |
| `v5/mixed_claims/authoring_atomic.py` | `software/v5/interface_views/authoring_atomic.py` |
| `v5/client/workspace_evidence.py` | `software/v5/interface_views/workspace_evidence.py` |
| `v5/client/workspace_staged.py` | `software/v5/interface_views/workspace_staged.py` |
| `v5/client/semantic_reader.py` | `software/v5/interface_views/semantic_reader.py` |
| `v5/transport/semantic_staging.py` | `software/v5/interface_views/semantic_staging.py` |
| **Added** `v5/mixed_claims/interface_projection.py` | `software/v5/interface_views/projection.py` |
| **Added** `v5/transport/declaration_resilience.py` | `software/v5/transport/declaration_resilience.py` |

The evidence-client and reader overlays already contain the tested
`supplier_complete` declaration continuation. Do not install an additional
parallel supplier implementation or overwrite them with the older installed
`supplier_resilient` files. The required outcome is one logical source graph.

SDK rows increase **106 to 108**; v5 Python/preparation-source rows increase
**85 to 87**. All 21 portable location rows stay byte-identical. Keep the
existing runtime-efficient receipt verifier, mixed receiver and
`admission.pin_phase` mappings unchanged. No typed-row guest, new guest image,
geometry host, certificate, index, networking mechanism or optional cache is
included. Test adapters and tests are not distribution SDK files.

The six binary asset roles, complete Lean support graph, Python/Node/base
projection, foundation, checking policy, I/A image identities and retained
preparation-template roles remain unchanged. No compiler or proof operation is
part of consolidation.

## Small builder successor: documentation plus required helper names

The used connected builder stays frozen. A fresh successor needs only:

1. The embedded README/API changes described below.
2. Add `v5/mixed_claims/interface_projection.py` and
   `v5/transport/declaration_resilience.py` to `required_sources(role)`, so a
   missing newly mandatory helper is rejected during build/manifest validation,
   before an installed owner fails to start.

No packaging framework, new schema or filename allowlist expansion is needed.
Both helpers are ordinary `.py` SDK files accepted by `_build` and
`validate_manifest`. The SDK ceiling is 141, RuntimeProfile's Python-source
ceiling is 120 and the profile-list ceiling is 128; the selected 108/87 map
fits all three. The builder's relative `preparation.source_pins` is generated
from **all** v5 Python rows, so the new projection pin required by
`MixedOwnerPreparation` is supplied automatically. `RuntimeProfile.from_context`
then uses the ordinary checked launch snapshot; it needs no mutation.

The input/release schemas can remain `DMKN_V5_DISTRIBUTION_INPUT_V3` and
`DMKN_V5_DIRECTORY_RELEASE_V3`: the changed source map and release hash identify
the new candidate, and no protocol/configuration shape changes. Preserve the
current `mathematical-client-location-v1` role, public wrappers and launch
command names. A new destination must be a fresh canonical sibling; do not
migrate old workspace state or modify the existing installation.

The expected payload-map delta is eight replacements (six SDK files, builder,
generated README) and two additions. No deletion, binary/support change or
unexplained payload may be accepted. The manifest's build-input identity,
source maps and corresponding relative preparation pins necessarily change.

## Documentation that must ship

The generated installed README is currently the public SDK guide. The builder
does not accept arbitrary `.md` files in `sdk_sources`; do not add a new docs
packaging mechanism merely to copy `interface_views/README.md`. Incorporate a
short accurate subset into the existing embedded README:

- Document `SemanticReader(..., definition_mode="interface-only")`, direct
  `client.import_context(..., definition_mode="interface-only")` and direct
  `client.preview_context(..., definition_mode="interface-only")`.
- Omission means `eager`. The reader/live import's selected mode is fixed and
  inherited by continuation; there is no retry, silent downgrade or renewed
  grant. Interface-only is selected explicitly by trusted local owner policy.
- Only missing ordinary-definition bodies may be deferred. Types, present
  bodies, inductive groups and recursor rules keep their obligations.
- The frontend view is an untrusted rigid-constant proposal environment. The
  final native witness uses original definition descriptors/hash/hints. A
  frontend or native missing-body failure is not acceptance and does not
  authorize automatic fallback. New local axioms remain forbidden.
- Extend the existing supplier example with `helper.try_resolve(...)` and the
  corresponding direct `client.try_resolve_declaration(...)`: an explicit
  second authorized supplier is permitted only after the typed settled
  `UNAVAILABLE_AT_SELECTED_SUPPLIER` result. Malformed successful data,
  unauthorized contacts, exhausted allowance and uncertain cleanup remain
  fatal. Existing fail-stop `resolve` is still available.
- Distinguish three-context/two-rule-body evidence from total network savings:
  the retained input packet still contains its earlier native-tail bodies.
  Neither this candidate nor its example creates a new succinct certificate.
- Preserve the existing trusted-owner/not-hostile-source-sandbox, license,
  no-final-v5 and deployment limits. Documentation must not promote a package
  checksum or a focused positive test to a global-readiness claim.

The context's existing `frontend_packet_bytes` reports the original selected
packet, not necessarily exact post-projection request bytes. Use actual saved
request byte counts for any transfer-size claim, rather than relabeling that
inert accounting field.

## Smallest genuinely changed installation check

After a successful actual source integration, build once through the existing
bounded file-only build path. Compare the complete candidate manifest map
against the baseline, explaining exactly the ten payload changes above. Also
compare every candidate SDK hash against the successful actual integration's
source map; unchanged mathematical binary pins must match too.

The builder already calls `verify_release(..., full=True)` after copying and
writing its manifest, and returns only after full readback/census. Do **not**
automatically schedule another full `verify` readback, the old location/HTTP
campaigns, or the same mathematical contribution merely to repeat old evidence.
The previous file-only build cost 32.59375 known CPU seconds and
177.6106053 wall seconds for 842,219,712 payload bytes; these are historical
planning data, not guaranteed successor timings. Retain an explicit finite
build envelope rather than investigating RAM again.

The genuinely new public boundary is the installed distribution's own source
map and generated preparation profile. Test it with **one ordinary public
`distribution.py launch RELEASE_SHA run REQUEST REQUEST_SHA`** that:

1. Uses the installed runtime/foundation placeholders and the new release hash.
2. Opens a fresh validated Workspace and exactly one real RuntimeProfile
   operation with authoring enabled, without submitting source or mathematics.
3. Explicitly imports the optional SemanticReader and checks exact snapshot
   origins/hashes of the seven interface modules and declaration helper; checks
   that the live preparation/client owner maps include the projection helper.
4. Closes the client/owners and workspace, recording zero native, receipt,
   proof, authoring and network calls, no new admission/publication and clean
   ordinary operation closure.

This is not a fake mathematical test or substitute for the genuine interface
integration. It specifically tests the new installed map, import graph, helper
pin obligations and public placeholder/profile relocation. The already
passing mathematical run plus exact SDK/binary identity supplies the separate
mathematical evidence. Report the scopes separately; the public smoke itself
does not establish theorem admission. If source-map equality fails or a code
change affects mathematics, this reduced follow-up is insufficient and root
must select the corresponding changed-boundary test instead.

No new runtime factory, discovery fixture, fake issuer or subclass-identity
bypass is needed. An inexpensive missing-helper manifest rejection can be
covered in the existing builder's pure contract style if its two-line
`required_sources` change is selected; no broad test-suite rerun is required.

## Stop conditions

No build before independent adoption of the genuine interface integration and
review of final builder/docs/source map. Preserve failures without automatically
creating successor variants. A byte-verified candidate and one public source-
origin/profile check consolidate the tested software; they do not close cold
certification affordability, independent hostile-input assurance, global
discovery/availability, licensing or the unchanged full v5 goal.
