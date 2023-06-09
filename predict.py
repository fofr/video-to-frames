from cog import BasePredictor, Input, Path
from typing import List
import subprocess
import os

class Predictor(BasePredictor):
    def predict(self,
                video: Path = Input(description="Video to split into frames"),
                fps: int = Input(description="Number of images per second of video, when not exporting all frames", default=1, ge=1),
                extract_all_frames: bool = Input(description="Get every frame of the video. Ignores fps. Slow for large videos.", default=False),
    ) -> List[Path]:
        """Run ffmpeg to split the video into frames"""
        os.makedirs("/tmp/frames", exist_ok=True)

        if not extract_all_frames:
            command = f"ffmpeg -i {video} -vf fps={fps} /tmp/frames/out%03d.png"
        else:
            command = f"ffmpeg -i {video} /tmp/frames/out%03d.png"

        subprocess.run(command, shell=True, check=True)
        frame_files = sorted(os.listdir("/tmp/frames"))
        frame_paths = [Path(os.path.join("/tmp/frames", frame_file)) for frame_file in frame_files]

        return frame_paths
