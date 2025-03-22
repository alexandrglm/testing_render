/* Cambiar los shaders, por tiempo */
const shaders = ['16', '15', '14', '13', '12', '11', '6', '5', '4', '3', '2', '1'];
let currentIndex = 0;

function changeShader() {
const esfera = document.getElementById('esfera');
if (esfera) {
    esfera.setAttribute('material', 'shader', shaders[currentIndex]);
    currentIndex = (currentIndex + 1) % shaders.length;
}
}

setInterval(changeShader, 6000);


/* Pendiente:
Cambiar los shaders, por acciones:
- pueden ser acciones con los controles o las manos (los clicks en pc)
*/