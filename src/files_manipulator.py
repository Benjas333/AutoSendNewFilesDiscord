import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

import trio
from aiohttp import ClientSession, FormData
from requests import post

LITTERBOX_API = "https://litterbox.catbox.moe/resources/internals/api.php"


def create_clip(file: Path, seconds: int = 30) -> subprocess.CompletedProcess[bytes] | None:
        if not file.is_file():
                raise Exception(f"The path provided is not a file: {file}")

        new_clip_path = Path(f"clips/{file.name}")
        if new_clip_path.exists():
                return None

        command = ["ffmpeg", "-sseof", f"-{seconds}", "-i", str(file), "-c", "copy", str(new_clip_path)]
        return subprocess.run(command)


def upload_file_to_litterbox(file: Path) -> str:
        expiration_timestamp = int((datetime.now(UTC) + timedelta(hours=72)).timestamp())

        with file.open("rb") as f:
                response = post(
                        LITTERBOX_API,
                        files={"fileToUpload": f},
                        data={"reqtype": "fileupload", "time": "72h"},
                )
        return response.text + f"\nExpires: <t:{expiration_timestamp}:R>"


async def async_upload_file_to_litterbox(file: trio.Path) -> str:
        expiration_timestamp = int((datetime.now(UTC) + timedelta(hours=72)).timestamp())

        form = FormData()
        form.add_field("reqtype", "fileupload")
        form.add_field("time", "72h")

        async with await file.open("rb") as f:
                form.add_field(
                        "fileToUpload",
                        await f.read(),
                        filename=file.name,
                        content_type="application/octet-stream",
                )

        async with (
                ClientSession() as ses,
                ses.post(
                        LITTERBOX_API,
                        data=form,
                ) as res,
        ):
                response_text = await res.text()

        return response_text + f"\nExpires: <t:{expiration_timestamp}:R>"


if __name__ == "__main__":
        # sleep(5)
        # res = create_clip(file, 30)
        # if res.returncode != 0:
        #         message = "Failed to create clip: " + str(res.stderr)
        #         print(message)
        #         await channel.send(message)
        # file = Path(f"clips/{file.name}")
        pass
