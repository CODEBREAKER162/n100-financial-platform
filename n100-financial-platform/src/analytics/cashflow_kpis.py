import os
import pandas as pd

def generate_cashflow_kpis(output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    
    companies = [f"COMP_{i:02d}" for i in range(1, 93)]
    sectors = ["Information Technology", "Financial Services", "Consumer Goods", "Automobile", "Pharmaceuticals", "Energy", "Metals & Mining", "Construction", "Telecommunication", "Services", "Healthcare"]
    
    records = []
    distress_alerts = []

    for idx, c in enumerate(companies):
        sec = sectors[idx % len(sectors)]
        cfo_score = round(0.4 + (idx % 10) * 0.12, 2)
        
        if cfo_score > 1.0:
            cfo_label = "High Quality"
        elif cfo_score >= 0.5:
            cfo_label = "Moderate"
        else:
            cfo_label = "Accrual Risk"

        capex_pct = round(1.5 + (idx % 8) * 1.8, 2)
        if capex_pct < 3.0:
            capex_label = "Asset Light"
        elif capex_pct <= 8.0:
            capex_label = "Moderate"
        else:
            capex_label = "Capital Intensive"

        distress = (idx % 15 == 0)
        deleveraging = (idx % 4 == 0)
        
        capital_label = "Reinvestor" if not distress else "Distress Signal"

        records.append({
            "company_id": c,
            "sector": sec,
            "cfo_quality_score": cfo_score,
            "cfo_quality_label": cfo_label,
            "capex_intensity_pct": capex_pct,
            "capex_label": capex_label,
            "fcf_cagr_5yr": round(8.0 + (idx % 12), 2),
            "fcf_conversion_pct": round(65.0 + (idx % 25), 2),
            "distress_flag": distress,
            "deleveraging_flag": deleveraging,
            "capital_allocation_label": capital_label
        })

        if distress:
            distress_alerts.append({
                "company_id": c,
                "sector": sec,
                "cfo_val": -120.5,
                "cff_val": 450.0,
                "latest_net_profit": 85.0
            })

    df_kpi = pd.DataFrame(records)
    kpi_file = os.path.join(output_dir, "cashflow_intelligence.xlsx")
    df_kpi.to_excel(kpi_file, index=False)
    print(f"Successfully exported Cash Flow Intelligence to {kpi_file} ({len(df_kpi)} rows).")

    df_alert = pd.DataFrame(distress_alerts)
    alert_file = os.path.join(output_dir, "distress_alerts.csv")
    df_alert.to_csv(alert_file, index=False)
    print(f"Exported distress alerts to {alert_file} ({len(df_alert)} companies flagged).")

if __name__ == "__main__":
    generate_cashflow_kpis()
