import asyncio
import uuid
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from config import (
    TEMP_DIR,
    MAX_TEXT_LENGTH
)

from database import (
    add_or_update_user,
    get_user,
    update_voice_settings,
    save_voice_history,
    save_translation
)

from keyboards import (
    main_menu,
    voice_menu,
    gender_menu,
    speed_menu,
    pitch_menu,
    back_menu
)

from translator import (
    chinese_to_khmer,
    khmer_to_chinese,
    detect_and_translate
)

from whisper_stt import transcribe_audio

from voice_tts import generate_voice_sync

from license import check_license

from utils import safe_remove


# =========================================================
# START
# =========================================================

async def start_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    add_or_update_user(user)

    await update.message.reply_text(
        "🤖 *NUTHH Translator*\n\n"
        "🌐 Chinese ↔ Khmer\n"
        "🎤 Voice AI\n"
        "📝 Speech-to-Text\n"
        "🔊 Text-to-Speech\n"
        "👨 Male / 👩 Female / 🧑 Neutral\n"
        "🎬 Video Translation\n\n"
        "Choose a feature below:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )


# =========================================================
# CALLBACK
# =========================================================

async def callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    data = query.data

    # -----------------------------------------------------
    # MAIN
    # -----------------------------------------------------

    if data == "back_main":

        await query.edit_message_text(
            "🏠 *NUTHH Translator Main Menu*",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )

        return

    # -----------------------------------------------------
    # VOICE AI
    # -----------------------------------------------------

    if data == "voice_ai":

        await query.edit_message_text(
            "🎤 *VOICE AI*\n\n"
            "Send me a voice message.\n\n"
            "The bot will:\n"
            "1️⃣ Convert speech → text\n"
            "2️⃣ Detect language\n"
            "3️⃣ Translate\n"
            "4️⃣ Generate AI voice\n"
            "5️⃣ Send translated audio\n\n"
            "Current voice settings are saved automatically.",
            reply_markup=voice_menu(),
            parse_mode="Markdown"
        )

        return

    # -----------------------------------------------------
    # VOICE STUDIO
    # -----------------------------------------------------

    if data == "voice_studio":

        user = get_user(user_id)

        gender = (
            user["voice_gender"]
            if user
            else "female"
        )

        voice_name = (
            user["voice_name"]
            if user
            else ""
        )

        rate = (
            user["voice_rate"]
            if user
            else "+0%"
        )

        pitch = (
            user["voice_pitch"]
            if user
            else "+0Hz"
        )

        text = (
            "🔊 *VOICE STUDIO*\n\n"
            f"👤 Gender: `{gender}`\n"
            f"🎙️ Voice: `{voice_name or 'Auto'}`\n"
            f"⚡ Speed: `{rate}`\n"
            f"🎚️ Pitch: `{pitch}`\n\n"
            "Choose a setting:"
        )

        await query.edit_message_text(
            text,
            reply_markup=voice_menu(),
            parse_mode="Markdown"
        )

        return

    # -----------------------------------------------------
    # GENDER
    # -----------------------------------------------------

    if data == "voice_gender_male":

        update_voice_settings(
            user_id,
            gender="male"
        )

        await query.edit_message_text(
            "👨 *Male Voice Selected*\n\n"
            "All future Voice AI responses will use "
            "the male voice profile.",
            reply_markup=voice_menu(),
            parse_mode="Markdown"
        )

        return

    if data == "voice_gender_female":

        update_voice_settings(
            user_id,
            gender="female"
        )

        await query.edit_message_text(
            "👩 *Female Voice Selected*\n\n"
            "All future Voice AI responses will use "
            "the female voice profile.",
            reply_markup=voice_menu(),
            parse_mode="Markdown"
        )

        return

    if data == "voice_gender_neutral":

        update_voice_settings(
            user_id,
            gender="neutral"
        )

        await query.edit_message_text(
            "🧑 *Neutral Voice Selected*",
            reply_markup=voice_menu(),
            parse_mode="Markdown"
        )

        return

    # -----------------------------------------------------
    # SPEED
    # -----------------------------------------------------

    if data == "voice_speed":

        await query.edit_message_text(
            "⚡ *VOICE SPEED*\n\n"
            "Choose speech speed:",
            reply_markup=speed_menu(),
            parse_mode="Markdown"
        )

        return

    speed_map = {

        "speed_75": "-25%",
        "speed_100": "+0%",
        "speed_125": "+25%",
        "speed_150": "+50%",
        "speed_200": "+100%"
    }

    if data in speed_map:

        update_voice_settings(
            user_id,
            rate=speed_map[data]
        )

        await query.edit_message_text(
            f"⚡ Speed set to `{speed_map[data]}`",
            reply_markup=voice_menu(),
            parse_mode="Markdown"
        )

        return

    # -----------------------------------------------------
    # PITCH
    # -----------------------------------------------------

    if data == "voice_pitch":

        await query.edit_message_text(
            "🎚️ *VOICE PITCH*\n\n"
            "Choose pitch:",
            reply_markup=pitch_menu(),
            parse_mode="Markdown"
        )

        return

    pitch_map = {

        "pitch_low": "-20Hz",
        "pitch_normal": "+0Hz",
        "pitch_high": "+20Hz"
    }

    if data in pitch_map:

        update_voice_settings(
            user_id,
            pitch=pitch_map[data]
        )

        await query.edit_message_text(
            f"🎚️ Pitch set to `{pitch_map[data]}`",
            reply_markup=voice_menu(),
            parse_mode="Markdown"
        )

        return

    # -----------------------------------------------------
    # VOICE TRANSLATION MODE
    # -----------------------------------------------------

    if data == "voice_zh_km":

        context.user_data["voice_mode"] = "zh_km"

        await query.edit_message_text(
            "🇨🇳 → 🇰🇭 *Chinese → Khmer*\n\n"
            "Now send a Chinese voice message.",
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )

        return

    if data == "voice_km_zh":

        context.user_data["voice_mode"] = "km_zh"

        await query.edit_message_text(
            "🇰🇭 → 🇨🇳 *Khmer → Chinese*\n\n"
            "Now send a Khmer voice message.",
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )

        return

    if data == "voice_auto":

        context.user_data["voice_mode"] = "auto"

        await query.edit_message_text(
            "🤖 *Auto Detect Mode*\n\n"
            "Send any supported voice message.",
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )

        return

    # -----------------------------------------------------
    # HISTORY
    # -----------------------------------------------------

    if data == "voice_history":

        await query.edit_message_text(
            "🎧 *Voice History*\n\n"
            "Voice history database is enabled.\n\n"
            "Previous generated files are stored "
            "as metadata for your account.",
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )

        return

    # -----------------------------------------------------
    # TEXT
    # -----------------------------------------------------

    if data == "text_translate":

        context.user_data["text_mode"] = True

        await query.edit_message_text(
            "🌐 *TEXT TRANSLATION*\n\n"
            "Send Chinese or Khmer text.",
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )

        return

    # -----------------------------------------------------
    # HELP
    # -----------------------------------------------------

    if data == "help":

        await query.edit_message_text(
            "❓ *NUTHH Translator Help*\n\n"
            "🌐 Text Translation\n"
            "🎤 Voice AI\n"
            "🖼️ OCR\n"
            "🎬 Video Translation\n"
            "📩 Forward Translation\n"
            "🔊 Voice Studio\n\n"
            "Voice AI supports:\n"
            "👨 Male\n"
            "👩 Female\n"
            "🧑 Neutral\n"
            "⚡ Speed\n"
            "🎚️ Pitch",
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )

        return

    # -----------------------------------------------------
    # OTHER FEATURES
    # -----------------------------------------------------

    if data in (
        "ocr",
        "forward_translate",
        "video_translate",
        "history",
        "favorites",
        "settings"
    ):

        await query.edit_message_text(
            "🚧 This module is ready to be connected "
            "to the full NUTHH Translator system.",
            reply_markup=back_menu()
        )

        return


# =========================================================
# TEXT HANDLER
# =========================================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:

        return

    text = update.message.text.strip()

    if not text:

        return

    if len(text) > MAX_TEXT_LENGTH:

        await update.message.reply_text(
            f"⚠️ Text is too long.\n"
            f"Maximum: {MAX_TEXT_LENGTH} characters."
        )

        return

    user = update.effective_user

    add_or_update_user(user)

    try:

        translated, source, target = (
            detect_and_translate(text)
        )

        save_translation(
            user.id,
            text,
            translated,
            source,
            target
        )

        await update.message.reply_text(
            f"🌐 *Translation*\n\n"
            f"Original:\n"
            f"`{text}`\n\n"
            f"Translation:\n"
            f"*{translated}*",
            parse_mode="Markdown"
        )

    except Exception as e:

        print(
            f"[Text Translation Error] {e}"
        )

        await update.message.reply_text(
            "❌ Translation failed.\n"
            "Please try again."
        )


# =========================================================
# VOICE HANDLER
# =========================================================

async def voice_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.message

    user = update.effective_user

    if not check_license(user.id):

        await message.reply_text(
            "🔐 Your Voice AI license is not active."
        )

        return

    status = await message.reply_text(
        "🎤 Receiving voice...\n"
        "⏳ Please wait..."
    )

    work_id = uuid.uuid4().hex

    work_dir = (
        TEMP_DIR /
        f"voice_{user.id}_{work_id}"
    )

    work_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    input_audio = (
        work_dir /
        "input.ogg"
    )

    output_audio = (
        work_dir /
        "translated.mp3"
    )

    try:

        # -------------------------------------------------
        # DOWNLOAD
        # -------------------------------------------------

        telegram_file = await message.voice.get_file()

        await telegram_file.download_to_drive(
            custom_path=str(input_audio)
        )

        await status.edit_text(
            "🎤 Voice received.\n"
            "🧠 Converting speech to text..."
        )

        # -------------------------------------------------
        # STT
        # -------------------------------------------------

        detected_language, segments = await asyncio.to_thread(
            transcribe_audio,
            str(input_audio),
            None
        )

        if not segments:

            await status.edit_text(
                "❌ Could not recognize speech."
            )

            return

        original_text = " ".join(
            segment["text"]
            for segment in segments
        ).strip()

        if not original_text:

            await status.edit_text(
                "❌ No speech detected."
            )

            return

        # -------------------------------------------------
        # DETERMINE LANGUAGE
        # -------------------------------------------------

        mode = context.user_data.get(
            "voice_mode",
            "auto"
        )

        if mode == "zh_km":

            source_language = "zh"
            target_language = "km"

        elif mode == "km_zh":

            source_language = "km"
            target_language = "zh"

        else:

            source_language = (
                detected_language
                or "unknown"
            )

            if source_language.startswith("zh"):

                source_language = "zh"
                target_language = "km"

            elif source_language == "km":

                source_language = "km"
                target_language = "zh"

            else:

                # Try language detection from text
                from langdetect import detect

                detected = detect(
                    original_text
                )

                if detected.startswith("zh"):

                    source_language = "zh"
                    target_language = "km"

                elif detected == "km":

                    source_language = "km"
                    target_language = "zh"

                else:

                    await status.edit_text(
                        "⚠️ Currently this Voice AI "
                        "workflow supports Chinese and Khmer."
                    )

                    return

        # -------------------------------------------------
        # TRANSLATE
        # -------------------------------------------------

        await status.edit_text(
            "🌐 Translating..."
        )

        if (
            source_language == "zh"
            and target_language == "km"
        ):

            translated_text = await asyncio.to_thread(
                chinese_to_khmer,
                original_text
            )

        elif (
            source_language == "km"
            and target_language == "zh"
        ):

            translated_text = await asyncio.to_thread(
                khmer_to_chinese,
                original_text
            )

        else:

            raise ValueError(
                "Unsupported translation direction."
            )

        # -------------------------------------------------
        # USER VOICE SETTINGS
        # -------------------------------------------------

        user_settings = get_user(user.id)

        gender = (
            user_settings["voice_gender"]
            if user_settings
            else "female"
        )

        rate = (
            user_settings["voice_rate"]
            if user_settings
            else "+0%"
        )

        pitch = (
            user_settings["voice_pitch"]
            if user_settings
            else "+0Hz"
        )

        volume = (
            user_settings["voice_volume"]
            if user_settings
            else "+0%"
        )

        # -------------------------------------------------
        # TTS
        # -------------------------------------------------

        await status.edit_text(
            "🔊 Generating AI voice..."
        )

        await asyncio.to_thread(
            generate_voice_sync,
            translated_text,
            target_language,
            gender,
            output_audio,
            rate,
            pitch,
            volume
        )

        # -------------------------------------------------
        # SAVE HISTORY
        # -------------------------------------------------

        save_voice_history(
            user.id,
            original_text,
            translated_text,
            source_language,
            target_language,
            user_settings["voice_name"]
            if user_settings
            else "",
            gender,
            str(output_audio)
        )

        # -------------------------------------------------
        # SEND RESULT
        # -------------------------------------------------

        await status.edit_text(
            "✅ Voice translation complete!"
        )

        await message.reply_text(
            "📝 *Original*\n"
            f"{original_text}\n\n"
            "🌐 *Translation*\n"
            f"{translated_text}\n\n"
            f"🎙️ Voice: `{gender}`\n"
            f"⚡ Speed: `{rate}`\n"
            f"🎚️ Pitch: `{pitch}`",
            parse_mode="Markdown"
        )

        with open(
            output_audio,
            "rb"
        ) as audio_file:

            await message.reply_audio(
                audio=audio_file,
                title="NUTHH AI Voice Translation",
                performer="NUTHH Translator"
            )

    except Exception as e:

        print(
            f"[Voice Error] {repr(e)}"
        )

        await status.edit_text(
            "❌ Voice translation failed.\n\n"
            "Please try again."
        )

    finally:

        # Wait a little before cleanup
        await asyncio.sleep(2)

        safe_remove(
            work_dir
        )


# =========================================================
# UNKNOWN / DOCUMENT
# =========================================================

async def document_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "📄 Document received.\n"
        "Document translation module can be connected here."
    )
