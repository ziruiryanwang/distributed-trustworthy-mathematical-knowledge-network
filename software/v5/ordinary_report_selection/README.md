# Continue existing work with an updated operator package

This fresh operator companion adds an explicit way to prepare from prior-package
reports. It is source-only until root records its review, controls and adoption.
It does not change the product package or establish general upgrade compatibility.
Keep `prepare.py`, `prepare_selected.py` and `compatibility.json` together.

The practical problem is simple: an auxiliary query/hosting update changes the
package PROFILE even when the same checked local mathematics remains usable.
Previously, the helper required the old package merely to read its report's
parent root and acquired target selections. The new option extracts those exact
selections while preserving the report's original identity. The current product
still checks them against the selected owner before mathematical acceptance.

## Use the explicit selection policy

Keep the existing request and pinned report references. To prepare a contribution
using an older report, add this single field:

```json
"selection_report_policy": "prior-profile-extract-only-v1"
```

The [contribution template](example-contribution.json) shows its placement. Fill
all required nulls with your actual selections and select only source execution
you approve. The template's limits are illustrative finite ceilings, not measured
requirements. Save UTF-8 JSON without a BOM. A project-backed request can retain
its existing `project_authoring`, `approve_local_project` and
`authoring_frontier_report` fields; the same policy covers its frontier selection.

Run the companion using the already approved Python and explicitly selected
current package. Replace these illustrative paths and PROFILE hash:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons\operator-kit\prepare_selected.py' `
  --package 'C:\commons\package' --profile-sha256 APPROVED_PROFILE_SHA256 `
  --request 'C:\commons-work\request-01.json' `
  --output 'C:\commons-work\prepared-01'
```

The unchanged compatibility map recognizes the dedicated-host interface's
48 direct source roles and 72 generated roles. The adapter checks the selected
PROFILE and actual direct source bytes without importing product code. Generated
artifacts and mathematical compatibility are not approved by this helper. Do not
alter pins to force an unsupported package through it.

The output contains the usual `arguments.json`, `RECEIPT.json` and operation
inputs. Opted-in requests additionally contain `selection-disclosure.json`, pinned
by the receipt. For every selected parent, acquired-target or frontier report,
this records its input file/hash, original PROFILE, report operation, extraction
role and exact selected root/target rows. It states that no mathematical acceptance
or package compatibility has been established. Report files are never rewritten.

Inspect these inputs and launch through the current package's existing bounded
`run.py` using `arguments.json` and its normal resource allowances. This companion
does not launch anything, open an owner database, replay proofs, or repair state.
A prepared root/target may still be refused by the product. Preserve such a refusal
and resolve its actual compatibility or selection cause; changing the report's
PROFILE is never a repair.

## Exact scope

The policy is allowed only for these selection roles:

| Request action | Reports whose selections may come from another PROFILE |
|---|---|
| `contribute` | `parent_report`, reports in `acquired`, optional `authoring_frontier_report` |
| `receive` | `parent_report` only |
| `intake-baseline` | `parent_report` only |
| `prepare-query` or `prepare-symbol-query` | `parent_report` only |

The option requires a `parent_report`. A symbol query using a direct `context_root`
already needs no old report and therefore does not accept this option. Unrecognized
policy values and policies on other actions are rejected.

Without the field, all earlier strict PROFILE checks remain. Even with the field,
all selected reports must retain a known successful operation/result shape, exact
input hash, valid identity syntax, matching explicitly selected state fields,
target identity checks, size limits and clean result/closure indicators. Their
success words are historical input data, not today's proof authority.

Find, preview, publication, producer and query-result reports remain strict. For
example, an older receive report may select a contribution's acquired theorem;
an older find report cannot silently supply today's receive selection. An old
query result cannot silently supply today's query-key interpretation. A publish
request must still use its current-PROFILE report path. Source/project approvals,
contacts and operational paths come only from the explicit current request.

The selected product enforces the actual store/implementation binding, context
membership, selected name/export/unit relationships, evidence integrity and normal
mathematical checks. State relocation, arbitrary old schemas, incompatible native
implementations and missing custody are outside this convenience option. It removes
one continuation obstacle; it does not demonstrate faster discovery or complete v5.
