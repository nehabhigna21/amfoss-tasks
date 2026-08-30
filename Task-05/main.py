
import time

from rich.console import Console
from rich.live import Live

import proc_reader
import ui
from actions import kill_process
from input_handler import RawTerminal,get_key
from models import ProcessRow

REFRESH_INTERVAL=0.5
STEP=0.05

def collect_rows(pids,previous_cpu_ticks,system_ticks_delta):
    rows=[]

    for pid in pids:
        try:
            name=proc_reader.get_process_name(pid)
            memory_kb=proc_reader.get_process_memory_kb(pid)

            current_ticks=proc_reader.get_process_cpu_ticks(pid)
            delta=current_ticks-previous_cpu_ticks.get(pid,0)

            if system_ticks_delta>0:
                cpu_percent=(delta/system_ticks_delta)*100
            else:
                cpu_percent=0.0

            rows.append(ProcessRow(pid=pid,name=name,cpu_percent=cpu_percent,memory_kb=memory_kb))

        except(FileNotFoundError,IndexError,PermissionError):
            continue

    return rows

def main():
    console=Console()
    selected=0
    status_message=""

    with RawTerminal(),Live(console=console,auto_refresh=False,screen=True)as live:
        while True:
            pids=proc_reader.list_pids()

            previous_cpu_ticks={pid:proc_reader.get_process_cpu_ticks(pid) for pid in pids}
            previous_idle,previous_total=proc_reader.get_system_cpu_times()

            quit_program=False
            elapsed=0.0

            while elapsed<REFRESH_INTERVAL:
                key=get_key()

                if key=="q":
                    quit_program=True
                    break
                elif key=="UP":
                    selected=max(0,selected-1)
                elif key=="DOWN"and pids:
                    selected=min(len(pids)-1,selected+1)
                elif key=="x"and pids:
                    status_message=kill_process(pids[selected])

                time.sleep(STEP)
                elapsed+=STEP

            if quit_program:
                break

            current_idle,current_total=proc_reader.get_system_cpu_times()
            total_delta=current_total-previous_total
            idle_delta=current_idle-previous_idle

            if total_delta>0:
                system_cpu_percent=(1-idle_delta/total_delta)*100
            else:
                system_cpu_percent=0.0

            mem_used_kb,mem_total_kb=proc_reader.get_system_memory_kb()

            rows=collect_rows(pids,previous_cpu_ticks,total_delta)

            if not rows:
                selected=0
            elif selected>=len(rows):
                selected=len(rows)-1

            live.update(
                ui.build_screen(
                    system_cpu_percent,
                    mem_used_kb,
                    mem_total_kb,
                    rows,
                    selected,
                    status_message,
                    console.size.height,
                )
            )
            live.refresh()

    print("\nGrand Line Guardian stopped.")

if __name__=="__main__":
    main()
