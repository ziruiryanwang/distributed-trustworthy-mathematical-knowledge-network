# Public contact-federation selection

Status: source-only launch specification; not executed by this author. Root owns
the launch decision and actual-result adoption. No previous test is renewed.

The exact selection is `experiments/contact-federation-public01-selection.json`.
It snapshots the frozen finite runner and independently reviewed
`software/v5/ordinary_contact_federation/test_public.py` (SHA-256
`98f3eb0b60e95bcdadca280c636c65ddaa2b6be47793ea43c264ab20abef7879`).
The independent full-source reviewer, `/root/concept_software_bridge`, gave GO
for this harness; that review is not an execution result.

## Package and binding

The package is the actual new
`experiments/v5-local-checks/contact-federation-assembly01/assembled/package`.
Its observed PROFILE SHA-256 is
`3d127796190ca3d049bd956288025c10c4ac7e383a15685aca6ea8d2fbc61479`;
the assembly receipt SHA-256 is
`02739f6f44aeb0d56765dea12f82a5e195c1040379db9407221254d7f2dbe79d`.
The receipt reports 149 files excluding PROFILE, ten changed/added payloads and
139 unchanged payloads. Assembly is file-only, not mathematical acceptance.

The selection pins Python's executable and two core DLLs, the assembly receipt,
PROFILE, the profile loader and the public launcher before and after the command.
The harness pins PROFILE and loader before loading the package; that selected
loader checks the payload map and installation manifest, and the installation
verifier checks remaining installed payloads and named runtime attachments.
This is a chained package-binding check, not a claim of a hermetic operating
system or hostile-local-writer protection. No Lean process is selected.

## Changed boundary and envelope

One fresh synthetic, inert ordinary-preview record is offered by a real local
provider. A separate public `directory-serve` command advertises its contact.
A separate public `directory-find` command receives only the directory contact,
learns the provider through HTTP and returns the exact record. The explicit
loopback egress port is permission, not a discovery input. The harness checks
one directory lookup, two search exchanges, the single combined prepaid grant,
false mathematical-acceptance/completeness flags, the original service lease
and clean child/provider/index/connection closure.

Outer bounds: 90 wall seconds, 60 inclusive worker-Job CPU seconds, 1024 MiB,
eight processes, 1 MiB each stdout and stderr. Supervisor CPU is separately
reported. Harness bounds remain 80 wall / 45 own CPU seconds; public service
and reader bounds remain 60/45 wall seconds respectively, each 25 CPU seconds,
512 MiB and three processes. Parallel child overlap is covered by the outer
process/memory allowance; no limit renewal or retry is selected.

This tests public command integration and bounded advisory contact discovery
using loopback HTTP. It does not test TLS, independent hosting, mathematical
acceptance, semantic relevance, corpus completeness, useful-growth advantage
or global-scale deployment. Existing mathematical state is not opened.
