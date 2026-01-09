import re

def normalize_text(text):
    """
    OCR-safe, context-aware normalizer.
    Fixes numeric OCR errors without destroying words, times, or dates.
    """

    # Join list input
    if isinstance(text, list):
        text = "\n".join(t for t in text if t)
    elif not isinstance(text, str):
        return ""

    text = text.upper()

    #  Basic cleanup
    text = text.replace("—", "-").replace("~", "")
    text = re.sub(r"[ \t]+", " ", text)

    #  Fix known OCR keyword errors
    text = re.sub(r"\bSUBT0TA\b", "SUBTOTAL", text)
    text = re.sub(r"\bT0TAL\b", "TOTAL", text)
    text = re.sub(r"\bTOTAI\b", "TOTAL", text)

    #  Normalize currency spacing
    text = re.sub(r"(\$|₹|€|£)\s+(\d)", r"\1\2", text)

    #  PROTECT TIME VALUES (DO NOT TOUCH THESE)

    TIME_PLACEHOLDER = "__TIME__"
    times = {}

    def protect_time(match):
        key = f"{TIME_PLACEHOLDER}{len(times)}__"
        times[key] = match.group(0)
        return key

    # Protect 10:20, 15:39:12, 10.20 AM
    text = re.sub(
        r"\b\d{1,2}[:.]\d{2}([:.]\d{2})?\s*(AM|PM)?\b",
        protect_time,
        text
    )

    # FIX 1: split decimals (money only)
    # $4 55 | 4 55 | ₹12 99

    text = re.sub(
        r"(?<!\w)(\$|₹|€|£)?(\d{1,4})\s+(\d{2})(?!\w)",
        r"\1\2.\3",
        text
    )

    # FIX 2: comma decimal (not thousand separators)
    # 4,55 | 12,99

    text = re.sub(
        r"(?<!\d)(\d{1,4}),(\d{2})(?!\d)",
        r"\1.\2",
        text
    )

    # FIX 3: OCR O/I → 0/1 ONLY in numeric tokens
    # AND only if token has at most ONE decimal

    def fix_ocr_digits(match):
        token = match.group(0)

        # Skip if token already looks invalid (15.39.12)
        if token.count(".") > 1:
            return token

        return (
            token.replace("O", "0")
                 .replace("I", "1")
        )

    text = re.sub(
        r"\b\d+[A-Z0-9.]*\b",
        fix_ocr_digits,
        text
    )

    # RESTORE TIME VALUES

    for key, value in times.items():
        text = text.replace(key, value)

    #  Clean empty lines
    text = "\n".join(
        line.strip() for line in text.splitlines() if line.strip()
    )

    return text
