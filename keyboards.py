from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🌐 Text Translate",
                callback_data="text_translate"
            )
        ],

        [
            InlineKeyboardButton(
                "🎤 Voice",
                callback_data="voice_translate"
            ),

            InlineKeyboardButton(
                "🖼️ OCR",
                callback_data="ocr_translate"
            )
        ],

        [
            InlineKeyboardButton(
                "🎬 Video Translate",
                callback_data="video_translate"
            )
        ],

        [
            InlineKeyboardButton(
                "📩 Forward Translate",
                callback_data="forward_translate"
            )
        ],

        [
            InlineKeyboardButton(
                "🔄 Language Mode",
                callback_data="language_mode"
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
                "🔐 My License",
                callback_data="license"
            )
        ],

        [
            InlineKeyboardButton(
                "⚙️ Settings",
                callback_data="settings"
            )
        ],

        [
            InlineKeyboardButton(
                "❓ Help",
                callback_data="help"
            )
        ]
    ]

    return InlineKeyboardMarkup(
        keyboard
    )


def video_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "🇨🇳 → 🇰🇭",
                callback_data="video_zh_km"
            ),

            InlineKeyboardButton(
                "🇰🇭 → 🇨🇳",
                callback_data="video_km_zh"
            )
        ],

        [
            InlineKeyboardButton(
                "🤖 Auto Detect",
                callback_data="video_auto"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 Subtitle Only",
                callback_data="video_subtitle"
            )
        ],

        [
            InlineKeyboardButton(
                "🎞️ Burn Subtitle",
                callback_data="video_burn"
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="main_menu"
            )
        ]
    ]

    return InlineKeyboardMarkup(
        keyboard
    )


def back_menu():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⬅️ Back",
                    callback_data="main_menu"
                )
            ]
        ]
    )
