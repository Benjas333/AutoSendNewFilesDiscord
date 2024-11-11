import src.files_handler as files_handler
from src.files_manipulator import uploadFileToLitterbox
from pathlib import Path
from typing import Optional
from time import sleep
from discord_webhook import DiscordWebhook

class Webhook():
        def __init__(
                self,
                directory: str,
                url: str | list[str],
                user: Optional[str] = None,
                extension: str | list[str] = "*",
                recursive: bool = False,
                seconds: float = 1.0,
                litterboxMBThreshold: float = 25.0,
                litterboxExtensions: list[str] = [],
                **kwargs
        ) -> None:
                super().__init__()
                self.webhook_urls = set(url if isinstance(url, list) else [url])
                self.directory = directory
                self.extension = extension
                self.recursive = recursive
                self.seconds = seconds
                self.webhooks = [DiscordWebhook(webhook_url, rate_limit_retry=True, username="New Files AutoSender", **kwargs) for webhook_url in self.webhook_urls]
                self.userPrefix = f"({user}) " if user else ''
                self.litterboxThreshold = litterboxMBThreshold * 1024 * 1024
                self.litterboxExtensions = set(litterboxExtension.lower().removeprefix(".") for litterboxExtension in litterboxExtensions)
        

        def sendMessage(
                self,
                message: str,
                file: Optional[Path] = None
        ):
                message = f"{self.userPrefix}{message}"
                for webhook in self.webhooks:
                        webhook.content = message
                        if not file:
                                webhook.execute()
                                continue
                        
                        if not file.is_file():
                                raise Exception("The path provided is not a file: " + file)

                        print(f"Sending file: {file.name}")
                        if file.stat().st_size >= self.litterboxThreshold or (self.litterboxExtensions and file.suffix.lower().removeprefix('.') in self.litterboxExtensions):
                                webhook.content += "\n" + uploadFileToLitterbox(file)
                        else:
                                webhook.add_file(file.read_bytes(), file.name)
                        webhook.execute()
                        webhook.remove_files()
                print(message)


        def checkForNewFiles(
                self,
                directory: str,
                extension: str | list[str],
                recursive: bool
        ):
                new_files = files_handler.globNewFiles(directory, extension, recursive)
                if not new_files: return

                self.sendMessage("**New file(s) detected**")

                for file in new_files:
                        fileObj = Path(file)
                        file_size = -1
                        while files_handler.isFileBeingUsed(fileObj, file_size):
                                print(f"Waiting for file to stop being used... {file}")
                                file_size = fileObj.stat().st_size
                                sleep(0.5)
                        self.sendMessage(f"New file: `{fileObj.name}`", fileObj)
                        files_handler.updateFile([file], doAppend=True)
        

        def mainloop(self):
                self.sendMessage("Successfully started webhook")
                while True:
                        sleep(self.seconds)
                        self.checkForNewFiles(self.directory, self.extension, self.recursive)


if __name__ == "__main__":
        import src.config as config
        webhook = Webhook(
                url=[config.WEBHOOK_URL],
                directory=config.FILES_DIRECTORY,
                extension=[config.FILES_EXTENSION, "m4a"],
                recursive=config.RECURSIVE_DIRECTORIES,
                litterboxExtensions=["mp4"]
        )
        webhook.mainloop()
