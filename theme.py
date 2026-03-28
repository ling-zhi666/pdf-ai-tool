# d:/Pdf_ai_tool/theme.py
"""Theme system for PDF AI Tool - supports light/dark mode toggle."""

# Light Theme Colors
LIGHT_THEME = {
    "PRIMARY": "#165DFF",
    "ACCENT": "#FF7D00",
    "SUCCESS": "#00B42A",
    "WARNING": "#FF9A2E",
    "ERROR": "#F53F3F",
    "BG_WINDOW": "#F5F7FA",
    "BG_CARD": "#FFFFFF",
    "BG_LIST_EVEN": "#F9FAFC",
    "BG_HOVER": "#E8F3FF",
    "TEXT_PRIMARY": "#1D2129",
    "TEXT_SECONDARY": "#4E5969",
    "TEXT_TERTIARY": "#86909C",
    "BORDER": "#E5E6EB",
}

# Dark Theme Colors
DARK_THEME = {
    "PRIMARY": "#4080FF",
    "ACCENT": "#FF9D4D",
    "SUCCESS": "#23C343",
    "WARNING": "#FFB84D",
    "ERROR": "#FF7875",
    "BG_WINDOW": "#1D2129",
    "BG_CARD": "#252B33",
    "BG_LIST_EVEN": "#2A313A",
    "BG_HOVER": "#363D47",
    "TEXT_PRIMARY": "#E8ECF0",
    "TEXT_SECONDARY": "#A6C0E0",
    "TEXT_TERTIARY": "#6B8BAD",
    "BORDER": "#3D4654",
}

# Current theme state
_current_theme = "light"

def get_current_theme():
    """Return current theme name."""
    return _current_theme

def get_colors():
    """Return current theme color dictionary."""
    return LIGHT_THEME if _current_theme == "light" else DARK_THEME

def toggle_theme():
    """Toggle between light and dark theme. Returns new theme name."""
    global _current_theme
    _current_theme = "dark" if _current_theme == "light" else "light"
    return _current_theme

def is_dark():
    """Return True if dark mode is active."""
    return _current_theme == "dark"