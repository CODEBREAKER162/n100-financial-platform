def clean_financial_data(data: dict) -> dict:
    cleaned = data.copy()
    if "amount" in cleaned and isinstance(cleaned["amount"], str):
        cleaned["amount"] = float(cleaned["amount"].replace("$", "").replace(",", "").strip())
    return cleaned
