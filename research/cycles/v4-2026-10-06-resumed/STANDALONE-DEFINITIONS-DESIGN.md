# Direct circulation of checked definitions: a substantive missing boundary

2026-10-06. Mechanism source/design investigation under the canonical root.
No code, imports, execution, network action or new source selection. Root owns
any implementation scope. This is higher priority than automatic lambda lifting.

## Decision

Select a narrowly typed **inert definition artifact** lane if integration time
permits. A participant should be able to publish a safe F-closed canonical
definition directly, have another participant discover/acquire its exact capsule,
and use it through the existing definition compiler or `--local-definition`.
No theorem wrapper and no expensive cryptographic certificate are mathematically
necessary. Optional explicit native checking can establish local validity before
publication; recipients never inherit the sender's local check as authority.

The new consequence is real: a reusable function/type can circulate as itself,
before anyone has proved a theorem about it. Today compact agents can construct
such capsules locally, but current network objects are proposition fragments.
This is not a new foundation, inductive feature, recursive named-definition DAG
or general Lean/mathlib compatibility claim.

## What already exists, and what does not

The adopted `project/guest/src/relation.rs` already supports requested
`Role::OutputDefinition`. Its exact checks include safe/nonopaque definition,
canonical content-derived name, F-closed type and value, exact output order,
no output self/cross reference, and genuine `export.check_declar` on the definition.
The typed journal already has `KIND_DEFINITION=2` and an empty required-definition
list for a definition. `native_check.rs` checks the generic adopted relation and
does not restrict its output to Prop. Thus no Rust checker/guest/image change is
required to check a singleton definition packet.

Full installed `prepare --kind definition` already captures and can cryptographically
certify a closed definition. `cert_bundle.py` understands typed definition bundles.
Those paths are not a certificate-free standalone definition circulation API,
and the compact installation does not contain native Lean authoring or a prover.

The concrete current blockers are:

| Source boundary | Existing restriction |
|---|---|
| cert_application.assemble | Requires proposition output and emits final `thm` |
| cert_fragments.bind | Requires proposition capsule/output; selected frontier is Prop only |
| cert_workflow/state validation | Fragment output requires root_kind proposition |
| fragment_index | Discovery namespace, offer.member_kind, type keys and loader are Prop-fragment specific |
| fragment_peer.receive_frame | Exact manifest has input/journal/capsule plus certified parent bundles |
| candidate_terms.from_capsule | Explicitly requires proposition |

The pure definition compiler can already consume exact canonical definition
capsules and emit a new F-closed one. Existing `apply`/`apply-fast` accepts up to
four local-definition capsule files, merges their actual values into the checked
packet, and checks definitions even when used only inside the proof. No sender's
definition-success flag substitutes for that check. These existing endpoints
should be reused, not recreated as another compiler or execution engine.

## Important simplification: the checking frontier is necessarily empty

For a singleton output definition, the adopted relation requires every constant
in its type and value to belong to F. Selected proposition parents must actually
occur in the root proof/value; selected definition parents must be actually used.
Those conditions are incompatible with any nonfoundation selected parent here.
Unused semantic definitions are likewise rejected. The valid standalone case is
therefore precisely **zero selected parents, rank0**, with only the authenticated
foundation and one canonical output definition.

There is no need to invent fake parent receipts or permit an arbitrary nonempty
frontier. The producer's typed body is the mathematical witness of its claimed
type. The native host checker must still check it. This observation removes an
unnecessary certification step; it does not make the body free to obtain/check.

## Proposed minimal artifact contract

Prefer a compact two-leaf object to duplicating the installed foundation witness
in every transmitted definition packet:

`definition.json` — exact canonical current definition capsule, <=4MiB.

`object.json` — small canonical manifest with new definition-artifact schema,
adopted mathematical profile/image/foundation, `kind=definition`, exact canonical
definition ID, and exact definition.json bytes/SHA256. No receipt, assurance flag,
parent list or sender-selected executable is permitted. The object ID hashes a
definition-specific domain plus the complete canonical manifest. Exact type/body
identity remains the existing definition ID, not an author's name or prose label.

Do not change the interpretation of an existing proposition-fragment schema or
advertise this object as a genuine certificate. Existing peers should refuse an
unknown artifact kind/version cleanly. A new catalog/store/protocol version or
kind-separated namespace must bind that distinction. Storage/custody can reuse
the existing bounded immutable-snapshot, framed-transfer, quarantine, complete
hashing and atomic-index machinery; it must not bypass those checks by adding a
raw-file HTTP route. Old successful proposition paths remain intact.

The representation could instead reuse a fresh typed-fragment container carrying
input/journal/capsule, but that sends redundant foundation/packet bytes and widens
the proof-fragment loader/state semantics. It is not the preferred minimal
long-term representation. Root may choose a bounded compatibility successor if
the exact code delta is materially safer; any extra bytes must be reported.

### Local check/pack operation

1. Owner selects exact capsule bytes and adopted profile; inspect canonical
   definition/F-closure/finite syntax and body/type identity with existing codec.
2. A new untrusted pure packet adapter emits the adopted foundation witness and
   exactly one final `def` declaration from that capsule, using the existing
   bounded graph interner. Do not emit an axiom or a tautological theorem. The
   adapter has no compiler/execution authority of its own.
3. Derive header with unchanged relation/image, rank0, one target and parents[].
   Derive the typed expected journal from the exact definition ID/kind2 and packet
   hash, using the existing journal codec. Snapshot and bind all bytes.
4. Invoke the same adopted native executable under the existing finite owner
   containment. Require the complete exact conditional report and exact generated
   journal. Since the frontier is provably empty, no parent-verifier token is
   required. Reject a nonempty header/frontier rather than generalizing this rule.
5. Record a distinct local, nontransferable checked-definition result with native
   executable/input/journal/capsule pins. Export the inert two-leaf artifact. The
   artifact never carries that local marker as proof authority.

Structural packing/publication of unverified candidates can also be allowed,
consistent with current advisory publication, but it must be visibly unverified.
It cannot create an accepted definition record. Every recipient independently
checks before treating a definition as checked; ordinary final `--local-definition`
use already supplies a genuine checking boundary and may avoid a redundant
standalone recheck when no intermediate acceptance is claimed.

### Discovery, custody and reuse

Advisory offers bind artifact kind, definition ID, exact type descriptor/policy,
manifest/frame pins and finite size. Start with exact ID and kind-separated exact
type keys; type-head/argument-head features may be shared only with explicit
definition-kind domain separation and coverage statements. A definition's type
may terminate in a bound variable; current constant-head theorem features can
honestly return unsupported/incomplete instead of pretending completeness.

Metadata never certifies that a body has the type. Acquisition recomputes the
canonical capsule/ID/type descriptor from complete custody and rejects substituted
body/type, wrong policy, added files or stale mismatched rows before commitment.
Return the actual retained `definition.json` path. The existing compiler consumes
that exact path as a selected source; `apply-fast --local-definition` consumes it
as an intrinsic checked definition. No natural-language question or global task
list is required.

Publication alone does not assert that every participant retains or accepts the
object. Existing transfer/custody quotas and durable reservations remain; all
advertisements, new index postings and stored bytes are charged. There is no
ancestral proof tree for an F-closed capsule, but its demanded semantic body can
still be large. Namespace/version migration and mixed-peer refusal must be explicit.

## Narrow qualification with actual consequences

Use a newly selected safe F-closed capsule built by the already adopted compiler,
not a theorem wrapper. Check it as a genuine definition, offer/discover/acquire
it through a real bounded peer path, stop its supplier, and use the acquired
capsule in a new definition composition or checked application. A second receiver
must consume actual acquired bytes, not the producer's original local file.

Necessary negatives: canonical-looking ill-typed body reaches actual checker
refusal; changed body/type or offered ID fails exact rebind; nonempty parent
frontier/rank refuses; wrong policy refuses; truncated/extra payload refuses;
sender local-success metadata never grants recipient acceptance. Counts or a
successful transfer alone do not establish useful growth.

The genuine advance is certificate-free circulation of reusable mathematical
operations/types with unchanged final correctness authority. Its cost advantage
over the present certificate route is a route-level comparison: avoid an otherwise
required successful certificate and its receipt transfer, while paying actual body
transfer, reconstruction and local checking. Do not charge a certificate baseline
if an equally acceptable uncatalogued raw-capsule channel was already in the
baseline endowment. Broad sustained discovery remains the separate uniform-policy
question in GROWTH-UNIFORMITY.md.
