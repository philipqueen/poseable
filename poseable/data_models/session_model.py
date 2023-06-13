import numpy as np

from pydantic import BaseModel
from pathlib import Path

class SessionModel(BaseModel):
    image_path: Path = None
    image_data_path: Path = None
    num_tracked_points: int = None
    camera_num: int = None
