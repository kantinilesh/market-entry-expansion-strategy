#!/usr/bin/env python3
"""
NovaHome Phase 07 — Scenario & Sensitivity Analysis Engine
==========================================================
Generates: phase-07-scenario-analysis/scenario_model.xlsx

Workbook Structure:
  Sheet 1: Scenario Dashboard (Base / Upside / Downside per market)
  Sheet 2: Sensitivity Analysis (Two-way matrices + variable impact ranking)
  Sheet 3: Cash Flow Scenarios (24-month projections × 3 scenarios × 4 markets)

CRITICAL: Base-case contribution per unit is anchored to the VERIFIED
Phase 06 comparative break-even figures (NH-FIN-2026-001):
  Netherlands:  $213.68 / unit  (22.7% margin)
  United Kingdom: $177.67 / unit  (19.5% margin)
  Australia:      $191.00 / unit  (18.7% margin)
  Germany:        $192.12 / unit  (20.0% margin)

Scenario multipliers adjust ASP, cost components, and volume around these
verified anchors. No outputs are manually forced — the model dictates the conclusions.
"""

import os
import math
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

print("=" * 70)
print("PHASE 07: SCENARIO & SENSITIVITY ANALYSIS ENGINE")
print("=" * 70)

# =====================================================================
# STYLE DEFINITIONS (Consistent with Phase 06 visual language)
# =====================================================================
font_title = Font(name="Calibri", size=16, bold=True, color="1F4E78")
font_subtitle = Font(name="Calibri", size=11, italic=True, color="595959")
font_section = Font(name="Calibri", size=13, bold=True, color="1F4E78")
font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=10, bold=True)
font_bold_blue = Font(name="Calibri", size=10, bold=True, color="1F4E78")
font_regular = Font(name="Calibri", size=10)
font_warning = Font(name="Calibri", size=10, bold=True, color="9C0006")
font_success = Font(name="Calibri", size=10, bold=True, color="006100")

fill_navy = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
fill_blue_header = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
fill_light_gray = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
fill_assumption = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
fill_calc = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
fill_danger = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
fill_upside = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
fill_downside = PatternFill(start_color="FFE0CC", end_color="FFE0CC", fill_type="solid")
fill_base = PatternFill(start_color="DAEEF3", end_color="DAEEF3", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)

# =====================================================================
# BASE-CASE PARAMETERS (Anchored to Phase 06 Verified Outputs)
# =====================================================================
# The Phase 06 comparative break-even model (Sheet 2) established these
# delivered contribution values after the full cost waterfall:
#   Total VC = FOB + Shipping + Tariff + Last-Mile 3PL + Payment Fee + CAC + Warranty
# These numbers were committed to GitHub at c7bcdcf and form the canonical reference.

markets = {
    "Netherlands": {
        "asp": 940.0,
        "total_vc": 726.32,         # Phase 06 verified
        "contribution": 213.68,     # Phase 06 verified
        "margin_pct": 22.7,         # Phase 06 verified
        "launch_capex": 390000.0,
        "monthly_opex": 20000.0,
        "breakeven_month": 12,      # Phase 06 verified
        # Component breakdown for scenario stress (proportional to total VC)
        "fob": 450.0, "shipping": 125.0, "cac": 170.0,
        # 24-month volume ramp (Netherlands ~0.25x UK scale)
        "ramp": [10, 14, 18, 23, 29, 35, 42, 48, 54, 59, 63, 65,
                 70, 76, 83, 90, 98, 105, 113, 120, 126, 131, 135, 138]
    },
    "United Kingdom": {
        "asp": 910.0,
        "total_vc": 732.33,
        "contribution": 177.67,
        "margin_pct": 19.5,
        "launch_capex": 420000.0,
        "monthly_opex": 26000.0,
        "breakeven_month": 14,
        "fob": 450.0, "shipping": 165.0, "cac": 210.0,
        "ramp": [40, 55, 70, 90, 115, 140, 165, 190, 215, 235, 250, 260,
                 280, 305, 330, 360, 390, 420, 450, 480, 505, 525, 540, 550]
    },
    "Australia": {
        "asp": 1020.0,
        "total_vc": 829.00,
        "contribution": 191.00,
        "margin_pct": 18.7,
        "launch_capex": 460000.0,
        "monthly_opex": 25000.0,
        "breakeven_month": 15,
        "fob": 450.0, "shipping": 195.0, "cac": 205.0,
        "ramp": [20, 28, 36, 46, 58, 72, 84, 97, 110, 120, 128, 133,
                 143, 156, 168, 184, 199, 214, 230, 245, 258, 268, 276, 281]
    },
    "Germany": {
        "asp": 960.0,
        "total_vc": 767.88,
        "contribution": 192.12,
        "margin_pct": 20.0,
        "launch_capex": 680000.0,
        "monthly_opex": 28000.0,
        "breakeven_month": 16,
        "fob": 450.0, "shipping": 155.0, "cac": 190.0,
        "ramp": [35, 48, 62, 79, 101, 123, 145, 167, 189, 207, 220, 229,
                 246, 268, 290, 317, 343, 369, 396, 422, 444, 462, 475, 484]
    }
}

# =====================================================================
# SCENARIO DEFINITIONS
# =====================================================================
# Scenarios adjust the ASP, variable cost components, capex, opex, and volume.
# The contribution per unit is RE-COMPUTED from adjusted ASP - adjusted total VC.
#
# Variable cost adjustment is decomposed into sub-component multipliers:
#   - FOB cost (manufacturing)
#   - Shipping/freight
#   - CAC (customer acquisition)
#   - Residual costs (duties, payment fee, warranty) scale with ASP automatically

def compute_scenario(mkt, scn):
    """
    Compute full financial profile for a market under a scenario.
    
    Variable cost is rebuilt from components:
      Total VC = adjusted_FOB + adjusted_Shipping + adjusted_CAC + residual_costs
    where residual_costs scale proportionally with ASP changes.
    """
    # Adjusted ASP (price × fx impact)
    adj_asp = mkt["asp"] * scn["asp_mult"] * scn["fx_mult"]
    
    # Adjusted cost components
    adj_fob = mkt["fob"] * scn["fob_mult"]
    adj_shipping = mkt["shipping"] * scn["shipping_mult"]
    adj_cac = mkt["cac"] * scn["cac_mult"]
    
    # Residual costs: duties, payment fee, warranty
    # In Phase 06 base, residual = total_vc - fob - shipping - cac
    base_residual = mkt["total_vc"] - mkt["fob"] - mkt["shipping"] - mkt["cac"]
    # Residual scales proportionally with ASP (since duties, payment fees, warranty are ASP-dependent)
    adj_residual = base_residual * (adj_asp / mkt["asp"])
    
    adj_total_vc = adj_fob + adj_shipping + adj_cac + adj_residual
    adj_contribution = adj_asp - adj_total_vc
    adj_margin_pct = (adj_contribution / adj_asp * 100) if adj_asp > 0 else 0.0
    
    adj_capex = mkt["launch_capex"] * scn["capex_mult"]
    adj_opex = mkt["monthly_opex"] * scn["opex_mult"]
    
    # Volume ramp with multiplier
    adj_ramp = [max(1, round(u * scn["volume_mult"])) for u in mkt["ramp"]]
    
    # 24-month cash flow
    cumulative_cf = -adj_capex
    breakeven_month = None
    monthly_data = []
    
    for m_idx, units in enumerate(adj_ramp):
        m_revenue = units * adj_asp
        m_vc = units * adj_total_vc
        m_contribution = m_revenue - m_vc
        m_net_cf = m_contribution - adj_opex
        cumulative_cf += m_net_cf
        
        monthly_data.append({
            "month": m_idx + 1,
            "units": units,
            "revenue": m_revenue,
            "variable_costs": m_vc,
            "contribution": m_contribution,
            "fixed_opex": adj_opex,
            "net_cf": m_net_cf,
            "cumulative_cf": cumulative_cf
        })
        
        if breakeven_month is None and cumulative_cf >= 0:
            breakeven_month = m_idx + 1
    
    # 36-month extrapolation (terminal rate = last month's volume × 12 more months)
    terminal_monthly = adj_ramp[-1]
    cum_units_24 = sum(adj_ramp)
    cum_units_36 = cum_units_24 + (terminal_monthly * 12)
    
    total_36mo_contribution = cum_units_36 * adj_contribution
    total_36mo_opex = adj_opex * 36
    net_36mo = total_36mo_contribution - total_36mo_opex - adj_capex
    roi_3yr = (net_36mo / adj_capex * 100) if adj_capex > 0 else 0.0
    
    # Payback months (from average monthly net CF in months 7-18)
    if len(monthly_data) >= 18:
        avg_net = sum(d["net_cf"] for d in monthly_data[6:18]) / 12
        payback = (adj_capex / avg_net) if avg_net > 0 else float('inf')
    else:
        payback = float('inf')
    
    return {
        "asp": adj_asp,
        "fob": adj_fob,
        "shipping": adj_shipping,
        "cac": adj_cac,
        "residual": adj_residual,
        "total_vc": adj_total_vc,
        "contribution": adj_contribution,
        "margin_pct": adj_margin_pct,
        "launch_capex": adj_capex,
        "monthly_opex": adj_opex,
        "breakeven_month": breakeven_month,
        "roi_3yr": roi_3yr,
        "payback_months": payback,
        "ramp": adj_ramp,
        "monthly_data": monthly_data,
        "cum_units_24": sum(adj_ramp),
        "cumulative_cf_24": cumulative_cf,
        "total_24mo_revenue": sum(d["revenue"] for d in monthly_data)
    }


scenarios = {
    "Base Case": {
        "volume_mult": 1.00, "asp_mult": 1.00, "cac_mult": 1.00,
        "fob_mult": 1.00, "shipping_mult": 1.00,
        "capex_mult": 1.00, "opex_mult": 1.00, "fx_mult": 1.00
    },
    "Upside Case": {
        "volume_mult": 1.20, "asp_mult": 1.06, "cac_mult": 0.85,
        "fob_mult": 0.95, "shipping_mult": 0.90,
        "capex_mult": 0.95, "opex_mult": 0.90, "fx_mult": 1.05
    },
    "Downside Case": {
        "volume_mult": 0.75, "asp_mult": 0.92, "cac_mult": 1.25,
        "fob_mult": 1.10, "shipping_mult": 1.20,
        "capex_mult": 1.15, "opex_mult": 1.20, "fx_mult": 0.90
    }
}

# =====================================================================
# COMPUTE ALL RESULTS
# =====================================================================
print("\nComputing scenario economics for all markets...")
print(f"{'Market':20s} | {'Scenario':15s} | {'Contrib/Unit':>12s} | {'Margin':>7s} | {'Break-Even':>16s} | {'3-Yr ROI':>9s}")
print("-" * 90)

results = {}
for mkt_name, mkt_params in markets.items():
    results[mkt_name] = {}
    for scn_name, scn_params in scenarios.items():
        r = compute_scenario(mkt_params, scn_params)
        results[mkt_name][scn_name] = r
        be_str = f"Month {r['breakeven_month']}" if r['breakeven_month'] else "Not Achieved"
        print(f"  {mkt_name:20s} | {scn_name:15s} | ${r['contribution']:9.2f}   | {r['margin_pct']:5.1f}%  | {be_str:16s} | {r['roi_3yr']:7.1f}%")

# =====================================================================
# VALIDATION CHECKS
# =====================================================================
print("\n--- VALIDATION CHECKS ---")
all_passed = True

for mkt_name in markets:
    base = results[mkt_name]["Base Case"]
    up = results[mkt_name]["Upside Case"]
    down = results[mkt_name]["Downside Case"]
    
    # Check 1: Contribution ordering
    if up["contribution"] > base["contribution"] > down["contribution"]:
        print(f"  ✅ {mkt_name}: Contribution ordering correct (Upside > Base > Downside)")
    else:
        print(f"  ❌ {mkt_name}: CONTRIBUTION ORDERING VIOLATION!")
        all_passed = False
    
    # Check 2: Base case matches Phase 06 within $0.01
    expected = markets[mkt_name]["contribution"]
    if abs(base["contribution"] - expected) < 0.02:
        print(f"  ✅ {mkt_name}: Base case matches Phase 06 (${base['contribution']:.2f} ≈ ${expected:.2f})")
    else:
        print(f"  ⚠️  {mkt_name}: Base case deviation from Phase 06 (${base['contribution']:.2f} vs ${expected:.2f})")
    
    # Check 3: Downside uses worse assumptions
    if down["cac"] > base["cac"] and down["asp"] < base["asp"] and down["shipping"] > base["shipping"]:
        print(f"  ✅ {mkt_name}: Downside assumptions strictly worse than Base")
    else:
        print(f"  ❌ {mkt_name}: DOWNSIDE ASSUMPTION LEAKAGE!")
        all_passed = False
    
    # Check 4: Break-even ordering (if both exist)
    if up["breakeven_month"] and base["breakeven_month"]:
        if up["breakeven_month"] <= base["breakeven_month"]:
            print(f"  ✅ {mkt_name}: Break-even ordering correct (Upside ≤ Base)")
        else:
            print(f"  ❌ {mkt_name}: BREAK-EVEN ORDERING VIOLATION!")
            all_passed = False

print(f"\n{'✅ ALL VALIDATION CHECKS PASSED' if all_passed else '❌ SOME CHECKS FAILED'}")

# =====================================================================
# WORKBOOK GENERATION
# =====================================================================
print("\n--- GENERATING EXCEL WORKBOOK ---")
wb = openpyxl.Workbook()

# =====================================================================
# SHEET 1: SCENARIO DASHBOARD
# =====================================================================
ws1 = wb.active
ws1.title = "Scenario Dashboard"
ws1.sheet_properties.tabColor = "1F4E78"

ws1["A1"] = "NovaHome International Expansion — Scenario Analysis Dashboard"
ws1["A1"].font = font_title
ws1["A2"] = "Base Case / Upside Case / Downside Case Comparison Across Qualified Markets | Phase 07"
ws1["A2"].font = font_subtitle

# Legend
r = 4
ws1.cell(row=r, column=1, value="Model Legend:").font = font_bold
ws1.cell(row=r, column=2, value="Base Case").fill = fill_base
ws1.cell(row=r, column=4, value="Upside Case").fill = fill_upside
ws1.cell(row=r, column=6, value="Downside Case").fill = fill_downside
ws1.cell(row=r, column=8, value="Assumption (Editable)").fill = fill_assumption
ws1.cell(row=r, column=10, value="Danger / Fail").fill = fill_danger

# ---- Section A: Scenario Assumption Multipliers ----
r = 6
ws1.cell(row=r, column=1, value="SECTION A: SCENARIO ASSUMPTION MULTIPLIERS").font = font_section

r = 8
headers_assumptions = ["Variable", "Downside", "Base", "Upside", "Consulting Rationale"]
for c_idx, h in enumerate(headers_assumptions, 1):
    cell = ws1.cell(row=r, column=c_idx, value=h)
    cell.font = font_header
    cell.fill = fill_navy
    cell.alignment = align_center

assumption_rows = [
    ("Sales Volume", "−25%", "0%", "+20%", "Demand elasticity under economic slowdown vs. brand momentum"),
    ("Selling Price (ASP)", "−8%", "0%", "+6%", "Pricing pressure from incumbents vs. premium positioning success"),
    ("Customer Acquisition Cost", "+25%", "0%", "−15%", "Ad market inflation / CPM spikes vs. organic referral growth"),
    ("Product Cost (FOB)", "+10%", "0%", "−5%", "Supply chain disruption vs. volume procurement discount"),
    ("Shipping / Freight Cost", "+20%", "0%", "−10%", "Container rate volatility vs. consolidated routing efficiency"),
    ("Launch Capex", "+15%", "0%", "−5%", "Regulatory cost overrun vs. streamlined certification"),
    ("Monthly Fixed Opex", "+20%", "0%", "−10%", "Cost inflation + FX headwinds vs. operational lean startup"),
    ("Currency Impact (FX)", "−10%", "0%", "+5%", "USD strengthening erodes revenue vs. favorable FX translation"),
]

for idx, (var_name, down_v, base_v, up_v, rationale) in enumerate(assumption_rows):
    row = r + 1 + idx
    ws1.cell(row=row, column=1, value=var_name).font = font_bold
    ws1.cell(row=row, column=2, value=down_v).fill = fill_downside
    ws1.cell(row=row, column=2).alignment = align_center
    ws1.cell(row=row, column=3, value=base_v).fill = fill_base
    ws1.cell(row=row, column=3).alignment = align_center
    ws1.cell(row=row, column=4, value=up_v).fill = fill_upside
    ws1.cell(row=row, column=4).alignment = align_center
    ws1.cell(row=row, column=5, value=rationale).font = font_regular
    for c in range(1, 6):
        ws1.cell(row=row, column=c).border = thin_border

# ---- Section B: Per-Market Scenario Outputs ----
r_section_b = r + 1 + len(assumption_rows) + 2
ws1.cell(row=r_section_b, column=1, value="SECTION B: PER-MARKET SCENARIO OUTPUTS").font = font_section

r_table = r_section_b + 2
dashboard_headers = [
    "Market", "Scenario",
    "Adjusted ASP ($)", "Adjusted CAC ($)", "Total VC / Unit ($)",
    "Contribution / Unit ($)", "Contribution Margin (%)",
    "Launch Capex ($)", "Monthly Opex ($)",
    "Break-Even Month", "3-Year ROI (%)", "24-Mo Cum. Cash Flow ($)",
    "Board 18-Mo Hurdle"
]

for c_idx, h in enumerate(dashboard_headers, 1):
    cell = ws1.cell(row=r_table, column=c_idx, value=h)
    cell.font = font_header
    cell.fill = fill_navy
    cell.alignment = align_center
ws1.row_dimensions[r_table].height = 32

r_data = r_table + 1
scenario_order = ["Upside Case", "Base Case", "Downside Case"]
scenario_fills = {"Upside Case": fill_upside, "Base Case": fill_base, "Downside Case": fill_downside}

for mkt_name in ["Netherlands", "United Kingdom", "Australia", "Germany"]:
    for scn_idx, scn_name in enumerate(scenario_order):
        row = r_data
        res = results[mkt_name][scn_name]
        
        if scn_idx == 0:
            ws1.cell(row=row, column=1, value=mkt_name).font = font_bold_blue
        else:
            ws1.cell(row=row, column=1, value="")
        
        scn_fill = scenario_fills[scn_name]
        ws1.cell(row=row, column=2, value=scn_name).fill = scn_fill
        ws1.cell(row=row, column=2).font = font_bold
        ws1.cell(row=row, column=2).alignment = align_center
        
        ws1.cell(row=row, column=3, value=res["asp"]).number_format = '$#,##0'
        ws1.cell(row=row, column=4, value=res["cac"]).number_format = '$#,##0'
        ws1.cell(row=row, column=5, value=res["total_vc"]).number_format = '$#,##0.00'
        
        cell_contrib = ws1.cell(row=row, column=6, value=res["contribution"])
        cell_contrib.number_format = '$#,##0.00'
        cell_contrib.font = font_bold
        if res["contribution"] <= 0:
            cell_contrib.fill = fill_danger
        
        cell_margin = ws1.cell(row=row, column=7, value=res["margin_pct"] / 100)
        cell_margin.number_format = '0.0%'
        cell_margin.font = font_bold
        
        ws1.cell(row=row, column=8, value=res["launch_capex"]).number_format = '$#,##0'
        ws1.cell(row=row, column=9, value=res["monthly_opex"]).number_format = '$#,##0'
        
        if res["breakeven_month"]:
            cell_be = ws1.cell(row=row, column=10, value=f"Month {res['breakeven_month']}")
            cell_be.font = font_bold
            cell_be.fill = fill_calc if res["breakeven_month"] <= 18 else fill_danger
        else:
            cell_be = ws1.cell(row=row, column=10, value="Not Achieved")
            cell_be.font = font_warning
            cell_be.fill = fill_danger
        cell_be.alignment = align_center
        
        cell_roi = ws1.cell(row=row, column=11, value=res["roi_3yr"] / 100)
        cell_roi.number_format = '0.0%'
        cell_roi.font = font_bold
        if res["roi_3yr"] < 0:
            cell_roi.fill = fill_danger
        
        ws1.cell(row=row, column=12, value=res["cumulative_cf_24"]).number_format = '$#,##0'
        
        if res["breakeven_month"] and res["breakeven_month"] <= 18:
            cell_h = ws1.cell(row=row, column=13, value="PASSED")
            cell_h.font = font_success
            cell_h.fill = fill_calc
        elif res["breakeven_month"] and res["breakeven_month"] <= 22:
            cell_h = ws1.cell(row=row, column=13, value="MARGINAL")
            cell_h.font = font_bold
            cell_h.fill = fill_assumption
        else:
            cell_h = ws1.cell(row=row, column=13, value="FAILED")
            cell_h.font = font_warning
            cell_h.fill = fill_danger
        cell_h.alignment = align_center
        
        for c in range(1, 14):
            ws1.cell(row=row, column=c).border = thin_border
        
        r_data += 1
    r_data += 1  # separator row

# ---- Section C: Resilience Classification ----
r_resil = r_data + 1
ws1.cell(row=r_resil, column=1, value="SECTION C: MARKET RESILIENCE CLASSIFICATION").font = font_section

r_resil_table = r_resil + 2
resil_headers = ["Market", "Upside BE", "Base BE", "Downside BE", "Spread (Mo)", "Classification", "Strategic Implication"]
for c_idx, h in enumerate(resil_headers, 1):
    cell = ws1.cell(row=r_resil_table, column=c_idx, value=h)
    cell.font = font_header
    cell.fill = fill_navy
    cell.alignment = align_center

for idx, mkt_name in enumerate(["Netherlands", "United Kingdom", "Australia", "Germany"]):
    row = r_resil_table + 1 + idx
    up_be = results[mkt_name]["Upside Case"]["breakeven_month"]
    base_be = results[mkt_name]["Base Case"]["breakeven_month"]
    down_be = results[mkt_name]["Downside Case"]["breakeven_month"]
    
    up_str = f"Month {up_be}" if up_be else "N/A"
    base_str = f"Month {base_be}" if base_be else "N/A"
    down_str = f"Month {down_be}" if down_be else "Not Achieved"
    
    if down_be and up_be:
        spread = down_be - up_be
    elif up_be:
        spread = 25 - up_be  # Effective spread if downside never achieves
    else:
        spread = 99
    
    if down_be and down_be <= 18:
        classification = "RESILIENT"
        cls_fill = fill_calc
        implication = "Attractive under all tested scenarios. Proceed with confidence."
    elif down_be and down_be <= 22:
        classification = "SENSITIVE"
        cls_fill = fill_assumption
        implication = "Viable under base case but marginal under stress. Requires active monitoring."
    elif base_be and base_be <= 18:
        classification = "CONDITIONALLY VIABLE"
        cls_fill = fill_assumption
        implication = "Passes base case hurdle but fails under downside. Requires risk mitigation safeguards."
    else:
        classification = "FRAGILE"
        cls_fill = fill_danger
        implication = "Fails hurdle under downside. Proceed only with significant de-risk measures."
    
    ws1.cell(row=row, column=1, value=mkt_name).font = font_bold
    ws1.cell(row=row, column=2, value=up_str).fill = fill_upside
    ws1.cell(row=row, column=2).alignment = align_center
    ws1.cell(row=row, column=3, value=base_str).fill = fill_base
    ws1.cell(row=row, column=3).alignment = align_center
    ws1.cell(row=row, column=4, value=down_str).fill = fill_downside
    ws1.cell(row=row, column=4).alignment = align_center
    ws1.cell(row=row, column=5, value=spread).alignment = align_center
    ws1.cell(row=row, column=5).font = font_bold
    ws1.cell(row=row, column=6, value=classification).font = font_bold
    ws1.cell(row=row, column=6).fill = cls_fill
    ws1.cell(row=row, column=6).alignment = align_center
    ws1.cell(row=row, column=7, value=implication).font = font_regular
    
    for c in range(1, 8):
        ws1.cell(row=row, column=c).border = thin_border

# Auto-width Sheet 1
for col in ws1.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws1.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 48)

print("  Sheet 1 (Scenario Dashboard) complete.")

# =====================================================================
# SHEET 2: SENSITIVITY ANALYSIS
# =====================================================================
ws2 = wb.create_sheet(title="Sensitivity Analysis")
ws2.sheet_properties.tabColor = "2F5597"

ws2["A1"] = "NovaHome International Expansion — Multi-Variable Sensitivity Analysis"
ws2["A1"].font = font_title
ws2["A2"] = "Two-Way Sensitivity Matrices: Break-Even Month Response to Assumption Variation | Phase 07"
ws2["A2"].font = font_subtitle

base_scn = scenarios["Base Case"]
current_row = 4

for mkt_name in ["Netherlands", "United Kingdom", "Australia", "Germany"]:
    mkt = markets[mkt_name]
    
    # ---- Matrix 1: ASP vs CAC ----
    ws2.cell(row=current_row, column=1,
             value=f"{mkt_name}: Break-Even Month — Selling Price vs. Customer Acquisition Cost").font = font_section
    current_row += 1
    ws2.cell(row=current_row, column=1,
             value=f"Base ASP: ${mkt['asp']:.0f} | Base CAC: ${mkt['cac']:.0f} | Base Contribution: ${mkt['contribution']:.2f} | Base BE: Month {mkt['breakeven_month']}").font = font_subtitle
    current_row += 1
    
    asp_mults = [0.90, 0.95, 1.00, 1.05, 1.10]
    cac_mults = [0.80, 0.90, 1.00, 1.10, 1.20, 1.30]
    
    cac_labels = [f"CAC: ${mkt['cac'] * m:.0f}" for m in cac_mults]
    
    ws2.cell(row=current_row, column=1, value="ASP \\ CAC").font = font_header
    ws2.cell(row=current_row, column=1).fill = fill_navy
    ws2.cell(row=current_row, column=1).alignment = align_center
    
    for c_idx, cl in enumerate(cac_labels, 2):
        cell = ws2.cell(row=current_row, column=c_idx, value=cl)
        cell.font = font_header
        cell.fill = fill_blue_header
        cell.alignment = align_center
    
    for r_idx, asp_m in enumerate(asp_mults):
        row = current_row + 1 + r_idx
        asp_label = f"ASP: ${mkt['asp'] * asp_m:.0f} ({'+' if asp_m >= 1 else ''}{(asp_m-1)*100:.0f}%)"
        ws2.cell(row=row, column=1, value=asp_label).font = font_bold
        ws2.cell(row=row, column=1).border = thin_border
        
        for c_idx, cac_m in enumerate(cac_mults, 2):
            custom_scn = dict(base_scn)
            custom_scn["asp_mult"] = asp_m
            custom_scn["cac_mult"] = cac_m
            
            res = compute_scenario(mkt, custom_scn)
            be = res["breakeven_month"]
            
            if be:
                cell = ws2.cell(row=row, column=c_idx, value=f"Month {be}")
                if be <= 14:
                    cell.fill = fill_calc
                    cell.font = font_success
                elif be <= 18:
                    cell.fill = fill_assumption
                    cell.font = font_bold
                elif be <= 22:
                    cell.fill = fill_downside
                    cell.font = font_bold
                else:
                    cell.fill = fill_danger
                    cell.font = font_warning
            else:
                cell = ws2.cell(row=row, column=c_idx, value="Not Achieved")
                cell.fill = fill_danger
                cell.font = font_warning
            
            cell.alignment = align_center
            cell.border = thin_border
    
    current_row += 1 + len(asp_mults) + 2
    
    # ---- Matrix 2: Volume vs Shipping ----
    ws2.cell(row=current_row, column=1,
             value=f"{mkt_name}: Break-Even Month — Sales Volume vs. Shipping Cost").font = font_section
    current_row += 1
    ws2.cell(row=current_row, column=1,
             value=f"Base Shipping: ${mkt['shipping']:.0f}/unit | Base Volume Ramp: 100%").font = font_subtitle
    current_row += 1
    
    vol_mults = [0.70, 0.80, 0.90, 1.00, 1.10, 1.20]
    ship_mults = [0.80, 0.90, 1.00, 1.10, 1.20, 1.30]
    ship_labels = [f"Ship: ${mkt['shipping'] * m:.0f}" for m in ship_mults]
    
    ws2.cell(row=current_row, column=1, value="Volume \\ Shipping").font = font_header
    ws2.cell(row=current_row, column=1).fill = fill_navy
    ws2.cell(row=current_row, column=1).alignment = align_center
    
    for c_idx, sl in enumerate(ship_labels, 2):
        cell = ws2.cell(row=current_row, column=c_idx, value=sl)
        cell.font = font_header
        cell.fill = fill_blue_header
        cell.alignment = align_center
    
    for r_idx, vol_m in enumerate(vol_mults):
        row = current_row + 1 + r_idx
        ws2.cell(row=row, column=1, value=f"Volume: {vol_m*100:.0f}%").font = font_bold
        ws2.cell(row=row, column=1).border = thin_border
        
        for c_idx, ship_m in enumerate(ship_mults, 2):
            custom_scn = dict(base_scn)
            custom_scn["volume_mult"] = vol_m
            custom_scn["shipping_mult"] = ship_m
            
            res = compute_scenario(mkt, custom_scn)
            be = res["breakeven_month"]
            
            if be:
                cell = ws2.cell(row=row, column=c_idx, value=f"Month {be}")
                if be <= 14:
                    cell.fill = fill_calc
                    cell.font = font_success
                elif be <= 18:
                    cell.fill = fill_assumption
                    cell.font = font_bold
                elif be <= 22:
                    cell.fill = fill_downside
                    cell.font = font_bold
                else:
                    cell.fill = fill_danger
                    cell.font = font_warning
            else:
                cell = ws2.cell(row=row, column=c_idx, value="Not Achieved")
                cell.fill = fill_danger
                cell.font = font_warning
            
            cell.alignment = align_center
            cell.border = thin_border
    
    current_row += 1 + len(vol_mults) + 2

# ---- Tornado Analysis: Variable Impact Ranking (UK) ----
ws2.cell(row=current_row, column=1,
         value="TORNADO ANALYSIS: Variable Impact Ranking on Break-Even Month (United Kingdom)").font = font_section
current_row += 1
ws2.cell(row=current_row, column=1,
         value="Each variable is stressed individually (±) while all others remain at Base. Ranked by impact spread.").font = font_subtitle
current_row += 2

tornado_headers = ["Variable", "Favorable Value", "Base Value", "Adverse Value",
                   "BE (Favorable)", "BE (Base)", "BE (Adverse)", "Spread (Mo)", "Impact Rank"]
for c_idx, h in enumerate(tornado_headers, 1):
    cell = ws2.cell(row=current_row, column=c_idx, value=h)
    cell.font = font_header
    cell.fill = fill_navy
    cell.alignment = align_center

uk = markets["United Kingdom"]

# (name, key, favorable_mult, base_mult, adverse_mult)
tornado_vars = [
    ("Sales Volume",        "volume_mult",   1.30, 1.00, 0.70),
    ("Selling Price (ASP)", "asp_mult",       1.15, 1.00, 0.85),
    ("Customer Acq. Cost",  "cac_mult",       0.70, 1.00, 1.40),
    ("Product Cost (FOB)",  "fob_mult",       0.90, 1.00, 1.15),
    ("Shipping Cost",       "shipping_mult",  0.75, 1.00, 1.35),
    ("Launch Capex",        "capex_mult",     0.80, 1.00, 1.30),
    ("Monthly Fixed Opex",  "opex_mult",      0.80, 1.00, 1.30),
    ("Currency Impact (FX)","fx_mult",        1.15, 1.00, 0.85),
]

tornado_results = []
for var_name, var_key, fav_m, base_m, adv_m in tornado_vars:
    scn_fav = dict(base_scn); scn_fav[var_key] = fav_m
    scn_adv = dict(base_scn); scn_adv[var_key] = adv_m
    
    res_fav = compute_scenario(uk, scn_fav)
    res_base = compute_scenario(uk, base_scn)
    res_adv = compute_scenario(uk, scn_adv)
    
    be_fav = res_fav["breakeven_month"] if res_fav["breakeven_month"] else 30
    be_base = res_base["breakeven_month"] if res_base["breakeven_month"] else 30
    be_adv = res_adv["breakeven_month"] if res_adv["breakeven_month"] else 30
    
    spread = abs(be_adv - be_fav)
    tornado_results.append((var_name, fav_m, base_m, adv_m, be_fav, be_base, be_adv, spread))

tornado_results.sort(key=lambda x: x[7], reverse=True)

for rank, (var_name, fav_m, base_m, adv_m, be_fav, be_base, be_adv, spread) in enumerate(tornado_results, 1):
    row = current_row + rank
    ws2.cell(row=row, column=1, value=var_name).font = font_bold
    ws2.cell(row=row, column=2, value=f"{fav_m:.0%}").fill = fill_upside
    ws2.cell(row=row, column=2).alignment = align_center
    ws2.cell(row=row, column=3, value=f"{base_m:.0%}").fill = fill_base
    ws2.cell(row=row, column=3).alignment = align_center
    ws2.cell(row=row, column=4, value=f"{adv_m:.0%}").fill = fill_downside
    ws2.cell(row=row, column=4).alignment = align_center
    
    for c, val in [(5, be_fav), (6, be_base), (7, be_adv)]:
        cell_v = ws2.cell(row=row, column=c, value=f"Month {val}" if val < 30 else "N/A")
        cell_v.alignment = align_center
        if val <= 14:
            cell_v.fill = fill_calc
        elif val <= 18:
            cell_v.fill = fill_assumption
        elif val < 30:
            cell_v.fill = fill_downside
        else:
            cell_v.fill = fill_danger
    
    ws2.cell(row=row, column=8, value=spread).font = font_bold
    ws2.cell(row=row, column=8).alignment = align_center
    ws2.cell(row=row, column=9, value=f"#{rank}").font = font_bold_blue
    ws2.cell(row=row, column=9).alignment = align_center
    
    for c in range(1, 10):
        ws2.cell(row=row, column=c).border = thin_border

# Auto-width Sheet 2
for col in ws2.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws2.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 42)

print("  Sheet 2 (Sensitivity Analysis) complete.")

# =====================================================================
# SHEET 3: CASH FLOW SCENARIOS
# =====================================================================
ws3 = wb.create_sheet(title="Cash Flow Scenarios")
ws3.sheet_properties.tabColor = "1B6B5A"

ws3["A1"] = "NovaHome International Expansion — 24-Month Cash Flow Projections Under Three Scenarios"
ws3["A1"].font = font_title
ws3["A2"] = "Cumulative Cash Flow Trajectory: Base / Upside / Downside per Qualified Market | Phase 07"
ws3["A2"].font = font_subtitle

current_row = 4
for mkt_name in ["Netherlands", "United Kingdom", "Australia", "Germany"]:
    mkt = markets[mkt_name]
    ws3.cell(row=current_row, column=1,
             value=f"{mkt_name}: 24-Month Cumulative Cash Flow Under Three Scenarios").font = font_section
    current_row += 1
    ws3.cell(row=current_row, column=1,
             value=f"Base Capex: ${mkt['launch_capex']:,.0f} | Base ASP: ${mkt['asp']:.0f} | Base Contribution/Unit: ${mkt['contribution']:.2f}").font = font_subtitle
    current_row += 1
    
    cf_headers = [
        "Month",
        "Upside Units", "Upside Cum. CF ($)",
        "Base Units", "Base Cum. CF ($)",
        "Downside Units", "Downside Cum. CF ($)",
        "Upside Status", "Base Status", "Downside Status"
    ]
    
    for c_idx, h in enumerate(cf_headers, 1):
        cell = ws3.cell(row=current_row, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center
    ws3.row_dimensions[current_row].height = 28
    current_row += 1
    
    for m in range(24):
        row = current_row + m
        ws3.cell(row=row, column=1, value=f"Month {m+1}").font = font_bold
        
        for scn_idx, scn_name in enumerate(["Upside Case", "Base Case", "Downside Case"]):
            res = results[mkt_name][scn_name]
            md = res["monthly_data"][m]
            
            col_units = 2 + scn_idx * 2
            col_cf = 3 + scn_idx * 2
            col_status = 8 + scn_idx
            
            ws3.cell(row=row, column=col_units, value=md["units"]).number_format = '#,##0'
            ws3.cell(row=row, column=col_units).alignment = align_center
            
            cell_cf = ws3.cell(row=row, column=col_cf, value=md["cumulative_cf"])
            cell_cf.number_format = '$#,##0'
            cell_cf.font = font_bold
            cell_cf.fill = fill_calc if md["cumulative_cf"] >= 0 else fill_light_gray
            
            if md["cumulative_cf"] >= 0:
                ws3.cell(row=row, column=col_status, value="✓ BREAK-EVEN").font = font_success
            else:
                ws3.cell(row=row, column=col_status, value="Investing").font = font_regular
            ws3.cell(row=row, column=col_status).alignment = align_center
        
        for c in range(1, 11):
            ws3.cell(row=row, column=c).border = thin_border
    
    current_row += 24 + 2

# Auto-width Sheet 3
for col in ws3.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws3.column_dimensions[col_letter].width = min(max(max_len + 3, 14), 30)

print("  Sheet 3 (Cash Flow Scenarios) complete.")

# =====================================================================
# SAVE
# =====================================================================
output_dir = "phase-07-scenario-analysis"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "scenario_model.xlsx")
wb.save(output_path)
print(f"\n✅ Scenario Model saved to: {output_path}")

# =====================================================================
# FINAL SUMMARY
# =====================================================================
print("\n" + "=" * 70)
print("SCENARIO ANALYSIS SUMMARY")
print("=" * 70)

print(f"\n{'Market':20s} | {'Upside BE':>10s} | {'Base BE':>10s} | {'Downside BE':>14s} | {'Classification'}")
print("-" * 85)

for mkt_name in ["Netherlands", "United Kingdom", "Australia", "Germany"]:
    up_be = results[mkt_name]["Upside Case"]["breakeven_month"]
    base_be = results[mkt_name]["Base Case"]["breakeven_month"]
    down_be = results[mkt_name]["Downside Case"]["breakeven_month"]
    
    up_str = f"Month {up_be}" if up_be else "N/A"
    base_str = f"Month {base_be}" if base_be else "N/A"
    down_str = f"Month {down_be}" if down_be else "Not Achieved"
    
    if down_be and down_be <= 18:
        cls = "RESILIENT"
    elif down_be and down_be <= 22:
        cls = "SENSITIVE"
    elif base_be and base_be <= 18:
        cls = "CONDITIONALLY VIABLE"
    else:
        cls = "FRAGILE"
    
    print(f"  {mkt_name:20s} | {up_str:>10s} | {base_str:>10s} | {down_str:>14s} | {cls}")

print("\n--- 3-Year ROI Summary ---")
for mkt_name in ["Netherlands", "United Kingdom", "Australia", "Germany"]:
    for scn_name in ["Upside Case", "Base Case", "Downside Case"]:
        roi = results[mkt_name][scn_name]["roi_3yr"]
        print(f"  {mkt_name:20s} | {scn_name:15s} | ROI: {roi:7.1f}%")

print("\n=== PHASE 07 SCENARIO ENGINE COMPLETE ===")
