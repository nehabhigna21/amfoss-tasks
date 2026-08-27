import os
import time
import sys
import signal
import termios
import tty
import select

PROC_DIR = "/proc"
REFRESH_INTERVAL = 0.5  # seconds; must stay under 1s per spec


# --------------------------------------------------
# Get memory usage of a process
# --------------------------------------------------

def get_memory(pid):
    try:
        with open(f"/proc/{pid}/status", "r") as file:
            for line in file:
                if line.startswith("VmRSS:"):
                    return line.split()[1] + " kB"

    except FileNotFoundError:
        return "N/A"

    return "0 kB"


# --------------------------------------------------
# Get the process name
# --------------------------------------------------

def get_process_name(pid):
    try:
        with open(f"/proc/{pid}/comm", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "?"


# --------------------------------------------------
# Get CPU time used by a process
# --------------------------------------------------

def get_process_cpu_time(pid):
    try:
        with open(f"/proc/{pid}/stat", "r") as file:
            values = file.read().split()

            # Field 14 = user CPU time
            utime = int(values[13])

            # Field 15 = kernel CPU time
            stime = int(values[14])

            return utime + stime

    except (FileNotFoundError, IndexError):
        return 0


# --------------------------------------------------
# Get total CPU time of the system
# --------------------------------------------------

def get_total_cpu_time():
    try:
        with open("/proc/stat", "r") as file:
            first_line = file.readline()

        values = first_line.split()[1:]

        return sum(int(value) for value in values)

    except (FileNotFoundError, ValueError):
        return 0


# --------------------------------------------------
# List every currently running PID, sorted
# --------------------------------------------------

def list_pids():
    return sorted(
        (entry for entry in os.listdir(PROC_DIR) if entry.isdigit()),
        key=int,
    )


# --------------------------------------------------
# Terminate a process by PID
# --------------------------------------------------

def kill_process(pid):
    try:
        os.kill(int(pid), signal.SIGTERM)
        return f"Sent SIGTERM to PID {pid}"
    except ProcessLookupError:
        return f"PID {pid} no longer exists"
    except PermissionError:
        return f"Permission denied killing PID {pid}"


# --------------------------------------------------
# Read a single keypress, resolving arrow-key escape
# sequences (ESC [ A = up, ESC [ B = down).
# --------------------------------------------------

def get_key():
    # Read straight from the raw fd (not the buffered sys.stdin wrapper) so
    # that select() and read() agree on what's actually pending.
    fd = sys.stdin.fileno()

    if not select.select([fd], [], [], 0)[0]:
        return None

    ch = os.read(fd, 1).decode(errors="ignore")
    if ch != "\x1b":
        return ch

    if select.select([fd], [], [], 0)[0]:
        ch2 = os.read(fd, 1).decode(errors="ignore")
        if ch2 == "[" and select.select([fd], [], [], 0)[0]:
            ch3 = os.read(fd, 1).decode(errors="ignore")
            return {"A": "UP", "B": "DOWN"}.get(ch3)

    return "ESC"


# --------------------------------------------------
# Main program
# --------------------------------------------------

def main():
    old_settings = termios.tcgetattr(sys.stdin)
    selected = 0
    status_message = ""

    try:
        # Put terminal into character-at-a-time mode
        tty.setcbreak(sys.stdin.fileno())

        while True:
            pids = list_pids()

            # ------------------------------------------
            # FIRST CPU SNAPSHOT
            # ------------------------------------------

            previous_process_times = {
                pid: get_process_cpu_time(pid) for pid in pids
            }
            previous_system_time = get_total_cpu_time()

            # ------------------------------------------
            # Wait REFRESH_INTERVAL seconds while
            # checking the keyboard for navigation,
            # a kill request, or quit.
            # ------------------------------------------

            quit_program = False
            elapsed = 0.0
            step = 0.05

            while elapsed < REFRESH_INTERVAL:
                key = get_key()

                if key == "q":
                    quit_program = True
                    break
                elif key == "UP":
                    selected = max(0, selected - 1)
                elif key == "DOWN" and pids:
                    selected = min(len(pids) - 1, selected + 1)
                elif key == "x" and pids:
                    status_message = kill_process(pids[selected])

                time.sleep(step)
                elapsed += step

            if quit_program:
                break

            # ------------------------------------------
            # SECOND CPU SNAPSHOT
            # ------------------------------------------

            current_system_time = get_total_cpu_time()
            system_delta = current_system_time - previous_system_time

            # ------------------------------------------
            # Display table
            # ------------------------------------------

            os.system("clear")

            print("=" * 75)
            print("                     GRAND LINE GUARDIAN")
            print("=" * 75)
            print()

            print(
                f"{'':<3}"
                f"{'PID':<10}"
                f"{'PROCESS NAME':<25}"
                f"{'CPU %':<12}"
                f"{'MEMORY'}"
            )

            print("-" * 75)

            count = 0

            for index, pid in enumerate(pids):
                try:
                    process_name = get_process_name(pid)
                    memory = get_memory(pid)

                    current_process_time = get_process_cpu_time(pid)
                    process_delta = (
                        current_process_time
                        - previous_process_times.get(pid, 0)
                    )

                    if system_delta > 0:
                        cpu_percent = (process_delta / system_delta) * 100
                    else:
                        cpu_percent = 0

                    marker = ">" if index == selected else " "

                    print(
                        f"{marker:<3}"
                        f"{pid:<10}"
                        f"{process_name:<25}"
                        f"{cpu_percent:<12.2f}"
                        f"{memory}"
                    )

                    count += 1

                except (FileNotFoundError, IndexError, PermissionError):
                    # Process may have disappeared between snapshots
                    continue

            if count == 0:
                selected = 0
            elif selected >= count:
                selected = count - 1

            # ------------------------------------------
            # Footer
            # ------------------------------------------

            print("-" * 75)
            print(f"Total Active Processes: {count}")
            if status_message:
                print(status_message)
            print()
            print("Up/Down: move   x: terminate selected ship   q: quit")

    finally:
        # Restore normal terminal settings
        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            old_settings
        )

        print("\nGrand Line Guardian stopped.")


if __name__ == "__main__":
    main()
