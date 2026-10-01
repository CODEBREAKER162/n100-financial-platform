-- Exploratory Queries for NIFTY 100 Financial Intelligence Platform
SELECT company_id, roe, debt_to_equity FROM financial_ratios ORDER BY roe DESC LIMIT 10;
SELECT sector, AVG(pat_margin) AS avg_pat_margin FROM financial_ratios GROUP BY sector;
