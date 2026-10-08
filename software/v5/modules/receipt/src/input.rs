//! Move large, already parsed Value fields without reconstructing their trees.
//! Typed leaves still use serde; both map and positional struct forms survive.

use crate::canonical::{require, R};
use nanoda_lib::module_correspondence::BodyOpening;
use serde::{de::DeserializeOwned, Deserialize};
use serde_json::Value;

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Parent {
    pub journal: Vec<u8>,
    pub openings: Vec<Value>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Input {
    pub schema: String,
    pub image: [u32; 8],
    pub rank: u64,
    pub local_spec: Value,
    pub rows: Vec<Value>,
    pub parents: Vec<Parent>,
    pub bodies: Vec<BodyOpening>,
}

fn ordered<const N: usize>(value: Value, keys: [&str; N]) -> R<[Value; N]> {
    match value {
        Value::Object(mut values) => {
            require(values.len() == N && keys.iter().all(|key| values.contains_key(*key)),
                    "exact input record fields")?;
            Ok(std::array::from_fn(|index| values.remove(keys[index]).unwrap()))
        },
        Value::Array(values) => values.try_into().map_err(|_| "exact input record arity".into()),
        _ => Err("input record object or sequence required".into()),
    }
}

fn sequence(value: Value) -> R<Vec<Value>> {
    match value { Value::Array(values) => Ok(values), _ => Err("input array required".into()) }
}

fn typed<T: DeserializeOwned>(value: Value) -> R<T> {
    serde_json::from_value(value).map_err(|error| error.to_string())
}

fn parent(value: Value) -> R<Parent> {
    let [journal, openings] = ordered(value, ["journal", "openings"])?;
    Ok(Parent { journal:typed(journal)?, openings:sequence(openings)? })
}

fn body(value: Value) -> R<BodyOpening> {
    let [universes, digest, expression] = ordered(value, ["universes", "digest", "expression"])?;
    Ok(BodyOpening { universes:typed(universes)?, digest:typed(digest)?, expression })
}

/// Shape/typed extraction only, never mathematical admission. The public
/// relation always hashes/validates the complete input before calling this.
/// serde_json's selected default+std feature set makes Value deserialization
/// structurally the identity; raw_value/arbitrary_precision are not enabled.
pub(crate) fn extract(value: Value) -> R<Input> {
    let [schema, image, rank, local_spec, rows, parents, bodies] = ordered(value,
        ["schema", "image", "rank", "local_spec", "rows", "parents", "bodies"])?;
    Ok(Input { schema:typed(schema)?, image:typed(image)?, rank:typed(rank)?, local_spec,
        rows:sequence(rows)?, parents:sequence(parents)?.into_iter().map(parent).collect::<R<_>>()?,
        bodies:sequence(bodies)?.into_iter().map(body).collect::<R<_>>()? })
}
