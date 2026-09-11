-- =====================================================================
-- NovaHome International Expansion Strategy 2026
-- Relational Database Schema (SQLite / ANSI-SQL Compatible)
-- Document ID: NH-SQL-2026-001
-- =====================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- Table 1: markets
-- Dimension table storing candidate and benchmark countries
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS pricing;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS competitors;
DROP TABLE IF EXISTS market_metrics;
DROP TABLE IF EXISTS markets;

CREATE TABLE markets (
    market_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL UNIQUE,
    region TEXT NOT NULL,
    currency TEXT NOT NULL,
    is_domestic_benchmark BOOLEAN NOT NULL DEFAULT 0 CHECK(is_domestic_benchmark IN (0, 1))
);

-- ---------------------------------------------------------------------
-- Table 2: market_metrics
-- Fact table tracking verified macroeconomic, category, and cost metrics
-- ---------------------------------------------------------------------
CREATE TABLE market_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_id INTEGER NOT NULL UNIQUE,
    population_m REAL NOT NULL CHECK(population_m > 0),
    urban_population_pct REAL NOT NULL CHECK(urban_population_pct BETWEEN 0.0 AND 100.0),
    disposable_income_usd REAL NOT NULL CHECK(disposable_income_usd > 0),
    fitness_participation_pct REAL NOT NULL CHECK(fitness_participation_pct BETWEEN 0.0 AND 100.0),
    ecommerce_penetration_pct REAL NOT NULL CHECK(ecommerce_penetration_pct BETWEEN 0.0 AND 100.0),
    home_fitness_demand_index REAL NOT NULL CHECK(home_fitness_demand_index BETWEEN 0.0 AND 100.0),
    market_growth_cagr_pct REAL NOT NULL,
    avg_selling_price_usd REAL NOT NULL CHECK(avg_selling_price_usd > 0),
    import_logistics_cost_usd REAL NOT NULL CHECK(import_logistics_cost_usd >= 0),
    competitor_intensity_score REAL NOT NULL CHECK(competitor_intensity_score BETWEEN 1.0 AND 5.0),
    regulatory_complexity_score REAL NOT NULL CHECK(regulatory_complexity_score BETWEEN 1.0 AND 5.0),
    digital_ad_cost_index REAL NOT NULL CHECK(digital_ad_cost_index > 0),
    sam_usd_m REAL NOT NULL CHECK(sam_usd_m > 0),
    data_status TEXT NOT NULL CHECK(data_status IN ('verified', 'estimated', 'proxy', 'synthetic_assumption')),
    FOREIGN KEY (market_id) REFERENCES markets(market_id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------
-- Table 3: competitors
-- Dimension table tracking industry competitors and their strategic tier
-- ---------------------------------------------------------------------
CREATE TABLE competitors (
    competitor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitor_name TEXT NOT NULL UNIQUE,
    headquarters_country TEXT NOT NULL,
    tier TEXT NOT NULL CHECK(tier IN ('Discount', 'Mid-Market', 'Luxury')),
    business_model TEXT NOT NULL CHECK(business_model IN ('Connected D2C', 'Traditional Retail', 'Hybrid Hardware+Software'))
);

-- ---------------------------------------------------------------------
-- Table 4: products
-- Dimension table tracking hardware products across categories
-- ---------------------------------------------------------------------
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitor_id INTEGER,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('Spin Bike', 'Rower', 'Strength Station', 'Treadmill')),
    has_connected_screen BOOLEAN NOT NULL DEFAULT 0 CHECK(has_connected_screen IN (0, 1)),
    weight_kg REAL NOT NULL CHECK(weight_kg > 0),
    FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id) ON DELETE SET NULL
);

-- ---------------------------------------------------------------------
-- Table 5: pricing
-- Fact table tracking localized product pricing and channel economics
-- ---------------------------------------------------------------------
CREATE TABLE pricing (
    pricing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    market_id INTEGER NOT NULL,
    local_price REAL NOT NULL CHECK(local_price > 0),
    price_usd REAL NOT NULL CHECK(price_usd > 0),
    subscription_monthly_usd REAL NOT NULL DEFAULT 0.0 CHECK(subscription_monthly_usd >= 0),
    distribution_channel TEXT NOT NULL CHECK(distribution_channel IN ('D2C Online', 'Retail Store', 'Hybrid Omnichannel')),
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
    FOREIGN KEY (market_id) REFERENCES markets(market_id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------
-- Helpful Indexes for Query Optimization
-- ---------------------------------------------------------------------
CREATE INDEX idx_metrics_market_id ON market_metrics(market_id);
CREATE INDEX idx_pricing_market_id ON pricing(market_id);
CREATE INDEX idx_pricing_product_id ON pricing(product_id);
CREATE INDEX idx_products_category ON products(category);
