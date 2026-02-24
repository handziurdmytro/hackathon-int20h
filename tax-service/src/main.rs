mod geo;
mod geometry;

use axum::http::StatusCode;
use axum::routing::{get, post};
use axum::{Json, Router};
use serde::{Deserialize, Serialize};

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(root))
        .route("/tax", post(handle_task));

    /*TODO: add port to config files*/
    let port = 3030u16;

    let listener = tokio::net::TcpListener::bind(format!("127.0.0.1:{port}"))
        .await
        .unwrap();

    axum::serve(listener, app).await.unwrap();
}

async fn root() -> String {
    "OK\n".to_string()
}

async fn handle_task(Json(payload): Json<Order>) -> Result<(StatusCode, Json<TaxedOrder>), StatusCode> {
    let tax = geo::calculate_tax(payload.latitude, payload.longitude, payload.subtotal);
    Ok((StatusCode::OK, Json(TaxedOrder{tax})))
}

#[derive(Deserialize, Debug)]
struct Order {
    latitude: f64,
    longitude: f64,
    subtotal: f64,
}

#[derive(Serialize, Debug)]
struct TaxedOrder {
    tax: f64,
    /* TODO: add more data */
}