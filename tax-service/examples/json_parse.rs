use tax_service::geo::read_geo_json;

fn main() {
    let state = String::from("../data/geo/State.json");
    let cities = String::from("../data/geo/Cities.json");
    let counties = String::from("../data/geo/Counties.json");

    // read_geo_json(state).unwrap();
    read_geo_json(cities).unwrap();
    // read_geo_json(counties).unwrap();
}