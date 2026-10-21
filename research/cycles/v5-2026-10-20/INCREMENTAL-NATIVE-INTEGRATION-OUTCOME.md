# Genuine incremental-native integration01: failed setup audit

2026-10-21, adaptive_audit. **FAIL before product imports, constructors or any
mathematical checking.** This is a preserved adapter-envelope failure, not a
receiver/product failure and not a successful integration. No rerun occurred.

Actual directory: `experiments/v5-local-checks/incremental-native-integration-01`.

| Retained artifact | SHA-256 |
|---|---|
| Saved selection | `1ee506eaede600f6d21cf881f86d3babb2c7fdac659a3a50d186da6bf2c93adf` |
| Owner input | `3611e1267d6f5d4906c6a2db79facda3f6c34e39a133d7524c8412a97240917f` |
| Outer RESULT | `ac760d671e3eb00e038144e216ad2450fb85571c4e45418107dfecc730668d6f` |

Read-only validation matched all119 selected original files and their immutable
snapshot copies, and all28 runtime pins. The exact source map is unchanged:
SHA-256 `d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0`,
actual/input-row size2,805,479 bytes.

## Observed cause and extent

Actual stderr terminates at `stage` line110:

```python
raw = read(pin(map_row, 2*MIB), 2*MIB)
```

`pin` raises `FILE_PIN_SHAPE` because2,805,479 exceeds2MiB=2,097,152. The
reviewed adapter incorrectly applied the per-source-file ceiling to the larger
distribution source-map JSON. The prior source GO missed that size mismatch.
The selection had correctly pinned the actual map and did not authorize a
different/smaller input.

This occurs before selected-code directory creation and before product imports,
TrustDomain creation, ReceiptVerifier or MixedDeltaVerifier construction.
Directory inspection confirms no selected-code, trust, mixed operation or
integration-result artifact. The earlier setup only inspected selected local
assets/runtime/retained packet bytes. No native or receipt verification, live
admission handle, warm reuse, new certificate or network operation occurred.

## Actual costs and closure

The outer status is `COMMAND_FAILED`, exit1, with child reaped, Job closed,
no cleanup errors, no termination request and0 final active/terminated
processes. Original90CPU/180wall/512MiB/four limits were unchanged.

- Actual Job CPU:0.40625 seconds.
- Runner wrapper CPU:0.578125 seconds.
- Known combined CPU:0.984375 seconds.
- Whole runner wall:2.696222399827093 seconds.
- Supervised wall through cleanup:0.893883400131017 seconds.
- stdout/stderr:0 /1742 bytes.

No authority was provisioned, so no trust withdrawal or owner cleanup is missing.
The outer process closure is clean even though the operation failed.

## Decision

Preserve used adapter `d6445354`, its selector/input/allocation and this failure.
The narrow prospective correction is a fresh adapter with an explicit exact
MAP_BYTES=2,805,479 check/read ceiling, not a general increase of object limits
or new product changes. Fresh source review and root selection are required
before another run; no automatic retry, budget renewal or old evidence rewrite
is authorized here. No mathematical, cache-integration or growth claim follows.
