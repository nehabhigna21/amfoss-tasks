# Grand Line Guardian

A terminal-based, real-time process monitor (in the spirit of `htop`/`btop++`)
written in pure Python, using only the standard library. Every running
process is treated as a "ship" on the Grand Line — the navigator (this tool)
keeps watch over all of them.

## Features

- Live table of every active process, refreshed every 0.5 seconds:
  - Process ID (PID)
  - Process Name
  - CPU Usage (%)
  - Memory Usage (RSS)
- Total Active Process Count
- Keyboard navigation: **Up/Down** arrows move the selection cursor through
  the process list
- **x** sends `SIGTERM` to the selected process (terminate a troublesome
  ship)
- **q** quits and restores the terminal to its normal state

## Approach

Rather than depending on a third-party library like `psutil`, the tool reads
process and system information directly from the `/proc` virtual
filesystem, which is how tools like `ps`, `top`, and `htop` get their data
on Linux:

- `/proc/<pid>/comm` — the process name
- `/proc/<pid>/stat` — fields 14 and 15 are the process's user-mode (`utime`)
  and kernel-mode (`stime`) CPU ticks
- `/proc/<pid>/status` — `VmRSS` is the process's resident memory
- `/proc/stat` — the first line's summed fields give total system CPU ticks
  since boot
- `/proc/<pid>/` disappearing between reads means the process exited; this
  is treated as a normal, expected race rather than an error

**CPU percentage** is computed the same way `top` does it: take two
snapshots of a process's CPU ticks (and of the system's total CPU ticks)
half a second apart, then:

```
cpu% = (process_ticks_delta / system_ticks_delta) * 100
```

A single instantaneous read of `/proc/<pid>/stat` can't give a percentage —
CPU ticks are cumulative since the process started, so at least two samples
over a known time window are required.

**Keyboard input** is handled without any external UI library:

- `tty.setcbreak()` puts the terminal into character-at-a-time mode so
  keys are available immediately instead of only after Enter is pressed.
- `select.select()` on `stdin`'s file descriptor makes reading
  non-blocking, so the refresh loop can redraw the screen every 0.5s while
  still noticing a keypress the moment it happens.
- Arrow keys arrive as a 3-byte escape sequence (`ESC [ A` for up, `ESC [ B`
  for down). Because `select()` watches the raw file descriptor, all reads
  in `get_key()` use `os.read(fd, 1)` directly instead of the buffered
  `sys.stdin.read()` — mixing the two caused `select()` and `read()` to
  disagree about what was actually pending, which silently broke arrow-key
  detection during testing.
- The original terminal settings are always restored in a `finally` block,
  even if the program is interrupted, so the shell isn't left in raw mode.

The process list is re-sorted by PID on every refresh so the selection
cursor's row index stays meaningful between frames, and the cursor is
clamped if the selected process disappears (e.g. after being killed).

## Running it

```bash
python3 main.py
```

No `pip install` is required — see `requirements.txt`.

Controls:

| Key        | Action                              |
|------------|--------------------------------------|
| Up / Down  | Move the selection cursor            |
| x          | Terminate the selected process (SIGTERM) |
| q          | Quit                                 |

## Resources used

- [`proc(5)` man page](https://man7.org/linux/man-pages/man5/proc.5.html) —
  the field layout of `/proc/<pid>/stat` and `/proc/<pid>/status`
- [Python `termios`/`tty` documentation](https://docs.python.org/3/library/tty.html)
- [Python `select` documentation](https://docs.python.org/3/library/select.html)
- How `top`/`htop` compute CPU percentage from two time-separated tick
  samples (general OS-monitoring background reading)

## New concepts learned

- The `/proc` filesystem is not a real disk filesystem — it's a virtual
  interface the Linux kernel exposes so user-space tools can read live
  kernel process/system state as plain text files, without special syscalls.
- CPU usage isn't a value the kernel hands you directly per process — it's
  derived by sampling cumulative tick counters twice and dividing by the
  elapsed system-wide ticks.
- Terminal raw/cbreak mode and why `select()` must operate on the same file
  descriptor that ultimately performs the `read()` — Python's buffered
  `sys.stdin` wrapper can silently consume bytes that `select()` doesn't
  know about, which breaks multi-byte input like arrow-key escape
  sequences.
- Sending `SIGTERM` via `os.kill()` versus `SIGKILL`: `SIGTERM` gives a
  process a chance to clean up, which is the more polite default for an
  interactive "terminate" action.
