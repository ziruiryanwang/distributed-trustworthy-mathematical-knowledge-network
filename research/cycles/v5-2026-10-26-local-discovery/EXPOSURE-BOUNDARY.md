# Finite serving and investigator disclosure boundary

2026-10-26. Source-only audit; no product import, native execution, network,
state modification or new experiment. Scope is the default package selected by
`software/v5/ordinary_release_bundle/ADOPTION.md`, PROFILE
`b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7`.
Below, `P/` denotes
`experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package/`.

## Decision

No unintended publication-ACL bypass or remote source-execution path was found
in the inspected ordinary serving path. Whole-custody disclosure is an explicit,
documented operator choice, not a hidden implementation deviation. Do not add an
ACL subsystem or rerun transport tests to repair this intentional contract.

The practical rule is stronger than “publish only my chosen theorem”: **never
serve an investigation custody unless every retained object's disclosure is
acceptable**. A discovery index selects advertisements, not permitted reads.
Separate private investigation and shareable owner/custody/index state already
suffices for that boundary, under the existing protected-filesystem premise.
It does not provide recipient confidentiality or hostile-code isolation.

## Exact source argument

- `software/v5/ordinary_network_kit/START-HERE.md:157` discloses the entire
  addressable scope. Its `prepare.py:623` requires both approval booleans true.
  `P/peer.py:205` and `P/peer_api.py:826` independently enforce them.
- `P/peer_api.py:738` checks selected target bindings and publishes their
  previews to the index. `P/peer_api.py:804` expressly disclaims per-object ACLs;
  line 866 passes the whole selected custody to the provider, not target rows.
- `P/support/transport/http_provider.py:393` dispatches ordinary routes directly
  to custody. `P/support/transport/ordinary_acquisition.py:287` maps exact
  requests to preview, locator or evidence reads. It does not consult the index.
  `:166` creates locators for every output of each retained evidence unit,
  including outputs not selected for publication.
- `P/support/transport/ordinary_acquisition.py:255` and `:260` use semantic IDs,
  content/export IDs and parameterized SQLite queries. The exact request schemas
  at `:41` accept no filename, arbitrary URI, source text or execution command.
  `P/support/transport/http_provider.py:459` refuses the separate module-storage
  role because ordinary `serve` does not supply that role. Within this path no
  arbitrary filesystem read or source loader was found. This is not a general
  proof of parser/runtime exploit absence.
- Retention is not acceptance: `P/peer_api.py:622` attaches local custody to
  acquisition; `P/support/transport/ordinary_acquisition.py:487` retains evidence
  after structural/identity validation, before `P/peer_api.py:693` calls admit.
  Thus incomplete/refused receive attempts can leave addressable inert material.
  A public store must be treated as disclosure-approved storage, not merely a
  collection of successfully published or mathematically accepted results.
- `software/v5/ordinary_bounded_transport/http_provider.py:73` configures server
  TLS but no client-certificate requirement. HTTP request dispatch contains no
  requester authentication. TLS protects/authenticates the connection according
  to client policy; it does not limit readers to chosen collaborators. Knowledge
  of a content hash is neither consent nor a secret-access capability.

## Realistic existing workflow

For approved ordinary Lean project work, keep the exploratory owner/custody
private. Select completed output names for `owner produce-baseline`; inspect the
inert resulting bundle's entire declaration/dependency content for disclosure.
Initialize a distinct shareable owner/custody, perform strict `intake-baseline`
there, publish selected targets, and finite-serve **that** store and index only.
Do not copy an entire private catalog/database or merely create a fresh index
over the same private custody. Reuse the approved package; no second native build
is required. This costs ordinary export/intake work, not a privacy-specific proof.

This route is already documented in
`software/v5/ordinary_operator_kit/START-HERE.md:181` and `:229`; the final source
handoff specifies which selector/package supersede that guide's historical pins.
`P/owner.py:524` independently intakes the exact inert bundle. Production binds
the selected writer at `P/authoring/py/baseline_production.py:270` and writes only
its manifest units at `:272`. Selection is dependency-closed, not exact-name-only:
`software/v5/ordinary_lean/OrdinaryExport.lean:136` schedules target owner groups
and their dependencies. Group siblings, proof dependencies and definitions may
be required disclosures. Do not claim that inspecting target names suffices.

For direct no-project contributions, the simplest preventive workflow is to use
a separate disclosure-approved state from the outset. There is no demonstrated
one-command inert selective export of an arbitrary existing mixed custody in
this audit; `owner export-module` is a local compiled realization, not that
privacy export. Do not suggest serving the mixed store briefly on loopback as a
confidential migration: other local users may connect. Existing retained approved
bundles can be intaken into fresh state; otherwise identify the actual selected
material and required closure before proposing a new export helper.

## Minimal justified correction

If root selects a fresh revision of the reuse companion, add one short warning before
its publish/serve transition: publication is advertisement, not read permission;
serve only a disclosure-approved custody; use separate state while investigating
private material. Link the existing explicit whole-custody contract. A fresh
package, new privacy mechanism or experiment is not justified by this audit.
Private collaborator-only access would require separately selected network access
control; it is neither currently implemented nor authorized for deployment here.
