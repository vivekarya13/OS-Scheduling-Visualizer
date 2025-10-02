let processes = [];
const colors = ["#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#FF33A8", "#33FFF3"]; // Array of colors

function addProcess() {
    const name = document.getElementById('processName').value;
    const arrivalTime = parseInt(document.getElementById('arrivalTime').value);
    const burstTime = parseInt(document.getElementById('burstTime').value);
    
    if (name && !isNaN(arrivalTime) && !isNaN(burstTime)) {
        fetch('/add_process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, arrivalTime, burstTime })
        }).then(response => response.json()).then(data => {
            alert(`Process ${name} added!`);
            
            // Display new process info
            const newProcessInfoDiv = document.getElementById('newProcessInfo');
            newProcessInfoDiv.innerHTML = `
                Process Name: ${name}<br />
                Arrival Time: ${arrivalTime}<br />
                Burst Time: ${burstTime}<br />
                `;

            // Clear input fields
            document.getElementById('processName').value = '';
            document.getElementById('arrivalTime').value = '';
            document.getElementById('burstTime').value = '';

            // Refresh the table after adding a new process
            refreshProcessTable();
        }).catch(error => {
            console.error("Error adding process:", error);
        });
    } else {
        alert("Please fill in all fields correctly.");
    }
}

function refreshProcessTable() {
    const tbody = document.querySelector('#processTable tbody');
    tbody.innerHTML = ''; // Clear existing rows
    
    processes.forEach((process, index) => {
        const row = `<tr>
            <td>${index + 1}</td>
            <td>${process.arrival}</td>
            <td>${process.burst}</td>
            <td>${process.completion}</td>
            <td>${process.turnaround}</td>
            <td>${process.waiting}</td>
        </tr>`;
        tbody.innerHTML += row; // Add new row for each process
    });
}

function runFCFS() {
    fetch('/run_fcfs')
        .then(response => response.json())
        .then(data => {
            processes = data.output; // Update global processes array with new data
            refreshProcessTable();
            displayGanttChart(data.output);
        }).catch(error => {
            console.error("Error running FCFS:", error);
        });
}

function runRR() {
    const quantum = parseInt(prompt("Enter Quantum Time:", "2"));
    
    if (isNaN(quantum) || quantum <= 0) {
        alert("Please enter a valid quantum time.");
        return;
    }

    fetch('/run_rr', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quantum })
    }).then(response => response.json()).then(data => {
        processes = data.output; // Update global processes array with new data
        refreshProcessTable();
        displayGanttChart(data.output);
    }).catch(error => {
        console.error("Error running Round Robin:", error);
    });
}

function displayGanttChart(output) {
    const ganttChartDiv = document.getElementById('ganttChart');
    ganttChartDiv.innerHTML = ''; // Clear previous Gantt chart
    
    let currentTime = 0;
    
    output.forEach((process, index) => {
        const startTime = Math.max(currentTime, process.arrival);
        const endTime = startTime + (process.burst || 0);
        
        const barWidth = (endTime - startTime) * 10; // Scale factor for visualization

        const barDiv = document.createElement('div');
        barDiv.style.width = `${barWidth}px`;
        barDiv.style.height = '50px';
        barDiv.style.backgroundColor = colors[index % colors.length]; // Assign color from array
        barDiv.style.position = 'absolute';
        barDiv.style.left = `${startTime * 10}px`; // Scale factor for positioning

        barDiv.innerText = `${process.name} (C:${process.completion})`; // Show process name and completion time
        barDiv.style.color = 'white';
        barDiv.style.textAlign = 'center';
        barDiv.style.lineHeight = '50px';

        ganttChartDiv.appendChild(barDiv);

        currentTime += (process.burst || 0); // Increment current time by burst time of the current process
    });

    // Add time scale below the Gantt chart
    addTimeScale(currentTime);
}

// Function to add a time scale below the Gantt chart
function addTimeScale(totalDuration) {
    const ganttChartDiv = document.getElementById('ganttChart');
    
    const scaleDiv = document.createElement('div');
    scaleDiv.style.position = 'relative';
    scaleDiv.style.height = '20px'; // Height for the scale

    for (let i = 0; i <= totalDuration; i++) {
        const tickMark = document.createElement('span');
        
        tickMark.innerText = i;
        tickMark.style.position = 'absolute';
        tickMark.style.left = `${i * 10}px`; // Scale factor for positioning
        tickMark.style.fontSize = '10px'; // Font size for tick marks

        scaleDiv.appendChild(tickMark);
    }

    ganttChartDiv.appendChild(scaleDiv); // Append scale below Gantt chart
}

// Function to reset all processes and clear the table and Gantt chart
function resetProcesses() {
    processes.length = 0; // Clear the processes array
    refreshProcessTable(); // Refresh the table to show no processes
    document.getElementById('newProcessInfo').innerHTML = ''; // Clear new process info display
}

// Function to clear all data and restart the server from scratch
function clearAllData() {
   if (confirm("Are you sure you want to clear all data and restart the server?")) {
       processes.length = 0; // Clear the processes array
       refreshProcessTable(); // Refresh the table to show no processes
       document.getElementById('newProcessInfo').innerHTML = ''; // Clear new process info display
       document.getElementById('ganttChart').innerHTML = ''; // Clear Gantt chart display

       // Reset input fields as well
       document.getElementById('processName').value = '';
       document.getElementById('arrivalTime').value = '';
       document.getElementById('burstTime').value = '';

       // Optionally, make an API call to reset any backend state if applicable.
       fetch('/reset', { method: 'POST' }) 
           .then(response => response.json())
           .then(data => console.log("Server reset successfully:", data))
           .catch(error => console.error("Error resetting server:", error));
   }
}