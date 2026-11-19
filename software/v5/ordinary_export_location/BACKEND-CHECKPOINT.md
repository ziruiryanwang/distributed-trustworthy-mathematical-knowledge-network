# Backend source checkpoint

2026-10-28. Ordinary backend source is ready for independent review and root's
joint integration. No source import, compilation, product execution, database
open, network use or Git action was performed. Root owns exact runtime selection.
The agreed [wire contract](WIRE-CONTRACT.md) is
`d0caa96cbf5b03a26800b8a725e27bf63a78dea2bb6f6480ad97eac8681c4591`.

The ordinary-only domain and descriptor preserve retained Noise/DHT/transport
composition. Startup builds the charged set before libp2p construction; publish
reserves before intent commit, and confirmed revoke releases after intent/self
row deletion. Pending intent is reported separately. The new controller exposes
explicit same-config create/reopen, matching finite IPC caps, report/stop
reserves, fail-fast busy, and poison-plus-drain on issued uncertainty. Config and
wire bytes retain unescaped UTF-8 canonical JSON. HTTP gateway and custodian are
distinct roles; local self-discovery is not implemented. The gateway must own
the whole locate/descriptor sequence under one busy lock.

The first source review remains preserved as BACKEND-REVIEW.md. A subsequent
root-selected startup correction adds PREPARED/BEGIN before state/network
effects: parent durations are anchored at the earlier Node marker, so setup
consumes the wrapper's original service horizon. `service_deadline` is separate
from the channel/cleanup deadline. PREPARED and READY use the existing two
reply lifecycle frames; BEGIN input bytes use the same IPC counters. Only the
three source pins below and the contract changed for this correction; no runtime.

Root then selected the minimal honest-revocation correction: a valid request
for an unadvertised exact route now receives an authenticated, nonce/key/peer
bound `NOT_ADVERTISED` descriptor without endpoint/lifetime authority, rather
than a stream abort. Protocol and the descriptor-serving branch changed only;
malformed/authentication/cleanup failures remain terminal. Query_scaling owns
the matching gateway validator and counted skip. This is source-only too.

Textual inspection covered every changed block. Six retained `.mjs` files were
copied with exact SHA-256 equality: intent from body_location, and runtime,
framing, transport, raw-connect composition and Ping composition from
portable_runtime. No claim of executable correctness follows from this check.

| Source | SHA-256 |
|---|---|
| controller.py | `0b7846e3936e6120d7d227e438d700e85b812139054808824dac2da503437b3d` |
| protocol.mjs | `340f38269e490c3628fe71ad0f7bf9b9bf2dcd39424eaec258a18cb05171783f` |
| intent.mjs | `220bff266e58f9a460cb182bdc16fb86654fa26f88eee27e8994fb7cd028ad08` |
| maintained_roles.mjs | `87b7b9ee2fb6f9a29e09ed8477f9e94063536f49a8d47ba941d9ced26ca0dc7a` |
| ipc_wire.mjs | `4ffbf08417f2824ef25de0ff3b473f189ca14552661f2c8d52b98e5ac3c1741f` |
| node_entry.mjs | `086936eac4cf9444e20bd4c485777aaa9a3ea277a000d0aeef703d633104d43e` |
| runtime.mjs | `8beb9f5d5fa2714572da060626fb54fd0d949216bddd6fd6ce610a639ffb8841` |
| framing.mjs | `689d1336d8d5aadd3f7068208605dc0abb6d1e01ea72e8d3b9b2b1592ed929a5` |
| transport.mjs | `df2ce9a11c453ae9f94a58577fd1d01dcd80fd8326b42682cd5dd1f3688d4e33` |
| role_composition.mjs | `5502bd2ed81295e2b2b70cec0bd8abe13a8a4d930ec3619243ff9bb267d503ca` |
| services_composition.mjs | `94341e6e01c62a3b6d2d587a5ed8f12e99fbe491d7960582282fc4c0ef02d51f` |

The separate operator map uses exactly these ten Node module names. Controller
is imported as `transport.ordinary_location_controller` in root's pinned Python
operator closure. Its runtime verifier selects the same 5,896 overlay/Node
payloads from the retained release manifest, with a 192 MiB payload-size bound;
there is no full certified application or Lean requirement. Root's separate
bundle-delta helper and exact own-endpoint locator eligibility check precede
new publication; neither is duplicated in this backend.
