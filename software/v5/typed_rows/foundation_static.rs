//! Allocation-free exact comparison with the image-adopted immutable foundation.
//!
//! Generated data is independently bound to policy.rs by source/build evidence.
//! This compares every value; the stored digest label is NOT a runtime oracle.
use serde_json::Value;

pub(crate) enum StaticValue {
    Null,
    Bool(bool),
    U64(u64),
    String(&'static [u8]),
    Array(&'static [StaticValue]),
    Object(&'static [(&'static [u8], StaticValue)]),
}

include!("../modules/receipt/src/foundation_data.rs");

fn same(expected: &StaticValue, actual: &Value) -> bool {
    match (expected, actual) {
        (StaticValue::Null, Value::Null) => true,
        (StaticValue::Bool(a), Value::Bool(b)) => a == b,
        (StaticValue::U64(a), Value::Number(b)) => b.as_u64() == Some(*a),
        (StaticValue::String(a), Value::String(b)) => *a == b.as_bytes(),
        (StaticValue::Array(a), Value::Array(b)) => a.len() == b.len()
            && a.iter().zip(b).all(|(x, y)| same(x, y)),
        (StaticValue::Object(a), Value::Object(b)) => a.len() == b.len()
            && a.iter().zip(b).all(|((key, value), (actual_key, actual_value))|
                *key == actual_key.as_bytes() && same(value, actual_value)),
        _ => false,
    }
}

pub fn matches_rows(rows: &[Value]) -> bool {
    // serde_json is pinned without preserve_order: object iteration is sorted.
    // Exact lengths also refuse ignored metadata, extra keys and omitted rows.
    let StaticValue::Array(expected) = &ADOPTED_FOUNDATION else { unreachable!() };
    rows.len() == expected.len() && expected.iter().zip(rows).all(|(a, b)| same(a, b))
}


/// Same exact foundation equality over borrowed mixed rows, without cloning
/// the fixed prefix or treating a hash label as a substitute for its values.
pub fn matches_mixed_rows(rows: &[nanoda_lib::typed_rows::Row]) -> bool {
    use nanoda_lib::typed_rows::Row;
    let StaticValue::Array(expected) = &ADOPTED_FOUNDATION else { unreachable!() };
    rows.len() == expected.len() && expected.iter().zip(rows).all(|(a, b)| match b {
        Row::Legacy(value) => same(a, value),
        Row::Dag(_) => false,
    })
}
