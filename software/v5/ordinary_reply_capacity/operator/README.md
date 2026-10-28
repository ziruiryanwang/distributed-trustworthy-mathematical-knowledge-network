# Operator companion for the reply-capacity package

This companion combines the existing operator interface with explicit prior-report
selection. Its preparation code is byte-identical to ordinary_report_selection;
only the exact compatibility map and its adapter pin select the reply-capacity
provider successor. Root adoption records the actual package and control status.

Use [the report-selection guide](../../ordinary_report_selection/README.md) for
the opt-in `selection_report_policy: "prior-profile-extract-only-v1"`. Earlier
reports remain unchanged and their original PROFILE values appear in a pinned
selection disclosure. Default strict behavior and unrelated report roles remain
strict. Current product checks are unchanged. The [example request](example-contribution.json)
requires explicit local inputs and source approval before preparation.

Run prepare_selected.py from this directory with an explicitly selected package,
PROFILE hash, request and fresh output. Keep it with prepare.py and compatibility.json.
The companion prepares inputs only. Execute those inputs through the approved
package's bounded run.py; no script or request supplied by a remote peer is run
automatically.

The provider now treats locator/evidence response sizes as upper bounds. A full
object may fit the remaining host allowance even when the client's maximum is
larger. Objects that do not fit still refuse; client failed-attempt charging,
preview sizes, discovery coverage and mathematical verification do not change.

Existing dedicated-host generations retain their original PROFILE-bound seals.
This package does not migrate or rebind those generations. Use their selected
earlier package, or explicitly prepare a fresh generation from retained inert
bytes under the new package. This companion cannot turn an old host seal or
an old mathematical report into an acceptance by the new package.
