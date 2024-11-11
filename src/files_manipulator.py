import subprocess
from pathlib import Path
from datetime import datetime, timedelta, timezone
from requests import post


def create_clip(file: Path, seconds: int = 30):
        if not file.is_file():
                raise Exception("The path provided is not a file: " + file)
        new_clip_path = Path(f"clips/{file.name}")
        if new_clip_path.exists():
                return
        
        command = ["ffmpeg", "-sseof", f"-{seconds}", "-i", str(file), "-c", "copy", str(new_clip_path)]
        res = subprocess.run(command)
        return res


def uploadFileToLitterbox(file: Path) -> str:
        expiration_timestamp = int((datetime.now(timezone.utc) + timedelta(hours=72)).timestamp())
        with file.open('rb') as f:
                response = post(
                        'https://litterbox.catbox.moe/resources/internals/api.php',
                        files={ "fileToUpload": f },
                        data={ "reqtype": "fileupload", "time": "72h" }
                )
        return response.text + f"\nExpires: <t:{expiration_timestamp}:R>"


if __name__ == "__main__":
        # sleep(5)
        # res = create_clip(file, 30)
        # if res.returncode != 0:
        #         message = "Failed to create clip: " + str(res.stderr)
        #         print(message)
        #         await channel.send(message)
        # file = Path(f"clips/{file.name}")
        pass
