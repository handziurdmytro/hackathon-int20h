mod geo;
mod geometry;
mod tax;

use crate::geo::{Location, parse_all_data};
use crate::tax::{TaxRateRecord, TaxedOrder, parse_csv};
use axum::extract::State;
use axum::http::StatusCode;
use axum::routing::{get, post};
use axum::{Json, Router};
use rayon::iter::ParallelIterator;
use rayon::prelude::IntoParallelRefIterator;
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
        .route("/taxes", post(handle_multiple_tasks))
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

async fn handle_multiple_tasks(
    State(app_state): State<AppState>,
    Json(payload): Json<OrderBatch>,
) -> Result<(StatusCode, Json<TaxedOrderBatch>), StatusCode> {
    let taxes: Vec<TaxedOrder> = payload
        .orders
        .par_iter()
        .map(|order| {
            tax::calculate_tax(order.longitude, order.latitude, order.subtotal, &app_state)
                .unwrap_or_else(|_| TaxedOrder::empty_error(order.latitude, order.longitude))
        })
        .collect();

    Ok((StatusCode::OK, Json(TaxedOrderBatch { taxes })))
}

#[derive(Deserialize, Debug)]
struct Order {
    latitude: f64,
    longitude: f64,
    subtotal: f64,
}

#[derive(Deserialize, Debug)]
struct OrderBatch {
    orders: Vec<Order>,
}

#[derive(Serialize, Debug)]
struct TaxedOrderBatch {
    taxes: Vec<TaxedOrder>,
}

#[derive(Debug, Clone)]
struct AppState {
    pub state: Arc<Location>,
    pub cities: Arc<Location>,
    pub counties: Arc<Location>,
    pub taxes: Arc<HashMap<String, TaxRateRecord>>,
}