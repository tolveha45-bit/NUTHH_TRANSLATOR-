from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from config import BOT_TOKEN

from database import (
    init_database
)

from handlers import (
    start_handler,
    callback_handler,
    text_handler,
    video_handler
)


def main():

    print(
        "================================"
    )

    print(
        " NUTHH TRANSLATOR BOT"
    )

    print(
        " Long Video Edition"
    )

    print(
        "================================"
    )

    init_database()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # /start
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

    # Video
    application.add_handler(
        MessageHandler(
            filters.VIDEO,
            video_handler
        )
    )

    # Text
    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND,
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
