# Proposal: owner-selected offers at initial configuration

Status: source-only proposal, 2026-09-21. No product code was changed, imported,
run, or tested to prepare it. This proposal is deferred from the current useful
reuse experiment; that experiment can continue through the existing producer
route. No consumer target or proof source was inspected.

## Smallest useful change

Add repeatable `manage.py configure --offer PATH`, with zero through eight
selections, to populate the existing schema-3 `offers` list. `PATH` denotes a
portable canonical package directory containing `manifest.json` and its object
files. It is not a source file, bundle archive, node state directory, or proof
acceptance receipt. Relative CLI paths may resolve against the invocation's
working directory; the saved configuration contains resolved absolute paths.

Keep the existing `Domains.require_package` policy. For a fresh configuration,
state and scratch do not exist, so usable preexisting package directories are
under the selected installation's `assets` tree. The owner can place retained
portable packages in `INSTALL/assets/offers/<chosen-name>` while preparing the
new installation. The command itself does not copy into or modify installation
assets. Outside-domain source paths are refused in this first extension.

This narrow interface addresses reuse from an owner-prepared installation
without extending checker reads to arbitrary archives or adding a second
canonical package loader. It deliberately leaves direct external archive
ingestion for a separately reviewed owner-copy change.

## Existing behavior that supports this design

- `software/manage.py:43` requires fresh state and scratch. At line 100 it
  hardcodes `offers: []`; lines 106-114 validate domains, check physical supply,
  create the two roots, write the configuration, and load it.
- `software/py/node.py:66` already allows an `offers` list of length 0..8.
  `load_config` does not authenticate each offer's contents or shape.
- `software/py/node.py:208` starts initialization by bootstrapping the common
  packages, then calls `Checker.offer` separately for every configured offer.
  The commit path at lines 247-263 creates client contexts only from the common
  bootstrap result and appends offered metadata to P1.
- `software/py/checking.py:209` validates the existing package-pin shape
  `{path, manifest_sha256}`. `package` checks the manifest digest, reads canonical
  bytes, and enforces the existing package/cache bounds. `import_package` at
  line 233 exports the selected closure into request work, rereads it, and
  checks the copied root and closure.
- `Checker.offer` at `software/py/checking.py:479` imports the package and derives
  formal metadata. It does not request native replay. `Checker.admit` at line
  487 performs the later context union and native description check.
- `software/py/domains.py:104` permits canonical package directories beneath
  installation assets, state, or scratch. Runtime directories and other local
  paths are not package domains. `require_write` permits request work and
  scratch, so the setup command should not invent checker write authority to
  installation assets.
- `software/build.py:63` authenticates enumerated asset-lock entries; it does
  not require that every file in `assets` appear in that lock. Supplemental
  owner-prepared packages therefore need their own saved manifest pins and the
  existing initialization authentication. They do not become locked common
  assets or accepted mathematics by being placed there.

## Proposed implementation, before coding

Only `software/manage.py` needs behavior changes:

1. Register `--offer` using `action="append", type=Path`. Update the configure
   help from "new empty-offer node" to describe optional inert offers.
2. Early in `configure`, read `getattr(args, "offer", None) or []` and require
   at most eight entries with the existing `CONFIG_OFFERS` refusal code. Do
   this before creating state or scratch. Preserve CLI order and existing
   duplicate behavior; do not add an implicit selection or deduplication rule.
3. Replace the unused domain-validation expression at line 106 with a local
   `domains = Domains.from_config(config)`. For each selection, resolve it and
   apply `domains.require_package` before reading its manifest. Resolve the
   manifest through `domains.require_read`; require a regular file whose
   resolved path remains beneath the selected package directory. This small
   check prevents the new setup pin operation from following a manifest link
   outside its selected package. Reuse the existing bounded `pin` function.
4. Populate each entry as exactly
   `{"path": str(package), "manifest_sha256": pin(manifest)["sha256"]}`.
   Finish all selection/pin checks before the current physical-supply check
   and directory creation. Save and reload the configuration as today.

Do not change the configuration version, acceptance paths, `load_config`,
`Domains`, common packages, provider schema, quotas, or checker behavior.
The existing `CONFIGURED_NOT_INITIALIZED` result and `acceptance: false` remain
accurate; no extra return fields are necessary.

Add a short CLI example and boundary explanation to the operator quickstart
and API documentation. State that configuration pins manifest bytes only.
Canonical objects and candidate metadata are authenticated by ordinary `init`;
`find`/`preview` expose candidates, and `admit` still performs fresh receiving
acceptance. `init` returning `accepted: true` describes its common bootstrap
context, not mathematical acceptance of every configured offer.

## Limits and failure behavior

Offer count does not expand the working-context package limit. Existing
selected package, aggregate cache, request-work, time, and metadata bounds
continue to apply during initialization and later admission. Eight offers is
a selection ceiling, not a promise that every eight-package collection fits.

If object bytes are missing or malformed, or the manifest changes after
configuration, initialization refuses using its existing checks. Bootstrap
runs before offers are authenticated, so such a refusal may consume its native
stage; this proposal does not claim a free preflight or reorder initialization.
No partial configuration or failed initialization is silently removed or retried.
After successful initialization, the provider's candidate uses the imported
request-work package, so subsequent use need not rely on the original source
directory. This is existing custody behavior, not a backup guarantee.

## Smallest proposed verification set

The root operator alone executes qualification. Use existing valid canonical
package fixtures, without inventing new mathematics for this CLI feature.

| Check | Evidence needed |
| --- | --- |
| Configuration contract, parametrized | Zero offers preserves the current configuration; one and eight selections save exact absolute paths and manifest hashes in order; nine refuses before state/scratch creation. |
| Path and pin contract, parametrized | An in-assets package is selectable; external, runtime, nonexistent, non-directory, missing-manifest, oversized-manifest, and escaping-manifest-link selections refuse before state creation. Exercise the link case only with an actual supported Windows fixture, or report it untested. |
| Existing inert authentication boundary | A valid configured package passes `Checker.offer` without a native allocation; changed manifest or object bytes are refused. Exercise the real canonical reader with a bounded fixture, not a mocked successful checker. |
| One fresh native end-to-end run | Configure one retained offer, initialize, and find it. Verify the initial context contains only common declarations and the offer is candidate-only. Admit that candidate and verify fresh native evidence plus the resulting receiving description. Verify initialization retained a state/work copy and no native stage was allocated for offer registration. |

No broad new regression suite is proposed. A failure that exposes a broader
boundary problem should be reported and scoped before widening this change.

## External-path copy follow-up

If direct `--offer E:/archives/package` is subsequently required, add a bounded
owner setup copy into the newly selected scratch or state/work domain, then
retain the same `{path, manifest_sha256}` entries and ordinary `init` path.
That follow-up must first specify total bytes/file count, exact manifest-listed
closure copying, file/link validation, source-change detection, unique target
creation, partial-copy retention, and manifest pin binding. A generic recursive
directory copy or a new unrestricted `Domains.require_package` exception would
expand this proposal substantially. No such copy implementation is included.
