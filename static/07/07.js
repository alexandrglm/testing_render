const fetchPath = "/project/07"
var map = L.map('map').setView([0, 0], 4); // [lat, long], zoom -> INICIALES!

var issIcon = L.icon({
    iconUrl: '/static/07/ico.png',
    iconSize: [50, 50],     
    iconAnchor: [25, 25], 
    popupAnchor: [0, -25]
});


L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Source: Esri, Maxar, Earthstar Geographics'
}).addTo(map);

var issMarker = L.marker([0, 0], {icon: issIcon}).addTo(map);

function updateISSPosition() {
    fetch(`${fetchPath}/iss_position`)
        .then(response => response.json())
        .then(data => {
            var lat = data.latitude;
            var lon = data.longitude;
            issMarker.setLatLng([lat, lon]);
            map.setView([lat, lon], 4);
        })
        .catch(error => console.error('DEBUG: No data received:', error));
}

setInterval(updateISSPosition, 5000);
updateISSPosition();

