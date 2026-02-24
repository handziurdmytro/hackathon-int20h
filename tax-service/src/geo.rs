use serde::{Deserialize, Serialize};
use std::fs;

pub fn parse_geo_data_file() {
    /* Storage -> RAM */
}

#[derive(Serialize, Deserialize, Debug)]
struct GeoData {
    #[serde(rename = "type")]
    data_type: String,
    features: Vec<Feature>,
}

#[derive(Serialize, Deserialize, Debug)]
struct Feature {
    #[serde(rename = "type")]
    feature_type: String,
    properties: serde_json::Value,
    // geometry: Vec<serde_json::Value>,
}

pub fn calculate_tax(latitude: f64, longitude: f64, price: f64) -> f64 {
    666.666
}

pub fn read_geo_json(path: String) -> Result<(), Box<dyn std::error::Error>> {
    let content = fs::read_to_string(path)?;
    let parsed: GeoData = serde_json::from_str(&content)?;

    println!("{:#?}", parsed);

    Ok(())
}
