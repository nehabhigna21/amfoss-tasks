# TASK-11: TimeFlow Wallpaper Sync

A Python program that watches a text file and renders its content, plus a
live clock, straight onto the desktop wallpaper — updating automatically
whenever the file changes or once every second for the clock.

"this is running windows desktop , not linux"

This repo is developed inside WSL2 (Ubuntu on Windows). WSL itself has no
desktop or wallpaper of its own ,the wallpaper lives on the actual Windows
side. So timeflow.py targets the Windows API user32.SystemParametersInfoW
via ctypes) and is meant to be run with Windows Python, not the WSL
one, so the result is actually visible on screen.


## Usage
pip install -r requirements.txt
python timeflow.py <path_to_text_file>

Edit the text file in another window/editor,the wallpaper updates within
about a second. Press Ctrl+C in the terminal to stop and restore your
previous wallpaper.
notes_sample.txt is included as a ready-to-use example file to point it at.

## What i learnt

Testing this made the WSL/Windows split obvious in a way the task
description doesn't call out  a "wallpaper" script only makes sense
against a real desktop. The trickiest part was making the long-text
case degrade gracefully nstead of just overflowing
off the bottom of the screen or crashing.

