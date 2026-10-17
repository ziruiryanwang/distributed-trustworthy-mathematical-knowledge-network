# Explicit producer resource capability, separate from mathematical acceptance

2026-10-16 root source selection. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
No proof, native invocation, SDK change, resource reservation or larger-memory
launch is authorized by this source selection.

## Decision and reason

The tested aggregate producer and newly built stage host are retained. A
source-derived allocation lower bound rules out the proposed po19 proof under
its 4096 MiB producer ceiling; independent strengthening is being finalized in
PROVER-MEMORY-REVIEW. A small synthetic passing controller cannot establish
resource feasibility. The current host's available memory also does not justify
a larger actual operation; no application or pagefile will be changed implicitly.

The final architecture need not require every lightweight reader to operate a
low-memory prover. A separately provisioned producer may use more resources
without changing mathematical acceptance or client verification. The exact
retained supervisor already supports memory caps up to8192 MiB. Reusing that
capability is a smaller change than modifying the SDK or expanding segment
counts, which additionally affects complete-composite serialization and Windows
argument length. It preserves the existing capsule, image and stage host.

This is not an assertion that8192 MiB suffices or that memory is reserved by
writing a profile. A future launch still needs a finite exact allocation and
available host capacity, and must preserve failure/closure accounting.

## Minimal selected successor

Only new `software/v5/aggregate_resources/producer.py` and `__init__.py` are
selected initially. Copy the tested aggregate producer796eb246 exactly, then
make only the following changes:

1. Require profile schema `DMKN_V5_AGGREGATE_PRODUCER_PROFILE_V2` with the added
   mandatory `stage_memory_ceiling_mib` field. No inferred/default increase.
2. Validate an exact built-in integer in1..8192 and no greater than the adopted
   supervisor's actual `CEILINGS["memory_mib"]`. Pin the new package's two actual
   source files just as the previous package pins its own files.
3. Only the request's per-stage memory upper bound comes from that explicit
   profile field. CPU, wall, process, output, input, accounting, native argv,
   mathematical formats and acceptance rules are unchanged.
4. Keep the entire profile in the existing canonical profile identity and live
   mutation checks. Earlier reports require identical profile identity and
   budget. A new resource profile cannot renew an old allowance or silently
   rebind its successful checkpoints/history.

No mutation of `production.producer.COMMON`, subclass-global patch, legacy
source edit, implicit profile conversion or source alias substitution is allowed.
The new package is a byte-preserved successor with a small auditable delta,
not a new prover implementation. Retain old package imports and frozen results.
Request/stage/attempt formats stay their existing versions because their
fields/meaning are unchanged; the exact profile identity distinguishes policies.

Do not hard-code the current fixture's capsule/host hash or apply a universal
`bytes_per_row * 2^session.po2` rejection: session.po2 is a maximum geometry,
not proof that every required segment has that exponent. Actual SDK-specific
memory lower bounds remain explicit source-based funding evidence. A future
general resource-quote API would need actual selected stage geometry and
backend-model identity; it is not needed for this minimal policy correction.

## Focused verification and ownership

Author: memo_tests_review, after completing the smaller-segment comparison.
Checkpoint: `PRODUCER-RESOURCE-IMPLEMENTATION.md`. Independent source/delta
review: v5_growth_decision; root owns tests/launch selection and Git.

Before any execution compare the complete successor to796eb246. Add only
focused native-free controls for explicit profile-field validation, actual
supervisor ceiling, request memory bounds, profile identity/mutation and
incompatible history. Do not rerun the ten unchanged aggregate-control methods.
Do not claim real constructor/build/certificate acceptance from mocked inputs.
Controls and any runtime each need a separate exact finite root selection.

The next actual producer integration remains unfunded. The two central goals
and all v5 release gates stay unchanged.
