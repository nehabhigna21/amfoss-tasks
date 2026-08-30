package main

import (
	"fmt"
	"strconv"
	"strings"
)
func PrintGantt(segments []GanttSegment) {
	if len(segments) == 0 {
		fmt.Println("(no execution)")
		return
	}

	var bar strings.Builder
	var ticks strings.Builder

	bar.WriteString("|")
	ticks.WriteString(strconv.Itoa(segments[0].Start))

	for _, seg := range segments {
		label := fmt.Sprintf(" %s ", seg.ID)
		bar.WriteString(label)
		bar.WriteString("|")

		endStr := strconv.Itoa(seg.End)
		padding := len(label) + 1 - len(endStr)
		if padding < 1 {
			padding = 1
		}
		ticks.WriteString(strings.Repeat(" ", padding))
		ticks.WriteString(endStr)
	}

	fmt.Println(bar.String())
	fmt.Println(ticks.String())
}
func PrintResults(results []ProcessResult) {
	fmt.Printf("\n%-8s %-8s %-8s %-10s %-12s %-10s\n",
		"PID", "Arrival", "Burst", "Complete", "Turnaround", "Waiting")

	var totalTAT, totalWT int
	for _, r := range results {
		fmt.Printf("%-8s %-8d %-8d %-10d %-12d %-10d\n",
			r.ID, r.ArrivalTime, r.BurstTime, r.CompletionTime, r.TurnaroundTime, r.WaitingTime)
		totalTAT += r.TurnaroundTime
		totalWT += r.WaitingTime
	}

	n := float64(len(results))
	fmt.Printf("\nAverage Waiting Time:    %.2f\n", float64(totalWT)/n)
	fmt.Printf("Average Turnaround Time: %.2f\n", float64(totalTAT)/n)
}
