# Tentative v3: how mathematics can be reused without replaying its history

This guide explains the selected scale-first architecture and the actual
restricted v3 implementation. It is not a claim that every layer is already
release-qualified. The dated [02:43 results](RESULTS.md) adopt the actual final
L certificate and installed receiver; the ordinary child's certificate is
still pending. The final dated results, not this
explanation or a successful intermediate checkpoint, determine what passed.
The delivered native v2 remains unchanged.

## The central idea

A theorem is useful to a later mathematician primarily through its exact
statement: knowing `x = y` allows a suitable later proof to use that equality
without rereading every line of its derivation. The network should offer an
analogous machine-checkable interface, without trusting whoever supplied it.

The proposed reusable object has two parts:

- An **interface** says exactly what the result is, including its formal type,
  universe parameters and the meaning of referenced constants.
- A **validity certificate** lets a recipient check evidence for that result
  under an independently adopted foundation and checking policy.

The original proof can remain available for inspection and native rechecking.
It is not a mandatory input to every later use. A new contributor supplies its
own new proof plus certificates for its immediate premises, not the complete
proof archives of all preceding contributors.

This is not “trust a summary.” The certificate must justify the exact summary
the recipient actually uses. Nor is it “trust a popular mathematician.”
Identity, reputation and usage counts do not establish mathematical validity.

## Layer 1: give every formal statement one unambiguous meaning

For an undergraduate analogy, the sentence “f is continuous” has no complete
meaning until we know the spaces, their topologies and what `f` denotes.
Formal interfaces face the same issue, even when their syntax is precise.

The general design therefore binds an interface to an exact foundation,
declaration, ordered universe parameters, type and referenced semantics.
Two contributors cannot silently use the same name for different definitions
and then combine the results as if the meanings agreed.

The current profile takes a deliberately narrower route: it has one fixed,
authenticated support vocabulary, and new theorem interfaces may reference
only that baseline vocabulary in their types. It binds exact structural
names and type hashes; readable names alone are not identities. This avoids
pretending that arbitrary growing Lean environments have already been solved.

There are several different bindings:

| Binding | Question it answers |
|---|---|
| Foundation commitment | Which exact mathematical baseline is being adopted? |
| Interface commitment | Which exact named proposition and universe parameters are certified? |
| Checker image identity | Which exact executable checking program ran? |
| Application journal | Which foundation, interface, rank and new packet commitment did it report? |
| Locally adopted profile | Which installed verifier, data and verification parameters may the recipient use? |

A hash identifies bytes or a committed object; it does not prove that the
object is correct. The receiver adopts its profile independently of the
untrusted sender. A sender cannot choose a permissive checker and make it
trusted merely by providing that checker's hash.

## Layer 2: reuse a theorem through a body-free proposition interface

In Lean, a theorem's statement has a type in `Prop`. A **body-free interface**
retains that exact statement while omitting the old proof term. A local
author can then write a new proof using the named statement as a premise.

The important logical rule is conditional:

```text
The foundation proves each imported statement T_i.
The new proof p checks as U using precisely those compatible T_i.
----------------------------------------------------------------
The realized extension of that foundation proves U.
```

The first line must come from valid certificates or another explicitly adopted
validity basis. Merely adding an axiom-shaped entry to Lean establishes no
such fact. Lean accepting a proof *conditional on that entry* is only the
second line.

The actual ordinary-source experiment demonstrates the second line for a
small but genuine composition:

```lean
theorem CommonsV3.compose_congr
    {alpha : Sort u} {beta : Sort v} {gamma : Sort w}
    (f : alpha -> beta) (g : beta -> gamma)
    {x y : alpha} (e : x = y) : g (f x) = g (f y) :=
  ScaleIface.L g (ScaleIface.L f e)
```

Here L expresses preservation of equality by a function. The exported new
proof really uses L twice. Its packet carries L's exact type, not L's proof.
This conditional native import/export passed its own audit. It does **not**
itself mean either cryptographic certificate has passed; those are separate
gates. The later L and receiver gates have now passed, while the child's final
certificate remains pending in the dated results. The complete scale lane is not yet an installed upgrade to
the native v2 node.

## Layer 3: certify the new check and discharge the old premises

The selected experimental system uses a RISC Zero succinct STARK receipt.
“Succinct” refers to checking a compact certificate of a computation; it
does not imply that producing the certificate is cheap. This path does not
use the SDK's optional Groth16 receipt form.

The producer's intended sequence is:

```text
Exact parent interfaces + their real certificates + new proof
        |
        v
Check the new proof under the fixed supported foundation
and bind each external premise to a parent interface
        |
        v
Prove that computation; discharge every parent assumption
using the corresponding existing certificate
        |
        v
New exact interface + final certificate with no unresolved assumptions
```

The guest records same-image parent assumptions. Recording an assumption is
not the same as discharging it. The producer must compose the genuine parent
receipts into the new certificate, and the final receiver requires full
verification of the successful exact claim with no unresolved assumptions.
An intermediate proof segment or an integrity-only check is not accepted as
a final mathematical certificate.

Each parent also has a strictly smaller unsigned **rank** than its child;
a rank-zero contribution has no parent premises. Rank is a local derivation
measure, not a blockchain height or a global clock. It rules out the intended
circular justification “A relies on B, B relies on A” when applied with the
full certificate rules. It does not, by itself, prove that the cryptographic
recursion scheme is sound.

The actual guest authenticates selected baseline declarations and checks the
new theorem and parent types using an experimental Nanoda checker. It does
not rerun every old proof. Its parent journal/interface matches, foundation,
rank and executable-image bindings all matter: a correct receipt about a
different theorem or checker would not justify the desired interface.

## Layer 4: receive one certified object, not a worldwide ledger

The small receiver takes a bundle containing exactly four files:

| File | Role |
|---|---|
| `bundle.json` | Bounded manifest binding the other files |
| `capsule.json` | Exact named proposition interface |
| `journal.bin` | The 148-byte application claim |
| `receipt.bin` | The actual cryptographic certificate |

It checks the structural bindings and invokes the adopted verifier on the
receipt and exact journal. That command requires no parent proof packet,
ancestor trace, Lean installation or guest-image file. The separate installed
receiver includes its own Python runtime and verifier; it does not include a
complete mathematical database.

Every result need not be ordered relative to every unrelated result. Two
independent valid contributions can coexist. Nodes may exchange exact objects
through available peers and keep different selected collections. Content
commitments and certificate verification protect the objects they actually
receive; they do not require one central server or a global consensus ledger.

Search remains a distinct service. Indexes can help locate useful candidates,
but a misleading index cannot replace their independent validity checks.
An index may miss a result or list an unavailable holder. The current small
receiver is given an exact bundle; it does **not** implement a worldwide
search engine or establish fast semantic search at arbitrary scale.

The right scaling requirement is selective access, not complete awareness.
If the network produces explicit information faster than one node can read
it, that node cannot stay fully synchronized with every statement. Certificates
can authenticate selected summaries; they cannot make reading arbitrary
amounts of information free.

## Layer 5: keep computation and availability honest

Omitting a theorem's proof is not permission to omit every definition's body.
The type `Nat -> Nat` does not tell us whether a function doubles its input
or always returns zero. A computation using that function may need its exact
authenticated definition and reduction rules.

The broader design therefore separates:

- Sealed proposition interfaces used as logical premises.
- Exact definitions or inductive groups needed for selected computations.
- Optional archives used to inspect or natively recheck old proofs.

The current profile supports new theorems over fixed baseline support; it
does not admit arbitrary new definitions or inductive types. General selective
computational-support retrieval remains unfinished. Some Lean checking also
depends on proof-sensitive reduction, so sealing old theorem bodies is not
a guarantee that every existing Lean development behaves unchanged.
Unsupported use must be refused or explicitly moved to a separately costed
transparent/native path, never silently filled with a placeholder.

A valid certificate also does not guarantee future data availability.
Someone must retain and serve the needed interfaces, certificates and any
selected computational bodies. Replication and independent holders can help;
no cryptographic validity rule can recover data after every holder deletes it.
Nodes are not all required to become complete archives.

## Layer 6: distinguish correctness, usable knowledge and useful growth

These questions must remain separate:

| Question | What would justify an answer? |
|---|---|
| Is this result valid under the selected profile? | Exact checking/certificate evidence under explicit assumptions |
| Can this agent use it now? | Compatible exact interface, supported import/computation and available data |
| Can another agent obtain it later? | Actual reachable custody and service, not a validity certificate alone |
| Is it helpful or novel? | Task-relevant comparison, reuse evidence and defensible heuristics |
| Does the software accelerate useful accumulation? | Resource-accounted comparative outcomes over meaningful work |

Agents choose their own investigations. There is no mandatory root goal,
global unsolved-task list or human-intention criterion in mathematical
acceptance. Usage frequency and other fallible signals may help rank results;
they cannot turn an invalid statement into a valid one. Conversely, being
valid does not make a tautology, duplicate or irrelevant result valuable.

The scale argument is an opportunity for faster growth, not its proof: make
earlier results cheap enough to reuse that later work can benefit from them.
A meaningful test must compare the same downstream mathematical task and
count discovery, receiving, import, proof production, failures and retained
resource costs. Counting objects or proof certificates alone is insufficient.

For a simplified break-even calculation in one chosen resource measure, let
`R` be the native cost of one matched consumption, `V` the complete certified
cost of that consumption, `G` the additional certification cost and `F` the
additional provisioning cost. Reuse by `m` consumers saves that resource only
if:

```text
m * (R - V) > G + F
```

This is an accounting model, not measured v3 data. The terms must be measured
under the same task and assurance requirements; CPU, wall time, memory and
bandwidth may yield different conclusions. Recurring contributions require
charging their additional `G` values too. No exponential-growth conclusion
follows from the formula or from recursive certificates.

## What the actual implementation still costs

The source audit found no mandatory input equal to all ancestor proof bytes
`H` or the unrelated corpus `N`. With a fixed profile and downstream task,
the receiver instead depends on its installed baseline, selected interface
and certificate. The producer depends on the new proof, selected support and
immediate parent certificates. This is the essential locality distinction.

It is not a claim of negligible overhead:

- The small receiver's selected assets occupy about 97 MB. Its wrapper hashes
  that entire installed closure twice per successful invocation, in addition
  to checking the selected bundle and receipt.
- The present CPU producer is a resumable research implementation. Every
  segment/lift/join/resolve/finish stage re-executes the new guest computation
  and rechecks direct parents. Each non-capture stage decodes the whole saved
  coherent trace snapshot.
- For `s` new trace segments and `a` actual assumptions, one uninterrupted
  complete schedule performs `3s+a+1` guest executions including capture,
  `3s+a` whole-snapshot decodes and a separate final cold verification.
- The research controller repeatedly hashes its accumulating checkpoints and
  evidence. This can be quadratic in its own stage count. It is not a global
  mathematics scan, but remains chargeable work.
- Failed proof attempts and preparation are retained and counted. Cheap
  receipt checking cannot retroactively erase expensive certification.

The audit establishes the selected source/input boundary, not enforced OS
denial of every ancestor file. The implementation assumes owner-controlled
local files and a functioning supported Windows host. “Cold verification”
means a fresh verifier process without ancestor proof inputs; it does not
mean an independent physical machine or a hostile-host sandbox.

## What must be trusted, and what is not yet established

The selected profile is explicitly experimental. A successful receipt would
establish a claim about the **adopted guest computation**, conditional on the
selected proof system, its parameters and implementations. Moving from that
claim to “this is a theorem of the adopted Lean foundation” additionally needs
faithful encoding/checking, a sound foundation and compatible realization of
the sealed interfaces. The current Nanoda-to-Lean correspondence is not proved
in general. Finite differential and native-source tests are supporting
evidence, not a replacement for that distinction.

Recursive security also needs justification for the actual accepted verifier
profile over many adaptively generated claims. The receiver accepts the SDK's
default allowed recursion-program root, a broader set than the honest
producer's `lift/join/resolve` schedule. An argument about only that schedule
would not cover everything a malicious producer could submit. The audit found
no acceptance shortcut, but does not claim a completed production security
argument or invent a numerical security-bit estimate.

The next central completion criteria are concrete: beyond the now-passed L
certificate and fresh receiver, ordinary downstream contribution with all
premises discharged, an installed usable contribution path, and honest
whole-workflow costs. Broader Lean support and exact assurance remain central
scope limits. Political attribution, a global ledger and extra coordination
mechanisms do not substitute for any of these.

## Evidence and deeper specifications

- [Implemented locality and cost audit](../../research/cycles/v3-2026-09-27/IMPLEMENTED-LOCALITY-AUDIT.md)
- [Exact-profile assurance audit](../../research/cycles/v3-2026-09-27/CERTIFIED-PROFILE-ASSURANCE.md)
- [Scale design and logical import bridge](../../research/cycles/v3-2026-09-27/SCALE-DESIGN.md)
- [Quantitative dataflow contract](../../research/cycles/v3-2026-09-27/SCALE-DATAFLOW.md)
- [Actual conditional ordinary-source outcome](../../experiments/certified-importer-probe-02/OUTCOME.md)
- [Current execution/adoption checkpoint](../../research/NOW.md)

These links separate design, inspected source and actual execution. A later
runtime pass changes the evidence at its stated boundary; it does not silently
remove the restrictions or assumptions explained here.
