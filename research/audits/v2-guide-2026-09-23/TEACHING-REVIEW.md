# Teaching review for the delivered v2 guide

2026-09-23. Scope: a detailed Markdown explanation of the frozen delivered
source13 v2 for an undergraduate reader. This is a teaching outline and review
checkpoint, not a competing guide or a product qualification. No product code,
installation, experiment, or delivered release document was changed or run.
The canonical project guard passed using the process-local policy invocation.

## Source boundary

Read `AGENTS.md`, `GOAL.md`, the current section of `research/NOW.md`, and the
complete delivered v2 `START-HERE.md` and `QUALIFICATION.md`. The reference
release is `deliverables/2026-09-23-v2-local-release`, source13. Source14 is a
separate development successor and must not become a v2 capability in this
guide. Frozen release documents and their evidence remain authoritative.

## Suggested layered path

1. **Purpose and one complete story.** A supplies a definition; B obtains and
   locally checks it, builds a new result using it, and returns the result;
   A checks it. Introduce an agent as the chooser/author and a node as the
   local software, state, and checking service. A reader should know what the
   loop accomplishes before seeing file formats, API names, or release history.
2. **Small mathematical prerequisite.** A definition specifies an object or
   operation, a theorem states a proposition, and a proof term is the formal
   object checked against that proposition. Explain the difference between
   reading an informal argument and checking an exact formal statement under
   explicit foundations. Formal acceptance does not establish that the formal
   statement captures an intended informal question.
3. **Separate six questions.** Correctness asks whether a proof checks;
   identity asks which exact encoded object this is; discovery asks where a
   candidate might be; transport asks how its bytes arrive; custody asks who
   retains and serves them; usefulness asks whether they help an agent's task.
   Give one concrete failure that each of the other successes cannot prevent.
4. **The object and its prerequisites.** Explain dependency closure as the
   selected object plus everything needed to interpret/check it. Then introduce
   canonical encoding, digest, reference, package, and local accepted context.
   A dependency graph picture helps only after its arrows are defined.
5. **The actual v2 workflow.** Introduce the verbs by their purpose, followed by
   literal API spelling: find, acquire, admit, submit, publish, expose, host.
   Distinguish receipt of bytes from fresh admission, and exposure from a
   running server. Use a sequence diagram only if each arrow says what moves
   and which receiving check remains required.
6. **The Rose example.** Explain a finite tree whose node contains a list of
   smaller trees; an empty child list gives a leaf. Explain ordinary recursion
   on a tree and helper recursion on a list of trees before saying "main and
   auxiliary recursors." Then explain nodeCount, forestCount and the two count
   equations. The purpose is substantive reuse of the received type and its
   checked recursion facilities, not impressive mathematical novelty.
7. **Why the repair mattered.** Explain the kernel as the checker's internal
   account of constants and the frontend as the source language's account of
   names. Source12 reconstructed a recursor that new ordinary source could not
   name. Source13 repaired that visibility while checking the binding; it did
   not add an axiom or generate a replacement theorem.
8. **Why one accepted theorem still could not be published.** The public
   type-symbol index supported fewer expression forms than the checker. The
   literal-bearing statement was accepted but its publication refused. The
   explicit constructor spelling was a new source submission with fresh
   checks and a different formal identity. This is a particularly effective
   concrete lesson about independent boundaries.
9. **Operating reality and evidence.** Explain finite capacity, owner grants,
   selected contacts and custody. End with a short evidence ladder: what was
   observed, under which conditions, what follows, and what remains untested.
   Put long hash lists, protocol versions and detailed cost ledgers behind
   links or in a reference layer; do not force readers to decode them first.

## Analogies worth using, with their limits beside them

| Analogy | What it explains | Limit to state immediately |
| --- | --- | --- |
| A carefully checked library exchange | Independently held mathematical resources can be borrowed and used in new work. | A library record or librarian's reputation does not replace local formal checking. |
| A checksum as a fingerprint of a particular file | Finding the same exact encoded content, subject to the hash assumptions. | It does not identify a human author, prove a theorem, or detect mathematical equivalence between different expressions. |
| Ingredients for a recipe | A result needs definitions and earlier results, not just its concluding line. | A proof dependency has an exact typed reference; a suggestive informal ingredient is insufficient. |
| A catalog card | Metadata helps locate a candidate without reading every full proof. | The catalog is bounded and incomplete; matching a symbol does not establish relevance or truth. |
| A sealed delivery channel | TLS limits who the client is communicating with and protects transfer. | A correctly delivered package still requires local mathematical checking. |
| A finite lending/storage arrangement | Custody can keep exact packages available after the producer stops serving. | Storage is resource funded and finite; the mechanism does not promise permanent preservation. |
| A book present in a warehouse but absent from the public lookup desk | The frontend-visibility failure made a checked constant unavailable to source authors. | Lean's two maps and exact binding checks are the real mechanism; this is not a synchronization theorem or a distributed-database analogy. |

Avoid "blockchain of mathematics," "global mathematical truth," "all proofs
are searchable," "trustless," and "self-improving knowledge network." Each
would teach a capability or trust model beyond this delivery.

## Prerequisites to explain on first use

- **Formal type:** the exact proposition of a theorem or the kind of a term;
  do not assume readers already know propositions-as-types.
- **Proof term:** a structured formal witness checked against its type.
- **Kernel / frontend:** checking core versus the layer that resolves and
  elaborates source; avoid presenting them as two independent votes.
- **Inductive type / constructor:** a type described by ways to build its
  finite values. Rose.node builds a tree from a list of children.
- **Recursor:** the type's structured recursion/elimination principle. In the
  Rose example, the auxiliary addresses the nested list; it is not an extra
  arbitrary rule added by this product.
- **Canonical:** a prescribed encoding under the selected schema, not a claim
  that mathematically equivalent proofs or propositions share one encoding.
- **Dependency closure:** all exact prerequisites reachable from a selected
  root, not the whole world's corpus and not automatically the whole library.
- **Foundation:** the selected trusted mathematical starting assumptions and
  interpretation; omit dense identifier syntax until this idea is clear.
- **Admission / context:** fresh local checking and the selected admitted
  material available to subsequent local authoring.
- **P1 / snapshot:** if needed, define before the acronym is used; explain that
  a returned handle refers to a particular current candidate state and can
  become stale after acquisition. Prefer purpose before internal naming.
- **Native stage / reservation:** a bounded authorized checking operation and
  a conservative resource charge; do not equate free disk with permission.

## Comprehension exercises and answer criteria

These require no product execution and can be used as brief section-end checks.

1. A peer package arrives over pinned TLS with the expected digest. Can the
   receiver use its theorem as admitted mathematics immediately? **Answer:**
   no; channel identity and content identity do not replace fresh local admit.
2. A theorem submits successfully but cannot publish because its type contains
   an unsupported literal node. Has Lean disproved it? **Answer:** no; this is
   the distinct public-index boundary, as observed in delivered source13.
3. Replace statement spelling `1` with `Nat.succ Nat.zero`. Is this the same
   package identity, and can the old publication be marked successful?
   **Answer:** no to both; the exact representation changes and fresh checks
   are required even though the selected mathematical spelling is equivalent.
4. Draw a Rose leaf and a Rose node with two leaf children. What are their
   counts? **Answer:** one and three, under the example's node-count definition.
   Then explain why counting a forest also needs recursion over a list.
5. A custodian supplies A's exact package after A's server stops. Is the
   custodian making a new theorem? **Answer:** no; continued supply is distinct
   from authorship, novelty and fresh receiving acceptance.
6. A type-symbol search returns no match. Does the commons contain no relevant
   theorem? **Answer:** no; the selected local/peer search is bounded and not
   semantically complete, and relevance can exceed exact symbol occurrence.
7. Two nodes on one Windows machine complete a reciprocal exchange. What has
   that shown, and what has it not? **Answer:** the selected local workflow and
   its actual checking/transport outcomes; not independent physical hosts,
   Internet deployment, broad-library support or sustained useful growth.
8. B has request credits and free disk but zero native-stage credits. Can it
   perform another fresh admit? **Answer:** not on those grounds; it requires
   a deliberate owner renewal of the necessary authorization.

## Review checklist for the root's GUIDE.md

The later review should check that the novice can answer the eight questions
above without reading implementation files; that every acronym is explained
at first occurrence; that the same terms retain the same meaning; that the
Rose story precedes its release archaeology; that a conceptual illustration
is distinguished from the executed source; that figures label trust and data
flows separately; and that observed local evidence is never promoted to
general or future capability. Detailed operating instructions should point
to the frozen release's startup/walkthrough and must not encourage using the
retained, capacity-consumed qualification nodes as a beginner exercise.

## Complete guide review

Read the entire 900-line first draft of
`deliverables/2026-09-23-v2-guide/GUIDE.md` on 2026-09-23. The canonical guard
passed again before this resumed review. This was a static reading review;
no product code or guide command was executed, and no guide content was edited.

Disposition: **ACCESSIBLE_WITH_SMALL_EDITS_RECOMMENDED**. The guide builds a
coherent undergraduate explanation, preserves the six important distinctions,
explains the Rose construction and actual theorem accurately at a teaching
level, limits its analogies, and clearly separates source13 from source14.
Its exercises are answerable from the prose. No misleading analogy was found.

Actionable findings sent to the root author (line references are to this
900-line draft and may move with edits):

1. Lines 74, 97, 170 and 321 use **API**, **LLM**, **kernel** and **native** before
   explaining them. Add short first-use glosses: defined software operations;
   large language model; Lean's core proof/type checker; the actual selected
   Lean checking process. API and kernel currently receive explanations only
   much later. These need only a clause each, not another prerequisite section.
2. Before line 438, explain the central source13 repair in a short paragraph.
   The source12 checker could reconstruct the auxiliary recursor, but ordinary
   source could not name it. Source13 made the already-checked binding visible
   to the source frontend and checked the binding. At present the reader learns
   the remaining numeral-publication limit but not why source13 enabled this
   previously blocked reuse. Explain frontend as the layer that resolves names
   and turns source into formal declarations if that term is introduced.
3. Line 263 labels the working loop "six different milestones," but the table
   presents seven operation rows. "Distinct milestones" avoids a distracting
   counting mismatch without changing the account of the workflow.
4. Line 270's "particular cut" is database jargon. "Particular recorded
   version" conveys the snapshot idea directly.
5. Optional sequencing improvement: the first-reading shortcut at line 35
   skips Layers 3 and 4 before the example. This bypasses definitions of
   canonical objects, submission and publication used later in the example.
   Recommend Layers 0–5 in order, or add a short workflow reminder at the
   beginning of Layer 5.

The final guide needs no new experiment or qualification to address these
teaching findings. The review is about explanation; actual technical authority
continues to reside in the frozen release and its referenced evidence.
