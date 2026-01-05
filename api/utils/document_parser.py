import re
from datetime import datetime
from decimal import Decimal


DATE_PATTERNS = [
    r"\b(\d{2}/\d{2}/\d{4})\b",
    r"\b(\d{2}-\d{2}-\d{4})\b",
    r"\b(\d{4}-\d{2}-\d{2})\b",
]

AMOUNT_PATTERNS = [
    r"TOTAL\s*[:\-]?\s*₹?\s?(\d+[.,]\d{2})",
    r"AMOUNT\s*[:\-]?\s*₹?\s?(\d+[.,]\d{2})",
    r"NET\s*TOTAL\s*₹?\s?(\d+[.,]\d{2})",
    r"₹\s?(\d+[.,]\d{2})",
    r"TOTAL\s*AMOUNT\s*[:\-]?\s*₹?\s?(\d+[.,]\d{2})",
    r"GRAND\s*TOTAL\s*[:\-]?\s*₹?\s?(\d+[.,]\d{2})",
    r"AMOUNT\s*DUE\s*[:\-]?\s*₹?\s?(\d+[.,]\d{2})",
]


def extract_date(text: str):
    for pattern in DATE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            try:
                return datetime.strptime(
                    match.group(1).replace("-", "/"), "%d/%m/%Y"
                ).date()
            except:
                pass
    return None


def extract_total_amount(text: str):
    for pattern in AMOUNT_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return Decimal(match.group(1).replace(",", "."))
            except:
                pass
    return None


def extract_merchant_name(text: str):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines:
        return lines[0][:255]  # First non-empty line
    return None


def extract_payment_mode(text: str):
    text = text.lower()
    if "upi" in text:
        return "upi"
    if "cash" in text:
        return "cash"
    if "card" in text:
        return "card"
    if "wallet" in text:
        return "wallet"
    return None


def extract_invoice_number(text: str):
    match = re.search(r"invoice\s*no[:\-]?\s*(\S+)", text, re.IGNORECASE)
    return match.group(1) if match else None


def extract_gst_number(text: str):
    match = re.search(
        r"\b\d{2}[A-Z]{5}\d{4}[A-Z]\d[Z]\w\b", text
    )
    return match.group(0) if match else None


def parse_document(text: str, doc_type: str):
    data = {
        "merchant_name": extract_merchant_name(text),
        "date": extract_date(text),
        "total_amount": extract_total_amount(text),
        "category": "shopping",  
    }

    if doc_type == "receipt":
        data["payment_mode"] = extract_payment_mode(text)

    if doc_type == "invoice":
        data["invoice_number"] = extract_invoice_number(text)
        data["gst_number"] = extract_gst_number(text)

    return data