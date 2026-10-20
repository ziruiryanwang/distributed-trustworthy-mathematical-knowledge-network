# Interface distribution source checkpoint

Source-only implementation under [root's selection](INTERFACE-CONSOLIDATION-SELECTION.md).
No runtime, build, proof, native call, network request or Git mutation was performed
by this author. All predecessors and used interface implementation bytes remain
unchanged. Root owns exact integration selections and adoption.

## Exact sources for independent review

| Fresh source | SHA-256 |
|---|---|
| `software/v5/distribution_interfaces/distribution.py` | `ea3df90064ce7e759b311b95ba63d4486d7c8fd0b949de714fe37a85d77ea0bc` |
| `software/v5/distribution_interfaces/startup.py` | `3c7249be829dc269720e9ef35185e683bf41e426acdd6d2513506afd09cb74ef` |

Builder predecessor: `software/v5/distribution_connected/distribution.py`, SHA
`8e34df2a98fc3bf017f3d57ea2f92211bbcf156ee801479cbfaf9261f76763a6`.
The successor changes only the embedded usage README, the required presence of
`mixed_claims/interface_projection.py` and `transport/declaration_resilience.py`,
and a trailing newline. Manifest schemas, file checking, source selection,
runtime roles, packaging algorithm and launch behavior are unchanged.

The README documents explicit interface-only mode, the unchanged eager default,
fixed reader/live-import mode, eager structural/computation-rule obligations,
frontend-only opaque surrogates with original final semantics, and explicit
declaration-supplier continuation after settled unavailability. No automatic
fallback, new axiom, grant renewal, bandwidth or growth claim is introduced.

## Minimal installed startup boundary

The new trusted owner uses ordinary `RuntimeProfile.from_context`, validated
`Workspace.open`, reservation and `open_operation(..., authoring=True)`. It
constructs the real issuers and preparation owner, not substitutes. It compares
the eight selected SDK files against the caller's reviewed hashes, launch source
map, actual imported module origins, runtime description, real issuer source maps
and preparation source map. The projection must also be in the client guard.

The source check distinguishes the existing map types: issuer/client pins are
`Path -> {bytes,sha256}`; preparation pins are
`str(path) -> {path,bytes,sha256}`. It inspects but never mutates those maps.

Before and after closure, reports must show zero public client calls, zero
admission/author/publication/import-session counts, zero verifier attempts,
zero preparation calls/worker charge, no search/location/transport owner,
no failures and no publications. All real owners and the workspace close;
cleanup failure or deadline expiration makes the run fail. Cancellation and
evidence-write errors remain errors. The inert report has
`mathematical_acceptance=false` and `full_v5_release=false`.

Parameters use `DMKN_V5_DISTRIBUTION_INTERFACE_STARTUP_V1`; `expected_sources`
contains the eight relative-v5 paths without a `v5/` prefix, each mapped to its
reviewed lowercase SHA-256. Entry is `startup.py` / `main(context)`; output is
`interface-startup-result.json` under the launch location workspace.
Root's `Select-InterfaceStartup.ps1` matches this parameter/entry contract.

This is a packaging/profile/origin/lifetime gate only. Prior actual interface
integration and exact installed payload identity provide the distinct
mathematical evidence; this startup does not rerun it or create a new receipt.
Independent source review and any actual build/startup outcomes remain separate.
