package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

var reader = bufio.NewReader(os.Stdin)

func readLine(prompt string) string {
	fmt.Print(prompt)
	line, _ := reader.ReadString('\n')
	return strings.TrimSpace(line)
}

func readInt(prompt string) int {
	for {
		val, err := strconv.Atoi(readLine(prompt))
		if err == nil {
			return val
		}
		fmt.Println("Please enter a whole number.")
	}
}

func readProcesses() []Process {
	n := readInt("How many pirate crews are arriving? ")
	processes := make([]Process, 0, n)
	for i := 1; i <= n; i++ {
		fmt.Printf("\n-- Crew %d --\n", i)
		id := readLine("  Process ID (e.g. P1): ")
		if id == "" {
			id = fmt.Sprintf("P%d", i)
		}
		arrival := readInt("  Arrival Time: ")
		burst := readInt("  Burst Time: ")
		processes = append(processes, Process{ID: id, ArrivalTime: arrival, BurstTime: burst})
	}
	return processes
}

func main() {
	fmt.Println("=========================================")
	fmt.Println(" Pirate King's Scheduler - CPU Simulator")
	fmt.Println("=========================================")

	processes := readProcesses()

	fmt.Println("\nChoose a scheduling algorithm:")
	fmt.Println("  1. First Come First Serve (FCFS)")
	fmt.Println("  2. Shortest Job First - Non-Preemptive (SJF)")
	fmt.Println("  3. Round Robin (RR)")

	var gantt []GanttSegment
	var results []ProcessResult

	for {
		choice := readLine("Enter choice [1-3]: ")
		switch choice {
		case "1":
			gantt, results = RunFCFS(processes)
		case "2":
			gantt, results = RunSJF(processes)
		case "3":
			quantum := readInt("Time Quantum: ")
			gantt, results = RunRoundRobin(processes, quantum)
		default:
			fmt.Println("Invalid choice, try again.")
			continue
		}
		break
	}

	fmt.Println("\nExecution Timeline (Gantt Chart)")
	PrintGantt(gantt)

	PrintResults(results)
}
