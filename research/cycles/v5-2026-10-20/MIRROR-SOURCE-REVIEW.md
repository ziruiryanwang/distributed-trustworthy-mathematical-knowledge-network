# Mirror application: root source argument and independent query construction

2026-10-20. Source review only; no Lean/native/import/query execution.

Root read both complete owner sources and the retained EvaluatorUniqueness.lean
signature. Mirror uses the genuine imported Tree recursor, not a replacement
datatype. At a leaf double mirror reduces to that leaf. At a node it reduces to
node(double-mirror left, double-mirror right). Identity has the same equations.
Thus evaluator_unique applies at B=Tree A with exactly the four supplied `rfl`
equations. Its output is the proposed universal involution statement. This
uses M's theorem, not its proof or a new induction.

For injectivity, Eq.ndrec transports reflexivity along h:mirror x=mirror y
with motive z |-> mirror(mirror x)=mirror z. Its result q is the equality of
double mirrors. The explicit term is (V x)^(-1) ; q ; V y : x=y. It requires
only imported mirror/involution interfaces and the existing equality foundation;
it does not unfold mirror. Root finds no mathematical/source-signature blocker
in sources766750ca and9021d215. Compilation and native correspondence have not
run; do not label this an admitted theorem or actual onward use.

The fixed first source's M address is a target known to this example author,
not evidence of unknown-ID discovery. Root separately authored the pure local
`software/v5/examples/mirror_method/method_query.py`, from the formal evaluator
contract and codec grammar, without reading M's encoded type/opening/packet.
It takes only the previously known Tree module and adopted codec, builds the
11-binder type using named variables lowered to de Bruijn indices, and hashes
its relocated type. It has no file/network lookup, M address or recorded answer
digest. Relocation under two different dummy owners must agree.

Two predeclared universe-order alternatives address the format's parameter-order
sensitivity. They are independently constructible before any answer; at most
two original-budget query generations would be needed. No arbitrary equivalence
or broad corpus scan follows. Binder flags and constructor applications remain
exact; later source review must compare them with the explicit formal contract.
The constructor has not been imported/run or compared with the answer.

core_release or adaptive_audit should review this small constructor after current
assignments; root must not independently approve its own new code. A later actual
owner may validate discovery against the known fixture only after query/resolve,
and must render the contribution using the genuinely returned admitted address,
not silently fall back to the answer embedded in the standalone example.
No experiment or cryptographic work is selected by this checkpoint.
