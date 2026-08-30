
import os
import signal

def kill_process(pid):
    try:
        os.kill(int(pid),signal.SIGTERM)
        return f"Sent SIGTERM to PID {pid}"
    except ProcessLookupError:
        return f"PID {pid} no longer exists"
    except PermissionError:
        return f"Permission denied killing PID {pid}"
