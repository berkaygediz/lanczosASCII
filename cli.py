import os
import subprocess
import sys
import time


def playASCII(txt_f, video_f, duration):
    try:
        with open(txt_f, "r") as f:
            f_raw = f.read()
            f_raw = f_raw.replace(".", " ")
            f_raw = f_raw.replace(";", " ")
            f_raw = f_raw.replace("c", " ")
        frames = f_raw.split("SPLIT")

        subprocess.Popen(
            [
                "ffplay",
                "-vn",
                video_f,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        total_fs = len(frames)
        f_rate = 10
        expected_fs = int(duration * f_rate)
        total_fs = min(total_fs, expected_fs)
        init_time = time.time()

        while time.time() <= init_time + duration:
            os.system("cls")
            elapsed_time = time.time() - init_time
            current_frame = int(elapsed_time * f_rate)

            if current_frame < total_fs:
                print(frames[current_frame])
            time.sleep(0.05)

    except FileNotFoundError:
        print(f"Error: File '{txt_f}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python cli.py <path_to_txt_file> <path_to_video_file> <video_duration_in_seconds>"
        )
        sys.exit(1)

    txt_f = sys.argv[1]
    video_f = sys.argv[2]
    try:
        duration = int(sys.argv[3])
    except ValueError:
        print("Error: Video duration must be an integer.")
        sys.exit(1)

    playASCII(txt_f, video_f, duration)
