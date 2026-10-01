VOICE_PROFILES = {

    "zh": {

        "male": {
            "name": "Chinese Male",
            "voice": "zh-CN-YunxiNeural"
        },

        "female": {
            "name": "Chinese Female",
            "voice": "zh-CN-XiaoxiaoNeural"
        },

        "neutral": {
            "name": "Chinese Neutral",
            "voice": "zh-CN-XiaoxiaoNeural"
        }
    },

    "km": {

        # Khmer voices may not be available
        # in the selected TTS service.
        # Fallback is configured below.

        "male": {
            "name": "Khmer Male Fallback",
            "voice": "en-US-GuyNeural"
        },

        "female": {
            "name": "Khmer Female Fallback",
            "voice": "en-US-JennyNeural"
        },

        "neutral": {
            "name": "Khmer Neutral Fallback",
            "voice": "en-US-AriaNeural"
        }
    },

    "en": {

        "male": {
            "name": "English Male",
            "voice": "en-US-GuyNeural"
        },

        "female": {
            "name": "English Female",
            "voice": "en-US-JennyNeural"
        },

        "neutral": {
            "name": "English Neutral",
            "voice": "en-US-AriaNeural"
        }
    }
}


def get_voice(
    language,
    gender
):

    language = language.lower()

    gender = gender.lower()

    if language in VOICE_PROFILES:

        profile = VOICE_PROFILES[language]

        if gender in profile:

            return profile[gender]["voice"]

    return "en-US-JennyNeural"


def get_voice_name(
    language,
    gender
):

    language = language.lower()

    gender = gender.lower()

    if language in VOICE_PROFILES:

        profile = VOICE_PROFILES[language]

        if gender in profile:

            return profile[gender]["name"]

    return "Default Female Voice"
