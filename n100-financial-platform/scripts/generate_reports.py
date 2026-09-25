import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
import pandas as pd
from src.screener.engine import screen_stocks
from src.screener.pdf_generator import generate_pdf_report

def run_batch_export():
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)
    
    print("[*] Running Screener Engine...")
    results = screen_stocks()
    df = pd.DataFrame(results)
    
    csv_path = output_dir / "nifty100_summary.csv"
    pdf_path = output_dir / "nifty100_summary.pdf"
    
    # Save CSV
    df.to_csv(csv_path, index=False)
    print(f"[+] Saved CSV Report to {csv_path}")
    
    # Save PDF
    pdf_bytes = generate_pdf_report(df)
    with open(pdf_path, "wb") as f:
        f.write(pdf_bytes)
    print(f"[+] Saved PDF Report to {pdf_path}")
    print("[✓] Batch Export Completed Successfully!")

if __name__ == "__main__":
    run_batch_export()
