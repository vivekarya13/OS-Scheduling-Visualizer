from flask import Flask, render_template, request, jsonify
from collections import deque
import heapq

app = Flask(__name__)

# Global variable to hold processes
processes_data_store = []

class Process:
    def __init__(self, name, arrival_time, burst_time, priority=1):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.priority = priority  # Added priority attribute

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_process', methods=['POST'])
def add_process():
    data = request.json
    process = Process(data['name'], data['arrivalTime'], data['burstTime'], data.get('priority', 1))
    processes_data_store.append(process)
    return jsonify({"status": "success"})

@app.route('/run_fcfs', methods=['GET'])
def run_fcfs():
    time = 0
    output = []
    
    sorted_processes = sorted(processes_data_store, key=lambda p: p.arrival_time)

    for process in sorted_processes:
        if time < process.arrival_time:
            time = process.arrival_time
        
        process.completion_time = time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        
        output.append({
            "name": process.name,
            "arrival": process.arrival_time,
            "burst": process.burst_time,
            "completion": process.completion_time,
            "turnaround": process.turnaround_time,
            "waiting": process.waiting_time,
        })
        
        time += process.burst_time

    return jsonify({"output": output})

@app.route('/run_sjf', methods=['GET'])
def run_sjf():
    time = 0
    output = []
    
    processes_copy = sorted(processes_data_store, key=lambda p: (p.arrival_time, p.burst_time))
    
    while processes_copy:
        # Get only the processes that have arrived by the current time
        available_processes = [p for p in processes_copy if p.arrival_time <= time]
        
        if not available_processes:
            # If no processes are available, move time forward to the next arrival
            time = processes_copy[0].arrival_time
            continue
        
        # Select the process with the shortest burst time
        current_process = min(available_processes, key=lambda p: p.burst_time)
        
        # Update times for the selected process
        current_process.completion_time = time + current_process.burst_time
        current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
        
        output.append({
            "name": current_process.name,
            "arrival": current_process.arrival_time,
            "burst": current_process.burst_time,
            "completion": current_process.completion_time,
            "turnaround": current_process.turnaround_time,
            "waiting": current_process.waiting_time,
        })
        
        # Update the current time and remove the finished process from the list
        time += current_process.burst_time
        processes_copy.remove(current_process)

    return jsonify({"output": output})

@app.route('/run_srtf', methods=['GET'])
def run_srtf():
    time = 0
    output = []
    
    remaining_processes = sorted(processes_data_store, key=lambda p: p.arrival_time)

    while remaining_processes:
        # Get only the processes that have arrived by the current time
        available_processes = [p for p in remaining_processes if p.arrival_time <= time]
        
        if not available_processes:
            # If no processes are available, move time forward to the next arrival
            time += 1  # Increment until a new process arrives
            continue
        
        # Select the process with the shortest remaining time using SRTF logic.
        remaining_heap = [(p.remaining_time, p) for p in available_processes]
        
        # Get the process with the shortest remaining time from the heap.
        heapq.heapify(remaining_heap)
        
        _, current_process = heapq.heappop(remaining_heap)

        # Execute one unit of time on this process.
        current_process.remaining_time -= 1
        
        if current_process.remaining_time == 0:
            # Process has completed execution.
            current_process.completion_time = time + 1
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            
            output.append({
                "name": current_process.name,
                "arrival": current_process.arrival_time,
                "burst": current_process.burst_time,
                "completion": current_process.completion_time,
                "turnaround": current_process.turnaround_time,
                "waiting": current_process.waiting_time,
            })
            
            remaining_processes.remove(current_process)  # Remove completed process from list.
        
        time += 1  # Increment global time

    return jsonify({"output": output})

@app.route('/run_rr', methods=['POST'])
def run_rr():
    quantum = request.json['quantum']
    queue = deque(processes_data_store)
    time = 0
    output = []

    while queue:
        process = queue.popleft()
        
        if process.remaining_time > quantum:
            time += quantum
            process.remaining_time -= quantum
            queue.append(process)
        else:
            time += process.remaining_time
            process.completion_time = time
            process.turnaround_time = time - process.arrival_time
            process.waiting_time = process.turnaround_time - (process.burst_size)
            
            output.append({
                "name": process.name,
                "arrival": process.arrival_size,
                "burst": process.burst_size,
                "completion": time,
                "turnaround": process.turnaround_size,
                "waiting": process.waiting_size,
            })
            
            # Mark the burst time as completed.
            process.remaining_size=0

    return jsonify({"output": output})

@app.route('/run_priority', methods=['GET'])
def run_priority():
    time = 0
    output = []
    
    # Sort processes based on arrival time and then by priority
    sorted_processes = sorted(processes_data_store, key=lambda p: (p.arrival_time, p.priority))

    while sorted_processes:
        # Get only the processes that have arrived by the current time
        available_processes = [p for p in sorted_processes if p.arrival_time <= time]
        
        if not available_processes:
            # If no processes are available, move time forward to the next arrival
            time = sorted_processes[0].arrival_time
            continue
        
        # Select the highest priority (lowest number) job
        highest_priority_job = min(available_processes, key=lambda p: p.priority)

        # Update times for selected job
        highest_priority_job.completion_time = time + highest_priority_job.burst_time
        highest_priority_job.turnaround_time = highest_priority_job.completion_time - highest_priority_job.arrival_time
        highest_priority_job.waiting_time = highest_priority_job.turnaround_time - highest_priority_job.burst_time
        
        output.append({
            "name": highest_priority_job.name,
            "arrival": highest_priority_job.arrival_time,
            "burst": highest_priority_job.burst_time,
            "completion": highest_priority_job.completion_time,
            "turnaround": highest_priority_job.turnaround_time,
            "waiting": highest_priority_job.waiting_time,
        })
        
        # Update time and remove completed job from the list
        time += highest_priority_job.burst_time
        sorted_processes.remove(highest_priority_job)

    return jsonify({"output": output});

@app.route('/reset', methods=['POST'])
def reset():
    global processes_data_store
    processes_data_store.clear()  # Clear stored processes on server side.
    return jsonify({"status": "success", "message": "Server state reset."})

if __name__ == '__main__':
    app.run(debug=True)