import src.files_handler as files_handler
from typing import Optional
from pathlib import Path
from time import sleep
# from clips_manipulator import create_clip
from discord_webhook import DiscordWebhook

class Webhook():
        def __init__(
                self,
                url: str | list[str],
                directory: str,
                extension: str | list[str] = "*",
                recursive: bool = False,
                seconds: float = 1.0,
                **kwargs
        ) -> None:
                super().__init__()
                self.webhook_urls = set(url if isinstance(url, list) else [url])
                self.directory = directory
                self.extension = extension
                self.recursive = recursive
                self.seconds = seconds
                self.webhooks = [DiscordWebhook(webhook_url, username="New Files AutoSender", **kwargs) for webhook_url in self.webhook_urls]
        

        def sendMessage(
                self,
                message: str,
                file: Optional[Path] = None
        ):
                print(message)
                for webhook in self.webhooks:
                        webhook.content = message
                        if not file:
                                webhook.execute()
                                continue
                        
                        if not file.is_file():
                                raise Exception("The path provided is not a file: " + file)
                        
                        # sleep(5)
                        # res = create_clip(file, 30)
                        # if res.returncode != 0:
                        #         raise Exception("Failed to create clip: " + str(res.stderr))
                        # file = Path(f"clips/{file.name}")

                        print(f"Sending file: {file.name}")
                        webhook.add_file(file.read_bytes(), file.name)
                        webhook.execute()
                        webhook.remove_files()


        def checkForNewFiles(
                self,
                directory: str,
                extension: str | list[str],
                recursive: bool
        ):
                new_files = files_handler.globNewFiles(directory, extension, recursive)
                if not new_files: return

                self.sendMessage("### New file(s) detected")

                for file in new_files:
                        fileObj = Path(file)
                        file_size = -1
                        while files_handler.isFileBeingUsed(fileObj, file_size):
                                print(f"Waiting for file to stop being used... {file}")
                                file_size = fileObj.stat().st_size
                                sleep(0.5)
                        self.sendMessage(f"New file: {fileObj.name}", fileObj)
                        files_handler.updateFile([file], doAppend=True)
        

        def loop(self):
                self.sendMessage("Successfully started webhook")
                while True:
                        sleep(self.seconds)
                        self.checkForNewFiles(self.directory, self.extension, self.recursive)


if __name__ == "__main__":
        import src.config as config
        webhook = Webhook(
                url=[config.WEBHOOK_URL, "https://discord.com/api/webhooks/1274975754324541463/zVOzPaCyswyYix1K8k1DU7thmedrT6wclki5GBe4y6A7BTMji1gZqrH1-Ao9VKslrlPi"],
                directory=config.FILES_DIRECTORY,
                extension=[config.FILES_EXTENSION, "m4a"],
                recursive=config.RECURSIVE_DIRECTORIES
        )
        webhook.loop()
