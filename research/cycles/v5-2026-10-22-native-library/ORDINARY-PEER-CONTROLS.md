# Focused ordinary-peer controls: source-only selection

2026-10-23, owner_cli. Root selected one new `peer_controls.py` under
`software/v5/ordinary_peer_package`; no test/import/build/native/network run has
been performed by its author. Parent owns the exact source/package/runtime pins,
outer allocation, execution and subsequent evidence adoption.

## Changed boundary and payoff

The new public CLI/coordinator joins existing checked admission, discovery and
custody mechanisms. The consequential new risks are loss of earlier committed
effects in a later failure report, incorrectly renewed composed grants, and
configuration routing that reaches work before its intended refusal. These six
small groups address those seams; they do not repeat previous mathematical,
storage, transport or package campaigns.

| Group | Actual selected code exercised | Scope and stop boundary |
|---|---|---|
| Owner JSON | Exact profile parser | Whitespace/bool/null accepted; duplicates/floats/nonfinite numbers refused |
| Explicit contacts | Coordinator contact validation and exact-file pin checks | Remote plaintext, unpaired CA pin and wrong CA hash refused; no TLS handshake |
| Malformed inputs | Coordinator field/limit/record validation | Refuses before native allocation or acquisition; owner-binding check is mocked only where needed |
| Shared find/receive grant | Actual find coordinator, search client/session construction, OrdinaryBudget and receive validation | Stubbed first offer proves prepayment occurs before I/O dispatch; failed offer leaves prepaid costs; original caps required and no deadline/counter renewal |
| Partial effects | Actual PeerFailure and terminal-report helper used by CLI | Successful checked/reused admission survives later report-budget failure; oversized partial publication retains concise committed IDs |
| Serve scope | Actual service coordinator validation | Refuses absent full-custody/exclusive authorization, fractional lease, insufficient cleanup reserve, create-index and remote plaintext before state/provider work |

## Invocation and finite envelope

```text
<selected-python> -I -S -B <selected-peer_controls.py>
  --package <absolute selected package>
  --profile-sha256 <exact PROFILE.json SHA-256>
  --python-runtime <absolute selected Python runtime>
  --lean-runtime <absolute selected Lean runtime>
  --output <existing fresh run directory>
```

Root proposed an outer 60 wall-second / 35 CPU-second / 512 MiB envelope. The
script's cooperative inner guard is 50 wall / 30 controller CPU seconds from
entry. The package is loaded once through its checked peer/bootstrap/profile
chain. Runtime identities and bytes are verified, but no native executable runs.
The script writes a fresh `CONTROLS.json` plus stdout. Existing package, sources,
stores, catalogs and earlier evidence are not rewritten or copied.

The mocked receive/serve controls replace only `_state`, explicitly avoiding a
real owner/custody open; they do not test ownership validation. Shared-search
controls replace only the first offer dispatch and preserve real session/budget
construction. Guards refuse SQLite opening, subprocess creation, peer exchange
and Provider start. asyncio's internal local wakeup socket is not peer traffic.
The selected package/code, local immutable storage, Python and OS remain trusted.

The post-admission cases use small synthetic native-result records. They exercise
the exact reporting helper, not actual admission, recovery, locking or rollback.
The CA-positive control selects existing pinned package bytes to test file
selection only; those bytes are not claimed to be a CA certificate. Invalid
service configurations are rejected before `_index`, so no index is opened.

## Review and later interpretation

Independent source review and an exact root launch selection must precede use.
A future pass would establish only these six finite changed-boundary controls.
Actual installed CLI exchange/acceptance and Provider shutdown under the same
owner lock require the separate root-owned integration. No networking, useful
knowledge growth, independent-host deployment or final-v5 completion follows
from these source files or synthetic controls.
