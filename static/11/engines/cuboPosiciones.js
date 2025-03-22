AFRAME.registerComponent('mover-cubo', {
  schema: {
    radio: { type: 'number', default: 3 }, 
    velocidad: { type: 'number', default: 0.0005 },
    altura: { type: 'number', default: 0.8 }
  },

  init: function () {


    this.angulo = 0;
  },

  tick: function (time, delta) {

    var cubo = this.el;

    // angulo = angulo * tiempo
    this.angulo += this.data.velocidad * delta; 

    /*
    Coseno
    seno
    */
    var ejeX = Math.cos(this.angulo) * this.data.radio; 
    var ejeZ = Math.sin(this.angulo) * this.data.radio; 
    var ejeY = this.data.altura + Math.sin(this.angulo * 2) * 0.5; 

    
    cubo.setAttribute('position', { x: ejeX, y: ejeY, z: ejeZ });
  }
});

document.querySelector('#cubo').setAttribute('mover-cubo', '');