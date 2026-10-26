# Materialization refusal: causal source screen

2026-10-26. `practical_library_route`. Source/saved-data analysis only, after
root reported the terminal `std-materialize01` failure. No retry, timing test,
cap increase, package/native call or owner-state access was performed here.
The independently assigned outcome reviewer owns actual closure/pin auditing.

## What the evidence establishes

The materializer reported `FAIL`, phase `BIND_ONCE`, error
`STD_MATERIALIZE_FIXED_90_WALL_70_CPU`, at 70.015625 process CPU seconds and
79.04565110011026 wall seconds. Its outer result reports `COMMAND_FAILED`,
70.515625 inclusive Job CPU, 592408576 peak Job private bytes and clean closure.
The guard stopped the operation before binding returned, hence before the
unit-writing loop. This is not an fsync/write-cost failure. No complete inert
baseline exists, and the strict public selector correctly refuses this result.

The prior retained diagnostic completed the same frozen binder with a measured
28.125 process CPU seconds inside binding. Its whole inner process cost was
31.015625 CPU seconds; the separate outer Job cost was 31.078125. The old
28.125 value is an observation, not an execution-time bound or entitlement.

## Compared source paths

Both operations load the same four helper modules and adopted binder, use the
same exact writer/inventory/request, and call:

```text
B.bind_writer(writer, inventory, expected_targets, check_budget=budget)
```

The new `budget` and old `budget` perform the same cumulative `monotonic` and
`process_time` comparisons. The materializer prefixes an exception's message
only when `need` fails; successful callback calls do not concatenate strings.
The binder calls the callback per selected name/unit/batch/manifest entry,
not inside each expression-node walk or byte of the lexical parser. Therefore
the new callback body does not identify a credible deterministic 40-plus-second
increment. No additional binder pass was introduced.

New pre-binding work is the tiny pinned-helper load, 468097-byte saved-manifest
read, and creating two fresh directories. The 708-file partial check was also
present in the old diagnostic. The common clock origin now includes helper
bootstrap explicitly, but this small difference cannot itself explain the
observed scale without additional evidence. New complete output checks/writes
occur only after the failing call and did not run.

The preserved terminal report contains no binder-internal phase or progress
census. Thus it does not identify whether writer decoding, evidence inspection,
portable encoding/decoding, or a later step consumed the allowance. CPU seconds
are not invariant instruction counts: processor frequency/core placement,
memory/GC behavior and contention can change them. None of these is established
as the actual cause. Do not label the failure a slow filesystem, memory shortage,
callback defect, or implementation regression solely from these two reports.

## A potentially better route, not an implementation selection

The original diagnostic already retained an independently reviewed exact
manifest. Reconstructing its missing bytes is a narrower problem than producing
and validating a new general baseline manifest. The current materializer repeats
general writer and portable lexical validation even though both its input writer
and desired per-unit output hashes are already pinned.

A possible test-only reconstruction could:

1. Check the exact retained writer, inventory and manifest identities.
2. Decode the already-pinned writer with the standard JSON decoder; preserve
   bounds and one-pass unit ordering. This is not an untrusted general parser.
3. Reuse the unchanged inspector only to obtain exact external references;
   construct each unit's imports from exact already-bound outputs and the fixed
   basis. Use the saved ordered manifest entry as the expected unit identity.
4. Canonically encode each portable unit and require its exact saved raw length,
   SHA-256 and domain-separated UnitID before exclusive writing. Compare retained
   partial bytes as well, with final complete census and unchanged-input checks.
5. Fail on any mismatch. Keep all mathematical acceptance in later unchanged
   strict public intake; never treat restored hashes as native acceptance.

For a fixed desired hash `h`, reconstruction correctness is simply
`SHA256(reconstructed_bytes)=h` under the same collision-resistance assumption
already used by the manifest. An imperfect reconstruction procedure cannot
silently supply a different manifest-selected object without a hash collision;
it can only fail or produce the exact selected object. This removes the need to
repeat arbitrary-input lexical validation during this specific restoration.
It does not justify weakening the public producer or receiver.

This route eliminates the general Python byte-by-byte scans of the roughly
38 MB known writer and 45 MB freshly re-encoded portable output, as well as the
portable reparse. Unit inspection and actual filesystem costs remain. No runtime
bound or completion prediction follows. A source-level operation-count reduction
is stronger justification than rerunning the unchanged failure or raising caps,
but root must decide whether this finite input-preparation work is worth doing.

The simpler alternative is to stop this rich-library discriminator and select a
different core task. Repeating native extraction, adding a certificate mechanism
or privately editing owner state is unnecessary. No repair is commissioned by
this note; all used failed/successful sources and evidence stay frozen.
