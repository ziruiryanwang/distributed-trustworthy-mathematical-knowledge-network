//! Exact Python codec-compatible canonical JSON and cryptographic hash framing.
//! Unlike serde_json::Value's ordinary parser, duplicate object keys refuse.

use risc0_zkvm::sha::{Impl, Sha256};
use serde::{Deserialize, Deserializer};
use serde::de::{Error, MapAccess, SeqAccess, Visitor};
use serde_json::{Map, Number, Value};
use std::{fmt, io::{self, Write}};

pub const MAX_BYTES: usize = 16 * 1024 * 1024;
pub const MAX_NODES: usize = 1_000_000;
pub type R<T> = Result<T, String>;

pub fn require(condition: bool, reason: &str) -> R<()> {
    if condition { Ok(()) } else { Err(reason.into()) }
}

pub fn fields(value: &Value, keys: &[&str]) -> R<()> {
    let object = value.as_object().ok_or("object required")?;
    require(object.len() == keys.len() && keys.iter().all(|key| object.contains_key(*key)), "exact object fields")
}

pub fn array(value: &Value) -> R<&[Value]> { value.as_array().map(|v| v.as_slice()).ok_or("array required".into()) }
pub fn text(value: &Value) -> R<&str> { value.as_str().ok_or("string required".into()) }
pub fn uint(value: &Value, maximum: u64) -> R<u64> {
    let integer = value.as_u64().ok_or("unsigned integer required")?;
    require(integer <= maximum, "integer bound")?;
    Ok(integer)
}

struct Strict(Value);

impl<'de> Deserialize<'de> for Strict {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Exact;
        impl<'de> Visitor<'de> for Exact {
            type Value = Strict;
            fn expecting(&self, f: &mut fmt::Formatter) -> fmt::Result { write!(f, "integer-only JSON without duplicate keys") }
            fn visit_bool<E: Error>(self, value: bool) -> Result<Strict, E> { Ok(Strict(Value::Bool(value))) }
            fn visit_unit<E: Error>(self) -> Result<Strict, E> { Ok(Strict(Value::Null)) }
            fn visit_u64<E: Error>(self, value: u64) -> Result<Strict, E> { Ok(Strict(Value::Number(Number::from(value)))) }
            fn visit_i64<E: Error>(self, _value: i64) -> Result<Strict, E> { Err(E::custom("negative integer forbidden")) }
            fn visit_f64<E: Error>(self, _value: f64) -> Result<Strict, E> { Err(E::custom("noninteger number forbidden")) }
            fn visit_str<E: Error>(self, value: &str) -> Result<Strict, E> { Ok(Strict(Value::String(value.to_owned()))) }
            fn visit_string<E: Error>(self, value: String) -> Result<Strict, E> { Ok(Strict(Value::String(value))) }
            fn visit_seq<A: SeqAccess<'de>>(self, mut sequence: A) -> Result<Strict, A::Error> {
                let mut values = Vec::new();
                while let Some(value) = sequence.next_element::<Strict>()? {
                    if values.len() >= MAX_NODES { return Err(A::Error::custom("array bound")); }
                    values.push(value.0);
                }
                Ok(Strict(Value::Array(values)))
            }
            fn visit_map<A: MapAccess<'de>>(self, mut mapping: A) -> Result<Strict, A::Error> {
                let mut values = Map::new();
                while let Some(key) = mapping.next_key::<String>()? {
                    if values.len() >= MAX_NODES || values.contains_key(&key) {
                        return Err(A::Error::custom("duplicate key or object bound"));
                    }
                    values.insert(key, mapping.next_value::<Strict>()?.0);
                }
                Ok(Strict(Value::Object(values)))
            }
        }
        deserializer.deserialize_any(Exact)
    }
}

fn parse_syntax(bytes: &[u8]) -> R<Value> {
    require(!bytes.is_empty() && bytes.len() <= MAX_BYTES, "input byte bound")?;
    let mut deserializer = serde_json::Deserializer::from_slice(bytes);
    let value = Strict::deserialize(&mut deserializer).map_err(|e| e.to_string())?.0;
    deserializer.end().map_err(|e| e.to_string())?;
    // The parser retains its safe default nesting bound; do not silently
    // advertise the pure codec's wider 192-depth envelope for this profile.
    Ok(value)
}

pub fn parse(bytes: &[u8]) -> R<Value> {
    let value = parse_syntax(bytes)?;
    canonical(&value)?;
    Ok(value)
}

/// Strict raw entry with the same canonical structure/size domain as parse,
/// without serializing or hashing a whole execution witness.
pub fn parse_validated(bytes: &[u8]) -> R<Value> {
    let value = parse_syntax(bytes)?;
    canonical_size(&value)?;
    Ok(value)
}

/// Representation-bounded strict parse, NOT mathematical or receipt authority.
/// Only parse_bounded constructs this immutable owned token. No caller-provided
/// counts or mutable Value access can invalidate its structural invariant.
pub struct BoundedValue {
    value: Value,
    nodes: usize,
    maximum_depth: usize,
}

impl BoundedValue {
    pub fn as_value(&self) -> &Value { &self.value }
    pub fn nodes(&self) -> usize { self.nodes }
    pub fn maximum_depth(&self) -> usize { self.maximum_depth }
    pub(crate) fn into_value(self) -> Value { self.value }
}

// Counts Value nodes (not keys), root depth zero. Parameterization is private;
// production always supplies MAX_NODES and 256, never caller-selected limits.
fn structural_counts(value: &Value, node_limit: usize, depth_limit: usize) -> R<(usize, usize)> {
    fn visit(value: &Value, depth: usize, nodes: &mut usize, maximum_depth: &mut usize,
             node_limit: usize, depth_limit: usize) -> R<()> {
        *nodes = nodes.checked_add(1).ok_or("canonical structure overflow")?;
        require(depth <= depth_limit && *nodes <= node_limit, "canonical structure bound")?;
        *maximum_depth = (*maximum_depth).max(depth);
        match value {
            Value::Array(values) => for value in values {
                visit(value, depth.checked_add(1).ok_or("canonical depth overflow")?,
                      nodes, maximum_depth, node_limit, depth_limit)?;
            },
            Value::Object(values) => for value in values.values() {
                visit(value, depth.checked_add(1).ok_or("canonical depth overflow")?,
                      nodes, maximum_depth, node_limit, depth_limit)?;
            },
            _ => {},
        }
        Ok(())
    }
    let (mut nodes, mut maximum_depth) = (0, 0);
    visit(value, 0, &mut nodes, &mut maximum_depth, node_limit, depth_limit)?;
    Ok((nodes, maximum_depth))
}

/// The pinned strict integer-only JSON parser and compact formatter satisfy
/// len(K_infinity(parse_syntax(bytes))) <= bytes.len(). Thus the unchanged raw
/// MAX_BYTES cap implies the canonical byte bound. A separate structural count
/// remains mandatory; raw length does NOT imply MAX_NODES or depth limits.
/// This lemma does not apply to arbitrary caller-created Values.
pub fn parse_bounded(bytes: &[u8]) -> R<BoundedValue> {
    let value = parse_syntax(bytes)?;
    let (nodes, maximum_depth) = structural_counts(&value, MAX_NODES, 256)?;
    Ok(BoundedValue { value, nodes, maximum_depth })
}

// Counter-only test seam; it never constructs or returns a BoundedValue.
#[cfg(test)]
pub(super) fn test_shape(value: &Value, node_limit: usize, depth_limit: usize) -> R<(usize, usize)> {
    structural_counts(value, node_limit, depth_limit)
}

/// Exact byte length of canonical(value), under identical bounds. Object key
/// order changes no lengths. serde_json's compact formatter emits valid UTF-8
/// unchanged except quotes, backslashes and ASCII controls; keys follow the
/// same string rule. Nodes count Values, not keys, exactly as canonical does.
pub fn canonical_size(value: &Value) -> R<usize> {
    struct Census { bytes: usize, nodes: usize }
    impl Census {
        fn add(&mut self, count: usize) -> R<()> {
            require(count <= MAX_BYTES.saturating_sub(self.bytes), "canonical byte bound")?;
            self.bytes += count;
            Ok(())
        }
        fn string(&mut self, value: &str) -> R<()> {
            self.add(2)?;
            // UTF-8 continuation bytes and all non-ASCII bytes pass through.
            for byte in value.bytes() {
                self.add(match byte {
                    b'"' | b'\\' | b'\x08' | b'\x0c' | b'\n' | b'\r' | b'\t' => 2,
                    0..=0x1f => 6,
                    _ => 1,
                })?;
            }
            Ok(())
        }
        fn visit(&mut self, value: &Value, depth: usize) -> R<()> {
            self.nodes += 1;
            require(depth <= 256 && self.nodes <= MAX_NODES, "canonical structure bound")?;
            match value {
                Value::Null => self.add(4),
                Value::Bool(value) => self.add(if *value { 4 } else { 5 }),
                Value::Number(value) => {
                    let mut number = value.as_u64().ok_or("canonical unsigned integer")?;
                    let mut digits = 1;
                    while number >= 10 { number /= 10; digits += 1; }
                    self.add(digits)
                },
                Value::String(value) => self.string(value),
                Value::Array(values) => {
                    self.add(2)?;
                    self.add(values.len().saturating_sub(1))?;
                    for value in values { self.visit(value, depth + 1)?; }
                    Ok(())
                },
                Value::Object(values) => {
                    self.add(2)?;
                    self.add(values.len().saturating_sub(1))?;
                    for (key, value) in values {
                        self.string(key)?; self.add(1)?; self.visit(value, depth + 1)?;
                    }
                    Ok(())
                },
            }
        }
    }
    let mut census = Census { bytes: 0, nodes: 0 };
    census.visit(value, 0)?;
    Ok(census.bytes)
}

/// Internal jointly validated entry: hash enforces the complete canonical
/// structure/size contract before the parsed Value leaves this function.
pub(crate) fn parse_hashed(domain: &str, bytes: &[u8]) -> R<(Value, [u8; 32])> {
    let value = parse_syntax(bytes)?;
    let digest = hash(domain, &value)?;
    Ok((value, digest))
}

struct Bounded(Vec<u8>);
impl Write for Bounded {
    fn write(&mut self, bytes: &[u8]) -> io::Result<usize> {
        if bytes.len() > MAX_BYTES.saturating_sub(self.0.len()) {
            return Err(io::Error::new(io::ErrorKind::Other, "canonical byte bound"));
        }
        self.0.extend_from_slice(bytes); Ok(bytes.len())
    }
    fn flush(&mut self) -> io::Result<()> { Ok(()) }
}

pub fn canonical(value: &Value) -> R<Vec<u8>> {
    fn emit(out: &mut Bounded, value: &Value, depth: usize, nodes: &mut usize) -> R<()> {
        *nodes += 1;
        require(depth <= 256 && *nodes <= MAX_NODES, "canonical structure bound")?;
        match value {
            Value::Array(values) => {
                out.write_all(b"[").map_err(|e| e.to_string())?;
                for (index, value) in values.iter().enumerate() {
                    if index != 0 { out.write_all(b",").map_err(|e| e.to_string())?; }
                    emit(out, value, depth + 1, nodes)?;
                }
                out.write_all(b"]").map_err(|e| e.to_string())?;
            },
            Value::Object(values) => {
                out.write_all(b"{").map_err(|e| e.to_string())?;
                let mut keys = values.keys().collect::<Vec<_>>(); keys.sort();
                for (index, key) in keys.into_iter().enumerate() {
                    if index != 0 { out.write_all(b",").map_err(|e| e.to_string())?; }
                    serde_json::to_writer(&mut *out, key).map_err(|e| e.to_string())?;
                    out.write_all(b":").map_err(|e| e.to_string())?;
                    emit(out, &values[key], depth + 1, nodes)?;
                }
                out.write_all(b"}").map_err(|e| e.to_string())?;
            },
            Value::Number(number) => {
                require(number.as_u64().is_some(), "canonical unsigned integer")?;
                serde_json::to_writer(&mut *out, number).map_err(|e| e.to_string())?;
            },
            _ => serde_json::to_writer(&mut *out, value).map_err(|e| e.to_string())?,
        }
        Ok(())
    }
    let mut result = Bounded(Vec::new());
    emit(&mut result, value, 0, &mut 0)?;
    Ok(result.0)
}

pub fn sha(bytes: &[u8]) -> [u8; 32] { Impl::hash_bytes(bytes).as_bytes().try_into().unwrap() }

pub fn hash(domain: &str, value: &Value) -> R<[u8; 32]> {
    require(domain.is_ascii() && domain.len() <= 128, "hash domain")?;
    let encoded = canonical(value)?;
    Ok(hash_encoded(domain, &encoded))
}

/// Return raw-canonical SHA and framed-domain hash after one checked encoding.
/// Arbitrary caller-supplied bytes or claimed digests are never inputs.
pub(crate) fn hash_with_canonical_sha(domain: &str, value: &Value) -> R<([u8; 32], [u8; 32])> {
    require(domain.is_ascii() && domain.len() <= 128, "hash domain")?;
    let encoded = canonical(value)?;
    Ok((sha(&encoded), hash_encoded(domain, &encoded)))
}

// Both callers above validate the domain and construct encoded with canonical.
fn hash_encoded(domain: &str, encoded: &[u8]) -> [u8; 32] {
    let mut frame = b"DMKN-V5-MODULE\0".to_vec();
    frame.extend_from_slice(&(domain.len() as u32).to_be_bytes());
    frame.extend_from_slice(domain.as_bytes());
    frame.extend_from_slice(&(encoded.len() as u64).to_be_bytes());
    frame.extend_from_slice(encoded);
    sha(&frame)
}

pub fn hex(bytes: &[u8; 32]) -> String { bytes.iter().map(|byte| format!("{byte:02x}")).collect() }
pub fn unhex(value: &str) -> R<[u8; 32]> {
    require(value.len() == 64 && value.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)), "lowercase digest")?;
    let mut bytes = [0u8; 32];
    for (index, byte) in bytes.iter_mut().enumerate() {
        *byte = u8::from_str_radix(&value[index * 2..index * 2 + 2], 16).map_err(|e| e.to_string())?;
    }
    Ok(bytes)
}
