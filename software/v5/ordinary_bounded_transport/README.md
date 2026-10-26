# Bounded transport: pre-handshake admission and shutdown

This source successor changes one transport implementation. Its execution and
review disposition are recorded separately; source availability is not a test
pass or a complete v5 release. Existing mathematical checking, query formats,
discovery policy, custody and native bytes are unchanged.

## Operator-visible difference

The provider reserves a connection slot **before** TLS handshake or HTTP work.
The configured `max_connections` bounds owned processing slots, including
handshakes, active work and cleanup. The OS listen queue is a separate bounded
queue, not an extra set of application processing slots. This does not guarantee
service under network saturation or provide per-participant fairness.

`max_requests` is now conservatively a finite ceiling on accepted connection
attempts as well as HTTP handler starts. Status `accepted_attempts` counts socket
acceptance; `requests` counts HTTP handlers begun, not parsed or successful
requests. An incomplete or failed TLS attempt consumes the accepted-attempt
allowance even though it never starts an HTTP handler. Do not read
`requests` as the total connection cost or enlarge the allowance
automatically when a client fails. A peer can exhaust a finite lease's allowance;
this change bounds work, not the attacker's ability to deny useful service.

The accept owner uses nonblocking socket acceptance with a 10 ms idle poll when
no connection is ready. This avoids hidden pending accept-socket ownership on
the supported Windows runtime, at the cost of polling and nominal idle detection
delay. Scheduler delay is additional; 10 ms is not a hard latency guarantee.
Busy acceptance does not add the idle polling sleep.

Shutdown stops accepting first, cancels/closes the provider's owned connections,
then awaits their closure. Original service and cleanup deadlines still apply;
cleanup does not receive a fresh budget. The outer process/resource supervisor
remains necessary. HTTP grammar, TLS authentication, byte ceilings, routes and
the one-request-per-connection protocol remain selected from the predecessor.

Read [EXECUTION-TRUST.md](EXECUTION-TRUST.md) before approving local projects.
Mathematical correctness, source execution permission and resource containment
are different assurances. Neither this transport repair nor local operation
demonstrates global availability, faster mathematical growth or exploit absence.

## Exact file-only integration

The only supported base for this overlay is the preserved sparse assembly:

- PROFILE: `97f93cc66f77ebcecd7a3a341baaaf4725236a8dec5fb9cee3c3e67d478f2834`.
- Installation manifest: `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
- Immediate sparse ASSEMBLY receipt: `b138a6402a921ea1b7690a805cdab5d6bef2a3484659ff970eb4726dc90ba1a8`.

`assemble.py` reuses the frozen fair assembler's exact pinned file helpers. The
root-selected OVERLAY must have schema `DMKN_ORDINARY_BOUNDED_TRANSPORT_OVERLAY_V1`
and exactly three `files` entries, each with actual `bytes` and `sha256`:

| Destination in fresh package | Source in this directory |
|---|---|
| `support/transport/http_provider.py` | `http_provider.py` |
| `BOUNDED-TRANSPORT.md` | `README.md` |
| `EXECUTION-TRUST.md` | `EXECUTION-TRUST.md` |

Use the approved Python with `-I -S -B` and `assemble.py`'s explicit arguments:
`--source-root`, `--base-package`, `--base-profile-sha256`, `--base-receipt`,
`--base-receipt-sha256`, `--overlay`, `--overlay-sha256`, `--output`,
`--wall-seconds`, `--cpu-seconds`. No build or run is selected by this recipe.
The source root must retain `software/v5/ordinary_fair_search/assemble.py`.
The output leaf must be fresh and its parent must exist. Approve actual hashes
independently; a directory name or historical passing report is not approval.

The assembler checks the complete 152-file base before and after copying. The
successor has 154 files including PROFILE, with the same 117 auxiliary roles.
Only the provider role changes; two root documentation sidecars are added, and
PROFILE commits last. All native and other predecessor payload bytes remain
unchanged, including the older README. `ASSEMBLY.json` outside the package binds
the exact changed/doc files and resulting profile; it is not runtime adoption.
Retain partial outputs and failures. Do not overwrite old evidence or retry
automatically. Immutable owner-controlled source/storage is a premise, not a
defense against hostile concurrent writers.

## Prepare operations for the resulting profile

Keep this directory and the unchanged sibling `ordinary_network_kit` under the
source checkout's `software/v5`. Use **this** `prepare_selected.py`, not the old
network wrapper, with `--package`, the new `--profile-sha256`, `--request` and a
fresh `--output`. It loads only the exact pinned offline network preparer and
recognizes the same 45 noncompiled/72 native role names, with only the selected
provider source pin replaced. Unknown interfaces are refused.

Use the existing network kit's request forms and guide. There is no new config
schema, provider-discovery trust rule or execution approval. Preparation neither
imports product modules, checks native artifacts, opens owner state nor starts
a command. After separately reviewing its generated files, use the existing
public launcher with the **new** profile and original finite resource envelope.
The actual product retains its native checking and local-state obligations.

This directory is a separate successor; the previous source ZIP and wrappers
remain unchanged. It is not a newly rebuilt native installation or a universal
platform/deployment package.
