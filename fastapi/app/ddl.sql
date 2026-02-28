DROP TABLE IF EXISTS orders;

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    subtotal NUMERIC(15, 2) NOT NULL,
    order_timestamp TIMESTAMP(6) NOT NULL,

    composite_tax_rate NUMERIC(10, 7),
    tax_amount NUMERIC(15, 2),
    total_amount NUMERIC(15, 2),

    state_rate NUMERIC(10, 7),
    county_rate NUMERIC(10, 7),
    city_rate NUMERIC(10, 7),
    special_rates NUMERIC(10, 7),

    jurisdictions JSONB DEFAULT '[]',
    dbg_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_orders_timestamp
    ON orders(order_timestamp);

CREATE INDEX IF NOT EXISTS idx_orders_total
    ON orders(total_amount);
