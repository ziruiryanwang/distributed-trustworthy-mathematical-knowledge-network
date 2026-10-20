# Interface consolidation: independent saved-build audit

2026-10-20, core_release. **PASS for the selected directory build and exact
SDK-map consolidation.** No test, build, proof, native call, Git mutation or
second full-payload verification was run by this reviewer. Final v5 remains
unfinished; installed startup is a separate gate, not claimed here.

## Adoptable release identity

- Directory: `product-local/v5-distribution-interface-01/Mathematical Commons v5`.
- `V5-RELEASE.json`: 2,364,109 bytes, SHA-256
  `c249d086928e62a00ec194f1b556c6cffa918c1106159102e32a8617c9fbadf0`.
- Payload: 9,853 files / 842,249,173 bytes, exactly matching saved builder output.
- Selected input SHA-256:
  `a0d5fad85893bdda55ae10530cd59bc513d4fe90654a2b0661aad624793159b2`.
- Build selection and saved copy both SHA-256:
  `91cd374c422c9c6008054c2abc72fe2cd75fcc46d5252e200adf8f731c9dcae1`.

The two selected source files match both their current and saved-snapshot pins.
The reviewed builder `ea3df90064ce7e759b311b95ba63d4486d7c8fd0b949de714fe37a85d77ea0bc`
also matches the installed entry. Source review `0edbd02f` remains unchanged.

## Exact map, not another full installation readback

Compared every manifest row against the retained connected release
`69d9456eb53135061bc68a8d657ae0f25bc71013cd9c8d2cd5f571c4c7996ef5`.
The only differences are:

- Replaced: `distribution.py`, `README.md`;
  `sdk/v5/mixed_claims/imports_atomic.py`, `authoring_atomic.py`;
  `sdk/v5/client/workspace_evidence.py`, `workspace_staged.py`,
  `semantic_reader.py`; `sdk/v5/transport/semantic_staging.py`.
- Added: `sdk/v5/mixed_claims/interface_projection.py` and
  `sdk/v5/transport/declaration_resilience.py`.
- Removed: none. No other payload row changed.

Independently hashed these ten changed/added payloads; all match the manifest.
All 108 SDK rows match byte length and SHA-256 in successful actual integration
plan `99492605f7b1c868f4661f614db7f764a81fd0c4a4a391d882855ad6adf1aa96`.
The map contains exactly its 108 SDK entries, with no owner-adapter inclusion.
The 87 preparation source pins equal all installed v5 Python rows; the remaining
21 portable SDK rows are unchanged. Preparation differs only in those derived
source pins. All other preparation settings, binary/support rows, release
schema, base role/manifest, role paths and aggregate image are unchanged.

The selected input differs from the retained connected input only in
`distribution_source` and `sdk_sources`. Thus no new mathematical policy,
foundation, I/A image, native checker or Lean runtime was introduced.

The saved builder reports `DIRECTORY_CREATED_AND_EXACTLY_VERIFIED` only after
`verify_release(..., full=True)`: exact census, every payload pin, then exact
base-role projection. Its exit-zero evidence supports that full readback;
this audit intentionally did not repeat the 842 MB verification.

## Saved execution and costs

`experiments/v5-local-checks/distribution-interface-build-01/RESULT.json`
records the selected input/output argv, exit 0, empty cleanup errors, reaped
direct child, zero final active processes, closed Job and no termination request.
Stdout is the single 350-byte successful result; stderr is empty.

- Worker Job CPU: 33.234375 seconds.
- Total wrapper CPU: 0.90625 seconds (includes inner supervision 0.65625;
  do not add that inner figure again).
- Known combined CPU: **34.140625 seconds**.
- Total saved wall time: **203.5330866 seconds**.
- Original limits remain 120 CPU / 300 wall seconds / two active processes.

Evidence identities:

| Saved file | SHA-256 |
|---|---|
| RESULT.json | ebe326e9df21ffeb4bd7726887b4c1493a049885e2c2e2e2c16f244a03598850 |
| command/stdout.txt | b0408c3c65024ae53c0d5d8006d6e3d78387d8f060e89fb32a9e2f8da1232baa |
| command/stderr.txt | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |

This qualifies packaging identity and saved clean completion. It is not a new
mathematical acceptance, speedup measurement, full-cost growth result, or public
deployment qualification. Root may use the release digest above for the
separately reviewed installed zero-work startup selection.

## Subsequent installed startup outcome

2026-10-20, separate saved-outcome audit: **PASS for installed source origins,
real owner pins and zero-work lifecycle.** This section follows the build audit;
it does not retroactively change what the build alone established.

The selected request `b046a7ce829bf8d1e5e50f9a2cb3f58e76807949f5cf455046a10bae9ccddfe1`
used public installed `launch ... run` on release `c249d086`. Its preserved
operation is `product-local/v5-distribution-interface-01/startup-operations/installed-interface-startup-01`.
The generated plan SHA-256 is
`dc6e71c3ce1f8f1b09d52565abbc5931b11b72cd1ea94f0a79911f47a627046f`.
Every one of its 108 SDK map entries matches the adopted manifest; its only
additional source is the reviewed 8,773-byte owner `3c7249be`.

The saved owner result is `COMPLETED`, with no primary or cleanup error. The
eight changed/new loaded module paths point to that operation's source snapshot,
not development files or the prior installation. Their bytes and digests were
independently checked against the adopted manifest. The reviewed adapter's
executed checks establish their membership in the actual receipt, aggregate,
mixed and preparation owners, and the projection helper in the client guard.
The runtime contains 87 v5 Python sources. The bootstrap's imported-origin
record agrees with the eight reported modules and records `OWNER_EXITED_ZERO`.

The real client starts OPEN and ends CLOSED, with its acquisition, receipt,
aggregate, mixed and preparation owners closed; the workspace also closes.
Before and after closure: zero public calls, admission submissions, authoring,
imports, stores, publications, verification attempts and preparation worker
charge. Search, location and transport are absent. The ordinary foundation read
is accurately charged as 23,313 submitted input bytes; this is not literally a
zero-input operation. No mathematical or network work is inferred from startup.

The launch records exit 0, reaped direct child, zero final active processes,
closed Job, empty stderr/stdout and no cleanup error or termination request.
Known CPU is **9 seconds** (4.640625 Job + 4.359375 total wrapper), with
**11.204368 seconds** saved wall time. Bootstrap 4.296875 and supervision
0.03125 CPU are already inside wrapper accounting, not additional costs;
pre-clock interpreter startup remains explicitly unmeasured.

| Saved startup file | SHA-256 |
|---|---|
| RESULT.json | 47e17a3a713a8e4a4df39903eaade4473e0cd23bdb7ee2293abab58a189e3302 |
| BOOT-RESULT.json | a20cdd9d02276a8dd2ecca60f3d9cb6d9797befe051d992dbc95bc181f0785b3 |
| work/interface-startup-result.json | 308e7558dcf5344288c87b11c07ab8de2a2943247fa778e0da69ace8852367ad |

The installed consolidation now has its separate source-map/lifecycle gate.
Actual mathematical behavior remains supported by the earlier integration plus
exact source/runtime identity, not by this zero-work startup. No campaign was
replayed, no full installation rehash was performed, and full v5 is not complete.
