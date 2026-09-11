-- =====================================================================
-- NovaHome International Expansion Strategy 2026
-- Strategic SQL Analysis & Competitor Benchmarking Suite
-- Document ID: NH-SQL-2026-002
-- Database: novahome_expansion.db (SQLite / ANSI-SQL)
-- =====================================================================

-- ---------------------------------------------------------------------
-- Query 01: Largest Addressable Markets (Ranked by SAM $M)
-- Business Purpose: Identify the largest addressable revenue prizes for NovaHome.
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    m.region,
    mm.sam_usd_m,
    mm.population_m,
    ROUND(mm.sam_usd_m / mm.population_m, 2) AS sam_per_capita_usd,
    RANK() OVER (ORDER BY mm.sam_usd_m DESC) AS market_size_rank
FROM markets m
JOIN market_metrics mm ON m.market_id = mm.market_id
WHERE m.is_domestic_benchmark = 0
ORDER BY mm.sam_usd_m DESC;

-- ---------------------------------------------------------------------
-- Query 02: Fastest-Growing Markets (Ranked by 3-Year CAGR %)
-- Business Purpose: Isolate high-momentum markets expanding faster than the 4.5% hurdle.
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    m.region,
    mm.market_growth_cagr_pct,
    CASE 
        WHEN mm.market_growth_cagr_pct >= 8.0 THEN 'High Momentum (>8%)'
        WHEN mm.market_growth_cagr_pct >= 4.5 THEN 'Moderate Momentum (4.5%-8%)'
        ELSE 'Slow Growth / Maturing (<4.5%)'
    END AS growth_classification,
    RANK() OVER (ORDER BY mm.market_growth_cagr_pct DESC) AS growth_rank
FROM markets m
JOIN market_metrics mm ON m.market_id = mm.market_id
ORDER BY mm.market_growth_cagr_pct DESC;

-- ---------------------------------------------------------------------
-- Query 03: Most Competitive Markets (Ranked by Competitor Intensity)
-- Business Purpose: Identify where incumbent saturation drives up ad costs (CAC).
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    mm.competitor_intensity_score,
    mm.digital_ad_cost_index,
    CASE 
        WHEN mm.competitor_intensity_score >= 4.0 THEN 'Saturated / Hyper-Competitive'
        WHEN mm.competitor_intensity_score >= 3.0 THEN 'Moderate Rivalry'
        ELSE 'Favorable Whitespace'
    END AS competitive_environment
FROM markets m
JOIN market_metrics mm ON m.market_id = mm.market_id
ORDER BY mm.competitor_intensity_score DESC;

-- ---------------------------------------------------------------------
-- Query 04: Average Competitor Price by Country
-- Business Purpose: Benchmark localized hardware willingness-to-pay.
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    COUNT(p.pricing_id) AS product_count,
    ROUND(AVG(p.price_usd), 2) AS avg_hardware_price_usd,
    ROUND(MIN(p.price_usd), 2) AS min_price_usd,
    ROUND(MAX(p.price_usd), 2) AS max_price_usd,
    ROUND(AVG(p.subscription_monthly_usd), 2) AS avg_monthly_subscription_usd
FROM markets m
JOIN pricing p ON m.market_id = p.market_id
JOIN products prod ON p.product_id = prod.product_id
JOIN competitors c ON prod.competitor_id = c.competitor_id
WHERE c.competitor_name != 'NovaHome (Benchmark)'
GROUP BY m.country
ORDER BY avg_hardware_price_usd DESC;

-- ---------------------------------------------------------------------
-- Query 05: Lowest Average Selling Price Markets
-- Business Purpose: Detect highly discounted markets where mid-market margins suffer.
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    ROUND(AVG(p.price_usd), 2) AS avg_competitor_price_usd,
    mm.disposable_income_usd
FROM markets m
JOIN pricing p ON m.market_id = p.market_id
JOIN market_metrics mm ON m.market_id = mm.market_id
GROUP BY m.country
ORDER BY avg_competitor_price_usd ASC
LIMIT 3;

-- ---------------------------------------------------------------------
-- Query 06: Highest Average Selling Price Markets
-- Business Purpose: Detect premium markets capable of absorbing higher shipping fees.
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    ROUND(AVG(p.price_usd), 2) AS avg_competitor_price_usd,
    mm.disposable_income_usd
FROM markets m
JOIN pricing p ON m.market_id = p.market_id
JOIN market_metrics mm ON m.market_id = mm.market_id
GROUP BY m.country
ORDER BY avg_competitor_price_usd DESC
LIMIT 3;

-- ---------------------------------------------------------------------
-- Query 07: Competitor Brand Count by Country
-- Business Purpose: Measure brand fragmentation vs. oligopolistic concentration.
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    COUNT(DISTINCT c.competitor_id) AS active_competitor_brands,
    GROUP_CONCAT(DISTINCT c.competitor_name) AS brand_list
FROM markets m
JOIN pricing p ON m.market_id = p.market_id
JOIN products prod ON p.product_id = prod.product_id
JOIN competitors c ON prod.competitor_id = c.competitor_id
WHERE c.competitor_name != 'NovaHome (Benchmark)'
GROUP BY m.country
ORDER BY active_competitor_brands DESC;

-- ---------------------------------------------------------------------
-- Query 08: Product Category Distribution Across Candidate Universe
-- Business Purpose: Identify category availability (Spin Bikes vs. Rowers vs. Strength).
-- ---------------------------------------------------------------------
SELECT 
    category,
    COUNT(product_id) AS total_products,
    ROUND(COUNT(product_id) * 100.0 / (SELECT COUNT(*) FROM products), 1) AS category_share_pct,
    ROUND(AVG(weight_kg), 1) AS avg_weight_kg
FROM products
GROUP BY category
ORDER BY total_products DESC;

-- ---------------------------------------------------------------------
-- Query 09: Market Opportunity Ranking (Combined Scale + Growth Index)
-- Business Purpose: Triangulate addressable SAM and growth velocity.
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    mm.sam_usd_m,
    mm.market_growth_cagr_pct,
    mm.home_fitness_demand_index,
    ROUND(mm.sam_usd_m * (1 + mm.market_growth_cagr_pct / 100.0) * (mm.home_fitness_demand_index / 100.0), 2) AS composite_opportunity_score,
    DENSE_RANK() OVER (
        ORDER BY mm.sam_usd_m * (1 + mm.market_growth_cagr_pct / 100.0) * (mm.home_fitness_demand_index / 100.0) DESC
    ) AS opportunity_rank
FROM markets m
JOIN market_metrics mm ON m.market_id = mm.market_id
WHERE m.is_domestic_benchmark = 0;

-- ---------------------------------------------------------------------
-- Query 10: Markets with High Demand and Low Competition (The Sweet Spot)
-- Business Purpose: Screen for markets where consumer demand is high but rivals are weak.
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    mm.home_fitness_demand_index,
    mm.competitor_intensity_score,
    mm.sam_usd_m
FROM markets m
JOIN market_metrics mm ON m.market_id = mm.market_id
WHERE mm.home_fitness_demand_index >= 70.0
  AND mm.competitor_intensity_score <= 3.5
  AND m.is_domestic_benchmark = 0
ORDER BY mm.home_fitness_demand_index DESC;

-- ---------------------------------------------------------------------
-- Query 11: Markets with High Landed Margin Potential
-- Business Purpose: Calculate the Spread between Retail ASP and Landed Logistics Cost.
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    mm.avg_selling_price_usd AS asp_usd,
    mm.import_logistics_cost_usd AS landed_logistics_usd,
    (mm.avg_selling_price_usd - mm.import_logistics_cost_usd) AS gross_spread_usd,
    ROUND((mm.avg_selling_price_usd - mm.import_logistics_cost_usd) * 100.0 / mm.avg_selling_price_usd, 1) AS logistics_adjusted_margin_pct
FROM markets m
JOIN market_metrics mm ON m.market_id = mm.market_id
ORDER BY logistics_adjusted_margin_pct DESC;

-- ---------------------------------------------------------------------
-- Query 12: High Logistics Friction Watchlist
-- Business Purpose: Flag markets where freight/tariffs exceed the $180/unit warning ceiling.
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    mm.import_logistics_cost_usd,
    mm.avg_selling_price_usd,
    ROUND(mm.import_logistics_cost_usd * 100.0 / mm.avg_selling_price_usd, 1) AS logistics_share_of_price_pct,
    CASE 
        WHEN mm.import_logistics_cost_usd >= 250 THEN 'Critical Cost Barrier (Disqualification Risk)'
        WHEN mm.import_logistics_cost_usd >= 180 THEN 'Elevated Freight / Margin Squeeze'
        ELSE 'Acceptable Inbound Cost'
    END AS logistics_risk_tier
FROM markets m
JOIN market_metrics mm ON m.market_id = mm.market_id
ORDER BY mm.import_logistics_cost_usd DESC;

-- ---------------------------------------------------------------------
-- Query 13: Country-Level Competitor Tier Concentration
-- Business Purpose: Profile market composition (Luxury vs. Mid-Market vs. Discount).
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    SUM(CASE WHEN c.tier = 'Luxury' THEN 1 ELSE 0 END) AS luxury_count,
    SUM(CASE WHEN c.tier = 'Mid-Market' THEN 1 ELSE 0 END) AS midmarket_count,
    SUM(CASE WHEN c.tier = 'Discount' THEN 1 ELSE 0 END) AS discount_count,
    COUNT(p.pricing_id) AS total_tracked_products
FROM markets m
JOIN pricing p ON m.market_id = p.market_id
JOIN products prod ON p.product_id = prod.product_id
JOIN competitors c ON prod.competitor_id = c.competitor_id
WHERE c.competitor_name != 'NovaHome (Benchmark)'
GROUP BY m.country
ORDER BY luxury_count DESC;

-- ---------------------------------------------------------------------
-- Query 14: Mid-Market Whitespace Analysis ($600 - $1,200 Price Band)
-- Business Purpose: Determine whether the $600-$1,200 tier is empty or crowded.
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    COUNT(CASE WHEN p.price_usd < 600 THEN 1 END) AS discount_sub_600_count,
    COUNT(CASE WHEN p.price_usd BETWEEN 600 AND 1200 THEN 1 END) AS mid_market_600_1200_count,
    COUNT(CASE WHEN p.price_usd > 1200 THEN 1 END) AS luxury_above_1200_count,
    CASE 
        WHEN COUNT(CASE WHEN p.price_usd BETWEEN 600 AND 1200 THEN 1 END) = 0 THEN 'Complete Whitespace (Unserved Mid-Tier)'
        WHEN COUNT(CASE WHEN p.price_usd BETWEEN 600 AND 1200 THEN 1 END) <= 1 THEN 'Open Whitespace (1 Competitor)'
        ELSE 'Competitive Mid-Tier (2+ Competitors)'
    END AS whitespace_status
FROM markets m
JOIN pricing p ON m.market_id = p.market_id
JOIN products prod ON p.product_id = prod.product_id
JOIN competitors c ON prod.competitor_id = c.competitor_id
WHERE c.competitor_name != 'NovaHome (Benchmark)'
GROUP BY m.country
ORDER BY mid_market_600_1200_count ASC;

-- ---------------------------------------------------------------------
-- Query 15: Strategic Candidate Screening Filter (Stage 1 Knockout + Growth)
-- Business Purpose: Multi-condition query identifying surviving priority markets.
-- Filters:
-- 1. Not a domestic benchmark (is_domestic_benchmark = 0)
-- 2. SAM >= $50M (KO-1: Scale floor)
-- 3. Logistics <= $200 (KO-2: Cost threshold)
-- 4. Regulatory complexity <= 3.5 (KO-4: Compliance feasibility)
-- 5. Market growth >= 4.5% (NovaHome growth hurdle)
-- ---------------------------------------------------------------------
SELECT 
    m.country,
    m.region,
    mm.sam_usd_m,
    mm.market_growth_cagr_pct,
    mm.import_logistics_cost_usd,
    mm.regulatory_complexity_score,
    mm.competitor_intensity_score,
    'QUALIFIED FOR UNIT ECONOMICS MODEL' AS recommendation_status
FROM markets m
JOIN market_metrics mm ON m.market_id = mm.market_id
WHERE m.is_domestic_benchmark = 0
  AND mm.sam_usd_m >= 50.0
  AND mm.import_logistics_cost_usd <= 200.0
  AND mm.regulatory_complexity_score <= 3.5
  AND mm.market_growth_cagr_pct >= 4.5
ORDER BY mm.sam_usd_m DESC;
