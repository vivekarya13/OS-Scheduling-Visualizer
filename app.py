from flask import Flask, render_template, request, jsonify
from collections import deque

app = Flask(__name__)

# Global variable to hold processes
processes_data_store = []

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_process', methods=['POST'])
def add_process():
    data = request.json
    process = Process(data['name'], data['arrivalTime'], data['burstTime'])
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
            process.waiting_time = process.turnaround_time - (process.burst_time)
            
            output.append({
                "name": process.name,
                "arrival": process.arrival_time,
                "burst": process.burst_time,
                "completion": time,
                "turnaround": process.turnaround_time,
                "waiting": process.waiting_time,
            })
            
            # Mark the burst time as completed.
            process.remaining_time = 0

        # Remove completed processes from the queue
        queue = deque([p for p in queue if p.remaining_time > 0])

    return jsonify({"output": output})

@app.route('/reset', methods=['POST'])
def reset():
    global processes_data_store
    processes_data_store.clear()  # Clear stored processes on server side.
    return jsonify({"status": "success", "message": "Server state reset."})

if __name__ == '__main__':
    app.run(debug=True)