def compute_pe_ratio(price: float, eps: float) -> float:
    if eps <= 0:
        raise ValueError("EPS must be greater than zero")
    return round(price / eps, 2)


def compute_pb_ratio(price: float, book_value_per_share: float) -> float:
    if book_value_per_share <= 0:
        raise ValueError("Book value per share must be greater than zero")
    return round(price / book_value_per_share, 2)


def compute_roe(net_income: float, shareholder_equity: float) -> float:
    if shareholder_equity <= 0:
        raise ValueError("Shareholder equity must be greater than zero")
    return round((net_income / shareholder_equity) * 100, 2)


def calculate_debt_to_equity(total_debt: float, total_equity: float) -> float:
    if total_equity == 0:
        raise ValueError("Total equity cannot be zero.")
    return round(total_debt / total_equity, 4)


def calculate_quick_ratio(
    cash: float,
    marketable_securities: float,
    receivables: float,
    current_liabilities: float,
) -> float:
    if current_liabilities == 0:
        raise ValueError("Current liabilities cannot be zero.")

    quick_assets = cash + marketable_securities + receivables
    return round(quick_assets / current_liabilities, 4)
