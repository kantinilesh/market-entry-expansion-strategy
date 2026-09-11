# NovaHome International Expansion: Hypothesis Register

**Document ID:** `NH-STRAT-2026-003`  
**Methodology:** Hypothesis-Driven Consulting (Bain & Company standard)  
**Author:** Nilesh Kanti (Senior Consulting Analyst)  

---

## 1. Overview of Hypothesis-Driven Methodology

In strategy consulting, a **hypothesis** is not a blind guess; it is an informed, testable proposition regarding the root cause of a problem or the optimal solution. 

Instead of gathering data aimlessly ("boiling the ocean"), we formulate explicit hypotheses linked directly to the MECE Issue Tree branches. Each hypothesis possesses:
1. **Clear Statement**: A declarative assertion that can be proven true or false.
2. **Analysis Required**: The exact quantitative or qualitative work stream needed to test it.
3. **Primary Data Sources**: Verified external databases, benchmark reports, or model outputs.
4. **Falsification / Acceptance Threshold**: The unambiguous numerical or qualitative boundary that decides whether the hypothesis is supported or rejected.
5. **Status Tracker**: Current state (`Untested`, `Supported`, `Rejected`, `Refined`).

---

## 2. Master Hypothesis Register

| ID | Issue Tree Branch | Hypothesis Statement | Analytical Work Stream | Primary Data Sources | Pass / Fail Hurdle Threshold | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **H1.1** | 1.1 Market Sizing | The United Kingdom and Germany each represent addressable connected fitness markets (SAM) exceeding $150M with 3-year projected CAGR $\ge 4.5\%$. | Bottom-up TAM/SAM/SOM model using household demographics and fitness spending. | Statista Fitness Equipment Reports, Eurostat household data, UK ONS. | **Supported if:** SAM $\ge \$150\text{M}$ USD AND 2026–2029 CAGR $\ge 4.5\%$. | `Untested` |
| **H1.2** | 1.2 Demographics | Urban European households have a high density of qualified target buyers (disposable income $> \$65\text{k}$), but require compact, storable equipment due to smaller median home sizes ($<90\text{ m}^2$). | Spatial housing analysis & income distribution decile cross-tabulation. | Eurostat Housing Database, OECD Family Database. | **Supported if:** Target income households $\ge 2.5\text{M}$ AND median apartment size $< 90\text{ m}^2$. | `Untested` |
| **H2.1** | 2.1 Competitor Landscape | European markets exhibit an unserved "affordable premium" whitespace between budget imports ($< \$500$) and luxury connected hardware ($> \$1,800$). | Price-feature competitor matrix and market share concentration analysis. | Competitor pricing audits (Peloton, Echelon, Horizon, Decathlon), web scraping. | **Supported if:** No dominant competitor holds $>25\%$ market share in the $600–$1,200 tier. | `Untested` |
| **H2.2** | 2.2 Entry Channel | An in-market Direct-to-Consumer (D2C) model supported by a localized 3PL delivers higher long-term brand equity and customer margin than a wholesale retail partnership. | Channel margin waterfall comparison (D2C vs. Retail Wholesale vs. Hybrid). | 3PL rate cards, wholesale discount benchmarks (35–45% off MSRP). | **Supported if:** D2C Year 2 Contribution Margin exceeds Wholesale by $\ge 800\text{ bps}$. | `Untested` |
| **H3.1** | 3.1 Unit Economics | Localized hardware contribution margin will exceed 28% after absorbing international freight, local tariffs, and domestic last-mile delivery. | Unit economics waterfall model across candidate countries. | Drewry Container Index, EU TARIC import tariffs, UK Global Tariff, 3PL quotes. | **Supported if:** Delivered Contribution Margin $M_c \ge 28.0\%$ of net revenue. | `Untested` |
| **H3.2** | 3.2 Payback & Break-Even | A phased entry into the top priority market can achieve operating cash-flow break-even within 18 months, requiring $< \$3.5\text{M}$ initial working capital. | Monthly dynamic financial model and cumulative cash burn tracking. | Financial Model (Phase 06 & 07). | **Supported if:** Cash-flow break-even $\le 18\text{ months}$ AND max cash trough $< \$3.5\text{M}$. | `Untested` |
| **H3.3** | 3.3 Return on Investment | The 3-year project Internal Rate of Return (IRR) will exceed NovaHome’s corporate hurdle rate of 15.0%. | 36-month discounted cash flow (DCF) with conservative terminal value. | Scenario Model (Phase 07). | **Supported if:** 3-Year Project $\text{IRR} \ge 15.0\%$. | `Untested` |
| **H4.1** | 4.1 Logistics & Delivery | Local 3PL fulfillment can execute two-person scheduled room-of-choice delivery for under $110 per unit with an unboxing damage rate $< 1.5\%$. | 3PL benchmarking and specialized two-person freight provider interviews. | Freight forwarding quotes (Kuehne+Nagel, DHL Supply Chain, local specialist carriers). | **Supported if:** Delivered cost $\le \$110/\text{unit}$ AND return rate $\le 3.0\%$. | `Untested` |
| **H4.2** | 4.2 Regulatory & Localization | NovaHome’s hardware requires minor electrical plug modifications and CE/UKCA self-certification without structural redesign, taking $< 90$ days. | Regulatory engineering gap audit. | EU Machinery Directive 2006/42/EC, Low Voltage Directive 2014/35/EU, RED. | **Supported if:** Regulatory compliance certification budget $< \$75\text{k}$ and time-to-market $< 90\text{ days}$. | `Untested` |

---

## 3. Hypothesis Testing Protocol

Every phase of the downstream project maps directly to proving or disproving these hypotheses:
* **Phase 02 & 04**: Tests `H1.1`, `H1.2`, and `H2.1` via demographic data and market sizing models.
* **Phase 03 & 05**: Tests `H2.2` via customer acquisition data, channel performance, and cohort queries.
* **Phase 06 & 07**: Tests `H3.1`, `H3.2`, and `H3.3` via unit economics waterfalls and dynamic financial simulations.
* **Phase 08 & 09**: Consolidates `H4.1` and `H4.2` into the final operational roadmap.

---

## 4. Revision & Decision Log

| Date | Hypothesis ID | Decision | Analytical Evidence | Strategic Implication |
| :--- | :--- | :--- | :--- | :--- |
| *Pending* | — | — | To be updated dynamically upon completion of Phases 02–07 | — |
