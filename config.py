from dotenv import load_dotenv
load_dotenv()
from os import getenv
from pathlib import Path

TOKEN = getenv('TOKEN')
WEBHOOK_URL = getenv('WEBHOOK_URL')
if not TOKEN and not WEBHOOK_URL:
        raise ValueError("You must provide one of TOKEN or WEBHOOK_URL.")
if WEBHOOK_URL and not WEBHOOK_URL.startswith('http'):
        raise ValueError("Invalid format for WEBHOOK_URL. Expected 'http' followed by a valid URL.")

channel_id_str = getenv('CHANNEL_ID')
if len(channel_id_str) > 0 and not channel_id_str.isdecimal():
        raise ValueError("Invalid format for CHANNEL_ID. Expected a decimal number.")
CHANNEL_ID = int(channel_id_str)

CLIPS_DIRECTORY = getenv('CLIPS_DIRECTORY')
if not CLIPS_DIRECTORY:
        raise ValueError("Missing CLIPS_DIRECTORY environment variable.")
if not Path(CLIPS_DIRECTORY).is_dir():
        raise ValueError("CLIPS_DIRECTORY does not exist or is not a directory.")

CLIPS_EXTENSION = getenv('CLIPS_EXTENSION')
if not CLIPS_EXTENSION:
        raise ValueError("Missing CLIPS_EXTENSION environment variable.")

str_to_bool = {
        "true": True,
        "false": False
}

recursive_directories_str = getenv('RECURSIVE_DIRECTORIES', "true").strip().lower()
RECURSIVE_DIRECTORIES = str_to_bool.get(recursive_directories_str, True)

seconds_str = getenv('SECONDS', 1.0)
if isinstance(seconds_str, str) and len(seconds_str) > 0 and not seconds_str.isdecimal():
        raise ValueError("Invalid format for SECONDS. Expected a decimal number.")
