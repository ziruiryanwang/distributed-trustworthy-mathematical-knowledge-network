# Exact-declaration continuation controls

Source-ready, not executed. Owner: `core_release`. Root selects any finite run.

Selected test source:
`software/v5/client/supplier_complete/test_declaration.py`

SHA-256: `7101aaf574e9c6ec1a56ec4411ac23d71072719b7b255dc2913cf8a296cb7d69`.

Prelaunch independent review caught a test-only locator assumption: the real
adapter also returns schema and descriptor identity fields. The actual loopback
assertion now compares the requested module/name/group subset and separately
checks the committed descriptor. No runtime occurred on the earlier test source.

## Scope and economical discriminator

Ten mandatory controls (seven real-facade controls and three helper controls)
exercise the newly added exact-declaration continuation boundary. Existing
fixture constructors are reused; no predecessor suite is selected. One small
actual loopback scenario requests a missing second declaration from P, retains
the operation, then obtains the exact committed opening from Q. This is actual
transport, structural validation and SQLite custody, with explicitly inert
mathematical issuers. No genuine warrant, native check, proof, install or RAM
experiment is part of this test.

The decisive distinction is between a positively settled unavailable supplier
and an invalid successful mathematical-data response. Only the former may
continue. The tests do not re-enumerate the already reviewed body-transport
timeout/reset/error matrix.

## Selected obligations

| Control | Required observation |
|---|---|
| Actual P-absence then Q | P leaves origin/candidate count/custody and inert warrant sentinel unchanged. Q returns a new Q-bound candidate for the exact requested module/name/group, with real custody/readback. Original grant and budget survive; two requests and exact reply charges; both providers close cleanly. |
| Fixed group route and refusal | HTTP 404/503 use `/v5/modules/group` and exact `{module_id, relative_name, group_index: null}`. One dial, full reservation charge, no candidate or target group. |
| Invalid successful opening | Malformed/noncanonical JSON, different module, absent requested name, corrupted committed group, refusal disguised as HTTP 200, and HTTP 400 are fatal. No target custody or mathematical admission. |
| Cancellation / uncertain cleanup | Neither is downgraded to supplier absence; original reservation is settled conservatively and the client fails. |
| Custody / final binding | Failed put, failed post-commit readback, and changed contact immediately after settlement remain fatal. A committed group after failed readback is preserved as data, not acceptance. |
| Original acquisition allowance | Four unavailable explicit choices consume the four remaining requests after the original search reservation. A fifth cannot dial; no grant/deadline renewal. |
| Contact/source guard | Unknown/expired/changed contact, absent new source pin and replaced declaration hook fail before dialing. |
| Reader retained work | A reader already retaining a selected packet/member, group and body loses none of them on declaration refusal. Pending demands, bytes and revision stay exact; one step is consumed. Explicit Q then adds the exact new group. |
| Reader fatal/refusal binding | Fatal client error or a refusal for a different requested name fails the reader. |
| Reader cached/step limits | Cached Q still checks authorization and timeout; refusals consume the original finite helper step allowance. |

## API assumptions and fixture boundary

The test selects fresh logical overlays `client.workspace_evidence` and
`client.semantic_reader` from `supplier_complete`, plus the existing
`staging_members/workspace_staged.py` overlay. It imports existing
`client.test_direct_contacts` and `client.test_semantic_reader` constructors only.
Its source map must include the new `transport.declaration_resilience.py` and
these three fresh overlay/test sources in addition to the predecessor selected
fixture dependency map.

The facade API is `try_resolve_declaration(...)`, returning either
`DECLARATION_CUSTODIED` with a candidate and `mathematical_acceptance: false`,
or exact `DMKN_SEMANTIC_DECLARATION_ATTEMPT_V1` refusal fields. The helper API is
`try_resolve(...)`, returning its existing `RESOLVED`/`NO_PROGRESS` shape or the
same exact refusal. Refusals have no mathematical authority.

The runner requires an already-created canonical output directory and
exclusively creates `controls-result.json`; there is no evidence overwrite.
Only the ten explicit method names are selected. Subprocess creation is blocked
for the run. It reports exact test-source hashes, control names/counts, actual
loopback requests, budgets and provider closures. Independent source review and
the root's finite selection remain pending; this note claims no passing outcome.
