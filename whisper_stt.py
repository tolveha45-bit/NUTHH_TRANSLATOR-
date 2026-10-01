from faster_whisper import (
    WhisperModel
)

from config import (
    WHISPER_MODEL,
    WHISPER_DEVICE,
    WHISPER_COMPUTE_TYPE
)


_model = None


def get_model():

    global _model

    if _model is None:

        print(
            "Loading Whisper model:",
            WHISPER_MODEL
        )

        _model = WhisperModel(
            WHISPER_MODEL,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE_TYPE
        )

    return _model


def transcribe_audio(
    audio_path,
    language=None
):

    model = get_model()

    whisper_language = None

    if language == "zh":

        whisper_language = "zh"

    elif language == "km":

        whisper_language = "km"

    segments, info = model.transcribe(
        audio_path,
        language=whisper_language,
        beam_size=5,
        vad_filter=True,
        condition_on_previous_text=True
    )

    result = []

    for segment in segments:

        text = (
            segment.text or ""
        ).strip()

        if not text:

            continue

        result.append(
            {
                "start": float(
                    segment.start
                ),
                "end": float(
                    segment.end
                ),
                "text": text
            }
        )

    return (
        info.language,
        result
    )
