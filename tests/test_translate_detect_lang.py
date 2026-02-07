from translate import detect_lang


def test_detect_lang_english():
    assert detect_lang("hello world") == "en"


def test_detect_lang_chinese():
    assert detect_lang("中文測試") == "zh"


def test_detect_lang_japanese():
    assert detect_lang("日本語テスト") == "ja"


def test_detect_lang_korean():
    assert detect_lang("한국어 테스트") == "ko"
