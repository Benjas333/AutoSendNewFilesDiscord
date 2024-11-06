from pathlib import Path

files_backup = "old_clips.txt"


def loadListFromFile():
        if not Path(files_backup).exists():
                with open(files_backup, 'x'): pass
        
        with open(files_backup, 'r', encoding="utf-8") as f:
                return [line.strip() for line in f]


def updateFile(new_list: list[str], doAppend: bool):
        global files
        with open(files_backup, 'w' if not doAppend else 'a', encoding="utf-8") as f:
                new_list_str = "\n".join(new_list)
                f.write(new_list_str if not doAppend or not files else "\n" + new_list_str)
        if doAppend:
                files.extend(new_list)
        else:
                files = new_list

files = loadListFromFile()


def globNewFiles(directory: str, extension: str, recursive: bool = False):
        directory_path = Path(directory)
        match_string = f"*.{extension}"
        all_files = list(map(lambda file: str(file), directory_path.glob(match_string) if not recursive else directory_path.rglob(match_string)))
        new_files = set(all_files).difference(files.copy())
        # updateFile(all_files)
        return new_files


def isFileBeingUsed(file: Path, last_size: int) -> bool:
        return file.stat().st_size > last_size


if __name__ == "__main__":
        import config
        clips_list = globNewFiles(config.CLIPS_DIRECTORY, config.CLIPS_EXTENSION, config.recursive_directories)
        updateFile(clips_list, doAppend=True)
        print(clips_list)
