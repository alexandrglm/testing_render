AFRAME.registerComponent('rotate-cube', {
  tick: function (time, delta) {
    var cubo = this.el;
    var rotation = cubo.getAttribute('rotation');
    rotation.y += (delta / 1000) * 45; // 45 grados por segundo
    rotation.x += (delta / 1000) * 45; // 45 grados por segundo
    cubo.setAttribute('rotation', rotation);
  }
});

// Asigna el componente al cubo
document.querySelector('#cubo').setAttribute('rotate-cube', '');