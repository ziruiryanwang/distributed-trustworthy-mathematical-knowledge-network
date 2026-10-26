# Prepare an ordinary investigator's network operations

This offline kit connects the ordinary Lean workflow to the contact-and-sparse
package interface. It prepares explicit input files; it never starts a provider,
dials a peer, opens owner databases, loads a Lean project or checks mathematics.
Its source and execution disposition are separate from these instructions; see
[IMPLEMENTATION.md](IMPLEMENTATION.md) and the independent review when available.
It is not a completed worldwide v5 release.

Supported runtime profile: Windows x86-64, approved Python 3.14.6 and Lean 4.34.0.
Keep this kit outside the hash-bound package. The selected-interface wrapper
recognizes exactly 45 known auxiliary source roles and 72 native-role names.
It checks the auxiliary bytes, **not** native artifacts, installation-core safety,
report authenticity or mathematical truth. Approve the package/build and runtimes
independently; the product's loader and checker retain their own obligations.

## Obtain one coherent package

The complete source-to-package sequence is:

```text
bounded native build -> fair file-only overlay -> contact overlay -> sparse overlay
       BUILD-RESULT          ASSEMBLY               ASSEMBLY          ASSEMBLY
```

Use the [bounded build recipe](../ordinary_bounded_operations/README.md), then
the [fair assembly recipe](../ordinary_fair_search/README.md). Next use
`ordinary_contact_federation/assemble.py` and finally
`ordinary_sparse_access/assemble.py`, with their corresponding exact OVERLAY.json
files. Both latter commands require:

```text
--source-root --base-package --base-profile-sha256
--base-receipt --base-receipt-sha256 --overlay --overlay-sha256
--output --wall-seconds --cpu-seconds
```

Each base receipt is its **immediate predecessor's ASSEMBLY.json**, not the
original native BUILD-RESULT. Every output is fresh. The overlays copy native
bytes without recompiling; final commands use the **final sparse PROFILE**.
Choose hashes from independently approved inputs/receipts, not guessed names.
See the [sparse package guide](../ordinary_sparse_access/README.md) for the full
selection and failure rules. The older compact source archive does not include
these later overlays or this kit; a new handoff must explicitly include them.
These instructions do not run or authorize a new build automatically.

## Prepare one request, then decide whether to run it

Copy exactly one entry from [examples.json](examples.json)'s `requests` object
into a separate UTF-8 JSON file **without a byte-order mark**. Do not submit the
whole examples catalog. Replace required nulls with actual paths, identities,
choices and exact report hashes. Null TLS/CA fields in loopback examples are
intentional. Whole-custody approval booleans start false deliberately.

All paths must be absolute and owner-controlled. Output leaves must not exist;
their parents must exist. Preparation output, future operation output, inputs,
state and package directories must not overlap. No old output is overwritten.
Finite policy numbers are examples, not capacity guarantees.

For this project's existing selected sparse package, the exact preparation
invocation is the following, **after** you have chosen and saved the request:

```powershell
& 'D:\Python314\python.exe' -I -S -B `
  'E:\Distributed Trustworthy Mathematical Knowledge Network\software\v5\ordinary_network_kit\prepare_selected.py' `
  --package 'E:\Distributed Trustworthy Mathematical Knowledge Network\experiments\v5-local-checks\sparse-access-assembly01\assembled\package' `
  --profile-sha256 '97f93cc66f77ebcecd7a3a341baaaf4725236a8dec5fb9cee3c3e67d478f2834' `
  --request 'C:\commons-work\request-find.json' `
  --output 'C:\commons-work\prepared-find-01'
```

Those C: request/output paths are examples, not files supplied with this kit.
For a relocated or independently approved fresh build, replace package/runtime
paths and use that build's final exact PROFILE hash. The wrapper still rejects
unknown auxiliary layouts; changing a profile argument is not approval of code.
Do not edit the preparer's embedded hashes or use the old predecessor wrapper.

Success creates `config.json`, `arguments.json` and `RECEIPT.json` for a peer
request; stateful requests also get explicit custody limits. Review these files.
The generated arguments are structured tokens, not a command string. They must
be passed to the selected package's bounded `run.py` with separately chosen
runtime paths, fresh diagnostics and original wall/CPU/memory/process/log caps.
Follow [LAUNCHER.md](../ordinary_bounded_operations/LAUNCHER.md); the unchanged
[structured-token example](../ordinary_operator_kit/START-HERE.md#launch-one-prepared-operation)
shows how, but use **this** kit and the **final sparse** profile, not its old paths
or historical profile. Preparation itself executes zero product commands.

## Search, inspect the report, then explicitly select retrieval

1. **Direct search is the default.** Start from `find-atomic`. You choose known
   provider contacts and supported formal specs. Omitting `candidate_mode`
   preserves `atomic-v1`. The broad theorem-kind example teaches the shape;
   selective known-symbol queries are usually more useful at scale.
2. **Sparse search is optional.** `find-sparse` adds `candidate_mode: sparse-v2`
   and two portable-symbol specs. Fill the symbols from actual known bindings,
   not guessed theorem names. A compatible provider may use a configured pair
   index; without a suitable pair it uses atomic traversal in the same V2 grant.
   An old provider rejecting V2 produces a charged incomplete outcome, not an
   automatic V1 retry. Neither mode changes mathematical acceptance.
3. **Unknown provider:** `directory-find` contacts only your selected directory
   seeds, under explicit egress rules, then performs one bounded search using
   admissible short-lived hints. Its optional mode belongs inside `search`.
   Registration and requested routes must agree exactly; every route is a subset
   of the query. The example allows only a particular loopback endpoint. Public
   use instead requires explicit `public-ipv4`, sorted allowed public ports and
   empty test_endpoints; suggested remote hosts need HTTPS/system-CA validation.
   This is not a network security sandbox, a global directory or complete search.
4. **Read the actual report first.** Use the peer operation's `RESULT.json`, not
   the launcher's RUN.json, copied console fragments or an edited result. Check
   failure/cleanup, matches, provider errors, truncation and charged budgets.
   `INCOMPLETE_SEARCH` may contain useful verified positive metadata; an empty
   answer does not prove mathematical absence. A record proof establishes
   committed metadata, not that its theorem has been checked locally.
5. **Choose a candidate and new contacts.** Preview/receive still use the request
   key `find_report`; it may point to an actual successful `find` **or**
   `directory-find` report with the same selected profile. Supply its exact
   SHA-256 and a deliberate zero-based `match_index`. Do not rewrite its operation.
   Replace the example contact label with the selected match's exact `provider`
   label, and explicitly choose that operation's endpoint/TLS policy. The kit
   never copies `learned_contacts` or treats an old hint's lifetime as renewed.
   You may choose an approved replica under that label; fetched identities are
   still checked by the product. A report's provider label authenticates nobody.
6. **Preview, optionally inspect, then receive.** Preview binds the inert type;
   `inspect` subsequently selects a zero-based binding from the actual preview
   report to inspect an unfamiliar definition. It does not precede preview.
   Receive requires another explicit contact selection, your existing state,
   a successful parent report for that state, and a deliberate dependency policy.
   `selected-unit-only` may refuse missing premises; `bounded-closure` permits
   bounded ancestor acquisition. Neither promises cheap arbitrary cold checking.
   Only the actual accepted receive/intake result supplies local mathematical
   acceptance; kit output, preview, inspection and downloaded bytes do not.

The kit's spec subset is portable type symbols, object/declaration kinds and exact
declared-type keys. It does not turn prose into mathematics or guess what an agent
should investigate. See [CONTACTS.md](../ordinary_contact_federation/CONTACTS.md)
for directory limits and [SPARSE-SEARCH.md](../ordinary_sparse_access/SPARSE-SEARCH.md)
for sparse accounting. Those frozen documents' predecessor-kit warnings do not
mean their old wrapper now accepts this layout: use this new wrapper instead.

## Provider: static pair access and finite services

`publish-pairs` demonstrates a fresh optional index. A pair contains **compiled
atomic feature IDs**, not the portable symbol IDs used in query specs. Obtain the
two feature atoms from a genuine selected-profile query's `result.features` in
the correct namespace, or the existing query compiler. Sort each distinct pair,
then sort/deduplicate the 1..8 pair list. Count two oriented rows per matching
pair; quotas and the ordinary index's total limits both matter.

`create: true` requires a fresh directory. To reopen, retain exactly the same
ordinary limits and pair configuration and set `create: false`, as in
`serve-pairs`. Omitting/nulling pairs selects the disabled default; it does **not**
remove an enabled store's requirement for its original configuration. Adding
pairs to an old index is not a migration. Do not alter quotas or reindex material
automatically. An index-admission failure can leave earlier publication targets
or custody previews intact; it does not revoke accepted mathematics.

Ordinary serve exposes the selected custody's **entire addressable contents**.
Approve `share_all_custody` and `exclusive` deliberately. Its finite lease needs
setup and cleanup time in the original launcher budget. `directory-serve` is a
separate state-free finite service holding only your explicit registrations; it
does not start or check the advertised providers. Start neither automatically.
For port 0, wait for actual READY.json and use its nonzero port. The examples use
fixed loopback ports only; they are not a public bootstrap network.

## Continue mathematical work and contribute it

Initialization, approved ordinary-project export, independent intake and accepted
target publication are unchanged. Reuse the predecessor guide's
[concept/theory contribution instructions](../ordinary_operator_kit/START-HERE.md#develop-a-new-concept-or-theory-then-return-it)
and [authoring-offer explanation](../ordinary_operator_kit/AUTHORING-OFFERS.md),
with this wrapper and your final profile. Source suggestions are not execution
approval. Local agents choose concepts, hypotheses and theories; the network
does not require a global task list or a human-intention acceptance field.

Keep failures and partial outputs. There is no background retry, grant renewal,
root selection, automatic publication or source execution. Resource limits are
not hostile-code isolation. The full release still needs its separate assurance,
deployment, maintenance and license decisions; no growth acceleration or worldwide
availability claim follows merely from a successful prepared operation.
