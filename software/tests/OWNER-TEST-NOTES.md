# Owner-contract test authoring checkpoint

Status: authored and statically reviewed only. No Python import, compilation, test execution, SQLite connection, Lean stage, or native acceptance was performed by the author. A later execution report must record its own results; this note is not a pass claim.

## Scope and authority

`test_owner_contracts.py` contains **20 unittest methods**. It exercises the real production `Domains` implementation, `build.read_record`, and the early refusal paths of `manage.configure` and `build.build`. It does not patch production behavior or manufacture successful native receipts.

This is a separate owner-contract suite. The existing transport suite remains frozen at 18 tests with discovery pattern `test_peer_wire.py`. Do not silently broaden that discovery, reuse its fixed test count, or treat its previous allocation as authorization for this suite.

Root owns the future bounded worker/coordinator, source-pin review, fixture allocation, execution, and outcome report. The prospective worker should require the exact 20-test discovery count, fail on skips/errors/failures or an unexpected count, and emit an explicit non-acceptance result. It should set `DTMKN_TEST_ROOT` to its separately selected existing fixture directory, retain stdout/stderr and all fixtures, and use the reviewed supervisor's finite wall/CPU/memory/process/output envelope. No native-stage budget is needed or authorized by these tests.

## Future execution prerequisites

- Windows and the product's selected Python runtime, including `os.path.isreserved`; launch with `-B -E -s -S`.
- Explicit discovery pattern `test_owner_contracts.py`, not all tests in the directory.
- `DTMKN_TEST_ROOT` must be an existing absolute non-root directory. There is no ambient temporary-directory fallback.
- Every test gets a new retained `owner-...` child and `test-case.json`. Synthetic install/runtime/state/scratch domains are sibling paths below that child. Their construction must not be confused with the actual product installation.
- The suite authorizes only fixture writes below that root. It creates no database, executable process, `.olean`, build receipt, accepted context, or mathematical result. Real module imports prospectively load definitions, including `sqlite3` and the Windows runner, but the suite neither opens SQLite nor invokes the runner.
- Fixture bytes are dominated by two approximately 1 MiB record-size cases. Allocate at least 4 MiB for fixture payloads, plus separate supervisor outputs and normal filesystem overhead. The executor must select and record a finite envelope rather than derive an unlimited allocation from this estimate.
- Tests retain failures too. There is no fixture deletion or teardown cleanup.

## Decision-changing checks

| Test group | Required behavior | Deliberately not established |
| --- | --- | --- |
| Startup and schema | Actual four-flag Python profile; exact domain fields; schema 2 is an integer, not bool or float | Negative child-startup matrix or hostile Python import defense |
| Domain separation | Construction is non-mutating; state/scratch disjoint; writable domains separated from immutable ones; runtime nesting allowed only in the declared direction | ACL enforcement, junction races, malicious same-owner mutation |
| Path capabilities | Exact state binding; reads from existing declared domains; strict work/write descendants; stages remain below the selected request; package reads narrower than general reads | A hostile-source sandbox or network peer policy |
| Lean path selection | Only the selected runtime's exact `bin/lean.exe` path qualifies | Authentic Lean executable, version binding, compilation, or kernel acceptance |
| Execution-record parser | Finite timing floats accepted; public integer-only JSON still rejects them; duplicate keys and nonfinite values rejected; exact byte bound and JSON framing | Complete receipt schema validation, timing accuracy, exact decimal preservation |
| Configure preflight | Invalid client declarations fail before state/scratch creation; existing selected paths refuse without altering their marker or creating the sibling | Successful configuration, support-build authenticity, database initialization |
| Build preflight | Existing work refuses before a stage; its marker remains unchanged | Successful support compilation or mathematical acceptance |

The `lean.exe` fixture is inert text, labelled as such in the test. It is used only with `Domains.require_lean`; it must never be executed or passed to a positive build. The build-preflight test has a separate runtime fixture with no executable.

## Exact parser distinctions

The execution-record parser is not the public request parser. It accepts ordinary finite binary floating-point timing values, including finite underflow to zero. It rejects duplicate keys recursively with `Refusal("DUPLICATE_RECORD_KEY")`.

JSON literals `NaN`, `Infinity`, and `-Infinity` currently raise `ValueError("NONFINITE_RECORD_NUMBER")`; overflowing numeric tokens such as `1e400` raise `Refusal` with that code. Tests preserve this distinction instead of wrongly assuming one exception class. Oversized input raises `Refusal("INPUT_LIMIT")`; malformed or trailing JSON raises `json.JSONDecodeError`.

The size-boundary case uses a scalar JSON value with whitespace. This intentionally checks `read_record`'s byte/framing contract, not an invented requirement that the generic parser itself validate build-receipt fields.

## Preflight case limitations

The client cases cover reserved `owner`, duplicates, punctuation, empty and overlong names, more than 16 names, and hashable non-string scalar entries. `configure` receives strings from its real CLI; this suite does not claim a general arbitrary-Python-object input contract. An empty client list is not a refusal case because it selects the default `local` client.

No positive `configure` test bypasses the real support-build requirement. No node acceptance, transport-failure classification, dependency replay, theorem reuse, persistence recovery, decentralized discovery, or utility/growth claim follows from these tests. Those remain separate qualification responsibilities.

## Production source checkpoint reviewed for authoring

These are authoring-time SHA-256 pins, not an execution allowlist. Root must repin the complete executable/import closure and worker/coordinator before any future run; changed product sources require reviewing the affected assertions.

| Source | SHA-256 |
| --- | --- |
| `software/py/domains.py` | `A3F44CCE31DDD79056F0683DE17D46712BFD46C99DFE71FAC56E27DD1DEB59C9` |
| `software/build.py` | `9F57312577C3E48683D4BFC365134A964CF85BB2FD3C86B98D642926DD1E08CF` |
| `software/manage.py` | `037E1A4067837E17EF2523371C4ABCBD5F94D3FA5157297286BADFA7DCA80A69` |
| `software/py/storage.py` | `31AB3C08C218F82F354F6F263B0F0325FE8E1124BF7940D580D6D0981D5B11CA` |
| `software/py/node.py` | `832E68E8B4A5449A80BF3F324CD14790C7F20A6F5DBE34C696DA49F65EA4DD77` |

Only `test_owner_contracts.py` and this note belong to this authoring assignment. The transport worker/coordinator and production files were not edited.
