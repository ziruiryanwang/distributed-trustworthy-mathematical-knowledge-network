# Two finite small-host links

2026-10-17, root. This records exact prepared plans and the execution decision
after independent final-native/plan clearance. It does not authorize proofs,
guest execution, SDK/guest rebuilds or a layout attempt.

| Plan in experiments/v5-local-checks | SHA-256 |
|---|---|
| small-aggregate-snapshot-host-build-01-selection.json | e4493418256735529f7fc19ed606ea459bf35b613b57680d2e0a31a7b858e4bd |
| small-aggregate-stage-host-build-01-selection.json | 049129dacf8b43ea3e4a1796a26098dfb207ddbc80d5c1b49cbfde94fc71fa38 |

Each plan binds three source files and the retained 1,071 compiler/library pins,
2,320,491,997 bytes. No libraries are replaced. The selected native source is
snapshot6644d9a0 and stage975e68df, including pre-read nonrefundable accounting.
The snapshots preserve the relative include of the unchanged receipt helper.

Each link is bounded by 240 inclusive worker CPU seconds, 300 worker wall seconds,
3,072 MiB, six active processes, 40 ordinary / 60 total controller CPU seconds,
420 total wall seconds, 512 MiB output and 8,192 output entries. One compiler link
only. Failures are preserved, never automatically retried. Used sources freeze.

Run these links **sequentially**. Read-only capacity observation before selection
was 3,715,452 KiB free physical and 5,537,112 KiB free commit, not reserved memory.
Two concurrent 3 GiB link ceilings exceed that observed commit headroom. The
combined sequential allowance is at most 480 worker CPU plus 120 controller CPU,
840 wall seconds, 1 GiB retained output and 16,384 entries; peak worker ceiling
stays 3 GiB. No multi-GiB proof or other link overlaps. Independent source/review
work continues while each link runs. Do not terminate unrelated applications.

Root launches only after the independent reviewer clears these exact plans.
The native author may audit actual compilation bindings/closure/cost separately;
that operational audit is not independent review of their own implementation.
The independent source reviewer remains a different agent.

Completion provides host build evidence, not proof memory sufficiency, mathematical
acceptance, a growth advantage or final v5. Next actual layout still needs its
own reviewed exact finite selection.
