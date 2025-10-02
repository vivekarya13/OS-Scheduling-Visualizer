# OS Scheduling Visualizer

## Project Overview
The OS Scheduling Visualizer is an educational tool designed to demonstrate various CPU scheduling algorithms. It provides a visual representation of how processes are managed by the CPU, allowing users to understand the dynamics of scheduling algorithms such as:

1. **First Come First Serve (FCFS)**
2. **Shortest Job First (SJF)**
3. **Shortest Remaining Time First (SRTF)**
4. **Round Robin (RR)**
5. **Priority Scheduling**

The tool features animated state diagrams that illustrate the lifecycle of processes as they transition between different states: New, Ready, Running, Waiting, and Terminated.

## Objectives
- To provide an intuitive understanding of CPU scheduling algorithms.
- To calculate and display key performance metrics like average waiting time, turnaround time, and CPU utilization.
- To allow users to input different processes with attributes like burst time, arrival time, and priority.
- To serve as a learning resource for students and instructors.

## File Structure

OS-Scheduling-Visualizer
├── app.py # Main Flask application handling backend logic
├── index.html # Frontend HTML file for user interface
├── script.js # JavaScript file managing interactivity and logic
└── styles.css # CSS file for styling the application


## How to Run the Project

### Prerequisites
- Python 3.x installed on your machine.
- Flask library installed. You can install it using pip:
  ```bash
  pip install Flask 
  ```
### Steps to Run the Application
```bash
cd OS-Scheduling-Visualizer
   ```
### Run the Flask Application:
Open a terminal or command prompt in the project directory and execute:
```bash
python app.py
```

### Access the Application:
Open your web browser and navigate to: http://127.0.0.1:5000/

## Using the Application:
- Add processes by filling in the required fields (Process Name, Arrival Time, Burst Time, Priority).
- Choose a scheduling algorithm by clicking the corresponding button.
- View the process table and Gantt chart for visual representation of scheduling.


## Expected Outcomes
- Animated state diagrams showing process transitions.
- Performance metrics for each scheduling algorithm.
- Interactive user input for testing different scenarios.

## Algorithms and Data Structures Used
- Algorithms:
FCFS - First Come First Serve Scheduling
SJF - Shortest Job First Scheduling
SRTF - Shortest Remaining Time First Scheduling
RR - Round Robin Scheduling
Priority - Priority based Scheduling

- Data Structures:
Queue: For simulating FCFS and Round Robin algorithms.
Min-Heap / Priority Queue: For SJF and Priority Scheduling.
Array/Linked List: To store process attributes.
Gantt Chart Structure: For visualizing process execution timelines.

Feel free to modify any sections according to your project's specific needs or details! If you have any further questions or need assistance with anything else, let me know!




