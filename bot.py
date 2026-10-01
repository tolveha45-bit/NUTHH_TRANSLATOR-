from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from config import BOT_TOKEN

from database import init_database

from handlers import (
    start_handler,
    callback_handler,
    text_handler,
    voice_handler
)


def main():

    print("=" * 60)
    print("NUTHH TRANSLATOR")
    print("Chinese ↔ Khmer")
    print("Voice AI Enabled")
    print("=" * 60)

    # Database
    init_database()

    # Telegram
    application = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler(
            "start",
            start_handler
        )
    )

    # Buttons
    application.add_handler(
        CallbackQueryHandler(
            callback_handler
        )
    )

    # Voice
    application.add_handler(
        MessageHandler(
            filters.VOICE,
            voice_handler
        )
    )

    # Text
    application.add_handler(
        MessageHandler(
            filters.TEXT &
            ~filters.COMMAND,
            text_handler
        )
    )

    print(
        "Bot is running..."
    )

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":

    main()
