# NovaHome: International Market Entry & Expansion Strategy (2026)

[![Strategy: Bain & Company Standard](https://img.shields.io/badge/Methodology-Bain%20%26%20Company%20Style-blue.svg)](https://www.bain.com)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://www.python.org/)
[![Database: SQL](https://img.shields.io/badge/Database-SQLite%20%2F%20PostgreSQL-orange.svg)](https://www.sqlite.org/)
[![Visualization: Power BI](https://img.shields.io/badge/BI-Power%20BI%20Ready-yellow.svg)](https://powerbi.microsoft.com/)

An end-to-end management consulting case project assessing international expansion for **NovaHome**, a mid-market smart connected fitness equipment manufacturer. 

This project demonstrates problem structuring, hypothesis-driven issue trees, secondary market sizing (TAM/SAM/SOM), Python exploratory data analysis, relational SQL database modeling, Excel unit economics, financial break-even modeling, scenario stress-testing, and executive presentation via the Minto Pyramid Principle.

---

## Executive Summary & Business Problem

* **Client**: NovaHome
* **Industry**: Smart Home Fitness & Connected Wellness Hardware ($600–$1,200 price tier)
* **Core Products**: Smart Connected Ergometers (Spin Bikes, Water Rowers) & Digital Resistance Strength Stations.
* **Context**: Following post-pandemic market normalization in North America, domestic revenue growth has decelerated to 4.2% YoY. To sustain growth and prepare for a Series C / growth equity round in late 2026, the Board of Directors commissioned an evaluation of international expansion opportunities across Europe and Asia-Pacific.
* **Core Mandate**: 
  1. Which international markets should NovaHome enter, and which should be explicitly disqualified?
  2. What is the optimal entry mode (Direct-to-Consumer eCommerce, Retail Partnership, or Local Entity/3PL)?
  3. What are the unit economics, break-even timeline, capital requirement, and risk-adjusted return?
  4. What is the actionable 12-month operational execution roadmap?

---

## Data Integrity & Research Governance

To ensure the analysis meets institutional consulting standards:
* **Verified External Data**: Sourced from official statistical bureaus (e.g., Eurostat, US Bureau of Labor Statistics, World Bank) and validated industry benchmarks.
* **Explicit Assumptions**: Every variable without an audited empirical source is transparently identified with its operational rationale, formula, and conservative bounding.
* **Model-Driven Conclusions**: Priority markets, hurdle rates, and break-even timelines are strictly calculated outputs of our financial and quantitative models—not preconceived narratives.

---

## Project Structure & 10-Phase Roadmap

```
market-entry-expansion-strategy/
│
├── README.md                              <- Project overview, executive summary, and repo roadmap
├── requirements.txt                       <- Python dependencies
├── .gitignore                             <- Git ignore rules for environments, temp files, and checkpoints
│
├── data/
│   ├── raw/                               <- Unmodified raw source datasets
│   ├── processed/                         <- Cleaned and transformed datasets
│   └── external_sources/                  <- Reference reports, citation logs, and external indices
│
├── phase-01-business-problem/             <- [ACTIVE] Problem structuring, issue tree, hypotheses, hurdle criteria
│   ├── case_brief.md
│   ├── issue_tree.md
│   ├── hypothesis_register.md
│   └── decision_criteria.md
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

## Phase 01: Business Problem Structuring Deliverables

* [Case Brief](phase-01-business-problem/case_brief.md): Company profile, market context, strategic dilemma, and expansion constraints.
* [MECE Issue Tree](phase-01-business-problem/issue_tree.md): Hierarchical structural breakdown into Market Attractiveness, Competitive Advantage, Financial Viability, and Operational Feasibility.
* [Hypothesis Register](phase-01-business-problem/hypothesis_register.md): Falsifiable hypothesis cards linking strategic questions to quantitative metrics, data sources, and pass/fail thresholds.
* [Decision Criteria & Hurdle Matrix](phase-01-business-problem/decision_criteria.md): Quantitative hurdles (IRR, Payback Months, Contribution Margin) and qualitative gatekeepers.

---

## Tech Stack & Tooling

* **Problem Structuring**: MECE Issue Trees, Hypothesis-Driven Consulting Frameworks, Minto Pyramid Principle
* **Data Processing & Analytics**: Python 3.10+ (`pandas`, `numpy`, `matplotlib`, `seaborn`)
* **Relational Database**: SQL (ANSI-SQL / SQLite / PostgreSQL compatible)
* **Financial Modeling**: Excel / OpenPyXL (Dynamic multi-scenario DCF, Unit Economics, Break-Even)
* **Business Intelligence**: Power BI (Star Schema data modeling, DAX measures)
* **Version Control & Documentation**: Git, GitHub, Markdown

---

## Author & Project Contact
* **Analyst**: Nilesh Kanti
* **Repository**: [github.com/kantinilesh/market-entry-expansion-strategy](https://github.com/kantinilesh/market-entry-expansion-strategy)
