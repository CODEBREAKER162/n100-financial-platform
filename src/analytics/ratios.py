def calculate_debt_to_equity(total_debt, total_equity):
    if total_equity == 0:
        raise ValueError('Total equity cannot be zero')
    return total_debt / total_equity

def calculate_quick_ratio(cash, marketable_securities, receivables, current_liabilities):
    if current_liabilities == 0:
        raise ValueError('Current liabilities cannot be zero')
    return (cash + marketable_securities + receivables) / current_liabilities
