const socket = io.connect('https://justlearn.ing');

socket.on('commander_output', (data) => {
    output.innerHTML += `
        <div>${data.output}</div>
        <br>
        <div>
            <span class="pwd-color">~$</span> 
            <input type="text" id="commandInput">
        </div>
    `;

    inputAlwaysOn();
    outputContainer.scrollTop = outputContainer.scrollHeight;
});

const output = document.getElementById('output');
const outputContainer = document.getElementById('output-container');


function inputAlwaysOn() {
    const commandInput = document.getElementById('commandInput');
    if (commandInput) {
        commandInput.focus();
    }
}

document.addEventListener('mousedown', (e) => {
    const commandInput = document.getElementById('commandInput');
    if (commandInput && e.target !== commandInput) {
        e.preventDefault();
        commandInput.focus();
    }
});
inputAlwaysOn();

let commanderHistorial = [];
let historialIdx = -1;

function handleCommand(command) {
    if (command) {
        commanderHistorial.unshift(command);
        historialIdx = -1;

        socket.emit('exec_commander', { command });

        const commandInput = document.getElementById('commandInput');
        if (commandInput) {
            commandInput.value = '';
        }
    }
}

document.addEventListener('keypress', (e) => {
    if (e.target.id === 'commandInput' && e.key === 'Enter') {
        const command = e.target.value.trim();
        handleCommand(command);
    }
});

document.addEventListener('keydown', (e) => {
    if (e.target.id === 'commandInput') {
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (historialIdx < commanderHistorial.length - 1) {
                historialIdx++;
                e.target.value = commanderHistorial[historialIdx];
            }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (historialIdx > 0) {
                historialIdx--;
                e.target.value = commanderHistorial[historialIdx];
            } else {
                historialIdx = -1;
                e.target.value = '';
            }
        }
    }
});


