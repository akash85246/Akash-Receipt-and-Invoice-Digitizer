import re
from datetime import datetime
from decimal import Decimal
from .line_items import extract_line_items
from .currency import extract_currency
from .address import extract_address
from .categorizer import auto_classify_category
from .confidence import weighted_value
from .expense_type import classify_expense_type
from .patterns import DATE_PATTERNS, AMOUNT_PATTERNS, MERCHANT_BLACKLIST,  GST_WITH_LABEL, GST_PATTERN_STRICT
from .normalizers import normalize_text
from .tax import extract_tax_amount, extract_subtotal, extract_total


def extract_date(text):
    text = normalize_text(text)
    for pattern in DATE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            try:
                return datetime.strptime(
                    match.group(1).replace("-", "/"),
                    "%d/%m/%Y"
                ).date()
            except ValueError:
                pass
    return None


def extract_total_amount(text):
    text = normalize_text(text)

    for pattern in AMOUNT_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return Decimal(match.group(1))
            except Exception:
                continue

    return None


def extract_merchant_name(text):
    text = normalize_text(text)

    lines = [
        l.strip()
        for l in text.splitlines()
        if l.strip() and len(l.strip()) > 2
    ]

    for line in lines[:5]:
        lower = line.lower()
        if any(bad in lower for bad in MERCHANT_BLACKLIST):
            continue
        cleaned = re.sub(r"(#\d+|store\s*\d+)", "", line, flags=re.IGNORECASE)
        cleaned = re.sub(r"[^\w\s&.-]", "", cleaned)

        cleaned = cleaned.strip()
        if 3 <= len(cleaned) <= 50:
            return cleaned[:255]

    return None


def extract_gst_number(text):
    text = normalize_text(text).upper()

    # Prefer GST with label (HIGH confidence)
    labeled_match = re.search(GST_WITH_LABEL, text)
    if labeled_match:
        return labeled_match.group(1)

    # raw GSTIN pattern (MEDIUM confidence)
    raw_match = re.search(GST_PATTERN_STRICT, text)
    if raw_match:
        return raw_match.group(0)

    return None



def base_document_data(text,ocr_confidence):
    """
    Shared fields for ALL documents
    """
    text = normalize_text(text)
    document_total = extract_total_amount(text) or extract_subtotal(text) or Decimal("0.00")
    
    return {
        "merchant_name": extract_merchant_name(text),
        "date": extract_date(text),
        "total_amount": extract_total_amount(text),
        "gst_number": extract_gst_number(text),
        "currency": extract_currency(text),
        "address": extract_address(text),
        "items": extract_line_items(text,document_total),
        "category": auto_classify_category(text),
        "confidence_score": weighted_value(text),
        "subtotal": extract_subtotal(text),
        "tax_amount": extract_tax_amount(
            text,
            subtotal=extract_subtotal(text),
            total=extract_total(text)
        ),
    }
