# Persistent withdrawal controls: saved outcome audit

**PASS within the selected native-free scope.** Independent reviewer core_release
read the saved result, complete stderr, empty stdout and control report; hashed
all 117 retained source-snapshot files against the saved exact selection, with
zero missing or mismatched files. No rerun, native call, proof, build or Git edit.

Evidence root: `experiments/v5-local-checks/trust-withdrawal-controls-01/`.

| Evidence | SHA-256 |
|---|---|
| selection.json | 64be70eb04b7c885fd4ffee485b06b5599b7f682a6244878e856ca92fe95d03c |
| RESULT.json | 0a1fc8aadf49b1b01f707b2bfbc2ca552d6110db0642048bb1e3fb1b525b445b |
| controls-result.json | 48e7bd0768ee33bb1efc9fc038f15a4f7e4363dbf2b7d1ee00228e6c9eff6ee3 |
| command/stderr.txt | 0d0bbd3efbaec3d4ae8c49686e90de2ca39a859b1a65e2592f7d49dedb6927ef |

All 11 selected tests ran and passed, with zero failures, errors or skips. The
supervisor reports exit zero, direct child reaped, Job closed, zero active or
terminated processes, no cleanup errors and no requested termination. Source
selection retains 111 predecessor inputs plus six fresh withdrawal files; only
the new controls entry executes, not a predecessor test suite. Used controls
SHA-256 is `748bd8bd6ddeed3680c74f67ef84f5e9fa62427af8f1943c6f2d8ccebec6dfef`.

Observed: ordinary reopen preserves adoption; wrong/unregistered binding
refuses; withdrawal survives reopen and old-domain denial remains sticky after
fixture tampering; missing/malformed adoption and incomplete marker refuse;
failed marker create/sync never falsely acknowledges persistence; busy I/A
revocation clears registries; actual I.receive refuses at postworker trust gate
before binding/minting while preserving charges; new runtime operation refuses;
both constructor doubles receive the same original binding and the final
pretransfer guard closes delta/A/I without transferring ownership.

Cost: Job CPU 0.921875 s + wrapper CPU 0.59375 s = **1.515625 known CPU s**;
whole wrapper wall **5.370337400 s**, including selected-source/runtime handling.
Unittest's inner 0.235 s is not the total cost. Selected allowance was
30 CPU / 60 wall seconds / 256 MiB; no enlargement or retry occurred.

These are real persisted guards with explicitly inert issuer/runtime shells.
Native and proof call counts are zero; mathematical_acceptance is false.
Synthetic worker closure proves only refusal ordering, not receipt validity.
Remote-reader startup is source-reviewed but not invoked here. This does not
establish actual certified-receipt integration, hostile-input isolation,
antirollback, concurrent recall, public deployment or completed v5. Original
source/selection/evidence remain frozen. Root alone selects any next operation.
