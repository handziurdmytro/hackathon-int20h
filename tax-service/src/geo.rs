use crate::geometry::Edge;
use serde::{Deserialize, Serialize};
use std::fs;

pub type Location = Vec<Jurisdiction>;

#[derive(Debug)]
pub struct Jurisdiction {
    pub name: String,
    pub edges: Vec<Vec<Edge>>,
}

fn parse_geo_data_files() -> (
    GeoData<StateProperties>,
    GeoData<CitiesProperties>,
    GeoData<CountiesProperties>,
) {
    let state_path = String::from("../data/geo/State.json");
    let cities_path = String::from("../data/geo/Cities.json");
    let counties_path = String::from("../data/geo/Counties.json");

    let state_content = fs::read_to_string(state_path).unwrap();
    let cities_content = fs::read_to_string(cities_path).unwrap();
    let counties_content = fs::read_to_string(counties_path).unwrap();

    let state: GeoData<StateProperties> = serde_json::from_str(&state_content).unwrap();
    let cities: GeoData<CitiesProperties> = serde_json::from_str(&cities_content).unwrap();
    let counties: GeoData<CountiesProperties> = serde_json::from_str(&counties_content).unwrap();

    (state, cities, counties)
}

#[derive(Serialize, Deserialize, Debug)]
struct GeoData<P> {
    #[serde(rename = "type")]
    data_type: String,
    features: Vec<Feature<P>>,
}

#[derive(Serialize, Deserialize, Debug)]
struct Feature<P> {
    #[serde(rename = "type")]
    feature_type: String,
    properties: P,
    geometry: Geometry,
}

#[derive(Serialize, Deserialize, Debug)]
#[serde(tag = "type")]
enum Geometry {
    Polygon {
        coordinates: Vec<Vec<Vec<f64>>>,
    },
    MultiPolygon {
        coordinates: Vec<Vec<Vec<Vec<f64>>>>,
    },
}
#[derive(Serialize, Deserialize, Debug)]
struct StateProperties {
    #[serde(rename = "NAME")]
    name: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct CitiesProperties {
    #[serde(rename = "NAME")]
    name: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct CountiesProperties {
    #[serde(rename = "NAME")]
    name: String,
}

pub fn parse_all_data() -> (Location, Location, Location) {
    let (state, cities, counties) = parse_geo_data_files();

    (
        geo_to_edges::<StateProperties>(&state),
        geo_to_edges::<CitiesProperties>(&cities),
        geo_to_edges::<CountiesProperties>(&counties),
    )
}

fn geo_to_edges<T: HasName>(geo: &GeoData<T>) -> Location {
    geo.features
        .iter()
        .map(|f| {
            let name = f.properties.get_name();
            let edges = match &f.geometry {
                Geometry::Polygon { coordinates } => vec![handle_polygon(coordinates)],
                Geometry::MultiPolygon { coordinates } => {
                    coordinates.iter().map(|p| handle_polygon(p)).collect()
                }
            };
            Jurisdiction { name, edges }
        })
        .collect()
}

fn handle_polygon(poly: &[Vec<Vec<f64>>]) -> Vec<Edge> {
    let mut edges = vec![];
    for ring in poly {
        for i in 0..ring.len() {
            let p1 = &ring[i];
            let p2 = &ring[(i + 1) % ring.len()];
            edges.push(Edge::new((p1[0], p1[1]), (p2[0], p2[1])))
        }
    }
    edges
}

trait HasName {
    fn get_name(&self) -> String;
}

impl HasName for StateProperties {
    fn get_name(&self) -> String {
        self.name.clone()
    }
}

impl HasName for CitiesProperties {
    fn get_name(&self) -> String {
        self.name.clone()
    }
}

impl HasName for CountiesProperties {
    fn get_name(&self) -> String {
        self.name.clone()
    }
}