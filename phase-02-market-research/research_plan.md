# NovaHome International Expansion: Secondary Market Research Plan

**Document ID:** `NH-RESRCH-2026-001`  
**Phase:** Phase 02 — Secondary Market Research & Intelligence  
**Author:** Senior Consulting Analyst  
**Date:** September 2026  

---

## 1. Research Objectives & Core Questions

The objective of Phase 02 is to construct a rigorous, comparable, and methodologically transparent factual foundation across **10 candidate markets** (including domestic benchmark markets) to evaluate NovaHome's 2026 international expansion.

### Core Research Questions
1. **Macroeconomic Capacity**: Which candidate markets possess sufficient consumer purchasing power and urbanization to support high-ticket connected fitness equipment ($800–$1,300 price points)?
2. **Category Momentum**: Where is digital and home fitness demand expanding, and what are the structural demand drivers (e.g., climate, fitness club density, disposable income)?
3. **Competitive Pressure**: Which markets are dominated by entrenched luxury or discount incumbents, and where does genuine mid-market whitespace exist?
4. **Frictional Costs & Regulatory Barriers**: What are the landed freight, tariff, digital marketing (CAC), and electrical/compliance costs across each market?

---

## 2. Candidate Market Universe

The candidate pool spans 10 countries across North America, Europe, the Middle East, and Asia-Pacific:
* **Domestic Benchmarks**: United States (US), Canada (CA) — *used to anchor baseline performance and comparative metrics*.
* **Western Europe**: United Kingdom (UK), Germany (DE), Netherlands (NL).
* **Asia-Pacific**: Australia (AU), Singapore (SG), India (IN).
* **Middle East**: United Arab Emirates (UAE), Saudi Arabia (KSA).

> [!NOTE]
> Inclusion in the research universe does **not** imply selection. Several markets are evaluated specifically to test disqualification rules and stress-test the MECE issue tree.

---

## 3. Required Research Indicators & Definitions

| # | Indicator Name | Unit | Type | Definition & Measurement Standard |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **Population** | Millions | Macro | Total resident population (2025/2026 est.). |
| 2 | **Urban Population %** | Percentage (%) | Demographic | Proportion of population residing in urban agglomerations. |
| 3 | **Disposable Income Proxy** | USD / Capita / Yr | Economic | Net adjusted annual disposable income per capita. |
| 4 | **Fitness Participation Proxy** | Percentage (%) | Cultural | % of adult population engaging in structured physical exercise $\ge 2\times/\text{week}$. |
| 5 | **E-Commerce Penetration** | Percentage (%) | Commercial | % of retail transactions conducted via digital/e-commerce channels. |
| 6 | **Home Fitness Demand Proxy** | Index (0–100) | Category | Composite search volume & survey index for home workout equipment. |
| 7 | **Market Growth Estimate** | CAGR (%) | Momentum | 3-year projected compound annual growth rate of home fitness equipment (2026–2029). |
| 8 | **Average Selling Price (ASP)** | USD / Unit | Commercial | Prevailing average retail price for mid-tier cardio equipment in-market. |
| 9 | **Import & Logistics Cost Proxy** | USD / Unit | Cost | Estimated landed inbound freight, import tariffs, and last-mile two-person bulky delivery. |
| 10 | **Competitor Intensity** | Index (1–5) | Competitive | 1 = Highly fragmented / Low competition; 5 = Saturated / Dominated by major incumbents. |
| 11 | **Regulatory Complexity** | Index (1–5) | Legal | 1 = Standard mutual recognition; 5 = Heavy local testing, labeling, and data localization. |
| 12 | **Digital Ad Cost Proxy (CAC)** | USD (CPM/CAC index) | Marketing | Relative cost to acquire customer via digital media (indexed vs. US baseline = 100). |

---

## 4. Preferred Source Hierarchy & Quality Rules

To preserve data integrity, research adheres to a strict 4-tier credibility hierarchy:

```
Tier 1: Multilateral Institutions & National Statistical Bureaus (Gold Standard)
        [World Bank, IMF, OECD, Eurostat, US Census Bureau, UK ONS]
                             │
                             ▼
Tier 2: Audited Financial Disclosures & Public Equity Filings
        [Peloton 10-K, Technogym Annual Reports, Basic-Fit SEC filings]
                             │
                             ▼
Tier 3: Specialized Industry Analytics & Intelligence Platforms
        [Statista Mobility & Consumer Markets, EuropeActive European Health & Fitness Reports, IHRSA]
                             │
                             ▼
Tier 4: Synthetic Modeling & Calibrated Assumptions
        [Clearly labeled internal proxies where empirical country-level data is unavailable]
```

### Source Quality Rules
1. **Rule of Verification**: Never cite unverified blogs, anonymous forums, or AI-hallucinated citations. Every public source must have an authentic domain and organization.
2. **Rule of Recency**: All economic and demographic indicators must be dated between 2023 and 2026.
3. **Rule of Explicit Labeling**: Every data point must be classified under one of four statuses:
   * `verified`: Sourced directly from published public statistical bodies or audited reports.
   * `estimated`: Derived via standard economic interpolations from official source data.
   * `proxy`: A related indicator used to represent a metric that cannot be directly measured.
   * `synthetic_assumption`: Calibrated parameter created for modeling where empirical data is absent.

---

## 5. Data Limitations & Comparability Challenges

1. **Purchasing Power Parity (PPP) vs. Nominal USD**: Disposable income varies greatly across nominal exchange rates. High nominal GDP does not always equal high willingness to spend on imported fitness hardware.
2. **Bulky Freight Rate Volatility**: Ocean freight container rates (Drewry / SCFI) fluctuate seasonally. Freight proxies reflect normalized 2025/2026 baseline contracts.
3. **Cultural Definition of "Fitness Participation"**: Southern European and Asian physical activity surveys often include casual walking, whereas Nordic and Anglo-Saxon metrics focus on gym/cardio workouts. We standardize on *structured fitness activity*.
4. **Non-Tariff Regulatory Barriers**: Technical standards (e.g., electrical plug compliance, CE marking, Saudi SASO, India BIS certification) create hidden operational friction that cannot be captured by import duty percentages alone.

---

## 6. Research Completion Checklist

- [x] Define research scope and candidate countries (10 markets).
- [x] Standardize metric definitions, units, and measurement criteria.
- [x] Audit authentic institutional sources and catalog in `source_register.csv`.
- [x] Compile raw standardized dataset in `data/raw/market_research.csv` with explicit `data_status` column.
- [x] Write qualitative strategic dossier for each country in `market_research_notes.md`.
- [x] Perform automated data hygiene validation (no missing cells, consistent units, valid percentages).
