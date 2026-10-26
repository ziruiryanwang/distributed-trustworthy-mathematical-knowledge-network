# Independent fresh-public-route source review

Disposition: **PASS_PLAN; ACTUAL INIT SELECTION REQUIRED AFTER PACKAGE ADOPTION**.

Reviewed PUBLIC-PLAN, 9,810 bytes, SHA-256
`319717f8f93f79989458f54745796e9c6c3ea94c89edbbc425b059e4746e1d26`.
Read the two exact command templates and the unchanged public launcher/owner
initialization, intake, failure and close paths; also the installation/custody/
catalog identity and freshness boundaries. These were file/source reads, not
product imports, owner/status calls, database access, native execution or Git.
Canonical guard passed. Build/control theory and packaging audits were not
repeated.

The shortest route is appropriate: the existing public init command creates a
fresh owner, followed only after audited success by the existing intake command
over the retained bundle. Neither a new selector nor an old-owner recovery or
identity migration is necessary. The corrected intake template is the actually
executed current selection, not the stale unused draft.

| Existing input | Verified SHA-256 |
|---|---|
| std-init01.selection.json | `9076770d368ca86a5ea58fa96f22765658c35ac491da394e4690158580848f59` |
| std-intake02-current.selection.json | `1f168a31dda79d80b6e2a933431999ac4e4a1beb1bbc27acd39d6464df60343b` |
| custody_limits.json | `0342d3558227a97c665832209a0b88a9dc39aef2106ced5b500b9cb145c8a7ce` |
| retained bundle manifest | `1de776b3d131c8c1be3414ed0e0cf066ebd05caebbcd1cf1b6ca80853962e59c` |

Both template argvs and full limits objects agree with the plan. Init is public
90 wall/60 CPU/1280 MiB/three processes under outer 120/90/1536/four; intake is
360/300/1536/three under 420/330/1792/four. Bundle path/manifest, quota values,
diagnostics layout and runtime attachments remain unchanged. The focused-control
four-process setting does not silently replace the public three-process setting.

Owner init requires absent ordinary catalog/custody paths and separates them
from support/runtime paths. It creates custody and the catalog under the actual
installation semantics/implementation, then performs checked fixed-basis
initialization. Subsequent operations require the exact implementation/store
adoption binding; the catalog derives its local basis root from implementation
and store identity. Therefore an unchanged BasisSnapshot object is no basis for
reusing the old owner root or store label. The new deterministic label computes to
`fb625cc1b7d03d081e45bbcf73f7d59765f04a64a402484f23d00ac3e60ce4e7`.
All six proposed run/selection/catalog/custody paths were absent at review time.
Their absence and the 3 GiB free-disk premise must be checked again at selection.

Intake validates the manifest hash, opens the selected owner normally and uses
the supplied actual parent. Startup costs reduce the remaining intake budget;
the same nonrefundable per-batch reservations and original limits apply. Errors
retain accepted/uncertain state, and close errors change success to failure.
Public/outer zero exit is operational evidence; the child mathematical result,
native reports and exact selected bindings still require inspection. No private
state repair, diagnostic suppression or implied rollback is introduced.

The compact pin strategy is viable in principle: the init template has 191
external entries; replace its package entries and enumerate immediate new
evidence within the existing 256 limit. Exact counts and absence of stale package
paths remain launch-review obligations. Pin immutable mathematics by its complete
manifest and actual intake validation, rather than trying to make all 2,651 inert
files executable-selection entries. Mutable owner files must not be pinned as
unchanged inputs. This review did not reread all inert bundle payloads.

No package identity is predicted or adopted here. Review the actual complete
package map/identity before deriving the direct init selection. After successful
init, derive the intake parent solely from its saved checked result, bind that
evidence, and review the separate intake selection. A successful intake enables
the finite-map concept workflow; it is not itself evidence of useful growth,
general warm-authoring compatibility, all-Std support or completed v5.
