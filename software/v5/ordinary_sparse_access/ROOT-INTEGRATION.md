# Root integration source checkpoint

Six fresh successors now implement the selected public forwarding boundary:
`peer_api.py`, `peer.py`, `profile.py`, `search_session.py`, `fair_search.py`,
`fair_exchange.py`. Each derives from the exact contact-federation package
identified by CONTRACT.md. Baseline files were read, never edited. New changed
sources use LF; this does not renormalize any frozen predecessor or evidence.

The held SearchSession request selects V1/V2 verification while retaining the
existing `candidates` operation and every conservative accounting branch.
FairSearch binds owner candidate_mode immutably, chooses the corresponding
endpoint, and passes the mode to session creation. Absolute deadline propagation
and settlement are unchanged. The settled transport's closed route allowlist
adds only the new read-only candidate endpoint.

Direct find and directory-find's nested search accept/validate/forward optional
candidate_mode. Absent means atomic-v1. API and CLI repeated index validators
accept optional access_pairs, forwarded to Store without changing existing
path, state, exclusivity or create/reopen rules. The profile requires the new
pair_access helper in its verified support closure.

No target code was imported, executed, packaged or tested by this source edit.
Independent integration review is assigned; helper/store/candidate/provider
authors have separate files. Public instructions are prospective until review
and finite execution pass. Existing acceptance/custody/native sources are not
part of this change.
