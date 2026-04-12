from __future__ import annotations

from pathlib import Path
from time import sleep
from typing import Any

from discord_webhook import DiscordWebhook

import src.files_handler as files_handler
from src.files_manipulator import upload_file_to_litterbox

_seconds = 1.0


class Webhook:
        def __init__(
                self,
                directory: str,
                url: str | list[str],
                user: str | None = None,
                extension: str | list[str] = "*",
                *,
                recursive: bool = False,
                seconds: float = _seconds,
                litterbox_mb_threshold: float = 25.0,
                litterbox_extensions: list[str] | None = None,
                **kwargs: dict[str, Any],
        ) -> None:
                super().__init__()
                self.webhook_urls: set[str] = set(url if isinstance(url, list) else [url])
                self.directory: str = directory
                self.extension: str | list[str] = extension
                self.recursive: bool = recursive
                self.seconds: float = seconds
                self.webhooks: list[DiscordWebhook] = [
                        DiscordWebhook(
                                webhook_url,
                                rate_limit_retry=True,
                                username="New Files AutoSender",
                                **kwargs,
                        )
                        for webhook_url in self.webhook_urls
                ]
                self.userPrefix: str = f"({user}) " if user else ""
                self.litterboxThreshold: float = litterbox_mb_threshold * 1024 * 1024
                self.litterboxExtensions: set[str] = {
                        litterboxExtension.lower().removeprefix(".") for litterboxExtension in litterbox_extensions or []
                }

        def send_message(self, message: str, file: Path | None = None) -> None:
                message = f"{self.userPrefix}{message}"
                for webhook in self.webhooks:
                        webhook.content = message
                        if not file:
                                _ = webhook.execute()
                                continue

                        if not file.is_file():
                                raise Exception(f"The path provided is not a file: {file}")

                        file_stats = file.stat()
                        if file_stats.st_size >= 1024**3:
                                print(f"{file.name} size is bigger than 1 GB! Skipped")
                                continue

                        print(f"Sending file: {file.name}")
                        if file_stats.st_size >= self.litterboxThreshold or (
                                self.litterboxExtensions
                                and file.suffix.lower().removeprefix(".") in self.litterboxExtensions
                        ):
                                webhook.content += "\n" + upload_file_to_litterbox(file)
                        else:
                                webhook.add_file(file.read_bytes(), file.name)
                        _ = webhook.execute()
                        webhook.remove_files()
                print(message)

        def check_for_new_files(self, directory: str, extension: str | list[str], *, recursive: bool) -> None:
                new_files = files_handler.glob_new_files(directory, extension, recursive=recursive)
                if not new_files:
                        return

                self.send_message("**New file(s) detected**")

                for file in new_files:
                        file_path = Path(file)
                        file_size = -1
                        while files_handler.is_file_being_used(file_path, file_size):
                                print(f"Waiting for file to stop being used... {file}")
                                file_size = file_path.stat().st_size
                                sleep(0.5)
                        self.send_message(f"New file: `{file_path.name}`", file_path)
                        files_handler.update_file([file], should_append=True)

        def mainloop(self) -> None:
                self.send_message("Successfully started webhook")
                while True:
                        sleep(self.seconds)
                        self.check_for_new_files(self.directory, self.extension, recursive=self.recursive)


if __name__ == "__main__":
        import src.config as config

        webhook = Webhook(
                url=[config.WEBHOOK_URL],
                directory=config.FILES_DIRECTORY,
                extension=[config.FILES_EXTENSION, "m4a"],
                recursive=config.RECURSIVE_DIRECTORIES,
                litterbox_extensions=["mp4"],
        )
        webhook.mainloop()
