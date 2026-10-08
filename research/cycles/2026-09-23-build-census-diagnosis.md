# Build census diagnosis: mixed-exposure preparation01

Date: 2026-09-23. Author: `central_release_recalibration`.

Disposition: **reachable Windows namespace false-rejection mechanism identified
by source inspection; the retained build's triggering entry and cause remain
undetermined.** No retry, Python import, compiler invocation, product edit, or
evidence mutation was performed for this diagnosis. This note proposes a bounded
discriminator, not a successful experiment or a qualified fix.

## Scope and evidence

All project paths below are relative to the sole canonical root,
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

Read evidence:

- `experiments/mixed-exposure-01/preparation-01/RESULT.json`.
- `product-local/mixed-exposure-integration-08/build-work/scratch/support-build/stage-build/stage.json`.
- The adjacent `plan.json`, `run_stage.py`, empty stdout/stderr logs, and retained
  filesystem entries, inspected using read-only PowerShell commands.
- `product-local/mixed-exposure-integration-08/install/py/run_stage.py`.
- `D:\Python314\Lib\ntpath.py` and
  `D:\Python314\Lib\pathlib\__init__.py`, read as source, not imported.

The source07 runner, source08 runner, used source08 installed runner, and staged
runner all have 26,509 bytes and SHA-256
`2b2a33de45490d124f0828f0e1de15e5c57c91facd326fd4ae054027c7952f4d`.
Thus this runner logic is inherited; this evidence does not locate its first
historical introduction or prove prior executions free of the defect.

Inspected stdlib pins:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `D:\Python314\Lib\ntpath.py` | 31,768 | `1cba5dfc7442371d1fe7ab83120496c4f7c17abb1f35ec54fa6e517c0525582e` |
| `D:\Python314\Lib\pathlib\__init__.py` | 48,114 | `208546aa566ca8df4b8e1259f30209c0f803c3f920e6d080ae1b10d53d05bd72` |

## What actually failed

The package command exited zero. The support-build command exited one before
any node initialization or network connection. Its first recorded child is
`build-BootstrapSupport`. The failure traceback points to the active-child
polling call at `run_stage.py:391`, and the explicit raise at line 47:

```python
for number, p in enumerate(path.rglob("*"), 1):
    if number > MAX_STAGE_ENTRIES or not p.resolve().is_relative_to(path.resolve()):
        raise RuntimeError("SELECTED_STAGE_ENTRY_OR_PATH_LIMIT")
```

The constant is 4,096. This particular exception proves one of the two
disjuncts evaluated true; it does not record which one. It is not the separate
selected-stage byte-limit condition. It is also not evidence of Lean rejection,
mathematical unsoundness, or mixed-catalog behavioral failure.

The affected child row remains `RUNNING`, without a recorded exit code. The
runner caught the exception, performed cleanup, and retained its failure. Final
Job accounting reports zero active processes, zero terminated processes, and
21.875 CPU seconds. The endpoint census succeeded and reported 5,571,286 bytes.
Stage wall time was approximately 44.700 seconds. The outer preparation reports
32.625 Job CPU seconds and approximately 46.622 seconds wall time.

These successful cleanup observations do not convert the failed build into a
successful build. In particular, the presence of an `.olean` does not establish
the interrupted command's exit status or the completion of later support steps.

## Retained tree inspection

The stage root is a normal directory. The subsequent read-only enumeration has
14 entries: four directories and ten files. None is reported as a reparse
point or a link by this enumeration. Files and sizes are:

| Relative file | Bytes |
| --- | ---: |
| `00.stderr.log` | 0 |
| `00.stdout.log` | 0 |
| `plan.json` | 3,268 |
| `run_stage.py` | 26,509 |
| `stage.json` | 6,766 |
| `input/domains.py` | 4,934 |
| `input/native/AgentClient.lean` | 12,550 |
| `input/native/AgentReplayCore.lean` | 27,641 |
| `input/native/BootstrapSupport.lean` | 46,420 |
| `out/lib/BootstrapSupport.olean` | 5,444,408 |

The directories are `input`, `out`, `input/native`, and `out/lib`. Final receipt
writes explain why a later filesystem total need not equal the earlier endpoint
byte count.

This tree does not reconstruct the tree during the failing poll. It therefore
cannot exclude transient entry-count excess, a transient genuine resolution
outside the stage, or a disappearing compiler file. No offending path is in the
receipt, and no compiler temporary filename has been established by this read.

## Reachable false-rejection mechanism in the installed stdlib

The parent's investigation identified the following branch. Independent source
inspection confirms it:

1. `Path.resolve()` delegates to `os.path.realpath()` and constructs a new path
   from the resulting spelling (`pathlib/__init__.py:932` onward).
2. On this Windows implementation, `ntpath.realpath()` first calls
   `_getfinalpathname(path)`. A successful call sets `initial_winerror = 0`.
   The returned spelling carries the extended `\\?\` prefix.
3. If the original input lacked that prefix, `realpath()` constructs an ordinary
   spelling `spath` and calls `_getfinalpathname(spath)` again before stripping
   the prefix (`ntpath.py`, approximately lines 696-732).
4. If the second call raises `OSError`, the prefix is stripped only when
   `ex.winerror == initial_winerror`. A file disappearing between successful
   first resolution and the second lookup can produce error 2 or 3, not zero.
   In that case the function returns the already obtained extended spelling.
5. Meanwhile, a stable root can resolve to the ordinary spelling because both
   root lookups succeed.
6. `Path.is_relative_to()` is lexical ancestor comparison; it is not a fresh
   filesystem-identity check (`pathlib/__init__.py:498` onward). Windows path
   ancestors with drive `\\?\E:` do not equal a root with drive `E:`.

Consequently an actual descendant can be represented as
`\\?\E:\stage\out\temporary` while its root is represented as `E:\stage`.
The original containment expression can return false solely because its
operands use different namespaces.

This is a conditional source-level demonstration: **if** those ordered lookup
outcomes occur, this false rejection follows. It is not evidence that those
outcomes occurred during preparation01. Neither the failure receipt nor the
retained files records them. Merely catching `FileNotFoundError` around `stat`
does not address this branch: the second lookup error is caught inside
`ntpath.realpath()`, which returns a path instead of propagating that error.
Using `resolve(strict=True)` alone does not remove this particular second-lookup
branch either; its `except OSError` is independent of the initial strict-mode
exception selection.

## Smallest useful bounded discriminator

Before any compiler retry, authorize one separately allocated native-free test
against the pinned Python interpreter and stdlib. It should import only the
required stdlib and selected test code, perform no network activity, and avoid
modifying the failed allocation.

Use deterministic mocking of `ntpath._getfinalpathname`, not a probabilistic
rename race. For an ordinary absolute child spelling, return its extended
spelling on the first lookup and raise a Windows `OSError` with `winerror = 2`
on the ordinary-spelling recheck. Resolve the root stably. Assert all of:

- The exact installed `Path.resolve()` returns the extended child spelling.
- The exact existing `resolved_child.is_relative_to(resolved_root)` is false.
- A proposed same-namespace comparison returns true for this genuine descendant.
- The recorded mock-call sequence matches the proposed branch; unexpected calls
  fail the test instead of inventing additional successful behavior.

Also test error 3, the stable no-race descendant, reversed namespace spellings,
and both operands already extended. A direct pure-path example alone is
insufficient to demonstrate the stdlib transition; retain both the lookup
transition and the resulting comparison evidence.

An appropriate narrow regression suite additionally requires rejection of:

- A resolved sibling with a shared string prefix, such as `stage-other`.
- A resolved target outside the root, including a simulated symlink/junction
  target. Compare the resolved target, never just the original in-stage name.
- A different drive, different UNC server/share, or unsupported device namespace.
- More than 4,096 enumerated entries.

Retain existing byte accounting and the narrow disappearance handling around
file type/size observation. Neither namespace canonicalization nor a missing
file observation may become a general exception-to-acceptance rule. Test
non-disappearance errors as errors. This is not a claim of hostile filesystem
race isolation; the runner explicitly trusts the owner/runtime and has that
limitation already.

## Candidate repair boundary, conditional on the discriminator

The targeted repair is a comparison-only canonical representation of
**already-resolved** absolute Windows paths. One conservative approach is to
promote ordinary DOS paths to the extended DOS namespace and ordinary UNC paths
to the extended UNC namespace, while preserving recognized extended forms.
Reject unrecognized device/volume forms unless explicit support and tests are
added. Preserve path components and use ancestor comparison, not string prefix
comparison. Do not remove `\\?\` from paths subsequently used for I/O; doing so
can change Windows name semantics. Do not collapse arbitrary device prefixes or
equate distinct resolved targets.

This keeps resolution of links in the decision and fixes a representational
mismatch, not a lack of trust in the result. Apply the same comparison rule to
the census and selected-output census if a successor is selected; do not leave
one endpoint with the original mismatch. Root should decide whether other
containment callers belong in that narrowly reviewed successor. Product changes
require a new selected source, not editing the frozen source08 or its used
installation.

Split entry-limit and path-limit errors and retain a bounded offending entry,
enumeration count, and both resolved spellings on path failure. This would let a
future failed attempt discriminate alternatives without expensive blind retries.
Such diagnostics must remain within the receipt-byte limit and avoid private
contents. No new diagnostics can reconstruct the absent observation in the
existing receipt.

## Decision

Preparation01 remains failed and retained. A small deterministic test is
justified because a concrete source-level false rejection has been identified
in the exact installed stack. A narrow successor fix is justified only after
that mechanism and escape-rejection behavior pass independent review. A later
successful build would qualify the later bytes/workflow; it would not prove
this failure's historical cause. No additional native execution is recommended
merely to make the current failed record turn green.
