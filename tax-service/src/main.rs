mod geo;
mod geometry;
mod tax;

use crate::geo::{parse_all_data, Location};
use crate::tax::{parse_csv, TaxRateRecord, TaxedOrder};
use axum::extract::State;
use axum::http::StatusCode;
use axum::routing::{get, post};
use axum::{Json, Router};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Instant;

#[tokio::main]
async fn main() {
    let start = Instant::now();
    println!("Start...");

    let (state, cities, counties) = parse_all_data();
    let taxes = parse_csv();

    let shared_state = AppState {
        state: Arc::new(state),
        cities: Arc::new(cities),
        counties: Arc::new(counties),
        taxes: Arc::new(taxes),
    };

    let app = Router::new()
        .route("/", get(root))
        .route("/tax", post(handle_task))
        .with_state(shared_state);

    let port = 3030u16;

    let listener = tokio::net::TcpListener::bind(format!("127.0.0.1:{port}"))
        .await
        .unwrap();

    println!("BOOM!!! Elapsed: {:?}", start.elapsed());
    axum::serve(listener, app).await.unwrap();
}

async fn root() -> String {
    "OK\n".to_string()
}

async fn handle_task(
    State(app_state): State<AppState>,
    Json(payload): Json<Order>,
) -> Result<(StatusCode, Json<TaxedOrder>), StatusCode> {
    Ok((
        StatusCode::OK,
        Json(tax::calculate_tax(
            payload.longitude,
            payload.latitude,
            payload.subtotal,
            &app_state,
        )?),
    ))
}

#[derive(Deserialize, Debug)]
struct Order {
    latitude: f64,
    longitude: f64,
    subtotal: f64,
}
#[derive(Debug, Clone)]
struct AppState {
    pub state: Arc<Location>,
    pub cities: Arc<Location>,
    pub counties: Arc<Location>,
    pub taxes: Arc<HashMap<String, TaxRateRecord>>,
}