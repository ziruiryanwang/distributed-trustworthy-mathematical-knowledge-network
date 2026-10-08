#![no_main]

use dmkn_module_relation::{canonical, relation};
use risc0_zkvm::guest::env;
use std::io::Read;

risc0_zkvm::guest::entry!(main);

fn main() {
    let mut input = env::stdin();
    let mut length = [0u8; 4];
    input.read_exact(&mut length).expect("module witness frame");
    let length = u32::from_le_bytes(length) as usize;
    assert!(length > 0 && length <= canonical::MAX_BYTES, "module witness bound");
    let mut bytes = vec![0u8; length];
    input.read_exact(&mut bytes).expect("module witness bytes");
    let mut trailing = [0u8; 1];
    assert_eq!(input.read(&mut trailing).expect("module witness EOF"), 0, "trailing module witness input");
    let conclusion = relation::check_bytes(&bytes)
        .expect("fully bound mathematical module relation");
    // A self image cannot be embedded inside its own binary. The final receipt
    // verifier MUST pin the actual adopted image and require journal.image to
    // equal it. The same exact image binds every recursively used parent.
    for parent in &conclusion.parent_journals {
        env::verify(conclusion.journal.image, parent.as_slice()).expect("genuine module parent assumption");
    }
    // Receipt generation/receiving additionally must fully discharge recursive
    // assumptions. No native success flag or serialized verified boolean exists.
    env::commit_slice(&conclusion.journal.encode().expect("module journal encoding"));
}
