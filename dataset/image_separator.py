import cv2
import os
import numpy as np
from typing import Union, List
import shutil

class VideoSeparator:
    def __init__(self, video_path: str, data_folder: str = 'training_images'):
        self.video = cv2.VideoCapture(video_path)
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        self.data_folder = data_folder

    def get_next_frames(self, skip: int = 5, frames: int = 20, clear=True) -> List[str]:
        frame_paths = []
        if clear:
            shutil.rmtree(self.data_folder, ignore_errors=True)
            try:
                os.mkdir(self.data_folder)
            except FileExistsError:
                pass
        for i in range(frames):
            for _ in range(skip-1):
                if not self.video.isOpened():
                    return frame_paths
                _, _ = self.video.read()
            if not self.video.isOpened():
                return frame_paths
            ret, frame = self.video.read()
            cv2.imwrite(f'{self.data_folder}/{i}.png', frame)
            frame_paths.append(f'{self.data_folder}/{i}.png')
        return frame_paths

def make_square(image: Union[str, np.ndarray], dimension=512, outpath: Union[None, str] = None) -> np.ndarray:
    if isinstance(image, str):
        image = cv2.imread(image)
    h, w, _ = image.shape
    if w > h:
        x_start = int(w / 2 - h / 2)
        image = image[:, x_start:x_start + h, :]
    elif h < w:
        y_start = int(h / 2 - w / 2)
        image = image[y_start:y_start + w, :, :]
    cv2_img = cv2.resize(image, (dimension, dimension))
    if outpath is None:
        return cv2_img
    cv2.imwrite(outpath, cv2_img)
    return cv2_img

