# Ordinary acquisition: independent saved-controls audit

2026-10-23. Reviewer: `admission_event_audit`. **PASS for all five selected
changed-boundary groups**, using synthetic unproved ordinary syntax. Actual
loopback transport and cold inert rehosting are distinguished from mocked hostile
replies. No Lean checking, mathematical acceptance, external networking or public
deployment is established. The reviewer ran no test or product API.

Run: `experiments/v5-local-checks/ordinary-acquisition-controls-01`.

| Evidence | SHA-256 |
|---|---|
| Selection | `0fccb5a6ffef87e778a5d263a2269c3f57c8b342be30d7a98efddc6530cfce00` |
| `RESULT.json` | `3d4bda80eac6ebf809b0267e16f48464689a578b228cf85a040a58c5b829eba0` |
| Control source | `3d25f19fd33db1339347e55ba161404aa5023000b295762c205a35331a1e4527` |
| Acquisition implementation | `e69bd0f33829e4709fdc1a7c3afe4150704dfeabfe30243195b379945081e826` |
| HTTP provider | `431aae7f10f1a2c0c0323c4aea720f4139e57bb4bf7b61bf98e9e5b69d6cdd59` |

All 18 selected source snapshots and three interpreter/runtime pins independently
match. The complete control source and saved stdout, supervision and reports were
read. Stdout contains exactly five group PASS lines plus the final five-group
summary. Stderr is empty. Supervision records exit 0, direct child reaped, Job
closed, no cleanup errors or termination request, final active/terminated both 0.

## What actually passed

1. Atomic custody retained three evidence objects and four distinct export
   locators: same-name outputs of distinct units stayed distinct and both outputs
   of the multi-output unit were retained. Duplicate insertion did not recharge.
   Export-quota refusal and a callback failure after the first locator both left
   zero objects, zero exports and zero logical bytes.
2. Real loopback preview, locator and evidence requests returned exact bytes and
   bindings. The source provider recorded three successful requests; the client
   recorded 1,956 actual reply-body bytes, with the preview/evidence binding
   checked separately and still explicitly nonaccepting.
3. The source provider was stopped and source/receiver stores closed. The receiver
   was reopened and served the three objects through a replacement loopback
   provider using the same parent budget/deadline. One actual missing-object
   request then failed and charged its full 4,096-byte cap. The shared final
   budget shows seven requests, 8,008 charged reply bytes and no outstanding
   reservation: two successful 1,956-byte rounds plus that failure cap.
4. Explicitly mocked replies tested malformed locator, wrong S, wrong UnitID,
   wrong expected name, and a self-consistent locator for an absent output. The
   latter locator alone could be read as a claim, but evidence acquisition rejected
   its missing output. Five failures were charged over six completed mocked
   responses, with zero pending tickets. These are not live adversarial-peer tests.
5. Explicitly mocked transport failure and time tested the shared prepaid request
   budget, byte exhaustion and unchanged absolute deadline. Two failed provider
   calls plus one prepaid search consumed three requests and 8,320 charged bytes;
   the byte-limited case stopped after one charged 4,096-byte attempt. Expiry
   refused before any call. The time patch is a deterministic boundary control,
   not a wall-clock load/timeout experiment.

## Independent retained-state checks

Five SQLite databases were inspected only with `mode=ro&immutable=1`, with each
hash unchanged before/after. SQL object/export counts match their quota counters;
all stored raw digests match actual bytes. Supplier and reopened receiver have
identical object and locator rows. The atomic store has `(3,4,5916)` counters;
the two rollback stores have `(0,0,0)`; supplier and receiver both have
`(2,1,2355)`.

| Database under `inert-stores/` | Preserved SHA-256 |
|---|---|
| `atomic/ordinary.sqlite` | `188c6340f13b4d9e77653d306fbdc404ceb2c0659fed52cdbf60aa62cfd361ef` |
| `export-quota/ordinary.sqlite` | `09cfa8561010ff15f65980a3f46cc2ef68dfb500c02c566488997782251e15e0` |
| `rollback-after-first-locator/ordinary.sqlite` | `523e84e8bc954e87636a678c845d02c855919150a54e4af58c179b2184bb9a94` |
| `supplier/ordinary.sqlite` | `dcf9768e3f4e8d16fd5515542bd4b369702580d0c62ac2ec0ec098e2f1ef6cbe` |
| `receiver/ordinary.sqlite` | `e0eaac531af765b29542744300fe9396b801efb3c2014a8c92bc490342688abc` |

Known inclusive CPU is **0.421875 seconds**: Job 0.328125 plus outer wrapper
0.09375. Nested supervision 0.015625 is not added again. Outer wall is 0.937665
seconds and peak Job private commit is 23,056,384 bytes, under the selected
30 CPU seconds / 60 wall seconds / 256 MiB / two-process envelope.

The implemented transport seam has focused positive and refusal evidence. The
next central obligation is integrating ordinary admission and authoring, not
rerunning these controls or promoting inert custody into mathematical authority.
