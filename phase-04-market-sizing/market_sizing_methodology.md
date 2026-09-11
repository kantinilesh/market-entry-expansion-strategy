# NovaHome International Expansion: Market Sizing Methodology & Attractiveness Scoring

**Document ID:** `NH-SIZING-2026-001`  
**Phase:** Phase 04 — Market Sizing & Attractiveness Scoring  
**Author:** Senior Consulting Analyst  
**Date:** September 2026  

---

## 1. Executive Summary & Sizing Architecture

A cornerstone of management consulting engagements (Bain, McKinsey, BCG) is establishing defensible, transparent, and triangulated market sizing.

Market sizing answers a critical executive question:
> *"Is the revenue prize in a candidate country large enough to justify the capital, logistics, and organizational bandwidth required to enter?"*

To avoid single-model bias, this project employs **two complementary sizing methodologies**:
1. **Top-Down Sizing (Macro-to-Micro Filtering)**: Starts with the broad fitness equipment market and filters down to NovaHome’s addressable price band and market share potential.
2. **Bottom-Up Sizing (Unit Economics / Customer Capacity)**: Starts with the count of addressable target households, annual hardware replacement frequency, and average order value (AOV).

---

## 2. Core Sizing Definitions

```
┌────────────────────────────────────────────────────────────────────────┐
│ TOTAL ADDRESSABLE MARKET (TAM)                                          │
│ Total global or national spend on all home fitness equipment.          │
│                                                                        │
│      ┌──────────────────────────────────────────────────────────┐      │
│      │ SERVICEABLE ADDRESSABLE MARKET (SAM)                     │      │
│      │ The portion of TAM within NovaHome's mid-market          │      │
│      │ connected fitness product and price segment ($600-$1,200).│      │
│      │                                                          │      │
│      │      ┌────────────────────────────────────────────┐      │      │
│      │      │ SERVICEABLE OBTAINABLE MARKET (SOM)        │      │      │
│      │      │ The realistic revenue NovaHome can capture │      │      │
│      │      │ within 3 years given competition & channels│      │      │
│      │      └────────────────────────────────────────────┘      │      │
│      └──────────────────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Total Addressable Market (TAM)**:
   * The total annual market demand for all home fitness equipment (treadmills, exercise bikes, rowers, free weights, ellipticals) across all price tiers ($100 discount to $4,000+ luxury).
2. **Serviceable Addressable Market (SAM)**:
   * The specific segment of TAM that directly matches NovaHome’s product category and value proposition: **connected smart cardio & digital resistance hardware ($600–$1,200 MSRP)** purchased by urban/suburban households with sufficient purchasing power.
3. **Serviceable Obtainable Market (SOM)**:
   * The realistic, defensible market share of SAM that NovaHome can win within **3 years (by Year-End 2028/2029)**, given marketing budget constraints, competitive resistance, and logistics capacity.
4. **Market Share**:
   * The percentage of the addressable category volume or revenue controlled by a company:
     $$\text{Market Share} = \frac{\text{NovaHome Annual Revenue}}{\text{Total Segment Market Size (SAM)}} \times 100$$
5. **Compound Annual Growth Rate (CAGR)**:
   * The annualized smoothed growth rate of market spend:
     $$\text{CAGR} = \left( \frac{\text{Value}_{2029}}{\text{Value}_{2026}} \right)^{\frac{1}{3}} - 1$$

---

## 3. Mathematical Sizing Formulations

### Method A: Top-Down Market Sizing
Top-down sizing leverages audited national industry reports and applies sequential eligibility filters:

$$\text{TAM} = \text{Total National Retail Spend on Home Fitness Equipment}$$

$$\text{SAM} = \text{TAM} \times S_{\text{connected}} \times E_{\text{price}} \times U_{\text{urban}}$$
Where:
* $S_{\text{connected}}$ = Segment share of connected/smart equipment (assumed 35%–45% based on country digital maturity).
* $E_{\text{price}}$ = Proportion of buyers within the mid-market price tier ($600–$1,200) vs. budget or luxury (assumed 40%–50%).
* $U_{\text{urban}}$ = Urban population access adjustment factor.

$$\text{SOM} = \text{SAM} \times \text{Achievable Market Share } (MS_{\text{target}})$$
Where:
* $MS_{\text{target}}$ = Realistic 3-year market share (calibrated at 2.0%–5.0% depending on competitive concentration).

---

### Method B: Bottom-Up Market Sizing
Bottom-up sizing models the fundamental customer economics from demographic census data:

$$\text{Addressable Target Households} = \text{Total Households} \times \text{Urban } \% \times \text{Income Eligibility } \% \times \text{Fitness Participation } \%$$

$$\text{Annual Category Hardware Units} = \text{Target Households} \times \text{Annual Hardware Purchase Rate } (\alpha)$$
Where:
* Total Households $\approx \frac{\text{Population}}{\text{Average Household Size (2.3–2.6)}}$.
* $\alpha$ = Annual replacement/new adoption frequency for heavy fitness equipment (typically 8.0%–12.0% annually, reflecting an 8-to-10-year product lifespan).

$$\text{Bottom-Up SAM} = \text{Annual Category Hardware Units} \times \text{Average Selling Price (ASP)}$$

$$\text{Bottom-Up SOM} = \text{Bottom-Up SAM} \times \text{Achievable Market Share } (MS_{\text{target}})$$

---

## 4. Attractiveness Scoring Framework (1.0 to 5.0 Scale)

To evaluate candidate countries holistically beyond raw market size, we apply a multi-factor scoring rubric across six core market dimensions:

| Dimension | Metric / Indicator | Evaluation Direction | Normalization Method & Strategic Logic |
| :--- | :--- | :--- | :--- |
| **1. Market Size** | Serviceable Addressable Market (SAM in $M) | **Higher is Better** | Min-max scaled on log base to prevent mega-markets from skewing scores. |
| **2. Growth** | 3-Year Forecasted Category CAGR (%) | **Higher is Better** | Scaled against 4.5% hurdle: $<3.0\% = 1.0$; $4.5\% = 3.0$; $>8.0\% = 5.0$. |
| **3. Demand** | Home Fitness Demand Index (0–100) | **Higher is Better** | Linear scaling: Score $= 1.0 + 4.0 \times \left( \frac{\text{Index} - 50}{50} \right)$. |
| **4. Competition** | Competitor Intensity Score (1.0–5.0) | **LOWER is Better (Inverted)** | Inverted score: $\text{Score} = 6.0 - \text{Raw Intensity}$. Low competition = higher attractiveness. |
| **5. Pricing** | Average Selling Price / Income Ratio | **Higher is Better** | Evaluates consumer ability to sustain $900+ hardware and $19.99/mo app. |
| **6. Regulatory** | Regulatory & Trade Complexity (1.0–5.0) | **LOWER is Better (Inverted)** | Inverted score: $\text{Score} = 6.0 - \text{Raw Complexity}$. Low friction = higher attractiveness. |

### Proposed Market Attractiveness Pillar Weights (Assumption)
Within the Market Attractiveness Pillar (which itself constitutes 35% of the macro investment decision), the sub-weights are distributed as:
* **Market Size (SAM)**: **25%**
* **Market Growth (CAGR)**: **20%**
* **Customer Demand**: **20%**
* **Competitive Whitespace**: **15%**
* **Pricing & Income Capacity**: **10%**
* **Regulatory Ease**: **10%**
* **Total**: **100%**

---

## 5. Data Sources & Provenance

* **Macro Population & Urbanization**: World Bank Open Data (`SRC-001`, `SRC-002`).
* **Household Income**: OECD Better Life Index & US Bureau of Economic Analysis (`SRC-003`, `SRC-007`).
* **Fitness Participation**: EuropeActive European Health & Fitness Market Report & AusPlay (`SRC-004`, `SRC-010`).
* **Category Revenue & Growth**: Statista Worldwide Fitness Equipment Market Insights (`SRC-006`).
* **Landed Import Duties & Logistics**: National Customs Schedules (EU TARIC, UK Global Tariff, Indian CBIC `SRC-013`).

---

## 6. Sizing Limitations & Methodological Caveats

1. **Exchange Rate Volatility**: Sizing is denominated in USD. Substantial fluctuations in GBP, EUR, AUD, or JPY will adjust real purchasing power.
2. **Post-COVID Normalization**: Home fitness experienced pull-forward demand in 2020–2022; current projections assume normalized 8-to-10-year replacement cycles.
3. **App Subscription Revenues**: This model isolates upfront **hardware equipment sales**. Recurring software subscription revenue ($19.99/month) is modeled separately in Phase 06 (Unit Economics).
