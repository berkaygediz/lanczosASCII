# lanczosASCII

Convert videos to ASCII using Lanczos sampling and display them in a GUI.

## Requirements

```bash
pip install -r requirements.txt
```

- PySide6
- opencv-python
- Pillow

## Usage

### `convert.py`

```bash
python convert.py <video_file> <new_width> <new_height> <output_txt_file>
```

### `cli.py`

```bash
python cli.py <txt_file> <video_file> <video_duration_in_seconds>
```

### `qt_thread.py`

Display ASCII frames in a PySide6 GUI. Use the `VideoThread` class to load and show frames.

```python
from qt_thread import VideoThread
```
