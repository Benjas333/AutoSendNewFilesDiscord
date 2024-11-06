import subprocess
from pathlib import Path

def create_clip(file: Path, seconds: int = 30):
        if not file.is_file():
                raise Exception("The path provided is not a file: " + file)
        new_clip_path = Path(f"clips/{file.name}")
        if new_clip_path.exists():
                return
        
        command = ["ffmpeg", "-sseof", f"-{seconds}", "-i", str(file), "-c", "copy", str(new_clip_path)]
        res = subprocess.run(command)
        return res
