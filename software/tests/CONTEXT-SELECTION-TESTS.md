# Native-free context selection contracts

Prospective test source, 2026-09-21. Authoring and static inspection only: the
author did not import, execute, compile or test this suite. Root alone may run
it after implementation/source review under a separately bounded allocation.
It is not part of any frozen peer, recovery or transport-test source cut.

## Contract and intended interface

The selected prospective contract is `drafts/CONTEXT-SELECTION.md`, 10,756 bytes,
SHA-256 `ECA26C33892D22FEFCDD6B237AA5906F339F51581D11F96BDE9E2E57499A4004`.
Root confirmed these implementation interfaces before test authoring:

- Ordinary request `select_context` with exact arguments `context` and
  `selected`. Prepare authenticates both client-owned context records and the
  current head; commit rechecks both bindings and the expected head. Success
  has only the specified pointer/authentication fields, no `accepted` or fresh
  mathematical description. Existing exact-byte prior lookup stays first.
- `node.context_package_limit(value, common_count)` validates exact integer
  `common_count` in 1..16 (`CONFIG_PACKAGES` otherwise), then exact integer cap
  between `common_count` and 16 (`CONFIG_LIMIT:packages` otherwise).
- Configure locally imports/calls that helper with its fixed five common
  packages and `getattr(args, "context_packages", 16)`, before pinning, build
  inspection or directory creation. The CLI option is integer-valued with
  default 16. `load_config` validates `limits.get("packages", 16)` against the
  actual common-package-list length, preserving omitted-field compatibility.

The tests target those existing dispatcher/store and proposed helper APIs.
They intentionally do not silently skip missing implementation: before the
change, failures such as missing helper or unknown operation are expected.

After authoring, root's implementation was inspected without execution. The
new branches and helper signatures match these tests: `py/node.py` SHA-256
`5E2368E04BD0F12CC752BFE12E3949A2867B7F6683EC47B4973FDB635E9233E9`,
and `manage.py` SHA-256
`21A1788157C6298486CAB9A31A0624751264F8898E17528049D873599666F021`.
The suite has 24 test methods (eight cap/configuration, sixteen dispatcher/store)
plus bounded table-driven subtests. These are source counts, not executed passes.

## What is real and what is synthetic

`test_context_selection.py` imports the actual selected `node`, `storage`,
`manage` and `domains` files and checks their module paths. Dispatcher tests
use the real `ControlStore`, SQLite schema, indexes, transactions, ordinary
request parser, reservation, exact-byte prior lookup, record encoding and
terminal handling. An actual owner lock is held per isolated fixture.

The initial contexts, initialized bit, provider entry, candidate, artifact and
publication marker are deliberately **synthetic metadata fixtures** constructed
through store methods/explicit fixture SQL. No bootstrap was performed; these
are not mathematically checked contexts, actual published mathematics or
supervisor receipts. Contexts intentionally reference nonexistent package paths.
Every retained test directory declares this scope. This is appropriate for
testing metadata pointer transitions, not evidence of native mathematical trust.

No native file, `.olean`, build receipt, successful acceptance record or
supervisor receipt is fabricated. No fixture is copied into a production or
previously qualified state. Context-record tampering and intervening head
changes occur only in their own explicitly synthetic test stores.

Fail-on-use guards replace only forbidden checker, peering and native-stage
entry points. They return no simulated success and are asserted never called.
The dispatcher, record lookup, reservation, commit, replay and transaction
methods otherwise execute unchanged. One atomicity control injects a failure
at the first terminal write while retaining the real surrounding SQLite
transaction; the ordinary refusal-terminal write then uses the real method.

For configure preflight only, a narrow first-`pin` sentinel intentionally stops
valid input before build inspection. This establishes correct default/range
validation and rejection ordering without mocking a successful build or
pretending configure completed. Real `load_config` tests use actual installed
domain/source pins and synthetic configuration JSON; they create no state or
scratch directory. There is no claim that a native-capable node was configured.

## Coverage and exact observations

| Area | Required observations |
| --- | --- |
| Successful selection | Exact response bytes/fields; selected head only; no fresh mathematical authority, checker, peering or native work |
| Real ledger bookkeeping | Complete eight-table comparison: precisely one terminal request, one config-bound attempt marker, ordinary request/byte charges, cleared active slot, permitted pointer change only |
| Preserved knowledge metadata | Nonempty preexisting context/artifact/candidate/publication records, provider cuts, snapshots and entries unchanged; other client's head unchanged |
| No-op and missing live files | Successful charged no-op; metadata-only selection can succeed with missing selected dependencies and reports `UNCHECKED` |
| Record selection guards | Both expected and selected ownership/kind checks, unknown handles, stale head, malformed arguments; reservation timing follows existing parser/dispatcher behavior |
| Exact replay | Success replay after later head movement returns old bytes without reselection or charge; stale refusal remains historical even after head later matches |
| Request identity | Different bytes under one ID conflict, including whitespace-only byte variation; pending retry remains blocked without a new reservation |
| Content-handle ABA | A previously unexecuted request may run after the pointer moves away and returns to the same exact context; this is not an epoch-based workflow guard |
| Commit guards | Intervening pointer change refuses at commit; changed expected or selected record bytes fail binding; selected-head update rolls back if terminal write fails |
| Cap helper | Every valid helper `(common_count, cap)` pair; exact type and bounds reject booleans, strings, floats and out-of-range integers |
| Configuration loading | Current caps 5..16, omitted cap default 16, actual common count, bad count, malformed cap representations, immutable raw configuration hash |
| Configure preflight | Invalid caps refuse before any pin/build/directory work; valid 5..16 and omitted default forward exact values then stop at the explicit pin sentinel |

Argument validation after normal reservation is expected to consume that
reservation and retain its terminal refusal. Parser and exact-prior failures
before reservation must leave the complete ledger unchanged. A refusal is not
a mathematical judgment. Test fixture origin paths permit testing the ordinary
attempt-record encoding; they are clearly labelled synthetic paths and supply
no worker-quiescence claim.

## Invocation and evidence boundary

Root must select a fresh existing absolute `DTMKN_TEST_ROOT` outside—and not
containing—the real `software/` installation. A suitable separately allocated
location is project-level `product-local/context-contract-01/`. The suite
creates one exclusive `tempfile.mkdtemp` child per test and retains every child;
it never deletes or repairs test/production state. It requires Windows and the
product's SQLite 3.50.4 runtime through the actual store, plus Python startup
flags `-B -E -s -S`. It invokes no subprocess or network API.

The intended standalone test discovery pattern is exactly
`test_context_selection.py`, not broad discovery of frozen suites. A separate
root-reviewed worker/supervisor must provide wall/CPU/memory/process/output and
retained-fixture accounting. This note is not an executable launch grant and
does not silently reuse the owner-test allocation.

Retained per-invocation files contain exact request/response bytes and marked
synthetic before/after ledger observations. Test completion alone supplies no
supervisor cleanup evidence; the enclosing reviewed worker must supply that.
A failed test retains its fixture and is reported as failure, not repaired or
converted to success. Fixture counts and total test outcomes must be observed
from the actual run, not inferred from this prospective note.

## Deliberate exclusions

This suite does not qualify Lean acceptance, live context-byte validation,
growth, native work under the reduced package cap, full successful configure,
the end-to-end public CLI parser, crash recovery, concurrent writers or
hostile-owner tampering protection. A separate source-reviewed native-backed
experiment must exercise cap six, real admissions, selection and later fresh
source use. It must also audit preservation of historical evidence and actual
costs. The suite does not add `select_context` to peer recovery's allowlist.
