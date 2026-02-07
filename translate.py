import re


def detect_lang(text: str):
    # Very light heuristic: CJK ranges
    if re.search(r"[\u4e00-\u9fff]", text):
        return "zh"
    if re.search(r"[\u3040-\u30ff]", text):
        return "ja"
    if re.search(r"[\uac00-\ud7af]", text):
        return "ko"
    return "en"


class Translator:
    def __init__(self, backend: str = "marian", src: str = "auto", tgt: str = "en", allow_pivot: bool = True):
        self.backend = backend
        self.src = src
        self.tgt = tgt
        self.allow_pivot = allow_pivot
        self._init_backend()

    def _init_backend(self):
        if self.backend == "argos":
            try:
                import argostranslate.translate as ar_translate
            except Exception as e:
                raise RuntimeError("Argos Translate not available. Install argostranslate.") from e
            self.ar_translate = ar_translate
        else:
            try:
                from transformers import MarianMTModel, MarianTokenizer
            except Exception as e:
                raise RuntimeError("Transformers not available. Install transformers, torch, sentencepiece.") from e
            self.MarianMTModel = MarianMTModel
            self.MarianTokenizer = MarianTokenizer
            self._model_cache = {}

    def translate_text(self, text: str):
        if not text.strip():
            return text

        src = detect_lang(text) if self.src == "auto" else self.src
        tgt = self.tgt

        if src == tgt:
            return text

        if self.backend == "argos":
            return self.ar_translate.translate(text, src, tgt)

        try:
            return self._translate_marian(text, src, tgt)
        except Exception:
            if not self.allow_pivot or src == "en" or tgt == "en":
                raise
            # Pivot through English if a direct model isn't available.
            interim = self._translate_marian(text, src, "en")
            return self._translate_marian(interim, "en", tgt)

    def _translate_marian(self, text: str, src: str, tgt: str):
        model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"
        if model_name not in self._model_cache:
            tokenizer = self.MarianTokenizer.from_pretrained(model_name)
            model = self.MarianMTModel.from_pretrained(model_name)
            self._model_cache[model_name] = (tokenizer, model)
        tokenizer, model = self._model_cache[model_name]

        batch = tokenizer([text], return_tensors="pt", truncation=True)
        generated = model.generate(**batch, max_length=512)
        return tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
