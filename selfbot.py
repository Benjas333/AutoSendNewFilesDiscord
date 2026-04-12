from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, override

import discord
import trio
from discord.ext import tasks

import src.files_handler as files_handler
from src.files_manipulator import async_upload_file_to_litterbox

if TYPE_CHECKING:
        from discord.channel import DMChannel, GroupChannel
        from discord.threads import Thread

_seconds: float = 1.0


class SelfBot(discord.Client):
        def __init__(
                self,
                directory: str,
                channel_id: int | list[int],
                token: str | None = None,
                extension: str | list[str] = "*",
                *,
                recursive: bool = False,
                seconds: float = _seconds,
                litterbox_mb_threshold: float = 10.0,
                litterbox_extensions: list[str] | None = None,
                **kwargs,  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]  # noqa: ANN003
        ) -> None:
                super().__init__(**kwargs)  # pyright: ignore[reportUnknownArgumentType]
                self.channel_ids: set[int] = set(channel_id if isinstance(channel_id, list) else [channel_id])
                self.directory: str = directory
                self.extension: str | list[str] = extension
                self.recursive: bool = recursive
                self.seconds: float = seconds
                global _seconds
                _seconds = self.seconds
                self.channels: list[
                        DMChannel | GroupChannel | Thread | discord.VoiceChannel | discord.TextChannel | discord.StageChannel
                ] = []
                self.token: str | None = token
                self.litterboxThreshold: float = litterbox_mb_threshold * 1024 * 1024
                self.litterboxExtensions: set[str] = {
                        litterboxExtension.lower().removeprefix(".") for litterboxExtension in litterbox_extensions or []
                }

        async def send_message(
                self,
                message: str,
                file: trio.Path | None = None,
        ) -> None:
                for channel in self.channels:
                        await asyncio.sleep(0.5)
                        if not file:
                                _ = await channel.send(message)
                                continue

                        if not file.is_file():
                                raise Exception(f"The path provided is not a file: {file}")

                        file_stats = await file.stat()
                        if file_stats.st_size >= 1024**3:
                                print(f"{file.name} size is bigger than 1 GB! Skipped")
                                continue

                        print(f"Sending file: {file.name}")
                        if file_stats.st_size >= self.litterboxThreshold or (
                                self.litterboxExtensions
                                and file.suffix.lower().removeprefix(".") in self.litterboxExtensions
                        ):
                                _ = await channel.send(message + "\n" + await async_upload_file_to_litterbox(file))
                        else:
                                _ = await channel.send(message, file=discord.File(file, file.name))
                print(message)

        @override
        async def setup_hook(self) -> None:
                _ = self.send_new_files.start()

        async def on_ready(self) -> None:
                print(f"\033[92m===== Logged in as {self.user} =====\033[0m")
                for channel_id in self.channel_ids:
                        await asyncio.sleep(1)
                        channel = self.get_channel(channel_id)
                        if isinstance(
                                channel,
                                (
                                        type(None),
                                        discord.CategoryChannel,
                                        discord.ForumChannel,
                                        discord.DirectoryChannel,
                                ),
                        ):
                                continue

                        self.channels.append(channel)
                        _ = await channel.send("Successfully started sending new files")
                if len(self.channels) == 0:
                        raise Exception("No channels were started")

        @tasks.loop(seconds=_seconds)
        async def send_new_files(self) -> None:
                new_files = files_handler.glob_new_files(self.directory, self.extension, recursive=self.recursive)
                if not new_files:
                        return

                await self.send_message("**New file(s) detected**")

                for file in new_files:
                        await asyncio.sleep(0.5)
                        file_path = trio.Path(file)
                        file_size: int = -1
                        while await files_handler.async_is_file_being_used(file_path, file_size):
                                print(f"Waiting for file to stop being used... {file}")
                                file_size = (await file_path.stat()).st_size
                                await asyncio.sleep(0.5)

                        await self.send_message(f"New file: `{file_path.name}`", file_path)
                        files_handler.update_file([file], should_append=True)

        @send_new_files.before_loop
        async def before_send_new_files(self) -> None:
                await self.wait_until_ready()

        def mainloop(self) -> None:
                if not self.token:
                        print("No token provided at the object initialization. Use run('TOKEN') instead.")
                        return

                self.run(self.token)


if __name__ == "__main__":
        import src.config as config

        client = SelfBot(
                channel_id=[config.CHANNEL_ID],
                directory=config.FILES_DIRECTORY,
                extension=[config.FILES_EXTENSION, "m4a"],
                recursive=config.RECURSIVE_DIRECTORIES,
        )
        client.run(config.TOKEN)
