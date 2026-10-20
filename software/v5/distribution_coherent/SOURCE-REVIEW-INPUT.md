# Coherent distribution: source review input

2026-10-20, core_search. Canonical guard passed. Source-only implementation of
CONSOLIDATION-SELECTION; no imports, tests, build, proof, network or Git work.
Used predecessors remain unchanged. Root owns exact build/launch selection.

## Selected fresh files

All paths below are relative to `software/v5/distribution_coherent/`.

| File | SHA-256 |
|---|---|
| distribution.py | `6d6f541112f5f25493a67da6a67065535d8a5e8347456004c89435cbfdc14ee6` |
| examples/contribute.py | `b6bcf87c1441ff69c4a438073ab4defae2c5d9f112c40edb3259dddf1c4a8682` |
| examples/README.md | `3e3bbaef2c75dba5173eb1203b160a5c6b20bb0c7438f7c21047bf8038f9fafa` |
| RUNTIME.md | `5e2ebf11832fa308f9dcf06240c689647292017ba393c05ac86f5f221dc64ef8` |
| REMOTE-READER.md | `463e448426273747a7b08b111af1a14e4fccd2c77159089bb2da28de472315f1` |

The builder derives from `distribution_interfaces/distribution.py`. Whole-source
comparison with its README section excluded confirms exactly TWO executable
changes: built-in reader schema becomes DMKN_V5_REMOTE_READER_WITHDRAWAL_V1;
required_sources additionally requires v5/admission/trust.py. Build/verify/run,
schemas, role projection, source cap, wrappers, hash checking and limits stay.
Generated README adds actionable separate adoption/ordinary-open owner snippets,
mandatory reader trust_domain, withdrawal limits and optional paired config.
Existing interface-only, supplier continuation, deadline/cleanup and deployment
limitations remain. README is still the builder's only packaged documentation;
the four other files here are separate source examples/guides, not new SDK rows.

Contributor derives from `software/v5/examples/contribute.py`. It adds only
TrustDomain import, DMKN_V5_CONTRIBUTE_EXAMPLE_WITHDRAWAL_V1 schema, required
top-level trust_domain, and existing-domain open before RuntimeProfile creation.
trust_domain has exact directory/domain_id/support_id fields. It never calls
create, repairs policy or falls back after denial. Input/source/name validation,
author/admit/publish body, budgets, result schema and cleanup remain unchanged.
The revised caller request includes retained explicit adoption configuration.

The full map remains root-owned: baseline distribution-interface-01, eleven
logical SDK replacements and admission/trust.py addition = 109 SDK entries.
Do not lose the existing interface-only/supplier/efficient-owner selections.
Legacy evidence workspace remains default; paired workspace is a fresh explicit
config/schema. New software support requires deliberate adoption; distinct run
paths and owner strategy bytes do not alter the support identity by themselves.

## Independent source review of the integration owner

Narrow source PASS for core_release's integration_actual.py
`02dc6c15254dfecf5b4d6f05a96420931c0e4de97ccacc443200d7ab709e2886`.
Separate adopt/startup/withdraw actions have exact input fields; only adopt
creates policy. Startup opens it, creates real validated and preparation owners,
binds 13 actual source origins/pins (12 new selections plus retained interface),
asserts zero mathematical/network/author work and closes all owners. The actual
paired Workspace then reopens with the same namespace and closed operation.
State paths are disjoint, fresh output is retained, errors/cleanup are preserved.
Issuer/preparation pin key shapes and no-work report fields match their current
implementations. No mathematical fixture or hidden retry was introduced.

Installed success/denial and actual package binding remain unrun at this source
checkpoint. Do not convert this review into a release or useful-growth claim.
