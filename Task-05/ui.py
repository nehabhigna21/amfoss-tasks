
from datetime import datetime
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

def format_kb(kb):
    if kb>=1024*1024:
        return f"{kb/(1024*1024):.2f} GB"
    if kb>=1024:
        return f"{kb/1024:.1f} MB"
    return f"{kb} kB"

def build_header(cpu_percent,mem_used_kb,mem_total_kb,process_count):
    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mem_percent=(mem_used_kb/mem_total_kb*100)if mem_total_kb else 0

    stats=Text()
    stats.append(f"Time: {now}",style="bold cyan")
    stats.append("    ")
    stats.append(f"Total CPU: {cpu_percent:5.1f}%",style="bold yellow")
    stats.append("    ")
    stats.append(
        f"Total Memory: {format_kb(mem_used_kb)} / {format_kb(mem_total_kb)} "
        f"({mem_percent:.1f}%)",
        style="bold magenta",
    )
    stats.append("    ")
    stats.append(f"Active Processes: {process_count}",style="bold green")

    return Panel(stats,title="GRAND LINE GUARDIAN",border_style="cyan")

def build_table(rows,selected_index):
    table=Table(expand=True,show_lines=False)
    table.add_column("",width=1)
    table.add_column("PID",justify="right")
    table.add_column("Process Name")
    table.add_column("CPU %",justify="right")
    table.add_column("Memory",justify="right")

    for index,row in enumerate(rows):
        is_selected=index==selected_index
        table.add_row(
            ">" if is_selected else "",
            row.pid,
            row.name,
            f"{row.cpu_percent:.2f}",
            format_kb(row.memory_kb),
            style="reverse" if is_selected else None,
        )

    return table

NON_TABLE_LINES=11

def build_footer(status_message,scroll_info=None):
    status_line=Text(status_message,style="bold red") if status_message else Text("")

    controls=Text("Up/Down: move   x: terminate selected ship   q: quit")
    if scroll_info:
        start,end,total=scroll_info
        controls=Text(f"Showing {start+1}-{end} of {total} processes    ")+controls

    return Panel(Group(status_line,controls),border_style="cyan")

def build_screen(cpu_percent,mem_used_kb,mem_total_kb,all_rows,selected_index,status_message,terminal_height):
   
    available=max(terminal_height-NON_TABLE_LINES,3)

    if len(all_rows)>available:
        start=max(0,selected_index-available//2)
        start=min(start,len(all_rows)-available)
        visible_rows=all_rows[start:start+available]
        visible_selected=selected_index-start
        scroll_info=(start,start+len(visible_rows),len(all_rows))
    else:
        visible_rows=all_rows
        visible_selected=selected_index
        scroll_info=None

    return Group(
        build_header(cpu_percent,mem_used_kb,mem_total_kb,len(all_rows)),
        build_table(visible_rows,visible_selected),
        build_footer(status_message,scroll_info),
    )
