from pathlib import Path

import trio

FILES_BACKUP = "old_files.txt"


def load_list_from_file() -> list[str]:
        if not Path(FILES_BACKUP).exists():
                with open(FILES_BACKUP, "x"):
                        pass

        with open(FILES_BACKUP, encoding="utf-8") as f:
                return [line.strip() for line in f]


def update_file(new_list: list[str] | set[str], *, should_append: bool) -> None:
        global files
        with open(FILES_BACKUP, "w" if not should_append else "a", encoding="utf-8") as f:
                new_list_str = "\n".join(new_list)
                _ = f.write(new_list_str if not should_append or not files else "\n" + new_list_str)
        if should_append:
                files.extend(new_list)
        else:
                files = new_list


files = load_list_from_file()


def glob_new_files(directory: str, extension: str | list[str], *, recursive: bool = False) -> set[str]:
        directory_path = Path(directory)
        match_strings = [f"*.{ext}" for ext in extension] if isinstance(extension, list) else [f"*.{extension}"]
        func = directory_path.glob if not recursive else directory_path.rglob
        all_files: set[str] = {str(file) for match_string in match_strings for file in func(match_string)}
        return all_files.difference(files)


def is_file_being_used(file: Path, last_size: int) -> bool:
        return file.stat().st_size > last_size


async def async_is_file_being_used(file: trio.Path, last_size: int) -> bool:
        return (await file.stat()).st_size > last_size


if __name__ == "__main__":
        import config

        files_list = glob_new_files(
                config.FILES_DIRECTORY,
                [config.FILES_EXTENSION, "m4a"],
                recursive=config.RECURSIVE_DIRECTORIES,
        )
        update_file(files_list, should_append=True)
        print(files_list)
