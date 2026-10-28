# Prior-profile selection: independent source review

2026-10-28. Reviewer: portable_integration. **PASS for the selected source-only
scope.** This does not record test execution, product adoption, mathematical
acceptance or general upgrade compatibility. Root owns subsequent selections.

## Exact reviewed artifacts

All paths below are relative to this directory. SHA-256 values were read from
the actual files after reviewing their source and documentation.

| File | SHA-256 |
|---|---|
| `prepare.py` | `203f6249e0659d13b58c79232b8e7a9533d0fc44d843c55a9eba03f244bb0892` |
| `prepare_selected.py` | `c86960216bc537bd61aa43940a62b7496bcdb2ecfd430ba28e5ed1abd35c65c2` |
| `compatibility.json` | `fa9fa6371e855f6ae711a866cdc31ed906ceb725274d776716d2416767fe3846` |
| `README.md` | `ba8be93001c80d97c1bc36000b4dfeee2913d1754752e5684612fc556389d96e` |
| `example-contribution.json` | `c934d64942bf88a03859e133a1aa03d4d98d947b573449bc3459febe41f4d7a1` |

Compared the helper and adapter text with the frozen
`../ordinary_dedicated_host/operator/` predecessors. The compatibility map is
byte-identical. The adapter changes only its helper hash, retaining its explicit
package selection, 48 direct-source checks, 72 generated-role boundary and
no-product-import behavior.

## Why the selected relaxation is sound

The architectural dependency is the previously completed
[consumer-chain audit](../ordinary_dedicated_host/REPORT-CONTINUATION-AUDIT.md),
SHA-256 `16b637471f58a7c6f7aa1cb11adefd6526a9a634ab8b9bfdfb2487bed4e5aad7`.
Reports supply proposed identifiers; the current product resolves them against
actual locked state and checks selected mathematics through its unchanged route.
No report statement can create a catalog root, repair a store binding, establish
parent membership, authorize source execution or import historical acceptance.

The new helper satisfies that argument:

1. `selection_report_policy` accepts only the exact
   `prior-profile-extract-only-v1` value. It is permitted only for `contribute`,
   `receive`, `intake-baseline`, `prepare-query` and `prepare-symbol-query`, and
   requires a `parent_report`. Unknown actions/policies cannot acquire the mode
   through permissive extra request fields.
2. `accepted_report` defaults to `selection_only=False`. Opt-in relaxes only
   equality of the reported PROFILE with the selected PROFILE and still requires
   the reported PROFILE to be a syntactically valid identifier. Known operation,
   successful result, clean error indicators, exact selected state, root/target
   syntax and applicable export-identity checks remain unchanged.
3. The flag reaches only the selected parent, acquired-target and authoring-frontier
   calls. Publication's call to the shared `accepted_report` remains strict.
   `Inputs.report`, `query_specs`, `selected_match` and producer handling are
   unchanged. In particular, an opted-in receive can use an old parent report
   but cannot use an old find report. An intake request's producer report remains
   strict. Interpreted query results are never relabeled or reinterpreted.
4. Acquired targets are precisely the explicitly selected report rows; no name,
   unit ID or export ID is rewritten. The combined existing target checks and
   bounded selection limits remain. A frontier contributes only its root to the
   unchanged current product's actual prefix/context check.
5. Every opted-in selection contributes a disclosure with original report reference,
   role, operation, reported PROFILE, comparison with the selected PROFILE and
   exact extracted roots/targets. The disclosure explicitly denies mathematical
   acceptance and established package compatibility. It is included in the
   existing output size bound and receipt byte/hash map.
6. Existing input grammar remains exact `{path, sha256}`. Bounded reading, pins,
   path exclusions and fresh-output checks remain. Source and project approvals
   come only from the explicit current request. No report-contained path is
   followed and no report is rewritten. State-directory metadata checks are not
   state/database opening.

The README and example accurately describe strict defaults, opt-in roles,
current-versus-original PROFILE disclosure, approval boundaries and exclusions.
The example is an intentionally incomplete template with explicit approval false.
The documented command selects the current package explicitly; no old report
chooses an executable or package.

## Remaining evidence boundary

No blocker was found in this changed source boundary. The opt-in is selection
convenience, not a compatibility assertion. A nonexistent root, absent target,
incompatible store or sibling frontier must still fail at its current product
consumer. An old report can honestly or maliciously propose unusable identifiers;
preparation alone is not their acceptance. Historical successful-status fields
remain untrusted data, and retained failed wrappers are not salvaged.

The smallest useful controls distinguish strict mismatch refusal, opted-in exact
parent/acquired/frontier extraction and disclosure, malformed/wrong-state refusal,
strict unrelated report roles, and byte-preserved inputs. One inert preparation
from retained real reports is sufficient to test the integration seam; no grounding,
Lean proof, service, reciprocal demonstration or owner-state run is implied.

This review ran only the canonical workspace guard and source/document/hash reads.
It did not import or execute the product/helper, run tests, open owner/database
state, perform native work, alter used predecessors or access Git.
