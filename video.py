import json
import math
import os
import shutil
import subprocess
import time

from pathlib import Path


from config import (
    VIDEO_CHUNK_MINUTES,
    VIDEO_MAX_RETRIES
)

from whisper_stt import (
    transcribe_audio
)

from translator import (
    translate_chinese_to_khmer,
    translate_khmer_to_chinese
)

from subtitle import (
    create_translated_srt
)


# ============================================================
# COMMAND
# ============================================================

def run_command(
    command,
    retries=VIDEO_MAX_RETRIES
):

    last_error = ""

    for attempt in range(
        1,
        retries + 1
    ):

        try:

            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode == 0:

                return result

            last_error = result.stderr

            print(
                f"Command failed "
                f"{attempt}/{retries}"
            )

        except Exception as error:

            last_error = str(error)

            print(
                f"Command error "
                f"{attempt}/{retries}: "
                f"{error}"
            )

        if attempt < retries:

            time.sleep(
                attempt * 2
            )

    raise RuntimeError(
        "Command failed:\n"
        + last_error
    )


# ============================================================
# DURATION
# ============================================================

def get_video_duration(
    video_path
):

    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ]

    result = run_command(
        command
    )

    try:

        return float(
            result.stdout.strip()
        )

    except Exception:

        raise RuntimeError(
            "Cannot detect video duration."
        )


# ============================================================
# CHECKPOINT
# ============================================================

def get_checkpoint_path(
    work_dir
):

    return (
        Path(work_dir) /
        "checkpoint.json"
    )


def load_checkpoint(
    work_dir
):

    path = get_checkpoint_path(
        work_dir
    )

    if not path.exists():

        return {
            "completed_chunks": [],
            "segments": []
        }

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return {
            "completed_chunks":
                data.get(
                    "completed_chunks",
                    []
                ),
            "segments":
                data.get(
                    "segments",
                    []
                )
        }

    except Exception:

        return {
            "completed_chunks": [],
            "segments": []
        }


def save_checkpoint(
    work_dir,
    data
):

    path = get_checkpoint_path(
        work_dir
    )

    temporary = (
        str(path) +
        ".tmp"
    )

    with open(
        temporary,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

    os.replace(
        temporary,
        path
    )


# ============================================================
# AUDIO CHUNK
# ============================================================

def extract_audio_chunk(
    video_path,
    output_path,
    start,
    duration
):

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    command = [
        "ffmpeg",
        "-y",

        "-ss",
        str(start),

        "-i",
        str(video_path),

        "-t",
        str(duration),

        "-vn",

        "-ac",
        "1",

        "-ar",
        "16000",

        "-c:a",
        "pcm_s16le",

        str(output_path)
    ]

    run_command(
        command
    )

    if not output_path.exists():

        raise RuntimeError(
            "Audio chunk was not created."
        )


# ============================================================
# CREATE CHUNKS
# ============================================================

def create_chunks(
    video_path,
    work_dir,
    chunk_minutes
):

    duration = get_video_duration(
        video_path
    )

    chunk_seconds = (
        chunk_minutes * 60
    )

    total = math.ceil(
        duration /
        chunk_seconds
    )

    chunks_dir = (
        Path(work_dir) /
        "chunks"
    )

    chunks_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    chunks = []

    for index in range(total):

        start = (
            index *
            chunk_seconds
        )

        end = min(
            start +
            chunk_seconds,
            duration
        )

        chunks.append(
            {
                "index": index,
                "start": start,
                "end": end,
                "duration":
                    end - start,
                "audio": str(
                    chunks_dir /
                    f"chunk_{index:05d}.wav"
                )
            }
        )

    return chunks


# ============================================================
# TRANSLATION
# ============================================================

def translate_segment(
    text,
    source,
    target
):

    if (
        source == "zh"
        and target == "km"
    ):

        return translate_chinese_to_khmer(
            text
        )

    if (
        source == "km"
        and target == "zh"
    ):

        return translate_khmer_to_chinese(
            text
        )

    if target == "km":

        return translate_chinese_to_khmer(
            text
        )

    return translate_khmer_to_chinese(
        text
    )


# ============================================================
# PROCESS CHUNK
# ============================================================

def process_chunk(
    video_path,
    chunk,
    mode,
    checkpoint,
    work_dir
):

    index = chunk["index"]

    audio_path = Path(
        chunk["audio"]
    )

    # --------------------------------------------------------
    # Extract audio
    # --------------------------------------------------------

    if not audio_path.exists():

        extract_audio_chunk(
            video_path,
            audio_path,
            chunk["start"],
            chunk["duration"]
        )

    # --------------------------------------------------------
    # Whisper
    # --------------------------------------------------------

    whisper_language = None

    if mode == "zh_km":

        whisper_language = "zh"

    elif mode == "km_zh":

        whisper_language = "km"

    detected_language, segments = (
        transcribe_audio(
            str(audio_path),
            whisper_language
        )
    )

    # --------------------------------------------------------
    # No speech
    # --------------------------------------------------------

    if not segments:

        checkpoint[
            "completed_chunks"
        ].append(index)

        save_checkpoint(
            work_dir,
            checkpoint
        )

        return []

    # --------------------------------------------------------
    # Language
    # --------------------------------------------------------

    if mode == "zh_km":

        source = "zh"
        target = "km"

    elif mode == "km_zh":

        source = "km"
        target = "zh"

    else:

        if detected_language.startswith(
            "zh"
        ):

            source = "zh"
            target = "km"

        elif detected_language.startswith(
            "km"
        ):

            source = "km"
            target = "zh"

        else:

            source = detected_language
            target = "km"

    # --------------------------------------------------------
    # Translate
    # --------------------------------------------------------

    translated_segments = []

    for segment in segments:

        original = (
            segment["text"]
            .strip()
        )

        if not original:

            continue

        absolute_start = (
            chunk["start"] +
            segment["start"]
        )

        absolute_end = (
            chunk["start"] +
            segment["end"]
        )

        try:

            translated = (
                translate_segment(
                    original,
                    source,
                    target
                )
            )

        except Exception as error:

            print(
                "Translation error:",
                error
            )

            translated = original

        translated_segments.append(
            {
                "start":
                    absolute_start,

                "end":
                    absolute_end,

                "text":
                    original,

                "translated_text":
                    translated
            }
        )

    # --------------------------------------------------------
    # Save checkpoint
    # --------------------------------------------------------

    if index not in (
        checkpoint[
            "completed_chunks"
        ]
    ):

        checkpoint[
            "completed_chunks"
        ].append(index)

    checkpoint[
        "segments"
    ].extend(
        translated_segments
    )

    save_checkpoint(
        work_dir,
        checkpoint
    )

    return translated_segments


# ============================================================
# LONG VIDEO
# ============================================================

def process_long_video(
    video_path,
    work_dir,
    mode="auto",
    chunk_minutes=VIDEO_CHUNK_MINUTES,
    progress_callback=None
):

    video_path = Path(
        video_path
    )

    work_dir = Path(
        work_dir
    )

    work_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    chunks = create_chunks(
        video_path,
        work_dir,
        chunk_minutes
    )

    total_chunks = len(
        chunks
    )

    checkpoint = load_checkpoint(
        work_dir
    )

    completed = set(
        checkpoint[
            "completed_chunks"
        ]
    )

    for position, chunk in enumerate(
        chunks,
        start=1
    ):

        index = chunk["index"]

        # ----------------------------------------------------
        # RESUME
        # ----------------------------------------------------

        if index in completed:

            percent = int(
                position /
                total_chunks *
                100
            )

            if progress_callback:

                progress_callback(
                    percent,
                    position,
                    total_chunks,
                    "Resumed"
                )

            continue

        # ----------------------------------------------------
        # RETRY
        # ----------------------------------------------------

        success = False

        last_error = None

        for attempt in range(
            1,
            VIDEO_MAX_RETRIES + 1
        ):

            try:

                if progress_callback:

                    percent = int(
                        (
                            position - 1
                        )
                        /
                        total_chunks
                        *
                        100
                    )

                    progress_callback(
                        percent,
                        position,
                        total_chunks,
                        f"Processing "
                        f"attempt "
                        f"{attempt}/"
                        f"{VIDEO_MAX_RETRIES}"
                    )

                process_chunk(
                    video_path,
                    chunk,
                    mode,
                    checkpoint,
                    work_dir
                )

                success = True

                break

            except Exception as error:

                last_error = error

                print(
                    f"Chunk {index} "
                    f"failed: "
                    f"{error}"
                )

                if attempt < (
                    VIDEO_MAX_RETRIES
                ):

                    time.sleep(
                        attempt * 3
                    )

        if not success:

            raise RuntimeError(
                f"Chunk {index + 1} "
                f"failed after "
                f"{VIDEO_MAX_RETRIES} "
                f"attempts: "
                f"{last_error}"
            )

        percent = int(
            position /
            total_chunks *
            100
        )

        if progress_callback:

            progress_callback(
                percent,
                position,
                total_chunks,
                "Chunk completed"
            )

    # --------------------------------------------------------
    # Sort segments
    # --------------------------------------------------------

    segments = checkpoint[
        "segments"
    ]

    segments.sort(
        key=lambda x:
        x["start"]
    )

    checkpoint[
        "segments"
    ] = segments

    save_checkpoint(
        work_dir,
        checkpoint
    )

    # --------------------------------------------------------
    # SRT
    # --------------------------------------------------------

    srt_path = (
        work_dir /
        "translated.srt"
    )

    create_translated_srt(
        segments,
        srt_path
    )

    return {
        "srt":
            str(srt_path),

        "segments":
            segments,

        "total_chunks":
            total_chunks
    }


# ============================================================
# SUBTITLE PATH
# ============================================================

def escape_subtitle_path(
    path
):

    path = (
        Path(path)
        .resolve()
        .as_posix()
    )

    path = path.replace(
        "\\",
        "\\\\"
    )

    path = path.replace(
        ":",
        "\\:"
    )

    path = path.replace(
        "'",
        "\\'"
    )

    return path


# ============================================================
# BURN SUBTITLE
# ============================================================

def burn_subtitles(
    video_path,
    subtitle_path,
    output_path
):

    subtitle = (
        escape_subtitle_path(
            subtitle_path
        )
    )

    video_filter = (
        f"subtitles='{subtitle}'"
    )

    command = [
        "ffmpeg",
        "-y",

        "-i",
        str(video_path),

        "-vf",
        video_filter,

        "-c:v",
        "libx264",

        "-preset",
        "veryfast",

        "-crf",
        "23",

        "-c:a",
        "aac",

        "-b:a",
        "128k",

        "-movflags",
        "+faststart",

        str(output_path)
    ]

    run_command(
        command
    )

    if not Path(
        output_path
    ).exists():

        raise RuntimeError(
            "Output video was not created."
        )

    return output_path


# ============================================================
# COMPLETE PIPELINE
# ============================================================

def translate_long_video(
    video_path,
    work_dir,
    mode="auto",
    chunk_minutes=VIDEO_CHUNK_MINUTES,
    burn=True,
    progress_callback=None
):

    result = process_long_video(
        video_path,
        work_dir,
        mode,
        chunk_minutes,
        progress_callback
    )

    output_video = None

    if burn:

        output_video = (
            Path(work_dir) /
            "translated_video.mp4"
        )

        if progress_callback:

            progress_callback(
                100,
                result[
                    "total_chunks"
                ],
                result[
                    "total_chunks"
                ],
                "Burning subtitles"
            )

        burn_subtitles(
            video_path,
            result["srt"],
            output_video
        )

    return {
        **result,
        "output_video":
            str(output_video)
            if output_video
            else None
    }


# ============================================================
# CLEANUP
# ============================================================

def cleanup_job(
    work_dir
):

    work_dir = Path(
        work_dir
    )

    if work_dir.exists():

        shutil.rmtree(
            work_dir,
            ignore_errors=True
        )
