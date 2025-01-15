from datetime import datetime

def format_timestamp(timestamp: int, date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Convert a Unix timestamp to a formatted date string."""
    try:
        return datetime.fromtimestamp(timestamp).strftime(date_format)
    except Exception as e:
        return f"Invalid timestamp: {timestamp} ({e})"

def format_percentage(value: float) -> str:
    """Format a float as a percentage."""
    try:
        return f"{value * 100:.2f}%"
    except Exception as e:
        return f"Invalid percentage: {value} ({e})"

def format_currency(value: float, currency_symbol: str = "$") -> str:
    """Format a float as a currency."""
    try:
        return f"{currency_symbol}{value:,.2f}"
    except Exception as e:
        return f"Invalid currency value: {value} ({e})"
