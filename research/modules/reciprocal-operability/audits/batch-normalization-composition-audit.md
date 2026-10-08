# Published-batch normalization composition audit

Date: 2026-09-20. Reviewer: `egress_composition_audit`, independent of the source author. Scope: exact target partition, dyadic normalization/carries, publication-owner and borrower composition, inherited F/G/H authority/lifecycle rules, and N recovery-scope boundaries. The joint numerical resource/calendar proof has a separate reviewer. Concept and document inspection only: no implementation, executable model, extraction, native replay or measurement.

Final disposition: **no blocking composition issue remains within this review's scope at source `34DA63220B9483E7CB7E825CBB21092AAD1F27E43F8F9B052EE14A3760714DB0`.** The complete repaired source was independently hash-confirmed and reread. The coordinated clarification makes pre-mutation coverage invalidation explicit and supplies conservative joint RAM accounting. Neither this review nor those clarifications select the proposal, establish actual resource fit, or complete the project's operability/growth goal.

Historical initial disposition: no blocking composition finding was identified at the first held cut. The reviewer called out the required transition-entry interpretation for cached coverage; root then requested explicit source wording in the coordinated clarification. The initial-cut reasoning below is preserved, with the exact repaired-cut review recorded at the end.

## Exact reviewed source and inherited contracts

The reviewer independently hash-confirmed and read the complete [batch-normalization contract](../batch-normalization-contract.md) at SHA-256 `85BD95952A8958969DCA09B5B516567449EB838B072D39954EC09963CA1C1112`. The author reported 26,426 bytes; this audit's source identity is the independently observed hash, not the author's report.

The inherited passages inspected directly were:

- [F exact routing coverage](../../../../notes/analyses/CP-001F-exact-routing-coverage.md): immutable scope and group identities; unique cell/provider row ownership; DROP-before-PUT; exact roots/versions; group OPEN/BATCH/RENEW/CLOSE; historical observations; generation-fenced reclamation.
- [F dissemination/routing](../../../../notes/analyses/CP-001F-dissemination-and-routing.md): provider ad identity, revisions, authenticated mutation and the separation of retained advertisements from guaranteed discovery.
- [G structural retrieval](../../../../notes/analyses/CP-001G-structural-retrieval.md): semantic targetRef grammar, FeatureScope construction, ProviderAd2/descriptor/replay binding, grouped feature service and anchor eligibility.
- [H resource supply/discovery](../../../../notes/analyses/CP-001H-resource-supply-and-discovery.md): shared provider-level owner ledger, borrowed obligations, mixed ownership status, original dyadic-tier policy, single active handoff and aggregate scope/resource ceilings.
- [N routing recovery](../routing-recovery-contract.md): pending twenty-target inputs, finite admitted key obligations, publication-scope changes versus physical placement replacement, and conditional rather than automatic recovery.

This audit does not freshly audit every inherited native or transport contract. Those remain separate dependencies.

## The actual gap, without rejecting the finite N witness

H allows an arbitrary bounded input batch but specifies equal-size union into power-of-two completed tiers. Under disjoint exact target sets, a twenty-target run can only grow by whole equal-size doubling to `20·2^k`; that number always has odd factor five and cannot be a power of two. Paying for such merges does not itself supply a path into H's selected binary tiers.

The original per-token logarithmic bound for successful doublings is not thereby disproved. The missing piece is arbitrary-batch ingress into the stronger settled-tier invariant. In particular, without that restriction, distinct odd-sized runs need not collide at all. Seven disjoint runs of sizes `1,3,5,7,9,11,13` contain 49 targets, admit no equal-size merge, and exceed the asserted six occupied completed levels if treated as arbitrary settled runs.

N explicitly keeps its eight twenty-target scopes pending. Its existing finite service/stock witness therefore remains valid. This proposal supplies a separately admitted continuation for such already-published inputs; it does not silently reinterpret N's earlier pending state as completed consolidation.

## Exact targets and partition proof

The admitted input uses G's semantic targetRef, rather than an evidence instance, descriptor or proof identifier. Equal mathematical targetRefs with changed evidence are guarded updates, not two units of insertion mass. The admitted parent is nonempty, sorted and duplicate-free, and its target set is disjoint from every other logical run/pending input in the selected collection. Missing exact partition state produces nondecision. Already-published overlaps are explicitly outside this normalizer's admitted domain; refusal preserves their actual rows, evidence and custody obligations.

Let the remaining target count initially be n. Each selected block has size `2^floor(log2 remaining)`, consumes the next consecutive segment of the already canonical target order, and strictly decreases the nonnegative remaining count. Thus blocks are nonempty, disjoint and exhaust the parent. Their sizes are precisely the nonzero bits of n; the block count is popcount(n). For n = 20, these are 16 and 4. For a power-of-two n, the single child is the same exact target/token scope, so the specified no-op reuse avoids an unnecessary physical migration. Empty input is not fabricated into a singleton.

Each child union is computed from every target in that child, including tokens it will borrow. An unchanged G scope format and its actual canonical commitment are used; no new target identity or mathematical evidence is created by repartitioning. Actual feature construction, hashing, traversal and fit checking remain funded preparation, not consequences of the cardinality proof.

During physical migration the parent and provisional children are one logical partition, not additional mathematical contributions. Their physical scope records, maps, lists, references and histories are nevertheless separately charged. The source explicitly distinguishes logical replacement at guarded settlement from subsequent physical retirement.

## Publication ownership, anchors and borrowers

For every parent-owned key, the existing eligible anchor determines exactly one child: the child containing that anchor's semantic target. The fixed target partition makes this choice unique. If the old anchor cannot continue, a deterministic choice among actual eligible supporting records determines a child; lack of support stops/degrades the operation rather than granting new publication authority. Every selected anchor therefore belongs to its new exact owner scope and actually emits the key under the fixed F/E.

A token emitted by both children is not assigned twice. One child owns its provider/key publication, and the other records an ordinary borrowed obligation. Keys already owned outside the parent retain that owner and their rows. Consequently splitting a target set does not multiply provider/key ownership or convert borrowed coverage into G's independent FULL_FEATURE status.

The proposal also covers the less local case: a parent-owned key borrowed by a scope outside the split. Such a borrower retains its stable provider/F/E/key ledger reference and resolves the exact current owner/transition version. Changed versions invalidate cached coverage; a stale cached aggregate is not current merely because the borrower's immutable FeatureScope is unchanged. Any actual recomputation/reverse-dependency traversal is separately paid. An implementation using unversioned copied references must supply a complete paid compatible update plan or decline this normalizer. Thus indirection is a stated admitted representation premise, not an assumed free global rewrite.

Transition invalidation applies when the selected owner entry enters its in-flight/mixed state, before asserting current settled coverage. This reading follows the explicitly inherited H handoff ledger and the source's requirement that owner/transition versions and coverage status publish together at the guarded local authority boundary. The later final logical-partition commit is not permission to keep a stale settled owner assertion throughout intermediate mutations. Remote operations still have separate actual commits and uncertain outcomes; no cross-machine atomic transaction is inferred.

ProviderAd2 has no scopeID field. The immutable holder group supplies the scope binding; the signed ad supplies provider, exact key, revision, contact and anchor descriptor/replay. The source gets this distinction right. Preserving an unchanged eligible anchor and other signed fields can preserve the exact ad bytes where existing revision rules allow, but it never bypasses actual group ownership migration. A changed signed field requires the ordinary higher revision; equal-revision/different-byte replacement is not accepted.

## F/G physical lifecycle and truthful interruption

The source uses existing grouped operations, exact mode/F/E and actual provider authentication. At a given holder/cell/provider key it first resolves the old-group DROP and only then admits the new-group PUT. It does not invent cross-group make-before-break or count a planned destination as an observed row. OPEN alone neither reserves arbitrary later row work nor extends an already existing group's lease.

A lost response leaves a counted uncertain transition. The source cannot treat it as a failed mutation, repeat a spent invocation, or insert a conflicting owner without exact outcome/reconciliation. Group roots and versions come from reconciled local observations. A successful DROP followed by failed PUT leaves a genuinely missing copy; the other actual current replicas may help but supply no unconditional continuity theorem.

Per-key mixed old/new copies remain TRANSFERRING/PARTIAL rather than settled single-owner coverage. A parent group is closed only after its exact empty state is established; removing one moved key does not close unrelated remaining members. Old/current group renewals, anchors, remote leases, snapshots and generation-fenced cleanup remain required. Native proof custody has separate ownership and is not released by an operational scope retirement.

Current eligibility and disclosure/incident guards can defeat an old plan. The normalizer then stops or requires actual revalidation/readmission; retained bytes or an earlier receipt do not restore authority. Deep marker paths remain separately funded. The numerical trace's depth-zero assumption does not remove them from the general contract.

## Carries, finite termination and the single handoff

After a split settles, its power-of-two children are processed by increasing size and exact scopeID. A ready run either occupies an empty tier or encounters that tier's unique incumbent. Because the admitted logical target sets are disjoint, two size-2^k parents have an exact union of size-2^(k+1), not merely at most that size. The source therefore supplies the premise needed for actual doubling.

An occupied-tier collision is a ready/pending carry, never two completed incumbents. Its immutable result contains the full parent union; owned keys move through the same actual group fences, while keys owned externally remain borrowed. Existing eligible anchors lie inside the union. The new logical frontier commits only on real guarded settlement, with all old physical state still charged until cleanup.

Let R count dyadic completed plus ready runs and Q count ready runs in the fixed admitted pool. A carry reduces R by one. Installation into an empty tier preserves R and reduces Q by one. Lexicographic `(R,Q)` over nonnegative integers therefore strictly decreases after each successful step. This proves finite successful-step termination, not that any remote service must accept a step. At the settled end, distinct power-of-two sizes sum to M, hence there are popcount(M) runs and exactly `R0 - popcount(M)` carries after normalization. The proof does not include arbitrary other pending inputs or late arrivals outside its frozen pool.

The physical lineage shares H's single active handoff. It does not gain a slot per child or conflate serial mutation calls with free concurrent state. Earlier tails can coexist only as separately charged retained stock; insufficient capacity delays further work. The complete carry union, including the largest planned carry, must fit the admitted 4096-target envelope or receive a distinct future capacity admission.

Normalization can increase logical run count and cause one successful parent-to-child owner movement per retained placement row. This is a separate charge. Thereafter a key owned by a child of size m can move on at most `floor(log2(M/m))` successful doublings in the fixed insertion-only epoch. Repeated splitting, failure/retry, additional copies, anchor churn and repair remain separate work, as H requires. No unbounded stream or sustained throughput conclusion follows from the finite potential.

## Published twenty-target and occupied-tier trace

The source takes two distinct twenty-target scopes A and B already among N's eight pending scopes. It does not create forty uncounted new targets. A becomes A16/A4. B becomes B16/B4, then actual occupied-tier carries create C8 from A4+B4 and C32 from A16+B16. The final selected forty-target cohort is 32+8; the main 2048-target run and six other pending twenty-target scopes remain as stated. Total logical target mass stays 2208.

Each selected target has eight unique tokens and eight common tokens owned by the unaffected main scope. The 640-row moves for each twenty-target split and the 256/1024 moves for the size-four/size-sixteen carries are actual ownership work. Common-token borrowing neither moves those main owners nor rechecks mathematical evidence merely because group scope organization changes. Detailed joint call/CPU/traffic/peak/calendar fit is the independent resource audit's subject, not supplied by these arithmetic counts alone.

The favorable example states existing versioned owner indirection, no uncounted initial partial/empty/uncertain parent state, actual valid anchors/leases and successful row operations. Failures retain their stock and can introduce extra renewals or require readmission. Its use of N's discretionary reserve is expressly contingent on that reserve being genuinely uncommitted; previously promised repair/tail duties cannot disappear by relabeling calls.

## N composition, defeating cases and evidence limit

Changing a key's publication-scope owner changes the affected N admitted cut, even if its holders and ad bytes remain the same. The source requires a newly admitted obligation set/calendar before claiming the resulting recovery bound. This differs from N's permitted physical holder replacement inside an unchanged publication owner. Unaffected main keys keep their own exact guards; neither a scope hash nor this operation grants whole-network invalidation authority or fresh resources.

The stated countercases are substantive: overlapping logical inputs, missing anchor support, externally borrowed keys with stale caches, lost DROP replies, inadequate tail capacity/lease headroom, committed reserve exhaustion and arrivals outpacing actual service. Each can prevent completion while preserving safety and counted obligations. Those are not successful accumulation. Likewise, no valid group response, signature or owner-ledger entry changes mathematical acceptance; independently checked native evidence remains necessary for reuse.

At this initial held cut, the proposed mechanism closes the specific non-dyadic ingress choice within its explicit disjoint fixed-feature domain. It does not implement overlap repair, qualify real resources, execute native contribution/reuse, or establish beneficial exponential growth. No source or frozen document was edited by this reviewer. A separately coordinated source repair will be reviewed at its exact new hash before this audit's final handoff.

## Repaired-cut review and final handoff

The complete repaired source was independently hash-confirmed and reread at SHA-256 `34DA63220B9483E7CB7E825CBB21092AAD1F27E43F8F9B052EE14A3760714DB0`, observed length 27,282 bytes. The reviewer reversed only the two stated clarification fragments in memory and reproduced initial SHA-256 `85BD95952A8958969DCA09B5B516567449EB838B072D39954EC09963CA1C1112` exactly. No additional hidden source delta is covered by the handoff.

### Explicit pre-mutation coverage invalidation

The source now requires the owner entry to enter transitional state and advance its version **before dispatching its first ownership-changing mutation**. Earlier settled-coverage assertions and caches, including external borrowers' aggregates, thereby lose current status before mixed placements and before final logical partition commit. Historical observations remain historical. Actual surviving individual copies do not become a settled aggregate assertion.

This makes the initial review's inherited-H interpretation explicit. It closes the potential final-commit-only reading without changing group operations, native authority, or the distinction between local observation and remote actual commit. Unversioned owner references still require a paid complete compatible update plan or refusal. Recomputing aggregates still costs actual work.

### Conservative joint resident state

The revised resource row explicitly supplies at most 48 MiB of additional simultaneous resident metadata, planning and transition state: all 32 MiB retained metadata plus a separate 16 MiB planning allowance. Adding that to the existing stipulated 1.75 GiB gives 1.796875 GiB, below the 2 GiB supplied ceiling. This is a conditional joint residency premise, not an inference from serialized disk bytes or a native-memory measurement. The detailed cross-resource/calendar disposition remains the independent resource review's responsibility.

### Continued scope and limitations

The final full reread preserves the exact semantic disjoint-input domain; deterministic dyadic partition; power-of-two no-op; single-provider/key ownership; anchor-in-child requirement; external borrower versioning; actual DROP/PUT and uncertain-outcome fences; and one active H handoff with all-state physical accounting. N's affected publication-owner cuts require readmission rather than inheriting an unchanged recovery bound.

The `(R,Q)` termination/count argument remains restricted to successful paid steps in a finite admitted pool with no new inputs into that pool. It proves neither remote willingness, wall-clock completion, a sustained processing rate nor eventual normalization of the unselected six pending inputs. One-time normalization work remains separate from the later successful-doubling bound. The two published twenty-target inputs still become the nonempty 32+8 cohort without rewriting proofs or counting extra target mass.

No new wire opcode/schema, global authority, human-intention condition or mathematical acceptance shortcut has been added. Implementation, native qualification, actual resource fit and useful reciprocal growth remain **NOT RUN / unestablished**. No additional source repair is requested by this composition review. This audit is handed off for preservation; future substantive changes to the reviewed identity, ownership, transition, carry or N-boundary clauses reopen the affected review.
