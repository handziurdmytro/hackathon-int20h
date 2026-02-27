use crate::AppState;
use crate::geo::{Jurisdiction, Location};
use crate::geometry::{Point, is_in_polygon};
use axum::http::StatusCode;
use csv::Reader;
use serde::{Deserialize, Deserializer, Serialize};
use std::collections::HashMap;
use std::sync::Arc;

#[derive(Debug, Deserialize, Clone)]
pub struct TaxRateRecord {
    pub locality: String,
    pub tax_rate: f64,
    pub reporting_code: String,
    pub is_special: bool,
}

pub fn calculate_tax(
    longitude: f64,
    latitude: f64,
    price: f64,
    app_state: &AppState,
) -> Result<TaxedOrder, StatusCode> {
    let state = app_state.state.clone();
    let point = (longitude, latitude);

    if !is_inside_location(point, state) {
        return Err(StatusCode::UNPROCESSABLE_ENTITY);
    }

    const STATE_RATE: f64 = 0.04;
    const SPECIAL_RATE: f64 = 0.00375;
    const NYC_BOROS: [&str; 5] = ["bronx", "kings", "new york", "queens", "richmond"];

    let mut locality = String::new();
    let mut is_city = false;
    let mut tax_record = None;

    let normalize = |name: &str| -> String {
        name.to_lowercase()
            .replace("county", "")
            .replace("(city)", "")
            .trim()
            .to_string()
    };

    if let Some(city) = app_state
        .cities
        .iter()
        .find(|j| is_inside_jurisdiction(point, j))
    {
        let name = normalize(&city.name);

        if let Some(record) = app_state.taxes.get(&name){
            tax_record = Some(record.clone());
            is_city = true;
            locality = city.name.clone();
        }
    }

    if tax_record.is_none() {
        if let Some(county) = app_state
            .counties
            .iter()
            .find(|j| is_inside_jurisdiction(point, j))
        {
            let name = normalize(&county.name);
            locality = county.name.clone();

            if let Some(record) = app_state.taxes.get(&name){
                tax_record = Some(record.clone());
                if NYC_BOROS.contains(&name.as_str()){
                    is_city = true;
                }
            } else {
                locality = county.name.clone();
            }
        }
    }

    if locality.is_empty() {
        locality = "New York State only".to_string();
    }

    let (composite_rate, has_special) = match &tax_record {
        Some(record) => (record.tax_rate / 100.0, record.is_special),
        None => (STATE_RATE, false),
    };

    let special_rates = if has_special { SPECIAL_RATE } else { 0.0 };
    let mut local_rate = composite_rate - STATE_RATE - special_rates;
    local_rate = (local_rate * 10_000.0).round() / 10_000.0;

    let (city_rate, county_rate) = if is_city {
        (local_rate, 0.0)
    } else {
        (0.0, local_rate)
    };

    let tax_amount = (composite_rate * price * 100.0).round() / 100.0;

    Ok(TaxedOrder {
        composite_tax_rate: composite_rate,
        tax_amount,
        total_amount: price + tax_amount,
        breakdown: TaxBreakdown {
            state_rate: STATE_RATE,
            county_rate,
            city_rate,
            special_rates,
        },
        jurisdictions: vec!["New York State".to_string(), locality],
    })
}

pub fn parse_csv() -> HashMap<String, TaxRateRecord> {
    let path = "../data/taxes/pub718.csv".to_string();
    let mut reader = Reader::from_path(path).unwrap();
    let mut taxes = HashMap::new();

    for record in reader.deserialize() {
        let record: TaxRateRecord = record.unwrap();
        taxes.insert(record.locality.to_lowercase(), record);
    }

    taxes
}

fn is_inside_location(point: Point, location: Arc<Location>) -> bool {
    for x in &*location {
        if is_inside_jurisdiction(point, x) {
            return true;
        }
    }
    false
}

fn is_inside_jurisdiction(point: Point, jurisdiction: &Jurisdiction) -> bool {
    jurisdiction
        .edges
        .iter()
        .any(|polygon| is_in_polygon(point, polygon))
}

#[derive(Serialize, Debug)]
pub struct TaxedOrder {
    composite_tax_rate: f64,
    tax_amount: f64,
    total_amount: f64,
    breakdown: TaxBreakdown,
    jurisdictions: Vec<String>,
}

#[derive(Serialize, Debug)]
pub struct TaxBreakdown {
    state_rate: f64,
    county_rate: f64,
    city_rate: f64,
    special_rates: f64,
}