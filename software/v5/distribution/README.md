# Relocatable Windows directory distribution

`distribution.py` is a small release builder and public entry. It does not
replace the existing verifier, runtime factory, launcher, Windows Job supervisor
or mathematical acceptance policy. Source-only implementation is not a release
qualification. Licensing, independent deployment/security and final-v5
obligations remain separate.

## Build an explicitly adopted release

```text
python -I -S -B distribution.py build INPUT.json INPUT_SHA256 FRESH_ABSOLUTE_DIRECTORY
```

Run the file-copy operation under the owner's separately selected resource
limits. It does not enforce a new installation Job or start any mathematical
worker. The input has exactly:

```text
schema: DMKN_V5_DISTRIBUTION_INPUT_V1
base_root: absolute immutable support-installation directory
base_manifest: {path, bytes, sha256}
sdk_sources: "v5/..." or "portable/..." -> {path, bytes, sha256}
preparation_template: {path, bytes, sha256}
assets: native, receipt, aggregate, image, frontend, foundation -> pins
aggregate_image: exact locally adopted aggregate image ID
lean_runtime: path relative to original Lean root -> pin
distribution_source: pin of this exact distribution.py
```

The owner adopts the input digest and role selection before invocation. The
builder does not discover binaries and bless their freshly computed hashes.
It preserves the exact nested support manifest, validates the preparation
template's foundation/policy/roles, confines destination names, streams each
selected file, checks copied bytes and performs a full output-map verification.
It never overwrites or deletes a directory. Failure leaves partial output for
inspection, not an installation to use or automatically retry.

The emitted layout is:

```text
INSTALL/
  distribution.py
  V5-RELEASE.json                 relative files, SDK sources and runtime roles
  README.md                      installed public-command instructions
  base/                          exact unchanged support distribution
  sdk/v5/                        selected product sources, no fixture owner
  sdk/portable/location/         unchanged selected portable closure
  assets/{native,receipt,aggregate,image,frontend,foundation}/
  assets/lean/                   selected Lean files, original relative layout
  owners/{reader,serve}.py        trivial release-owned entry wrappers
```

The release digest is printed after exact verification. No archive, publication,
remote fetch, license choice, build or proof-production call occurs.

## Trust and relocation

Before executing, independently trust/verify the bootstrap interpreter and
`distribution.py` itself, then adopt `V5-RELEASE.json`'s digest. A compromised
program can lie about its own hash; self-checking is not publisher authentication.
There is no signing policy silently invented here.

All operative runtime paths in the release manifest are relative. Each launch
materializes a fresh absolute preparation profile outside the installation
using only its release-pinned roles, including the host, guest image, AuthorLean
frontend, Lean root/files, native checker and I/A verification executables.
Moving the directory therefore does not require editing immutable installed
profiles. User workspaces, requests and TLS secrets stay outside the installation.
Historical prose inside the exact nested base is preserved, not runtime authority.

Full verification streams all payloads. Launch validates the complete bounded
manifest and exact filesystem census, hashes the selected SDK/assets, and keeps
the existing base/helper/Python checks in `client.launch` / `boot`. It does not
rehash unused nested-base payloads on every operation. Dynamic OS dependencies
and the retained worker's OS-loader/PATH assumptions are not replaced by a
hostile-code sandbox.

## Installed public commands

From any working directory, use absolute paths:

```text
INSTALL/base/receiver/runtime/python/python.exe -I -S -B INSTALL/distribution.py verify RELEASE_SHA
INSTALL/base/receiver/runtime/python/python.exe -I -S -B INSTALL/distribution.py launch RELEASE_SHA reader REQUEST.json REQUEST_SHA
INSTALL/base/receiver/runtime/python/python.exe -I -S -B INSTALL/distribution.py launch RELEASE_SHA serve REQUEST.json REQUEST_SHA
INSTALL/base/receiver/runtime/python/python.exe -I -S -B INSTALL/distribution.py launch RELEASE_SHA run REQUEST.json REQUEST_SHA
```

Each request has schema `DMKN_V5_INSTALLED_REQUEST_V1`, `name`,
`workspace_root`, `parameters`, `limits`, `output_limits`, `owner`, and
`runtime_mode`. Use an existing allocation directory disjoint from installation,
a fresh lowercase run name, and explicitly finite existing Job/output limits.
The source of truth for their exact schemas remains the installed
`sdk/v5/client/launch.py`; no research path is required.

| Command | Owner | Runtime mode | Parameters |
|---|---|---|---|
| `reader` | `null` | `aggregate` | Ordinary remote-reader fields, omitting injected runtime_adoption/foundation |
| `serve` | `null` | `null` | Ordinary finite serving fields |
| `run` | Explicit trusted local source map | `atomic` or `aggregate` | Local strategy's own parameter schema |

`reader` uses the **validated** workspace, not the historical atomic/I-only
default. Its runtime includes the selected A verifier, even when the actually
acquired packet needs only I/native verification. No missing A evidence is
silently replaced with I. Source/config choices do not establish an A certificate.

The public reader accepts `workspace_path`, `workspace_config`,
`create_workspace`, `operation_limits`, and `query`; it sets its entry schema
and installed runtime/foundation. The exact query field layout is in installed
`sdk/v5/client/remote_reader.py`. Its simple policy uses one selected provider,
one nonempty-partition ordinal/page start, one returned candidate ordinal and
one offered packet ordinal. A local agent may instead use the callable SDK to
choose its own strategy. Completed `MISS`, `REFUSED`, or `NEED_SEMANTICS` is not
mathematical `READY`; inspect the saved outcome, not only exit zero.

For `serve`, pass `mode`, `workspace_path`, exact `workspace_config`, `bind`,
`tls`, and `service_limits`. The entry adds its schema if absent. It opens an
existing workspace exclusively, serves only the unchanged read-only remote
routes, writes readiness while live and closes at its finite deadline.
Remote read-only does not mean its backing SQLite metadata is immutable.

## Explicit trusted-owner programs

`run`'s `owner` has exactly `root`, `entry` and `sources`. The root is an
absolute ordinary directory; entry is a selected relative `.py` path; sources
maps each selected relative Python file to `{bytes,sha256}`. The program defines
`main(context)` and returns zero explicitly. This is locally adopted executable
code, **never** downloaded proof data or arbitrary peer-provided code.

Use exact singleton markers anywhere in this program's own parameters:

```json
{
  "reader": {
    "runtime_adoption": {"$installed": "runtime_adoption"},
    "foundation": {"$installed": "foundation"}
  }
}
```

Only those two installed roles are supported. No unrelated top-level keys are
injected into custom parameters. A trusted strategy may use
`context.parameters["reader"]["runtime_adoption"]["aggregate"]["image"]` to
construct the exact current `evidence_network.custody.public_profile(image)`;
it chooses its own storage quotas, mathematical inputs and research strategy.
No experiment ID, local source-map reconstruction or repository path is needed.

The launcher creates fresh `NAME-request/request.json`, `preparation.json`
(except service-only work), and `launch.json`; `client.launch` creates the
separate `NAME` run. Keep mathematical state a disjoint sibling. Preparation
and input validation are trusted prelaunch work, outside the child Job. Their
time and CPU remain included in the original wrapper clocks supplied unchanged
to the existing launcher; they do not obtain a fresh operation allowance.
This wrapper imposes small prelaunch refusal limits, not hard prelaunch isolation.

No automatic retry, migration, daemonization, referral dialing, publication or
proof-budget renewal is introduced. Saved records remain operational evidence;
live warrants still come only from the unchanged mathematical owners.
