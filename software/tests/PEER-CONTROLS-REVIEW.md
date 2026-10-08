# Post-cycle controls: root source review

2026-09-21. Static review only; no imports, compilation or execution. Root read
the whole harness and specification and checked the relevant frozen peer-wire,
peer-service and peer-node branches. The harness was authored independently by
`bounded_domains_author`; root owns launch/execution and the small test correction
disclosed below. This is not an independent outcome audit or a full security audit.

## Disposition

Suitable for a separately pinned allocation after successful H01 and its exact
G02/preparation lineage exist. No launch has yet been constructed or reviewed.
The remaining unexercised variant/recovery cases must stay explicitly open.

Reviewed current files, relative to `software/`, SHA-256:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/peer_controls.py` | 49073 | `D2A5FCA8441D0D673D7C54A9DE6987E1AF48BBDD972A9F0A0A662AC80CC87B41` |
| `tests/PEER-CONTROLS.md` | 13521 | `1A7FB2EFD3CB3AD4867DF2AED789FCB09B452A57948B738935E1371DCA7FE0BE` |

## Consequential checks

- The harness uses retained installed code, not mutable recovery-development
  sources; current config/source pins and original launch lineage are checked.
- It writes no ledger rows directly. Immutable SQLite reads occur only across
  quiescent command boundaries, under the honest sole-operator premise. Heads,
  entries, contexts, artifacts, candidates, publications and views cannot change
  across these controls. Ordinary remote/acquisition bookkeeping may grow.
- Each terminal response is compared with the actual selected request row;
  exact replay consumes no new request/stage/reservation. Fresh duplicate
  transfer does consume its grant, with package/candidate/snapshot reuse checked.
- Costs and bound cleanup observations persist before expected refusal or
  success assertions. A semantic mismatch cannot erase a bound Job's CPU or
  turn known quiescence into a claim of live descendants.
- The corruption layer expectations match the actual receiver: whole-bundle
  digest is checked before object identities; changing only the outer digest
  reaches the typed-CID check. Coherent advertised metadata reaches independent
  local metadata derivation before being refused. None creates acceptance.
- Fault senders are bounded cooperative threads, not separately isolated Jobs.
  They have finite routes/connections/output and are joined. Installed public
  commands retain their real supervision. No concurrent use of the selected
  nodes is allowed during controls; no HTTP readiness probe is added.
- Eleven ordinary calls (including one exact replay) plus one real service are
  consistent with twelve commands, ten new requests and 432 MiB conservative
  reservation. Zero new native stages is required, not assumed in accounting.

## Correction made before execution

The original private-route assertion checked only HTTP status 404. That is not
sufficient evidence for the stated no-private-bytes claim: an erroneous server
could send private content with a 404 status. Root added exact equality with the
fixed public `PEER_NOT_FOUND` response body and retained both complete responses.
No product source or previously executed artifact changed. The current table
binds that revised, still-unexecuted harness. Authorship of this correction means
the root review is not independent of these added test lines.

## Limits

This is a finite same-host honest-owner fault test. It neither proves every
transport failure fully accountable nor supplies independent-host deployment,
usefulness, hostile-source confinement, capacity renewal, valid package-variant
coverage or genuine interrupted-transfer recovery. Exact launch review and a
separate evidence audit remain necessary before recording runtime conclusions.
