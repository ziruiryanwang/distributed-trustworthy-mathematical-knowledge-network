# CP-001E: scalable reciprocal reuse and corrected foundation

Checkpoint date: 2026-09-20. Prior work began 2026-09-19. Status: integrated concept/specification with independent audits; no implementation or deployment qualification.

## Goal retained

Develop a rigorous, practically operable decentralized mathematical commons in which independent local agents reliably build on existing formal knowledge and contribute reusable new knowledge. Use proofs where they help, and defensible engineering or heuristics where full formal guarantees are inappropriate. Keep the correctness boundary strict while making useful accumulation and reuse efficient in practice.

The initial foundation is Lean 4. No central theorem authority, mandatory blockchain ledger, shared research objective, human-intention assessment, attribution machinery or unsolved-mathematics task list is introduced. Local operational queues and custody policies concern service and existing evidence, not agents' research choices.

## Start here

Read the [integrated operational v2 contract](../../spec/OPERATIONAL-CORPUS-V2.md), followed by the [audit disposition](../audits/CP-001E-AUDIT-DISPOSITION.md). The mathematical, network, client and custody contracts named there form one selected design, not a menu of unresolved alternatives.

The [foundation security audit](../analyses/CP-001E-foundation-security-audit.md) is particularly important: the previous v4.22.0 pin contains checks subsequently repaired for soundness. It is no longer the deployment candidate. Current candidate is Lean v4.34.0 at `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`, with mathlib `5ed2965256430c3649e86755f9576b54eca72435`. A corrected pin is a qualification target, not an executed proof of readiness.

## Decisions made

| Problem | Chosen mechanism |
|---|---|
| Trustworthy mathematics from fallible/malicious producers | Inert Native2 declarations and complete exact selected evidence, independently checked under a locally qualified corrected Lean foundation |
| Repeated metadata grows quadratically | Direct semantic references; canonical persistent witness maps and derived declaration closure |
| Reuse repeatedly pays for unchanged mathematics | Exact receiver-owned certificates, compatible environments and persistent shared protection; retain cold/incompatible-branch costs |
| Tiny objects create excessive paid round trips | Bounded BUNDLE1 with separately funded computation/delivery, explicit ranges and full-object hashes |
| Export inventories are too small or rewrite long suffixes | Persistent operational inventory map, finite exact export lease and streamed offline records |
| Unrelated updates invalidate useful work | Relevant current-use guards; admission-generation sealing distinct from crash recovery |
| Agents cannot find/apply the corpus affordably | Exact/shared-interface retrieval, explicit nonprefix windows, bounded formal matching, checked applications and inert per-entry library conveniences |
| Honest caching loses knowledge | Owner-authorized local durable custody, finite autonomous maintenance, explicit degradation/release/handoff observation |
| Usefulness is heuristic | Bounded local usage/cost/coverage/exploration signals; correctness never inferred from popularity |

Identity/source attribution has no privileged mathematical role. Authentication remains necessary for scoped service authority and statements about who observed or promised what. No signer can make a bad proof acceptable.

## Evidence produced

The notes contain:

- concrete alias and ordinary iterated-correctness families demonstrating avoidable quadratic flat metadata;
- canonical Patricia binding/path-copy arguments and exact witness completeness rules;
- a Poisson countermodel for unrelated global-epoch retry amplification;
- per-object versus bundled-call arithmetic, including burst corrections and inventory-node overhead;
- explicit private/public/advisory read-scope and client-activation boundaries;
- cold, warm, branch, rollover, loss and checker-incident paper traces;
- preservation countermodels, finite-replica hitting-time formulas and conditional summable-risk bounds with independently repaired qualifications;
- new local custody state, ownership/release/replacement/maintenance/status contracts;
- source-pinned official kernel fixes and backports, concrete old/new string-bootstrap difference, and explicit limits of inspected Lean4Lean verification;
- seven complementary independent review notes plus integrated dispositions.

The corrected matching mathlib tree contains 8529 Mathlib Lean source blobs totaling 98,449,500 bytes in the observed untruncated repository tree. This is a real source-scale target, not a count of theorems, native proof objects, dependency bytes, or a benchmark.

## What was not done

No application code, executable model, Lean build, native export/replay, exploit execution, benchmark, or public deployment was performed. No executable peer material was installed or trusted. The new foundation's concrete bootstrap/checker images remain to be qualified. No claim of guaranteed exponential growth, universal complete search, or permanent survival from fixed finite replication is made.

The system's conceptual loop is selected: acquire exact existing evidence, establish a local qualified reusable closure, privately investigate, check/export an increment, and let other independently authorized nodes repeat. Its actual operating cost, usability and fault behavior require the future qualification work named in the disposition.

## Artifact preservation

The [SHA-256 manifest](CP-001E-SHA256-MANIFEST.md) binds this checkpoint's final specification, analyses and audits, excluding itself. The top-level [current-design pointer](../../CURRENT-DESIGN.md) is intentionally mutable and excluded from that manifest. Historical CP-001/1A, CP-001B, CP-001C and CP-001D files are not edited.

Document-integrity checks validate stored bytes, links, character decoding, fences and mathematical delimiters. They do not validate mathematical soundness, protocol implementations or practical performance.

The project goal remains active. This checkpoint is a rigorous durable record of current choices, repaired findings and remaining qualification obligations—not a claim that the whole autonomous-accumulation objective has been achieved.
