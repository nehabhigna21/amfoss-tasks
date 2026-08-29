package main

// RunSJF schedules crews using non-preemptive Shortest Job First: once a crew
// starts using the CPU it runs to completion. Among crews that have already
// arrived, the one with the smallest burst time goes next; ties are broken by
// arrival time, then by input order.
func RunSJF(processes []Process) ([]GanttSegment, []ProcessResult) {
	remaining := make([]Process, len(processes))
	copy(remaining, processes)
	done := make([]bool, len(remaining))

	var gantt []GanttSegment
	completion := make(map[string]int)
	currentTime := 0
	finished := 0

	for finished < len(remaining) {
		best := -1
		for i, p := range remaining {
			if done[i] || p.ArrivalTime > currentTime {
				continue
			}
			if best == -1 {
				best = i
				continue
			}
			bp := remaining[best]
			switch {
			case p.BurstTime < bp.BurstTime:
				best = i
			case p.BurstTime == bp.BurstTime && p.ArrivalTime < bp.ArrivalTime:
				best = i
			}
		}

		if best == -1 {
			// No crew has arrived yet; fast-forward to the next arrival.
			next := -1
			for i, p := range remaining {
				if done[i] {
					continue
				}
				if next == -1 || p.ArrivalTime < remaining[next].ArrivalTime {
					next = i
				}
			}
			currentTime = remaining[next].ArrivalTime
			continue
		}

		p := remaining[best]
		start := currentTime
		currentTime += p.BurstTime
		gantt = append(gantt, GanttSegment{ID: p.ID, Start: start, End: currentTime})
		completion[p.ID] = currentTime
		done[best] = true
		finished++
	}

	return gantt, buildResults(processes, completion)
}
