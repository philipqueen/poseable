import numpy as np
from pathlib import Path


def load_mediapipe_data(data_path: Path, camera, frame, num_tracked_points) -> np.ndarray:
    data_array = np.load(data_path)

    print(f"loaded mediapipe data with shape {data_array.shape}")

    print(f"returning data with shape {data_array[camera,frame,:num_tracked_points,:2].shape}")

    return data_array[camera,frame,:num_tracked_points,:2]

if __name__ == "__main__":
    data_path = Path("YOUR/PATH/TO/mediapipe2dData_numCams_numFrames_numTrackedPoints_pixelXY.npy")
    data_array = load_mediapipe_data(data_path)