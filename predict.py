from cog import BasePredictor, Input, Path
from typing import List, Optional
import subprocess
import os

class Predictor(BasePredictor):
    def predict(self,
                video: Path = Input(description="Video input"),
                fps: int = Input(description="Frames per second", default=None)
    ) -> List[Path]:
        """Run ffmpeg to split the video into frames"""
        os.makedirs("/tmp/frames", exist_ok=True)

        # If fps is provided, use it in the ffmpeg command
        if fps is not None:
            command = f"ffmpeg -i {video} -vf fps={fps} /tmp/frames/out%03d.png"
        else:
            # Default to showing every frame
            command = f"ffmpeg -i {video} /tmp/frames/out%03d.png"

        subprocess.run(command, shell=True, check=True)

        # Get the paths to the frames
        frame_files = sorted(os.listdir("/tmp/frames"))
        frame_paths = [Path(os.path.join("/tmp/frames", frame_file)) for frame_file in frame_files]

        # Return the paths to the frames
        return frame_paths
