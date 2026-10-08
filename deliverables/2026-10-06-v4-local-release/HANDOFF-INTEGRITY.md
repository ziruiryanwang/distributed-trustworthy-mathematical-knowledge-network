# V4 local handoff integrity inventory

2026-10-06 UTC. Root-owned final inventory. All paths below are relative to
`E:\Distributed Trustworthy Mathematical Knowledge Network` unless indicated.
This inventory binds exact bytes; it does not by itself establish mathematical
truth, software security, provenance or independent-host operability.

## Handoff leaves

These four files are in `deliverables/2026-10-06-v4-local-release`. They are
frozen for independent final review. This inventory does not hash itself.

| Leaf | Bytes | SHA-256 |
|---|---:|---|
| `START-HERE.md` | 4772 | `ac89ca5f9179b2552171210bf0ef8ca65b4a7fbd997292bf1a673ece8ca34b03` |
| `RESULTS.md` | 16026 | `84693e9cf85b90a1d14ec0a453875b81770ee103b0e87afb3fe2c2255ba7035c` |
| `extract.py` | 14592 | `2fddc40318f77895fe5f4e93c5ed5917eace8dd496378dbd99f8acea39a20687` |
| `RELEASE-MANIFEST.json` | 2041394 | `cd25b9b2b671c3901bf42402fd5be11923bb6db13f032c068f6e315c07f990d1` |

The standalone extractor and manifest are exact copies of the adopted package
controls. For a new installation, verify these and the archive using independently
adopted hashes and a separately trusted Windows Python 3.13+; do not bootstrap
trust with an interpreter from an unverified archive. See the operator guide.

## Software distribution

The archive is retained once at
`product-local/v4-package-01/mathematical-commons-v4-local.zip`:

- Bytes: `2354272105`.
- SHA-256: `90ffbb12bd16d13eb4f6b916b3cefcf834ca8ff82a33bfc7e772621ad3d49780`.
- Payload: 12,496 files, 2,349,258,239 bytes; the additional manifest makes
  12,497 extracted files, 2,351,299,633 bytes.
- Fresh verified extraction: `product-local/v4-operator-integration-01/commons-v4`.

The adopted actual package audit includes an independent full archive hash and
ZIP-map review. This final inventory reuses that evidence; it does not claim
another complete archive audit. The extraction has been exercised through five
public commands, including checking the actual returned theorem. No duplicated
archive, extraction, proof campaign or test execution is required by this seal.

Packaged guide anchors, relative to the extracted release:

| Leaf | Bytes | SHA-256 |
|---|---:|---|
| `docs/START-HERE.md` | 15385 | `6751c4564bba39f180eca175ca90d0526f2a21ebdecff5dce37f7b06736cc224` |
| `docs/GROWTH-AND-ASSURANCE.md` | 12053 | `d20a2c98653d737bcd48b034095f5e958bcabfc5a01a7be4939409f6935b31ab` |
| `docs/LICENSE-AND-SCOPE.md` | 2332 | `5ec2090105a0492b2c024e23f62ed9d08a05a804c2de88f6b875733fa88f22b0` |

## Adopted terminal audit anchors

These files are in `experiments/v4-package-01`. Root has read and adopted each
within its stated scope; the operational auditor's source-authorship conflict
is explicitly disclosed. The mathematical receiver audit and independent
source/selection reviews remain distinct evidence.

| Audit | Bytes | SHA-256 |
|---|---:|---|
| `PACKAGE-OUTCOME.md` | 4723 | `cefec0ec20579457684206cd8a2b3614ac606b631638d30b4906e61cbdeba9fd` |
| `EXTRACT-OUTCOME.md` | 4230 | `eae7f195162ddedecdffa4364b4499a8b0543ee24ce263c94a4f6f474d687443` |
| `TEST-OUTCOME.md` | 2598 | `08d1fa24983f1ff85de94cd6ed224bbbfd72c035a7ef9d26621b2bc2164b4df5` |
| `OPERATOR-OUTCOME.md` | 13417 | `c7c76e6450e42868349092c2e2cf47ad26438c81877868b3e95ee1a54ab88b3b` |
| `RECEIVER-OUTCOME.md` | 6319 | `04ee0a6e41dbf42c3bad60621c090ed0e9150941743918440a153f941e32d3f8` |

The independent final review is
`experiments/v4-package-01/HANDOFF-AUDIT.md`. It must identify this inventory's
hash and separately check the final report's claim boundaries. It is excluded
from this inventory to avoid a circular hash dependency. Root records the
adopted final review and inventory hashes in mutable `research/NOW.md` and
`research/registry/WORK.md`; those navigation files are not sealed payloads.

No test identity/private key or live node state is included in the release.
License remains undecided; local delivery is not external publication or
deployment. V4's restricted, same-host qualification does not complete the
broader global-scale commons objective.
