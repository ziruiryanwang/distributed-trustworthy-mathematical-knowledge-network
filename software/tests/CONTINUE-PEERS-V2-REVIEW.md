# Continuation v2 delta and exact G02 launch review

## Verdict

**PASS for the narrow v2 source delta and exact G02 launch below.** The change
repairs the observed legitimate-source-refusal accounting path and preserves
authenticated command-level quiescence. No positive-path launch blocker was
found. A remaining conservative service-error reporting edge is explicitly
recorded below; this is not universal failure-accounting qualification.

Reviewer: `feasibility_checkpoint_audit`. The complete original-to-v2 source
diff, changed functions in surrounding context, full v2 contract, exact launch,
new author envelope and complete frozen source were read. Direct changed-input
and lineage pins were independently checked. This builds on the full original
source review and failed-G outcome audit, without repeating the unchanged
214-file transitive review. No Python execution/import, compilation, Lean,
product command, SQL/database inspection, port binding or service was performed.
Only this Markdown review was authored.

## Exact reviewed cut

Paths below are relative to
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `software/tests/continue_peers_v2.py` | 35518 | `a3d0c3b1dd985bb00d3e87dcd097f3c48ae7023b1422e373e52262d6d8416ca4` |
| `software/tests/CONTINUE-PEERS-V2.md` | 8515 | `3fa8056b751d4f748f1cd6a97b1945d15427b2d9ceda9b886101e8fe4b137b49` |
| `software/qualification/peer-g02-launch-01.json` | 2206 | `0f6ba6d71f0d1e5e8ff795a0f927833ce80e577eeace606dc061ae9b119da8da` |
| `software/qualification/peer-01-alpha-author-02/authoring.json` | 418 | `2cc1ac518edc6282320b800ca2bc29a1367d4e69496687d1ab3ca10b1636d12f` |
| `software/qualification/peer-01-alpha-author-02/G.lean` | 2055 | `0028d848359b95b501abe4d511c7bb3ba3b4992a27237e37eb752288117071bf` |
| `software/qualification/peer-01-g/continue-failure.json` | 41977 | `f4d53942f1782c1771024a91450c2236ddf77a5662858cf7116c1711ed47627f` |
| `software/qualification/peer-01-g/OUTCOME.md` | 12259 | `9c3b2dd4705187cabe33875d0772ad4bcfc80c25563b6fbf3a4cd374128f4f47` |

The launch is schema 2, phase `g_to_beta`, attempt `g02`. Both `prepare` and
`previous` pin the successful 23416-byte preparation result with SHA-256
`1a9f6fdd9038dfb926e88aa3a689afaefc7b2c53323a023eb6da044e9a8fc6f0`.
The original failure is `STOPPED`, belongs to G, and selects that same
preparation. The outcome note is pinned as historical bytes, not interpreted as
an executable instruction, state repair or mathematical authority.

The helper and Python executable were independently rehashed and match the
successful preparation's pins fieldwise:

- `prepare_peers.py`: 25349 bytes,
  `1cb723af882f4e3fbb4c65425534cdd3ac9668aecf4dfaef2c05a8ee9b33c660`.
- `D:\Python314\python.exe`: 106208 bytes,
  `03168c01b7b7491423350e82c26fee71f35b43694d1319d3c668bda6903a0c38`.

The original coordinator remains unchanged at SHA-256
`eb86ae23bb95e5001d11c511754d242c4c0ca12723c321e7303c113b5e5ac554`.
The revised source is a separate author artifact, not an overwritten G source.
Its selected root remains `PeerAlpha.lift_injective_on`, and its context is
`context:968c1489dc6c20d37a9f0888e86403a7581496d300775e8d2ff34915065ce4d8`,
matching Alpha's prepared public info. Reading it does not establish that Lean
will accept it; that is the purpose of the allocated submission.

No reparse ancestor was observed for the inspected new coordinator, launch,
author/source or original-history paths. At review time the new evidence root
`software/qualification/peer-01-g02` and Alpha service session
`scratch/services/peer-g02-service` were absent. No port availability or fresh
public-state observation is inferred from that absence.

## Refusal-accounting repair

For an ordinary command, v2 now separates observed transport/work from the
expected successful workload:

1. `binding` validates the actual original supervisor's transport completion,
   direct-child reap, zero-active Job, absence of cleanup errors, exact request
   and response bytes/hashes, and normal event origin. It then preserves the
   command's authenticated quiescence label.
2. It validates actual counter types/ranges, stores `actual_work`, accumulates
   actual native stages and reported pipeline children, and accounts the unique
   enclosing Job's CPU. Missing optional checker counters remain `null`; a
   missing pipeline count with the checker loaded marks that observation
   incomplete. Nested native Job CPU is not added separately.
3. It writes the immutable binding before the aggregate-budget check. A budget
   refusal at that point cannot erase the cost already recorded in memory and
   the successfully saved evidence binding.
4. `request` records the public status/code. A non-`OK` response stops with
   `PUBLIC_REFUSAL:<code>`. Only an `OK` reply reaches `success_workload`, where
   the existing successful-stage/checker/pipeline requirements are enforced.

Consider the exact shape of the old failure: valid bound transport, one actual
stage, one pipeline child, and public `REFUSED / SOURCE_REJECTED`. Substituting
those observations into the new branch records stage 1, child 1 and actual
public Job CPU, persists the binding, and then fails as
`PUBLIC_REFUSAL:SOURCE_REJECTED`. The five-child success requirement is not
reached. This is a source-level branch argument, not an executed regression
test or a reuse of the old run as new execution evidence.

`failed_direct` now returns immediately if the command already has the
authenticated empty-Job/reaped-worker label. Therefore a later public refusal
or successful-workload mismatch does not replace that command evidence with
the old generic unknown-cleanup label. When no such binding was established,
direct wrapper cleanup retains its conservative uncertainty.

The earlier wrapper `result.json` remains a pre-binding snapshot. Later
`binding.json` and the aggregate success/failure command records contain the
additional observations. They must be interpreted in that order rather than
assuming every immutable file was written at the final semantic endpoint.

## Fresh attempt and retained history

The phase-to-attempt map is fixed: G uses `g02`, H uses `h01`. The coordinator
requires an exclusively new phase root and derives new public request/service
identities from `peer-g02` or `peer-h01`. It does not replay old G IDs, clear the
old evidence root, edit control rows, reset counters, refund charges or repair
source. G02 records explicit pins to the old failed run and its separate audit.

The original failure did not create a successful contribution. G02 therefore
checks public heads/snapshots/descriptions against PREPARE, while its baseline
physical census includes the retained failed request and stage. These are
different assertions: a stable mathematical view does not mean an unchanged
journal or unused resources. Fresh runtime `info` comparisons are still
mandatory; this read-only launch audit did not perform them.

The H branch was included in the diff review but no H launch is approved here.
It requires both original-history fields to be exactly `null` and a pinned,
successful schema-2 `g02` predecessor at the new G02 result path. That
predecessor retains the historical lineage. H source authoring and its exact
launch remain separately allocated future work.

## Unchanged positive path and limits

The source diff preserves the eleven public commands and two new native stages
per successful direction. It preserves the finite 120-second/two-connection/
64-MiB service grant, discovery-derived remote handle, candidate-only
acquisition, pre-admission head check, original service supervision binding and
the requirement that sender quiescence precede receiver admission. No new
product call is inserted to repair reporting.

The exact allocation remains 500 seconds per ordinary command, 1800 aggregate
active-wall and observed-CPU seconds, and 1 GiB selected retained data/evidence.
The coordinator and direct wrappers still have cooperative checks, not a new
outer OS container. CPU remains incomplete; malformed/missing/unbound evidence
and direct wrapper CPU are not promoted to fully accounted execution.
Current-attempt aggregates do not include old-attempt costs, but those costs
remain separately audited and the live node's consumed charges persist.

The installed product-copy checks are unchanged and must run before/after a
successful attempt. This narrow review does not redo the previous selected
source-set audit or substitute mutable development recovery code for the
retained installation. Same-host shared runtime and owner-local trust premises
are unchanged.

## Remaining conservative service-error edge

`service_finish` can authenticate a service binding and then fail before
clearing the `service` variable, for example at a later service assertion or
the binding's aggregate-budget check. The outer failure cleanup may re-enter
`service_finish`. A second binding/accounting attempt can fail due to the
unique-Job guard or an existing immutable record, or an already exceeded budget
can stop it earlier. The outer handler then sets the aggregate
`service_descendants` text to `UNCONFIRMED` even when the command's preserved
binding already establishes actual quiescence.

This does not erase the v2 command-level binding, restart a service, authorize
admission, or create a false successful run. It is conservative but can produce
conflicting summary granularity. An outcome audit must prioritize the actual
bound supervisor facts and distinguish semantic failure from process cleanup.
Root was informed and accepted this limited reporting edge as nonblocking for
the bounded positive-path G02 attempt. No universal failure-path completeness
is claimed, and the stable reviewed source was not expanded again for it.

## Claim boundary

Root may consider one execution of this exact G02 allocation if its pins remain
unchanged. A refusal must remain a refusal, preserving diagnostics, costs and
all earlier evidence. No retry or source substitution is implied.

A successful G02 would still only be
`G_OFFLINE_ADMITTED_BY_BETA_AWAITING_INDEPENDENT_H_AUTHORING`. There is no
execution outcome in this review. Even later H completion requires independent
substantive-dependency audit and remaining controls before broader reciprocal
qualification; distinct result identity alone is insufficient.
