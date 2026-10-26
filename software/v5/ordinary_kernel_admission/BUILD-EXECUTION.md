# One receiver-only build selected

Root read complete three-file diffs, DESIGN, build.py and BUILD-PLAN; AST-only
parsing of build.py passed. Root fully read/adopts source REVIEW
7c2bb4ce77d954cc5efa854e10712a82bb54e452e304b29a2b10828f07b707c0 and
BUILD-REVIEW b502c570a85b50dbeb792110f5588f0c9a3694a33c00da809eea31493d592f8e.

Select kernel-admission-build01 once through its direct selection JSON under
experiments/v5-local-checks, SHA-256
6b9ca2c90ca8b9796b23f3761a5f339f63cdf1c9d896c71c6d316e875eb66635.
Eight source snapshots and 22 external pins. Inner180wall/120CPU/1024MiB;
outer240wall/150JobCPU/1280MiB/fourprocesses/1MiBstreams. Five dependency-ordered
compiler calls, three reused exact prerequisite objects. No other native work.

Used source/build inputs freeze. Preserve first outcome and partial outputs.
Compilation is not testing or mathematical acceptance. Independent actual build
audit must precede separately selected focused native controls; no package,
owner recovery/init/intake, full authoring rebuild or cap increase is selected.
