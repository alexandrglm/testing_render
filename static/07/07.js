var map = L.map('map').setView([0, 0], 4); // [lat, long], zoom -> INICIALES!

var issIcon = L.icon({
    iconUrl: '/static/07/ico.png',
    iconSize: [50, 50],     
    iconAnchor: [25, 25], 
    popupAnchor: [0, -25]
});

/*
// tilelayer sat
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '&copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics'
}).addTo(map);

// tilelayer map normal
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);
*/
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '&copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics'
}).addTo(map);

var issMarker = L.marker([0, 0], {icon: issIcon}).addTo(map);

function updateISSPosition() {
    fetch('/07/iss_position')
        .then(response => response.json())
        .then(data => {
            var lat = data.latitude;
            var lon = data.longitude;
            issMarker.setLatLng([lat, lon]);
            map.setView([lat, lon], 4); // El Zoom de la actualización, cuidado
        })
        .catch(error => console.error('DEBUG: No data received:', error));
}

setInterval(updateISSPosition, 5000);
updateISSPosition();


/* Google NON free API key, left here for edu purposes
async function reloadingMap() {
    const response = await fetch('/iss_position');
    const data = await response.json();
    const longitude = data.longitude;
    const latitude = data.latitude;
    const apiKey = "";
    const map = `https://www.google.com/maps/embed/v1/MAP_MODE?key=${apiKey}&center=${latitude},${longitude}&zoom=4&maptype=satellite`;

    document.getElementById("map").src = map;
}

setInterval(reloadingMap, 5000);
reloadingMap();
*/