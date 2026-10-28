# Keep the disclosed storage premise; do not fork the serializer

2026-10-28 root decision after RELEASE-BLOCKERS, NATIVE-OUTPUT-DECISION and the
independent OUTPUT-GRANT-PATH source audits. No code or experiment is selected.

The current mathematical acceptance gate remains intact. A clean admitted
artifact must match the actual checked report and fit its successful-output grant.
The reservation ledger is not a physical disk quota: failed native output may
exceed its original charge, and call spool/logs have separate storage obligations.
Current launcher documentation already discloses that boundary. No observed
disk-exhaustion witness or newly demonstrated unsound admission is asserted.

Exact upstream source establishes a useful conditional bound: one fresh v2 save
holds its whole output in initialized private heap before writing the body.
Under the selected ordinary allocator and Windows Job private-commit premises,
`M + 88` conservatively bounds this single artifact's logical content bytes,
including temporary output. It does not bound filesystem allocation overhead,
spool, logs or all writes. The current ledger does not reserve that larger amount.

Do not introduce a C++ runtime fork or internal-ABI bridge for the exact 64 MiB
pre-write cap now. It adds version-specific maintenance and support-adoption work
for a resource premise already stated honestly. A conservative accounting change
is possible without changing the serializer, but at the guide's 1280 MiB memory
ceiling it charges roughly 20 times as much for failed artifacts and still does
not cover the whole call. That tradeoff needs an actual storage policy, not a
passing unchanged proof test. Existing catalogs must not be relabeled as having
stronger guarantees.

Retain explicit operator-controlled storage capacity/isolation for this release
scope. Public deployments requiring a hard total write quota must supply that
isolation; the application has not implemented it. Preserve all failed evidence.
Revisit tighter accounting only when that deployment policy makes its costs
worthwhile. The source feasibility question is closed; no further C++ exploration,
memory campaign, quota setup or native rebuild follows.

Return effort to the main scale requirement: determine whether repeated point
queries on a large selected local library still need whole-context metadata
reconstruction, and whether an existing safe lookup can remove that dependence.
That is a source-led decision first, not authorization to build another index.
