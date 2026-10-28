# Focused dedicated-host controls

Source only. Root selects execution after independent source review and exact
package assembly. Author has not imported or executed these sources.

`control_tests.py --package <selected package> --profile-sha256 <exact pin>
--output <fresh canonical experiments/v5-local-checks child>` loads only the
profile-pinned `owner.py`, `run.py` and `custodian.py`. It rechecks captured
source/profile bytes afterward and retains scratch files and partial failures.
It has an internal 45-wall/25-CPU-second allowance and needs the ordinary outer
supervisor. It does not bootstrap the installed product or open a database.

Five bounded groups cover the changed boundary:

- Current ordinary command guards refuse marked roots and descendants, including
  malformed markers; unexpected path errors fail closed. The launcher permits
  only the host entry's exact host root, never marked diagnostics/output or an
  ordinary peer's indirect index path.
- A producer call with inert support doubles refuses a marked output before
  reaching production or an operation budget.
- Real Windows byte locking uses two handles on a scratch marker/lock, verifies
  contention and later reacquisition. Pure close failures still attempt both
  stores and preserve uncertain closure rather than asserting success.
- The actual seal parser is driven with explicitly inert semantic/codec doubles:
  exact pin, field shape, profile, assurance, namespace, target census and duplicate
  target failures are exercised. This does not qualify evidence codecs.
- An inert asynchronous SDK deliberately leaks a pending task and fails. The
  task's cancellation cleanup must observe the real host lock held, finish before
  custody closes, and leave the wrapper's index closure unconfirmed. This directly
  distinguishes the repaired inner-runner design from premature lock release.

Native process creation, SQLite connections and normal application network entry
points are replaced with failing sentinels. Asyncio's own event-loop wakeup
machinery remains available; the suite does not claim an OS network sandbox.
No theorem, native owner, evidence database, real HTTP service or external data
is created. The two-handle lock check is one-process Windows locking evidence;
it is not a separate-host or hostile-local-user isolation test.

The retained-bundle plan separately covers the actual positive prepare/provider
integration. Do not expand this harness into another mathematical or scaling
campaign. Any failure is retained; no automated retries or resets are included.
