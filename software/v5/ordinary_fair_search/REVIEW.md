# Fair-search controls and ordinary bridge: source review

Disposition: **SOURCE GO for the proposed finite 16-control native-free suite**.
No blocking source defect was found in the reviewed test/bridge changes. This is
not an execution result, installed-product qualification, performance result or
completion of v5. Root retains exact source selection and launch authority.

## Independence and scope

Reviewer: `/root/current_security_obstruction`. This reviewer authored
`fair_exchange.py` and `fair_search.py`; it does **not** claim an independent
audit of those implementation files. Root independently read that implementation.
This review independently examines root's `test_fair_search.py`, `peer_api.py`
and `profile.py`, including their use of the implementation and import closure.
Only this Markdown checkpoint was written. No runtime, import, socket, database
access, native invocation, test execution or Git mutation was performed here.

Reviewed SHA-256 identities:

| File | SHA-256 |
|---|---|
| `test_fair_search.py` | `4162484ff1a366ea0b2ef5005373b73e1e274c15b3b1d207b65158a3d1ba3749` |
| `peer_api.py` | `06663bcda04345cb9ea38ca422d7545b5736a208c2d79742bebc095f5409b7e5` |
| `profile.py` | `828031e82f3dd43865d189587affa61dd6f8abe5b8667d45da0673949a069743` |
| implementation: `fair_exchange.py` | `3fe626b2dc4e63c345e54a517b1b37eea6eedada6d0fbb497aa18745a93eb828` |
| implementation: `fair_search.py` | `2567fcb2308c7e477c08b958a3661348eee682c5a98ce2389dd9add02d48e652` |

## Direct findings

1. **The bridge is narrow.** Read-only exact comparison with
   `ordinary_bounded_operations/peer_api.py` shows the selected client import,
   `find` orchestration/documentation and partial-result capture changed. Config
   validation, original network precharge, deadline narrowing, CA pin checks,
   result bounds and remaining public operations are preserved. Two trailing
   blank lines are also removed. `find` passes the existing `SearchSession`,
   a 5000-ms attempt ceiling, an allowance/ledger/CA check callback and the
   unchanged metadata-refusal predicate. Transport and uncertain-cleanup failures
   do not enter that predicate. Partial matches/offers/errors survive failures;
   the facade's existing error and ledger-finalization paths remain active.

2. **The loader change matches the new imports.** Exact comparison of `profile.py`
   adds only `transport/fair_exchange.py` and `discovery/fair_search.py` to its
   pinned support roles. Existing exact census, hash and loaded-path checks stay
   unchanged. A future package must actually supply and pin those roles; this
   source review does not establish successful package assembly or loading.

3. **The controls exercise the consequential scheduling boundary.** The first
   test requires both offers and both first candidate pages before another page.
   Separate stalled-offer and stalled-page tests require a later-provider hit and
   retained charges. Other controls cover refused connect; fatal dirty closure,
   cancellation, unreturned connect timeout/reset and unknown local failure;
   rejected membership; no legal cleanup slice; single-use refusal; exhausted
   request cap with retained offers; exact JSON-refusal recovery; owner-deadline
   mutation before dialing; and nonprogress cursor with another provider's hit.
   They assert settled reservations, no false coverage and relevant charging or
   no-further-dial outcomes. These are falsifiable controls, not pass assertions
   inferred merely from HTTP success.

4. **The synthetic test import selection is sufficient for its exercised routes.**
   The test explicitly binds `ordinary_authoring_offers/http_provider.py` as
   `transport.http_provider`, avoiding the older same-named provider. Its closure
   consists of the two implementation files, the test, `transport/clients.py`,
   `custody/module_store.py`, and discovery's `formal_features.py`,
   `authenticated_index.py`, `summary_wire.py`, `discovery_query.py`,
   `candidate_query.py`, `discovery_store.py`, `search_session.py` and
   `test_candidate_query.py`, plus the standard library. `clients` eagerly imports
   custody; custody imports discovery storage, so both are required even though
   the scenario exercises no custody operation. Other provider routes lazily load
   ordinary acquisition/authoring modules, and other record schemas lazily load
   adapters; neither branch is selected by this index-only synthetic fixture.
   The predecessor test module contributes only its fixture/constants; its tests
   are not selected and its main entrypoint is guarded.

## Proposed execution boundary and remaining limits

The proposed root-owned run is one finite native-free suite under the frozen
runner, with a 60-wall-second / 45-CPU-second / 768-MiB envelope. This review does
not replace root's exact snapshot/runner/runtime pin validation. Preserve the
result or failure; no retry or enlarged allocation follows automatically.

The fixture creates fresh **in-memory SQLite** metadata and uses the real
authenticated-index/session logic. Only `asyncio.open_connection` is replaced by
in-memory stream fixtures. It creates a fresh output directory and `RESULT.json`.
There is no actual TCP connection, TLS handshake, native checker, subprocess or
retained mathematical state. The session clock is artificial while asynchronous
stall timers are real; timing and hard-wall performance claims are unsupported.
The nonprogress case has one nonempty partition: it tests other-provider
continuation, not continuation to a later partition.

The suite does not import or execute the public facade/loader, qualify ordinary
export-record parsing, or establish a deployment sandbox. Source inspection is
the bridge evidence at this stage. Synchronous local work, inadequate aggregate
budgets and fatal uncertain cleanup can still prevent later-provider progress.
Successful controls would justify the selected conditional opportunity-fairness
mechanism, not completeness, relevance, mathematical acceptance, useful novelty
or creative concept/theory growth. Those remain separate project obligations.
