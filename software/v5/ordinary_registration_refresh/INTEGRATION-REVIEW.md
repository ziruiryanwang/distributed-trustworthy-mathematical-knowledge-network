# Refresh routing and file-only integration review

2026-10-28, query_scaling. **PASS, source-only scope.** Canonical guard passed;
reviewed SELECTION.md and the three root-owned files below. No imports, runtime,
tests, owner/database/network access or Git. This review does not qualify the
peer API/Provider implementation or an ungenerated source map/build/output.

| Reviewed file | SHA256 |
| --- | --- |
| peer.py | `c70c8ad123b564ce2927eeb48d6e802695a8ab16c437dc74925362a94dd2fe6d` |
| run.py | `13394976a25f9dc492a6ecfb19cc96748e3cf43a8d11df54417a71edfc0a6dff` |
| assemble.py | `b2efbf164d67bcacf17dfd1c0ec3c26372874f874eb87d082e56e63e5c2a8ca2` |

`peer.py` differs from the selected ordinary_sparse_access entry only in its
operation lists, state-free classification, explanatory text and directory
dispatch selection. `directory-refresh-serve` explicitly selects
`api.directory_refresh_serve`; static service still selects `directory_serve`.
Both receive the existing fresh READY writer, and the entry does not synthesize
readiness itself. An API no-listen result therefore produces no READY file unless
the API incorrectly calls the callback. Final reporting and API-owned cleanup
are unchanged.

The operation rejects all catalog, custody, store-id and custody-limit arguments
before opening state. It does not enter the publish/serve index branch or owner
opening branch. Normal package/runtime verification still occurs; state-free
does not mean code-free bootstrap. `run.py` differs from the adopted
ordinary_name_directory launcher only by the new exact peer-operation name.
It preserves child argument grammar, original finite allocation, supervision,
path separation and the publish/serve-only indirect-index rule.

`assemble.py` binds the adopted directory kit by its exact manifest and external
receipt hashes, PROFILE `7687d527...`, installation `9112bc5d...` and old source
map `46709b30...`. Its helper pin matches the retained file-only assembler
`9acc1b24...`. It does not import or execute product/native code. The baseline
package must contain exactly 160 bounded payloads, all matching the adopted
manifest; the baseline profile and 78 copy roles are bound to those bytes.

The selected new map is read with the explicitly supplied SHA256. Equality to
the old map after precisely four role/source substitutions preserves its schema,
other fields and 93-source count. The only replacements are peer.py, run.py,
peer_api.py and support/transport/http_provider.py. Each replacement is pinned,
bounded and required to differ from its predecessor. No pattern integration or
additional source role can pass this equality check.

Assembly changes exactly those four payloads plus PROFILE.json. The profile is
rebuilt by replacing only their file pins, preserving its schema, remaining
fields and 122-file auxiliary set. The exact 160-file result therefore has 155
unchanged files, including installation/native payloads. Existing ordinary-path,
fresh-output, copy-readback and final source/input rechecks preserve the baseline
and refuse a changed input. The report correctly says ASSEMBLED_NOT_ADOPTED and
claims file assembly only. This is package assembly; copying the coherent source
bundle/companions into a later kit is a separate root-owned step.

No blocker was found in this selected integration boundary. The future map SHA
must be selected explicitly when invoking the assembler; this verdict does not
stand in for that byte selection, actual assembly outcome or public operation
evidence.
