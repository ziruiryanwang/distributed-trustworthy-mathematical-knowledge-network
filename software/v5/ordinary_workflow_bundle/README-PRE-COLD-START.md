# Start here: the ordinary Lean mathematical-commons workflow

This is the authoritative guide for this **one self-contained source archive**.
It is stored as `START-HERE.md` at the archive root. It brings together the existing
ordinary Lean-first build, bounded discovery/receive, source-based extension,
selected offline export, receiver checking, finite serving and recovery routes.
No project-repository checkout, research tree or historical default installation
is required to use these routes after extraction.

The supported profile is **Windows x86-64, Python 3.14.6 and Lean 4.34.0**, using
independently approved runtime distributions. Runtime binaries are not bundled
or downloaded. This is local, unpublished candidate software; [the license is
undecided](software/v5/ordinary_release_bundle/LICENSE-STATUS.md). It does not
grant redistribution permission or claim that the complete worldwide v5 goal
has been achieved.

## 1. What to trust, and what the archive proves

The archive contains 154 payload files plus `WORKFLOW-SOURCE-MANIFEST.json`:

- The original 143-file transport-release source payload, byte-for-byte intact.
- Eight companion payloads: three unchanged code files, two unchanged guides
  and three narrowly revised distribution-specific guides.
- This start guide, the new bundle utility and `BASE-SOURCE-MANIFEST.json`, an
  exact copy of the old manifest retained only as base-association data.

**Use the new verifier below.** The retained old
`ordinary_release_bundle/bundle.py` expects a different 143-file root; its
`SOURCE-MANIFEST.json` format and full-root verification/packing instructions
do not apply to this enlarged extraction. There is no `SOURCE-MANIFEST.json`
at this archive's root and no competing root selection.

Independently approve the utility, archive and external `RECEIPT.json`. Check
the archive digest before extracting into a fresh owner-controlled directory.
Then use the new manifest digest from that approved receipt:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_workflow_bundle\bundle.py' verify `
  --source-root 'C:\commons-source' `
  --manifest-sha256 'REPLACE_WITH_APPROVED_WORKFLOW_MANIFEST_SHA256'
```

This checks the exact root census, complete payload hashes, unchanged base
projection and companion selection. It first checks ordinary paths and the
exact original helper bytes before loading that helper's file-only functions.
It imports no product module, starts no Lean process and uses no network.
It does execute this Python utility and the selected helper: approve those
sources independently before invoking them. A hash supplied by an untrusted
sender is not authentication or code approval.

Successful verification means **selected source bytes are present**, not that a
build is correct, a theorem is accepted, an installation is safe or a license
exists. Inputs must remain owner-controlled and unchanged. Preserve all refusal
evidence and partial outputs; do not edit expected hashes to make a check pass.

## 2. Build one package, then choose its actual identities

Keep build and operation outputs outside the verified source root. Every output
leaf must be absent and its parent must exist. Supply the approved runtime roots
and follow the [base build-and-overlay guide](software/v5/ordinary_release_bundle/README.md)
for these exact stages:

| Order | Source entrypoint | Input |
|---|---|---|
| Native build | `software/v5/ordinary_bounded_operations/build.py` | Approved source and runtimes |
| Overlay 1 | `software/v5/ordinary_fair_search/assemble.py` | Actual build package and BUILD-RESULT receipt |
| Overlay 2 | `software/v5/ordinary_contact_federation/assemble.py` | Actual fair package, PROFILE and ASSEMBLY receipt |
| Overlay 3 | `software/v5/ordinary_sparse_access/assemble.py` | Actual contact package, PROFILE and ASSEMBLY receipt |
| Overlay 4 | `software/v5/ordinary_transport_release/assemble.py` | Actual sparse package, PROFILE and ASSEMBLY receipt |

All four overlays copy native bytes; none rebuilds them. Select the **actual
generated package, PROFILE and immediately preceding receipt** at each stage.
Fresh supported builds can have different native hashes: do not insert the
historical default installation's PROFILE into new commands. Inspect successful
terminal results and clean closure before proceeding; partial files alone do not
establish success. The supported pinned source/runtime policy still applies.

For the final package, the offline operation selector is exclusively:

```text
software/v5/ordinary_bounded_transport/prepare_selected.py
```

The old `ordinary_network_kit/prepare_selected.py` is not the final selector.
Preparation writes inert inputs; it does not start an operation. Launch the
prepared operation through the **built package's** `run.py` with that package's
actual PROFILE and finite allowances. Read the included
[launcher instructions](software/v5/ordinary_bounded_operations/LAUNCHER.md).
This start guide overrides the older source-verification/packing sections and
any historical recipe that stops at sparse assembly or uses the old selector;
it does not change operation arguments or mathematical acceptance rules.

## 3. Select a workflow

| You want to… | Read/use |
|---|---|
| Initialize an owner, find candidates, preview and receive | [Network operation guide](software/v5/ordinary_network_kit/START-HERE.md), with the final selector/profile above |
| Extend received mathematics with your own definition or theorem | [Source-based reuse and explicit publication](software/v5/ordinary_reuse_workflow/README.md) |
| Copy only selected inert mathematics from existing custody | [Selected export](software/v5/ordinary_selected_export/README.md) |
| Independently accept an offline selected bundle | [Direct receiver intake](software/v5/ordinary_selected_export/INTAKE.md) |
| Serve already approved custody for several prepaid finite leases | [Finite service plan](software/v5/ordinary_service_plan/README.md) |
| Replace software or recover selected mathematics after a trust change | [Update and recovery](software/v5/UPDATE-AND-RECOVERY.md) |

Keep these source-side companions outside the hash-bound built package. Their
locations in this extraction are:

```text
software/v5/ordinary_selected_export/export.py
software/v5/ordinary_selected_export/selected_export.py
software/v5/ordinary_service_plan/service_plan.py
```

For the export guide's example `C:\commons-export\export.py`, substitute the
first path under your actual source root and select both exact code hashes from
the approved workflow manifest; the helper must stay adjacent. For the service
guide's example `C:\commons-tools\service_plan.py`, substitute the third path.
No extra executable needs to be fetched from the research repository.
Other example paths refer to operator-created requests/state, independently
approved runtimes, fresh outputs or the built package, not missing archive files.

Agents independently choose what to investigate. They may construct definitions,
derive consequences, connect earlier theories and explicitly return accepted
work. No global research agenda, human-intention predicate, model provider or
mandatory certificate producer is required. Search supplies candidates; receiving
and checking establish local warrants. Export and publication do not make an
unchecked theorem true. Existing bounds can refuse oversized or unsupported work;
the archive does not remove cold dependency-checking costs or establish growth
merely by counting exports.

## 4. Protect execution, private mathematics and state

Read [the execution-trust boundary](software/v5/ordinary_bounded_transport/EXECUTION-TRUST.md)
before using Lean/Lake source or local projects. Approved local source executes
with the account's permissions. Windows Jobs bound resources but are **not security
sandboxes**. Do not execute arbitrary peer projects or import peer native `.olean`
files as a substitute for the supported inert-data checking route.

Serving discloses the **entire addressable custody**, including unindexed,
dependency/sibling and retained unaccepted data. Publication controls
advertisements, not per-object read access. TLS does not create collaborator-only
permissions. Keep private investigation separate from disclosure-approved custody;
selected export and independent intake can populate a deliberately separate store.

The service plan is finite: all leases, horizon and aggregate quotas are prepaid.
It never admits or publishes new mathematics. Exclude writers for the **entire
plan, including inter-lease gaps**; there is no cross-epoch catalog lock or frozen
content snapshot. End the plan and inspect closure before explicit publication
or mutation. A clean quota-exhausted lease can advance only to its already paid
next epoch. Unknown accounting, accept-loop failure or unclean closure stops it.
There is no automatic retry, resume, perpetual daemon or availability promise.

Updates do not automatically transfer trust. A changed checking implementation
requires fresh checked state and independent checking of selected inert evidence
under supported identical portable semantics. Preserve old state and reports;
never rewrite markers, remove journals or relabel old warrants to bypass a refusal.
The recovery guide is conditional procedure, not an automatic migration utility.

## 5. Evidence scope and historical documents

The full project retains independently reviewed base archive/build/relocation,
selected-export, reciprocal reuse and bounded-operation evidence. The finite
service companion has adopted controls and two idle loopback leases. That service
evidence is not a loaded-service performance result or continuous-availability
test. This consolidation changes distribution/navigation only; it neither reruns
nor extends those mathematical/native/network claims.

The retained 143 base files intentionally preserve their original bytes, including
historical descriptions and links to research, ADOPTION and experiment records
outside this compact archive. Those links identify **archival evidence**, not
required operational inputs. Follow the current workflow table above and this
guide's overrides, not historical adoption paths or default package hashes.
No new research/evidence tree, credentials, owner state, compiled binaries or
runtimes are included. Local companion recipes are instructions, not evidence
that a new operator has already executed them successfully.

This archive's own successful packing/relocation outcome must be established
separately; writing these instructions is not that outcome. Global semantic
search completeness, sustained useful growth, broad platform support, independent
host deployment and public release remain separate claims and responsibilities.

## 6. Exact source-to-archive mapping

The base 143 payload paths and bytes are unchanged. Of the added paths:

| Repository source | Archive destination |
|---|---|
| `software/v5/ordinary_selected_export/export.py` | Same path, unchanged |
| `software/v5/ordinary_selected_export/selected_export.py` | Same path, unchanged |
| `software/v5/ordinary_selected_export/INTAKE.md` | Same path, unchanged |
| `software/v5/ordinary_reuse_workflow/README.md` | Same path, unchanged |
| `software/v5/ordinary_service_plan/service_plan.py` | Same path, unchanged |
| `software/v5/ordinary_workflow_bundle/guides/SELECTED-EXPORT.md` | `software/v5/ordinary_selected_export/README.md` |
| `software/v5/ordinary_workflow_bundle/guides/UPDATE-AND-RECOVERY.md` | `software/v5/UPDATE-AND-RECOVERY.md` |
| `software/v5/ordinary_workflow_bundle/guides/SERVICE-PLAN.md` | `software/v5/ordinary_service_plan/README.md` |
| `software/v5/ordinary_workflow_bundle/bundle.py` | Same path |
| `software/v5/ordinary_workflow_bundle/README.md` | `START-HERE.md` |
| Explicit selected old manifest | `BASE-SOURCE-MANIFEST.json` |

The three guide copies change only navigation/status text (and normalize copied
text to LF): selected export replaces its missing default-package ADOPTION
reference with this guide and says final package; recovery replaces two ADOPTION
links with included guides and replaces its missing research link with the
archival-evidence explanation; service replaces its pending-review sentence with
the adopted finite evidence scope and a link here. Their commands and operational
semantics are unchanged. The original repository guides are preserved.

`WORKFLOW-SOURCE-MANIFEST.json` is generated, not a source file. Its externally
selected hash binds all 154 payloads. `BASE-SOURCE-MANIFEST.json` has the exact
SHA-256 `f1beab01d43e4b5fc6d7b9999ff2795598e3f2ee77c0dc85f1d99e82a15b31f1`.
The new utility validates it as the exact original base projection, not as an
alternative approval for companions.

## 7. Recreate a handoff from the canonical development checkout

Packing is a **repository-only maintenance operation**: its explicit input map
uses the fresh distribution-guide source paths above, which are not duplicated
inside the archive. End-user verification, building and workflows do not need
that checkout. Do not run the old packer over the enlarged extraction or expect
an extracted archive to reproduce itself through the repository-only command.

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\approved-checkout\software\v5\ordinary_workflow_bundle\bundle.py' pack `
  --source-root 'C:\approved-checkout' `
  --base-manifest 'C:\approved-inputs\old-SOURCE-MANIFEST.json' `
  --output 'C:\commons-handoffs\ordinary-workflow-01'
```

The separately supplied base manifest must have the exact hash above. The output
leaf must be absent. Packing writes stored `source.zip`, reads its actual bytes
back and writes external terminal `RECEIPT.json`; it neither extracts nor executes
the payload or overwrites anything. Partial failures remain intact. The utility
uses bounded files/census and cooperative 60-wall/30-CPU-second checks inherited
from the approved helper; hard process containment needs an enclosing owner Job.
None of this authorizes external publication or grants a license.
