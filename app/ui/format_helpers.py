def format_currency(value):

    suffixes = [
        (10**12, 'T'),
        (10**9, 'B'),
        (10**6, 'M'),
        (10**3, 'K') # Added K for completeness
    ]
    
    for limit, suffix in suffixes:
        if abs(value) >= limit:
            # Divide and format to 2 decimal places
            return f"${value / limit:.2f}{suffix}"
            
    # Return as-is if it's smaller than 1000
    return f"${value:,.0f}"

def format_percent(value):
    return f"{value:.1f}%"

def format_score(value):
    return f"{value:.2f}"