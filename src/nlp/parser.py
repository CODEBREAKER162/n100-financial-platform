import os
import re
import pandas as pd

def parse_analysis_text(input_file="data/analysis.xlsx", output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    xls = pd.ExcelFile(input_file)
    parsed_records = []
    failures = []

    pattern = re.compile(r"(\d+)\s*Years?:?\s*([\d.]+)%")

    target_fields = [
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe"
    ]

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        company_id = sheet_name

        for field in target_fields:
            if field in df.columns:
                for text_entry in df[field].dropna():
                    text_str = str(text_entry)
                    matches = pattern.findall(text_str)
                    
                    if matches:
                        for period, value in matches:
                            parsed_records.append({
                                "company_id": company_id,
                                "metric_type": field,
                                "period_years": int(period),
                                "value_pct": float(value)
                            })
                    else:
                        failures.append({
                            "company_id": company_id,
                            "metric_type": field,
                            "raw_text": text_str
                        })

    df_parsed = pd.DataFrame(parsed_records)
    parsed_csv = os.path.join(output_dir, "analysis_parsed.csv")
    df_parsed.to_csv(parsed_csv, index=False)
    print(f"Successfully saved parsed data to {parsed_csv} ({len(df_parsed)} records).")

    df_failures = pd.DataFrame(failures)
    failures_csv = os.path.join(output_dir, "parse_failures.csv")
    df_failures.to_csv(failures_csv, index=False)
    print(f"Logged parse failures to {failures_csv} ({len(df_failures)} entries).")

if __name__ == "__main__":
    parse_analysis_text()
