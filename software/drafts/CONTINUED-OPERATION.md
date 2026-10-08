# Continued operation: concrete product limits

Prospective root analysis, 2026-09-21. Not an implemented or selected protocol.
The immediate test remains reciprocal offline use. This note identifies the
smallest next operability decisions from current code, without adding a global
mathematical agenda, consensus ledger or usefulness oracle.

## Lifetime allowances are not a sustained service

`manage.configure` currently fixes 128 requests, 16 native stages and 4 GiB of
conservative staging reservations. `ControlStore.reserve/stage` monotonically
consume those allowances. Configuration identity hashes its exact bytes; editing
that file after initialization is not renewal. The parser also caps requests at
4,096 and stages at 64, and the database is limited to 8,192 pages of 4 KiB.
These are deliberate demonstration bounds, not evidence of continuing operation.

A minimal future owner-local extension can separate cumulative authorization
from cumulative consumption. For each renewable resource dimension j, require

`used_j + proposed_charge_j <= initial_authorization_j + granted_j`.

An explicit grant increments only `granted`, never decrements `used`. Grant IDs
are idempotent: identical retries return the same result; conflicting bytes under
one ID refuse. An atomic grant transaction must preserve request/stage histories,
mathematical records, heads and existing charges. Grants do not clear pending
work or change the foundation. Remote peers cannot issue them. A grant is owner
authorization, not proof of free disk space, an SLA or actual resource supply.

Per-operation byte/time/process limits remain distinct from renewable lifetime
allowances. Adding authorization must not quietly widen the input language,
trusted runtime, native limits or foundations. Exact bounds for grant integers,
their sums and persistent representation are required before implementation.

This alone cannot solve physical exhaustion: the ledger still grows, obsolete
staging remains charged, and a fixed database page cap can eventually refuse.
Choose and measure a supported v1 envelope, then implement either bounded
expansion or safe archival/compaction. Do not claim indefinite service from
ever-larger logical grants. Reclamation requires a separate reachability and
historical-replay contract; observed file deletion is not automatically refundable
reservation credit. No garbage collection is selected by this note.

## A local proof context is not the entire corpus

The current `admit` unions selected packages with the client's current context;
later operations require that exact head. Package count and canonical byte bounds
therefore eventually stop a client even if most known mathematics is irrelevant
to its next investigation. Other nodes' results need not all be imported at once.

The minimum alternative to unrestricted context surgery is explicit selection
of an existing, client-owned, previously checked context, followed by ordinary
admission. Its mathematical content is immutable; changing which context is the
current head creates no theorem and does not retract any candidate publication.
Before source execution, the existing checking path must still authenticate its
selected evidence and bytes. A historical handle alone cannot waive missing or
corrupted dependencies. Selection must not silently copy another client's
authority or pretend two incompatible contexts have been merged.

The simplest discriminating workload: admit an irrelevant large branch to one
head, return to an authenticated smaller historical context, then acquire and
use a fresh unrelated result within unchanged per-operation bounds. Old cuts,
published candidates, historical replies and accounting must survive. Compare
its cost with monotonically unioning everything. Unrestricted construction of
arbitrary subcontexts is a different, stronger feature and need not come first.

## Discovery must beat exhaustive catalog enumeration

The current peer interface returns a finite immutable catalog and local `find`
paginates P1. That suffices for the two-node discriminator, but not a very large
heterogeneous commons. The next retrieval decision should use a measured corpus
and fixed queries, with exact-ID lookup and local-library search as baselines.

Structural indexing, approximate embeddings or LLM ranking may prioritize
candidates. Their scores and omitted results are not mathematical judgments.
Compare successful downstream reuse, query/checking costs and duplicate burden,
not only returned row count. A peer's popularity/usage claims are untrusted hints;
they cannot add axioms or bypass receiver checking. A useful v1 can select a
bounded heuristic without a universal theorem of mathematical importance.

## Fixed contacts are not an evolving network

Current configuration also binds at most two peer aliases to permanent loopback
endpoints. Changing those bytes invalidates initialized config identity. This is
appropriate for the frozen exchange discriminator, not a usable growing network:
operators eventually need to add or replace contacts without losing mathematical
state. Separately, loopback-only transport needs an explicit multi-host profile.

A future minimal contact-book operation should be owner-local, preserve old
request replies and remote-selection identity, and never silently reinterpret an
old selected endpoint as a newly assigned alias target. Immutable contact
versions plus an explicit current alias pointer are one candidate, not a selected
schema. Endpoint policy and peer discovery hints must remain separate from local
proof acceptance. Neither a public DHT nor a global consensus ledger is required
to test explicit two-host exchange and safe contact replacement. This operation
does not itself supply reachable hosts, transport confidentiality, uptime or a
qualified deployment. Avoid enlarging the current loopback grant while designing it.

## Order of work and falsifiable stopping points

### New evidence informing efficiency work

The independently audited G02 run provides a useful cost decomposition:
Beta's enclosing admission Job consumed 22.046875 CPU seconds, while its nested
single-command native replay Job consumed 4.671875 seconds. The latter is already
included, so the difference is 17.375 seconds, not an additional fee to add to
the total. Alpha's five-command submission pipeline used 29.625 nested Job CPU
seconds inside 63.453125 enclosing Job seconds; that pipeline includes multiple
kinds of work and is not a pure kernel-verifier benchmark.

These are one small workload under a shared trusted runtime, not general speed
ratios or a causal profiling experiment. Nevertheless, they rule out presenting
proof-check acceleration alone as an evidenced solution to this observed total
cost. Before selecting SNARKs or a new proof engine, measure package processing,
context reconstruction, source/pipeline setup and repeated validation separately.
Succinct proofs would add their own circuit/runtime/soundness assumptions and
prover cost; they do not by themselves make the local-library interface or
candidate retrieval usable. Historical-context selection remains a simpler
first response to needless context growth, not a substitute for that profiling.

Finish the current genuine reciprocal-use test and its controls. Integrate the
separately reviewed narrow interruption recovery. Then choose the smallest
renewal/context intervention that defeats an actual saturation workload, retaining
every failed attempt and cost. Broader retrieval and meaningful benefit require
their own baseline comparison. No result here establishes exponential growth,
unlimited storage or release readiness. These are system-operability tasks, not
a mandatory list of unsolved mathematical questions for participants.

## Later v3 measurement: renewal01

The independently audited [native-renewal run](../qualification/capacity-native-01/OUTCOME.md)
provides another finite observation, not a new benchmark allocation. Its saved
sequence and stage receipts report:

| Operation | Public CLI elapsed seconds | Enclosing public Job CPU seconds | Pipeline Job CPU seconds, already included |
| --- | ---: | ---: | ---: |
| Bootstrap | 29.8307046 | 28.46875 | 4.875 |
| Stage-quota-refused submit | 10.7992936 | 10.359375 | No stage allocated |
| Accepted composition submit | 57.1253016 | 59.484375 | 30.125 |

The accepted pipeline contains three Lean commands totaling 15.046875 observed
CPU seconds and two Python commands totaling 15.078125. Those sum to 30.125;
none is an additional cost to add to the enclosing 59.484375. The remaining
29.359375 enclosing CPU seconds are outside those pipeline children, but this
does not identify a specific cause. The analogous bootstrap difference is
23.59375 CPU seconds. Public replay/status calls took about 0.39–0.48 elapsed
seconds in this run; cold support build took 32.2363386 elapsed seconds.

These observations strengthen the case for phase-level profiling before choosing
proof acceleration. They do not establish that package hashing, parsing, source
capture, process startup or any one checker function causes all overhead. The
quota-refused submit also shows a testable optimization hypothesis: known stage
exhaustion might be rejected before expensive checker preparation. That would
need an explicit error-order/state-preservation contract and fresh comparison;
no optimization or early-refusal policy is selected here. The immediate product
work remains recovery and exact-byte custody; do not hide these measured costs
when evaluating subsequent useful accumulation.

### Existing package-phase timing recovered from the same run

Read-only inspection of renewal01's retained events supplies more information
without rerunning any allocation or adding instrumentation. The pinned
`Checker.read_package` times its call to `source_codec.read_package` plus the
selected byte-bound check. This includes decoding, address/closure validation
and plan construction, not just filesystem reads. It is wall time, not CPU time.

| Request | Worker elapsed seconds | Package-phase wall seconds | Package calls / reported canonical bytes |
| --- | ---: | ---: | ---: |
| `init` | 29.385111600 | 15.370664300 | 10 / 2809752 |
| `submit-exhausted` | 10.357071900 | 7.377348300 | 5 / 1404876 |
| `submit-renewed` | 56.707767000 | 13.060917800 | 9 / 2523588 |

All three events live under
`product-local/capacity-native-01/scratch/calls/` relative to the repository:

- `call-daabe83620db4fa88b11dd618adc5cf1/event.json`, SHA-256
  `B02ECF178A9CE8F0CEC0208BA1228DDFE6E983C5CB34ADA2327A0ADE9C861B0B`.
- `call-9fcf2f5f7b7148a3ac515364cceb809d/event.json`, SHA-256
  `CEF6A6980C84521ED8965823F562B6343B396E42ACF0E9B6BA6269039CA7D5DC`.
- `call-554b4f33012844a4aba45f12801ffb34/event.json`, SHA-256
  `4701F27826C66145A8830BE3519E7DE714ECD0F30A0F9DA0CB466A19F3C6F194`.

The bytes are sums reported by reconstructed stores; they are not measured disk
traffic or deduplicated retained stock. The five common packages are read twice
during initialization because the copied representations are checked too.
Submission rereads selected common packages and resulting candidate/inverse
packages. These observations identify a substantial measured phase, not the
cost of each internal validator or proof that a cache is safe. Child Python
pipeline work is outside this parent-only metric and already inside the
enclosing Job CPU. Do not add wall time to CPU or subtract it as if they were
the same measure. Future profiling can target this phase while preserving the
receiver's full selected-byte validation and mathematical checking boundary.
