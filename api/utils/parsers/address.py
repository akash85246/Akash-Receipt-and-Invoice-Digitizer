from .patterns import ADDRESS_HINTS, CITY_STATE_REGEX, PINCODE_REGEX, PHONE_REGEX
import re
from .normalizers import normalize_text

def extract_address(text):
    text = normalize_text(text)
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    address_block = []
    capture = False

    for i, line in enumerate(lines):
        lower = line.lower()

        # Start capturing if line looks address-like
        if (
            any(hint in lower for hint in ADDRESS_HINTS)
            or re.search(CITY_STATE_REGEX, line)
            or re.search(PINCODE_REGEX, line)
        ):
            capture = True

        if capture:
            # Remove phone numbers
            clean = re.sub(PHONE_REGEX, "", line).strip(" ,|-")
            address_block.append(clean)

            # Capture max 3 lines
            if len(address_block) >= 3:
                break

    if not address_block:
        return None

    # Remove duplicates & join
    address = ", ".join(dict.fromkeys(address_block))

    return address[:255]