import config
# from typing import Optional
from pathlib import Path
from time import sleep
from files_handler import globClips, isFileBeingUsed
# from clips_manipulator import create_clip
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
                config.updateFile(new_clips, doAppend=True)
        
        @sendNewClips.before_loop
        async def before_sendNewClips(self):
                await self.wait_until_ready()

client = SelfBot()
client.run(config.TOKEN)

