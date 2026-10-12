//! Native aggregate controls only. This program NEVER verifies receipts.
use dmkn_aggregate_relation::{membership, relation};
use dmkn_module_relation::canonical::{hex, require, sha, R};
use serde_json::{json, Value};
use std::io::Read;

fn run() -> R<Value> {
    let args = std::env::args().collect::<Vec<_>>();
    require(args.len() == 3 && args[1] == "check", "check AGGREGATE_INPUT")?;
    let file = std::fs::File::open(&args[2]).map_err(|e| e.to_string())?;
    const LIMIT: usize = 16 * 1024 * 1024;
    require(file.metadata().map_err(|e| e.to_string())?.len() <= LIMIT as u64, "native aggregate input limit")?;
    let mut bytes = Vec::new();
    file.take(LIMIT as u64 + 1).read_to_end(&mut bytes).map_err(|e| e.to_string())?;
    require(bytes.len() <= LIMIT, "native aggregate growing input limit")?;
    let conclusion = relation::check_bytes(&bytes)?;
    let mut members = Vec::new();
    for (index, journal) in conclusion.members().iter().enumerate() {
        members.push(json!({"index":index,"journal":journal,
            "siblings":membership::opening(conclusion.members(), index as u32)?}));
    }
    let claims = conclusion.assumptions().iter().map(|claim|
        json!({"image":claim.image(),"journal":claim.journal()})).collect::<Vec<_>>();
    let census = conclusion.census();
    Ok(json!({"schema":"DMKN_NATIVE_AGGREGATE_CONCLUSION_V1",
        "status":"CHECKED_CONDITIONAL_AGGREGATE_NOT_ADMISSION", "mathematical_admission":false,
        "input_sha256":hex(&sha(&bytes)),"input_bytes":bytes.len(),"wire_bytes":conclusion.wire_bytes(),
        "header":conclusion.header().encode()?,"assumptions":claims,"members":members,
        "edges":conclusion.edges(),"census":{"rows":census.rows,"bodies":census.bodies,
            "openings":census.openings,"nodes":census.nodes,"maximum_depth":census.maximum_depth,
            "parent_edges":census.parent_edges}}))
}

fn main() {
    let thread = std::thread::Builder::new().name("native_aggregate".into()).stack_size(16_777_216)
        .spawn(|| std::panic::catch_unwind(run));
    let result = match thread {
        Ok(thread) => match thread.join() {
            Ok(Ok(Ok(value))) => value,
            Ok(Ok(Err(reason))) => json!({"status":"REFUSED","reason":reason,"mathematical_admission":false}),
            _ => json!({"status":"REFUSED","reason":"CHECKER_PANIC_OR_UNRESOLVED_DEMAND",
                       "mathematical_admission":false}),
        },
        Err(_) => json!({"status":"REFUSED","reason":"CHECKER_THREAD_UNAVAILABLE",
                       "mathematical_admission":false}),
    };
    println!("{result}");
    if result["status"] == "REFUSED" { std::process::exit(2); }
}
