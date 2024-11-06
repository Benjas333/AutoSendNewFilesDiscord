import config
from typing import Optional
from pathlib import Path
from time import sleep
from files_handler import globClips, isFileBeingUsed
from clips_manipulator import create_clip
# from discord_webhook import DiscordWebhook
from discord.ext import tasks
import discord


class SelfBot(discord.Client):
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
        
        async def setup_hook(self) -> None:
                self.sendNewClips.start()

        async def on_ready(self):
                print(f"Logged in as {self.user}")
                channel = self.get_channel(config.CHANNEL_ID)
                await channel.send("Successfully started sending new clips")
        
        @tasks.loop(seconds=1)
        async def sendNewClips(self):
                channel = self.get_channel(config.CHANNEL_ID)
                new_clips = globClips(config.CLIPS_DIRECTORY)
                if not new_clips: return

                message = "### New file(s) detected"
                print(message)
                await channel.send(message)

                for clip in new_clips:
                        clipObj = Path(clip)
                        file_size = -1
                        while isFileBeingUsed(clipObj, file_size):
                                print(f"Waiting for file to stop being used... {clip}")
                                file_size = clipObj.stat().st_size
                                sleep(0.5)
                        # sleep(4)
                        # res = create_clip(clipObj, 20)
                        # if res.returncode != 0:
                        #         message = "Failed to create clip: " + str(res.stderr)
                        #         print(message)
                        #         await channel.send(message)
                        file = clipObj
                        # file = Path(f"clips/{clipObj.name}")

                        message = f"New file: `{file.name}`"
                        print(message)
                        with file.open('rb') as content:
                                await channel.send(message, file=discord.File(content, file.name))
                config.updateFile(new_clips, 'a')
        
        @sendNewClips.before_loop
        async def before_sendNewClips(self):
                await self.wait_until_ready()
                        
        
        # async def sendMessage(self, message: str, file: Optional[Path] = None):
        #         channel = self.get_channel(config.CHANNEL_ID)
        #         print(message)
        #         if not file:
        #                 await channel.send(message)
        #                 return

        #         if not file.is_file():
        #                 raise Exception("The path provided is not a file: " + file)
                
        #         sleep(5)
        #         res = create_clip(file, 30)
        #         if res.returncode != 0:
        #                 raise Exception("Failed to create clip: " + str(res.stderr))
        #         file = Path(f"clips/{file.name}")

        #         print(f"Sending file: {file.name}")
        #         await channel.send(message, file=discord.File(file.read_bytes(), file.name))

# webhook = DiscordWebhook(config.WEBHOOK_URL, username="New Clips AutoSender")
client = SelfBot()
client.run(config.TOKEN)


# def sendMessage(message: str, file: Optional[Path] = None):
#         print(message)
#         webhook.content = message
#         if not file:
#                 webhook.execute()
#                 return
        
#         if not file.is_file():
#                 raise Exception("The path provided is not a file: " + file)
        
#         sleep(5)
#         res = create_clip(file, 30)
#         if res.returncode != 0:
#                 raise Exception("Failed to create clip: " + str(res.stderr))
#         file = Path(f"clips/{file.name}")

#         print(f"Sending file: {file.name}")
#         webhook.add_file(file.read_bytes(), file.name)
#         webhook.execute()
#         webhook.remove_files()


# def checkForNewFiles():
#         new_clips = globClips(config.CLIPS_DIRECTORY)
#         if not new_clips: return

#         client.sendMessage("### New clip(s) detected")

#         for clip in new_clips:
#                 clipObj = Path(clip)
#                 client.sendMessage(f"New clip: {clipObj.name}", clipObj)


# if __name__ == "__main__":
#         client.sendMessage("Successfully started webhook")

#         while True:
#                 sleep(1)
#                 checkForNewFiles()
