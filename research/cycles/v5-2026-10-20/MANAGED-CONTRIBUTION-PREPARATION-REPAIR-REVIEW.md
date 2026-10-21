# Independent review: preparation-only DirectoryInfo repair

2026-10-21, core_release. **PASS for the exact source delta and one fresh
preparation attempt.** No product execution or integration outcome is asserted.

## Exact reviewed bytes

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Frozen `Select-ManagedContribution01.ps1` |10447|`e3aa2a7f434edfdb3f833f45656cef9ae5eb05280f6fa147b345aa4a26e6a9b9`|
| New `Select-ManagedContribution01-DirectoryInfo.ps1` |10528|`6bd7d82c2d1c65147a97b46eff9f5daca3eb74d7469970c867e8dffe31915d64`|
| `MANAGED-CONTRIBUTION-PREPARATION-REPAIR.md` |1486|`0bae46a88f58f10023aabc9a3a625046e6f00d7deca435b9bb71b2b12311ffb4`|

The reviewer read the successor and repair note. Read-only exact-text comparison
found one occurrence of the old guard and one of the new guard; replacing only
that condition in the frozen source produced exactly the successor text.
No other source, pin, path, ACL, timing, resource envelope or command changed.
This is a delta review relying on the separately completed integration review,
not a redundant full-source qualification.

## Why the correction is valid

The old loop used the PowerShell provider-added `PSIsContainer` property. The
initial `Get-Item` result has that property, but `.Parent` returns ordinary
`System.IO.DirectoryInfo` objects without it. A null property therefore caused
the old `-not` condition to reject a legitimate ancestor.

Read-only traversal independently observed:

| Ancestor | DirectoryInfo | Directory bit | Reparse bit | PSIsContainer |
|---|---|---|---|---|
| `experiments/v5-private-credentials` |true|true|false|true|
| `experiments` |true|true|false|null|
| canonical project root |true|true|false|null|
| `E:\` |true|true|false|null|

The successor requires both DirectoryInfo type and the Directory attribute,
while preserving the exact ReparsePoint refusal. These checks apply to the
plain parent objects and retain the intended ordinary-directory constraint.
This fixes the reported failure rather than suppressing it or removing the
ancestor walk. It does not claim protection against a hostile concurrent
same-account path replacement; the existing trusted-owner scope is unchanged.

## Freshness and effects

At this review, all four exact intended targets were absent:

- `experiments/v5-local-checks/managed-contribution-01-input.json`
- `experiments/v5-local-checks/managed-contribution-01-selection.json`
- `experiments/v5-local-checks/managed-contribution-01/`
- `experiments/v5-private-credentials/managed-contribution-01/`

The ordinary private parent exists and is preserved. In source order, the
reported ancestor-guard failure occurs before creation of the private child,
input and selection. This is consistent with their independently observed
absence; it is not a fabricated product-run result. Freshness is a point-in-time
observation: the unchanged selector checks it again and uses create-new output
writes before any later root-owned launch.

The protected current-user/SYSTEM DACL creation and verification are unchanged;
no existing directory ACL is modified by this repair. The selector still creates
no secret. Windows PowerShell remains the selected host for its existing
Directory.CreateDirectory security-overload dependency.

## Recommendation and boundary

Adopt exactly successor `6bd7d82c...` for one new preparation using the already
reviewed arguments. Preserve the original failed preparation and frozen selector.
The still-unused test identity does not require a new product build or rerun of
passed controls. Inspect the actual preparation result before root starts the
already-selected public integration; this review does not predict its success.

Reviewer actions were only the canonical guard, source/note reads, SHA-256 and
exact-text comparison, target-existence checks and ancestor attributes. No
selector was executed; no runtime, build, credential access, deletion, ACL
change or Git mutation occurred.
