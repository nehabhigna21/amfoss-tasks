
import os
import sys
import termios
import tty
import select

class RawTerminal:
    def __enter__(self):
        fd=sys.stdin.fileno()
        self._old_settings=termios.tcgetattr(fd)

        tty.setcbreak(fd)

        no_echo=termios.tcgetattr(fd)
        no_echo[3]&=~termios.ECHO
        termios.tcsetattr(fd,termios.TCSADRAIN,no_echo)

        return self

    def __exit__(self,*exc_info):
        termios.tcsetattr(sys.stdin,termios.TCSADRAIN,self._old_settings)

def get_key():
    fd=sys.stdin.fileno()

    if not select.select([fd],[],[],0)[0]:
        return None

    ch=os.read(fd,1).decode(errors="ignore")
    if ch!="\x1b":
        return ch

    if select.select([fd],[],[],0)[0]:
        ch2=os.read(fd,1).decode(errors="ignore")
        if ch2=="[" and select.select([fd],[],[],0)[0]:
            ch3=os.read(fd,1).decode(errors="ignore")
            return {"A":"UP","B":"DOWN"}.get(ch3)

    return "ESC"
