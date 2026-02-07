import io
from pathlib import Path

import fitz  # PyMuPDF
import img2pdf
from PIL import Image


def render_pdf_to_images(pdf_path: Path, dpi: int = 150, max_pages: int = 0):
    doc = fitz.open(pdf_path)
    images = []
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)

    page_count = doc.page_count if max_pages == 0 else min(max_pages, doc.page_count)
    for i in range(page_count):
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    doc.close()
    return images


def images_to_pdf(images, output_path: Path, jpeg_quality: int = 80, dpi: int = 150):
    jpeg_bytes_list = []
    for img in images:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=jpeg_quality, optimize=True)
        jpeg_bytes_list.append(buf.getvalue())

    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(jpeg_bytes_list, dpi=dpi))
