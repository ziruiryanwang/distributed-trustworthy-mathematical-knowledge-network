# Selected body-recovery controls

Source prepared; **not executed**. Root owns launch/adoption. This suite tests
only the new body-recovery boundary and borrows old fixture constructors without
running their predecessor suites. No native process, proof or genuine warrant
is constructed. Output is `controls-result.json`, avoiding the Windows
`RESULT.json`/`result.json` collision.

Source: `software/v5/client/supplier_resilient/test_resilience.py`, 28,624 bytes,
SHA-256 `c19a5b137133af39fe0ce0e3e5f24f4887a1f91d634e8fd4b1921904fb3ddbb8`.

Fourteen selected test methods cover:

- Actual loopback P with the selected group but no body returns EOF; Q returns
  the exact committed body. Real facade/contact/budget/validator/SQLite custody
  are used. The same client/grant/candidate and an explicitly inert warrant
  sentinel survive P; P is fully charged, Q succeeds, and providers close.
- Framed 404/503, clean EOF/refusal/reset/broken pipe and bounded read timeout
  settle once without retry or custody mutation, charging the full reply cap.
- Uncertain closure, cancellation/unreturned connect errors, malformed 200,
  wrong body hash/module/name/arity, a peer-serialized fake refusal, bad framing
  and HTTP 400 retain fatal behavior.
- Custody-write and after-commit readback failure stay fatal. The latter test
  explicitly retains already committed bytes rather than claiming rollback.
- Alternating suppliers exhaust the one original request allowance. Unauthorized,
  expired or changed contacts cannot dial. Missing adopted source pins and a
  replaced local hook cannot mint a refusal; all nine required source pins are
  populated in the otherwise inert fixture.
- Separate inert-client helper controls retain pending demands, selected
  semantics, revision and bytes after refusal; only steps advance. Explicit Q
  then progresses. Invalid refusal claims, fatal local errors, unauthorized
  cached suppliers and invalid cached timeout arguments still fail.

Transport fault controls use real parsing/settlement with explicit fake streams;
only the first control is real socket I/O. Helper controls test composition,
not mathematical admission. A preserved inert sentinel is not a genuine live
warrant. These controls do not claim full READY, new certification, global
availability, performance improvement or completed v5.

Author source inspection aligned the suite with transport `43fa1acd`, facade
`22c01a28` and helper `9b82de53`, including exact request-bound refusal fields.
The proposed finite selection is 20 CPU / 60 wall seconds / 128 MiB. No compile,
import, test, build, native run, memory probe or Git mutation was performed here.
