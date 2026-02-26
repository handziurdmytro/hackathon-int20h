use crate::geo::{Jurisdiction, Location};
use crate::geometry::{is_in_polygon, Point};
use crate::AppState;
use axum::http::StatusCode;
use csv::Reader;
use serde::{Deserialize, Deserializer, Serialize};
use std::collections::HashMap;
use std::sync::Arc;

#[derive(Debug, Deserialize, Clone)]
pub struct TaxRateRecord {
    #[serde(rename = "County_or_Locality")]
    pub locality: String,
    #[serde(rename = "Tax_Rate")]
    pub tax_rate: f64,
    #[serde(rename = "Reporting_Code")]
    pub reporting_code: String,
    #[serde(rename = "is_special")]
    pub special: bool,
}

pub fn calculate_tax(
    latitude: f64,
    longitude: f64,
    price: f64,
    app_state: &AppState,
) -> Result<TaxedOrder, StatusCode> {
    let state = app_state.state.clone();
    if !is_inside_location((latitude, longitude), state) {
        return Err(StatusCode::NOT_FOUND); //todo: change
    }
    let cities = Arc::clone(&app_state.cities);
    let counties = Arc::clone(&app_state.counties);
    let taxes = Arc::clone(&app_state.taxes);

    let mut target = "New York State only".to_string();
    if let Some(city) = cities
        .iter()
        .find(|j| is_inside_jurisdiction((latitude, longitude), j))
    {
        target = city.name.clone();
    } else if let Some(county) = counties
        .iter()
        .find(|j| is_inside_jurisdiction((latitude, longitude), j))
    {
        target = county.name.clone();
    }

    let tax = taxes
        .get(&target.to_lowercase())
        .cloned()
        .unwrap_or(TaxRateRecord {
            tax_rate: 4.0,
            reporting_code: "0".to_string(),
            special: false,
            locality: target,
        });

    let rate = tax.tax_rate / 100.0;
    let tax_amount = rate * price;
    Ok(TaxedOrder {
        composite_tax_rate: rate,
        tax_amount,
        total_amount: price + tax_amount,
        breakdown: TaxBreakdown {
            state_rate: 0.0,
            city_rate: 0.0,
            county_rate: 0.0,
            special_rates: 0.0,
        },
        jurisdictions: vec![tax.locality],
    })
}

pub fn parse_csv() -> HashMap<String, TaxRateRecord> {
    let path = "../data/taxes/pub718.csv".to_string();
    let mut reader = Reader::from_path(path).unwrap();
    let mut taxes = HashMap::new();

    for record in reader.deserialize() {
        let record: TaxRateRecord = record.unwrap();
        taxes.insert(record.locality.clone(), record);
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
    city_rate: f64,
    county_rate: f64,
    special_rates: f64,
}
