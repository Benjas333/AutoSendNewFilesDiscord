import config
from pathlib import Path


def globClips(directory: str):
        directory_path = Path(directory)
        match_string = f"*.{config.CLIPS_EXTENSION}"
        all_files = list(map(lambda file: str(file), directory_path.glob(match_string) if not config.recursive_directories else directory_path.rglob(match_string)))
        new_clips = set(all_files).difference(config.files.copy())
        # config.updateFile(all_files)
        return new_clips

def isFileBeingUsed(file: Path, last_size: int) -> bool:
        return file.stat().st_size > last_size

if __name__ == "__main__":
        clips_list = globClips(config.CLIPS_DIRECTORY)
        print(clips_list)
