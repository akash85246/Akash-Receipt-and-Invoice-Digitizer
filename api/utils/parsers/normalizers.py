import re

def normalize_text(text):
    """
    OCR-safe, context-aware normalizer.
    Fixes numeric OCR errors without destroying words.
    """

    # Join list input
    if isinstance(text, list):
        text = "\n".join(t for t in text if t)
    elif not isinstance(text, str):
        return ""

    text = text.upper()

    # --- Basic cleanup ---
    text = text.replace("—", "-").replace("~", "")
    text = re.sub(r"[ \t]+", " ", text)

    # --- Fix known OCR keyword errors ---
    text = re.sub(r"\bSUBT0TA\b", "SUBTOTAL", text)
    text = re.sub(r"\bT0TAL\b", "TOTAL", text)
    text = re.sub(r"\bTOTAI\b", "TOTAL", text)

    # --- Normalize currency spacing ---
    text = re.sub(r"(\$|₹|€|£)\s+(\d)", r"\1\2", text)

    # --- FIX 1: split decimals (ONLY numeric context) ---
    # Matches: $4 55 | 4 55 | ₹12 99
    text = re.sub(
        r"(?<!\w)(\$|₹|€|£)?(\d{1,4})\s+(\d{2})(?!\w)",
        r"\1\2.\3",
        text
    )

    # --- FIX 2: comma decimal (ONLY decimal commas) ---
    # Matches: 4,55 | 12,99  (not 1,234)
    text = re.sub(
        r"(?<!\d)(\d{1,4}),(\d{2})(?!\d)",
        r"\1.\2",
        text
    )

    # --- FIX 3: OCR 0/O and 1/I ONLY inside numeric tokens ---
    # Example: T0TAL → TOTAL, 2O.50 → 20.50

    def fix_ocr_digits(match):
        token = match.group(0)
        return (
            token.replace("O", "0")
                 .replace("I", "1")
        )

    text = re.sub(
        r"\b[A-Z]*\d+[A-Z0-9.]*\b",
        fix_ocr_digits,
        text
    )

    # --- Clean empty lines ---
    text = "\n".join(
        line.strip() for line in text.splitlines() if line.strip()
    )

    return text