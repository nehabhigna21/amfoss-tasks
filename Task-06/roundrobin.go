package main
import "sort"
func RunRoundRobin(processes []Process, quantum int) ([]GanttSegment, []ProcessResult) {
	byArrival := make([]Process, len(processes))
	copy(byArrival, processes)
	sort.SliceStable(byArrival, func(i, j int) bool {
		return byArrival[i].ArrivalTime < byArrival[j].ArrivalTime
	})
	remaining := make(map[string]int, len(processes))
	for _, p := range processes {
		remaining[p.ID] = p.BurstTime
	}

	var gantt []GanttSegment
	completion := make(map[string]int)

	arrived := make([]bool, len(byArrival))
	var queue []int
	currentTime := 0

	enqueueArrivals := func(upTo int) {
		for i, p := range byArrival {
			if !arrived[i] && p.ArrivalTime <= upTo {
				arrived[i] = true
				queue = append(queue, i)
			}
		}
	}

	if len(byArrival) > 0 {
		currentTime = byArrival[0].ArrivalTime
	}
	enqueueArrivals(currentTime)

	finished := 0
	for finished < len(byArrival) {
		if len(queue) == 0 {
			
			next := -1
			for i, p := range byArrival {
				if !arrived[i] && (next == -1 || p.ArrivalTime < byArrival[next].ArrivalTime) {
					next = i
				}
			}
			currentTime = byArrival[next].ArrivalTime
			enqueueArrivals(currentTime)
			continue
		}

		idx := queue[0]
		queue = queue[1:]
		p := byArrival[idx]

		run := quantum
		if remaining[p.ID] < run {
			run = remaining[p.ID]
		}

		start := currentTime
		currentTime += run
		remaining[p.ID] -= run
		gantt = append(gantt, GanttSegment{ID: p.ID, Start: start, End: currentTime})

		enqueueArrivals(currentTime)

		if remaining[p.ID] == 0 {
			completion[p.ID] = currentTime
			finished++
		} else {
			queue = append(queue, idx)
		}
	}

	return gantt, buildResults(processes, completion)
}
