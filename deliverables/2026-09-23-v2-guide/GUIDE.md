# Understanding the mathematical commons: a layered guide to v2

A guide for undergraduate readers. You need basic ideas about functions,
proofs and files, but no background in Lean, cryptography or blockchains.

This guide describes the **delivered local v2 of 23 September 2026**, whose
frozen implementation is called **source13** in the project records. It is a
separate explanatory companion, not a change to the sealed software package.
The unfinished source14 development work is not part of this version.

The authoritative package and installation instructions are in
[Start here](../2026-09-23-v2-local-release/START-HERE.md). The exact tested
scope is in [Qualification](../2026-09-23-v2-local-release/QUALIFICATION.md).
If you want to operate the software, use those documents alongside this guide.

## How to read this guide

The layers are a learning sequence, not a claim that the program has exactly
these software modules. Security and resource limits affect several layers.

| Layer | Question it answers |
|---|---|
| 0. The big picture | What are we building, and what is v2 today? |
| 1. Participants | What do an agent, a node and an operator each do? |
| 2. Mathematical trust | Why can I rely on somebody else's result? |
| 3. Knowledge objects | What is stored, identified and exchanged? |
| 4. The working loop | How does a result go from private work to checked reuse? |
| 5. A real example | What did the v2 tree-counting test actually demonstrate? |
| 6. Discovery and decentralization | How do nodes find results without one global server? |
| 7. Reliability | What happens when data, software, people or agents go wrong? |
| 8. Growth and usefulness | Does more verified material mean better mathematics? |
| 9. Practical use | What do I need before running v2? |
| 10. Reading the evidence | What is established, and what remains open? |

For a first reading, read Layers 0–5 in order: each introduces ideas used by
the next. For the complete mental model, continue through Layer 8. Read
Layers 9–10 before operating or
evaluating the software. A glossary and short self-check follow the layers.

## Layer 0 — The big picture

### The idea in one paragraph

An agent develops mathematics locally. It can obtain earlier work from other
participants, check that work on its own machine, use it in a new construction
or proof, and make the new result available for others to check and reuse.
Nobody has to trust the author's reputation as a substitute for checking the
mathematics. Nobody has to receive a centrally assigned research problem.

The central loop is:

**discover → obtain → check locally → use → contribute → check again elsewhere.**

The important word is **use**. Passing around files is not enough. A receiver
must be able to build on their mathematical contents.

### A useful analogy, with a limit

Think of a shared library whose books include machine-checkable proofs.
Each participant keeps a working collection, can obtain more books from peers,
and verifies selected books before relying on them.

Unlike an ordinary library, two books with similar titles cannot silently
substitute for one another: formal references identify exact mathematical
objects. And unlike a perfect imaginary library, v2 does not know where every
book is, keep every book forever, or decide which books are important.

### The vision is larger than the current software

The long-term aim is a decentralized mathematical commons that supports
reliable, useful accumulation by many diverse participants.

V2 is a bounded, working part of that vision: a Windows-based framework with
Lean checking, local storage and discovery, peer exchange, and contribution
APIs—defined software operations that an agent can call. It is **not** a
download containing all mathematics. It is **not** a
bundled AI mathematician that automatically discovers important theorems. Its
release test used two nodes on one physical machine, not a worldwide network.

### Keep these six questions separate

| Question | Example of an answer | What that answer does not establish |
|---|---|---|
| Is it proved? | A receiving node checks the proof under its selected foundation. | That the theorem is important. |
| Which object is it? | Its content identifier matches the received encoding. | That the object is a valid proof. |
| How do I find it? | A catalog or local index returns a candidate. | That every relevant result was found. |
| How do I receive it? | A peer supplies the selected package. | That the receiver has accepted it. |
| Who keeps it available? | A participant retains and serves a copy. | That a copy will remain online forever. |
| Is it useful? | An agent can use it to accomplish further mathematical work. | That the system has a universal usefulness score. |

Much of the design is about answering each question with the right mechanism,
rather than treating one successful check as an answer to all six.

## Layer 1 — Participants: agent, node and operator

These are roles, not necessarily three different people or machines.

An **agent** chooses mathematical work. It might be a human using Lean, an
LLM-based program (using a large language model), or another program. It
searches, reads interfaces, writes
definitions and proofs, and decides what to attempt next.

A **node** is the local software that stores packages, checks supported
contributions, maintains catalogs and handles permitted peer operations. The
node applies rules; it does not need to understand the agent's motivation.

An **operator**, or owner, controls the node's machine, configuration, resources,
authorized peer contacts and network serving. Ordinary agent operations do
not automatically grant more resources or start a permanent server.

For example, a university group could operate a node, while several programs
use its permitted local interfaces. This is a possible role arrangement, not
a claim that v2 has been tested as an adversarial multi-user hosting service.

### Where does human intention belong?

It can influence what a local agent chooses to investigate. It is not an
acceptance condition in the mathematical core.

The node does not ask, “Did this formal statement express the human's intended
question?” It checks the submitted formal work within its supported rules.
A valid proof of a different statement remains a proof of that different
statement. It does not thereby answer the original question.

There is no required natural-language-to-formal-mathematics interface in v2,
no mandatory root research goal, and no global list of unsolved tasks.

## Layer 2 — Mathematical trust: checking instead of reputation

### Statements and proofs are different objects

Consider the statement, “For every natural number n, n + 0 = n.” Writing the
statement down is not proving it.

Lean is a formal proof system. In its logical framework, a theorem's statement
can be represented as a type, and a proof is a term checked to have that type.
You do not need to master dependent type theory to understand the key idea:
the checker examines a precise justification, not just a confident sentence.

A definition can also be valuable without being a theorem: for example, a new
kind of tree or a function that counts its nodes. V2 supports selected
definitions, theorem proofs and inductive groups as mathematical contributions.
Defining a proposition is still not proving that proposition.

### Proof construction can be complicated; final checking is a separate job

An LLM may propose a bad proof. A human may misremember a lemma. A tactic—a
proof-building program—may fail. These are expected possibilities.

The intended boundary is that a successful proposal alone does not become
accepted mathematics. The supported contribution must survive the actual
checking pipeline. A receiver performs its own fresh check rather than
inheriting the sender's claim of acceptance.

### The foundation matters

A **foundation** here is the selected formal starting point: the logical
basis and precisely identified foundational declarations used for checking.
Results are not interpreted independently of that starting point.

A compact mathematical model is:

`F; Γ ⊢ p : P`

Read this as: “Under foundation F and the selected context Γ, p is a checked
proof of proposition P.” The symbol Γ—Greek gamma—stands for the relevant
available declarations and assumptions.

This is a model for understanding the trust claim, not an executable API or
a claim that the entire software stack has been formally verified.

The guarantee is conditional on the soundness of the selected foundation,
the Lean **kernel**—its core proof/type checker—and the correctness/integrity
of the relevant implementation,
runtime and operating environment. V2 does not prove its own foundation
consistent, nor is it protected against an operator replacing the checker
with malicious code.

### Why doesn't a malicious author just add an axiom?

Allowing arbitrary new axioms would let an author assume the desired answer.
That would not meet the intended contribution policy. The selected source
capture has restrictions on new external axioms and other unsupported
constructions; it is not a general permission to import any Lean environment.

Nevertheless, “valid under an explicit assumption” and “unconditionally true”
remain different claims. Readers must examine the actual theorem and its
foundation, not only its friendly name.

### What is not a proof check?

A matching hash, a trusted network connection, a popular author, a catalog
listing, a download, or a successful program exit code is not by itself a
mathematical acceptance result. Each serves a different purpose.

## Layer 3 — Knowledge objects: exact contents and dependencies

### Why a theorem needs more than its printed statement

Suppose a proof uses a function named `combine`. To check the proof, a receiver
needs to know which `combine` it uses. Two authors might use that name for
different functions.

The receiver therefore needs precise definitions, proof dependencies and
formal references, not just text that happens to look familiar.

A **dependency closure** is the selected object together with the prerequisites
needed to reconstruct and check it, relative to the configured foundation.
This does not mean downloading every theorem anyone has ever produced.

### Packages and canonical objects

The exchange format represents mathematics as structured data with precisely
specified encodings. A **canonical encoding** is a prescribed representation
that removes specified representational ambiguity. Canonical does not mean
“the unique encoding of every mathematically equivalent statement.”

A package contains a manifest—the package's contents list—and the selected
canonical objects and supporting data. Packages refer to dependencies by
exact references. A formula can be stored as a directed acyclic graph, or
**DAG**: a graph with no directed cycles, where repeated pieces can be shared.

For example, a large expression using the same subexpression twice can point
to one stored representation of that subexpression. Sharing representation
does not change the mathematical meaning or authorize skipping proof checks.

### Content identifiers are fingerprints, not certificates

A **content identifier**, or CID, identifies a particular typed canonical
object using its encoding and a cryptographic hash. V2 uses SHA-256 in its
content and file integrity machinery.

A hash is like a compact fingerprint of bytes. Under the relevant collision-
resistance assumption, it is practical to detect whether the identified bytes
have changed. The hash does not tell you whether those bytes form a correct
proof, who deserves credit, or whether they are useful.

Three distinctions are crucial:

- Same exact content identity is not the same claim as mathematical equivalence.
- Different content identities do not prove mathematical novelty.
- A sender's name or local file name is not the authority for a formal object.

V2 does not solve general theorem equivalence or remove all redundant
mathematics. Exact-content handling is a narrower, useful mechanism.

### Local handles are not content identifiers

An API may return a `candidate`, `artifact`, `context`, `snapshot` or `remote`
handle. Think of these as tickets issued by a particular node for particular
operations. They are not interchangeable with globally comparable object
identifiers, and are not transferable between nodes merely by copying strings.

Use the complete handles returned by the relevant node and client. Do not
invent one from a theorem name or reconstruct it by splitting a printed name.

### The name you type and the identity you rely on

After admission, the node supplies checked receiving names and types. An agent
uses the returned Lean spelling when writing new source. The precise canonical
reference and checked type remain the mathematical authority.

This is like importing a library through a documented interface: you need the
actual function signatures. Guessing the name or arguments of an unfamiliar
recursor is not a reliable substitute.

## Layer 4 — The working loop: distinct milestones

### The two pieces of local state beginners often confuse

A **context** records the selected mathematical environment available for
subsequent local work. A successful fresh `admit` advances that context.

A **P1 snapshot** identifies a particular recorded version of the node's local candidate
catalog. “P1” is the implementation's local provider/catalog label, not a
central global service. Publication and peer acquisition can update this
catalog without advancing the mathematical context.

A peer's returned catalog snapshot is another distinct kind of handle. Do not
use a remote pagination snapshot where a local publication snapshot is required.

### What the operations actually mean

The table uses API operation names. The command-line helper uses hyphens for
some names: for example, `peer-find` builds a `peer_find` request.
Later in this guide, **native checking** means checking through the actual
selected Lean runtime, not a simulated checker or a catalog lookup.

| Operation | What has happened on success | What has not happened merely from this operation |
|---|---|---|
| `peer_find` | A selected peer's catalog page was obtained. | Its results have not become trusted mathematics. |
| `peer_acquire` | A selected package was received and registered as a local candidate, with acquisition/custody information. | The receiving context has not advanced; fresh Lean admission has not happened. |
| `admit` | Selected candidates and their dependency union were freshly checked; on `accepted:true`, the context advances. | The receiver has not proved every item in the network. |
| `submit` | Locally authorized source passed the contribution pipeline and produced a private checked artifact. | It has neither been published nor added to the current context by this operation. |
| `publish` | The artifact was reauthenticated and registered as a local publication/candidate at the current catalog snapshot. | Other nodes have not accepted it; no network service was automatically started. |
| `expose` | An immutable sharing view was prepared from selected publications and, optionally, custody acquisitions. | The owner has not automatically started or funded serving. |
| Owner `host` / `serve` | A separately authorized finite service can supply the selected view. | Availability is not promised forever, and serving is not proof checking. |

An immutable view is a fixed selection for sharing, not a live view of all
future work. If the selection changes, callers must follow the documented
new-view and snapshot rules.

### A complete two-participant story

1. Alice's agent defines a mathematical object and submits it to Alice's node.
2. Alice's node returns a checked artifact. Alice explicitly publishes it.
3. Alice prepares a sharing view, and the operator runs a finite service.
4. Bob's agent discovers the offered result and acquires its package.
5. Bob's node freshly admits it. Only now does Bob have the checked receiving
   interface to use in this workflow.
6. Bob's agent uses that interface to author a new result. Bob submits,
   publishes and exposes the new result. Bob's operator separately starts an
   authorized finite service for that view.
7. Alice acquires Bob's package and freshly admits it in turn.

These are participant names for explanation. The actual v2 evidence uses
nodes A and B, and was a disclosed engineering exercise rather than a blinded
trial of two autonomous AI researchers.

### What happens inside submission?

At a high level, the pipeline connects ordinary Lean source to portable,
checkable data:

1. Elaborate the authorized source: turn its syntax into precise declarations.
2. Capture the selected declaration and needed dependencies.
3. Encode them as canonical objects and reconstruct/check them in a fresh
   native checking path.
4. Export the reconstructed result back to canonical data—the inverse check.
5. Reconstruct/check that inverse result again and compare required identities.

This is more than asking whether a `.lean` file compiled in some unrelated
environment. It checks the connection between the submitted source, exported
data and the mathematics the receiver can reconstruct.

The details and supported fragments matter; this is not arbitrary Lean project
interoperability. A successful support-library build is also not a theorem
acceptance result.

## Layer 5 — The real v2 example: sharing a tree, then counting its nodes

### First understand the tree

The example uses a **Rose tree**: every node contains a finite ordered list of
child trees. The number of children may vary.

The original datatype declaration was:

```lean
inductive Rose where
  | node : List Rose → Rose
```

This small declaration describes the mathematical shape. It is not a complete
copy-and-run script for authoring against a receiving node: the actual consumer
uses the exact names returned by admission.

The word **inductive** means that objects are built by specified constructors.
Here there is one constructor, `node`. A leaf is `node []`: a node whose child
list is empty. There is no separate empty-tree constructor.

Some small examples, using short teaching names:

```text
leaf       = node []                 one node
chain      = node [leaf]             two nodes
twoLeaves  = node [leaf, leaf]       three nodes
```

### What is a recursor?

A **recursor** is the formal rule supplied with an inductive datatype for
defining or proving things by its construction. For a tree, it lets you say
what to do at a node after obtaining the required results for its children.

Here a node contains a `List Rose`. Recursion must therefore handle both a
tree and a list of trees. The checked group exposes a main recursor and a
corresponding auxiliary recursor for the nested list part. “Auxiliary” means
supporting machinery for the construction, not an unproved extra axiom.

An **inductive group** is the related collection of declarations that must be
handled together—for example, the datatype, its constructor and generated
recursion rules. V2 can publish the selected group itself; it need not wrap
the datatype in a dummy theorem merely to share it.

### Bob's two counting functions

The actual consumer defines `nodeCount` for a tree and `forestCount` for a
list of trees—a forest. Their mathematical behavior can be understood through
these equations:

```text
nodeCount(node children) = 1 + forestCount(children)
forestCount([])          = 0
forestCount(t :: rest)   = nodeCount(t) + forestCount(rest)
```

Here `t :: rest` means a list with first element `t` and remaining list `rest`.
These are explanatory equations, not the exact submitted program. The tested
source defines the functions using the received main and auxiliary recursors.

Consequently, `nodeCount(leaf) = 1`, `nodeCount(chain) = 2`, and
`forestCount([leaf, chain]) = 3`. These examples help us read the definitions;
they are not a substitute for the general proof.

### What theorem was actually returned?

For every received Rose tree `t`, the result proves both:

```text
forestCount([t])     = nodeCount(t)
nodeCount(node [t])  = 1 + nodeCount(t)
```

In words: counting a one-tree forest gives the tree's count; placing one new
node above a tree adds one node.

The proof combines two reflexivity proofs, written using `And.intro` and
`Eq.refl`. Reflexivity means an expression equals itself. This works here
because, after the relevant definitions compute, the two sides coincide.
This is **definitional equality**, not an assumption that all expressions with
similar printed forms are equal.

Here are the computations in teaching notation; each arrow means “reduce
using the definitions,” not “assume a new fact”:

```text
forestCount([t])
  → nodeCount(t) + 0
  → nodeCount(t)

nodeCount(node [t])
  → 1 + forestCount([t])
  → 1 + nodeCount(t)
```

The proof is general in `t`; it is not a test of a few particular trees. It is
also a straightforward computation theorem, not a newly discovered deep result.

### Why is this still a meaningful software test?

The question is whether Bob can genuinely use Alice's mathematical vocabulary.
The outcome audit verified that:

- The original Rose group was retained exactly, not replaced by a look-alike.
- The returned theorem's statement referred to both counting definitions.
- The actual proof/value dependencies reached both received recursors, not
  merely mentions in comments or type annotations.
- The canonical representation matched the actual submitted type and proof.
- Alice received the exact contribution and freshly checked it after Bob's
  service had stopped.

It tests a critical building block for collaboration: one participant's
datatype can become another participant's usable mathematical infrastructure.
It does not, by itself, demonstrate mathematical novelty, broad library
compatibility or a high rate of useful discovery.

### What did the final v2 repair change?

Lean's proof checker and its source-language frontend do different jobs. The
checker validates precise internal objects; the frontend resolves the names
and notation an author writes into those objects.

In the preceding source12 version, the received auxiliary recursor existed in
the checked environment, but ordinary submitted source could not refer to it
by its advertised name. Imagine a library function that is present but missing
from the interface your program can import. The mathematics was available to
the checker but not usable through that authoring path.

Source13 repaired that visibility connection for the already-checked binding.
It did not add an axiom or relax the mathematical rules. The returned counting
proof demonstrates that ordinary source can now use both checked recursors
through the repaired path. This is the central final repair in delivered v2.

### The subtle failure that v2 still documents

The original counting theorem passed source/canonical/native checking. Its
publication then failed because the public type index did not accept the
literal node representing `1` in the theorem's formal type.

For the successful continuation, the theorem statement used `Nat.succ Nat.zero`
instead. `Nat.zero` is zero, and `Nat.succ` is successor, so this is another
way to express one. The count definitions and proof were unchanged.

The revised source was freshly checked, published and returned. The original
failed publication stayed failed and recorded. The revised exact encoding had
a different identity, even though the mathematical equation was definitionally
equivalent.

**V2 does not automatically make this transformation.** Its public type index
supports variables, sorts, constants, application, lambda and Pi nodes. In
plain language, these cover basic formal references, functions, function
application and quantified/function types. Literal, let and projection nodes
in a public type remain outside that index fragment.

This restriction concerns the elaborated **formal type**, not a rule that the
character `1` is forbidden everywhere in a source file. The actual count
definition bodies still contain literals. Other native/source restrictions
also exist: in particular, v2 does not support new external string literals
through its ordinary source capture. No general rewrite workaround is promised.

## Layer 6 — Discovery, storage and decentralization

### Does somebody keep one complete ledger of all mathematics?

No complete global ledger is required by this v2 design, and none is supplied
by this release. A node keeps its local packages, catalog entries, accepted
contexts and operational records.

Operational records help answer questions such as “Was this request already
processed?” and “How much capacity has been consumed?” They are not a globally
replicated blockchain of every theorem.

The system can exchange selected mathematical packages without imposing one
network-wide order on all research. Local request ordering still matters for
updating local state and accounting safely.

### An index is a finding aid, not the knowledge itself

An index maps a search condition to candidate entries. The proofs and
definitions live in packages; the index helps choose what to inspect or obtain.

V2 has two main discovery routes:

- **Local `find`:** enumerate the node's candidate catalog, optionally filtering
  by one exact formal reference occurring in an entry's type.
- **Remote `peer_find`:** obtain bounded, unfiltered catalog pages from an
  owner-approved peer.

Exact type-symbol search resembles looking up which library declarations
mention a particular precise identifier. It is not asking an LLM, “Find
anything relevant to topology.” It does not search proof bodies for arbitrary
meaning, establish theorem equivalence, or find every theorem obtainable by
unfolding definitions.

For a directly published inductive group, the catalog indexes the **first
original type**, not every constructor, recursor or other group member.
Fresh admission supplies the checked member interfaces for use. The group's
searchable catalog entry and its full receiving interface are different things.

The caller handles pagination: retain the relevant snapshot and cursor—the
continuation handle—and request the next page under the same rules. A completed
page sequence refers to that selected catalog snapshot, not all mathematics.

### Does everybody immediately learn every new result?

No. Different nodes can know about different results. Peers can be offline,
and a catalog snapshot can be older than a peer's later work.

V2 has no globally current dashboard or guarantee that every contribution
eventually reaches everyone. Its concrete mechanism is explicit bounded
discovery and acquisition from configured peers. A finite node also does not
load the entire known corpus into every proof context.

This separates two requirements:

- A selected received result must be checked before reliance.
- A relevant result must be discoverable and available if an agent is to use it.

Good checking does not solve discovery completeness or availability.

### Who keeps the packages available?

A participant may retain a received package and offer it again. The project
calls this **custody**. Holding a copy is useful even when the holder proves
no new theorem.

V2 distinguishes sharing one's own published contribution from sharing a
package acquired from elsewhere. Custody-only and mixed sharing views are
supported. A holder does not claim a new theorem or lend its own acceptance
to the next receiver; that receiver still performs fresh admission.

The analogy is a library keeping another publisher's book in circulation.
The limitation is that retention and serving consume finite resources. A view
alone does not start a server or guarantee future availability. If every
usable copy of needed data disappears, a content identifier cannot recreate it.

### Why no blockchain consensus for truth?

In this design, mathematical acceptance comes from local proof checking under
the selected foundation, not from a vote about a transaction history. A node
does not need a majority's approval to check a received proof.

That does not prove consensus mechanisms are useless for every possible future
application. They might address other shared-state problems. They are simply
not part of v2's mechanism for establishing mathematical correctness.

Likewise, v2 uses no SNARK-based shortcut for checking. A SNARK is a kind of
succinct cryptographic proof of a specified computation; introducing one would
require its own verified connection to the relevant mathematical checker and
its own trust/resource analysis.

## Layer 7 — Reliability: different failures need different defenses

### A threat-and-response map

| What can go wrong? | What the selected design uses | Important limit |
|---|---|---|
| Bytes are changed or a dependency is substituted. | Content commitments, manifests, exact references and package validation. | Hash equality alone does not prove mathematical correctness. |
| A peer supplies an invalid proof. | Fresh local native admission before relying on it. | Assurance depends on the foundation/checker and supported policy. |
| A connection reaches the wrong configured endpoint. | The tested peer profile uses pinned TLS 1.3: the expected certificate is checked. | An authenticated peer can still supply bad mathematics. |
| Work consumes excessive time, memory or output. | Finite operation/stage/service budgets and process supervision. | Not unlimited availability or protection from a hostile local owner. |
| A reply is lost or an operation is interrupted. | Exact request records, accounting, and documented narrow recovery rules. | Do not assume a blind retry is harmless or that every failure rolled back. |
| A supplier goes offline. | Already acquired packages may be checked locally or retained and served by another holder. | Somebody must actually retain and serve the needed bytes. |

### “Untrusted peer” does not mean “nothing is trusted”

Peers supply bounded inert package data, not permission to run their source
programs or choose the local checking configuration. That is an important
boundary, but it does not make parsers or the operating system infallible.

Locally submitted Lean source is different: it is owner-authorized executable
input. V2 is not a hostile-code sandbox for arbitrary strangers' Lean programs.
The local operator, relevant installed code, runtimes and OS remain part of
the trust assumptions.

Political attribution can remain secondary while operational identity matters:
the owner must control who configures resources and which endpoint a connection
is intended to reach. These identities authorize operations; they do not
replace proof checking.

### Resource accounting is part of correctness in operation

A **request** is an ordinary API operation. A **native stage** is a separately
budgeted unit of checking work and may contain several subprocess commands.
Not every request runs a native stage. Downloading a candidate is not the same
expense or claim as freshly checking it.

The system also tracks conservative reserved-byte charges. These are accounting
quantities, not a statement that the OS has physically set aside that much disk
space or that the current files occupy exactly that amount.

The final v2 test nodes illustrate why the distinctions matter:

| Node | Used requests / native stages / charged MiB | Remaining requests / native stages / authorized MiB |
|---|---|---|
| A | 7 / 3 / 568 | 5 / 1 / 456 |
| B | 9 / 4 / 712 | 3 / 0 / 312 |

MiB means 1,048,576 bytes. Both nodes began with authorization for 12 requests,
4 stages and 1,024 MiB. B still had request credit and byte allowance, but no
native-stage credit: more native work required deliberate owner renewal.

These are the consumed allocations of the **retained test nodes**, not the
universal starting capacities of every new installation. Renewing authorization
does not erase prior work or failures.

### A safe response to an unclear outcome

Preserve the request, reply, state and scratch evidence. Inspect the documented
status and recovery path. Do not edit counters, delete journals, silently
replace a used installation, or invent a new request ID just because the last
reply was uncertain.

Historical replay of an identical request can return recorded information;
that is not the same thing as fresh mathematical checking. General power-loss,
corruption, backup/restore and migration recovery are not established by v2's
narrow successful recovery tests.

## Layer 8 — Growth: validity is necessary, usefulness is a further question

A commons that accepts false proofs is unreliable. But a commons filled with
millions of unhelpful repetitions would not achieve the project's purpose
either. These are different failure modes.

It is useful to distinguish three levels:

1. **Valid material:** the supported formal object passes its checking rules.
2. **New representation:** its exact encoded identity differs from stored
   objects. This is not sufficient evidence of new mathematics.
3. **Useful contribution:** another agent can use it to accomplish valuable
   further work at an acceptable total cost.

V2 implements parts of the path from valid material to downstream reuse. It
does not implement a universal decision procedure for mathematical importance,
semantic novelty, or the best next research question.

For instance, how often later agents use a theorem could inform a future local
ranking policy. But raw usage counts can reflect duplication, automatic loops,
popularity or manipulation. Such a heuristic would need evaluation; it would
not be allowed to turn an invalid proof into a valid one. This is a possible
future policy, not an implemented v2 guarantee.

Similarly, an LLM can help a local agent select or construct mathematics. Its
confidence score is not a substitute for checking. Continual LLM training is
not the authoritative store of v2's proofs, and retraining on every network
contribution is not required by the protocol.

### What would convince us that accumulation is efficient?

We would want workloads where agents actually need earlier work, comparisons
with a reasonable local-library baseline, measured discovery/checking/storage/
serving costs, and successful further contributions over time. Merely counting
files, downloads, distinct hashes or passed toy examples would not suffice.

Exponential useful growth is a research aspiration, not an established outcome
of this release. V2 should be understood as a tested contribution/reuse
infrastructure with significant coverage and scale questions still open.

## Layer 9 — Practical use: an orientation before installation

### First choose the right artifact

Use the archive named `math-commons-source.zip` in the
[sealed v2 release](../2026-09-23-v2-local-release/START-HERE.md), together with
its manifest, qualification report and integrity record. Do not choose a
development directory just because its number is larger.

The archive contains 114 source payloads plus an embedded manifest. It does
not include Lean, Python, prebuilt support libraries, initialized nodes,
private keys, or a finished corpus of mathematics. Historical “v1 development”
wording in packaged documents does not select another release: the dated v2
manifest and companion qualification identify the exact delivered source13.

### Prerequisites

The qualified environment is Windows x64, PowerShell 7, fixed local NTFS
directories and cooperative owner control. Supply the complete Lean 4.34.0
Windows runtime and the qualified Python 3.14.6 distribution with SQLite
3.50.4, OpenSSL 3.5.7, TLS 1.3 and ALPN support. An arbitrary installation with
a similar version number is not automatically the qualified environment.

ALPN is the TLS mechanism used to agree which application protocol the
connection will carry. NTFS is the Windows filesystem used by this profile.

The default node requires a free-space sample of at least 5 GiB + 64 MiB,
excluding additional runtime, build and second-node needs. This is a check
of observed free space, not an OS reservation. Use fresh nonoverlapping
installation, node-state and scratch paths; do not upgrade a used node in place.

### The installation milestones, in order

Follow the exact commands in the release's startup page and extracted
`TLS-WALKTHROUGH.md`. This guide explains their meaning rather than introducing
a second competing installer.

1. **Verify and extract.** Check the exact archive/manifest identities and all
   payloads into a fresh installation.
2. **Build support once.** Compile the native support with the specified
   runtimes. A successful build means support code built, not that a theorem
   was checked. Do not run both alternative build snippets in the guides.
3. **Provision and configure.** Choose separate node domains, private owner
   identity material, peer certificate pins and finite limits. A configured
   node is not yet an initialized mathematical node.
4. **Initialize.** Require the actual documented success and acceptance fields
   for the bootstrap, not merely a configuration message.
5. **Give an agent its interface.** Supply its client label, current context,
   local P1 snapshot, approved peer aliases, API/agent documentation, and the
   v2 publication-fragment warning in the startup page.
6. **Operate deliberately.** Build a request, send it, inspect its reply,
   retain returned handles, and decide the next action.

The CLI—command-line interface—is how these tools are invoked from a terminal.
The API is the operation/argument contract that those commands implement.

### Creating a request is not sending it

`make_request.py` writes one request file. `manage.py request` sends that
saved request to the local node. The helper does not research, prove, publish,
retry, renew resources or start hosting on the agent's behalf.

Here is a template for an **already configured and initialized** node. It is
not an installer or a demonstration that has been executed for this guide.
Replace every path and handle using your actual deployment. Use a fresh
request ID and output path for a deliberately new request—not as an automatic
retry of an uncertain one.

```powershell
# Example paths only; these directories must already be correctly configured.
$Py = 'D:\Python314\python.exe'
$Install = 'E:\MathCommonsDemo\install'
$Config = 'E:\MathCommonsDemo\node-a\config.json'
$Request = 'E:\MathCommonsDemo\requests\find-001.json'

# Inspect existing state/capacity. This is not a fresh proof check.
& $Py -B -E -s -S "$Install\manage.py" status --config $Config

# Create one local-catalog query file; no request has been sent yet.
& $Py -B -E -s -S "$Install\make_request.py" find `
    --client local --request-id find-001 `
    --snapshot 'OWN_CURRENT_P1_SNAPSHOT' --output $Request

# Send exactly that file once and inspect the structured reply.
& $Py -B -E -s -S "$Install\manage.py" request `
    --config $Config --request $Request
```

The Python flags are part of the supported invocation: they suppress bytecode
writing and selected environment/site customization. They are not a security
sandbox. `status` does not consume an ordinary request or stage credit, but
does write administrative evidence in scratch. The sent `find` is an ordinary
operation. Owner status and ordinary `info` are not the same free operation.

After a successful query, a returned candidate still needs `admit` before
this workflow relies on it. After `submit`, retain the private artifact and
explicitly `publish` if desired. After `expose`, arrange separate owner-funded
serving. Always use the actual structured reply; exit code zero alone is not
enough to interpret the result.

### Files to read next

Use the copies extracted from your verified archive when operating a node.
These links point to the same frozen source13 documents in this project for
convenient reading:

- [AGENT-QUICKSTART.md](../../product-local/auxiliary-frontend-source-13/AGENT-QUICKSTART.md): request creation, sending and agent operations.
- [API.md](../../product-local/auxiliary-frontend-source-13/API.md): exact arguments, replies and limits.
- [TLS-WALKTHROUGH.md](../../product-local/auxiliary-frontend-source-13/TLS-WALKTHROUGH.md): complete operator sequence; apply the v2 startup page's path/build clarifications.
- [RECOVERY.md](../../product-local/auxiliary-frontend-source-13/RECOVERY.md): supported handling of interrupted or uncertain operations.

License selection remains undecided. Neither this guide nor the local package
asserts permission for public redistribution or external deployment.

## Layer 10 — What the v2 evidence establishes

### The central observed result

On two nodes on the same machine, the selected source13 workflow exchanged a
Rose datatype, used its checked recursion interfaces in new definitions,
published the revised counting theorem, transferred it back, and freshly
admitted it after the supplying service stopped.

Independent outcome review checked the actual source, canonical objects,
native outputs, transferred package identity, proof dependencies, resource
accounting and shutdown. A separate document review and final delivery
integrity check completed the local release handoff.

The original source13 exercise plus continuation used 16 attempted ordinary
requests: 15 succeeded and one publication was refused. There were seven
native stages. Including source13 preparation and the retained failed
publication, measured Job CPU was about **628 seconds**.

CPU time is processor work, not the same as elapsed time on a clock. These
measurements do not include every model, controller or audit cost, and are not
a general cost per theorem or a whole-agent speedup result. The final
continuation alone took about 189 seconds of elapsed time.

### What remains outside that conclusion?

| Established at the stated scope | Not established by it |
|---|---|
| This genuine recursive-type reuse and return path works. | Every Lean construct or arbitrary mathlib project works. |
| Exact received results survive fresh local checking. | The entire operating system or application is formally proved secure. |
| Selected peer exchange and finite serving work locally. | Independently operated Internet hosts, global completeness or permanent availability. |
| The revised theorem can be published in v2. | The original literal-bearing type is now supported automatically. |
| Package/build and final file integrity were checked. | A clean-machine installer, bundled runtimes or in-place state migration exists. |
| A concrete engineering contribution/reuse cycle succeeded. | Autonomous agents consistently discover valuable new mathematics or achieve exponential growth. |

The implementation also has explicit finite bounds, including at most 16
packages in a context (five are common packages), at most four selected
candidates per admission, and a 256-reference cap on checked descriptions.
These are real limits, not estimates of how large a worldwide commons could be.

Earlier component, contact, custody and recovery evidence is retained and
reused for unchanged code where justified. Not every historical test campaign
was rerun on source13. Detailed qualification states those scopes separately.

### How to read a PASS responsibly

Ask three questions: **Which exact bytes? Which behavior? Under which
assumptions and limits?** A PASS for a build is not a PASS for theorem
acceptance; a PASS for a local exchange is not a proof of global scalability.

Old failed runs remain in the evidence. A later successful continuation does
not rewrite them, refund their consumed work or prove that no other failure
mode remains.

## Short glossary

| Term | Meaning in this guide |
|---|---|
| Agent | A local researcher or program deciding what mathematical work to do. |
| Node | Software storing, checking and exchanging selected mathematical objects. |
| Operator | Owner controlling node configuration, resources and serving. |
| Foundation | Precisely selected formal starting basis for checking. |
| Kernel | Lean's trusted core proof/type checker. |
| Elaboration | Turning surface Lean syntax into precise formal declarations. |
| Canonical encoding | The prescribed exact representation of an object. |
| CID | Content identifier for an exact typed canonical object. |
| Manifest | Contents and integrity information for a package or distribution. |
| Dependency closure | The selected object and prerequisites needed for reconstruction/checking. |
| DAG | Directed acyclic graph; permits shared expression substructure. |
| Context | The selected local mathematical environment available for later work. |
| Candidate | Offered material that is not accepted merely because it was listed or acquired. |
| Artifact | In this API, the private checked result of successful submission. |
| Snapshot | A handle for a specific catalog cut, not universal current knowledge. |
| Cursor | A continuation handle for a particular paginated query. |
| View | A fixed selection prepared for sharing. |
| Custody | Retaining acquired data and offering it onward without claiming a new theorem. |
| Recursor | The formal recursion/elimination rule associated with an inductive datatype. |
| Native stage | A budgeted checking unit using the selected native runtime, possibly with multiple commands. |
| TLS pin | The exact expected endpoint certificate identity for a configured connection. |

## Check your understanding

Try answering before reading the short answers below.

1. A trusted university peer sends a package with a matching hash. May your
   node skip fresh mathematical admission because the source is reputable?
2. A source submission succeeds but publication fails. Is that necessarily
   evidence that the theorem is false?
3. If two objects have different content identifiers, have we discovered two
   mathematically different theorems?
4. Bob has downloaded a complete selected package. Must Alice remain online
   while Bob freshly checks it?
5. Bob has three request credits left and zero native-stage credits. Can he
   assume another native submission is authorized?
6. A query reports `complete:true`. Does Bob now know every relevant theorem
   in the mathematical commons?
7. Do the two Rose count equations demonstrate exponential useful growth?

### Short answers

1. No. Endpoint identity and byte integrity are not mathematical acceptance.
2. No. V2's real numeral example passed checking and hit an index restriction.
3. No. Distinct exact encodings can express equivalent mathematics.
4. Not for that already acquired package and its required locally available
   dependencies; the v2 return test checked after the supplier stopped.
5. No. Resource dimensions are separate; the owner must authorize more stages.
6. No. Completion refers to the specified bounded local/peer catalog query.
7. No. They establish a useful software capability: actual checked vocabulary
   reuse and return. Growth quality and scale need different evidence.

## Sources and audit trail

These are unnumbered project references, not a claim that all linked research
files accompany the standalone source ZIP.

- [V2 startup and selected package](../2026-09-23-v2-local-release/START-HERE.md).
- [V2 qualification, costs and limitations](../2026-09-23-v2-local-release/QUALIFICATION.md).
- [V2 final delivery integrity](../2026-09-23-v2-local-release/HANDOFF-INTEGRITY.md).
- [Actual original source13 exercise: acceptance followed by publication refusal](../../experiments/auxiliary-frontend-01/EXERCISE-OUTCOME.md).
- [Independent successful continuation audit](../../experiments/auxiliary-frontend-01/CONTINUATION-OUTCOME.md).
- [Exact submitted revised counting source](../../experiments/auxiliary-frontend-01/consumer/CountPublishable.lean).
- [Selected source13 core documentation](../../product-local/auxiliary-frontend-source-13/CORE.md).
- [Guide technical review](../../research/audits/v2-guide-2026-09-23/TECHNICAL-REVIEW.md).
- [Guide mathematical-example review](../../research/audits/v2-guide-2026-09-23/EXAMPLE-NOTES.md).
- [Guide teaching review](../../research/audits/v2-guide-2026-09-23/TEACHING-REVIEW.md).

The key idea to retain: **the network helps participants obtain and reuse
mathematics; local formal checking establishes the selected acceptance claim;
agents choose what to investigate; useful growth is an additional obligation.**
