from pathlib import Path
from itertools import chain

FILES_BACKUP = "old_files.txt"


def loadListFromFile():
        if not Path(FILES_BACKUP).exists():
                with open(FILES_BACKUP, 'x'): pass
        
        with open(FILES_BACKUP, 'r', encoding="utf-8") as f:
                return [line.strip() for line in f]


def updateFile(new_list: list[str], doAppend: bool):
        global files
        with open(FILES_BACKUP, 'w' if not doAppend else 'a', encoding="utf-8") as f:
                new_list_str = "\n".join(new_list)
                f.write(new_list_str if not doAppend or not files else "\n" + new_list_str)
        if doAppend:
                files.extend(new_list)
        else:
                files = new_list

files = loadListFromFile()


def globNewFiles(directory: str, extension: str | list[str], recursive: bool = False):
        directory_path = Path(directory)
        match_strings = [f"*.{extension_iter}" for extension_iter in extension] if isinstance(extension, list) else [f"*.{extension}"]
        func = directory_path.glob if not recursive else directory_path.rglob
        all_files = list(map(lambda file: str(file), chain.from_iterable(func(match_string) for match_string in match_strings)))
        new_files = set(all_files).difference(files.copy())
        # updateFile(all_files)
        return new_files


def isFileBeingUsed(file: Path, last_size: int) -> bool:
        return file.stat().st_size > last_size


if __name__ == "__main__":
        import config
        files_list = globNewFiles(config.FILES_DIRECTORY, [config.FILES_EXTENSION, "m4a"], config.RECURSIVE_DIRECTORIES)
        updateFile(files_list, doAppend=True)
        print(files_list)
