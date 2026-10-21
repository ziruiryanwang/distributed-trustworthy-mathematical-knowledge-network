# Recompile one small module, retain validated dependencies

2026-10-21, root. Source implementation selection; launch remains separate.

The original aggregate guest operation has an explicit finalization failure.
Its subsequent validation adopted its ELF/map, not every intermediate rlib.
The two guest preflights are preserved as failures; no override is removed.
Historical compiler output naming an intermediate artifact does not record its
then-current hash. A special new trust exception for that module pair would
add complexity without improving the product's acceptance argument.

Choose one fresh original-module compile against the already-adopted Nanoda
guest artifacts. Then compile RC core, aggregate and unchanged guest entry.
This is four project crates, not a general checker, SDK or dependency rebuild.
The exact original module has nine source files, matching adopted native and
guest source maps; combined production closure is21 files. Retained typed
module compilation took4.984375CPU seconds, an estimate of modest marginal
cost, not a guarantee for this source. All selected worker ceilings stay fixed.

Growth owns fresh build03.py/recipes03.py and exact retained-artifact provenance
checks. Adaptive reviews the changed boundary and saved evidence. Root owns
fresh selector03 and unused assembly consumers; release reviews those consumer
interfaces and finalizes the same-target paired adapter. No passing campaign
or historical build is repeated. Only two already-adopted Nanoda files are
copied; the236-file dependency view is reused in place.

Root fully reads/adopts snapshot-host actual audit31b7eaa8: one successful
source-bound link,90.40625knownCPU seconds, clean closure. That executable is
available for the later pair, but no guest has run and no receipt exists.
The exact matched target,75% row ratio,64segment cap and CPU-nonregression
screen are unchanged. The previous sharing workload's saving is not reused
as a benefit coefficient. Successful compilation alone funds no proof.
