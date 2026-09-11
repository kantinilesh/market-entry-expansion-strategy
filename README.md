# NovaHome: International Market Entry & Expansion Strategy 2026

[![Methodology: Bain & Company Standard](https://img.shields.io/badge/Methodology-Bain%20%26%20Company%20Style-blue.svg)](https://www.bain.com)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://www.python.org/)
[![Database: SQL](https://img.shields.io/badge/Database-SQLite%20%2F%20PostgreSQL-orange.svg)](https://www.sqlite.org/)
[![Visualization: Power BI](https://img.shields.io/badge/BI-Power%20BI%20Ready-yellow.svg)](https://powerbi.microsoft.com/)

An end-to-end management consulting case portfolio assessing international market expansion for **NovaHome**, a mid-market smart connected fitness equipment manufacturer. 

This project demonstrates problem structuring, MECE issue trees, hypothesis-driven analytics, secondary market research, bottom-up TAM/SAM/SOM market sizing, Python data cleaning and exploratory analysis, relational SQL database modeling, Excel unit economics, financial break-even modeling, scenario stress-testing, and executive presentation via the Minto Pyramid Principle.

---

## Institutional Disclaimers & Data Integrity Standards

> [!NOTE]
> **Fictional Entity Disclaimer**: NovaHome is a fictional mid-market connected fitness equipment brand created specifically as a rigorous case study for management consulting and strategy portfolio evaluation (tailored for Bain & Company screening). All organizational names and internal operational narratives are illustrative.

> [!IMPORTANT]
> **Data Integrity & Labeling Standards**:
> * **Verified External Data**: Macroeconomic indicators, population statistics, and industry benchmarks are sourced from accredited public agencies (e.g., Eurostat, US Bureau of Labor Statistics, World Bank, OECD).
> * **Clearly Labeled Assumptions**: Every operational parameter without an audited empirical source (e.g., initial baseline marketing weights, launch costs, conversion estimates) is explicitly labeled as an **Assumption**.
> * **Calculated Outputs**: Final metrics (priority markets selected, project IRR, break-even months, ROI) are calculated strictly by the underlying Python, SQL, and Excel models—not forced or pre-determined to fit a preconceived narrative.
> * **Synthetic Data Disclosure**: Where granular transactional customer logs are needed for SQL cohort analysis or Python EDA, data is generated via calibrated, reproducible synthetic scripts and transparently documented.

---

## 1. Project Purpose

The purpose of this project is to simulate a tier-one strategy consulting engagement (Bain & Company style), delivering an executive-level market entry recommendation for NovaHome's leadership team. The project bridges strategic problem structuring with technical data analysis, financial engineering, and business intelligence.

---

## 2. Main Business Question

> **Which international market(s) should NovaHome enter in 2026, which markets must be explicitly rejected, what entry mode should be adopted, and how can expansion achieve an attractive risk-adjusted return and break-even within 18 months without endangering domestic core profitability?**

---

## 3. Current Project Phase

* **Current Phase**: **Phase 01: Business Problem and Consulting Structure** `[ACTIVE / IN REVIEW]`
* **Focus**: Defining the business problem, building the 3-branch MECE issue tree, establishing the 9-point hypothesis register, and formalizing the decision criteria and scoring framework.

---

## 4. Repository Structure

```
market-entry-expansion-strategy/
│
├── README.md                              <- Project overview, business question, phase status, and integrity rules
├── requirements.txt                       <- Python dependencies
├── .gitignore                             <- Git ignore rules for environments, temp files, and checkpoints
│
├── data/
│   ├── raw/                               <- Unmodified raw source datasets (.gitkeep)
│   ├── processed/                         <- Cleaned and transformed datasets (.gitkeep)
│   └── external_sources/                  <- Reference reports, citation logs, and external indices (.gitkeep)
│
├── phase-01-business-problem/             <- [ACTIVE] Problem structuring, issue tree, hypotheses, hurdle criteria
│   ├── case_brief.md                      <- Company background, scope, business question, labeled assumptions
│   ├── issue_tree.md                      <- 3-branch MECE issue tree, Mermaid diagram, and overlap boundaries
│   ├── hypothesis_register.md             <- 9 falsifiable hypotheses with testing metrics and decision implications
│   └── decision_criteria.md               <- Knockout gates, weighted scoring framework, and metric formulas
│
├── phase-02-market-research/              <- Secondary market research, competitor benchmarking, source register
├── phase-03-python-analysis/              <- Data quality auditing, cleaning, and exploratory data analysis (EDA)
├── phase-04-market-sizing/                <- TAM / SAM / SOM calculation models and market attractiveness scoring
├── phase-05-sql-analysis/                 <- Relational schema, consulting SQL queries, customer cohort analytics
├── phase-06-unit-economics/               <- Customer unit economics, contribution margins, break-even model
├── phase-07-scenario-analysis/            <- Base / Bull / Bear financial forecasts and Monte Carlo sensitivity
├── phase-08-executive-recommendation/     <- Pyramid Principle memo, executive summary, and board slide deck outline
├── phase-09-powerbi/                      <- Data model, DAX measures, and Power BI dashboard specifications
├── phase-10-final-portfolio/              <- Bain interview case walkthrough, résumé bullets, and methodology review
│
└── reports/                               <- Exportable PDF memo and board-level presentation slides
```

---

## 5. Summary of Phase 01 Deliverables

* [Case Brief](phase-01-business-problem/case_brief.md): Company profile, current business situation, management objective, main/supporting questions, project scope, out-of-scope boundaries, time horizon, labeled assumptions, and expected deliverables.
* [MECE Issue Tree](phase-01-business-problem/issue_tree.md): 3-branch structural breakdown (Market Attractiveness, Economic Viability, Execution Feasibility) with 18 sub-elements, Mermaid diagram, and explicit overlap disambiguation rules.
* [Hypothesis Register](phase-01-business-problem/hypothesis_register.md): 9 falsifiable hypothesis cards linking strategic questions to quantitative metrics, test criteria, and decision implications.
* [Decision Criteria Framework](phase-01-business-problem/decision_criteria.md): 4 Stage 1 Knockout Gates, Stage 2 Weighted Scoring Rubric (Market 35%, Economics 40%, Feasibility 25% - labeled assumptions), rationale for weight adjustments, and exact financial formulas.

---

## 6. Author & Repository Contact
* **Analyst**: Nilesh Kanti
* **Repository**: [https://github.com/kantinilesh/market-entry-expansion-strategy](https://github.com/kantinilesh/market-entry-expansion-strategy)
