# TASK-11: TimeFlow Wallpaper Sync

A Python program that watches a text file and renders its content, plus a
live clock, straight onto the desktop wallpaper — updating automatically
whenever the file changes or once every second for the clock.

## Why this runs against Windows, not Linux

This repo is developed inside WSL2 (Ubuntu on Windows). WSL itself has no
desktop or wallpaper of its own — the wallpaper lives on the actual Windows
side. So `timeflow.py` targets the Windows API (`user32.SystemParametersInfoW`
via `ctypes`) and is meant to be **run with Windows Python**, not the WSL
one, so the result is actually visible on screen.

## Approach

- **Rendering** — Pillow draws a fixed-size image matching the real screen
  resolution (queried via `GetSystemMetrics`): a live `HH:MM:SS` clock, the
  date, and the watched file's content underneath.
- **Live clock** — the whole image is regenerated and re-applied as the
  wallpaper once per second, so the seconds field ticks in real time.
- **File watching** — rather than pulling in a separate file-watcher
  dependency, the same once-a-second loop checks the file's `mtime` and only
  reloads its content when that changes. Simpler, and the polling interval
  is already driven by the clock's own refresh rate.
- **Long text** — content is word-wrapped to the screen width; if it still
  doesn't fit vertically, the font size is shrunk step by step down to a
  minimum, and if it's *still* too long at that point, the visible lines are
  truncated with a trailing `...`.
- **Missing / empty file** — a missing file shows a "File not found: \<path>"
  message and keeps polling (so the wallpaper recovers automatically once the
  file appears); an empty file shows "(file is empty)". Neither crashes the
  program.
- **Extra feature** — on start, the program reads and remembers the
  wallpaper you already had set (`SPI_GETDESKWALLPAPER`). On `Ctrl+C`, it
  restores that original wallpaper and deletes its temp image, instead of
  leaving your desktop stuck on the last rendered frame.

## Usage

```powershell
pip install -r requirements.txt
python timeflow.py <path_to_text_file>
```

Edit the text file in another window/editor — the wallpaper updates within
about a second. Press `Ctrl+C` in the terminal to stop and restore your
previous wallpaper.

`notes_sample.txt` is included as a ready-to-use example file to point it at.

## Review

Testing this made the WSL/Windows split obvious in a way the task
description doesn't call out — a "wallpaper" script only makes sense
against a real desktop, so anyone doing amFOSS tasks from WSL will hit the
same "wait, which OS am I even targeting" question. Building it as
`ctypes`-against-Windows plus a polling loop meant no extra file-watcher
dependency was needed at all. The trickiest part was making the long-text
case degrade gracefully (shrink-then-truncate) instead of just overflowing
off the bottom of the screen or crashing.

## Screenshots

See `screenshots/` for: initial generation, live time + content update after
editing the file, empty-file handling, missing-file handling, and long-text
handling.
