import files_handler
from pathlib import Path
from time import sleep
# from clips_manipulator import create_clip
from discord.ext import tasks
import discord

_seconds = 1.0

class SelfBot(discord.Client):
        def __init__(
                self,
                channel_id: int,
                directory: str,
                extension = "*",
                recursive = False,
                seconds: float = _seconds,
                *args,
                **kwargs
        ):
                super().__init__(*args, **kwargs)
                self.channel_id = channel_id
                self.directory = directory
                self.extension = extension
                self.recursive = recursive
                self.seconds = seconds
                global _seconds
                _seconds = self.seconds
        

        async def setup_hook(self) -> None:
                self.sendNewClips.start()
        

        async def on_ready(self):
                print(f"\033[92m===== Logged in as {self.user} =====\033[0m")
                channel = self.get_channel(self.channel_id)
                await channel.send("Successfully started sending new files")
        

        @tasks.loop(seconds=_seconds)
        async def sendNewClips(self):
                channel = self.get_channel(self.channel_id)
                new_clips = files_handler.globNewFiles(self.directory, self.extension, self.recursive)
                if not new_clips: return

                message = "### New file(s) detected"
                print(message)
                await channel.send(message)

                for clip in new_clips:
                        clipObj = Path(clip)
                        file_size = -1
                        while files_handler.isFileBeingUsed(clipObj, file_size):
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
                files_handler.updateFile(new_clips, doAppend=True)
        

        @sendNewClips.before_loop
        async def before_sendNewClips(self):
                await self.wait_until_ready()


if __name__ == "__main__":
        import config
        client = SelfBot(
                channel_id=config.CHANNEL_ID,
                directory=config.CLIPS_DIRECTORY,
                extension=config.CLIPS_EXTENSION,
                recursive=config.RECURSIVE_DIRECTORIES
        )
        client.run(config.TOKEN)
