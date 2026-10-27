# Independent review of the retained-prefix status selection

Disposition: **GO for the one exact proposed public status operation**, subject
to root's fresh-output and exclusive-owner check immediately before launch.
This is a source and input review, not evidence that status has run or that the
full library intake succeeded. No product import, owner invocation, database
access, native execution or Git operation was performed by this reviewer.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root retains execution, result adoption and all state-operation ownership.

## Exact reviewed inputs

| Input | SHA-256 |
|---|---|
| `experiments/v5-local-checks/std-kernel-prefix-status01.selection.json` | `7c262debd658e1c6443dd9cd1e8b211e1704303b0422a3e1b3487b18d70b1084` |
| `software/v5/ordinary_kernel_admission/PREFIX-STATUS-PLAN.md` | `9505e7c3666569d90a2fbc4a351e7e87283f6ea4f0e3e7f357e9c334aed20173` |
| Existing status template | `6a78055e685335a845edc09f0a1e3e493e9b39e3312b32075134e067c92eff5f` |

I independently hashed all **232 external pins** and **three source files**;
all match. The source snapshots total 12,226 bytes; the plan is 6,416 bytes.
External pins partition into 154 current package files, 23 external runtime
files and 55 evidence/binding/artifact files. The complete on-disk package
census equals the selected map: **154 files / 39,316,958 bytes**, with no omitted
or additional file. No mutable database, journal, lock or WITHDRAWN marker is
pinned as an unchanged input. The two retained snapshot pins total
**2,820,152 bytes**.

The package PROFILE hash is
`60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b`;
its installation binding matches
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.
All 117 PROFILE file entries and 36 installation entries match their lengths
and hashes, resolving the installation's nine external Python/Lean entries to
the selected runtime roots. The outer runner's frozen supervisor manifest and
its three loaded source files also match their embedded expected identities.
This is an explicit input identity check, not a hermetic-toolchain proof.

The fresh output `experiments/v5-local-checks/std-kernel-prefix-status01` was
absent at the final review check. Both source count and external-pin count fit
the runner's existing 256-entry limits. All paths use the canonical root,
apart from the explicitly selected Python runtime `D:\Python314`.

## Command and cost boundary

The 40-token argv differs from the prior status template only in package path,
PROFILE, catalog, custody, store ID and selected context root. It retains the
existing `run.py ... owner -- status` route, `--limit 4`, diagnostics in fresh
output, and the snapshotted custody quota. Outer limits are identical to the
template: **60 wall seconds / 20 Job CPU seconds / 768 MiB / two processes**;
the public launcher retains **35 wall / 10 CPU / 512 MiB / one process**. Each
stream is limited to one MiB. There is no baseline-intake, native-worker or
new-initialization argument.

`Run-V5-Check.py` verifies external pins before and after the command, snapshots
the exact three source files, refuses an existing output directory and checks
the unchanged selection and saved snapshots afterward. Public and outer Job
supervision remain the hard process boundary; the owner's own Allowance checks
are cooperative. Hashing the explicit external pins and loading support also
have costs; this review does not treat status as free or guarantee completion
inside its unchanged envelope.

## State semantics and backup decision

The exact package source supports the plan's distinction between a bounded
public status operation and a read-only database open:

- `owner.py:233` enumerates at most `limit + 1` roots and calls
  `catalog.context` only on the explicit selected root. Its status branch
  (`owner.py:521`) launches no native worker. Cleanup closes owner and custody,
  and a close error forces `ok=false` (`owner.py:612`).
- `portable_catalog.py:145` validates implementation/adoption and activation,
  takes the owner lock, enforces database and journal bounds, then opens SQLite.
  On ordinary existing activation it changes residual RESERVED operations to
  INTERRUPTED (`:238`). SQLite may recover its bounded rollback journal. The
  operation consequently need not preserve database bytes.
- `portable_catalog.py:530` checks the selected chain back to its basis.
  `_validate_record` checks native root/request/operation binding and COMMITTED
  status; `_context_rows` checks parent-module order, no name shadowing and
  context limits. `_artifact` hashes actual retained snapshot bytes. None of
  these status paths replays mathematical proof steps.
- `ordinary_admission.py:692` quarantines uncertain native cleanup, but after
  observed clean closure calls `catalog.abandon`. That function marks the live
  failed operation FAILED_RETAINED while preserving files and charges
  (`portable_catalog.py:780`). Normal status does not delete accepted roots or
  rewrite their artifacts, and refuses a withdrawn catalog.
- The actual ordinary custody implementation is
  `support/transport/ordinary_acquisition.py`. Its open validates the exact
  semantic/quota configuration and bounds; `status` reads stored meta counters
  (`:147`). It does not scan or mathematically validate all custody payloads.

The retained intake evidence records both native outcomes and clean process
closure, unlike the earlier interruption with an unknown native outcome.
Therefore the plan's **no additional whole-state backup** recommendation is
reasonable for this specific public recovery check. Source imposes no such
backup prerequisite. Exclusive ownership, retained immutable artifacts and
saved failure evidence remain premises. Do not privately inspect or alter the
database, remove locks/journals/WITHDRAWN, or copy state merely to bypass a
refusal. Preserve a failed status and stop for a new decision.

## Required interpretation of the new result

Success must bind the actual store
`fb625cc1b7d03d081e45bbcf73f7d59765f04a64a402484f23d00ac3e60ce4e7`,
implementation
`86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea`,
basis `4d7cc70e515293b3037a8fa34f60fa97fe082196e005aa7cd894204464ca5f2b`
and selected prefix
`c3d0f6209f42abdc98a6975a358545b0d61701e849b6ed0a3e69bdc1b7f400f6`.
Expected context is **1,743 names / two modules / 2,820,152 artifact bytes**.
Expected inventory is precisely the basis and prefix, with the proper parent
edge and `has_more=false`. Require the plan's exact catalog/custody/quota
bindings, `ok=true`, LOCAL_OWNER_OPEN, non-null selected context, zero worker
CPU, empty stderr, no close errors and clean public/outer closure.

An extra/missing root, different context or exhausted limit is a distinct
outcome requiring assessment, not permission to choose another root or renew
an allowance. A successful status would establish current protected local
context eligibility only. It would neither turn the failed full intake into a
success nor clear its historical `possible_unreported_commit=true`. Suffix
partitioning and continuation remain separately selected work.
