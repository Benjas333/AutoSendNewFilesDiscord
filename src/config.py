from os import getenv
from pathlib import Path
from typing import Any, TypeGuard

from dotenv import load_dotenv

_ = load_dotenv()


def is_float(value: Any) -> TypeGuard[float]:  # noqa: ANN401
        if value is None:
                return False

        try:
                _ = float(value)
                return True
        except ValueError:
                return False


def is_int(value: Any) -> TypeGuard[int]:  # noqa: ANN401
        if value is None:
                return False

        try:
                _ = int(value)
                return True
        except ValueError:
                return False


TOKEN = getenv("TOKEN", "")
WEBHOOK_URL = getenv("WEBHOOK_URL", "")
if not TOKEN and not WEBHOOK_URL:
        raise ValueError("You must provide one of TOKEN or WEBHOOK_URL.")

if WEBHOOK_URL and not WEBHOOK_URL.startswith("http"):
        raise ValueError("Invalid format for WEBHOOK_URL. Expected 'http' followed by a valid URL.")

channel_id_str = getenv("CHANNEL_ID")
if not is_int(channel_id_str):
        raise ValueError("Invalid format for CHANNEL_ID. Expected a decimal number.")

CHANNEL_ID = int(channel_id_str)

FILES_DIRECTORY = getenv("FILES_DIRECTORY", "")
if not FILES_DIRECTORY:
        raise ValueError("Missing FILES_DIRECTORY environment variable.")

if not Path(FILES_DIRECTORY).is_dir():
        raise ValueError("FILES_DIRECTORY does not exist or is not a directory.")

FILES_EXTENSION = getenv("FILES_EXTENSION", "")
if not FILES_EXTENSION:
        raise ValueError("Missing FILES_EXTENSION environment variable.")

str_to_bool = {"true": True, "false": False}

recursive_directories_str = getenv("RECURSIVE_DIRECTORIES", "true").strip().lower()
RECURSIVE_DIRECTORIES = str_to_bool.get(recursive_directories_str, True)

seconds_str = getenv("SECONDS", 1.0)
if not is_float(seconds_str):
        raise ValueError("Invalid format for SECONDS. Expected a decimal number.")
