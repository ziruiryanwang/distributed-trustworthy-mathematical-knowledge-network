# Launcher integration: controls and file-map audit

2026-10-28. Read-only review of root-executed
`experiments/v5-local-checks/frontier-launcher-controls01` and
`frontier-launcher-package01`. **The focused parser controls and exact package
overlay pass their stated scopes.** The substantive public-launcher contribution
remains a separate operation; no mathematical or full-v5 acceptance follows.

The actual controls report all seven planned groups: valid forwarding preserves
the actual parent and tokens; malformed frontier hex, duplicates, missing/equals
syntax and peer/query use refuse; no-frontier parsing agrees with the frozen
parser; the frozen parser's omission is reproduced; source and other routing/path
sets/limits have exactly the planned two-site delta. Reported child launches,
native calls and owner operations are all zero.

Both outer operations report `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit zero,
direct child reaped, Job closed, zero active/terminated final processes, no
termination requested, empty cleanup errors and empty stderr. Selection hashes
match the outer results; all nine selected source snapshots match their pins.
Assembly stdout parses identically to saved `distribution/ASSEMBLY.json`.

I independently enumerated and rehashed every actual base and output payload:
both contain exactly **154 files**, with all file lengths and hashes matching
their respective assembly maps. Exactly **`LAUNCHER.md`, `PROFILE.json`, `run.py`**
change; **151 files remain byte-identical**. The new PROFILE equals the old one
with only its `run.py` file entry updated. Every installation, native helper,
owner and checking file is unchanged. Package payload totals 39,513,394 bytes.
External Python runtime binaries were not independently rehashed in this audit.

The new package is
`experiments/v5-local-checks/frontier-launcher-package01/distribution/package`.

| Binding | SHA-256 |
|---|---|
| New PROFILE | `efa1e0894a24859bf1c7648ccaf72674c7cf136c9fce32a62020e75cb24bcd45` |
| New sibling ASSEMBLY | `d3b2ccc6f3cad7dcf5ebae1852840c6238cf555b1340de7797e910bb6b01ecf0` |
| Unchanged INSTALLATION | `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27` |
| Unchanged implementation identity | `86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea` |
| Controls selection | `8fc121a09172c6b83ce445113f2c7ea8c1cbca9a50a5b5a2270fc85d7b3c44fb` |
| Controls outer RESULT | `d636a6b1eeeb41e64e0aac58627e41f34654892241f7a416d8b6f3f14f45366f` |
| Package selection | `985af9e0f9d7e702f46495cb1fc5f134d0fd78735193b77e6149cc26d85c36c9` |
| Package outer RESULT | `f57d5efedb45436d674d5f7091d1c41cca2090031b1fc9e9a775333492ee0d92` |

Controls cost 0.2790723 wall seconds and 0.078125 Job + 0.09375 outer-wrapper CPU
seconds: **0.171875 known CPU seconds**. Assembly cost 4.5043247 wall seconds and
1.46875 Job + 0.53125 outer-wrapper CPU seconds: **2.0 known CPU seconds**. Nested
assembler/supervision counters overlap these scopes and are not added again.
Peak Job private commitment was 15,060,992 and 17,141,760 bytes respectively.

The assembly's own status remains `ASSEMBLED_NOT_ADOPTED`. The new PROFILE and
package path have been sent to root and the substantive-run planner; root owns
adoption and fresh public-operation selection. No broad regression, native
operation, owner-state access, old-package change or Git mutation ran here.
