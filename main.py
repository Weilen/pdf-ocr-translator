#!/usr/bin/env python3
import argparse
from pathlib import Path

from image_edit import translate_image_inplace
from ocr import OCRProcessor
from pdf_utils import images_to_pdf, render_pdf_to_images
from translate import Translator


def parse_args():
    p = argparse.ArgumentParser(description="PDF OCR translator with layout preservation.")
    p.add_argument("--input", "-i", required=True, help="Input PDF path")
    p.add_argument("--output", "-o", required=True, help="Output PDF path")
    p.add_argument(
        "--ocr-lang",
        default="auto",
        choices=["auto", "en", "ch", "japan", "korean"],
        help="OCR language (PaddleOCR). 'auto' will try multilingual settings.",
    )
    p.add_argument(
        "--src-lang",
        default="auto",
        choices=["auto", "en", "zh", "ja", "ko"],
        help="Source language for translation",
    )
    p.add_argument(
        "--tgt-lang", default="en", choices=["en", "zh", "ja", "ko"], help="Target language"
    )
    p.add_argument(
        "--translation-backend",
        default="marian",
        choices=["marian", "argos"],
        help="Translation engine backend",
    )
    p.add_argument(
        "--no-pivot",
        action="store_true",
        help=("Disable pivot translation through English if direct model is missing (Marian only)"),
    )
    p.add_argument("--dpi", type=int, default=150, help="Render DPI for PDF pages")
    p.add_argument("--jpeg-quality", type=int, default=80, help="JPEG quality for output images")
    p.add_argument("--font-path", default="", help="Path to TTF font for rendering translated text")
    p.add_argument("--max-pages", type=int, default=0, help="Limit number of pages (0 = all)")
    return p.parse_args()


def main():
    args = parse_args()

    input_pdf = Path(args.input)
    output_pdf = Path(args.output)
    if not input_pdf.exists():
        raise SystemExit(f"Input not found: {input_pdf}")

    images = render_pdf_to_images(input_pdf, dpi=args.dpi, max_pages=args.max_pages)

    ocr = OCRProcessor(lang=args.ocr_lang)
    translator = Translator(
        backend=args.translation_backend,
        src=args.src_lang,
        tgt=args.tgt_lang,
        allow_pivot=not args.no_pivot,
    )

    edited_images = []
    for page_index, image in enumerate(images, start=1):
        print(f"Processing page {page_index}/{len(images)}")
        ocr_result = ocr.detect(image)
        edited = translate_image_inplace(
            image=image,
            ocr_result=ocr_result,
            translator=translator,
            font_path=args.font_path,
        )
        edited_images.append(edited)

    images_to_pdf(edited_images, output_pdf, jpeg_quality=args.jpeg_quality, dpi=args.dpi)
    print(f"Saved: {output_pdf}")


if __name__ == "__main__":
    main()
