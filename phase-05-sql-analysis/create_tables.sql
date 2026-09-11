-- =====================================================================
-- NovaHome International Expansion Strategy 2026
-- Database Initialization & Seed Data (create_tables.sql)
-- =====================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- 1. Create Schema Tables
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

CREATE TABLE competitors (
    competitor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitor_name TEXT NOT NULL UNIQUE,
    headquarters_country TEXT NOT NULL,
    tier TEXT NOT NULL CHECK(tier IN ('Discount', 'Mid-Market', 'Luxury')),
    business_model TEXT NOT NULL CHECK(business_model IN ('Connected D2C', 'Traditional Retail', 'Hybrid Hardware+Software'))
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitor_id INTEGER,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('Spin Bike', 'Rower', 'Strength Station', 'Treadmill')),
    has_connected_screen BOOLEAN NOT NULL DEFAULT 0 CHECK(has_connected_screen IN (0, 1)),
    weight_kg REAL NOT NULL CHECK(weight_kg > 0),
    FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id) ON DELETE SET NULL
);

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
-- 2. Populate 'markets'
-- ---------------------------------------------------------------------
INSERT INTO markets (market_id, country, region, currency, is_domestic_benchmark) VALUES
(1, 'United States', 'North America', 'USD', 1),
(2, 'Canada', 'North America', 'CAD', 1),
(3, 'United Kingdom', 'Western Europe', 'GBP', 0),
(4, 'Germany', 'Western Europe', 'EUR', 0),
(5, 'Netherlands', 'Western Europe', 'EUR', 0),
(6, 'Australia', 'Asia-Pacific', 'AUD', 0),
(7, 'Singapore', 'Asia-Pacific', 'SGD', 0),
(8, 'United Arab Emirates', 'Middle East', 'AED', 0),
(9, 'Saudi Arabia', 'Middle East', 'SAR', 0),
(10, 'India', 'Asia-Pacific', 'INR', 0);

-- ---------------------------------------------------------------------
-- 3. Populate 'market_metrics' (Grounded in clean_market_research.csv)
-- ---------------------------------------------------------------------
INSERT INTO market_metrics (
    market_id, population_m, urban_population_pct, disposable_income_usd,
    fitness_participation_pct, ecommerce_penetration_pct, home_fitness_demand_index,
    market_growth_cagr_pct, avg_selling_price_usd, import_logistics_cost_usd,
    competitor_intensity_score, regulatory_complexity_score, digital_ad_cost_index,
    sam_usd_m, data_status
) VALUES
(1, 336.5, 83.2, 54800, 38.5, 16.2, 88.0, 3.8, 950, 115, 4.8, 1.5, 100.0, 1680.0, 'verified'),
(2, 40.5, 81.8, 42600, 34.0, 14.5, 76.0, 4.1, 920, 140, 4.2, 1.8, 84.0, 164.0, 'verified'),
(3, 68.2, 84.5, 38400, 31.5, 26.5, 82.0, 4.8, 910, 165, 4.1, 2.5, 78.0, 260.0, 'verified'),
(4, 84.4, 77.8, 41200, 29.0, 18.4, 79.0, 5.2, 960, 155, 3.6, 3.2, 72.0, 312.0, 'verified'),
(5, 18.0, 92.8, 43500, 36.0, 21.2, 74.0, 5.0, 940, 125, 2.9, 2.1, 65.0, 64.0, 'verified'),
(6, 26.8, 86.6, 44100, 41.0, 17.5, 78.0, 5.6, 1020, 195, 3.4, 2.4, 82.0, 112.0, 'verified'),
(7, 6.0, 100.0, 42800, 32.0, 19.8, 62.0, 6.2, 1050, 110, 2.7, 2.0, 58.0, 26.0, 'verified'),
(8, 9.5, 87.5, 39200, 27.5, 18.0, 71.0, 7.8, 1100, 175, 2.8, 2.8, 62.0, 38.0, 'estimated'),
(9, 36.9, 84.7, 26500, 21.0, 15.2, 68.0, 8.5, 1080, 210, 2.5, 4.1, 54.0, 72.0, 'estimated'),
(10, 1440.0, 36.4, 3200, 9.5, 8.5, 55.0, 12.5, 680, 280, 3.8, 4.6, 28.0, 124.0, 'proxy');

-- ---------------------------------------------------------------------
-- 4. Populate 'competitors'
-- ---------------------------------------------------------------------
INSERT INTO competitors (competitor_id, competitor_name, headquarters_country, tier, business_model) VALUES
(1, 'Peloton', 'United States', 'Luxury', 'Connected D2C'),
(2, 'NordicTrack (iFit)', 'United States', 'Luxury', 'Hybrid Hardware+Software'),
(3, 'Technogym', 'Italy', 'Luxury', 'Hybrid Hardware+Software'),
(4, 'Echelon Fitness', 'United States', 'Mid-Market', 'Connected D2C'),
(5, 'Wattbike', 'United Kingdom', 'Luxury', 'Connected D2C'),
(6, 'NOHrD / WaterRower', 'Germany', 'Luxury', 'Traditional Retail'),
(7, 'Decathlon (Domyos)', 'France', 'Discount', 'Traditional Retail'),
(8, 'Sunny Health & Fitness', 'United States', 'Discount', 'Traditional Retail'),
(9, 'Cult.fit', 'India', 'Discount', 'Hybrid Hardware+Software'),
(10, 'NovaHome (Benchmark)', 'United States', 'Mid-Market', 'Connected D2C');

-- ---------------------------------------------------------------------
-- 5. Populate 'products'
-- ---------------------------------------------------------------------
INSERT INTO products (product_id, competitor_id, product_name, category, has_connected_screen, weight_kg) VALUES
(1, 1, 'Peloton Bike+', 'Spin Bike', 1, 63.0),
(2, 1, 'Peloton Tread', 'Treadmill', 1, 131.0),
(3, 2, 'NordicTrack Commercial S22i', 'Spin Bike', 1, 93.0),
(4, 2, 'NordicTrack RW900 Rower', 'Rower', 1, 60.0),
(5, 3, 'Technogym Ride', 'Spin Bike', 1, 67.0),
(6, 4, 'Echelon Smart Connect EX-5', 'Spin Bike', 0, 48.0),
(7, 4, 'Echelon Row Smart Rower', 'Rower', 0, 45.0),
(8, 5, 'Wattbike Atom V2', 'Spin Bike', 0, 44.0),
(9, 6, 'WaterRower Club Ash', 'Rower', 0, 31.0),
(10, 7, 'Domyos Basic Exercise Bike 100', 'Spin Bike', 0, 29.0),
(11, 7, 'Domyos Wood Rower 500', 'Rower', 0, 38.0),
(12, 8, 'Sunny Health Belt Drive Pro Bike', 'Spin Bike', 0, 40.0),
(13, 9, 'Cult.fit Transform Smart Bike', 'Spin Bike', 0, 35.0),
(14, 10, 'NovaPulse Smart Spin Bike', 'Spin Bike', 1, 46.0),
(15, 10, 'NovaGlide Water Rower', 'Rower', 1, 41.0),
(16, 10, 'NovaFlex Digital Strength Station', 'Strength Station', 1, 38.0);

-- ---------------------------------------------------------------------
-- 6. Populate 'pricing' (Localized Pricing & Distribution Channels)
-- ---------------------------------------------------------------------
INSERT INTO pricing (product_id, market_id, local_price, price_usd, subscription_monthly_usd, distribution_channel) VALUES
-- US Pricing (Market 1)
(1, 1, 2495.0, 2495.0, 44.0, 'D2C Online'),
(3, 1, 1999.0, 1999.0, 39.0, 'Hybrid Omnichannel'),
(6, 1, 999.0, 999.0, 34.99, 'D2C Online'),
(10, 1, 299.0, 299.0, 0.0, 'Retail Store'),
(14, 1, 899.0, 899.0, 19.99, 'D2C Online'),
(15, 1, 1099.0, 1099.0, 19.99, 'D2C Online'),
(16, 1, 1299.0, 1299.0, 19.99, 'D2C Online'),

-- Canada Pricing (Market 2)
(1, 2, 3395.0, 2515.0, 55.0, 'D2C Online'),
(3, 2, 2699.0, 1999.0, 49.0, 'Hybrid Omnichannel'),
(6, 2, 1349.0, 999.0, 45.0, 'D2C Online'),
(14, 2, 1249.0, 925.0, 26.99, 'D2C Online'),

-- UK Pricing (Market 3)
(1, 3, 1995.0, 2530.0, 39.0, 'D2C Online'),
(6, 3, 799.0, 1015.0, 29.99, 'D2C Online'),
(8, 3, 1999.0, 2538.0, 15.0, 'D2C Online'),
(10, 3, 249.0, 316.0, 0.0, 'Retail Store'),
(14, 3, 749.0, 951.0, 16.99, 'D2C Online'),
(15, 3, 899.0, 1141.0, 16.99, 'D2C Online'),

-- Germany Pricing (Market 4)
(1, 4, 2495.0, 2720.0, 39.0, 'D2C Online'),
(3, 4, 2199.0, 2397.0, 39.0, 'Hybrid Omnichannel'),
(6, 4, 999.0, 1089.0, 34.99, 'D2C Online'),
(9, 4, 1299.0, 1416.0, 0.0, 'Retail Store'),
(10, 4, 279.0, 304.0, 0.0, 'Retail Store'),
(14, 4, 849.0, 925.0, 19.99, 'D2C Online'),

-- Netherlands Pricing (Market 5)
(1, 5, 2495.0, 2720.0, 39.0, 'D2C Online'),
(6, 5, 949.0, 1034.0, 34.99, 'D2C Online'),
(10, 5, 269.0, 293.0, 0.0, 'Retail Store'),
(14, 5, 829.0, 903.0, 19.99, 'D2C Online'),

-- Australia Pricing (Market 6)
(1, 6, 3445.0, 2308.0, 59.0, 'D2C Online'),
(3, 6, 2999.0, 2009.0, 55.0, 'Hybrid Omnichannel'),
(6, 6, 1499.0, 1004.0, 49.0, 'D2C Online'),
(14, 6, 1399.0, 937.0, 29.99, 'D2C Online'),

-- Singapore Pricing (Market 7)
(1, 7, 3650.0, 2740.0, 55.0, 'D2C Online'),
(6, 7, 1450.0, 1090.0, 45.0, 'Hybrid Omnichannel'),
(14, 7, 1299.0, 977.0, 26.99, 'D2C Online'),

-- UAE Pricing (Market 8)
(1, 8, 9995.0, 2720.0, 160.0, 'D2C Online'),
(5, 8, 16500.0, 4490.0, 0.0, 'Retail Store'),
(6, 8, 3999.0, 1088.0, 125.0, 'Hybrid Omnichannel'),
(14, 8, 3499.0, 952.0, 75.0, 'D2C Online'),

-- Saudi Arabia Pricing (Market 9)
(1, 9, 10500.0, 2800.0, 165.0, 'D2C Online'),
(6, 9, 4200.0, 1120.0, 130.0, 'Retail Store'),
(14, 9, 3699.0, 986.0, 75.0, 'D2C Online'),

-- India Pricing (Market 10)
(10, 10, 18999.0, 228.0, 0.0, 'Retail Store'),
(13, 10, 24999.0, 300.0, 12.0, 'Hybrid Omnichannel'),
(14, 10, 89999.0, 1080.0, 20.0, 'D2C Online');
