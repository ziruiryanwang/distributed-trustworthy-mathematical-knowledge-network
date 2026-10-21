# Repair an exact contact-class mismatch

2026-10-20, root. Source-evidenced defect; no reproduction experiment needed.

The selected113 map uses `transport/acquisition_resilience.py` whose `_binding`
admits only exact `_ExpiringContact` and `direct_contacts._Contact`. Adaptive
located queries actually issue the distinct `located_queries._Contact` subclass.
Hence their already-authorized suppliers are refused before a settled body
attempt. `declaration_resilience` borrows this same binding and is also affected.
The no-provider installed query check could not observe this acquisition path.

Select the fresh successor
`software/v5/body_location/transport/acquisition_resilience.py`, initially the
exact predecessor logic plus the explicit actual located contact class in its
private binding allowlist. Keep the original endpoint membership,equality,
budget,policy,liveness and private binding checks. Do not use broad isinstance
acceptance or admit arbitrary subclasses. The same correction reaches the
unchanged declaration helper through its existing imported binding.

Root owns this source. It may later be extended by the separately reviewed
exact-demand custody contract; that broader implementation is not selected yet.
adaptive_audit will include one focused exact-class/forged-subclass control in
the subsequent selected suite. No whole located-query/native/proof repeat is
needed. Existing source,installation and all prior evidence remain unchanged;
their scoped passes are not relabeled as coverage of this missed case.
