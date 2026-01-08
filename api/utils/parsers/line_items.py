import re
from decimal import Decimal, InvalidOperation
from .normalizers import normalize_text
from .patterns import LINE_ITEM_PATTERNS, NON_ITEM_KEYWORDS, REFERENCE_PREFIXES


def classify_line(line: str) -> str:
    l = line.lower()

    if any(k in l for k in ["total", "subtotal", "change due"]):
        return "total"

    if any(k in l for k in ["mastercard", "visa", "upi", "cash"]):
        return "payment"

    if re.search(r"\d{2}/\d{2}/\d{4}", l):
        return "date"

    if re.search(r"\$\s*\d", l) or re.search(r"\d+\.\d{2}", l):
        return "amount"

    return "text"


def is_reference_line(line: str) -> bool:
    first = line.lower().split()[0]
    return first in REFERENCE_PREFIXES

def is_valid_item_name(name: str) -> bool:
    n = name.lower().strip()

    if any(k in n for k in NON_ITEM_KEYWORDS):
        return False

    if len(n) < 3:
        return False

    alpha_ratio = sum(c.isalpha() for c in n) / max(len(n), 1)
    if alpha_ratio < 0.4:
        return False

    if re.search(r"\d{4,}", n):
        return False

    return True


def safe_decimal(value):
    """Safely convert OCR price to Decimal or return None"""
    if not value:
        return None

    try:
        value = value.replace(",", ".")
        return Decimal(value)
    except (InvalidOperation, AttributeError):
        return None
    
def price_sanity_check(price, total):
    if total is None:
        return True

    # item cannot exceed total by more than 50%
    return price <= total * Decimal("1.5")

def strong_item_name(name: str) -> bool:
    letters = sum(c.isalpha() for c in name)
    digits = sum(c.isdigit() for c in name)

    return letters >= 4 and letters > digits

def extract_line_items(text, document_total=None):
    text = normalize_text(text)
    items = []


    for raw in text.splitlines():
        raw = raw.strip()
        if not raw:
            continue
       
        
        line_type = classify_line(raw)

        # hard reject non-item lines
        if line_type in {"total", "payment", "date"}:
            continue

        if any(k in raw.lower() for k in NON_ITEM_KEYWORDS):
            continue

        for pattern in LINE_ITEM_PATTERNS:
            match = re.search(pattern, raw, re.VERBOSE)
            if not match:
                continue

            name = match.group("name").strip()
            if not is_valid_item_name(name):
                continue

            price = safe_decimal(match.groupdict().get("price"))
            if price is None:
                continue
            
            if is_reference_line(raw):
                continue
            if not price_sanity_check(price, document_total):
                continue
            if not strong_item_name(name):
                continue


            qty_raw = match.groupdict().get("qty")
            qty = int(qty_raw) if qty_raw and qty_raw.isdigit() else 1

            items.append({
                "name": name[:255],
                "quantity": qty,
                "unit_price": price,
                "total_price": price * qty,
                "source_line": raw,
            })
            break

    return items