# Ordinary execution consent: bounded source review

2026-10-25. Reviewer: `execution_consent_review`; adoption belongs to root.
Read-only source inspection plus this checkpoint. No imports, builds, tests,
network, database access, Git mutation or used-source edits were performed.

## Decision

The current public workflow already separates choosing mathematical data from
approving local executable code. I found **no traced peer-hint path that silently
converts a source suggestion into executable authority**. Another approval
mechanism, sandbox implementation or test campaign is not justified by this
review alone.

There is a small but consequential documentation improvement: the front-door
authoring instructions should state the actual scope of approval in one place,
including current-account privileges, transitive compiled dependencies, and the
risk to the same account's warranted local state. Existing warnings are correct,
but scattered across the operator guide, producer guide, launcher and source.
This is a consent-clarity gap, not evidence of a runtime approval bypass.

## Exact reviewed boundary

Package-relative references below use
`experiments/v5-local-checks/sparse-access-assembly01/assembled/package` under the
canonical root `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Rehashed `PROFILE.json`:
`97f93cc66f77ebcecd7a3a341baaaf4725236a8dec5fb9cee3c3e67d478f2834`.

The separate current network kit's `prepare.py` rehashes to
`bca0979abaf9bb7e8a233b1432b9307bab53a3dd2532654536be5cb4fe5ef811`;
`START-HERE.md` rehashes to
`559e71632d7d6bf6572fcbe98d878557de891f9fadaf2a600111986be114324e`.
This review also read the cycle's `ORDINARY-RELEASE-TRUST-BOUNDARY.md` and the
referenced predecessor operator/contribution and authoring-offer instructions.

## Source-backed consent trace

| Boundary | Actual behavior |
|---|---|
| Example/default | `software/v5/ordinary_operator_kit/examples.json:54` supplies `approve_local_project: false`. The new network kit reuses that ordinary contribution workflow; its own nine examples concern network operations. No existing producer consent is inferred from a network result. |
| Offline preparation | `software/v5/ordinary_network_kit/prepare.py:568` accepts an exact producer field set and requires `approve_local_project is True`. It emits a local project selection and `--approve-local-project`; it does not run them. Producer input has no authoring-offer/peer-report field. Extra fields are refused. |
| Actual public producer | `owner.py:75` defines a `store_true` flag, false when omitted. `validate_producer_arguments`, at `:267`, requires true and forbids state/unrelated arguments. `run_producer`, at `:285`, applies this gate before loading support. Hashing the project-selection file at `:305` does not create consent; the flag is separately required. |
| What selection pins | `authoring/py/library_extraction.py:86` binds the exact JSON, paths and modules. It deliberately does not census/pin every transitive compiled artifact. `baseline_production.py:216` records `OWNER_APPROVED_PATHS_AND_MODULES_NOT_TRANSITIVE_ARTIFACT_PINS`. Changing referenced files without changing the JSON does not change its digest. |
| Actual export execution | `authoring/py/baseline_production.py:226` launches the selected local worker and fixed exporter under the existing budget. `baseline_worker.py:101` filters selected environment variables, fixes executable/argv and preserves the current OS principal. It does not establish filesystem/network permission isolation. `PRODUCER.md:72` explicitly says artifact approval remains essential even with `loadExts := false`. |
| Separate source-authoring lane | `owner.py:499` selects project-authoring only from explicit local arguments and exact JSON. `ordinary_contribution.py:61` describes imported code/plugins as trusted, executable, not completely hashed. Its source/default lane invokes `author_worker.py` at `:485`; the project lane is separately selected. `author_worker.py:19` compiles source; `:41` adds approved project imports/cwd. Both execute with inherited permissions. No Lake build, dependency retrieval or installation occurs here. |
| Approval flag is not universal | `owner.py:359` rejects production-only approval flags for other operations. `contribute --source` and optional `--project-authoring`, and `extract-project --project-extraction`, are explicit local executable selections under their own contract. `owner.py:464` states that extraction selection is a local controller choice, not a token from a peer. Do not tell users that the producer flag is a universal source-execution gate. |
| Peer offer retrieval | `peer_api.py:922` initializes `execution_approved=False`, then returns `UNVERIFIED_AUTHORING_ASSOCIATIONS`. `support/transport/ordinary_acquisition.py:424` fetches bounded offer data only, with no source access or custody retention. The repository is a returned locator, not subprocess input. |
| Kit's offer route | `prepare.py:540` uses preview identity and explicitly supplied contacts to prepare a lookup. It neither generates producer/project paths from the returned repository nor changes producer approval. `ordinary_operator_kit/AUTHORING-OFFERS.md:185` separately requires approval before source retrieval/execution. |

No direct producer-to-acceptance shortcut follows from approval. The operator
guide's produced status is `PRODUCED_INERT_BASELINE_NOT_ACCEPTED`; independent
intake remains necessary. Approval asserts permission to run code, not that
its exported mathematics is correct. Conversely, subsequent mathematical
checking cannot undo file, credential or network effects of previously executed
source.

## Existing documentation is materially sufficient in these respects

`ordinary_operator_kit/START-HERE.md:189` explicitly instructs setting approval
true only after accepting execution/loading, and warns that resource caps do
not protect against approved hostile code. Its `:267` excludes hostile
same-account path replacement. `PRODUCER.md:23` calls the flag execution approval,
not mathematical trust; `:38` distinguishes selection hashes from transitive
artifact pins. `LAUNCHER.md:107` excludes a filesystem/network sandbox and
hostile same-account protection. The network guide `:171` says source suggestions
are not execution approval. These are not missing controls that need to be
reimplemented.

The smallest useful addition is a concise successor/addendum at the immediate
contribution entry, not a rewrite of the frozen tested kit or archive:

> Approving a local project means trusting its source, build/import code and
> transitive compiled artifacts to run or load with this account's permissions.
> The selection hash pins paths and module names, not all files those paths
> resolve to. Keep that trusted material stable through use. These processes can
> access the account's accessible files and network, including commons catalogs,
> snapshots and credentials; a different folder and CPU/RAM limits do not
> isolate them. A peer offer or a true theorem never grants this approval. If
> that trust is unavailable, do not run/import the project in the commons owner's
> account. Use an independently protected environment and transfer only inert
> outputs for independent intake; this package does not provision that isolation.

For precision, distinguish source compilation/build execution from the producer's
compiled-artifact loading: the producer does not itself invoke Lake hooks or
arbitrary project source. Nonetheless untrusted native artifacts cannot be
made safe merely by describing the operation as an export or disabling extension
loading. A future public guide should not erase that distinction.

## Result and limit

**No concrete silent peer-to-executable-authority path found; targeted consent
clarification recommended.** Conditional mathematical acceptance still requires
the trusted implementation and protected local-state premises stated in the
companion trust-boundary audit. This result establishes neither exploit absence
nor full release readiness. It selects no additional experiment or mechanism,
and leaves all used sources, package bytes and evidence unchanged.
