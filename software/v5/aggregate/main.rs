#![no_main]

use dmkn_aggregate_relation::relation;
use risc0_zkvm::guest::env;

risc0_zkvm::guest::entry!(main);

fn main() {
    let conditional = relation::check_reader(env::stdin()).expect("conditional aggregate mathematical relation");
    // ALL unique actual claims must be discharged. Native checking, membership,
    // advertised receipts and serialized success fields never replace this.
    for assumption in conditional.assumptions() {
        env::verify(assumption.image(), assumption.journal()).expect("genuine aggregate boundary assumption");
    }
    // The final receiver MUST pin actual A and require header.A == actual A.
    // Production/receiving MUST fully resolve all recursive receipt assumptions.
    env::commit_slice(&conditional.header().encode().expect("exact aggregate header"));
}
