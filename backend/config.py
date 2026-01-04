import os

DEBUG = os.getenv("DEBUG", "True") == "True"
OCR_ENGINE = "paddle"