# Future role-projected distributions

2026-10-20, core_search. Read-only source/manifest decision requested by root.
No product edits, copying, execution, testing or optimization selection.
Build02 has since passed its original envelope; proceed with installed reader
and contributor checks. This note must not displace them.

## Decision

A distinct lightweight mathematical-client support role is source-compatible
with the current v5 runtime owners. It need not carry the old v4 Node overlay.
However, **the current distribution builder/verifier requires the full nested
base**, so deleting optional files from the completed installation is forbidden.
A future role-projected release needs an explicit new packaging contract,
not a claim that a partial directory is the exact complete v4 installation.

## Exact required base projection

Keep the unchanged `RELEASE-MANIFEST.json`, whose SHA256 is
`a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`,
and select these entries from its existing `files` map:

| Base role | Exact selection | Files | Bytes |
|---|---|---:|---:|
| Python runtime | Every name beginning `receiver/runtime/python/` | 584 | 30,459,330 |
| Supervisor | `operator/commons.py` | 1 | 41,984 |
| Domain helper | `receiver/helpers/domains.py` | 1 | 4,934 |
| Job helper | `receiver/helpers/run_stage.py` | 1 | 30,037 |
| Fixed source manifest | `RELEASE-MANIFEST.json` itself | 1 | 1,070,384 |

Total: 588 actual files, 31,606,669 bytes including the manifest, versus
6,653 files/236,732,832 bytes for the complete nested base including its manifest.
This removes 6,065 payload files/205,126,163 bytes from the *base role only*.
The v5 SDK, native/I/A executables, guest image, foundation, authoring frontend
and six Lean runtime files remain separately selected; they are not eliminated.
Thus a minimal base is not a claim that the whole contributor fits in 32 MB.

The three helper hashes remain exact original manifest rows:

- commons: `6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9`
- domains: `651db5f6bb707159c0d29dd6092174bfcebd1dc17b833fdfdacf7e2a66d8522a`
- run_stage: `bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028`

## Why the unchanged mathematical path permits it

`client/launch.py` loads the fixed manifest and those three helper modules.
`client/boot.py:95-111` explicitly enumerates and hashes **all 584 Python
runtime files**, then the helpers. It does not census the entire base. Therefore
do not further prune the Python subtree merely because an observed run did
not import a particular standard-library module.

`RuntimeProfile.from_context` checks selected producer runtime roles against
the manifest, not full-base presence. Its current producer Python/DLL/runtime
pins are all inside the required Python subtree. `ReceiptVerifier`,
`AggregateReceiptVerifier` and `Producer` load/check the same three helpers and
their selected runtime pins. Mixed/native and authoring owners add their own
external exact pins. Their filesystem censuses concern operation output, not
all historical v4 files.

The supervisor module is imported as a helper; its v4 `Release` class/public
CLI is not invoked by these paths. That old CLI requires additional profiles
and action-specific roles and must not be advertised as supported by this
projection. `child_environment` names receiver/bin on PATH but does not check
or populate it; the v5 path supplies actual external executables explicitly.
OS loader/PATH assumptions remain, not a new hermetic-runtime theorem.

## Optional location role and future packaging obligation

Portable `location/controller.py:93-120` separately selects **all 5,896**
`overlay/` or `runtime/node/` entries, totals 130,118,221 bytes, and requires
their exact subtree census and hashes. Its `AdoptedLocationRuntime` already
takes its own explicit installation root. Direct-contact discovery and the
current reader/service do not construct this Node process.
Consequently Node/location support is a credible separately adopted role;
do not prune its transitive npm files without a new corresponding contract.

A future outer release must label its base as a named projection, bind the
exact selected set to the unchanged full manifest, verify all selected bytes
and the actual projection census, and declare excluded v4 actions unavailable.
It must replace `DIST_EXACT_NESTED_BASE_MAP` with a precise role equality—not
simply remove that check. Retaining a full manifest is a source-pin catalogue,
not a false claim that every listed payload is installed.

No selected runtime owner appears to require a full-base census on the
ordinary mathematical path. This is a source compatibility finding, not an
executed lightweight-installation qualification. Defer implementation now
that the selected full distribution works.
