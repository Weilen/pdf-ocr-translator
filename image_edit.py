from PIL import ImageDraw, ImageFont


def _load_font(font_path: str, size: int):
    if font_path:
        try:
            return ImageFont.truetype(font_path, size=size)
        except Exception:
            pass
    # Common fallback
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def _fit_text(draw, text, box, font_path: str):
    x_min, y_min, x_max, y_max = box
    width = max(1, int(x_max - x_min))
    height = max(1, int(y_max - y_min))

    font_size = max(8, int(height * 0.9))
    font = _load_font(font_path, font_size)

    while font_size > 6:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        if text_w <= width and text_h <= height:
            return font
        font_size -= 1
        font = _load_font(font_path, font_size)
    return font


def translate_image_inplace(image, ocr_result, translator, font_path: str = ""):
    draw = ImageDraw.Draw(image)

    # PaddleOCR result format: list[ [ [box], (text, conf) ], ... ] per page
    for item in ocr_result:
        box = item[0]
        text = item[1][0]
        if not text.strip():
            continue

        translated = translator.translate_text(text)

        xs = [p[0] for p in box]
        ys = [p[1] for p in box]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)

        # Cover original text with white rectangle
        draw.rectangle([x_min, y_min, x_max, y_max], fill=(255, 255, 255))

        font = _fit_text(draw, translated, (x_min, y_min, x_max, y_max), font_path)
        draw.text((x_min, y_min), translated, fill=(0, 0, 0), font=font)

    return image
