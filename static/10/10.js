const WebShell = {
    socket: io.connect('https://justlearn.ing'),
    
    outputContainer: document.getElementById('output-container'),
    output: document.getElementById('output'),
    
    commandInput: null,
    
    commanderHistorial: [],
    historialIdx: -1,

    inputActive() {
        if (this.commandInput) {
            this.commandInput.focus();
        }
    },

    updateHistory(command) {
        if (command) {
            this.commanderHistorial.unshift(command);
            this.historialIdx = -1;
        }
    },

    handleCommand(command) {
        
        if (command) {
            
            this.updateHistory(command);
            this.socket.emit('exec_commander', { command });
            this.commandInput.value = '';
        }
    },

    renderNewPrompt() {
        
        this.output.innerHTML += `<div><span class="pwd-color">shell: ~$</span> <input type="text" id="commandInput"></div>`;
        this.commandInput = document.getElementById('commandInput');
        
        this.inputActive();
    },

    initEvents() {

        document.addEventListener('keypress', (e) => {
            
            if (e.target.id === 'commandInput' && e.key === 'Enter') {
                this.handleCommand(e.target.value.trim());
            }
        });

        document.addEventListener('keydown', (e) => {
            
            if (e.target.id === 'commandInput') {
                
                if (e.key === 'ArrowUp') {
                    
                    e.preventDefault();
                    
                    if (this.historialIdx < this.commanderHistorial.length - 1) {
                        
                        this.historialIdx++;
                        
                        e.target.value = this.commanderHistorial[this.historialIdx];
                    }
                
                } else if (e.key === 'ArrowDown') {
                    
                    e.preventDefault();
                    
                    if (this.historialIdx > 0) {
                        
                        this.historialIdx--;
                        
                        e.target.value = this.commanderHistorial[this.historialIdx];
                    
                    } else {
                        
                        this.historialIdx = -1;
                        
                        e.target.value = '';
                    }
                }
            }
        });

        document.addEventListener('mousedown', (e) => {
            if (e.target.id !== 'commandInput') {
                e.preventDefault();
                this.inputActive();
            }
        });

        this.socket.on('commander_output', (data) => {
            this.output.innerHTML += `<div>${data.output}</div><br>`;
            this.renderNewPrompt();
            this.outputContainer.scrollTop = this.outputContainer.scrollHeight;
        });
    },

    init() {
        this.renderNewPrompt();
        this.initEvents();
    }
};  

WebShell.init();
