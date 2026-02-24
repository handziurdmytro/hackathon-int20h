pub type Point = (f64, f64);
pub type Polygon = Vec<Edge>;

#[derive(Debug, Clone, Copy)]
pub struct Edge {
    pub p1: Point,
    pub p2: Point,
}

impl Edge {
    pub fn new(p1: Point, p2: Point) -> Self {
        Self { p1, p2 }
    }
}

pub fn is_in_polygon(point: Point, polygon: &[Edge]) -> bool {
    let mut toggle = false;
    let (x0, y0) = point;

    for edge in polygon {
        let (x1, y1) = edge.p1;
        let (x2, y2) = edge.p2;

        if is_point_on_edge(x0, y0, x1, y1, x2, y2) {
            return true;
        }

        if (y0 < y1) != (y0 < y2) {
            if x0 < (y0 - y1) * (x2 - x1) / (y2 - y1) + x1 {
                toggle = !toggle;
            }
        }
    }
    toggle
}

fn is_point_on_edge(x0: f64, y0: f64, x1: f64, y1: f64, x2: f64, y2: f64) -> bool {
    let cross = (x2 - x1) * (y0 - y1) - (y2 - y1) * (x0 - x1);

    if cross.abs() > f64::EPSILON {
        false
    } else {
        (x0 >= x1.min(x2) && x0 <= x1.max(x2)) && (y0 >= y1.min(y2) && y0 <= y1.max(y2))
    }
}

#[cfg(test)]
mod tests{
    use super::*;

    fn square_polygon() -> Polygon{
        vec![
            Edge::new((10.0, 10.0), (10.0, -10.0)),
            Edge::new((10.0, -10.0), (-10.0, -10.0)),
            Edge::new((-10.0, -10.0), (-10.0, 10.0)),
            Edge::new((-10.0, 10.0), (10.0, 10.0))
        ]
    }
    #[test]
    fn test_point_inside_square(){
        let polygon = square_polygon();

        assert!(is_in_polygon((0.0, 0.0), &polygon));

        assert!(!is_in_polygon((-10.1, 0.0), &polygon));
        assert!(!is_in_polygon((10.1, 0.0), &polygon));
        assert!(!is_in_polygon((0.0, 10.1), &polygon));
        assert!(!is_in_polygon((0.0, -10.1), &polygon));

        assert!(!is_in_polygon((10.1, 10.1), &polygon));
        assert!(!is_in_polygon((10.1, -10.1), &polygon));
        assert!(!is_in_polygon((-10.1, 10.1), &polygon));
        assert!(!is_in_polygon((-10.1, -10.1), &polygon));

        assert!(is_in_polygon((9.9, 9.9), &polygon));
        assert!(is_in_polygon((-9.9, 9.9), &polygon));
        assert!(is_in_polygon((9.9, -9.9), &polygon));
        assert!(is_in_polygon((-9.9, -9.9), &polygon));
    }

    #[test]
    fn test_point_on_edge(){
        let polygon = square_polygon();

        assert!(is_in_polygon((10.0, 10.0), &polygon));
        assert!(is_in_polygon((10.0, -10.0), &polygon));
        assert!(is_in_polygon((-10.0, 10.0), &polygon));
        assert!(is_in_polygon((-10.0, -10.0), &polygon));

        assert!(is_in_polygon((10.0, 0.0), &polygon));
        assert!(is_in_polygon((0.0, 10.0), &polygon));
        assert!(is_in_polygon((-10.0, 0.0), &polygon));
        assert!(is_in_polygon((0.0, -10.0), &polygon));
    }
}