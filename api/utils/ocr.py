import pytesseract
import cv2
from PIL import Image
import numpy as np


def extract_text_from_image(image_path: str) -> str:
    image = cv2.imread(image_path)

    if image is None:
        return ""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

 
    gray = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    config = "--oem 3 --psm 6"

    text = pytesseract.image_to_string(gray, config=config)

    return text.strip()