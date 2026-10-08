//! Bounded execution-only PC sampling. Never creates a receipt or admission.
//!
//! Unlike the SDK pprof finalizer, this retains samples after an execution error.
//! Counts are deterministic instruction samples, NOT attributed proof-cycle cost.
use super::*;
use risc0_zkvm::TraceEvent;

const SAMPLE_STRIDE: u64 = 256;
const SAMPLE_CELLS: usize = 131_072;

pub fn trace(args: &[String]) -> Result<()> {
    ensure!(args.len() == 8,
        "trace IMAGE INPUT EXPECTED_JOURNAL CYCLES PO2 FRESH_DIAGNOSTIC_JSON (no parents)");
    fresh(&args[7])?;
    // A diagnostic must not write an implicit SDK profile to an ambient path.
    ensure!(env::var_os("RISC0_PPROF_OUT").is_none(), "ambient profiler output forbidden");
    let image = read_bounded(&args[2], FILE_LIMIT)?;
    let id = compute_image_id(&image)?;
    let input = read_bounded(&args[3], INPUT_LIMIT)?;
    let expected = read_bounded(&args[4], JOURNAL_LIMIT)?;
    let bound = module_input(&input, id)?;
    ensure!(bound.parents.is_empty() && bound.child.rank == 0, "diagnostic is parent-free only");
    ensure!(checked(bound.child.encode())? == expected, "exact diagnostic expected journal");
    let cycles: u64 = args[5].parse()?;
    let po2: u32 = args[6].parse()?;
    ensure!((1..=(1 << 25)).contains(&cycles) && (12..=20).contains(&po2),
        "diagnostic does not widen original cycle ceiling");
    let mut instructions = 0u64;
    let mut sampled = 0u64;
    let mut max_cycle = 0u64;
    let mut last_cycle = None;
    let mut backwards_cycle_events = 0u64;
    let mut sample_limit_hit = false;
    // (reported cycle window, exact PC) -> deterministic sample count.
    let mut samples = BTreeMap::<(u64, u32), u64>::new();
    let started = Instant::now();
    let result = {
        let mut builder = ExecutorEnv::builder();
        builder.write_slice(&input).session_limit(Some(cycles)).segment_limit_po2(po2);
        builder.trace_callback(|event| {
            if let TraceEvent::InstructionStart { cycle, pc, .. } = event {
                instructions = instructions.checked_add(1).context("instruction counter overflow")?;
                if last_cycle.is_some_and(|previous| cycle < previous) {
                    backwards_cycle_events += 1;
                }
                last_cycle = Some(cycle);
                max_cycle = max_cycle.max(cycle);
                if (instructions - 1) % SAMPLE_STRIDE == 0 {
                    let key = (cycle >> 20, pc);
                    if samples.len() >= SAMPLE_CELLS && !samples.contains_key(&key) {
                        sample_limit_hit = true;
                        anyhow::bail!("diagnostic sample cell bound");
                    }
                    *samples.entry(key).or_default() += 1;
                    sampled += 1;
                }
            }
            Ok(())
        });
        LocalProver::new("dmkn-module-partial-trace").execute(builder.build()?, &image)
    };
    let elapsed_ms = started.elapsed().as_millis();
    let (outcome, error, completed) = match result {
        Ok(session) => {
            ensure!(session.exit_code == ExitCode::Halted(0) && session.journal.bytes == expected,
                "exact diagnostic successful conclusion");
            ("EXECUTION_COMPLETED_NO_CERTIFICATE", None,
             Some(json!({"segments":session.segments.len(), "rows":session.rows()})))
        },
        Err(error) => ("EXECUTION_ERROR_PARTIAL_SAMPLES", Some(format!("{error:#}")), None),
    };
    let rows = samples.into_iter().map(|((window, pc), count)| json!([window, pc, count]))
        .collect::<Vec<_>>();
    let report = json!({"schema":"DMKN_EXECUTION_PC_SAMPLE_V1", "outcome":outcome,
        "mathematical_admission":false, "proof_calls":0, "image_id":id.to_string(),
        "input_sha256":canonical::hex(&canonical::sha(&input)),
        "expected_journal_sha256":canonical::hex(&canonical::sha(&expected)),
        "cycle_ceiling":cycles, "segment_po2":po2, "sample_stride":SAMPLE_STRIDE,
        "sample_cell_limit":SAMPLE_CELLS, "sample_limit_hit":sample_limit_hit,
        "instructions_observed":instructions, "samples_observed":sampled,
        "max_reported_cycle":max_cycle, "backwards_cycle_events":backwards_cycle_events,
        "sample_window_cycles":1 << 20, "samples":rows, "elapsed_ms":elapsed_ms,
        "execution_error":error, "completed_execution":completed,
        "measurement":"DETERMINISTIC_INSTRUCTION_SAMPLES_NOT_PROOF_CYCLE_ATTRIBUTION"});
    write_new(&args[7], &serde_json::to_vec(&report)?)?;
    println!("DIAGNOSTIC_SAVED_NOT_CERTIFIED outcome={outcome} instructions={instructions} samples={sampled}");
    // A saved partial diagnostic is successful collection, never successful checking.
    Ok(())
}
