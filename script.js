let processes = [];

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
            document.getElementById('processName').value = '';
            document.getElementById('arrivalTime').value = '';
            document.getElementById('burstTime').value = '';
        });
    } else {
        alert("Please fill in all fields correctly.");
    }
}

function runFCFS() {
    fetch('/run_fcfs')
        .then(response => response.json())
        .then(data => {
            document.getElementById('output').textContent = data.output.join('\n');
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
        document.getElementById('output').textContent = data.output.join('\n');
    });
}