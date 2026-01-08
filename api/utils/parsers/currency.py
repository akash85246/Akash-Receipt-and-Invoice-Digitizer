from .patterns import CURRENCY_SYMBOLS, CURRENCY_WORD_PATTERNS
from .normalizers import normalize_text
import re


def extract_currency(text: str) -> str | None:
    text = normalize_text(text)

    # Strong detection: symbol followed by number (even broken)
    for symbol, code in CURRENCY_SYMBOLS.items():
        if re.search(rf"{re.escape(symbol)}\s*\d", text):
            return code

    # Symbol anywhere near amount
    for symbol, code in CURRENCY_SYMBOLS.items():
        if symbol in text:
            return code

    # Word / ISO fallback
    lower = text.lower()
    for pattern, code in CURRENCY_WORD_PATTERNS.items():
        if re.search(pattern, lower):
            return code

    return None