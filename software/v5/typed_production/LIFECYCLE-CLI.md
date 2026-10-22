# Typed lifecycle: separate snapshot and request commands

This trusted-local entry completes the existing producer's command boundary.
It creates neither mathematical authority nor funding and cannot run proof
stages. A local owner selects its inputs, source hashes and finite outer limits.
No network data is an instruction to invoke it. A report is not a certificate.

Use the selected isolated Windows Python (`-I -S -B`) with a separately selected
`lifecycle_operator.py`. Both commands take:

```text
snapshot | request
--source-root ABSOLUTE_STABLE_PRODUCER_ROOT
--entry-sha256 EXACT_ENTRY_SHA256
--profile PROFILE_JSON --profile-sha256 EXACT_PROFILE_SHA256
--input INPUT_JSON --input-sha256 EXACT_INPUT_SHA256
--owner-report FRESH_OWNER_REPORT_JSON
```

The entry's standard-library bootstrap verifies its own hash, all29 exact
producer-source pins and the existing `aggregate_small/operator.py` pin before
product imports. It rejects preloaded product packages, validates loaded origins
and rebinds the files. It does not add itself to the profile29, generate a profile
or import the consumer SDK. The selected source root must match existing profile
paths. The current retained producer root is the `software/v5` subtree below
`experiments/v5-local-checks/typed-production-controls-01/sources`.

## Snapshot: one execution capsule, no proof

For `snapshot`, `--input` is the existing generic configuration itself, schema
`DMKN_AGGREGATE_LIFECYCLE_SNAPSHOT_REQUEST_V1`; see [API.md](../aggregate_lifecycle/API.md).
Its profile-document pin must equal the CLI's complete profile pin. Supply the
actual packet pin, exact184-byte target J as368 lowercase hex characters, full
finite envelope and snapshot limits, fixed po18/stats geometry, and a fresh output
directory. This command does not select a target, synthesize a packet or infer
which mathematics is useful.

Also supply:

```text
--outer-selection {output}/selection.json
```

Run through `tools/Run-V5-Check.py`. The entry must be among that wrapper's source
pins and execute from `{snapshot}`; producer29 still loads from its stable root.
The copied selection is pinned at runtime and checked against the real original
argv, snapshotted entry hash, run name and input/profile pins. This intentional
late selection pin avoids a hash cycle: configuration/input hashes must not
contain the hash of the outer selection that already contains those input hashes.
The underlying lifecycle also requires configuration/profile/packet and all
adopted installation pins in the outer runtime map.

The entry invokes `prepare` and `snapshot` once each. Existing snapshot code
rederives exact preparation, checks parents and executes one guest layout. Its
limits are unchanged: at most180 worker CPU/60 controller CPU/240 wall seconds,
3,072MiB, two active processes and208MiB/288 output entries. The output reservation
includes both96MiB capsule/segment ceilings; choose caps that cover it rather
than assuming observed files determine reservation costs. The outer wrapper must
also cover startup, imports, constructor, closure and finalization.

Only a completed generic snapshot result plus clean owner closure and rebinding
earns `PASS_ONE_SNAPSHOT`. It still means an untrusted execution capsule. A raised
snapshot call records unknown host-dispatch extent unless the real result was
returned; it never reports that unobserved work as zero.

## Request: completed snapshot evidence to a pinned request

Invoke `request` separately, after snapshot's enclosing wrapper has actually
finished. `--outer-selection` is forbidden for this command. The pinned input is:

```text
schema = DMKN_TYPED_LIFECYCLE_REQUEST_ENTRY_V1
snapshot_evidence = {result, outer, selection, configuration, command}  # real pins
allowance_id
budget
checkpoints
prior_attempts
output_directory       # future fresh proof-stage directory; remains absent
stage_limit
carried_external_costs
request_output         # fresh file receiving the generated request
```

These are explicit ordinary producer options, not promises of resource adequacy.
The existing producer owns their validation and complete history. A new session
uses a new allowance; a same-session continuation preserves all prior attempts,
charges and successful checkpoints. No old costs or failed results are erased.

The entry calls `production_request` exactly once, which already performs its
full preflight; it does not call `preflight` again, quote through a private path,
or invoke `run`. It writes the request only after successful owner closure and
input rebinding. `PASS_REQUEST_CONSTRUCTION_ONLY` is not proof funding, a global
growth result or an assurance that the selected full-path envelope fits. A later
owner must inspect the actual request and applicable quote/policy, and explicitly
select the existing typed production `run` command if warranted.

## Output and failure contract

Both actions print a `DMKN_TYPED_LIFECYCLE_OPERATOR_RESULT_V1` report and, only
after establishing a safe fresh nonoverlapping path, save it. Inputs, source and
installation roots, snapshot/proof-stage directories, request file and report
paths must not overlap. Bootstrap failure with no safe report destination prints
failure but does not write to an unvalidated path.

Reports identify exact profile/input/entry and result/request pins, attempted
public calls, owner construction/closure and final rebindings. All claim zero
proof-stage dispatch and no mathematical admission/funding; actual snapshot
dispatch is separately recorded. Failure to construct, execute, close, rebind or
save is failure. A late failure creates `OWNER_REPORT.FINALIZATION-FAILED.json`
when safely possible, overriding the apparent owner report and generated request;
it does not rewrite either. If even the sentinel cannot be saved, stdout and the
nonzero exit remain failure evidence. Consumers must require the successful outer
operation, matching owner report and absence of finalization overrides before
using a generated request. No automatic retry or phase transition exists.

These are declared pinned local inputs and supervised resources, not an OS
filesystem sandbox. Existing cryptographic/checker assumptions and public-release
obligations remain unchanged. No test or actual lifecycle call is implied by this
source/documentation.
