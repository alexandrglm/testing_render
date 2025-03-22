// Movimiento con joysticks del Meta Quest...hay que mejorrlos

const camera = document.querySelector('[camera]');
const movementSpeed = 0.1;

document.querySelector('a-scene').addEventListener('thumbstickmoved', (event) => {
    const { x, y } = event.detail;
    const direction = new THREE.Vector3(x, 0, -y).normalize();
    camera.setAttribute('position', {
        x: camera.getAttribute('position').x + direction.x * movementSpeed,
        y: camera.getAttribute('position').y + direction.y * movementSpeed,
        z: camera.getAttribute('position').z + direction.z * movementSpeed
    });
});