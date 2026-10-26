# Selected first actual workflow-pack check

2026-10-26. Root adopts complete REVIEW03.md, SHA-256
`6c4f6604f503b26250d058b11beb5b4f81aa2196f015783296c24cf88bdeec07`,
building on the unchanged utility/test review and the selection-scope correction
in REVIEW02.md. Select exactly one controls03 run.

Selection: `experiments/workflow-source-controls03-selection.json`, SHA-256
`8e0a666ee576dafb8ec8727366d7931906f89825f4c677c3f6ac8da6462a4ed0`.
Output: `experiments/v5-local-checks/workflow-source-controls03`, confirmed absent.
Controls01 remains a failed runner preflight, with no test/output. Controls02 was
never executed. Their selections and records remain unchanged. There has been
no successful or failed workflow pack to repeat.

The unchanged runner takes 154 eligible source snapshots; 157 external pins
cover all 153 actual canonical pack inputs, original base ZIP and three Python
runtime files. The test itself runs from its snapshot but explicitly reads the
approved canonical source root/utility; every such pack input is pinned before
and after execution and rechecked by the utility. This replaces the unexecuted
all-mirror-input claim. Owner-controlled immutable inputs remain a premise.

Only the unexecuted start guide was revised to add the independently reviewed
fresh-basis authoring route; its original exact bytes are preserved separately.
Final guide SHA-256 is
`44a99a3e2276f2df240fb10d8683e70b2d06ca03c90b41bed02a4830d12b3f67`.
No base payload, executable, test or runner changed.

Bounds remain 120 wall / 60 inclusive Job CPU seconds, 384 MiB, four processes,
2 MiB stdout and 1 MiB stderr. Run unchanged Run-V5-Check.py with isolated selected
Python, absolute selection path and exact selection hash in the canonical root.
One public pack and one relocated public verify plus focused file/manifest/helper/
documentation controls only. No Lean, service, mathematics, network or external
publication. Preserve failures; no retry or budget renewal. Independently audit
the actual result, source/ZIP projection and clean process closure before adoption.
