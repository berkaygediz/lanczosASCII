import os
import sys

import cv2
from PIL import Image

ASCII_CHARS = "Ñ@#W$9876543210?!abc;:+=-,._"


def imgScale(img, new_w, new_h):
    (original_w, original_h) = img.size
    aspect_ratio = original_h / float(original_w)
    if new_h == 0:
        new_h = int(aspect_ratio * new_w)

    new_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    return new_img


def imgGrayscale(image):
    return image.convert("L")


def imgPixelsToASCII(image, range_width=12.75):
    pixels_in_image = list(image.getdata())
    pixels_to_chars = []

    for pixel_value in pixels_in_image:
        try:
            ascii_index = int(pixel_value / range_width)
            ascii_index = min(ascii_index, len(ASCII_CHARS) - 1)
            pixels_to_chars.append(ASCII_CHARS[ascii_index])
        except Exception as e:
            print(f"Error processing pixel value {pixel_value}: {e}")
            pixels_to_chars.append(" ")

    return "".join(pixels_to_chars)


def imgImageToASCII(image, new_width, new_height):
    image = imgScale(image, new_width, new_height)
    image = imgGrayscale(image)

    pixels_to_chars = imgPixelsToASCII(image)
    len_pixels_to_chars = len(pixels_to_chars)

    img_ascii = [
        pixels_to_chars[index : index + new_width]
        for index in range(0, len_pixels_to_chars, new_width)
    ]

    return "\n".join(img_ascii)


def imgConversion(image_fp, new_width, new_height):
    img = None
    try:
        img = Image.open(image_fp)
    except Exception as e:
        print(f"Unable to open image file {image_fp}.")
        print(e)
        return
    img_ascii = imgImageToASCII(img, new_width, new_height)
    return img_ascii


def process_video(video_f, new_w, new_h, txt_f):
    vidcap = cv2.VideoCapture(video_f)

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    total_fs = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_fs / fps

    print(f"Video süresi: {duration} saniye")

    time_count = 0
    frames = []

    if not os.path.exists(txt_f):
        with open(txt_f, "w") as f:
            pass

    processed_fs = 0

    while time_count <= duration:
        print(f"ASCII frame: {int(time_count)}/{int(duration)}")

        vidcap.set(cv2.CAP_PROP_POS_MSEC, time_count * 1000)
        success, image = vidcap.read()
        if success:
            cv2.imwrite("frame.jpg", image)
            frames.append(imgConversion("frame.jpg", new_w, new_h))
            processed_fs += 1

        time_count += 0.1

    with open(txt_f, "w") as f:
        f.write("SPLIT".join(frames))
    print(f"Saved to: {txt_f}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: python convert.py <path_to_video_file> <new_width> <new_height> <output_txt_file>"
        )
        sys.exit(1)

    video_f = sys.argv[1]
    try:
        new_w = int(sys.argv[2])
        new_h = int(sys.argv[3])
        txt_f = sys.argv[4]
    except ValueError:
        print("Error: Width, height must be integers.")
        sys.exit(1)

    process_video(video_f, new_w, new_h, txt_f)
