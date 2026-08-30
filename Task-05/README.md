# Grand Line Guardian

A terminal-based process monitor built in Python. It works like htop or btop++. With a fun twist. Every running process is treated as a ship on the Grand Line. The tool acts as the navigator watching over all these ships in time.

## Features
A live table showing every process updated every 0.5 seconds:
Process ID (PID)
Process Name
CPU Usage (%)
Memory Usage (RSS)
- System-wide stats in the header also refreshed every 0.5 seconds:
Current time
Total CPU usage (%)
Total memory usage (used / total with percentage)
Total active process count
Keyboard navigation:
use Up and Down arrows to move the selection through the list of processes. If the list is longer than the terminal the view scrolls like in htop.

Press x to send SIGTERM to the selected process. This terminates a ship.

Press q to quit. The terminal returns to its state after quitting.

## Project layout

On overall, The code is split into files based on responsibility:

proc_reader.py. Handles all reads from /proc. This includes getting process names, memory, CPU ticks, system-wide CPU ticks and system-wide memory data.
input_handler.py. Defines RawTerminal a context manager that sets the terminal to cbreak mode with echo off and restores it when the program ends. It also includes get_key() for reading keystrokes without blocking.
actions.py. Contains kill_process() the function that actually does something to a process.
models.py. Defines the ProcessRow structure used to pass data from collection to display.
ui.py. Builds the visual interface using rich. It creates the stats header panel, the process table, the footer and manages the viewport so the header and footer stay visible when the list of processes is too long.
main.py. 
Runs the main loop: 
take a snapshot sleep while checking for keypresses take another snapshot calculate the differences then update the display.

## Approach

 Reading process and system data of relying on external libraries like psutil this tool reads directly from the /proc virtual filesystem. This is how other tools like ps,top and htop get their data on Linux systems.

/proc/<pid>/comm gives the name of the process.

/proc/<pid>/stat provides fields 14 and 15 for user-mode (utime) and kernel-mode (stime) CPU ticks.

/proc/<pid>/status has the VmRSS value, which's the resident memory size.

/proc/stat contains the first line with system-wide CPU tick counts (user nice system idle iowait irq softirq steal guest guest_nice). Adding all fields gives ticks and idle + iowait gives idle ticks.

 /proc/meminfo includes MemTotal and MemAvailable which give total and available memory.

If a process disappears between two reads, its treated as a race condition. There is no error,its expected behavior.

**CPU percentage** both per process and system-wide is calculated the way as `top` does it. Of using a single read the tool takes two snapshots half a second apart. Then it divides the difference in tick counts by the elapsed ticks.

For a process:

process cpu% = (process_ticks_delta / system_ticks_delta) * 100
For the system:
system cpu% = (1. Idle_ticks_delta / system_ticks_delta) * 100
### Keyboard input

No external input library is used. Everything is handled natively.
 
 The terminal settings are always restored on exit even if the program is interrupted. This prevents leaving the shell in mode, which would break normal typing.


The display uses rich (https://github.com/Textualize/rich) the only external dependency. It enables full-screen UIs without manual clearing or padding.

Live(... auto_refresh=False, screen=True) draws to the terminal’s alternate screen buffer and only updates when live.refresh() is called. This keeps the 0.5-second poll-and-render loop fully in control. No background threads interfere with rendering timing.

 A Panel shows the system stats at the top.
 A Table displays the process list. The selected row appears in reverse video.
Another Panel at the bottom shows status messages and controls.
When the list of processes is taller than the terminal, ui.build_screen() creates a scrolling viewport centered on the selected row. Like htop this ensures the header and footer remain visible. The non-table parts (header, borders, footer) take up 11 lines. So the number of rows available for the process list is terminal_height. 11.

## Final Running it
pip install -r requirements.txt
python3 main.py

## Resources used

https://man7.org/linux/man-pages/man5/proc.5.html.
Explains the format of /proc/<pid>/stat` `/proc/<pid>/status` `/proc/stat and /proc/meminfo

https://docs.python.org/3/library/tty.html

Python select documentation-https://docs.python.org/3/library/select.html

https://rich.readthedocs.io/. Covers Live,Table and Panel
 How top and htop calculate CPU percentage using two time-separated tick samples (general OS monitoring knowledge)

## what i learnt

The /proc filesystem isn't a real disk file system. It's an interface provided by the Linux kernel. It lets programs read kernel data as plain text files without needing special syscalls.

CPU usage isn’t given directly by the kernel. It’s computed from two samples taken some time apart. The percentage is based on the change in ticks divided by total ticks. System "busy" percentage is simply 1. Idle_fraction.

Terminal raw and cbreak modes mean input becomes immediate and echoed characters don't appear on screen.. Using select() requires operating on the same file descriptor that performs the actual read. Mixing buffered sys.stdin with select() consumes bytes which breaks multi-byte inputs like arrow keys.

Sending SIGTERM via os.kill() is better than SIGKILL for interactive termination. SIGTERM lets a process clean up gracefully making it more polite.

rich.live.Live, with auto_refresh=False` allows control over when each frame is redrawn. This is crucial when the refresh must work alongside a managed keyboard polling loop not run on its own timer.

Real process monitors need to implement windowing and scrolling. In a screen Live display content doesn’t wrap or scroll automatically. If the output exceeds the height it gets clipped. The program must track the size and decide what part of the list should be visible.
