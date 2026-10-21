# Independent challenge: finite adaptive located queries

Reviewer: core_growth. Source/theory only; no implementation, import, experiment,
proof, process launch or Git mutation. Canonical workspace guard passed.
Read ADAPTIVE-LOCATED-DESIGN `27cec9e66687eb67302361b4011a581feee75b813ff6397b006a75b3dd3334be`
against selected110 map `e0e22f41`, portable WorkflowBudget/controller helpers,
the existing exact handoff checks, and iterative retirement/validated client.

## Verdict

**GO for root to select the one-helper implementation**, preserving the explicit
requirements below. No additional routing architecture, acceptance rule or
existing-core edit is needed in principle. This is design clearance, not an
executed result or a claim of globally complete discovery.

## Why the aggregate accounting closes

Let original acquisition budget be B and prepaid envelopes be L and S. Before
sequence advances, debit B once by L.route_operations + L.descriptor_requests +
S.requests, and by L.reply_bytes. Existing L.reply_bytes ALREADY includes search
reply capacity: charging L.reply_bytes + S.bytes again would double-count it.
Each per-generation workflow requires l_i.reply_bytes >= s_i.bytes + 1024.
Reserve all additive components of l_i and s_i before work, with sums bounded
componentwise by L and S. Then total descriptor replies plus search replies are
bounded by sum l_i.reply_bytes <= L.reply_bytes, and logical attempt counts by
the prepaid request sum. Actual later acquisition independently debits B.

Location events, peer/contact slots, descriptor attempts and all seven search
dimensions need their own monotone sums. Retiring a generation refunds none.
Per-generation lower/upper range checks remain; a nominal generation cap does
not promise enough remaining capacity to fund every generation. Inflight is a
concurrent cap. The fixed absolute envelope deadline never becomes now+wall.

This does not turn logical routes/events into network packets/bytes. Keep the
single retained child's existing transport limits and the Python channel's
monotone sequence, frame, sent/received and stderr caps. They must not restart
or reset between queries. No claimed complexity bound may ignore those costs.

## Original authority and retirement obligations

The new helper bypasses DeltaLocatedHandoff, so it must explicitly retain that
handoff's fresh-channel and original config/namespace/egress/deadline checks.
ServiceLocatedWorkflow's constructor alone does NOT establish those bindings.
Capture channel/adoption/config/policy/source origins once; preserve normal
monotone channel counters rather than freezing them at their initial values.
Use the existing exact route/descriptor helpers and genuine workflow tickets.

Every generation owns its original descriptor-derived endpoint expiry. Search
and acquisition must inherit it, narrowed by original deadlines, never recompute
now+age during handoff. Old saved workflow/search/contact/helper capabilities
must reject after retirement, including when a new generation reuses a label.
This remains a trusted owner-controlled Python boundary, not hostile same-process
code isolation; transfer of the raw channel does not authorize bypass commands.

Before retirement require no pending workflow/search/acquisition reservations,
no structural inflight, no concurrent channel command, and no detached work.
Mark the old workflow terminal even when it found no contacts and never created
a SearchSession. Preserve real warrants, shared budget, owners and cumulative
staging/import costs. Current inherited close owns the same channel exactly once.

## Empty outcomes, failures and observability

Derive a no-contact result from actual adopted contacts and their original
unexpired deadlines, not a stale label set. If expiry races begin_search, refuse
conservatively; an overall deadline failure is not ordinary absence. A typed,
settled descriptor dial miss may continue. Malformed/authentication/IPC failures
and Python cancellation still fail-close; none becomes a fresh funded attempt.

Publish allocated/terminal status and tombstone partial scopes BEFORE fallible
diagnostics. On unexpected failure, await existing child cleanup and perform
original owner cleanup even if report capture also fails. Preserve FAILED on
later close, all charges, and at most eight bounded generation records.

Compact reports should retain bounded route-termination counts/census as well as
resource counters: observed_route can return incomplete/error-marked hints with
a still-live channel. An empty such result is not evidence of an exhaustive
route, let alone mathematical absence. Do not retain full peer/coverage maps or
sum repeated cumulative channel/acquisition reports as independent costs.

The selected change supports adaptive unknown-provider discovery before one
combined import. Exact-J/semantic merge and sealed-view rules already apply;
no human-intention layer, mandatory research agenda or proof-policy change follows.
