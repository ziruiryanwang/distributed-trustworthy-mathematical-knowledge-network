# Exact-warrant delta imports (source-only successor)

Status: drafted for independent source review. No tests, native checking,
authoring, packet transfer or proof has run for this successor. Frozen `delta/`
callers keep their existing API and evidence. This package is not automatically
selected by installing or importing the old package.

## Why two identities are necessary

A ModuleID identifies a mathematical interface. An exact184-byte journal J
additionally identifies the adopted image, foundation, policy and derivation
rank. The same interface can have two valid warrants at different ranks.
Retaining both is necessary when independent branches used different warrants.

The receiver therefore retains ancestry by **exact J**, while the authoring
context installs declarations by **ModuleID and group index**. Sharing semantics
does not authorize substituting an old parent journal with another same-ModuleID
journal. All retained witnesses, ranks and parent lists remain unchanged.

For example, M0 at rank0 and M1 at rank1 share semantic M. M1 is derived through
a distinct helper H, not from M0. C1 uses M0, C2 uses M1, and T uses C1 and C2.
T's exact ancestry has both M warrants. M's declarations can nevertheless be
installed once. Rank variants do not count as new mathematical knowledge.

## Authority and wire boundaries

`DeltaVerifier` and `VerifiedDelta` in this package are distinct exact classes
from their frozen `delta.receiver` counterparts. The constructor still requires
the actual exact `admission.verifier.ReceiptVerifier`; it provides no injection
of a replacement checker. Frontiers require genuine legacy I receipts; every
native delta runs the unchanged adopted checker and binds its same-call output.

The packet remains `DMKN_NATIVE_DELTA_PACKET_V1`. It contains real I receipt
bytes plus complete bounded unsealed native witness ancestry. This is not a
succinct aggregate receipt and does not implement aggregate membership imports.
`aggregate_claims/` is a separate relation/authority path. A copied journal,
summary, result JSON or inventory never establishes mathematical authority.

The receiver profile uses the new
`local-native-delta-exact-warrants-profile-v1` domain. Its source pins include
the fresh receiver/init/claims plus the unchanged parser and transitive frozen
`delta` import closure. `DeltaOwnerPreparation` additionally requires fresh
authoring/imports pins and the frozen corrected emitter. Root must select exact
sources, native executable, source closure and finite owner allowances before
execution. Existing retained evidence is not qualification of these new bytes.

## Receiver API changes

```python
from delta_claims import DeltaVerifier, VerifiedDelta, Envelope

handle = receiver.receive(packet_bytes, expected_summary, ...)
facts = receiver.members(handle)
variants = receiver.variants(handle, semantic_module_id)
fact = receiver.describe_member(handle, exact_journal_bytes)
group = receiver.open_member_group(handle, exact_journal_bytes, opening)
```

`members` returns every established exact J, not just one entry per ModuleID.
Each fact contains `module`, `summary`, `journal`, `profile_id`,
`packet_sha256`, `proof_form` and `evidence_sha256`. The last digest binds the
original receipt or canonical native witness representation to this live handle.
It is not a second certificate. `variants` enumerates facts without selecting.
Exact lookup requires bytes J; passing a ModuleID refuses rather than choosing
the first result. Missing J is not satisfied by another warrant for the same M.

`describe(handle)` and `open_group(handle, opening)` continue to refer to the
packet's last checked target. Export returns the original complete packet.
Failure of `receive` revokes its earlier live handles as in the original owner.

## Import and new-author workflow

```python
from delta_claims.authoring import (
    DeltaImportSession, DeltaSourceOperation, DeltaOwnerPreparation,
    prepare_delta_context,
)

session = DeltaImportSession(receiver, ...)
target_journal = session.use_handle(handle)
available = session.variants(module_id)       # Enumeration only.
session.select_warrant(chosen_exact_journal) # Required even for one variant.
session.open_group(module_id, group_opening)
session.supply_body(module_id, universe_count, expression) # When demanded.
context = prepare_delta_context(session, foundation_bytes, foundation_sha256)
```

One established J must be selected explicitly for every imported semantic M.
The selection is immutable within the session. Repeating the same choice is
idempotent; a different choice yields `SELECTION_CONFLICT`. Use a new session
to choose differently. Groups and bodies remain semantic M-keyed, so multiple
retained rank variants do not duplicate Lean declarations. Opening or supplying
a body before selection yields `NEEDS_SELECTION`.

Context reconstruction returns missing group/body demands or an untrusted
frontend context, not acceptance. The unchanged ordinary Lean worker elaborates
the local source, and the corrected emitter produces canonical relation rows.
`DeltaSourceOperation` binds the session's exact selection before and after
preparation and completion. The binding includes all packet identities, explicit
warrant selections, selected complete derivations (including ancestors), a
monotone representation revision and semantic data. New acquisitions and changed
choices invalidate a prepared operation; switching choices back cannot revive it.

The new witness uses exactly the selected direct Js and rank
`1 + max(direct parent ranks)` (zero with no parents). The existing mathematical
relation still permits at most one direct J per M and rejects a direct parent
whose M equals the child's M. Supporting variants on different ancestor branches
does not remove these single-witness constraints.

`onward_packet` traverses the selected complete exact-J derivations, prunes stored
records not in that ancestry, emits each original selected witness without
rewriting its parent bytes or rank, and appends the new witness. Its result
is explicitly untrusted. Only a fresh actual `receiver.receive` can admit it.
This path still retains all unsealed ancestor witnesses and has finite caps;
it does not independently solve unbounded proof-history scalability.

## Same J, different proof representation

Distinct ranks have distinct Js and are retained separately. A different issue
is two complete derivations or receipt encodings that establish the *same* J.
Identical form, proof/receipt payload and exact parent list deduplicate. Conflicting
records require an explicit complete-record choice:

```python
session.use_handle(other_accepted_handle, resolutions={
    conflicting_exact_journal: "incoming", # Or "existing".
})
```

The directive keys must equal the exact set of conflicts with this incoming
handle. A missing, extra or malformed directive yields `REPRESENTATION_CONFLICT`.
There is no silent first-proof default and no caller-supplied replacement payload.
One whole already-established record is retained per J. Choosing incoming replaces
the previous complete representation; choosing existing preserves it. Its proof
payload and exact parent list cannot be separated or unioned with another proof.
The original packets stay retained and can be explicitly reacquired within the
same finite budgets to choose another representation later. Repeating a stored
packet does not bypass conflict handling. Even failed calls consume bytes/calls.
State changes are atomic after final liveness checks. Within one received packet
duplicate exact Js are still refused regardless of representation.

Why this is sound: the unchanged child proof cites J, not the parent's derivation
digest. Either complete already-established representation proves exactly that
J, and every chosen native parent has strictly smaller rank. Induction on rank,
with verified receipt records as terminals, therefore justifies the selected
graph. This reasoning never permits replacing J by another same-M/different-rank
journal. Direct M-to-J selection remains immutable; exact-J-to-derivation choice
is separate and invalidates any previously prepared source operation when changed.

`claims.bind_members` is a pure binding helper, not an admission interface.
Synthetic facts can pass it. Only the exact-class live session supplies facts
from the same real receiver, rechecks that inventory, and keeps its authority
alive. Public callers must not treat direct use of this helper as verification.

## Resource accounting and failure meaning

All API calls consume a finite session allowance. Every `use_handle` submission
charges packet bytes before packet/semantic deduplication, including repeat
submissions. Distinct exact warrants consume member storage even if their M is
shared. `census()` distinguishes retained warrants, unique semantic modules,
explicitly selected direct warrants, semantic openings, retained packets,
representation revision, submitted packet bytes and calls. All retained packet
alternatives remain byte-charged even if not chosen for onward emission. These
are capacity diagnostics, not a usefulness or growth metric.

Missing material, conflicting choices, incomplete resources and invalid/unbound
inputs are refusals of this operation, not claims that a theorem is false.
No network access, retries, credential changes or proof campaigns are initiated
by this package. Supervised ordinary-source execution is still not an enforced
hostile-source sandbox.

## Draft controls and remaining qualification

`test_claims.py` uses conspicuously fabricated nonproof journals, empty witnesses
and test-only patched exact-class owners. It tests bookkeeping, identity,
selection and byte preservation only. Even a passing result would establish
zero receipts and zero mathematical admissions. It must not be loaded as
product source or counted as a native/cryptographic correctness test.

Independent source review, root-selected bounded controls and a genuine mixed-
branch native/receipt scenario remain separate steps. No test or runtime result
is claimed by this API document.
