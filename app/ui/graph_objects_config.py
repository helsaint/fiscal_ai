RISK_COLORS = {
    "high": "#8B0000",        # deep red
    "moderate": "#C67C00",    # restrained amber
    "low": "#1B5E20"          # deep green
}

STABILITY_COLOR = {
    "watch": "#8B0000",
    "stable": "#C67C00",
    "strong": "#1B5E20"
}

def fiscal_classify_band(value):
    if value < 0.4:
        return "Stable", "#2E7D32"      # muted institutional green
    elif value < 0.6:
        return "Elevated", "#F9A825"    # restrained amber
    elif value < 0.75:
        return "High", "#EF6C00"        # controlled orange
    else:
        return "Critical", "#C62828"    # institutional red