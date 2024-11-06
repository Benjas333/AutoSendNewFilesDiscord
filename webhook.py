import config
from typing import Optional
from pathlib import Path
from time import sleep
from files_handler import globClips, isFileBeingUsed
# from clips_manipulator import create_clip
from discord_webhook import DiscordWebhook

webhook = DiscordWebhook(config.WEBHOOK_URL, username="New Clips AutoSender")


def sendMessage(message: str, file: Optional[Path] = None):
        print(message)
        webhook.content = message
        if not file:
                webhook.execute()
                return
        
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


def checkForNewFiles():
        new_clips = globClips(config.CLIPS_DIRECTORY)
        if not new_clips: return

        sendMessage("### New file(s) detected")

        for clip in new_clips:
                clipObj = Path(clip)
                file_size = -1
                while isFileBeingUsed(clipObj, file_size):
                        print(f"Waiting for file to stop being used... {clip}")
                        file_size = clipObj.stat().st_size
                        sleep(0.5)
                sendMessage(f"New file: {clipObj.name}", clipObj)
        config.updateFile(new_clips, doAppend=True)


if __name__ == "__main__":
        sendMessage("Successfully started webhook")

        while True:
                sleep(1)
                checkForNewFiles()
