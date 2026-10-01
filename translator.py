from deep_translator import GoogleTranslator


def translate_text(
    text: str,
    source: str,
    target: str
) -> str:

    text = (
        text or ""
    ).strip()

    if not text:

        return ""

    if source == target:

        return text

    translator = GoogleTranslator(
        source=source,
        target=target
    )

    return translator.translate(
        text
    )


def translate_chinese_to_khmer(
    text
):

    return translate_text(
        text,
        "zh-CN",
        "km"
    )


def translate_khmer_to_chinese(
    text
):

    return translate_text(
        text,
        "km",
        "zh-CN"
    )
