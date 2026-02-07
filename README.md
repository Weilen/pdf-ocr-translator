# PDF OCR Translator

Pipeline: Input PDF → OCR → translate → preserve layout → output PDF (compressed).

## Recommended engines (open source)
- OCR: PaddleOCR (high accuracy, strong CJK support)
- Translation: MarianMT (local) or Argos Translate (local)

## Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Note: `paddlepaddle`, `torch`, and translation models are large and may take time to install/download.

## CLI usage
```bash
python main.py \
  --input input.pdf \
  --output output.en.pdf \
  --ocr-lang auto \
  --src-lang auto \
  --tgt-lang en \
  --translation-backend marian \
  --dpi 150 \
  --jpeg-quality 80
```

## GUI usage
```bash
python gui.py
```

## Notes
- Layout preservation is done by rendering each page to an image and replacing text in its original bounding boxes.
- Output is image-based PDF; compression is controlled via DPI and JPEG quality.
- For best CJK rendering, provide a font that supports the target language with `--font-path`.
- If a direct Marian model is unavailable for a pair (e.g., JA→KO), the tool can pivot through English.
- Use `--no-pivot` to disable pivoting.

## File size targets
- Default settings (150 DPI, JPEG quality 80) are tuned for size reduction. If your output is still >10MB, lower DPI or JPEG quality.
