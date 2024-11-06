from dotenv import load_dotenv
load_dotenv()
from os import getenv
from pathlib import Path

TOKEN = getenv('TOKEN')
if not TOKEN:
        raise ValueError("Missing TOKEN environment variable.")
WEBHOOK_URL = getenv('WEBHOOK_URL')
if not WEBHOOK_URL.startswith('http'):
        raise ValueError("Invalid format for WEBHOOK_URL. Expected 'http' followed by a valid URL.")

CHANNEL_ID = int(getenv('CHANNEL_ID'))

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

recursive_directories = getenv('RECURSIVE_DIRECTORIES', "true").strip().lower()
recursive_directories = str_to_bool["true" if not recursive_directories in ["true", "false"] else recursive_directories]

files_backup = "old_clips.txt"


def loadListFromFile():
        with open(files_backup, 'r', encoding="utf-8") as f:
                return [line.strip() for line in f]


def updateFile(new_list: list[str], mode: str = 'w'):
        global files
        if mode == 'w':
                files = new_list
        elif mode == 'a':
                files.extend(new_list)
        with open(files_backup, mode, encoding="utf-8") as f:
                new_list_str = "\n".join(new_list)
                f.write(new_list_str if mode != 'a' else "\n" + new_list_str)

files = loadListFromFile()
