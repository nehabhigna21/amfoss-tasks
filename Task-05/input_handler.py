"""Raw-mode terminal input: cbreak mode, no echo, non-blocking keypresses."""

import os
import sys
import termios
import tty
import select


class RawTerminal:
    """Context manager that puts the terminal into cbreak mode with echo
    disabled, and always restores the original settings on exit."""

    def __enter__(self):
        fd = sys.stdin.fileno()
        self._old_settings = termios.tcgetattr(fd)

        tty.setcbreak(fd)

        no_echo = termios.tcgetattr(fd)
        no_echo[3] &= ~termios.ECHO  # lflags
        termios.tcsetattr(fd, termios.TCSADRAIN, no_echo)

        return self

    def __exit__(self, *exc_info):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)


def get_key():
    """Read a single keypress without blocking, resolving arrow-key escape
    sequences (ESC [ A = up, ESC [ B = down). Returns None if nothing is
    pending.

    Reads go through os.read() on the raw file descriptor rather than the
    buffered sys.stdin wrapper. select() only reports bytes still sitting
    at the fd level -- if the buffered TextIOWrapper had already pulled
    extra bytes into its own internal buffer, a follow-up select() call
    would see nothing pending even though more of the escape sequence was
    already available, silently breaking arrow-key detection.
    """
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
