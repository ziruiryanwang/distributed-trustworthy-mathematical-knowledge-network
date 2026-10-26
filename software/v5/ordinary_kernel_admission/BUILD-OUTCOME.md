# Independent actual build01 audit

Disposition: **PASS_BUILD_ONLY; CONTROLS AND ADOPTION NOT YET ESTABLISHED**.

Saved evidence: `experiments/v5-local-checks/kernel-admission-build01`.
The reviewer inspected/hashes files only; no build, native, owner or recovery
operation was launched. The saved selection matches the reviewed SHA-256
`6b9ca2c90ca8b9796b23f3761a5f339f63cdf1c9d896c71c6d316e875eb66635`.

All eight selected source/current-snapshot pairs, 22 external pins and 27 build
input rows match actual bytes. Eight staged Lean sources, three copied supervisor
files and all eight object rows also match their recorded lengths/hashes.
The object directory has exactly eight `.olean` files, 13,954,288 bytes total;
no extra companion or module appeared.

The compiler log records one successful call each, in order, for
CheckedExtension, LocalSnapshot, OrdinaryExport, BasisSnapshot and
OrdinaryWorkflowWorker. OriginalExpr, OriginalDecl and BootstrapSupport are
exact reused objects. BasisSnapshot was compiled but its object equals its
predecessor; equality does not imply that its recorded compile call was skipped.
The result map binds each object to the expected selected source. No fixture
main, mathematical request, owner state or package assembly occurred.

Both inner and outer reports show zero exit, reaped child, closed Job, no active
or terminated processes, no termination request and no cleanup errors. Both
stderr files are empty. Outer wall time is 7.4181178 seconds; inclusive outer
Job CPU is 6.265625 plus 0.4375 wrapper CPU, **6.703125 known CPU seconds**.
Peak aggregate private commit is 627,159,040 bytes. Inner worker CPU is 5.390625
and adapter CPU is 0.796875; these are contained in the outer accounting and
must not be added again. No resource-limit event appears.

| Evidence file | SHA-256 |
|---|---|
| RESULT.json | `203d082b6c8a821bf2ad1b8e13423287838dda2b5ed4d2ec35cb756eb123fb51` |
| native/BUILD.json | `275764e8b0da12ffb2254d0c257452e5ea2082082072de9e965618723866ded9` |
| native/SUPERVISION.json | `75d0f769e1d049e223bfc6b32590bf14f6b837a4fa05c49291c62834515ee895` |
| native/INPUTS.json | `26ac0b17ca026bc4542d134e0e4571e3b2b60bbec50cc2c6d43bfa8c5f201730` |

The outcome supports using these exact compiled modules in separately reviewed
focused controls. It establishes no acceptance of the failed Std intake, new
implementation identity, state migration, library-scale compatibility, growth
benefit or final v5 completion. Used build sources, inputs and outputs stay frozen.
