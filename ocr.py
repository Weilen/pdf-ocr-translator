from paddleocr import PaddleOCR


class OCRProcessor:
    def __init__(self, lang: str = "auto"):
        self.lang = lang
        if lang == "auto":
            # Use multilingual model by default; PaddleOCR uses 'ch' with english by default.
            self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        else:
            self.ocr = PaddleOCR(use_angle_cls=True, lang=lang)

    def detect(self, image):
        # PaddleOCR expects numpy array
        result = self.ocr.ocr(image, cls=True)
        # Normalize to a list of items for a single image
        if result and isinstance(result, list):
            if len(result) == 1 and isinstance(result[0], list) and result[0] and isinstance(result[0][0], list):
                return result[0]
        return result or []
