from deep_translator import GoogleTranslator


def translate_text(
    text: str,
    source: str,
    target: str
) -> str:

    text = text.strip()

    if not text:
        return ""

    if source == target:
        return text

    translator = GoogleTranslator(
        source=source,
        target=target
    )

    return translator.translate(text)


def chinese_to_khmer(text):

    return translate_text(
        text,
        "zh-CN",
        "km"
    )


def khmer_to_chinese(text):

    return translate_text(
        text,
        "km",
        "zh-CN"
    )


def detect_and_translate(text):

    from langdetect import detect

    language = detect(text)

    if language.startswith("zh"):

        translated = chinese_to_khmer(text)

        return (
            translated,
            "zh",
            "km"
        )

    if language == "km":

        translated = khmer_to_chinese(text)

        return (
            translated,
            "km",
            "zh"
        )

    raise ValueError(
        f"Unsupported language: {language}"
    )
