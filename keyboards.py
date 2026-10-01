from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🌐 Text Translation",
                callback_data="text_translate"
            )
        ],

        [
            InlineKeyboardButton(
                "🎤 Voice AI",
                callback_data="voice_ai"
            ),

            InlineKeyboardButton(
                "🎬 Video Translation",
                callback_data="video_translate"
            )
        ],

        [
            InlineKeyboardButton(
                "🖼️ Image / OCR",
                callback_data="ocr"
            ),

            InlineKeyboardButton(
                "📩 Forward Translate",
                callback_data="forward_translate"
            )
        ],

        [
            InlineKeyboardButton(
                "🔊 Voice Studio",
                callback_data="voice_studio"
            )
        ],

        [
            InlineKeyboardButton(
                "📜 History",
                callback_data="history"
            ),

            InlineKeyboardButton(
                "⭐ Favorites",
                callback_data="favorites"
            )
        ],

        [
            InlineKeyboardButton(
                "⚙️ Settings",
                callback_data="settings"
            ),

            InlineKeyboardButton(
                "❓ Help",
                callback_data="help"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def voice_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "👨 Male",
                callback_data="voice_gender_male"
            ),

            InlineKeyboardButton(
                "👩 Female",
                callback_data="voice_gender_female"
            )
        ],

        [
            InlineKeyboardButton(
                "🧑 Neutral",
                callback_data="voice_gender_neutral"
            )
        ],

        [
            InlineKeyboardButton(
                "🇨🇳 Chinese → Khmer",
                callback_data="voice_zh_km"
            )
        ],

        [
            InlineKeyboardButton(
                "🇰🇭 Khmer → Chinese",
                callback_data="voice_km_zh"
            )
        ],

        [
            InlineKeyboardButton(
                "🤖 Auto Detect",
                callback_data="voice_auto"
            )
        ],

        [
            InlineKeyboardButton(
                "⚡ Speed",
                callback_data="voice_speed"
            ),

            InlineKeyboardButton(
                "🎚️ Pitch",
                callback_data="voice_pitch"
            )
        ],

        [
            InlineKeyboardButton(
                "🎧 Voice History",
                callback_data="voice_history"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="back_main"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def gender_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "👨 Male",
                callback_data="voice_gender_male"
            ),

            InlineKeyboardButton(
                "👩 Female",
                callback_data="voice_gender_female"
            )
        ],

        [
            InlineKeyboardButton(
                "🧑 Neutral",
                callback_data="voice_gender_neutral"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="voice_ai"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def speed_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🐢 0.75x",
                callback_data="speed_75"
            ),

            InlineKeyboardButton(
                "▶️ 1.0x",
                callback_data="speed_100"
            )
        ],

        [
            InlineKeyboardButton(
                "⚡ 1.25x",
                callback_data="speed_125"
            ),

            InlineKeyboardButton(
                "🚀 1.50x",
                callback_data="speed_150"
            )
        ],

        [
            InlineKeyboardButton(
                "🔥 2.0x",
                callback_data="speed_200"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="voice_ai"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def pitch_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🔉 Low",
                callback_data="pitch_low"
            ),

            InlineKeyboardButton(
                "🔊 Normal",
                callback_data="pitch_normal"
            )
        ],

        [
            InlineKeyboardButton(
                "🔊 High",
                callback_data="pitch_high"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="voice_ai"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def back_menu():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="back_main"
            )
        ]
    ])
