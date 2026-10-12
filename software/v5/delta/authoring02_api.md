# Canonical-row authoring successor

The selected new source interface is `delta.authoring02`, with the same
`DeltaImportSession`, `DeltaSourceOperation`, and `DeltaOwnerPreparation`
operations described in authoring_api.md. Do not use frozen `delta.authoring`
for new witness emission: it confused frontend topological order with the
relation's canonical imported-group order. It remains retained for audit.

The successor delegates witness rows to `reprepare.emit_relation_rows`.
Frontend order stays topological; imported relation rows use `(owner,index)`;
local rows follow local-spec order. The verifier/Lean checker and proof rules
are unchanged. Profiles must pin authoring02.py AND reprepare.py along with
the original required dependencies; old profile pin lists are not interchangeable.

`reprepare_retained_export(foundation_bytes, request_bytes, export_bytes,
packet_bytes)` is a pure producer recovery operation, not a verifier or owner
authority. It derives a new packet from retained source export without running
Lean again, preserves all non-row packet fields, and binds the exact imported
group/body context. Its result is untrusted until a fresh DeltaVerifier admits
the entire packet. Saved success/failure reports do not grant mathematical use.

Actual evidence: delta-reprepare01 cold-admits the two-delta packet generated
by this shared emitter. The whole ordinary authoring02 live-owner wrapper has
source review but has not been independently rerun. No claim of full v5 release.
