# NovaHome Market Expansion: Data Dictionary

**Document ID:** `NH-DATA-2026-001`  
**Phase:** Phase 03 — Python Data Preparation & Exploratory Analysis  
**Author:** Senior Consulting Analyst & Lead Data Analyst  
**Date:** September 2026  

---

## 1. Overview & Purpose

This data dictionary defines the schema, operational business meaning, data types, measurement units, provenance, and data transformations applied to the NovaHome market research dataset. It serves as the single source of truth for both the raw dataset (`data/raw/market_research.csv`) and the cleaned analytical dataset (`data/processed/clean_market_research.csv`).

---

## 2. Schema Definition Table

| Column Name | Business Meaning | Data Type | Unit | Source or Assumption | Transformation Applied |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `country` | Name of candidate or domestic benchmark market. | `string` / `object` | Categorical | Official ISO/UN Country Name | Standardized to proper title case, stripped of leading/trailing whitespace. |
| `population_m` | Total resident population of the country. | `float64` | Millions (M) | World Bank Open Data (2024/2025) | Parsed as numeric float; rounded to 1 decimal place. |
| `urban_population_pct` | Percentage of total population living in metropolitan/urban agglomerations. | `float64` | Percentage (%) | World Bank Urban Indicator | Bounded strictly in range `[0.0, 100.0]`. |
| `disposable_income_usd` | Average annual net adjusted household disposable income per capita. | `float64` | USD ($) | OECD Better Life Index / US BEA / StatCan / IMF | Normalized to USD using standard 2025 annual average exchange rates. |
| `fitness_participation_pct` | Proportion of adult population engaging in structured sports or exercise $\ge 2\times/\text{week}$. | `float64` | Percentage (%) | EuropeActive / DSSV / AusPlay / IHRSA | Bounded in `[0.0, 100.0]`. |
| `ecommerce_penetration_pct` | Share of total retail commerce executed through online/digital checkout channels. | `float64` | Percentage (%) | UNCTAD Digital Economy / UK ONS / Statista | Bounded in `[0.0, 100.0]`. |
| `home_fitness_demand_index` | Normalized interest and search density for smart connected fitness equipment. | `float64` | Index (0–100) | Google Trends & Statista Consumer Survey Synthesis | Scaled to a standardized index where 100 represents peak interest. |
| `market_growth_cagr_pct` | Forecasted 3-year compound annual growth rate of home fitness equipment (2026–2029). | `float64` | Percentage (%) | Statista Worldwide Market Insights & Industry Reports | Stored as percentage points (e.g., 4.8 = 4.8%). |
| `avg_selling_price_usd` | Prevailing market average retail price for mid-tier smart cardio and strength machines. | `float64` | USD ($) | Competitor Catalog Benchmarking (Peloton, Technogym, Echelon) | Rounded to nearest integer USD. |
| `import_logistics_cost_usd` | Landed variable cost per unit (ocean freight + import duties + 3PL room-of-choice delivery). | `float64` | USD ($) | 3PL Rate Cards & Customs Schedules (TARIC / CBIC / UKGT) | Modeled per physical hardware unit delivered. |
| `competitor_intensity_score` | Level of rival entrenchment and market saturation (1 = fragmented, 5 = duopoly/saturated). | `float64` | Score (1.0–5.0) | Calibrated Synthetic Consulting Assumption | Standardized on a continuous 1.0 to 5.0 scale. |
| `regulatory_complexity_score` | Degree of regulatory friction, mandatory certifications, and data laws (1 = minimal, 5 = extreme). | `float64` | Score (1.0–5.0) | Calibrated Synthetic Consulting Assumption | Standardized on a continuous 1.0 to 5.0 scale. |
| `digital_ad_cost_index` | Relative cost of customer acquisition via digital media (indexed vs. US baseline = 100.0). | `float64` | Index (Base=100) | Wordstream / Meta Ads Regional CPM Benchmark Analysis | Indexed relative to United States ($215 blended CAC baseline). |
| `data_status` | Credibility classification indicating whether data is verified, estimated, proxy, or synthetic. | `string` / `category` | Categorical | Internal Research Governance | Verified against allowed set: `['verified', 'estimated', 'proxy', 'synthetic_assumption']`. |
| `is_domestic_benchmark` | Flag indicating whether country is a baseline North American operational market. | `bool` | Boolean (`True`/`False`) | Business Rule | Derived feature: `True` if country is US or Canada; `False` for international expansion candidates. |

---

## 3. Data Integrity & Validation Constraints

Every pipeline consuming this data must enforce the following validation assertions:
1. `population_m > 0`
2. `0 <= urban_population_pct <= 100`
3. `disposable_income_usd > 0`
4. `0 <= fitness_participation_pct <= 100`
5. `0 <= ecommerce_penetration_pct <= 100`
6. `0 <= home_fitness_demand_index <= 100`
7. `avg_selling_price_usd > 0`
8. `import_logistics_cost_usd >= 0`
9. `1.0 <= competitor_intensity_score <= 5.0`
10. `1.0 <= regulatory_complexity_score <= 5.0`
11. `digital_ad_cost_index > 0`
12. `country` must be unique (zero duplicate records permitted).
