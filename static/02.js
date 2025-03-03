"use strict";
var _a;
// Defined all posible colour with each own bin value. Consts don't work as inteded. Function instead. Switch - type - case used.
function colour2Bin(colour) {
    switch (colour.toUpperCase()) {
        case "B": return "00";
        case "Y": return "01";
        case "C": return "10";
        case "R": return "11";
        default: return "00";
    }
}
// Parsed the entire (2 blocks) bin value to hex, as string.
function bin2Hex(bin) {
    return parseInt(bin, 2).toString(16).toUpperCase().padStart(2, '0');
}
// This function reorder the bin values littleEndian Right to Left, as needed on Z80 CPC
function binReorderedR2L(mixed) {
    const binJoint = mixed.split('').map(colour2Bin);
    const binBlock1 = binJoint.map(b => b[1]).join('');
    const binBlock2 = binJoint.map(b => b[0]).join('');
    return binBlock1 + binBlock2;
}
// Here, all conversions are done while showing both final bin&hex values
function parseValuesAllSteps() {
    const dataTextInput = document.getElementById("inputColourText").value;
    const colour1Picker = document.getElementById("colour1Picker").value;
    const colour2Picker = document.getElementById("colour2Picker").value;
    const colour3Picker = document.getElementById("colour3Picker").value;
    const colour4Picker = document.getElementById("colour4Picker").value;
    const mixed = dataTextInput ? dataInputValidation(dataTextInput) : `${colour1Picker}${colour2Picker}${colour3Picker}${colour4Picker}`;
    const output = document.getElementById("output");
    if (mixed.length === 4) {
        const bin = binReorderedR2L(mixed);
        const hexValues = bin2Hex(bin);
        output.textContent = `D0ne! - Colour String: ${mixed} -> Fixed bin value: ${bin} -> Final hex value: ${hexValues}`;
    }
    else {
        output.textContent = "ERROR! Data content should be XXXX. Four digits, one valid colour (B,Y,C,R) for each block.";
    }
}
// Data input validation  method
function dataInputValidation(dataTextInput) {
    const coloursUppercase = ["B", "Y", "C", "R"];
    const fixedInput = dataTextInput.toUpperCase().replace(/[^BYCR]/g, "").trim();
    return fixedInput.length === 4 ? fixedInput : "";
}
(_a = document.getElementById("convertButton")) === null || _a === void 0 ? void 0 : _a.addEventListener("click", parseValuesAllSteps);

