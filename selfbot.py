import files_handler
from pathlib import Path
from time import sleep
from typing import Optional
# from clips_manipulator import create_clip
from discord.ext import tasks
import discord

_seconds = 1.0

class SelfBot(discord.Client):
        def __init__(
                self,
                channel_id: int | list[int],
                directory: str,
                extension: str | list[str] = "*",
                recursive: bool = False,
                seconds: float = _seconds,
                *args,
                **kwargs
        ):
                super().__init__(*args, **kwargs)
                self.channel_ids = set(channel_id if isinstance(channel_id, list) else [channel_id])
                self.directory = directory
                self.extension = extension
                self.recursive = recursive
                self.seconds = seconds
                global _seconds
                _seconds = self.seconds
                self.channels = []
        

        async def sendMessage(
                self,
                message: str,
                file: Optional[Path] = None,
        ):
                print(message)
                for channel in self.channels:
                        if not file:
                                await channel.send(message)
                                continue
                        
                        if not file.is_file():
                                raise Exception("The path provided is not a file: " + file)
                        
                        print(f"Sending file: {file.name}")
                        with file.open('rb') as content:
                                await channel.send(message, file=discord.File(content, file.name))


        async def setup_hook(self) -> None:
                self.sendNewFiles.start()
        

        async def on_ready(self):
                print(f"\033[92m===== Logged in as {self.user} =====\033[0m")
                for channel_id in self.channel_ids:
                        channel = self.get_channel(channel_id)
                        if not channel:
                                continue
                        self.channels.append(channel)
                        await channel.send("Successfully started sending new files")
        

        @tasks.loop(seconds=_seconds)
        async def sendNewFiles(self):
                new_files = files_handler.globNewFiles(self.directory, self.extension, self.recursive)
                if not new_files: return

                await self.sendMessage("### New file(s) detected")

                for file in new_files:
                        fileObj = Path(file)
                        file_size = -1
                        while files_handler.isFileBeingUsed(fileObj, file_size):
                                print(f"Waiting for file to stop being used... {file}")
                                file_size = fileObj.stat().st_size
                                sleep(0.5)
                        # sleep(4)
                        # res = create_clip(clipObj, 20)
                        # if res.returncode != 0:
                        #         message = "Failed to create clip: " + str(res.stderr)
                        #         print(message)
                        #         await channel.send(message)
                        # file = Path(f"clips/{clipObj.name}")

                        await self.sendMessage(f"New file: `{fileObj.name}`", fileObj)
                        files_handler.updateFile([file], doAppend=True)
        

        @sendNewFiles.before_loop
        async def before_sendNewFiles(self):
                await self.wait_until_ready()


if __name__ == "__main__":
        import config
        client = SelfBot(
                channel_id=[config.CHANNEL_ID, 1119884285156012076, 1303871037225832448],
                directory=config.FILES_DIRECTORY,
                extension=config.FILES_EXTENSION,
                recursive=config.RECURSIVE_DIRECTORIES,
        )
        client.run(config.TOKEN)
