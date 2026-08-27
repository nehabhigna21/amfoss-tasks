package main

// Process represents a pirate crew waiting to be served by the CPU (Grand Line).
type Process struct {
	ID          string
	ArrivalTime int
	BurstTime   int
}

// GanttSegment is one contiguous slice of CPU time given to a process.
type GanttSegment struct {
	ID    string
	Start int
	End   int
}

// ProcessResult holds the computed scheduling metrics for a single process.
type ProcessResult struct {
	ID             string
	ArrivalTime    int
	BurstTime      int
	CompletionTime int
	TurnaroundTime int
	WaitingTime    int
}

// buildResults derives per-process metrics from the recorded completion times.
func buildResults(processes []Process, completion map[string]int) []ProcessResult {
	results := make([]ProcessResult, len(processes))
	for i, p := range processes {
		ct := completion[p.ID]
		tat := ct - p.ArrivalTime
		wt := tat - p.BurstTime
		results[i] = ProcessResult{
			ID:             p.ID,
			ArrivalTime:    p.ArrivalTime,
			BurstTime:      p.BurstTime,
			CompletionTime: ct,
			TurnaroundTime: tat,
			WaitingTime:    wt,
		}
	}
	return results
}
