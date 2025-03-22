// Logica para agarrar el cubo, debe mejorar.

const cubo = document.getElementById('cubo');
const grabPoint = document.getElementById('grabPoint');
let isGrabbing = false;

document.getElementById('rightHand').addEventListener('gripdown', () => {
    if (!isGrabbing) {
        cubo.setAttribute('dynamic-body', 'mass: 0');
        cubo.setAttribute('position', grabPoint.getAttribute('position'));
        cubo.setAttribute('constraint', 'target: #grabPoint; type: lock');
        isGrabbing = true;
    }
});

document.getElementById('rightHand').addEventListener('gripup', () => {
    if (isGrabbing) {
        cubo.removeAttribute('constraint');
        cubo.setAttribute('dynamic-body', 'mass: 2');
        isGrabbing = false;
    }
});