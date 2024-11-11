import src.files_handler as files_handler
from src.files_manipulator import uploadFileToLitterbox
from pathlib import Path
from time import sleep
from typing import Optional
from discord.ext import tasks
import discord

_seconds = 1.0

class SelfBot(discord.Client):
        def __init__(
                self,
                directory: str,
                channel_id: int | list[int],
                token: Optional[str] = None,
                extension: str | list[str] = "*",
                recursive: bool = False,
                seconds: float = _seconds,
                litterboxMBThreshold: float = 10.0,
                litterboxExtensions: list[str] = [],
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
                self.token = token
                self.litterboxThreshold = litterboxMBThreshold * 1024 * 1024
                self.litterboxExtensions = set(litterboxExtension.lower().removeprefix('.') for litterboxExtension in litterboxExtensions)
        

        async def sendMessage(
                self,
                message: str,
                file: Optional[Path] = None,
        ):
                for channel in self.channels:
                        if not file:
                                await channel.send(message)
                                continue
                        
                        if not file.is_file():
                                raise Exception("The path provided is not a file: " + file)
                        
                        print(f"Sending file: {file.name}")
                        if file.stat().st_size >= self.litterboxMBThreshold or (self.litterboxExtensions and file.suffix.lower().removeprefix('.') in self.litterboxExtensions):
                                await channel.send(message + "\n" + uploadFileToLitterbox(file))
                        else:
                                with file.open('rb') as content:
                                        await channel.send(message, file=discord.File(content, file.name))
                        sleep(0.5)
                print(message)


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
                        sleep(1)
                if len(self.channels) == 0:
                        raise Exception("No channels were started")
        

        @tasks.loop(seconds=_seconds)
        async def sendNewFiles(self):
                new_files = files_handler.globNewFiles(self.directory, self.extension, self.recursive)
                if not new_files: return
                await self.sendMessage("**New file(s) detected**")

                for file in new_files:
                        fileObj = Path(file)
                        file_size = -1
                        while files_handler.isFileBeingUsed(fileObj, file_size):
                                print(f"Waiting for file to stop being used... {file}")
                                file_size = fileObj.stat().st_size
                                sleep(0.5)

                        await self.sendMessage(f"New file: `{fileObj.name}`", fileObj)
                        files_handler.updateFile([file], doAppend=True)
                        sleep(0.5)
        

        @sendNewFiles.before_loop
        async def before_sendNewFiles(self):
                await self.wait_until_ready()
        

        def mainloop(self):
                if not self.token:
                        print("No token provided at the object initialization. Use run('TOKEN') instead.")
                        return
                self.run(self.token)


if __name__ == "__main__":
        import src.config as config
        client = SelfBot(
                channel_id=[config.CHANNEL_ID],
                directory=config.FILES_DIRECTORY,
                extension=[config.FILES_EXTENSION, 'm4a'],
                recursive=config.RECURSIVE_DIRECTORIES,
        )
        client.run(config.TOKEN)
