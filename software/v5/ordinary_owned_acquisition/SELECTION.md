# Owned ordinary acquisition

2026-10-28, root. Implementation selected; runtime is not yet selected.

The user workflow is an investigator obtaining a preview, an exact import
locator and evidence from configured custodians, with bounded fallback when a
custodian is unavailable. Current acquisition suppresses connection-close
failures and starts its relative timeout after TLS setup. The adopted discovery
transport already owns sockets and distinguishes settled refusals from uncertain
cleanup. Reuse it rather than add a second transport design.

Read/adopt the fixed-provider argument in
`../ordinary_dependency_location/RECEIVER-SEAM.md`, SHA256
`801c193e75f31abaf4c1426317d11ba77c0c7f01d5c1cf0d5a0371ad5efe90ef`.
Fresh successor files here may change only ordinary acquisition and the owned
exchange helper. All four current typed read routes must remain supported,
including advisory authoring offers. Preserve exact validation, custody,
failure charging, no-retry default, terminal malformed input and mathematical
admission. Pass the original absolute ledger/attempt horizon through setup.
Uncertain cleanup, cancellation, TLS and unknown local failures remain terminal.
HTTP_PROTOCOL is not retryable; PEER_EOF maps to INCOMPLETE_READ only in the
existing explicit retry mode. No dynamic providers or location protocol yet.

Expected benefit is closing an existing fallback and deadline reliability gap
without changing Lean, the owner, native checking, anchor identity or wire data.
Two auxiliary payloads plus their fresh map/profile are the intended integration
cut. Preserve every used predecessor, the current kit and standalone inert host.
No proof generation or repeat mathematical campaign is justified by this change.

Owners: query_scaling implements `ordinary_acquisition.py`, `fair_exchange.py`
and CONTRACT.md. growth_design_audit independently reviews and prepares focused
controls. Root owns assembly, exact compatibility checks, finite operation
selection, adoption and Git. operable_scale_decision completes its distinct
dependency-location source feasibility before any further assignment.

Decision-changing validation: exact unchanged installation and anchor-support
closure; conservative charges/deadline across allowed refusal and success;
no fallback after malformed/unsettled outcomes; actual retained typed reads
after one settled unavailable provider. Existing owned-socket tests are reused
unless changed code introduces a new boundary. No package is adopted merely
because its sources exist. The final-v5 goal remains active, local/unpublished.
