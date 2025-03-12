document.getElementById("convertButton").addEventListener("click", function() {
    let colorInputText = document.getElementById("inputColourText").value.trim().toUpperCase();

    let color1, color2, color3, color4;

    // If colour input text, use this
    if (colorInputText.length === 4) {
        color1 = colorInputText[0];
        color2 = colorInputText[1];
        color3 = colorInputText[2];
        color4 = colorInputText[3];
    } else {
        // Else, colour pickers
        color1 = document.getElementById("colour1Picker").value;
        color2 = document.getElementById("colour2Picker").value;
        color3 = document.getElementById("colour3Picker").value;
        color4 = document.getElementById("colour4Picker").value;
    }

    // JSON constructor
    let colorJSON = {
        color1: color1,
        color2: color2,
        color3: color3,
        color4: color4
    };

    // debug
    console.log("Sending JSON:", colorJSON); 

    // Fecth, POST
    fetch('/04/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(colorJSON)
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            console.error("ERROR, Bad response: ", result.error);
            document.getElementById("output").textContent = `Error: ${result.error}`;
        } else {
            document.getElementById("output").textContent = `Hex Value: ${result.final_color}`;
        }
    })
    .catch(error => console.error("ERROR: POST,Fetch:", error));
});
