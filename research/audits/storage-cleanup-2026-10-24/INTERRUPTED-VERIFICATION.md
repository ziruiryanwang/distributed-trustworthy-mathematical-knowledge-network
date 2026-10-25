# Partial verifier outcome and narrowed cleanup

The single read-only verifier (script SHA-256
`f46856ba9731c225962229016bf173c9cecbe0d31d41a3d0c3416c4b810c8b70`)
ran as PowerShell PID 23196, start 2026-10-24 23:09:37 Chicago. Its original
tool session was 88634. Root observed these two completion messages:

```text
VERIFIED product-local\certified-v3-package-01\app files=13004 bytes=2444576373
VERIFIED product-local\certified-v4-package-01\app files=13004 bytes=2444835804
```

Each message is emitted only after complete actual ZIP/local per-file SHA-256,
length and file-census equality for that candidate. The reviewer-approved script
rejects reparse points and unsafe archive paths. No deletion code is present.

On the next goal continuation, the original session was missing, PID 23196 was
absent, and no verifier command process or ARCHIVE-VERIFICATION.json existed.
The final process exit status/cause was not recovered. Do not claim a complete
three-candidate pass or restart the whole operation. No removed payload exists
at this checkpoint. In particular, the old Lean extraction remains unqualified
for cleanup and is retained.

The two completed app comparisons remain observed evidence, not a missing final
report invented after the fact. Their already retained BASE-FILES.json and
CONTRIBUTOR-FILES.json supply full recovery path/length/SHA maps. Root selects a
fresh narrow guard that rehashes the four archives against historical audited
pins, checks both file manifests against archive directory membership/lengths,
checks the entire current local file/directory census and lengths, and refuses
any last-write timestamp at or after 2026-10-25T04:09:00Z (before the observed
verifier start). Research writers have stayed held throughout. Existing file
identity is established by the completed comparisons plus unchanged ordinary
filesystem metadata, not by pretending a new local hash pass occurred.

This has the same controlled-workspace/no-adversarial-timestamp-forgery premise
as the original reviewed metadata recheck. It is not safe against malicious
concurrent filesystem modification and does not claim that property. Current
runtime independence was separately checked by the two reference reviews.
All archive pins, guard results and per-target intents/results must be saved
before/after removal. The earlier three-target remover is not used.

This narrows the maintenance investment to 26,008 already verified files /
4,889,412,177 logical bytes. It does not weaken mathematical acceptance or the
overall v5 objective. No old experiment or research workload is restarted.
