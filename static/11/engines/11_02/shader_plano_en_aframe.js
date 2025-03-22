AFRAME.registerComponent('threejs-shader', {
    init: function () {
        // Crear un canvas para Three.js
        const canvas = document.createElement('canvas');
        canvas.id = 'webgl-canvas';
        canvas.style.position = 'absolute'; // Posicionar el canvas en la pantalla
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        document.body.appendChild(canvas);

        // Escena, cámara y renderizado de Three.js
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ canvas: canvas });
        renderer.setSize(window.innerWidth, window.innerHeight);

        // Geometría y material del shader
        const geometry = new THREE.PlaneGeometry(2, 2);

        const vertexShader = `
            void main() {
                gl_Position = vec4(position, 1.0);
            }
        `;

        const fragmentShader = `
            precision highp float;

            uniform vec2 iResolution;
            uniform float iTime;

            float grid(vec2 uv, float battery) {
                vec2 size = vec2(uv.y, uv.y * uv.y * 0.2) * 0.01;
                uv += vec2(0.0, iTime * 10.0 * (battery + 0.05));
                uv = abs(fract(uv) - 0.5);
                vec2 lines = smoothstep(size, vec2(0.0), uv);
                lines += smoothstep(size * 5.0, vec2(0.0), uv) * 0.4 * battery;
                return clamp(lines.x + lines.y, 0.0, 3.0);
            }

            void mainImage(out vec4 fragColor, in vec2 fragCoord) {
                vec2 uv = (2.0 * fragCoord.xy - iResolution.xy) / iResolution.y;
                float battery = 1.0;

                float fog = smoothstep(0.1, -0.02, abs(uv.y + 0.2));
                vec3 col = vec3(1, 0.1, 0.001);

                if (uv.y < -0.2) {
                    uv.y = 3.0 / (abs(uv.y + 0.2) + 0.05);
                    uv.x *= uv.y * 0.5;

                    uv += vec2(0.0, iTime * 10.0 * (battery + 0.05));

                    float fila = floor(uv.y);
                    float columna = floor(uv.x);

                    vec3 colorTesela1 = vec3(0.0, 0.0, 0.5);
                    vec3 colorTesela2 = vec3(0.5, 0.0, 0.5);

                    float patron = mod(fila + columna, 2.0);
                    col = (patron < 1.0) ? colorTesela1 : colorTesela2;

                    float gridVal = grid(uv, battery);
                    col = mix(col, vec3(0.5, 1., 0.22), gridVal);
                } else {
                    vec3 colorHorizonte = vec3(0.5, 1.0, 0.22);
                    vec3 colorCielo = vec3(0.5, 0.0, 0.5);

                    col = mix(colorHorizonte, colorCielo, smoothstep(-0.9, 1.0, uv.y));
                }

                col += fog * fog * fog;
                col = mix(vec3(col.r, col.r, col.r) * 0.5, col, battery * 0.7);

                fragColor = vec4(col, 1.0);
            }

            void main() {
                mainImage(gl_FragColor, gl_FragCoord.xy);
            }
        `;

        // Material con el shader
        const material = new THREE.ShaderMaterial({
            vertexShader,
            fragmentShader,
            uniforms: {
                iResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) },
                iTime: { value: 0.0 }
            }
        });

        const plane = new THREE.Mesh(geometry, material);
        scene.add(plane);

        // Cámara
        camera.position.z = 1;

        // Animación
        const animate = () => {
            requestAnimationFrame(animate);

            material.uniforms.iTime.value = performance.now() / 1000;
            renderer.render(scene, camera);
        };
        animate();
    }
});