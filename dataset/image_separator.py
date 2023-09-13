import cv2
import os

class VideoSeparator:
    def __init__(self, video_path, data_folder='training_images'):
        self.video = cv2.VideoCapture(video_path)
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        self.data_folder = data_folder

    def get_next_frames(self, skip=5, frames=20):
        frame_paths = []
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

