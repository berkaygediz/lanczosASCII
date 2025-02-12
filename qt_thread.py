import subprocess
import time

from PySide6.QtCore import *


class VideoThread(QThread):
    update_frame_signal = Signal(str)
    update_final_signal = Signal(str)

    def __init__(self, video_path, txt_path):
        super().__init__()
        self.frames = []
        self.init_time = None
        self.frame_count = 0
        self.video_path = video_path
        self.txt_path = txt_path

    def run(self):
        subprocess.Popen(
            ["ffplay", "-vn", self.video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        with open(self.txt_path, "r") as f:
            f_raw = f.read()
            f_raw = f_raw.replace(";", " ")
            f_raw = f_raw.replace("c", " ")
        self.frames = f_raw.split("SPLIT")

        self.init_time = time.time()

        while time.time() <= self.init_time + 218:
            current_frame = int((time.time() - self.init_time) * 10)

            if current_frame < len(self.frames):
                self.update_frame_signal.emit(self.frames[current_frame])
                self.frame_count += 1

            time.sleep(0.05)

        final_result = f"Frames: {self.frame_count}\n"
        self.update_final_signal.emit(final_result)
