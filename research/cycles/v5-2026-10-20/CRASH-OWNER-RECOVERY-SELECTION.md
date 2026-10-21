# Implement prospective crash-owner quiescence, not report-based recovery

2026-10-21, root. Root fully read `CRASH-OWNER-RECOVERY-DECISION.md`, SHA-256
`7a2ce0d32bc59410e6f419711d7e793e556a55e465904df05a516be588cf26aa`.
Select its surviving-supervisor lane for source implementation. No runtime,
fault campaign, existing-root migration, deletion or installation is selected.

The now-used bounded_reclamation source d59615b6/19713fc4 and composer40436584
remain frozen. Core_release owns new `software/v5/supervised_generations/`
source, checkpoint `SUPERVISED-GENERATIONS-SOURCE.md` in this cycle. Derive any
needed lifecycle successor from that exact base; preserve established startup,
clock, slot, charge, exact closure and reclaimer behavior. Reuse the unchanged
helper/composer where possible, rather than copying or redesigning their logic.
Root owns later selectors, integration, runtime decisions and Git. Guest reviews
after current actual service outcome; screen may author disjoint focused controls
only once concrete source/API is stable and root selects their exact scope.

## Required implementation boundary

New private enrolled managers only. Before child effects, durably reserve a
bounded one-shot supervisor/session with exact root/epoch/config, selected worker
profile, nonce and finite launch/cleanup limits. Every managed run reservation
must join that session before files or actors exist. No old UNKNOWN row can be
retrospectively adopted or relabeled through an imported outcome JSON.

Use the exact current Windows Job and direct-process handles; further launches
must be sealed. A successful exact direct wait plus fresh Job active-zero under
the selected containment profile permits the surviving supervisor to commit
`QUIESCED_UNCLEAN` while still holding the capability. Preserve original run
charges/retirement intent and never overwrite a newer session or genuine CLOSED.
There is no orderly-close claim, run refund or immediate storage adoption.

This guarded persisted state may satisfy the process-quiescence part of later
retirement only. Original horizons still require a fresh conservative-clock
adoption; exact inventory, root identity and prepaid-window checks still govern
reclamation. Unsafe partial roots, unknown data and exhausted authority hold.
The implementation must retain a finite slot/session census and no event-history
growth. Registry commit uncertainty must poison/hold, not resurrect state.

Prefer a narrow adapter around the existing finite supervisor/Job seam if its
actual APIs permit observing exact handles before close. Do not weaken the
supervisor, accept a bool/dictionary as closure, silently renew original limits,
or duplicate the entire launcher merely for convenience. Inspect the actual
call/cleanup ordering before choosing this seam.

Supervisor loss remains UNKNOWN. The existing suspended-before-assignment
orphan/resource gap is explicitly not solved by this lane. Do not add a keeper,
new named-job protocol or atomic process launcher in this source cut. The scoped
improvement is useful owner-crash recovery with a surviving finite supervisor,
not a new qualified-version replacement for the full v5 destination.

Canonical root is `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Guard/AGENTS, explicit workdir and absolute apply_patch paths are mandatory;
no subagent Git. Existing source, evidence, installation and user data stay intact.
