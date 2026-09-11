#!/usr/bin/env python3
"""
NovaHome Phase 04 Market Sizing & Attractiveness Scoring Engine
Builds:
1. phase-04-market-sizing/tam_sam_som_model.xlsx (multi-sheet financial model with dynamic formulas)
2. phase-04-market-sizing/market_attractiveness_scores.csv (standardized 1-5 multi-factor scoring)
"""

import os
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

print("Starting Phase 04 Market Sizing & Scoring Build...")

# 1. Load clean dataset
clean_data_path = os.path.join("data", "processed", "clean_market_research.csv")
df = pd.read_csv(clean_data_path)
print(f"Loaded clean market data for {len(df)} countries.")

# ---------------------------------------------------------------------
# CALCULATE ATTRACTIVENESS SCORES (1.0 to 5.0 Scale)
# ---------------------------------------------------------------------
# Sub-weights for Market Attractiveness Pillar:
# Size: 25%, Growth: 20%, Demand: 20%, Competition: 15%, Pricing: 10%, Regulatory: 10%
# Total: 100%

# Sizing Estimates for SAM (Estimated via Category spend):
# US TAM ~ $4,200M, UK ~ $650M, DE ~ $780M, NL ~ $160M, AU ~ $280M, SG ~ $65M, UAE ~ $95M, KSA ~ $180M, IN ~ $310M, CA ~ $410M
tam_estimates = {
    'United States': 4200.0,
    'Canada': 410.0,
    'United Kingdom': 650.0,
    'Germany': 780.0,
    'Netherlands': 160.0,
    'Australia': 280.0,
    'Singapore': 65.0,
    'United Arab Emirates': 95.0,
    'Saudi Arabia': 180.0,
    'India': 310.0
}
df['tam_usd_m'] = df['country'].map(tam_estimates)
# SAM is connected mid-tier fitness (~40% of TAM)
df['sam_usd_m'] = (df['tam_usd_m'] * 0.40).round(1)

# Normalization functions (1.0 to 5.0 scale)
# 1. Market Size Score (Log-normalized SAM):
min_sam = 25.0
max_sam = 1700.0
# Log scale score
df['market_size_score'] = (1.0 + 4.0 * (np.log(df['sam_usd_m']) - np.log(min_sam)) / (np.log(max_sam) - np.log(min_sam))).clip(1.0, 5.0).round(2)

# 2. Growth Score: Higher is better. Hurdle = 4.5% (score = 3.0), <3.0% = 1.0, >=8.5% = 5.0
def score_growth(cagr):
    if cagr <= 3.0:
        return 1.0
    elif cagr >= 8.5:
        return 5.0
    else:
        return round(1.0 + 4.0 * (cagr - 3.0) / (8.5 - 3.0), 2)
df['growth_score'] = df['market_growth_cagr_pct'].apply(score_growth)

# 3. Demand Score: Higher is better. Home Fitness Demand Index (0-100).
# Index 50 -> 1.0, Index 90 -> 5.0
def score_demand(idx):
    score = 1.0 + 4.0 * (idx - 50.0) / (90.0 - 50.0)
    return round(float(np.clip(score, 1.0, 5.0)), 2)
df['demand_score'] = df['home_fitness_demand_index'].apply(score_demand)

# 4. Competition Score: LOWER competitor intensity is BETTER (Inverted scale)
# Raw intensity: 1.0 (Low) to 5.0 (High)
# Inverted score = 6.0 - raw
df['competition_score'] = (6.0 - df['competitor_intensity_score']).round(2)

# 5. Pricing Score: Higher income / willingness to pay is better.
# Disposable income: $3,200 -> 1.0, $55,000 -> 5.0
def score_pricing(income):
    score = 1.0 + 4.0 * (income - 3000.0) / (55000.0 - 3000.0)
    return round(float(np.clip(score, 1.0, 5.0)), 2)
df['pricing_score'] = df['disposable_income_usd'].apply(score_pricing)

# 6. Regulatory Score: LOWER complexity is BETTER (Inverted scale)
# Raw complexity: 1.0 (Low) to 5.0 (High)
# Inverted score = 6.0 - raw
df['regulatory_score'] = (6.0 - df['regulatory_complexity_score']).round(2)

# Weighted Composite Attractiveness Score:
# Weights: Size 25%, Growth 20%, Demand 20%, Comp 15%, Pricing 10%, Reg 10%
w_size = 0.25
w_growth = 0.20
w_demand = 0.20
w_comp = 0.15
w_price = 0.10
w_reg = 0.10
assert abs((w_size + w_growth + w_demand + w_comp + w_price + w_reg) - 1.0) < 1e-6, "Weights must sum to 100%!"

df['weighted_market_attractiveness_score'] = (
    df['market_size_score'] * w_size +
    df['growth_score'] * w_growth +
    df['demand_score'] * w_demand +
    df['competition_score'] * w_comp +
    df['pricing_score'] * w_price +
    df['regulatory_score'] * w_reg
).round(2)

# Sort by score descending
df_scores = df[[
    'country', 'market_size_score', 'growth_score', 'demand_score',
    'competition_score', 'pricing_score', 'regulatory_score',
    'weighted_market_attractiveness_score'
]].sort_values('weighted_market_attractiveness_score', ascending=False)

scores_csv_path = os.path.join("phase-04-market-sizing", "market_attractiveness_scores.csv")
df_scores.to_csv(scores_csv_path, index=False)
print(f"Market attractiveness scores saved to: {scores_csv_path}")
print(df_scores.to_string(index=False))

# ---------------------------------------------------------------------
# BUILD DYNAMIC EXCEL MODEL: tam_sam_som_model.xlsx
# ---------------------------------------------------------------------
print("\nBuilding OpenPyXL Workbook: tam_sam_som_model.xlsx...")
wb = openpyxl.Workbook()

# Style definitions
font_title = Font(name="Calibri", size=16, bold=True, color="1F4E78")
font_subtitle = Font(name="Calibri", size=11, italic=True, color="595959")
font_section = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=10, bold=True)
font_regular = Font(name="Calibri", size=10)
font_assumption = Font(name="Calibri", size=10, color="002060")

fill_navy = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
fill_blue_header = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
fill_light_gray = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
fill_assumption = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # soft yellow
fill_calc = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid") # soft green

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
thick_bottom = Border(bottom=Side(style='medium', color='1F4E78'))

# ---------------------------------------------------------------------
# SHEET 1: Top-Down & Bottom-Up Sizing
# ---------------------------------------------------------------------
ws1 = wb.active
ws1.title = "TAM SAM SOM Sizing"
ws1.views.sheetView[0].showGridLines = True

ws1["A1"] = "NovaHome International Expansion — TAM / SAM / SOM Market Sizing Model"
ws1["A1"].font = font_title
ws1["A2"] = "Dynamic Top-Down & Bottom-Up Multi-Market Sizing (2026–2029) | Denominated in USD Millions"
ws1["A2"].font = font_subtitle

# Color Legend
ws1["A4"] = "Model Legend:"
ws1["A4"].font = font_bold
ws1["B4"] = "Input / Benchmark Data"
ws1["B4"].fill = fill_light_gray
ws1["D4"] = "Assumption Cell (Editable)"
ws1["D4"].fill = fill_assumption
ws1["F4"] = "Calculated Formula (Dynamic)"
ws1["F4"].fill = fill_calc

headers_s1 = [
    "Country", "Population (M)", "Urban %", "Disp. Income ($)", "Fitness %",
    "Total Fitness TAM ($M)", "Mid-Market Segment %", "Top-Down SAM ($M)", "Achievable Share %", "Top-Down SOM ($M)",
    "HH Size (Est)", "Total HH (M)", "Qualifying HH (k)", "Annual Buy Rate %", "Annual Category Units", "Bottom-Up SAM ($M)", "Bottom-Up SOM ($M)"
]

ws1.append([]) # blank row 5
ws1.row_dimensions[6].height = 28
for col_idx, h in enumerate(headers_s1, 1):
    cell = ws1.cell(row=6, column=col_idx, value=h)
    cell.font = font_header
    cell.fill = fill_blue_header
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

start_row = 7
for idx, row in df.iterrows():
    r = start_row + idx
    c_name = row['country']
    pop = row['population_m']
    urban_pct = row['urban_population_pct'] / 100.0
    income = row['disposable_income_usd']
    fit_pct = row['fitness_participation_pct'] / 100.0
    tam = row['tam_usd_m']
    
    # Section 1: Inputs
    ws1.cell(row=r, column=1, value=c_name).font = font_bold
    ws1.cell(row=r, column=2, value=pop).number_format = '#,##0.0'
    ws1.cell(row=r, column=3, value=urban_pct).number_format = '0.0%'
    ws1.cell(row=r, column=4, value=income).number_format = '$#,##0'
    ws1.cell(row=r, column=5, value=fit_pct).number_format = '0.0%'
    ws1.cell(row=r, column=6, value=tam).number_format = '$#,##0.0'
    
    # Top Down Assumption: Segment % = 40.0%
    cell_seg = ws1.cell(row=r, column=7, value=0.40)
    cell_seg.number_format = '0.0%'
    cell_seg.fill = fill_assumption
    
    # Top Down SAM = TAM * Segment %
    cell_td_sam = ws1.cell(row=r, column=8, value=f"=F{r}*G{r}")
    cell_td_sam.number_format = '$#,##0.0'
    cell_td_sam.fill = fill_calc
    
    # Top Down Share Assumption = 3.0% (except domestic US=8.0%, CA=5.0%)
    share_val = 0.08 if c_name == 'United States' else (0.05 if c_name == 'Canada' else 0.03)
    cell_share = ws1.cell(row=r, column=9, value=share_val)
    cell_share.number_format = '0.0%'
    cell_share.fill = fill_assumption
    
    # Top Down SOM = SAM * Share
    cell_td_som = ws1.cell(row=r, column=10, value=f"=H{r}*I{r}")
    cell_td_som.number_format = '$#,##0.0'
    cell_td_som.fill = fill_calc
    
    # Bottom Up Inputs & Assumptions
    hh_size = 2.5
    cell_hh_size = ws1.cell(row=r, column=11, value=hh_size)
    cell_hh_size.number_format = '0.0'
    cell_hh_size.fill = fill_assumption
    
    # Total HH = Population / HH Size
    cell_tot_hh = ws1.cell(row=r, column=12, value=f"=B{r}/K{r}")
    cell_tot_hh.number_format = '#,##0.0'
    cell_tot_hh.fill = fill_calc
    
    # Qualifying HH (thousands) = Total HH * Urban% * Fitness% * 1000
    cell_qual_hh = ws1.cell(row=r, column=13, value=f"=L{r}*C{r}*E{r}*1000")
    cell_qual_hh.number_format = '#,##0'
    cell_qual_hh.fill = fill_calc
    
    # Annual Buy Rate = 10.0% (Assumption)
    cell_buy_rate = ws1.cell(row=r, column=14, value=0.10)
    cell_buy_rate.number_format = '0.0%'
    cell_buy_rate.fill = fill_assumption
    
    # Annual Category Units = Qualifying HH * Buy Rate * 1000
    cell_units = ws1.cell(row=r, column=15, value=f"=M{r}*N{r}*10")
    cell_units.number_format = '#,##0'
    cell_units.fill = fill_calc
    
    # Bottom Up SAM ($M) = Units * $950 ASP * 40% mid-tier / 1,000,000
    cell_bu_sam = ws1.cell(row=r, column=16, value=f"=(O{r}*950*0.40)/1000000")
    cell_bu_sam.number_format = '$#,##0.0'
    cell_bu_sam.fill = fill_calc
    
    # Bottom Up SOM ($M) = Bottom Up SAM * Share
    cell_bu_som = ws1.cell(row=r, column=17, value=f"=P{r}*I{r}")
    cell_bu_som.number_format = '$#,##0.0'
    cell_bu_som.fill = fill_calc
    
    for c in range(1, 18):
        ws1.cell(row=r, column=c).border = thin_border

# Totals Row
tot_row = start_row + len(df)
ws1.cell(row=tot_row, column=1, value="Total / Average").font = font_bold
ws1.cell(row=tot_row, column=6, value=f"=SUM(F{start_row}:F{tot_row-1})").number_format = '$#,##0.0'
ws1.cell(row=tot_row, column=8, value=f"=SUM(H{start_row}:H{tot_row-1})").number_format = '$#,##0.0'
ws1.cell(row=tot_row, column=10, value=f"=SUM(J{start_row}:J{tot_row-1})").number_format = '$#,##0.0'
for c in range(1, 18):
    cell = ws1.cell(row=tot_row, column=c)
    cell.border = Border(top=Side(style='thin', color='1F4E78'), bottom=Side(style='double', color='1F4E78'))
    cell.font = font_bold

# Auto-adjust column widths
for col in ws1.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws1.column_dimensions[col_letter].width = max(max_len + 3, 12)

# ---------------------------------------------------------------------
# SHEET 2: Market Attractiveness Scoring Matrix
# ---------------------------------------------------------------------
ws2 = wb.create_sheet(title="Attractiveness Scoring")
ws2.views.sheetView[0].showGridLines = True

ws2["A1"] = "NovaHome Market Attractiveness Scoring Matrix (Pillar 1)"
ws2["A1"].font = font_title
ws2["A2"] = "Multi-Criteria Evaluation (1.0 = Worst, 5.0 = Best) | Weighted Composite Score"
ws2["A2"].font = font_subtitle

# Weight row
ws2["A4"] = "Criteria Weights:"
ws2["A4"].font = font_bold
weights_map = [
    ("Market Size (SAM)", 0.25),
    ("3-Yr CAGR Growth", 0.20),
    ("Customer Demand Index", 0.20),
    ("Competitive Whitespace", 0.15),
    ("Pricing / Income Capacity", 0.10),
    ("Regulatory Ease", 0.10)
]

for idx, (label, w) in enumerate(weights_map, 2):
    ws2.cell(row=4, column=idx, value=w).number_format = '0%'
    ws2.cell(row=4, column=idx).font = font_bold
    ws2.cell(row=4, column=idx).fill = fill_assumption
ws2.cell(row=4, column=8, value="100%").font = font_bold

headers_s2 = [
    "Country", "Market Size Score (25%)", "Growth Score (20%)", "Demand Score (20%)",
    "Competition Score (15%)", "Pricing Score (10%)", "Regulatory Score (10%)",
    "Weighted Attractiveness Score (1.0-5.0)"
]

ws2.row_dimensions[6].height = 26
for col_idx, h in enumerate(headers_s2, 1):
    cell = ws2.cell(row=6, column=col_idx, value=h)
    cell.font = font_header
    cell.fill = fill_navy
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

start_row_s2 = 7
for idx, row in df_scores.iterrows():
    r = start_row_s2 + idx
    ws2.cell(row=r, column=1, value=row['country']).font = font_bold
    ws2.cell(row=r, column=2, value=row['market_size_score']).number_format = '0.00'
    ws2.cell(row=r, column=3, value=row['growth_score']).number_format = '0.00'
    ws2.cell(row=r, column=4, value=row['demand_score']).number_format = '0.00'
    ws2.cell(row=r, column=5, value=row['competition_score']).number_format = '0.00'
    ws2.cell(row=r, column=6, value=row['pricing_score']).number_format = '0.00'
    ws2.cell(row=r, column=7, value=row['regulatory_score']).number_format = '0.00'
    
    # Dynamic Weighted Score Formula
    formula = f"=B{r}*$B$4 + C{r}*$C$4 + D{r}*$D$4 + E{r}*$E$4 + F{r}*$F$4 + G{r}*$G$4"
    cell_score = ws2.cell(row=r, column=8, value=formula)
    cell_score.number_format = '0.00'
    cell_score.font = font_bold
    cell_score.fill = fill_calc
    
    for c in range(1, 9):
        ws2.cell(row=r, column=c).border = thin_border

for col in ws2.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws2.column_dimensions[col_letter].width = max(max_len + 3, 14)

# ---------------------------------------------------------------------
# SHEET 3: Sensitivity Analysis
# ---------------------------------------------------------------------
ws3 = wb.create_sheet(title="SOM Sensitivity")
ws3.views.sheetView[0].showGridLines = True

ws3["A1"] = "NovaHome Serviceable Obtainable Market (SOM) Sensitivity Matrix"
ws3["A1"].font = font_title
ws3["A2"] = "Impact of Market Share Capture Rates (1.0% to 5.0%) on Annual Revenue Potential ($M USD)"
ws3["A2"].font = font_subtitle

share_scenarios = [0.01, 0.02, 0.03, 0.04, 0.05]
ws3.cell(row=5, column=1, value="Country").font = font_header
ws3.cell(row=5, column=1).fill = fill_navy
ws3.cell(row=5, column=2, value="Top-Down SAM ($M)").font = font_header
ws3.cell(row=5, column=2).fill = fill_navy

for idx, s in enumerate(share_scenarios, 3):
    cell = ws3.cell(row=5, column=idx, value=f"SOM @ {s*100:.0f}% Share")
    cell.font = font_header
    cell.fill = fill_blue_header
    cell.alignment = Alignment(horizontal="center")

start_row_s3 = 6
for idx, row in df.iterrows():
    r = start_row_s3 + idx
    ref_row_s1 = start_row + idx
    ws3.cell(row=r, column=1, value=row['country']).font = font_bold
    ws3.cell(row=r, column=2, value=f"='TAM SAM SOM Sizing'!H{ref_row_s1}").number_format = '$#,##0.0'
    
    for s_idx, s in enumerate(share_scenarios, 3):
        cell = ws3.cell(row=r, column=s_idx, value=f"=B{r}*{s}")
        cell.number_format = '$#,##0.0'
        cell.fill = fill_calc
        cell.border = thin_border
    ws3.cell(row=r, column=1).border = thin_border
    ws3.cell(row=r, column=2).border = thin_border

for col in ws3.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws3.column_dimensions[col_letter].width = max(max_len + 3, 14)

# ---------------------------------------------------------------------
# SHEET 4: Assumptions & Sources Notes
# ---------------------------------------------------------------------
ws4 = wb.create_sheet(title="Assumptions & Sources")
ws4.views.sheetView[0].showGridLines = True

ws4["A1"] = "NovaHome Market Sizing Model — Assumptions & Governance Register"
ws4["A1"].font = font_title
ws4["A2"] = "Audit Log for All Sizing Multipliers, Share Caps, and Baseline Benchmarks"
ws4["A2"].font = font_subtitle

headers_s4 = ["Parameter / Multiplier", "Baseline Value", "Type", "Operational & Strategic Rationale", "Primary Source"]
ws4.row_dimensions[5].height = 24
for c_idx, h in enumerate(headers_s4, 1):
    cell = ws4.cell(row=5, column=c_idx, value=h)
    cell.font = font_header
    cell.fill = fill_navy

assumptions_data = [
    ("Mid-Market Connected Segment %", "40.0%", "Commercial Assumption", "Share of home fitness equipment market in the $600-$1,200 connected tier vs. discount/luxury", "Statista Worldwide Fitness Insights (SRC-006)"),
    ("Target Achievable Market Share (SOM)", "3.0%", "Strategic Assumption", "Realistic 3-year market share achievable via D2C & 3PL distribution without retail presence", "NovaHome Executive Case Brief (NH-STRAT-2026-001)"),
    ("Domestic US Market Share", "8.0%", "Empirical Benchmark", "Current NovaHome domestic market share in North American mid-market connected segment", "NovaHome FY2025 Internal Financials"),
    ("Average Household Size", "2.5 Persons", "Demographic Standard", "Average household size in urban centers across OECD and European nations", "OECD Family Database / Eurostat"),
    ("Annual Hardware Buying / Upgrade Rate", "10.0%", "Category Assumption", "Reflects an 8-to-10-year product replacement and new customer adoption lifecycle", "IHRSA & EuropeActive Market Studies"),
    ("Average Selling Price (ASP)", "$950 USD", "Pricing Benchmark", "Blended average order value across NovaPulse Bike, Rower, and Strength Station", "NovaHome FY2025 Preliminary Accounts")
]

for idx, row_data in enumerate(assumptions_data, 6):
    for c_idx, val in enumerate(row_data, 1):
        cell = ws4.cell(row=idx, column=c_idx, value=val)
        cell.font = font_regular
        cell.border = thin_border
        if c_idx == 2:
            cell.font = font_bold
            cell.fill = fill_assumption

for col in ws4.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws4.column_dimensions[col_letter].width = max(max_len + 4, 16)

excel_path = os.path.join("phase-04-market-sizing", "tam_sam_som_model.xlsx")
wb.save(excel_path)
print(f"Excel Model saved successfully to: {excel_path}")
print("=== PHASE 04 BUILD COMPLETE ===")
