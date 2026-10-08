# Replica contract 01: integration and exact-launch review

2026-09-21, independent reviewer `context_dependency_audit`.

**PASS: exact reviewed integration and fresh bounded launch. No blocking finding.** This is permission at the source/launch gate only, not an execution result or native/serving/availability qualification. Root alone executes once and audits the retained outcome. The full 14-contract source review remains `REPLICA-CONTRACT-CODE-REVIEW.md`; it was not repeated here.

## Integration

Using only inert PowerShell/.NET text operations, this reviewer reconstructed the reviewed unified diff against all six preserved bases in `E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\ordinary-abort-native-02\install`. Every context/deletion line and old/new hunk count matched; all 14 hunks reconstructed text exactly equal the six actual integrated files. The preserved base hashes equal those in `REPLICA-CODE-REVIEW.md`. No patch was applied by this reviewer.

Reviewed patch: 22,216 bytes, SHA-256 `5618AE27E3FF592C6D8F1BDD7EAD6DAB23DE81D8CE07103329D917CA6DD72EBA`.

| Integrated target under `software` | Bytes | SHA-256 |
| --- | ---: | --- |
| `py/peer_node.py` | 22,334 | `296DE6D198A6A67995BF24D3FD27A4CA779F988C0A1303F5871999FF9158B2E3` |
| `py/service_worker.py` | 8,140 | `7D9D80DB3318DE67273B36C35EAE3FCEE02CF8BD6118D34B11D42CB8884A2979` |
| `py/peer_wire.py` | 16,924 | `BDF71281B0BCB81B762551AE33B502A9F75534774E11393A1B0B6131797E798C` |
| `py/node.py` | 25,402 | `635847507F823EF71358B0D619935B5581D2EA64C805FD4DB2162F0297D40866` |
| `manage.py` | 14,303 | `153BE0535329AAD8D05CEBAE7C1659C84CCD4E5098C6B0F63CE23846540476CF` |
| `py/recovery_worker.py` | 19,588 | `F327D76B42529C5E3ECAC5B4439D16C1121982697FBCA592ECAFCFFCFB5C53BC` |

The suite remains 35,765 bytes / `42834201F49FB6FB75F052B4D9BB2D411D91511220C77EB110B0756BFF3122D7`. The reviewed registry runner remains 12,490 bytes / `6D841EF83299961E381576E9966BCE3709DB88F9EE4D2FBDDEF17831AB241088`. No suite or registry change invalidates the preceding source review. `manage.py` is integration-checked but not a suite input: these contracts neither import nor invoke it.

## Exact launch

Launch: `E:\Distributed Trustworthy Mathematical Knowledge Network\software\qualification\replica-custody-contract-launch-01.json`, 3,717 bytes, SHA-256 `9A30D5D07BEFC1E514F8A9B4134C2DDE36C80BDE97BC2A0F4164D3C425D5B763`.

Schema 1, allocation `replica-custody-contract-01`, suite `test_replica_custody.py`, and count 14 match the actual reviewed registry. All 15 ordered path/size/hash pins were independently checked against current files. Their order is interpreter, runner, `run_stage.py`, `supervise.py`, `domains.py`, the nine reviewed suite-specific modules (`capacity`, `storage`, `node`, `peer_wire`, `peer_service`, `peer_node`, `inspect_context`, `service_worker`, `recovery_worker`), then the suite. All 15 paths are distinct, and the 14 archived-source basenames are distinct.

The supervisor appends the exact launch pin: 16 pins total, 367,923 bytes (364,206 input bytes plus launch), within its 16-pin / 64-MiB total / 16-MiB-per-file limits. This is the reviewed ten-product-module closure, including shared `domains.py`; it does not claim checker or public-management coverage.

Limits exactly match the unchanged runner: 60 wall seconds, 30 Job CPU seconds, 512 MiB, 8 active processes, and 65,536 bytes each for stdout/stderr/event. Retention exactly matches 268,435,456 bytes / 4,096 files / 8,192 entries. These are ceilings, not measurements. The coordinator remains outside the worker Job; its copying/census and startup/final-persistence measurement exclusions remain as stated by the runner.

At this review's inspection, neither allocation root existed, including any same-name filesystem entry:

- `E:\Distributed Trustworthy Mathematical Knowledge Network\software\qualification\replica-custody-contract-01`
- `E:\Distributed Trustworthy Mathematical Knowledge Network\product-local\replica-custody-contract-01`

The launch, all input paths, both existing allocation parents and their ancestors were checked: 25 distinct filesystem paths, no reparse points. The roots are separate from the installation. The runner independently repeats freshness, path and exact ordered-pin checks before creating either root. Root must retain the required `-B -E -s -S` Windows interpreter profile, run this allocation only once, preserve any failure, and use a new allocation and pins for any correction.

This reviewer did not import, parse/compile, execute or test Python/product code, query SQLite, or mutate any preserved source/evidence. Only this note was authored. Root's separate AST-only check is not represented as execution evidence. A later contract result must retain the source review's synthetic acquisition/quiescence, mocked preparation/supply, and no native acceptance or successful serving boundaries.
