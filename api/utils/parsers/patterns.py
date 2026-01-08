# api/utils/parsers/patterns.py

DATE_PATTERNS = [
    r"\b(\d{2}/\d{2}/\d{4})\b",
    r"\b(\d{2}-\d{2}-\d{4})\b",
    r"\b(\d{4}-\d{2}-\d{2})\b",
]

AMOUNT_PATTERNS = [
    r"\bTOTAL\b\s*[:\-|]?\s*(?:₹|\$|€)?\s*(\d+\.\d{2})",
    r"\bGRAND\s*TOTAL\b\s*[:\-|]?\s*(?:₹|\$|€)?\s*(\d+\.\d{2})",
    r"\bNET\s*TOTAL\b\s*(?:₹|\$|€)?\s*(\d+\.\d{2})",
    r"\bAMOUNT\s*DUE\b\s*[:\-|]?\s*(?:₹|\$|€)?\s*(\d+\.\d{2})",
    r"\bSUBTOTAL\b\s*[:\-|]?\s*(?:₹|\$|€)?\s*(\d+\.\d{2})",
]

INVOICE_NO_PATTERNS = [

    #  Standard Invoice
    r"\binvoice\s*(?:no|number|num|#)\.?\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-\/_]{2,})",

    #  Tax Invoice
    r"\btax\s*invoice\s*(?:no|number|#)?\.?\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-\/_]{2,})",

    #  Bill
    r"\bbill\s*(?:no|number|num|#)\.?\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-\/_]{2,})",

    #  Reference / Document
    r"\b(?:reference|ref|document|doc)\s*(?:no|number|#)\.?\s*[:\-]?\s*([A-Z0-9\-\/_]{3,})",

    #  POS / Retail
    r"\b(?:receipt|txn|transaction)\s*(?:id|no|number|#)\.?\s*[:\-]?\s*([A-Z0-9\-\/_]{3,})",

    #  Order / Purchase
    r"\b(?:order|po|purchase\s*order)\s*(?:no|number|#)\.?\s*[:\-]?\s*([A-Z0-9\-\/_]{3,})",

    #  E-commerce
    r"\b(?:order\s*id|invoice\s*id)\s*[:\-]?\s*([A-Z0-9\-\/_]{4,})",

    #  GST Specific
    r"\bgst\s*invoice\s*(?:no|number|#)?\.?\s*[:\-]?\s*([A-Z0-9\-\/_]{4,})",

    #  Fallback (Invoice-like tokens)
    r"\b([A-Z]{2,5}[-\/][0-9]{2,6}[-\/][0-9]{2,6})\b",
    r"\b([A-Z]{2,6}[0-9]{3,})\b",
]

RECEIPT_NO_PATTERNS = [

    # Starbucks / POS style
    r"\bCHK\s*[:\-]?\s*(\d{3,})",             
    r"#\s*(\d{3,})",                          

    # Generic receipt / invoice
    r"(?:receipt|rece1pt|bill|invoice)\s*(?:no|number|#|id)?\.?\s*[:\-]?\s*([A-Z0-9\-\/]{3,})",

    # Transaction / reference
    r"(?:txn|transaction)\s*(?:id|no|#)\s*[:\-]?\s*([A-Z0-9\-\/]{3,})",
    r"(?:ref|reference)\s*(?:no|#)\s*[:\-]?\s*([A-Z0-9\-\/]{3,})",

    # POS fallback: long numeric line
    r"\b(\d{6,})\b",                       
]

GST_PATTERN_STRICT = r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9]\b"

GST_WITH_LABEL = (
    r"(?:GSTIN|GST\s*NO|GST\s*NUMBER|GSTIN\s*NO)"
    r"[\s:]*"
    r"(\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9])"
)

SUBTOTAL_PATTERNS = [
    r"(?:sub\s*total|subtotal|subtota)\s*[:\-|]?\s*[₹$€]?\s*([\d.,\s]+)",
]

TOTAL_PATTERNS = [
    r"(?:grand\s*total|total\s*amount|amount\s*due|total)\s*[:\-|]?\s*[₹$€]?\s*([\d.,\s]+)",
]

TAX_AMOUNT_PATTERNS = [
    r"(?:tax|sales\s*tax|gst|vat)\s*[:\-]?\s*[₹$€]?\s*([\d.,]+)",
]

TAX_PERCENT_PATTERNS = [
    r"(?:tax|sales\s*tax|gst|vat)\s*[:\-]?\s*(\d{1,2}(?:\.\d+)?)\s*%",
]


DUE_DATE_PATTERNS = [


    # Explicit due-date keywords (numeric)

    r"(?:due\s*date|payment\s*due|pay\s*by|due\s*on|invoice\s*due)\s*[:\-]?\s*"
    r"(\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4})",

    r"(?:due\s*date|payment\s*due|pay\s*by)\s*[:\-]?\s*"
    r"(\d{4}[\/\-.]\d{1,2}[\/\-.]\d{1,2})",



    # Textual dates (15 Jan 2025)

    r"(?:due\s*date|payment\s*due|pay\s*by|due\s*on)\s*[:\-]?\s*"
    r"(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4})",

    r"(?:due\s*date|payment\s*due)\s*[:\-]?\s*"
    r"([A-Za-z]{3,9}\s+\d{1,2},?\s+\d{2,4})",



    # Relative terms (Net 30 / Due in X days)

    r"(?:net)\s*(\d{1,3})",

    r"(?:due\s*in)\s*(\d{1,3})\s*(?:days|day)",

    r"(?:payment\s*terms)\s*[:\-]?\s*(\d{1,3})\s*(?:days|day)",



    # Invoice language variations

    r"(?:settlement\s*date)\s*[:\-]?\s*(\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4})",

    r"(?:payable\s*by)\s*[:\-]?\s*(\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4})",



    # OCR-noisy variants

    r"(?:du[e|c]\s*d[a|o]te)\s*[:\-]?\s*(\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4})",

    r"(?:pay\s*b[y|v])\s*[:\-]?\s*(\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4})",
]

PAID_PATTERNS = [
    # Core
    r"\bpaid\b",
    r"\bfully\s+paid\b",
    r"\bpaid\s+in\s+full\b",
    r"\bsettled\b",
    r"\bcleared\b",

    # Payment confirmation
    r"\bpayment\s+received\b",
    r"\bpayment\s+successful\b",
    r"\bpayment\s+completed\b",
    r"\btransaction\s+successful\b",
    r"\btransaction\s+completed\b",

    # Amount references
    r"\bamount\s+paid\b",
    r"\btotal\s+paid\b",
    r"\bpaid\s+amount\b",

    # Zero balance indicators
    r"\bbalance\s+paid\b",
    r"\bbalance\s+cleared\b",
    r"\bbalance\s+zero\b",
    r"\bbalance\s*[:\-]?\s*0\.?0*\b",

    # Invoice-specific
    r"\binvoice\s+paid\b",
    r"\bstatus\s*[:\-]?\s*paid\b",
    r"\bpaid\s+on\b\s+\d{1,2}",

    # POS / Receipt language
    r"\bthank\s+you\s+for\s+your\s+payment\b",
    r"\breceived\s+with\s+thanks\b",

    # Accounting terms
    r"\bposted\s+payment\b",
    r"\bpayment\s+posted\b",
    r"\bclosed\b",
    r"\baccount\s+settled\b",
]

UNPAID_PATTERNS = [
    # Core
    r"\bunpaid\b",
    r"\bnot\s+paid\b",
    r"\bnot\s+yet\s+paid\b",

    # Pending / Due
    r"\bpayment\s+pending\b",
    r"\bpending\s+payment\b",
    r"\bawaiting\s+payment\b",
    r"\bawaiting\s+settlement\b",

    # Balance related
    r"\bbalance\s+due\b",
    r"\bbalance\s+pending\b",
    r"\boutstanding\b",
    r"\boutstanding\s+balance\b",

    # Amount due
    r"\bamount\s+due\b",
    r"\btotal\s+due\b",
    r"\bnet\s+amount\s+due\b",
    r"\bdue\s+amount\b",

    # Invoice language
    r"\binvoice\s+due\b",
    r"\binvoice\s+pending\b",
    r"\bstatus\s*[:\-]?\s*due\b",
    r"\bstatus\s*[:\-]?\s*pending\b",

    # Due dates
    r"\bdue\s+date\b",
    r"\bpay\s+by\b",
    r"\bpayment\s+due\s+on\b",

    # Partial payments
    r"\bpartially\s+paid\b",
    r"\bpartial\s+payment\b",

    # Accounting terms
    r"\bopen\b",
    r"\bopen\s+invoice\b",
    r"\bunsettled\b",
    r"\bpayment\s+overdue\b",
]


LINE_ITEM_PATTERNS = [

    # Latte 2 x 150.00 | Latte 2X150
    r"""
    ^(?P<name>[A-Za-z][A-Za-z0-9\s\-&/.()]+?)
    \s+(?P<qty>\d+)
    \s*[xX]\s*
    (?P<price>\d+(?:[.,]\d{2})?)$
    """,

    # Latte x2 150.00
    r"""
    ^(?P<name>[A-Za-z][A-Za-z0-9\s\-&/.()]+?)
    \s*[xX](?P<qty>\d+)
    \s+(?P<price>\d+(?:[.,]\d{2})?)$
    """,

    # Latte 2 150.00
    r"""
    ^(?P<name>[A-Za-z][A-Za-z0-9\s\-&/.()]+?)
    \s+(?P<qty>\d+)
    \s+(?P<price>\d+(?:[.,]\d{2})?)$
    """,

    # Latte @ 150.00
    r"""
    ^(?P<name>[A-Za-z][A-Za-z0-9\s\-&/.()]+?)
    \s*[@₹$]?\s*
    (?P<price>\d+(?:[.,]\d{2})?)$
    """,

    # Latte 150.00 A | Latte 150.00 T
    r"""
    ^(?P<name>[A-Za-z][A-Za-z0-9\s\-&/.()]+?)
    \s+(?P<price>\d+(?:[.,]\d{2})?)
    \s*[A-Za-z]?$ 
    """,
]

NON_ITEM_KEYWORDS = {
    # totals & summaries
    "total", "subtotal", "sub total", "grand total",
    "tax", "vat", "gst", "cgst", "sgst", "igst",
    "discount", "round off", "rounding",
    "change", "change due", "balance", "amount due",
    "paid", "payment", "payable",

    # payment methods
    "mastercard", "visa", "rupay", "amex", "american express",
    "debit", "credit", "card", "upi", "cash", "wallet",
    "netbanking", "bank", "imps", "neft", "rtgs",

    # receipt meta
    "invoice", "bill no", "bill#", "receipt", "txn",
    "transaction", "approval", "auth", "reference",
    "rrn", "terminal", "mid", "tid",

    # noise / footer
    "thank", "visit again", "customer copy",
    "signature", "authorized", "welcome",
    "offer", "promo", "reward", "points",

    # masked numbers
    "xxxx", "****",
}


REFERENCE_PREFIXES = {
    "chk", "check", "txn", "ref", "rrn",
    "auth", "approval", "invoice",
    "bill", "order", "table", "drawer",
    "reg", "terminal"
}


CATEGORY_KEYWORDS = {
    # FOOD & DINING
    "food": [
        "restaurant", "restauran", "restaurent",
        "cafe", "cafeteria", "coffee", "cofee",
        "pizza", "burger", "sandwich",
        "meal", "diner", "bistro", "canteen",
        "food", "snacks", "breakfast",
        "lunch", "dinner",
        "dominos", "mcdonald", "kfc", "subway",
        "starbucks", "barista",
        "swiggy", "zomato",
        "bakery", "bake", "pastry",
        "icecream", "dessert",
        "restaurant bill", "food bill"
    ],

    # TRAVEL & TRANSPORT
    "travel": [
        "uber", "ola", "rapido",
        "taxi", "cab", "auto",
        "flight", "airline", "airways",
        "boarding", "boarding pass",
        "airport", "terminal",
        "hotel", "hostel", "resort",
        "stay", "room", "check-in",
        "checkin", "checkout",
        "train", "railway", "irctc",
        "bus", "volvo", "redbus",
        "metro", "subway",
        "travel", "journey", "trip",
        "makemytrip", "goibibo", "oyo"
    ],

    # SHOPPING & E-COMMERCE
    "shopping": [
        "store", "shop", "shopping",
        "mall", "market", "bazaar",
        "amazon", "amaz0n",
        "flipkart", "myntra",
        "ajio", "meesho",
        "snapdeal",
        "order", "online order",
        "retail", "wholesale",
        "purchase", "buy",
        "invoice", "bill no",
        "electronics", "mobile",
        "laptop", "accessories",
        "fashion", "clothing",
        "footwear", "shoes"
    ],

    # UTILITIES & BILLS
    "utilities": [
        "electricity", "electric",
        "power", "energy",
        "water", "water bill",
        "gas", "lpg",
        "internet", "broadband",
        "wifi", "wi-fi",
        "mobile bill", "postpaid",
        "prepaid recharge",
        "telephone", "landline",
        "utility", "utilities",
        "bill payment",
        "electric bill",
        "bescom", "mseb", "dvcom",
        "jio", "airtel", "vi",
        "bsnl"
    ],

    # MEDICAL & HEALTHCARE
    "medical": [
        "pharmacy", "pharm", "chemist",
        "medicine", "medicines",
        "hospital", "clinic",
        "medical", "healthcare",
        "doctor", "dr.",
        "consultation", "diagnosis",
        "lab", "laboratory",
        "test", "blood test",
        "x-ray", "xray",
        "scan", "ct scan", "mri",
        "apollo", "fortis", "aiims",
        "prescription", "rx"
    ],

    # EDUCATION
    "education": [
        "school", "college", "university",
        "tuition", "fees", "fee receipt",
        "exam", "examination",
        "course", "training",
        "coaching", "institute",
        "education", "learning",
        "udemy", "coursera",
        "byjus", "unacademy",
        "books", "textbook"
    ],

    # ENTERTAINMENT & SUBSCRIPTIONS
    "entertainment": [
        "movie", "cinema", "theatre",
        "ticket", "show",
        "netflix", "prime video",
        "amazon prime", "hotstar",
        "spotify", "gaana",
        "subscription",
        "game", "gaming",
        "concert", "event",
        "bookmyshow"
    ],

    # RENT & HOUSING
    "housing": [
        "rent", "rental",
        "house rent",
        "apartment", "flat",
        "maintenance",
        "society charges",
        "housing",
        "property",
        "real estate",
        "brokerage"
    ],

    # BUSINESS & PROFESSIONAL
    "business": [
        "invoice", "tax invoice",
        "gst invoice",
        "professional fee",
        "consulting",
        "service charge",
        "office expense",
        "business expense",
        "vendor",
        "supplier",
        "company"
    ],
}

CURRENCY_SYMBOLS = {
    "₹": "INR",
    "Rs": "INR",
    "₨": "INR",

    "$": "USD",
    "US$": "USD",
    "USD$": "USD",

    "€": "EUR",
    "£": "GBP",

    "¥": "JPY",
    "￥": "JPY",

    "₩": "KRW",
    "₽": "RUB",
    "₺": "TRY",

    "₫": "VND",
    "₱": "PHP",

    "₪": "ILS",
    "₦": "NGN",
    "₴": "UAH",

    "₡": "CRC",
    "₲": "PYG",
    "₸": "KZT",

    "฿": "THB",
    "₭": "LAK",
    "₮": "MNT",

    "៛": "KHR",
    "৳": "BDT",
    "៛": "KHR",

    "₿": "BTC",
    "Ƀ": "BTC",
    "Ξ": "ETH",
    "Ł": "LTC",
    "Ð": "DOGE",
    "₠": "EUR",
    "₣": "FRF",
    "₤": "ITL",
    "₧": "ESP",
    "₯": "GRD",
}

CURRENCY_WORD_PATTERNS = {
    # Indian Rupee
    r"\b(inr|rs\.?|rupees?|rupee)\b": "INR",

    # US Dollar
    r"\b(usd|us\$|dollars?|bucks?)\b": "USD",

    # Euro
    r"\b(eur|euros?)\b": "EUR",

    # British Pound
    r"\b(gbp|pounds?|sterling)\b": "GBP",

    # Japanese Yen
    r"\b(jpy|yen)\b": "JPY",

    # Chinese Yuan
    r"\b(cny|yuan|renminbi|rmb)\b": "CNY",

    # South Korean Won
    r"\b(krw|won)\b": "KRW",

    # Russian Ruble
    r"\b(rub|ruble|rouble)\b": "RUB",

    # Turkish Lira
    r"\b(try|lira|liras)\b": "TRY",

    # Australian Dollar
    r"\b(aud|australian dollars?)\b": "AUD",

    # Canadian Dollar
    r"\b(cad|canadian dollars?)\b": "CAD",

    # Singapore Dollar
    r"\b(sgd|singapore dollars?)\b": "SGD",

    # Hong Kong Dollar
    r"\b(hkd|hong kong dollars?)\b": "HKD",

    # UAE Dirham
    r"\b(aed|dirham|dirhams)\b": "AED",

    # Saudi Riyal
    r"\b(sar|riyal|riyals)\b": "SAR",

    # South African Rand
    r"\b(zar|rand)\b": "ZAR",

    # Brazilian Real
    r"\b(brl|real|reais)\b": "BRL",

    # Mexican Peso
    r"\b(mxn|peso|pesos)\b": "MXN",

    # Chilean Peso
    r"\b(clp|chilean peso)\b": "CLP",

    # Argentine Peso
    r"\b(ars|argentine peso)\b": "ARS",

    # Thai Baht
    r"\b(thb|baht)\b": "THB",

    # Indonesian Rupiah
    r"\b(idr|rupiah)\b": "IDR",

    # Vietnamese Dong
    r"\b(vnd|dong)\b": "VND",

    # Nigerian Naira
    r"\b(ngn|naira)\b": "NGN",

    # Egyptian Pound
    r"\b(egp|egyptian pound)\b": "EGP",

    # 🇧🇩 Bangladeshi Taka
    r"\b(bdt|taka)\b": "BDT",

    # Sri Lankan Rupee
    r"\b(lkr|sri lankan rupee)\b": "LKR",

    # Nepalese Rupee
    r"\b(npr|nepalese rupee)\b": "NPR",

    # Crypto
    r"\b(btc|bitcoin)\b": "BTC",
    r"\b(eth|ethereum)\b": "ETH",
    r"\b(ltc|litecoin)\b": "LTC",
    r"\b(doge|dogecoin)\b": "DOGE",


}

ADDRESS_HINTS = [
    "road", "street", "st", "rd", "ave", "avenue",
    "lane", "ln", "boulevard", "blvd",
    "sector", "block", "floor", "building",
    "market", "plaza", "mall",
    "pier", "terminal", "complex",

]

CITY_STATE_REGEX = r"[A-Z][a-zA-Z\s]+,\s?[A-Z]{2}\b"
PINCODE_REGEX = r"\b\d{5,6}\b"
PHONE_REGEX = r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"

MERCHANT_BLACKLIST = [
    "receipt",
    "tax invoice",
    "invoice",
    "thank you",
    "welcome",
    "***",
]

PAYMENT_KEYWORDS = {
    "upi": [
        # Generic
        "upi", "upi ref", "upi txn", "upi id",

        # Google / PhonePe / Paytm
        "gpay", "google pay", "googlepay",
        "phonepe", "phone pe",
        "paytm", "paytm upi",

        # Banks
        "bhim", "bhim upi",
        "sbi upi", "icici upi", "hdfc upi", "axis upi",
    ],

    "cash": [
        "cash", "paid cash", "cash payment",
        "cash received", "paid in cash",
    ],

    "card": [
        # Generic
        "card", "debit", "credit", "credit card", "debit card",

        # Card networks
        "visa", "mastercard", "master card",
        "rupay", "ru pay",
        "amex", "american express",
        "diners", "discover",

        # Card terms
        "pos", "pos txn", "terminal",
        "chip", "swipe", "tap",
        "auth code", "approval code",
        "xxxx", "****",  # masked card numbers
    ],

    "wallet": [
        # Wallet keywords
        "wallet", "digital wallet",

        # Popular wallets
        "amazon pay", "amazonpay",
        "paytm wallet",
        "mobikwik", "freecharge",
        "ola money", "jiomoney",
        "airtel money",
    ],

    "net_banking": [
        "net banking", "internet banking",
        "online transfer", "bank transfer",
        "neft", "rtgs", "imps",
        "fund transfer",
    ],

    "bnpl": [
        # Buy Now Pay Later
        "pay later", "buy now pay later",
        "simpl", "lazy pay", "zest money",
        "postpaid", "amazon pay later",
        "flipkart pay later",
    ],
}

BUSINESS_KEYWORDS = {
    "office", "stationery", "printer", "paper", "toner",
    "software", "subscription", "cloud", "aws", "azure",
    "domain", "hosting", "server",
    "client", "invoice", "tax", "gst",
    "travel", "flight", "uber", "ola", "hotel",
    "conference", "meeting", "laptop", "monitor",
    "electronics", "consulting", "service fee",
}

PERSONAL_KEYWORDS = {
    "coffee", "latte", "cappuccino", "tea",
    "restaurant", "cafe", "starbucks", "food",
    "grocery", "supermarket", "mart",
    "movie", "cinema", "netflix",
    "clothing", "fashion", "shoes",
    "gym", "salon", "spa",
}