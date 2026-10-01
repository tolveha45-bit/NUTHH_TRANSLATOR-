import asyncio
from pathlib import Path

from telegram import Update

from telegram.ext import (
    ContextTypes
)

from keyboards import (
    main_menu,
    video_menu,
    back_menu
)

from database import (
    add_user,
    create_video_job,
    update_video_job
)

from license import (
    check_license
)

from config import (
    TEMP_DIR
)

from video import (
    translate_long_video
)


# ============================================================
# START
# ============================================================

async def start_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    add_user(user)

    await update.message.reply_text(
        "👋 Welcome to NUTHH Translator\n\n"
        "Professional Chinese ↔ Khmer Translator\n\n"
        "🎬 Long Video Translation\n"
        "📝 SRT Subtitle\n"
        "🎞️ Burn Subtitle\n\n"
        "Choose a feature:",
        reply_markup=main_menu()
    )


# ============================================================
# CALLBACK
# ============================================================

async def callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    data = query.data

    # --------------------------------------------------------
    # MAIN
    # --------------------------------------------------------

    if data == "main_menu":

        await query.edit_message_text(
            "🏠 MAIN MENU\n\n"
            "Choose a feature:",
            reply_markup=main_menu()
        )

        return

    # --------------------------------------------------------
    # VIDEO MENU
    # --------------------------------------------------------

    if data == "video_translate":

        await query.edit_message_text(
            "🎬 VIDEO TRANSLATION\n\n"
            "Choose translation mode:",
            reply_markup=video_menu()
        )

        return

    # --------------------------------------------------------
    # CHINESE → KHMER
    # --------------------------------------------------------

    if data == "video_zh_km":

        context.user_data[
            "video_mode"
        ] = "zh_km"

        context.user_data[
            "video_burn"
        ] = True

        await query.edit_message_text(
            "🇨🇳 → 🇰🇭\n\n"
            "🎬 Send your video.\n\n"
            "The bot will:\n"
            "1. Split into chunks\n"
            "2. Speech-to-text\n"
            "3. Translate to Khmer\n"
            "4. Generate SRT\n"
            "5. Burn subtitle",
            reply_markup=back_menu()
        )

        return

    # --------------------------------------------------------
    # KHMER → CHINESE
    # --------------------------------------------------------

    if data == "video_km_zh":

        context.user_data[
            "video_mode"
        ] = "km_zh"

        context.user_data[
            "video_burn"
        ] = True

        await query.edit_message_text(
            "🇰🇭 → 🇨🇳\n\n"
            "🎬 Send your video.",
            reply_markup=back_menu()
        )

        return

    # --------------------------------------------------------
    # AUTO
    # --------------------------------------------------------

    if data == "video_auto":

        context.user_data[
            "video_mode"
        ] = "auto"

        context.user_data[
            "video_burn"
        ] = True

        await query.edit_message_text(
            "🤖 AUTO DETECT\n\n"
            "🎬 Send your video.\n\n"
            "The bot will detect the "
            "spoken language automatically.",
            reply_markup=back_menu()
        )

        return

    # --------------------------------------------------------
    # SUBTITLE ONLY
    # --------------------------------------------------------

    if data == "video_subtitle":

        context.user_data[
            "video_mode"
        ] = "auto"

        context.user_data[
            "video_burn"
        ] = False

        await query.edit_message_text(
            "📝 SUBTITLE ONLY\n\n"
            "🎬 Send your video.\n\n"
            "The bot will return "
            "translated.srt.",
            reply_markup=back_menu()
        )

        return

    # --------------------------------------------------------
    # BURN SUBTITLE
    # --------------------------------------------------------

    if data == "video_burn":

        context.user_data[
            "video_mode"
        ] = "auto"

        context.user_data[
            "video_burn"
        ] = True

        await query.edit_message_text(
            "🎞️ BURN SUBTITLE\n\n"
            "🎬 Send your video.\n\n"
            "The translated subtitle "
            "will be burned into the video.",
            reply_markup=back_menu()
        )

        return

    # --------------------------------------------------------
    # TEXT
    # --------------------------------------------------------

    if data == "text_translate":

        context.user_data[
            "text_mode"
        ] = True

        await query.edit_message_text(
            "🌐 TEXT TRANSLATE\n\n"
            "Send Chinese or Khmer text.",
            reply_markup=back_menu()
        )

        return

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    if data == "help":

        await query.edit_message_text(
            "❓ HELP\n\n"
            "🌐 Text Translation\n"
            "🎤 Voice Translation\n"
            "🖼️ OCR Translation\n"
            "🎬 Long Video Translation\n\n"
            "Video supports:\n"
            "• Chinese → Khmer\n"
            "• Khmer → Chinese\n"
            "• Auto Detect\n"
            "• 1–5 hour workflow\n"
            "• Chunk processing\n"
            "• Retry\n"
            "• Resume\n"
            "• SRT\n"
            "• Burn subtitles",
            reply_markup=back_menu()
        )

        return


# ============================================================
# TEXT
# ============================================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    add_user(user)

    if not context.user_data.get(
        "text_mode"
    ):
        return

    text = (
        update.message.text or ""
    ).strip()

    if not text:
        return

    await update.message.reply_text(
        "⏳ Translating..."
    )

    try:

        from langdetect import detect

        from translator import (
            translate_chinese_to_khmer,
            translate_khmer_to_chinese
        )

        detected = detect(
            text
        )

        if detected.startswith(
            "zh"
        ):

            result = (
                translate_chinese_to_khmer(
                    text
                )
            )

            label = "🇨🇳 → 🇰🇭"

        else:

            result = (
                translate_khmer_to_chinese(
                    text
                )
            )

            label = "🇰🇭 → 🇨🇳"

        await update.message.reply_text(
            f"{label}\n\n"
            f"{result}",
            reply_markup=main_menu()
        )

    except Exception as error:

        await update.message.reply_text(
            "❌ Translation failed.\n\n"
            f"{error}",
            reply_markup=main_menu()
        )

    finally:

        context.user_data[
            "text_mode"
        ] = False


# ============================================================
# VIDEO
# ============================================================

async def video_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    add_user(user)

    if not check_license(
        user.id
    ):

        await update.message.reply_text(
            "🔐 License inactive."
        )

        return

    video = update.message.video

    if not video:

        await update.message.reply_text(
            "❌ Please send a video."
        )

        return

    mode = context.user_data.get(
        "video_mode",
        "auto"
    )

    burn = context.user_data.get(
        "video_burn",
        True
    )

    # --------------------------------------------------------
    # DATABASE JOB
    # --------------------------------------------------------

    job_id = create_video_job(
        user.id,
        video.file_name or "video.mp4",
        mode,
        "khmer"
    )

    # --------------------------------------------------------
    # WORK DIRECTORY
    # --------------------------------------------------------

    work_dir = (
        TEMP_DIR /
        f"job_{job_id}"
    )

    work_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    video_path = (
        work_dir /
        "input.mp4"
    )

    status = await update.message.reply_text(
        "🎬 VIDEO TRANSLATION\n\n"
        "⏳ Downloading video..."
    )

    try:

        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        telegram_file = (
            await context.bot.get_file(
                video.file_id
            )
        )

        await telegram_file.download_to_drive(
            custom_path=str(
                video_path
            )
        )

        await status.edit_text(
            "🎬 VIDEO TRANSLATION\n\n"
            "✅ Download complete\n"
            "⏳ Preparing chunks..."
        )

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        last_progress = {
            "value": -1
        }

        loop = asyncio.get_running_loop()

        async def update_progress(
            percent,
            current,
            total,
            message
        ):

            if (
                percent ==
                last_progress["value"]
            ):
                return

            last_progress[
                "value"
            ] = percent

            try:

                await status.edit_text(
                    "🎬 VIDEO TRANSLATION\n\n"
                    f"📊 Progress: "
                    f"{percent}%\n"
                    f"📦 Chunk: "
                    f"{current}/{total}\n"
                    f"⚙️ {message}"
                )

            except Exception:

                pass

        def progress_callback(
            percent,
            current,
            total,
            message
        ):

            asyncio.run_coroutine_threadsafe(
                update_progress(
                    percent,
                    current,
                    total,
                    message
                ),
                loop
            )

        # ----------------------------------------------------
        # PROCESS
        # ----------------------------------------------------

        result = await asyncio.to_thread(
            translate_long_video,
            str(video_path),
            str(work_dir),
            mode,
            None,
            burn,
            progress_callback
        )

        update_video_job(
            job_id,
            "completed"
        )

        # ----------------------------------------------------
        # SRT
        # ----------------------------------------------------

        srt_path = result[
            "srt"
        ]

        with open(
            srt_path,
            "rb"
        ) as file:

            await update.message.reply_document(
                document=file,
                caption=(
                    "📝 SRT READY\n\n"
                    f"📦 Chunks: "
                    f"{result['total_chunks']}\n"
                    "🌐 Chinese ↔ Khmer"
                )
            )

        # ----------------------------------------------------
        # VIDEO
        # ----------------------------------------------------

        output_video = result.get(
            "output_video"
        )

        if output_video:

            await status.edit_text(
                "🎬 VIDEO TRANSLATION\n\n"
                "✅ Processing complete\n"
                "📤 Uploading translated video..."
            )

            with open(
                output_video,
                "rb"
            ) as file:

                await update.message.reply_video(
                    video=file,
                    caption=(
                        "🎬 VIDEO TRANSLATION COMPLETE\n\n"
                        "🌐 Chinese ↔ Khmer\n"
                        "📝 SRT generated\n"
                        "🎞️ Subtitle burned\n"
                        f"📦 Chunks: "
                        f"{result['total_chunks']}"
                    ),
                    supports_streaming=True
                )

        await status.edit_text(
            "✅ VIDEO TRANSLATION COMPLETE\n\n"
            "📝 Subtitle created\n"
            "🎞️ Subtitle burned\n"
            "💾 Processing finished."
        )

    except Exception as error:

        update_video_job(
            job_id,
            "failed"
        )

        print(
            "VIDEO ERROR:",
            repr(error)
        )

        await status.edit_text(
            "❌ VIDEO PROCESSING FAILED\n\n"
            f"{error}\n\n"
            "💾 Checkpoint was kept.\n"
            "You can resume this job "
            "after restarting the bot."
        )
