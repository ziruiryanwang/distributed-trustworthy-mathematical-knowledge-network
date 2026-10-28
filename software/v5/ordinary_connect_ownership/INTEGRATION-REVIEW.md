# Owned-connect integration review

2026-10-28, operable_scale_decision. **PASS, source-only integration scope.**
This independently reviews root's map, build recipe and file assembler. It does
not review my fair_exchange implementation; growth_design_audit owns that
independent source review. Guard passed. No product import, controls, build,
runtime, network, owner/native operation or Git action occurred.

| Input | SHA256 |
| --- | --- |
| source-map.json | `80d46cbedad723a90a87db80c4b5ac1dd6054526911c643c425ede48ce00f713` |
| build.py | `55794245fec2b6a65f0283440e951b99aa7348fcafb9002f766991c23392e474` |
| assemble.py | `dbb4fded57d169770917847354af9c2ff1a3a42ebddf5f6d8586139296575940` |
| Prior registration-refresh map | `aeab07b21fb755614ea1432ca9b748d2f8abbfe8c6f43f262de9d2da66cbdb85` |
| Prior registration-refresh assembler | `b2efbf164d67bcacf17dfd1c0ec3c26372874f874eb87d082e56e63e5c2a8ca2` |

## Map and direct recipe

Structured comparison against the independently reviewed registration-refresh
map finds the same **93 source inputs and 78 copy roles**. The only changed
copy value is `support/transport/fair_exchange.py`, replacing
`ordinary_sparse_access/fair_exchange.py` with
`ordinary_connect_ownership/fair_exchange.py`. Exactly that old source path is
removed and the new path added. All **92 common source pins are unchanged**.
Every selected source's current length and SHA256 matches its map pin.
The new selected source is 8,250 bytes, SHA256
`05cf2b5baef0130dbe3b43e594d6c800baf6b625c77125dd3356f59f78509575`.

Every other top-level field is structurally identical: schema, counts, profile,
documentation, authoring suffixes, tools, all native outputs/runtime pins, and
receiver/authoring/extractor/query lanes with their transforms and digests.
All 19 installation direct-copy roles and pins are unchanged. No new module
role, native input or owner-state migration is selected.

Complete build.py text equality holds after only the intended PREFIX and MAP_SHA
substitutions in the reviewed registration-refresh recipe. Counts, source-closure
checks, compiler stages, staging and final assembly behavior are unchanged.
This is source consistency, not a fresh-build or binary reproducibility result.

## File-only assembler

The assembler retains exact adopted directory-kit manifest/receipt, PROFILE
`7687d527...`, installation `9112bc5d...`, and baseline name-directory map
`46709b30...` bindings. Its helper remains the exact file-only assembler
`9acc1b243baf302ce2c350b4079b213673c651a8605d4b322c9907b52a3bbe30`;
the hash matches the retained source. No product or native code is imported by
this assembly lane. The separate direct build recipe is not invoked here.

Against the adopted kit, the five map replacements are exactly peer.py, run.py,
peer_api.py, support/transport/http_provider.py and
support/transport/fair_exchange.py. The first four still select the already
reviewed registration-refresh files at their unchanged pins. The fifth selects
the new fair_exchange pin above. Equality against the baseline map after those
five substitutions excludes unrelated map changes; each supplied source is
bounded, authenticated and required to differ from its baseline payload.

PROFILE.json changes only those five file pins. The existing 122-file auxiliary
set and all profile/installation identity fields remain unchanged. Exactly five
payloads plus PROFILE.json change, leaving **154 unchanged files out of 160**,
with no added payloads. Native/installation files remain among the unchanged
files. Existing fresh-output, path-separation, census, copy-readback and final
input/source checks remain intact. Report fields retain ASSEMBLED_NOT_ADOPTED,
zero native calls and the file-assembly-only claim.

Full assembler text equality against its reviewed predecessor holds after only
the declared four-to-five description, successor prefix, explicit five-role
mapping, diagnostic/module label and 155-to-154 unchanged-count substitutions.
No additional control flow changed.

No integration blocker was found. Actual assembly identity, selected runtime
controls and public behavior remain separate evidence. Later changes to these
reviewed bytes or selected source pins need a corresponding review update.
