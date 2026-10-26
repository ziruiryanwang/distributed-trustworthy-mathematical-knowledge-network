# Ordinary mathematical investigator: start here

This is one source distribution for investigating with the Lean-first commons:
build a supported package, ask formal questions, receive independently checked
mathematics, introduce definitions and prove consequences, then return selected
work for another owner to check. An existing Lean project, shared research agenda,
central server, model service and succinct certificate are not prerequisites.
The agent decides what to investigate; discovery hints never authorize truth.

**This README is authoritative for this distribution.** The unchanged root
`START-HERE.md` is the previous workflow guide. Its final transport package,
selector and full-root verification instructions are historical here. The final
package now includes the **exact-module overlay**, the operator selector is
`software/v5/ordinary_investigator_bundle/prepare_selected.py`, and the full-root
manifest is `INVESTIGATOR-SOURCE-MANIFEST.json`. Do not use an earlier selector,
patch an earlier manifest, or copy companions into the built package.

## Supported profile and approval

Use independently approved **Windows x86-64, Python 3.14.6 and Lean 4.34.0**.
Runtime binaries are external and are neither included nor downloaded. Builders
check their selected runtime pins; this does not attest every transitive library.
Other runtime/platform combinations have not been adopted by this distribution.

All current work remains **local and unpublished**. The
[license is undecided](software/v5/ordinary_release_bundle/LICENSE-STATUS.md).
Source identity and a successful build do not grant redistribution permission,
authenticate a supplier, establish a security sandbox, or complete final v5.
Approve the source utilities, native package, runtimes and executable local Lean
inputs independently before execution. Read the
[execution trust boundary](software/v5/ordinary_bounded_transport/EXECUTION-TRUST.md).
Windows Jobs limit resources, not filesystem/network privileges. Do not execute
untrusted peer source, projects or `.olean` files automatically.

## Verify the source, then follow one current route

Approve the archive and terminal external `RECEIPT.json` independently. Match the
archive digest before extracting into a fresh protected directory, and select the
manifest digest from that receipt. Do not trust a digest merely because it arrived
with the same untrusted archive. Using the approved isolated Python:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_investigator_bundle\bundle.py' verify `
  --source-root 'C:\commons-source' `
  --manifest-sha256 'REPLACE_WITH_APPROVED_INVESTIGATOR_MANIFEST_SHA256'
```

Require exit zero and `VERIFIED_EXACT_INVESTIGATOR_SOURCE_NOT_BUILT`. Verification
is file-only: exact paths/census, byte lengths/hashes and frozen source selection.
It imports neither product code nor native artifacts. It does execute the two
approved file-only predecessor helpers after checking their paths and exact bytes.
It is not a compiler validation or mathematical acceptance operation.

| What you want to do | Current instructions |
|---|---|
| Build, select the final package, initialize, receive and realize a module | [Build and module guide](software/v5/ordinary_investigator_bundle/guides/BUILD-MODULE.md) |
| Ask a formal type question, before supplying a proof | [Fixed-basis and received-vocabulary questions](software/v5/ordinary_investigator_bundle/guides/QUESTIONS.md) |
| Find, independently check, extend and return mathematics | [Investigation continuation](software/v5/ordinary_investigator_bundle/guides/CONTINUE.md) |
| Recover or choose an update | [Recovery rules](software/v5/UPDATE-AND-RECOVERY.md), with this README's current package/selector override |

The build route is **native build → fair → contact → sparse → transport → exact
module**. Each stage uses its immediate predecessor's actual generated PROFILE
and terminal receipt. No historical installation, private state, experiment path
or historical generated hash is needed. The two query programs stay in this
source tree, outside the hash-bound built package. No peer or useful corpus is
invented by installing the software; investigations can begin with the fixed
basis or actual explicitly supplied mathematical data.

## What is preserved and what is new

The archive has **169 payload files plus one current manifest**. It preserves all
154 previous workflow payloads unchanged at their original paths, including
`START-HERE.md` and `BASE-SOURCE-MANIFEST.json`. The exact previous workflow
manifest is stored as `PRIOR-WORKFLOW-SOURCE-MANIFEST.json`; it authenticates that
subset's association, not this larger root. The old full-root verifier is expected
to reject the augmented root. Do not treat that expected refusal as corruption.

The 15 additions are that prior association, five exact-module overlay files,
two query programs, the current selector/map, this README, three current guides
and this bundle utility. Research history, tests, qualification archives, runtime
binaries, secrets, catalogs and custody are excluded. Historical links in frozen
documents may identify unavailable project evidence; they are not build inputs
or required operational steps. The three current guides contain the required
operational navigation. Those guides supersede historical claims that no
received-vocabulary question command is available.

This is a deployability improvement, not a claim of worldwide qualification.
Search remains budgeted and incomplete, selected modules have explicit size and
support limits, cold local acceptance may require dependency work, and continued
availability requires real holders. Warm compatible local anchors reuse checked
modules; they are not remotely portable mathematical trust. Useful growth and
large-network benefits require separate evidence, not merely a larger archive.

## Maintainer-only source packing

A recipient does not need the old archive or repository to build/use this
extraction. Recreating this exact selection is a separate maintainer operation:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\approved-checkout\software\v5\ordinary_investigator_bundle\bundle.py' pack `
  --source-root 'C:\approved-checkout' `
  --workflow-root 'C:\preserved-workflow-extraction' `
  --output 'C:\commons-handoffs\investigator-01'
```

The exact old extraction is an authenticated packing input only. The utility
reads its fixed 154 payloads and manifest and the 14 explicitly mapped new source
files; it does not scan the repository for additions. It writes a deterministic
stored `source.zip` and external terminal `RECEIPT.json` into a fresh leaf with an
existing parent, rechecks the inputs and ZIP, and never overwrites or deletes.
Cooperative limits are 60 wall/30 CPU seconds; use an approved enclosing Job if
hard containment is required. Failed partial outputs are retained, not renewed.

