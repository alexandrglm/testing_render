document.addEventListener('DOMContentLoaded', function () {
    const socket = io();
    const output = document.getElementById('output');
    const jsonResponse = document.getElementById('json-response');
    const commandInput = document.getElementById('commandInput');

    function forceAutoscroll(element) {

        requestAnimationFrame(() => {
            element.scrollTop = element.scrollHeight;

        });
    }

    commandInput.addEventListener('keypress', function (e) {

        if (e.key === 'Enter') {

            const command = commandInput.value.trim();

            if (command) {
                socket.emit('execute_command', { command: command });


                output.innerHTML += `<div class="command-line">&gt; ${command}</div>`;

                commandInput.value = '';
                forceAutoscroll(output.parentElement);
            }
        }
    });

    // DEBUG
    socket.on('execute_command_response', function (data) {
        if (data.output) {
            output.innerHTML += `<div class="server-response">${data.output}</div>`;
            forceAutoscroll(output.parentElement);
        }

        if (data.raw_output) {
            jsonResponse.innerHTML += `<div class="json-response">${data.raw_output}</div>`;
            forceAutoscroll(jsonResponse.parentElement);
        }
    });
});
