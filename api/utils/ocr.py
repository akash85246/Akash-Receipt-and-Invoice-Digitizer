import cv2
import pytesseract
import numpy as np
import os
from paddleocr import PaddleOCR
from django.conf import settings
import uuid

paddle_ocr = PaddleOCR(
    use_angle_cls=True,
    lang="en"
)

CONFIDENCE_THRESHOLD = 0.65


def normalize_box(box):
    xs = [p[0] for p in box]
    ys = [p[1] for p in box]
    return min(xs), min(ys), max(xs), max(ys)


def group_words_into_lines(words, y_threshold=12):
    lines = []

    for word in words:
        x1, y1, x2, y2 = normalize_box(word["box"])
        y_center = (y1 + y2) / 2
        word["bbox"] = (x1, y1, x2, y2)
        word["y_center"] = y_center

        placed = False
        for line in lines:
            if abs(line["y_center"] - y_center) < y_threshold:
                line["words"].append(word)
                placed = True
                break

        if not placed:
            lines.append({
                "y_center": y_center,
                "words": [word]
            })

    return lines


def merge_lines(lines):
    merged_lines = []

    # Top to bottom
    lines.sort(key=lambda l: l["y_center"])

    for line in lines:
        # Left to right
        line["words"].sort(key=lambda w: w["bbox"][0])

        text = " ".join(w["text"] for w in line["words"])
        merged_lines.append(text)

    return merged_lines


def filter_vertical_text(words, ratio=2.5):
    filtered = []
    for w in words:
        x1, y1, x2, y2 = normalize_box(w["box"])
        width = x2 - x1
        height = y2 - y1

        if height / max(width, 1) < ratio:
            filtered.append(w)

    return filtered


def preprocess_image(image_path: str) -> tuple[np.ndarray, str]:
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.fastNlMeansDenoising(img, None, 30, 7, 21)
    img = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "processed"), exist_ok=True)

    filename = f"processed_{uuid.uuid4().hex}.png"
    save_path = os.path.join(settings.MEDIA_ROOT, "processed", filename)

    cv2.imwrite(save_path, img)

    # 🔹 Return both image + URL
    image_url = f"{settings.MEDIA_URL}processed/{filename}"

    return img, image_url

def run_paddle_ocr(image_path: str):
    result = paddle_ocr.ocr(image_path)

    if not result or not result[0]:
        return [], 0.0

    words = []
    confidences = []

    for line in result[0]:
        try:
            # PaddleOCR line format (robust)
            box = line[0]
            text = line[1][0]
            conf = float(line[1][1])

            if text.strip():
                words.append({
                    "text": text,
                    "box": box,
                    "confidence": conf
                })
                confidences.append(conf)

        except Exception:
            # Skip malformed lines safely
            continue

    avg_confidence = (
        sum(confidences) / len(confidences)
        if confidences else 0.0
    )

    return words, avg_confidence


def run_tesseract(preprocessed_img):
    data = pytesseract.image_to_data(
        preprocessed_img,
        output_type=pytesseract.Output.DICT,
        config="--oem 3 --psm 6"
    )

    lines = {}
    confidences = []

    n = len(data["text"])

    for i in range(n):
        text = data["text"][i].strip()
        conf = int(data["conf"][i])

        if conf <= 0 or not text:
            continue

        # Use block + paragraph + line as a unique line key
        line_key = (
            data["block_num"][i],
            data["par_num"][i],
            data["line_num"][i],
        )

        if line_key not in lines:
            lines[line_key] = []

        lines[line_key].append(text)
        confidences.append(conf)

    # Merge words into proper lines
    merged_lines = [
        " ".join(words) for _, words in sorted(lines.items())
    ]

    avg_conf = (sum(confidences) / len(confidences)) / 100 if confidences else 0.0

    return merged_lines, avg_conf

def hybrid_ocr(image_path: str):
    paddle_words, paddle_conf = run_paddle_ocr(image_path)

    if paddle_conf >= CONFIDENCE_THRESHOLD:
        paddle_words = filter_vertical_text(paddle_words)
        lines = group_words_into_lines(paddle_words)
        merged_text = merge_lines(lines)

        return {
            "engine": "paddle",
            "confidence": paddle_conf,
            "lines": merged_text,
            "raw_words": paddle_words
        }

    # Fallback to Tesseract
    processed_img, processed_image_url = preprocess_image(image_path)
    texts, conf = run_tesseract(processed_img)

    return {
        "engine": "tesseract",
        "confidence": conf,
        "lines": texts,
        "processed_image": processed_image_url
    }


def extract_text_from_file(file_path: str) -> dict:
    image = cv2.imread(file_path)

    if image is None:
        raise ValueError("Invalid image file")

    return hybrid_ocr(file_path)
