# Next core seam: contribute from the context already acquired

2026-10-20, `core_release`. Source-only bottleneck review. Canonical guard,
GOAL/NOW, v5 architecture/release obligations and current source/evidence were
read. No runtime, experiment, RAM investigation, product mutation or Git change.

## Recommendation

**Expose the already implemented contribution suffix as a small ordinary-owner
function that accepts the current live context.** Do not create another discovery
engine, importer, verifier, task language, sealed cache or proof campaign.

Suggested fresh source: `software/v5/examples/contribution.py`, with a synchronous
function (all suffix calls are synchronous):

```python
contribute_from_context(
    client, context, *, source, roots, export_names,
    author_limits, admission_limits,
)
```

This is the minimum missing **public composition** between demand-directed
semantic acquisition and ordinary checked onward contribution. The underlying
mathematical/client capabilities already exist. The gap is not that the system
needs to prescribe when an autonomous agent should search or what it should prove.
Those choices remain local; an owner/agent can call this function whenever it
chooses to continue from a ready context.

## Concrete existing boundary

| Source | Current behavior |
|---|---|
| `examples/contribute.py:113–157` | `_contribute` first calls the one-shot remote reader or bulk local-packet importer; only afterward author/check/publish runs. There is no supported entry accepting the live context the caller already obtained. |
| `client/remote_reader.py:55`, `:116–132` | Searches through explicit direct contacts, acquires/admit the selected packet, extracts bulk packet semantics and imports them. It can return `NEED_SEMANTICS`; it is not the pre-admission SemanticReader path. |
| `client/supplier_resilient/semantic_reader.py:382–437` | `finish` admits each staged packet once and imports explicitly selected members/data. On READY it returns the actual same-client context. No new grant/owner is created. |
| `client/semantic_check.py:198–225` and `client/supplier_selected/split_check.py` | Recent demand-directed actuals demonstrate READY and then close; they do not continue this context into the ordinary contribution example. |
| `client/workspace_atomic.py:649–679` | `_live_context` checks exact token identity/current selection. `author` requires the existing preparation owner, invokes the existing source preparation and returns untrusted mathematical output. |
| `client/runtime.py:183–254` | `open_operation(..., authoring=True)` provisions authoring under the original grant; this must be selected at initial open, not added by reopening after acquisition. |
| `examples/contribute.py:80–87`, `:125–157` | Already contains the exact new-output custody/admission/hash/module checks and ordinary publication policy to reuse. |

Older `actual_owner03.py`/`actual_resume_owner.py` already demonstrate actual
source authoring and onward publication from bulk packet semantics. Therefore
another broad proof-of-authoring campaign would be duplicative. Installed03
already passes relocated advertised synthetic discovery; repeating that loop
would not close this seam either.

The installed SDK contains the semantic reader and required client successors.
Its `run` entry already accepts explicitly selected trusted owner sources. The
new example/helper can initially be an owner-selected source through that entry;
no rebuild of the installation is needed merely to make this composition callable.
The final release can include the approved helper with its ordinary examples.

## Minimal behavior, not a new workflow framework

1. Validate bounded source/names/limits as in the existing contribution example.
   Borrow only the supplied client's own workspace and grant; do not accept a
   replacement owner/workspace, fabricate a context, or load one from JSON.
2. Call `client.author(context, ...)`. This existing call remains the live
   context/selection and preparation-authority gate. A missing semantic demand
   produces a clearly non-contributed outcome, not implicit reacquisition.
3. Require the existing untrusted prepared-packet schema, bytes/hash and module
   bindings. Store the **new output** structurally and call ordinary
   `client.admit_local` for that exact output. Fresh output checking is necessary;
   successful Lean export alone is not admission.
4. Bind the actual returned live fact to the new module, then call
   `client.publish` under the existing quota-bounded local custody policy.
5. Return only a bounded operational outcome with exact output/publication IDs.
   Do not close the borrowed client, renew its grant, perform search, acquire
   old input again, call `import_context` again, or persist context authority.
   The caller retains the existing final cleanup obligation.

Keep `examples/contribute.py` frozen initially. The suffix is small enough to
extract into a fresh owner-facing module; root can select a later wrapper
integration only if it helps avoid divergent copies. No changes to receipt or
native acceptance, packet grammar, index protocol, existing source imports or
global coordination are required.

## Invariant and why it matters

Let an operation be `(client, grant, issuers, context, deadline, remaining)`.
Suppose `SemanticReader.finish` returns a ready context `c` under that operation.
The proposed suffix must preserve client/grant/issuer/deadline identity throughout.
Every side effect must spend the existing allowances; `c` must still satisfy
the original client's exact current selection check when authoring starts.

The causal path is:

```text
selected formal candidate → demanded semantics → live imported context
    → caller-selected Lean extension → untrusted new packet
    → actual new-output admission → ordinary publication/indexing
```

It introduces no implication from structural preview, success JSON, popularity,
or human intention to mathematical truth. The new output's mathematical warrant
still comes from actual admission. Publication only reports local custody/index
completion; it is not global visibility, replication or perpetual availability.

Without this suffix, calling the existing contribution example after READY
starts its input acquisition/import path again. Besides wasting work, the same
client already has an import session, and `workspace_atomic.py:642–647` requires
that session to be absent on `import_context`. Starting another owner would
discard the live authority/context and incur another grant/admission. Direct
manual `client.author` is already a valid alternative; the new seam makes that
cheap composition an ordinary reusable interface, not a new trusted mechanism.

The work is local in the selected context and new contribution; it does not
scan global mathematics. It reduces avoidable orchestration/reacquisition cost
and makes verified reusable methods feed onward checked contributions. It does
**not** resolve economical frontier production or prove net useful growth by
itself. Those remain the dominant separate open obligations; typed producer work
continues in parallel.

## Smallest decisive checks

Source argument first: compare the suffix with the existing author/check/publish
path, and show it calls no opening, discovery, import or old-input admission API.
A few inert controls can cover exact call order, same context/owner/grant use,
new-output hash/module binding, author demand and refusal, output-admission
failure before publication, partial-publication propagation, and caller-owned
cleanup. No byte-count benchmark is needed.

One later bounded real check, if selected, should begin from a genuinely
demand-acquired ready context and call this suffix with a small substantive
extension using its imported result. Show no second input acquisition/import,
one author call, actual new-output admission and exact publication. Reuse the
existing pinned runtime, seed and serving mechanisms. Do not repeat the installed
discovery demonstration or start another succinct proof. A cold return may reuse
existing verification APIs if it tests a genuinely new publication boundary;
it should not become a mandatory replay of every old campaign.

## Deferred alternative, not another assignment

There is also a concrete availability gap: exact dependency-declaration fetches
still fail-stop the live client/helper on ordinary provider disappearance, whereas
body fetches now support settled supplier continuation. The trace is
`supplier_resilient/semantic_reader.py:242` →
`supplier_resilient/workspace_evidence.py:330` →
`transport/clients.py:135`; exceptions reach the existing `_async_action`/`_fail`
and helper `_call` failure transitions. This is worth a later narrow correction,
but it is not selected here. The present higher-payoff decision is completing
ordinary acquisition-to-contribution composition, not adding another supplier
exception variant before the existing successful context can flow onward.
