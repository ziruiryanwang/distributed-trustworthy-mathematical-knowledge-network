# Expose existing bounded local proof choices, without new paging machinery

2026-10-22, root. Source-only selection. Root fully read author decision
e159c49a7d136be2ea651ce8a18d0ff74a7045ee60cd7878e554c690cc7d7797 and independent
challenge93dc74137c0709beb8b5aab75d24028f11b4c1ff2eb852ef30618016fc022f25,
plus actual shared validator, evidence-store query/response checks and public
forwarding paths. This does not replace the pending exact-packet installed audit.

## Selected minimum and invariant

The current local store already caps each module/profile at64 packet variants.
Allow an explicit `max_offers=64,max_bytes=16384` on the existing metadata route.
All64 fixed digest/size rows fit the existing byte ceiling by the reviewed format
bound. One SQL statement returns a response-local view; no cursor, global scan,
new schema, background discovery or automatic retry is needed. Preserve default4,
old1..8 request results, byte/profile/order/count validation and all funding.

This is optional compatible-provider use. The unchanged wire profile does not
advertise the larger cap. Do not automatically probe old8-cap peers or promise
recovery after they reject a64 request. No proof validity or authenticated local/
global completeness is inferred from an offer. No packet-stage replacement,
certificate rejection recovery, verifier change or owner resurrection is selected.

## Ownership and exact source scope

Use the actual newly built129-row map
`experiments/v5-local-checks/distribution-exact-packet-01-input.json`, SHA256
`328c21bb585881d654f1a23f1704fbaa277ee865f7adb1250cf6c19b85647561`.
It preserves the six frozen exact-acquisition sources. All used source, controls,
installations and evidence remain immutable.

- storage_integration_adapter owns a fresh exact predecessor copy at
  `software/v5/offer_enumeration/delta/custody.py`, changing only the shared
  offer-count bound8 to64 (and minimal explanatory comment if helpful), plus
  README/source-map checkpoint. Review all actual selected importers and pins;
  report any required explicit pin successor before expanding source scope.
- storage_outcome_audit owns fresh focused controls and control checkpoint under
  this same new directory/cycle. Exercise one real64-variant typed local store
  and HTTP offer response, a formerly unreachable late identity, old prefix
  preservation, count65/bool and explicit-byte/response-binding refusals. Cover
  shared validator/legacy response consequences without repeating cryptographic
  admission or whole installed circulation. Existing harness helpers may be
  reused only with exact pins and explicit changed selection.
- storage_launch_review finishes the exact installed actual audit first, then
  independently reviews this one-source delta, focused controls and selector.
- root owns source-map/test selection, finite launches, integration and Git.

No controls/build/runtime is authorized by this source assignment. Prospectively
reuse the small30CPU/90wall/256MiB/one-process envelope if source review supports
it; no proof/native/Node work. Do not build another842MB installation just for
this numerical bound before evaluating the next integration need. The current
exact-packet candidate's genuine admission evidence must not be repeated merely
because this shared metadata parameter grows. Full v5 remains unfinished.
