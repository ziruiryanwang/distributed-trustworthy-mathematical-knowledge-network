# Persistent withdrawal: independent source review

Reviewer: core_release. Source-only; no tests, native calls, proofs, builds,
distribution rereads or Git mutations. Selection: TRUST-WITHDRAWAL-SELECTION.
**Changed product boundary passes source review; runtime evidence is not yet
present.** This is one local trust-update obligation, not final-v5 acceptance.

## Reviewed sources

Paths below are relative to `software/v5/trust_withdrawal/`.

| Source | SHA-256 |
|---|---|
| admission/trust.py | a60fd123845c7cd732967f995363b3132ebab1522cd90870ab728e6a54dd83ee |
| admission/verifier.py | 01fb93b5d0063110fe82978dcc8a593557b34eaa8b6497f596715ca65064e38c |
| aggregate_claims/aggregate_admission.py | 2ef830f849ff214b4e4b3c314332d8d3d3d23844c1a763828e1be5a5f37732aa |
| client/runtime.py | 70c52b5148c481ca840c6c55557c9bc5abf71f40d522365f0cb7b0398adbad39 |
| client/remote_reader.py | f8859ad37eb70d14016cec119a5b9114e19f11c7b74aa9a6c34eb87987c780eb |

The helper and runtime were read completely; issuer successor diffs preserve
the already inspected receive/close paths. A forwards mandatory binding before
base initialization and includes identity in its independently replaced profile.
The fresh reader requires explicit domain/support IDs and calls open, never create.

## Argument and resolved issue

For an original registered binding, each live gate rereads the bounded exact
adoption, verifies original directory/record identity and observes any WITHDRAWN
entry, irrespective of marker content. Observed missing/changed/withdrawn state
latches denial. Live I/A denial clears handles and A member caches without
calling busy-forbidden public close. Receipt reservations are never refunded.
Postworker installation checks and final active checks prevent minting after an
already applied withdrawal; direct I.describe now final-checks copied facts.

Runtime construction derives stable support and checks the original exact
domain/binding. Both issuers receive that same binding. New operation entry and
the immediately pretransfer check gate actual construction; failures close all
created owners, or poison workspace on cleanup error. No async rollback is
invented after transfer. Existing mixed/import/client liveness gates propagate
issuer denial; inert reports and retained custody are not live authority.

Initial support generation duplicated all 584 manifest Python-census rows,
exceeding the helper's 512-role bound. This was corrected before execution:
the exact supervisor-manifest commitment includes that table; active worker,
SDK, supervisor, verifier, authoring and Lean roles retain explicit pins. The
launcher validates the actual Python census. This transitive commitment does
not weaken the selected support coverage and avoids the duplicated flat table.
Generated profile bytes and per-operation paths are excluded, while their
selected role contents remain included. Relocation of unchanged role content
does not itself change this support identity.

## Controls proposed, not executed

`controls.py` SHA-256
`748bd8bd6ddeed3680c74f67ef84f5e9fa62427af8f1943c6f2d8ccebec6dfef`.
Eleven focused cases cover positive existing-domain reopen, exact/foreign binding,
sticky/persisted denial, malformed/missing adoption, partial marker and write/sync
failure, mandatory signatures, busy I/A revocation, actual I.receive postworker
refusal before binding/minting, original runtime binding/new-operation denial,
and same-binding forwarding with pretransfer refusal/cleanup. Exact exception
types/reasons prevent an AttributeError from counting as a trust refusal.

Trust records are real; issuer/runtime shells and supervisor/constructor doubles
are explicitly inert. No valid receipt, cryptographic acceptance or executable
adoption is fabricated. A postworker synthetic operational closure is only a
negative-gate fixture; bind_output is forbidden and no handle is minted. Mutation
and deletion affect only newly created bounded fixture files. Subprocess APIs
are forbidden. Authors/root must independently review controls before selection.

## Limits retained

Owner/OS and owner-serialized final-check ordering are trusted. An unwritten
withdrawal cannot survive restart; create/flush failures are raised, never
acknowledged as durable success. Complete bytes left after failed fsync may be
explicitly reopened; that does not retroactively prove durable acknowledgment.
Partial/malformed adoption never implicitly repairs. No hardware antirollback,
power-loss guarantee beyond the filesystem, concurrent atomic check-and-mint,
instantaneous recall, hostile-code isolation or secure-update distribution is
claimed. Root owns the separately pinned finite launch and outcome adoption.
