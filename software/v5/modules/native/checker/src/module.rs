//! Conditional module extension checking over an already reconstructed witness.
//!
//! This is NOT a certificate verifier or a public mathematical admission API.
//! Every skipped exact native record is an explicit external premise. The new
//! relation wrapper must bind each premise to codec descriptor/group openings
//! and genuine foundation/module authority before using a successful report.
//! Neither a sender flag nor successful native preflight discharges a premise.

use crate::demand::Demand;
use crate::env::{Declar, ValueSlot};
use crate::name::Name;
use crate::util::{DagMarker, ExportFile, NamePtr};
use std::collections::{BTreeMap, BTreeSet};

pub const CONDITIONAL_STATUS: &str = "CONDITIONAL_MODULE_EXTENSION_ONLY";
pub const MAX_MODULE_DECLARATIONS: usize = 16_384;
pub const MAX_MODULE_PREMISES: usize = 4_096;

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum PremiseAuthority {
    /// Exact adopted foundation binding, NOT a permission to add new axioms.
    Foundation { foundation_digest: [u8; 32] },
    /// These are exact alleged bindings, not verification-success flags.
    Module {
        module: [u8; 32],
        group_descriptor_digest: [u8; 32],
        journal_digest: [u8; 32],
        receipt_digest: [u8; 32],
    },
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ConditionalPremise {
    pub authority: PremiseAuthority,
    /// The exact native name-DAG indices, not rendered strings or map positions.
    pub export_name_indices: Vec<u32>,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ConditionalReport {
    pub status: &'static str,
    pub module: [u8; 32],
    pub checked_local_names: Vec<u32>,
    pub premises: Vec<ConditionalPremise>,
    pub receipt_verification_performed: bool,
    pub mathematical_admission: bool,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Preflight<T> {
    Conditional(T),
    Need(Demand),
    Refused,
}

/// Native-only caller convenience. A guest must call the relation directly and
/// abort if any witness is missing; it must never trust this function's result.
pub fn native_preflight<T>(work: impl FnOnce() -> T + std::panic::UnwindSafe) -> Preflight<T> {
    match std::panic::catch_unwind(work) {
        Ok(result) => Preflight::Conditional(result),
        Err(payload) => match payload.downcast::<Demand>() {
            Ok(demand) => Preflight::Need(*demand),
            Err(_) => Preflight::Refused,
        },
    }
}

fn hex(bytes: &[u8; 32]) -> String {
    const ALPHABET: &[u8; 16] = b"0123456789abcdef";
    let mut out = String::with_capacity(64);
    for byte in bytes {
        out.push(ALPHABET[(byte >> 4) as usize] as char);
        out.push(ALPHABET[(byte & 15) as usize] as char);
    }
    out
}

impl<'p> ExportFile<'p> {
    fn name_has_module_prefix(&self, name: NamePtr<'p>, module: &[u8; 32]) -> bool {
        self.with_ctx(|ctx| {
            let mut cursor = name;
            let mut components = Vec::new();
            loop {
                assert!(components.len() <= 67, "MODULE_NAME_DEPTH");
                match ctx.read_name(cursor) {
                    Name::Anon => break,
                    Name::Str(parent, s, _) => {
                        components.push(Some(ctx.read_string(s).as_ref().to_owned()));
                        cursor = parent;
                    }
                    Name::Num(parent, _, _) => {
                        components.push(None);
                        cursor = parent;
                    }
                }
            }
            components.reverse();
            components.len() > 3
                && components[0].as_deref() == Some("DMKN")
                && components[1].as_deref() == Some("Mod")
                && components[2].as_deref() == Some(hex(module).as_str())
        })
    }

    /// Check all new declarations, including new complete inductive groups,
    /// under EXPLICIT unresolved import/foundation premises.
    ///
    /// The wrapper must derive premises from exact native-record correspondence
    /// and authenticated descriptors. This method cannot infer that authority
    /// from its caller's request and deliberately never reports admission.
    pub fn check_module_extension_conditional(
        &self,
        module: [u8; 32],
        foundation: [u8; 32],
        premises: &[ConditionalPremise],
    ) -> ConditionalReport {
        assert!(self.declars.len() <= MAX_MODULE_DECLARATIONS, "MODULE_DECLARATION_LIMIT");
        assert!(premises.len() <= MAX_MODULE_PREMISES, "MODULE_PREMISE_LIMIT");
        let mut roles = BTreeMap::<usize, usize>::new();
        for (premise_index, premise) in premises.iter().enumerate() {
            assert!(!premise.export_name_indices.is_empty(), "EMPTY_PREMISE");
            assert!(premise.export_name_indices.len() <= MAX_MODULE_DECLARATIONS, "PREMISE_SIZE");
            match &premise.authority {
                PremiseAuthority::Foundation { foundation_digest } =>
                    assert_eq!(*foundation_digest, foundation, "FOUNDATION_PREMISE_BINDING"),
                PremiseAuthority::Module { module: imported, .. } =>
                    assert_ne!(*imported, module, "SELF_MODULE_IMPORT"),
            }
            for index in &premise.export_name_indices {
                let name = NamePtr::from(DagMarker::ExportFile, *index as usize);
                let declaration = self.require_declar(&name);
                assert!(roles.insert(*index as usize, premise_index).is_none(), "DUPLICATE_PREMISE_NAME");
                if let PremiseAuthority::Module { module: imported, .. } = &premise.authority {
                    assert!(self.name_has_module_prefix(declaration.info().name, imported), "IMPORT_NAMESPACE");
                    assert!(!matches!(declaration, Declar::Axiom { .. } | Declar::Quot { .. }),
                            "MODULE_CANNOT_GRANT_AXIOM_OR_PRIMITIVE");
                }
            }
        }

        // Every imported member of an atomic inductive block must have the same
        // exact premise. Never skip only its type and then admit arbitrary rules.
        let mut seen_blocks = BTreeSet::new();
        for &(start, size) in self.mutual_block_sizes.values() {
            if !seen_blocks.insert((start, size)) { continue; }
            let end = start.checked_add(size).expect("INDUCTIVE_BLOCK_OVERFLOW");
            assert!(size > 0 && end <= self.declars.len(), "INDUCTIVE_BLOCK_RANGE");
            let first = self.declars.get_index(start).unwrap().1.info().name.idx();
            let role = roles.get(&first).copied();
            for position in start..end {
                let name = self.declars.get_index(position).unwrap().1.info().name.idx();
                assert_eq!(roles.get(&name).copied(), role, "PARTIAL_IMPORTED_INDUCTIVE_GROUP");
            }
        }

        let mut local_started = false;
        let mut checked = Vec::new();
        for declaration in self.declars.values() {
            let name = declaration.info().name;
            if roles.contains_key(&name.idx()) {
                assert!(!local_started, "ALL_IMPORTS_MUST_PRECEDE_LOCALS");
                // This skip is conditional on the explicit premise, not a
                // successful check, a stored flag or an implicit trusted axiom.
                continue;
            }
            local_started = true;
            assert!(self.name_has_module_prefix(name, &module), "LOCAL_NAMESPACE");
            assert!(!matches!(declaration, Declar::Axiom { .. } | Declar::Quot { .. }),
                    "LOCAL_AXIOM_OR_PRIMITIVE_FORBIDDEN");
            match declaration {
                Declar::Definition { val, .. } | Declar::Opaque { val, .. }
                    | Declar::Theorem { val, .. } =>
                    assert!(matches!(val, ValueSlot::Present(_)), "NEW_LOCAL_VALUE_REQUIRED"),
                _ => (),
            }
            self.check_declar(declaration);
            checked.push(u32::try_from(name.idx()).expect("NAME_INDEX"));
        }
        assert!(!checked.is_empty(), "NO_LOCAL_EXTENSION");
        ConditionalReport {
            status: CONDITIONAL_STATUS,
            module,
            checked_local_names: checked,
            premises: premises.to_vec(),
            receipt_verification_performed: false,
            mathematical_admission: false,
        }
    }
}
