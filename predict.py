from cog import BasePredictor, Input, Path
from typing import List
import subprocess
import os

class Predictor(BasePredictor):
    def predict(self,
          video: Path = Input(description="Video input")
    ) -> List[Path]:
        """Run ffmpeg to split the video into frames"""
        os.makedirs("/tmp/frames", exist_ok=True)
        command = f"ffmpeg -i {video} -vf fps=1 /tmp/frames/out%03d.png"
        subprocess.run(command, shell=True, check=True)

        # Get the paths to the frames
        frame_files = sorted(os.listdir("/tmp/frames"))
        frame_paths = [Path(os.path.join("/tmp/frames", frame_file)) for frame_file in frame_files]

        # Return the paths to the frames
        return frame_paths
