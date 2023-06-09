from cog import BasePredictor, Input, Path
from typing import List
import subprocess
import os

class Predictor(BasePredictor):
    def setup(self):
        """Set up the directory to store frames"""
        os.makedirs("./frames", exist_ok=True)

    def predict(self,
          video: Path = Input(description="Video input")
    ) -> List[Path]:
        """Run ffmpeg to split the video into frames"""
        command = f"ffmpeg -i {video} -vf fps=1 ./frames/out%03d.png"
        subprocess.run(command, shell=True, check=True)

        # Get the paths to the frames
        frame_files = sorted(os.listdir("./frames"))
        frame_paths = [Path(os.path.join("./frames", frame_file)) for frame_file in frame_files]

        # Return the paths to the frames
        return frame_paths
