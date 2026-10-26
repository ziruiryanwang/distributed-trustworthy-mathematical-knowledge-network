# Direct intake guide: independent source review

2026-10-26. **SOURCE GO for this documentation-only public handoff.** Reviewed
`INTAKE.md`, SHA-256
`b0d8e19e74fef6167afc7bf432535ea10caf21f8d134b77a4e90229d7ce8bb5e`.
No command, product import, native checker, network operation or owner-state access
was executed. This is not an actual successful intake or full-v5 qualification.

The controlling source is the default package selected in
`../ordinary_release_bundle/ADOPTION.md`, under
`experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package/`.

- Its `run.py:160` accepts the `owner -- intake-baseline` token shape. The exact
  runtime/profile, state, parent and three bundle arguments in the example are
  allowed. `owner.py:372` requires the parent and prohibits `--output` for this
  operation; `:374` requires all three bundle arguments. The guide complies.
- The guide correctly uses fresh diagnostics and the owner report from
  `child/stdout.txt`, not a fictional intake output directory or exported helper
  report. `run.py:347` retains separate supervision and run reports.
- Parent mappings match `owner.py:520` for init, `baseline_intake.py`'s complete
  `local_root`, and existing receive/contribute admission roots. An explicitly
  selected receiver root is not inferred from sender state, publication metadata,
  the newest branch or an export report.
- Success checks bind the receiver/profile, selected parent, manifest hash,
  `BASELINE_INTAKE_COMPLETE` and final root. They also require the actual launcher's
  `CLI_EXITED_ZERO` and closure fields matching `run.py:280`. The owner sets
  `ok=false` on its close errors (`owner.py:631`); those errors are also explicitly
  checked by the guide. The guide does not treat exported inert bytes as accepted.
- Root requested two conservative guard additions after the initial review:
  explicit `SUPERVISION.termination_requested = false` and the launcher's
  `profile_sha256` equal to the chosen receiver profile. Both appear in the final
  reviewed bytes above; `run.py:331` supplies that profile field. The original
  report/schema conclusions are unchanged.
- `baseline_intake.py:30` sets the default batch CPU reservation to 60 seconds;
  its `capacity` check requires strictly more than the sum of those batch
  grants plus controller work. The example's warning that 120 CPU seconds is not
  sufficient authorization for two batches is correct. It does not guarantee
  that its sample allowance fits a particular mathematical input.
- The completed result has `batches` and `local_root`, not a receive-style
  `admission`. On `IntakeError`, `owner.py:610` preserves the error's report as
  `detail`; its `BASELINE_INTAKE_STOPPED`, `last_confirmed_root` and possible
  unreported commit do not mean rollback or completed whole-bundle admission.
  The guide distinguishes these cases and avoids automatic retries.
- The returned targets feed direct publication only after successful destination
  intake and with the new receiver root. Matching the helper manifest identifies
  selected locators; actual `peer publish` still validates their local accepted
  bindings. No report relabeling or portable producer warrant is suggested.
- The guide preserves whole-custody disclosure, local operational-report privacy,
  approved-runtime/source boundaries and the current no-publication constraint.

No blocking CLI, report-binding or partial-acceptance error was found in this
bounded review. The new guide fills the specific missing direct-command vocabulary;
there is no need to change code, the frozen README, the source archive or its pins.
