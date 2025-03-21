// Preloading socket url via promise - secret
let socket;

async function socketInit() {
    try {

        const response = await fetch('API_Secrets');
        
        const data = await response.json();


        const shell_uri = data.shell_uri;

        socket = io.connect(`${shell_uri}`);


        await new Promise((resolve, reject) => {
            socket.on('connect', () => {
                console.log('DEBUG: Promise OK, Secret OK, Socket OK');
                resolve();
            });

            socket.on('connect_error', (error) => {
                console.error('DEBUG: Promise ERROR - ', error);
                reject(error);
            });
        });
        
        initializeApp();

    } catch (error) {
        
        console.error('DEBUG: Promise OK, Socket ERROR (maybe URL???)', error);
    
    }
}

socketInit();


function initializeApp() {
    
    const output = document.getElementById('output');
    const outputContainer = document.getElementById('output-container');

    let commanderHistorial = [];
    let historialIdx = -1;

    const commandInput = document.createElement('input');
    commandInput.type = 'text';
    commandInput.id = 'commandInput';
    commandInput.style.backgroundColor = 'transparent';
    commandInput.style.color = 'whitesmoke';
    commandInput.style.fontFamily = '"JetBrains Mono", monospace';
    commandInput.style.fontSize = '1.5rem';
    commandInput.style.border = 'none';
    commandInput.style.outline = 'none';
    commandInput.style.padding = '0';
    commandInput.style.margin = '0 0 0 1.5em';
    commandInput.style.display = 'inline-block';
    commandInput.style.width = 'calc(100% - 10ch)';
    commandInput.style.caretColor = '#8fbc8f';

    function inputAlwaysOn() {
    
        commandInput.focus();
    }

    function handleCommand(command) {
    
        if (command) {
    
            commanderHistorial.unshift(command);
            historialIdx = -1;

            socket.emit('exec_commander', { command });

            commandInput.value = '';
        }
    }

    commandInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const command = e.target.value.trim();
            handleCommand(command);
        }
    });

    commandInput.addEventListener('keydown', (e) => {
    
        if (e.key === 'ArrowUp') {
            e.preventDefault();
    
            if (historialIdx < commanderHistorial.length - 1) {
                historialIdx++;
    
                commandInput.value = commanderHistorial[historialIdx];
            }
    
        } else if (e.key === 'ArrowDown') {
    
            e.preventDefault();
    
            if (historialIdx > 0) {
                historialIdx--;
    
                commandInput.value = commanderHistorial[historialIdx];
    
            } else {
    
                historialIdx = -1;
                commandInput.value = '';
            }
        }
    });

    document.addEventListener('mousedown', (e) => {
        if (e.target !== commandInput) {
            e.preventDefault();
            commandInput.focus();
        }
    });

    socket.on('commander_output', (data) => {
    
        const outputLine = document.createElement('div');
    
        outputLine.textContent = data.output;
    
        output.appendChild(outputLine);

        const newLine = document.createElement('div');
    
        newLine.innerHTML = `<br><span class="pwd-color">~$</span>`;
    
        newLine.appendChild(commandInput);

        output.appendChild(newLine);

        inputAlwaysOn();

        outputContainer.scrollTop = outputContainer.scrollHeight;
    });

    const initialLine = document.createElement('div');
    
    initialLine.innerHTML = `<span class="pwd-color">WebShell~$</span>`;
    
    initialLine.appendChild(commandInput);
    
    output.appendChild(initialLine);

    inputAlwaysOn();
}