# Mathematical commons: start here

Use this source distribution to investigate with ordinary Lean, find and check
other contributions, develop definitions and theories, and return selected work.
Alternatively, operate a storage-only mirror without running Lean. Local agents
choose what to investigate: no central server, mandatory research agenda, model
service or succinct certificate is required. Discovery never authorizes truth.

**This root README controls the current source handoff.** Its full manifest is
`COMMONS-SOURCE-MANIFEST.json`; its verifier is
`software/v5/ordinary_commons_bundle/bundle.py`. The older root `START-HERE.md`,
`HISTORICAL-INVESTIGATOR-README.md` and preserved guides describe earlier stages.
Use their unchanged mechanics with the explicit package/selector overrides below.
Do not patch a manifest or copy extra files into a hash-bound built package.

## Choose the simplest adequate role

| What you need | Route |
|---|---|
| Back up or transfer one already known complete mathematical bundle | Copy that exact inert bundle and its selected manifest; no service is needed. |
| Find, independently check, use and contribute mathematics | Investigator route below; approved Windows/Python/Lean and an actual local resource budget. |
| Keep selected mathematical bytes discoverable and retrievable for others | [Storage-only mirror](software/v5/ordinary_inert_mirror02/README.md); approved Windows/Python, not Lean or an owner. |

Installing software does not create peers, useful data, automatic replication or
an agent's research strategy. Select real contacts/data and finite work explicitly.
All current work remains **local and unpublished**;
[the license is undecided](software/v5/ordinary_release_bundle/LICENSE-STATUS.md).
No redistribution permission or final-v5 completion follows from this handoff.

## Approve and verify the source

The supported profile is **Windows x86-64, Python 3.14.6, Lean 4.34.0**. Lean is
needed only for mathematical investigator operations. Runtimes are external;
this distribution neither downloads nor bundles them. Other profiles have not
been adopted. Runtime pins identify selected files, not every transitive library.

Independently approve the utility, archive and terminal external `RECEIPT.json`.
Match the archive's exact byte length/SHA-256 before extraction into a fresh
protected directory. Select the current manifest hash from that approved receipt,
not an unrelated historical manifest or a digest treated as trustworthy merely
because it arrived beside untrusted code. Then run the approved isolated Python:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_commons_bundle\bundle.py' verify `
  --source-root 'C:\commons-source' `
  --manifest-sha256 'REPLACE_WITH_APPROVED_COMMONS_MANIFEST_SHA256'
```

Require exit zero and `VERIFIED_EXACT_COMMONS_SOURCE_NOT_BUILT`. Verification
checks the full path census, exact selected bytes and historical projection.
It executes only one pinned file-only helper after checking its bytes and paths;
it does not import a product, compile Lean, open state or validate mathematics.
The extraction must have exactly 187 files and their 47 parent directories.
Keep it protected and unchanged after verification.

Approve executable local source/projects, native packages and runtimes separately.
Read the [execution trust boundary](software/v5/ordinary_bounded_transport/EXECUTION-TRUST.md).
Windows Jobs limit resources, not filesystem/network privileges. Never execute
received Lean source, Python, native modules or `.olean` files automatically.
Hashes do not provide a hostile-source sandbox or authenticate an operator.

## Investigator: build, discover, check, extend, return

An existing Lean project is not required. Start with the fixed basis or actual
selected mathematical data, and follow these stages:

1. Follow the [build guide](software/v5/ordinary_investigator_bundle/guides/BUILD-MODULE.md)
   through the exact-module assembly. The route is native build, fair, contact,
   sparse, transport, then exact-module. Inspect each real terminal receipt and
   PROFILE before proceeding. Preserve failed outputs; no automatic retry.
2. For the current multi-source package, follow the
   [multi-source overlay guide](software/v5/ordinary_multi_source_package/README.md)
   using that immediate exact-module package and its actual receipt. This last
   stage is file-only: it preserves native checking/support and changes three
   transport files plus PROFILE. Select its new actual PROFILE digest, not a
   historical example digest.
3. Before initialization or later operations, replace the build guide's final
   package/profile variables with that multi-source result and use the current
   selector shown below. Use the original persistent store ID/limits for an
   existing compatible owner; do not initialize again to fabricate newer reports.
4. Ask [formal questions](software/v5/ordinary_investigator_bundle/guides/QUESTIONS.md)
   or search for [reusable methods](software/v5/METHOD-DISCOVERY.md). The query
   companions stay in the source tree and use the selected package's actual
   path/PROFILE. A question is not a proved statement, and a hit is a candidate.
5. Use [continuation](software/v5/ordinary_investigator_bundle/guides/CONTINUE.md)
   for preview, acquisition, independent checking, exact module realization,
   local Lean development and returning selected mathematics. Pass the current
   package/profile/selector wherever that guide uses earlier ones. Existing
   kernel checks, semantic identities and support limits remain in force.

After the multi-source guide's successful final receipt checks, its selected
variables can supply the continuing investigator guide:

```powershell
$investigatorPackage = $multiPackage
$investigatorProfile = $multiProfile
# Keep investigatorSource/Python/Lean bound to the already approved locations.
& $investigatorPython -I -S -B `
  "$investigatorSource\software\v5\ordinary_multi_source_package\prepare_selected.py" `
  --package $investigatorPackage --profile-sha256 $investigatorProfile `
  --request 'C:\commons-requests\request.json' `
  --output 'C:\commons-requests\prepared-01'
```

Preparation writes inert config/arguments; it does not execute the operation.
Select and launch the resulting finite operation through the actual final
package's `run.py` with fresh outputs and the original complete closure checks.
Do not bypass the public selector by calling its private preparer directly.

The multi-source update is optional, not a reason to rebuild a functioning
exact-module-only installation. Keep these exact interfaces paired:

| Selected package | Matching selector under `software/v5` |
|---|---|
| Exact-module only | `ordinary_investigator_bundle/prepare_selected.py` |
| Exact-module plus multi-source overlay | `ordinary_multi_source_package/prepare_selected.py` |

The latter preserves default behavior. Only `receive` optionally accepts all
three source-policy fields together. For old-PROFILE reports, its guide supplies
the direct public receive route with an explicitly selected existing parent and
new hashed config. Never rewrite old reports or relax PROFILE checks. Unchanged
support gives a narrow compatibility argument, not a claim that consolidation
reopened an old owner or performed new mathematical acceptance.

## What the current navigation supersedes

The preserved multi-source guide's opening "source integration only" status and
requirement for separately gathered supplement files are historical. The selected
integration has an adopted file-only package/preparation result, and this source
set includes its exact nine source files. Its operational constraints remain.
That result did not reopen state, run Lean or establish worldwide deployment.

The old investigator README's archive count and whole-root verifier are likewise
historical. This handoff preserves its 169 payload byte strings exactly once;
only old root `README.md` moves to `HISTORICAL-INVESTIGATOR-README.md`. The old
`INVESTIGATOR-SOURCE-MANIFEST.json` remains exact at root as an association for
that projection and the mirror's fixed dependencies. It is **not** the current
full-root manifest. Old full-root verifiers must reject this larger extraction.

The 17 added payloads include that old manifest, this current README/utility,
the repaired mirror and its current guide, method guidance and the nine
multi-source files. There are 186 payload rows plus the current manifest.
Tests, experiment history, adoption reports, runtimes, mathematical bundles,
credentials and owner state are excluded. Historical evidence links in frozen
documents need not be present; they are not required build inputs. Current
operational navigation is provided here and in the linked guides.

Search remains incomplete and resource bounded. Cold mathematical acceptance
may require selected dependency work; compatible warm local anchors avoid
repeating already checked work but are not remotely portable trust. Storage-only
retrieval can deliver false but structurally valid data; receivers still check.
Holders can disappear. Multiple sources cannot recover bytes all holders lost.
No sustained useful-growth or planet-scale recall claim follows from packaging.
Use the [update and recovery rules](software/v5/UPDATE-AND-RECOVERY.md) with these
package/selector overrides; preserve uncertainty and failed committed prefixes.

## Maintainer-only packing

Recipients need this extraction, approved runtimes and their own data, not the
repository or old archive. Recreating the selection is a separate operation:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\approved-checkout\software\v5\ordinary_commons_bundle\bundle.py' pack `
  --source-root 'C:\approved-checkout' `
  --investigator-root 'C:\preserved-investigator-extraction' `
  --output 'C:\commons-handoffs\commons-01'
```

The output leaf must not exist; its parent must exist. The packer reads the exact
169 old payloads/manifest and 16 explicitly mapped source files, never a repository
glob. It writes deterministic ZIP_STORED `source.zip`, rereads actual ZIP/inputs,
then writes the external terminal `RECEIPT.json`. Require exit zero and
`PACKED_COMMONS_SOURCE_NOT_BUILT`, and preserve the receipt with the archive.
No overwrite, deletion, automatic retry or build occurs. Cooperative limits are
60 wall/30 CPU seconds; use approved outer containment for hard resource limits.
