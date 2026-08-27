"""All reads of live process/system state from the /proc virtual filesystem."""

import os


def list_pids():
    return sorted((entry for entry in os.listdir("/proc") if entry.isdigit()), key=int)


def get_process_name(pid):
    try:
        with open(f"/proc/{pid}/comm", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "?"


def get_process_memory_kb(pid):
    try:
        with open(f"/proc/{pid}/status", "r") as file:
            for line in file:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1])
    except (FileNotFoundError, ValueError, IndexError):
        pass
    return 0


def get_process_cpu_ticks(pid):
    try:
        with open(f"/proc/{pid}/stat", "r") as file:
            values = file.read().split()
            # Field 14 = user CPU ticks, field 15 = kernel CPU ticks
            return int(values[13]) + int(values[14])
    except (FileNotFoundError, IndexError, ValueError):
        return 0


def get_system_cpu_times():
    """Return (idle_ticks, total_ticks) summed across all CPUs, from the
    first line of /proc/stat: user nice system idle iowait irq softirq ..."""
    try:
        with open("/proc/stat", "r") as file:
            values = [int(v) for v in file.readline().split()[1:]]
    except (FileNotFoundError, ValueError):
        return 0, 0

    idle = values[3] + (values[4] if len(values) > 4 else 0)  # idle + iowait
    total = sum(values)
    return idle, total


def get_system_memory_kb():
    """Return (used_kb, total_kb) for the whole system, from /proc/meminfo."""
    info = {}
    try:
        with open("/proc/meminfo", "r") as file:
            for line in file:
                key, _, rest = line.partition(":")
                info[key] = int(rest.split()[0])
    except (FileNotFoundError, ValueError, IndexError):
        return 0, 0

    total = info.get("MemTotal", 0)
    available = info.get("MemAvailable", info.get("MemFree", 0))
    return max(total - available, 0), total
