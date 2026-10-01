import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent


BOT_TOKEN = os.getenv(
    "BOT_TOKEN",
    ""
)


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    str(BASE_DIR / "data" / "nuthh.db")
)


TEMP_DIR = BASE_DIR / "temp"


WHISPER_MODEL = os.getenv(
    "WHISPER_MODEL",
    "small"
)


WHISPER_DEVICE = os.getenv(
    "WHISPER_DEVICE",
    "cpu"
)


WHISPER_COMPUTE_TYPE = os.getenv(
    "WHISPER_COMPUTE_TYPE",
    "int8"
)


MAX_VIDEO_SIZE_MB = int(
    os.getenv(
        "MAX_VIDEO_SIZE_MB",
        "200"
    )
)


VIDEO_CHUNK_MINUTES = int(
    os.getenv(
        "VIDEO_CHUNK_MINUTES",
        "10"
    )
)


VIDEO_MAX_RETRIES = int(
    os.getenv(
        "VIDEO_MAX_RETRIES",
        "3"
    )
)


TEMP_DIR.mkdir(
    parents=True,
    exist_ok=True
)


Path(
    DATABASE_PATH
).parent.mkdir(
    parents=True,
    exist_ok=True
)


if not BOT_TOKEN:

    raise RuntimeError(
        "BOT_TOKEN is missing. "
        "Please add it to .env"
    )
