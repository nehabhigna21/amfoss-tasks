"""
TimeFlow Wallpaper Sync

Watches a text file and renders its content, plus a live clock, onto the
Windows desktop wallpaper. The wallpaper refreshes every second (for the
clock) and reloads the file whenever its contents change on disk.

This targets Windows specifically (via ctypes/user32), since the desktop
wallpaper it updates lives on the Windows side, not inside WSL.

Usage (run from a Windows terminal, not WSL bash):
    python timeflow.py <path_to_text_file>

Press Ctrl+C to stop; the previous wallpaper is restored automatically.
"""

import sys
import os
import time
import ctypes
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SPI_SETDESKWALLPAPER = 20
SPI_GETDESKWALLPAPER = 0x0073
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

WALLPAPER_PATH = Path(tempfile.gettempdir()) / "timeflow_wallpaper.bmp"

BG_COLOR = (18, 18, 24)
TEXT_COLOR = (235, 235, 235)
TIME_COLOR = (120, 200, 255)
ACCENT_COLOR = (255, 140, 140)

MARGIN = 60
TIME_FONT_SIZE = 72
DATE_FONT_SIZE = 28
BODY_FONT_SIZE_MAX = 40
BODY_FONT_SIZE_MIN = 16

REFRESH_INTERVAL_SECONDS = 1


def get_screen_size():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def load_font(size):
    fonts_dir = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    for name in ("consola.ttf", "arial.ttf", "seguisym.ttf"):
        path = fonts_dir / name
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size)
            except OSError:
                continue
    return ImageFont.load_default()


def read_file_content(path):
    """Returns (mtime_or_None, display_text). mtime is None when the file
    is missing so the caller can distinguish that from a real 0-byte file."""
    p = Path(path)
    if not p.exists():
        return None, f"File not found:\n{p}"
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return None, f"Could not read file:\n{exc}"
    if not text.strip():
        return p.stat().st_mtime, "(file is empty)"
    return p.stat().st_mtime, text


def wrap_and_fit(draw, text, max_width, max_height):
    """Word-wraps text to max_width, shrinking the font until it fits
    max_height. If it still doesn't fit at the smallest size, truncates
    the visible lines and appends an ellipsis."""
    size = BODY_FONT_SIZE_MAX
    font, lines, line_height = None, [], 0

    while size >= BODY_FONT_SIZE_MIN:
        font = load_font(size)
        lines = []
        for paragraph in text.splitlines() or [""]:
            line = ""
            for word in paragraph.split(" "):
                trial = f"{line} {word}".strip()
                if draw.textlength(trial, font=font) <= max_width:
                    line = trial
                else:
                    if line:
                        lines.append(line)
                    line = word
            lines.append(line)
        line_height = font.getbbox("Ag")[3] + 8
        if line_height * len(lines) <= max_height:
            return font, lines
        size -= 4

    max_lines = max(1, max_height // line_height)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip() + " ..."
    return font, lines


def render_wallpaper(text_content, width, height):
    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    time_font = load_font(TIME_FONT_SIZE)
    draw.text((MARGIN, MARGIN), time.strftime("%H:%M:%S"), font=time_font, fill=TIME_COLOR)

    date_font = load_font(DATE_FONT_SIZE)
    draw.text(
        (MARGIN, MARGIN + TIME_FONT_SIZE + 10),
        time.strftime("%A, %d %B %Y"),
        font=date_font,
        fill=ACCENT_COLOR,
    )

    body_top = MARGIN + TIME_FONT_SIZE + 60
    body_font, lines = wrap_and_fit(draw, text_content, width - 2 * MARGIN, height - body_top - MARGIN)

    y = body_top
    for line in lines:
        draw.text((MARGIN, y), line, font=body_font, fill=TEXT_COLOR)
        y += body_font.getbbox("Ag")[3] + 8

    return img


def set_wallpaper(image):
    image.save(WALLPAPER_PATH, "BMP")
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, str(WALLPAPER_PATH), SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )


def get_current_wallpaper():
    buf = ctypes.create_unicode_buffer(260)
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, 260, buf, 0)
    return buf.value


def restore_wallpaper(path):
    if path:
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )
    try:
        WALLPAPER_PATH.unlink(missing_ok=True)
    except OSError:
        pass


def main():
    if len(sys.argv) != 2:
        print("Usage: python timeflow.py <path_to_text_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    width, height = get_screen_size()
    original_wallpaper = get_current_wallpaper()

    last_mtime = None
    content = "(waiting for file...)"

    print(f"TimeFlow Wallpaper Sync watching: {file_path}")
    print("Press Ctrl+C to stop and restore your previous wallpaper.")

    try:
        while True:
            mtime, current_content = read_file_content(file_path)
            if last_mtime is None or mtime != last_mtime:
                content = current_content
                last_mtime = mtime
            set_wallpaper(render_wallpaper(content, width, height))
            time.sleep(REFRESH_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nStopping and restoring previous wallpaper...")
        restore_wallpaper(original_wallpaper)


if __name__ == "__main__":
    main()
