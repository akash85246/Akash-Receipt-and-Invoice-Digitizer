import cv2
import numpy as np
import os
import uuid


class PreprocessImage:
    """
    Safe OCR preprocessing
    """

    @staticmethod
    def limit_image_size(img: np.ndarray, max_side: int = 3000) -> np.ndarray:
        """
        Resize image so max(height, width) <= max_side
        while preserving aspect ratio.
        """
        h, w = img.shape[:2]
        max_dim = max(h, w)

        if max_dim <= max_side:
            return img

        scale = max_side / max_dim
        new_w = int(w * scale)
        new_h = int(h * scale)

        return cv2.resize(
            img,
            (new_w, new_h),
            interpolation=cv2.INTER_AREA
        )

    @staticmethod
    def normalize(img: np.ndarray) -> np.ndarray:
        """
        Normalize lighting without destroying faint text.
        """
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return cv2.normalize(
            img,
            None,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX
        )

    @staticmethod
    def denoise(img: np.ndarray) -> np.ndarray:
        """
        Light denoising (safe for receipts & invoices).
        """
        return cv2.fastNlMeansDenoising(
            img,
            h=12,  # keep LOW to avoid text loss
            templateWindowSize=7,
            searchWindowSize=21
        )

    @staticmethod
    def preprocess_for_ocr(
        image_path: str,
        max_side: int = 3000
    ) -> str:
        """
        Full preprocessing pipeline:
        - Load image
        - Resize safely
        - Normalize lighting
        - Light denoise
        - Save and return file path
        """
        img = cv2.imread(image_path)

        if img is None:
            raise ValueError("Invalid image file")

        img = PreprocessImage.limit_image_size(img, max_side)
        img = PreprocessImage.normalize(img)
        img = PreprocessImage.denoise(img)

        # Save processed image
        processed_dir = os.path.join("media", "processed")
        os.makedirs(processed_dir, exist_ok=True)

        filename = f"ocr_{uuid.uuid4().hex}.png"
        processed_path = os.path.join(processed_dir, filename)

        cv2.imwrite(processed_path, img)

        return processed_path