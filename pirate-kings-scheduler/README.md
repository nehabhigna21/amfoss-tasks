# Pirate King's Scheduler

A terminal-based CPU scheduling simulator written in Go. Each pirate crew
arriving across the Grand Line is modeled as a process waiting for CPU time.
The simulator supports three classic scheduling algorithms and reports the
resulting execution timeline and performance metrics.

## Algorithms implemented

- **First Come First Serve (FCFS)** — crews are served strictly in arrival
  order.
- **Shortest Job First, Non-Preemptive (SJF)** — among crews that have
  already arrived, the one with the smallest burst time runs next; once
  started, a crew runs to completion.
- **Round Robin (RR)** — each crew gets a fixed time slice (the quantum).
  Crews that arrive while another is running join the back of the ready
  queue, ahead of the crew that just gave up the CPU.

## Approach

The program is split by responsibility:

- `models.go` — the `Process`, `GanttSegment`, and `ProcessResult` types, and
  a shared helper that turns a map of completion times into per-process
  turnaround/waiting time metrics.
- `fcfs.go`, `sjf.go`, `roundrobin.go` — one file per algorithm. Each exposes
  a `Run*` function that takes the list of processes (and, for Round Robin,
  the time quantum) and returns the Gantt chart segments plus the computed
  results. Keeping each algorithm in its own file/function made it easy to
  verify each one independently against hand-worked examples.
- `display.go` — renders the Gantt chart as an ASCII timeline bar and prints
  the results table with per-process and average waiting/turnaround times.
- `main.go` — the terminal UI: reads the number of crews and their
  Process ID / Arrival Time / Burst Time, lets the user pick an algorithm
  (asking for the Time Quantum only when Round Robin is chosen), then runs
  the simulation and prints the output.

Waiting Time and Turnaround Time are derived the standard way once a
process's completion time is known:

```
TurnaroundTime = CompletionTime - ArrivalTime
WaitingTime    = TurnaroundTime - BurstTime
```

Round Robin was the trickiest part: new arrivals have to be enqueued
*before* re-queuing the process that just used up its quantum, otherwise a
process that arrives at the exact moment another's slice ends gets served
out of order.

## Running it

```bash
go run .
```

You'll be prompted for:

1. How many crews are arriving
2. Each crew's Process ID, Arrival Time, and Burst Time
3. Which algorithm to run (FCFS / SJF / Round Robin)
4. The Time Quantum, if Round Robin was chosen

Example session and output:

```
=========================================
 Pirate King's Scheduler - CPU Simulator
=========================================
How many pirate crews are arriving? 4

-- Crew 1 --
  Process ID (e.g. P1): P1
  Arrival Time: 0
  Burst Time: 5
...

Choose a scheduling algorithm:
  1. First Come First Serve (FCFS)
  2. Shortest Job First - Non-Preemptive (SJF)
  3. Round Robin (RR)
Enter choice [1-3]: 1

Execution Timeline (Gantt Chart)
| P1 | P2 | P3 | P4 |
0    5    8   16   22

PID      Arrival  Burst    Complete   Turnaround   Waiting
P1       0        5        5          5            0
P2       1        3        8          7            4
P3       2        8        16         14           6
P4       3        6        22         19           13

Average Waiting Time:    5.75
Average Turnaround Time: 11.25
```

## Resources used

- [GeeksforGeeks — CPU Scheduling Algorithms](https://www.geeksforgeeks.org/cpu-scheduling-in-operating-systems/)
- [Go documentation](https://go.dev/doc/) for standard library usage
  (`bufio`, `sort`, `strconv`)

## New concepts learned

- The difference between preemptive and non-preemptive scheduling, and why
  SJF as specified here (non-preemptive) can still cause starvation of
  long jobs even though it minimizes average waiting time for a given batch.
- How Round Robin's fairness depends on queue *ordering*, not just the
  quantum size — enqueuing newly arrived processes before re-queuing the
  interrupted one is what keeps the simulation matching the textbook
  definition.
- Structuring a small Go CLI program across multiple files by
  responsibility (models, algorithms, display, entry point) instead of one
  large `main.go`.
