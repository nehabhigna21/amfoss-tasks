package main

import "sort"

// RunFCFS schedules crews strictly in arrival order. Ties in arrival time are
// broken by the order the crews were entered.
func RunFCFS(processes []Process) ([]GanttSegment, []ProcessResult) {
	order := make([]Process, len(processes))
	copy(order, processes)
	sort.SliceStable(order, func(i, j int) bool {
		return order[i].ArrivalTime < order[j].ArrivalTime
	})

	var gantt []GanttSegment
	completion := make(map[string]int)
	currentTime := 0

	for _, p := range order {
		if currentTime < p.ArrivalTime {
			currentTime = p.ArrivalTime
		}
		start := currentTime
		currentTime += p.BurstTime
		gantt = append(gantt, GanttSegment{ID: p.ID, Start: start, End: currentTime})
		completion[p.ID] = currentTime
	}

	return gantt, buildResults(processes, completion)
}
