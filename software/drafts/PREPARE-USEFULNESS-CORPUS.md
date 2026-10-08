# Preparation-only corpus helper

`prepare_usefulness_corpus.py` is a source-only draft for root's independent
review and execution. Its author has not imported, compiled, executed or tested
it. It creates one evaluator-prepared seven-entry static fixture, not a service,
coordinator, admission, publication, replica-custody grant or consumer trial.
Root must authorize the selected packages' sharing/provenance separately.

## Frozen input contract

Root supplies an independently frozen UTF-8 JSON pin file and its SHA-256. The
schema is exact; paths are absolute local paths and file hashes lowercase hex:

```json
{
  "schema": 1,
  "output": "E:\\ABSOLUTE\\FRESH-OUTPUT",
  "python": {"path": "D:\\Python314\\python.exe", "bytes": 123, "sha256": "..."},
  "helper": {"path": "E:\\ABSOLUTE\\prepare_usefulness_corpus.py", "bytes": 123, "sha256": "..."},
  "install": {
    "path": "E:\\ABSOLUTE\\INSTALLED-PRODUCT",
    "files": {"py/codec.py": {"bytes": 123, "sha256": "..."}}
  },
  "packages": [
    {"path": "E:\\ABSOLUTE\\PACKAGE-01", "files": {"manifest.json": {"bytes": 123, "sha256": "..."}}}
  ]
}
```

The displayed sizes, hashes and shortened maps are placeholders, not runnable
pins. `install.files` is the **entire** installation's file map; each package
map is its entire file map, including every object. Map keys are exact relative
POSIX paths. There must be exactly seven package records in CLI order: the six
selected inventory entries and root's separately qualified lemma package, in
one root-frozen randomized permutation of all seven selected before pinning or
dispatch. Do not systematically place the lemma last or otherwise mark its
position. The helper preserves the frozen CLI order without reshuffling.
No package path is embedded in the helper. Python/helper `path` spellings must
match the actual absolute `sys.executable`/`__file__` strings.

Freeze only quiescent owner-controlled inputs; keep them and the fresh output
parent exclusively controlled during execution. The helper checks all existing
path ancestors for symlinks/Windows reparse points, refuses UNC paths and any
existing output, verifies complete file maps before installed-module imports
and again at completion, and refuses installation bytecode caches. These checks
are not an adversarial filesystem sandbox or atomic snapshot. File maps do not
pin ACLs, timestamps, empty directories, the Python standard library or DLLs.
Only the executable is pinned, not the entire Python runtime.

Selected caps: pin JSON 16 MiB; installation 512 MiB/8,193 files; each package
17 MiB/8,193 files; aggregate package files 64 MiB; each installed analysis
source/seed at most 1 MiB; output census 512 MiB/65,536 files. Directory walks
also cap visited directories at twice the file-count cap plus 64. These are
local refusal ceilings, not a change to root's smaller prospective allocation
or a transient disk/CPU/memory quota. Root must supply external time/CPU/memory
supervision, resource accounting and a quiescent full endpoint census.

## Root-only invocation

After independent source review and a prospective frozen allocation, invoke
the pinned executable under root's bounded supervisor with this argument
vector (all metavariables are replaced by explicit frozen absolute values):

```text
PYTHON -B -E -s -S HELPER --install INSTALL --output FRESH_OUTPUT
  --pins PIN_FILE --pins-sha256 PIN_FILE_SHA256
  --package FROZEN_POSITION_01 --package FROZEN_POSITION_02 --package FROZEN_POSITION_03
  --package FROZEN_POSITION_04 --package FROZEN_POSITION_05 --package FROZEN_POSITION_06
  --package FROZEN_POSITION_07
```

This is one argument-vector illustration, not a multiline shell command. Capture
stdout/stderr and exit status outside `FRESH_OUTPUT`. No automatic retry,
cleanup, service launch, native stage or publication mutation occurs. A refusal
leaves any partial fresh output for audit; an existing directory can never be
resumed or overwritten. An exit-zero success must include the final stdout
receipt with status `CORPUS_FIXTURE_PREPARED_NOT_MATH_ACCEPTANCE`.

## Existing library contracts and evidence

The only installed modules loaded are `py/source_codec.py`, its configured
`py/codec.py`, `py/symbol_index.py`, and `py/peer_wire.py`. Seed input is fixed to
`assets/foundation/seed-verified.json`. `configure_codec` retains its existing
hardcoded codec digest check. `source_codec.read_package` verifies foundation,
object CIDs, inventories, exact root closure and the existing `make_plan`
structural checks. `symbol_index.describe_root` must return `OK` for each root;
its result does not verify or accept a proof/body. Prior mathematical evidence
remains separately audited, and receivers still need ordinary fresh admission.

Formal metadata matches `Checker.metadata`'s nine-field projection, including
the deliberately named `semantic_target` field populated from `semantic_ref`.
It is derived from copied original bytes, not handwritten or normalized by
`Checker.import_package`/`export_package`. All seven roots must be distinct.
Existing `peer_wire.build_view` and `load_view` enforce the actual 65,536-byte
catalog, seven entries within the 32-entry profile, per-package framing limits
and 64-MiB view limit. The constructor itself grants no sharing authority.

Outputs are exact package file copies under `packages/01` through `07`, the
unchanged `input-pins.json`, derived `offers.json`, and `view` with its catalog,
completion record and bundles. `result.json` pins every preceding output file;
the final stdout receipt pins `result.json`, avoiding a self-hash cycle. Retain
both to cover the complete output. The helper then exits: service availability,
endpoint configuration and any matched consumer trial remain separate gates.
