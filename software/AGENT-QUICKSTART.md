# Agent requests without hand-escaping source

This is an additive development client aid, not a release or mathematical
qualification. The archived development package predating this file does not
contain it; distribute it only with a separately reviewed fresh source package.
Do not change an installation already bound to node state.

An operator first builds, configures and initializes a node using its operator
quickstart. A new agent receives its own client label, current context and P1
snapshot, permitted library/documentation paths, and configured peer aliases.
The complete operations and source-language boundary are in [API.md](API.md).
The agent chooses the mathematics and any useful entries; this client does not.

`make_request.py` creates one bounded UTF-8 JSON request file. It does not import
the node, read private state, run Python/Lean source, send requests, select peers
or candidates, retry, renew capacity, publish automatically, or grant acceptance.
Use an existing owner-controlled request directory. Source/output paths must be
absolute local non-reparse paths; the output must not exist. These are safety
checks for cooperative local use, not a hostile-filesystem sandbox.

## Submit an exact source file, then publish explicitly

The paths and uppercase handle strings below are placeholders. Replace handles
with complete strings returned by **this node and client**; never manufacture
them or copy another node's handles. `UserResult` must be the actual declaration
root in the source you independently authored.

```powershell
& 'D:\Python314\python.exe' -B -E -s -S 'E:\MathCommons\install\make_request.py' submit --client local --request-id submit-001 --context 'OWN_CURRENT_CONTEXT' --source-file 'E:\MathCommons\work\result.lean' --root UserResult --output 'E:\MathCommons\requests\submit-001.json'
& 'D:\Python314\python.exe' -B -E -s -S 'E:\MathCommons\install\manage.py' request --config 'E:\MathCommons\state\config.json' --request 'E:\MathCommons\requests\submit-001.json'
```

The first command only returns `REQUEST_FILE_CREATED_NOT_SENT` and byte/hash
pins. Source bytes are read directly, decoded as strict UTF-8, and represented
without newline or Unicode normalization. A UTF-8 BOM is rejected, not silently
removed. Source is limited to 65,536 bytes; complete request JSON to 131,072
bytes. Escaping can make a source within its limit exceed the request limit.
The helper validates framing, not Lean syntax or handle ownership.
This helper accepts ASCII identifier roots and dotted ASCII identifier paths
(for example `MyNamespace.UserResult`). The underlying source/API may support
additional names; use its documented raw JSON route for those.

Only if the second command returns `status:"OK", accepted:true`, retain its
private `artifact`. Submission does not publish or advance the context. With
that artifact and the current P1 snapshot, separately create/send:

```powershell
& 'D:\Python314\python.exe' -B -E -s -S 'E:\MathCommons\install\make_request.py' publish --client local --request-id publish-001 --artifact 'OWN_RETURNED_ARTIFACT' --snapshot 'OWN_CURRENT_P1_SNAPSHOT' --output 'E:\MathCommons\requests\publish-001.json'
& 'D:\Python314\python.exe' -B -E -s -S 'E:\MathCommons\install\manage.py' request --config 'E:\MathCommons\state\config.json' --request 'E:\MathCommons\requests\publish-001.json'
```

Require `status:"OK"`; retain the returned candidate and updated snapshot.
Publication does not grant another node mathematical acceptance. To observe
current context/snapshot, the builder's `info` command takes only the common
`--client`, `--request-id`, `--output` options. Sending `info` is an ordinary
charged request, not a free local lookup.

## Optional discovery and local admission

Every command below creates a file only. Send that file separately with the
same `manage.py request --config ... --request ...` entrypoint, inspect the
actual reply, then decide the next operation. All commands require the common
three options shown above and a fresh output path.

| Builder command | Additional explicit arguments | Next returned value |
| --- | --- | --- |
| `peer-find` | `--peer CONFIGURED_ALIAS` | Agent-selected receiver-owned `remote` from untrusted catalog |
| `peer-acquire` | `--remote OWN_SELECTED_REMOTE` | Local `candidate` and updated P1 `snapshot`; no acceptance |
| `admit` | `--context OWN_CURRENT_CONTEXT --candidate OWN_CANDIDATE` | On `accepted:true`, new checked `context` and exact receiving names/types |

Repeat `--candidate` for at most four distinct, explicitly selected candidates.
Use the new context/receiving names in later source. Acquiring bytes does not
replace fresh local admission. A provider need not stay online after successful
acquisition for the receiving node to perform that admission.

Other operations, bounded local enumeration and ordinary-definition inspection
remain available through the exact JSON schemas in [API.md](API.md). This small
builder intentionally does not wrap owner initialization, service management,
renewal or recovery.

## Stop and preserve evidence

Keep each generated request file unchanged. Creating it consumes no product
credit; sending it can reserve capacity and run checked work. Do not regard a
CLI exit code alone as success: inspect the structured status and required
acceptance flags. A statement definition is not a proof of its proposition.

On refusal, retain the request, reply and evidence and follow the operator's
selected failure policy. On transport failure, pending state, `accepted:null`
or unknown outcome, stop: do not generate another ID or assume rollback.
Identical request bytes can have historical replay semantics, not fresh work;
any explicit recovery/retry is a separate operator decision. No automatic retry
is implemented. Failed work stays charged, and partial client files are retained.
