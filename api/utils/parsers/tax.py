import re
from decimal import Decimal
from .normalizers import normalize_text
from .patterns import SUBTOTAL_PATTERNS, TAX_AMOUNT_PATTERNS, TAX_PERCENT_PATTERNS, TOTAL_PATTERNS


def extract_subtotal(text):
    text = normalize_text(text)

    for pattern in SUBTOTAL_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None


def extract_total(text):
    text = normalize_text(text)

    for pattern in TOTAL_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None


def extract_tax_amount(text, subtotal=None, total=None):
    text = normalize_text(text)

    # Explicit tax amount
    for pattern in TAX_AMOUNT_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return match.group(1).strip()
            except Exception:
                pass

    # Percentage-based tax
    if subtotal:
        for pattern in TAX_PERCENT_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    percent = Decimal(match.group(1))
                    return (subtotal * percent / Decimal("100")).quantize(
                        Decimal("0.01")
                    )
                except Exception:
                    pass

    # Derived tax ONLY if meaningful
    if subtotal is not None and total is not None:
        try:
            tax = total - subtotal

            # IMPORTANT FIX
            if tax > Decimal("0.01"):
                return tax.quantize(Decimal("0.01"))

        except Exception:
            pass

    # No tax evidence
    return None
