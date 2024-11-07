from dotenv import load_dotenv
load_dotenv()
from os import getenv
from pathlib import Path

def isFloat(string):
        try:
                float(string)
                return True
        except ValueError:
                return False

def isInt(string):
        try:
                int(string)
                return True
        except ValueError:
                return False

TOKEN = getenv('TOKEN')
WEBHOOK_URL = getenv('WEBHOOK_URL')
if not TOKEN and not WEBHOOK_URL:
        raise ValueError("You must provide one of TOKEN or WEBHOOK_URL.")
if WEBHOOK_URL and not WEBHOOK_URL.startswith('http'):
        raise ValueError("Invalid format for WEBHOOK_URL. Expected 'http' followed by a valid URL.")

channel_id_str = getenv('CHANNEL_ID')
if not isInt(channel_id_str):
        raise ValueError("Invalid format for CHANNEL_ID. Expected a decimal number.")
CHANNEL_ID = int(channel_id_str)

FILES_DIRECTORY = getenv('FILES_DIRECTORY')
if not FILES_DIRECTORY:
        raise ValueError("Missing FILES_DIRECTORY environment variable.")
if not Path(FILES_DIRECTORY).is_dir():
        raise ValueError("FILES_DIRECTORY does not exist or is not a directory.")

FILES_EXTENSION = getenv('FILES_EXTENSION')
if not FILES_EXTENSION:
        raise ValueError("Missing FILES_EXTENSION environment variable.")

str_to_bool = {
        "true": True,
        "false": False
}

recursive_directories_str = getenv('RECURSIVE_DIRECTORIES', "true").strip().lower()
RECURSIVE_DIRECTORIES = str_to_bool.get(recursive_directories_str, True)

seconds_str = getenv('SECONDS', 1.0)
if not isFloat(seconds_str):
        raise ValueError("Invalid format for SECONDS. Expected a decimal number.")
