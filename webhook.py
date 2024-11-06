import files_handler
from typing import Optional
from pathlib import Path
from time import sleep
# from clips_manipulator import create_clip
from discord_webhook import DiscordWebhook

class Webhook(DiscordWebhook):
        def __init__(
                self,
                url: str,
                directory: str,
                extension = "*",
                recursive = False,
                seconds: float = 1.0,
                **kwargs
        ) -> None:
                super().__init__(url, username="New Files AutoSender", **kwargs)
                self.directory = directory
                self.extension = extension
                self.recursive = recursive
                self.seconds = seconds
        

        def sendMessage(
                self,
                message: str,
                file: Optional[Path] = None
        ):
                print(message)
                self.content = message
                if not file:
                        self.execute()
                        return
                
                if not file.is_file():
                        raise Exception("The path provided is not a file: " + file)
                
                # sleep(5)
                # res = create_clip(file, 30)
                # if res.returncode != 0:
                #         raise Exception("Failed to create clip: " + str(res.stderr))
                # file = Path(f"clips/{file.name}")

                print(f"Sending file: {file.name}")
                self.add_file(file.read_bytes(), file.name)
                self.execute()
                self.remove_files()


        def checkForNewFiles(
                self,
                directory: str,
                extension: str,
                recursive: bool
        ):
                new_clips = files_handler.globNewFiles(directory, extension, recursive)
                if not new_clips: return

                self.sendMessage("### New file(s) detected")

                for clip in new_clips:
                        clipObj = Path(clip)
                        file_size = -1
                        while files_handler.isFileBeingUsed(clipObj, file_size):
                                print(f"Waiting for file to stop being used... {clip}")
                                file_size = clipObj.stat().st_size
                                sleep(0.5)
                        self.sendMessage(f"New file: {clipObj.name}", clipObj)
                files_handler.updateFile(new_clips, doAppend=True)
        

        def loop(self):
                self.sendMessage("Successfully started webhook")
                while True:
                        sleep(self.seconds)
                        self.checkForNewFiles(self.directory, self.extension, self.recursive)


if __name__ == "__main__":
        import config
        webhook = Webhook(
                url=config.WEBHOOK_URL,
                directory=config.CLIPS_DIRECTORY,
                extension=config.CLIPS_EXTENSION,
                recursive=config.recursive_directories
        )
        webhook.loop()
