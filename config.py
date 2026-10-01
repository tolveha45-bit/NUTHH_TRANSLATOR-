import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is missing. Please put your Telegram Bot Token in .env"
    )


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/nuthh.db"
)

DATABASE_PATH = BASE_DIR / DATABASE_PATH

TEMP_DIR = BASE_DIR / "temp"
DATA_DIR = BASE_DIR / "data"

TEMP_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


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


DEFAULT_RATE = os.getenv(
    "DEFAULT_RATE",
    "+0%"
)

DEFAULT_PITCH = os.getenv(
    "DEFAULT_PITCH",
    "+0Hz"
)

DEFAULT_VOLUME = os.getenv(
    "DEFAULT_VOLUME",
    "+0%"
)


MAX_TEXT_LENGTH = int(
    os.getenv(
        "MAX_TEXT_LENGTH",
        "5000"
    )
)
