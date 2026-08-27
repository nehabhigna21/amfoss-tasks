# Grand Line Guardian

A terminal-based, real-time process monitor (in the spirit of `htop`/`btop++`)
written in Python. Every running process is treated as a "ship" on the
Grand Line — the navigator (this tool) keeps watch over all of them.

## Features

- Live table of every active process, refreshed every 0.5 seconds:
  - Process ID (PID)
  - Process Name
  - CPU Usage (%)
  - Memory Usage (RSS)
- System-wide totals in the header, also refreshed every 0.5 seconds:
  - Current time
  - Total CPU usage (%)
  - Total memory usage (used / total, with percentage)
  - Total active process count
- Keyboard navigation: **Up/Down** arrows move the selection cursor through
  the process list, scrolling the view (like `htop`) when the list is
  taller than the terminal
- **x** sends `SIGTERM` to the selected process (terminate a troublesome
  ship)
- **q** quits and restores the terminal to its normal state

## Project layout

The program is split by responsibility instead of living in one script:

- `proc_reader.py` — every read of `/proc` (the actual "how do we get this
  data" logic): per-process name/memory/CPU ticks, system-wide CPU ticks,
  system-wide memory.
- `input_handler.py` — `RawTerminal`, a context manager that puts the
  terminal into cbreak mode with echo off and always restores it on exit,
  plus `get_key()` for non-blocking keypress reads (including arrow-key
  escape sequences).
- `actions.py` — `kill_process()`, the one thing the tool does *to* a
  process rather than just reading.
- `models.py` — the `ProcessRow` record passed from data collection to
  rendering.
- `ui.py` — builds the `rich` renderables: the stats header panel, the
  process table, the footer, and the htop-style viewport windowing that
  keeps the header/footer on screen when the process list overflows the
  terminal.
- `main.py` — the refresh loop: snapshot, sleep-while-polling-keys,
  snapshot again, compute deltas, render.

## Approach

### Reading process/system data

Rather than depending on a third-party library like `psutil`, the tool
reads process and system information directly from the `/proc` virtual
filesystem, which is how tools like `ps`, `top`, and `htop` get their data
on Linux:

- `/proc/<pid>/comm` — the process name
- `/proc/<pid>/stat` — fields 14 and 15 are the process's user-mode
  (`utime`) and kernel-mode (`stime`) CPU ticks
- `/proc/<pid>/status` — `VmRSS` is the process's resident memory
- `/proc/stat` — the first line (`user nice system idle iowait irq softirq
  steal guest guest_nice`) gives system-wide CPU ticks; summing all fields
  gives total ticks, and `idle + iowait` gives idle ticks
- `/proc/meminfo` — `MemTotal` and `MemAvailable` give total and used
  system memory
- A process disappearing between reads (`FileNotFoundError`) is treated as
  a normal, expected race, not an error

**CPU percentage**, both per-process and system-wide, is computed the same
way `top` does it: take two snapshots half a second apart and divide the
*delta*, not an instantaneous value (ticks are cumulative since boot, so a
single read can't yield a rate):

```
process cpu%  = (process_ticks_delta   / system_ticks_delta) * 100
system  cpu%  = (1 - idle_ticks_delta  / system_ticks_delta) * 100
```

### Keyboard input

Handled without any external input library:

- `tty.setcbreak()` puts the terminal into character-at-a-time mode so
  keys are available immediately instead of only after Enter is pressed;
  echo is disabled separately so keystrokes don't visibly interfere with
  the live display.
- `select.select()` on `stdin`'s file descriptor makes reading
  non-blocking, so the refresh loop can redraw the screen every 0.5s while
  still noticing a keypress the moment it happens.
- Arrow keys arrive as a 3-byte escape sequence (`ESC [ A` for up, `ESC [
  B` for down). Because `select()` watches the raw file descriptor, all
  reads in `get_key()` use `os.read(fd, 1)` directly instead of the
  buffered `sys.stdin.read()` — mixing the two caused `select()` and
  `read()` to disagree about what was actually pending, which silently
  broke arrow-key detection during testing.
- The original terminal settings are always restored in
  `RawTerminal.__exit__`, even if the program is interrupted, so the shell
  isn't left in raw mode.

### Rendering

The display uses [`rich`](https://github.com/Textualize/rich) — the only
external dependency — for a proper full-screen UI instead of manually
clearing the terminal and printing padded strings:

- `Live(..., auto_refresh=False, screen=True)` draws to the terminal's
  alternate screen buffer and only redraws when `live.refresh()` is called
  explicitly, so the existing 0.5s poll-and-render loop stays in full
  control of pacing (no background refresh thread fighting with the
  keyboard-polling loop).
- A `Panel` header shows the system-wide stats; a `Table` shows the
  process list with the selected row rendered in reverse video; another
  `Panel` footer shows status messages and controls.
- If the process list is taller than the terminal, `ui.build_screen()`
  windows the table to a scrolling viewport centered on the selection
  (like `htop`) instead of letting content clip off the bottom — the
  non-table chrome (header + table borders + footer) is a constant 11
  lines, so the available row budget is just `terminal_height - 11`.

## Running it

```bash
pip install -r requirements.txt
python3 main.py
```

Controls:

| Key        | Action                                    |
|------------|--------------------------------------------|
| Up / Down  | Move the selection cursor / scroll          |
| x          | Terminate the selected process (SIGTERM)    |
| q          | Quit                                        |

## Resources used

- [`proc(5)` man page](https://man7.org/linux/man-pages/man5/proc.5.html) —
  the field layout of `/proc/<pid>/stat`, `/proc/<pid>/status`,
  `/proc/stat`, and `/proc/meminfo`
- [Python `termios`/`tty` documentation](https://docs.python.org/3/library/tty.html)
- [Python `select` documentation](https://docs.python.org/3/library/select.html)
- [`rich` documentation](https://rich.readthedocs.io/) — `Live`, `Table`,
  `Panel`
- How `top`/`htop` compute CPU percentage from two time-separated tick
  samples (general OS-monitoring background reading)

## New concepts learned

- The `/proc` filesystem is not a real disk filesystem — it's a virtual
  interface the Linux kernel exposes so user-space tools can read live
  kernel process/system state as plain text files, without special
  syscalls.
- CPU usage isn't a value the kernel hands you directly per process or
  system-wide — it's derived by sampling cumulative tick counters twice
  and dividing by the elapsed ticks, and system-wide "busy" percentage is
  just `1 - idle_fraction`.
- Terminal raw/cbreak mode, and why `select()` must operate on the same
  file descriptor that ultimately performs the `read()` — Python's
  buffered `sys.stdin` wrapper can silently consume bytes that `select()`
  doesn't know about, which breaks multi-byte input like arrow-key escape
  sequences.
- Sending `SIGTERM` via `os.kill()` versus `SIGKILL`: `SIGTERM` gives a
  process a chance to clean up, which is the more polite default for an
  interactive "terminate" action.
- `rich.live.Live` with `auto_refresh=False` gives full manual control over
  when a frame is redrawn, which matters when the redraw has to interleave
  with a hand-rolled keyboard-polling loop instead of running on its own
  timer.
- Why a real process monitor has to window/scroll its list instead of
  printing every row: content taller than the terminal doesn't wrap or
  scroll automatically inside an alternate-screen `Live` display, it just
  gets clipped — the tool has to track terminal height itself and decide
  what's currently visible.
