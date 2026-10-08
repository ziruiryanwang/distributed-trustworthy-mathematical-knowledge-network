# Certified module receiving

Source implementation; real v5 positive receipt admission is not yet qualified.
Current development uses the explicitly new existential journal profile 2
(`DMKNM002`, 184 bytes). Profile 1 receipts and 216-byte journals refuse; no
in-place reinterpretation or automatic trust migration is provided.
The public class is `admission.verifier.ReceiptVerifier`. Only the node owner
constructs it, from independently adopted image/foundation/policy, installed
verifier and runtime byte pins, exact supervisor manifest and finite session
budgets. Never construct this configuration from a downloaded offer.

```python
# verifier is constructed once from LOCAL adopted deployment configuration.
accepted = verifier.receive(receipt_bytes, expected_summary, fresh_operation_dir,
                            cpu_seconds=30, wall_seconds=60, memory_mib=1024)
group = verifier.open_group(accepted, downloaded_group_opening)
details = verifier.describe(accepted)
verifier.close()  # invalidates this instance's handles
```

`receive` launches the selected genuine verifier with dev mode disabled by its
compiled receiving gate, requires successful full resolved receipt verification,
then binds the exact same-call reply to receipt/journal/module/profile. Bad
receipts, malformed output, resource failure, dirty process closure or mutation
mint no handle. Calls have no automatic retries. Each attempted call reserves
its full worker CPU allowance and receipt byte count against aggregate limits,
even on failure; actual controller cost is separately reported, not included
in the worker reservation. The monotonic deadline includes wrapper work.
The selected runtime pin map is capped at 512MiB total, and is rechecked before
and after each call; this controller I/O/CPU is counted separately from the
inner cryptographic verification. It is not a claim of 12ms whole-call cost.
Process evidence is retained once a child call exists. A failure before the
operation directory is created may have only charged in-memory counters.
The final binding report is labeled pre-handle validation: if its disk write
outlasts the deadline, no live handle is minted despite the retained report.

Handles are not proof files. A manually created handle is not registered; a
saved success JSON or custody database cannot be loaded as acceptance. Cold
processes verify receipt bytes again. `bind_output` is a pure structural helper
and by itself confers **no** mathematical authority. Its unit tests deliberately
use nonreceipts and never claim cryptographic admission.

A profile 2 receipt establishes that a fully checked witness for the committed
module exists. It does **not** authenticate separately presented Lean source or
proof-witness bytes as the bytes used by the prover. No such bytes enter the
public admission API. Module types and computational bodies remain committed;
their content openings still must authenticate before reuse. Exact local
session/input/capsule hashes are engineering evidence, not transferable witness
attestation. The local adoption identifier also binds the journal profile.

The retained `refusal_integration.py` is the already executed profile 1 test,
not a launch path for this profile 2 source. Its immutable executed snapshot
and result remain under `experiments/v5-local-checks/admission-refusal-integration-01`.

The current adapter requires Windows and an exact adopted existing supervisor
installation. It trusts the owner process and local installation/filesystem;
it does not isolate malicious Python running in that same process. Pins do not
prove a hermetic OS/DLL dependency closure. Windows Jobs provide resource and
closure supervision, not filesystem/network isolation or a hostile-parser
security sandbox. These are explicit unfinished release obligations, not a
supported worldwide-deployment claim. An invalidated image/profile requires
closing its verifier and adopting a replacement under a separate local decision.
