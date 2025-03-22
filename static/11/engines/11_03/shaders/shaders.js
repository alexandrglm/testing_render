/*
Todos los shaders globales, aquí

Todos son test
*/

// Shader spaceharrier primitiva plano
AFRAME.registerShader('planoShader', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        precision highp float;
  
        uniform float time;
        varying vec2 vUv;
  
        float grid(vec2 uv, float battery)
        {
            vec2 size = vec2(uv.y, uv.y * uv.y * 0.00002) * 0.00001;
            uv += vec2(0.0, time * 0.00001 );
            uv = abs(fract(uv) - 0.5);
            vec2 lines = smoothstep(size, vec2(0.0), uv);
            lines += smoothstep(size * 5.0, vec2(0.0), uv) * 0.8 * battery;
            return clamp(lines.x + lines.y, 0.0, 3.0);
        }
  
        void main() {

            //ESCALAR LOS UV's
            vec2 uv = vUv * 2.0;
            float battery = 1.0;
  
            // Suelo (grid)

            // Horizonte va junto con PROPORCION SUELO y FOG
            float fog = smoothstep(0.1, -0.02, abs(uv.y - 0.9));
            // Color de suelo 1
            vec3 col = vec3(1, 0.1, 0.001);
  
            /// PROPORCION SUELO 1
            if (uv.y < 0.9) 
            {
                /// PROPORCION SUELO 2, creación de suelo junto a horizonte
                uv.y = 3.0 / (abs(uv.y - 0.9) + 0.05); 
                uv.x *= uv.y * 0.5;
  
                // TESELAS 1: Desplazamiento teselas (igual que grid)
                uv += vec2(0.0, time * 10.0 * (battery + 0.05));
  
                // TESELAS 2: filas y columnas
                float fila = floor(uv.y);
                float columna = floor(uv.x);
  
                // TESELAS 3: colores
                // Ojo, la malla se hace suelo por encima de teselas.
                vec3 colorTesela1 = vec3(0.0, 0.0, 0.5); 
                vec3 colorTesela2 = vec3(0.5, 0.0, 0.5); 
  
                // TESELAS 4: Ajedrez
                float patron = mod(fila + columna, 2.0);
                col = (patron < 1.0) ? colorTesela1 : colorTesela2;
  
                // GRID 1:  Superposición a teselas y color.
                float gridVal = grid(uv, battery);
                col = mix(col, vec3(0.5, 1., 0.22), gridVal);
            }
            else
            {
                // Cielo 1:
                vec3 colorHorizonte = vec3(0.5, 1.0, 0.22);
                vec3 colorCielo = vec3(0.5, 0.0, 0.5);
  
                // Mezclar horizonte y cielo basado en la coordenada Y
                col = mix(colorHorizonte, colorCielo, smoothstep(0.7, 1.0, uv.y));
            }
  
            // Aplicar niebla
            col += fog * fog * fog;
            col = mix(vec3(col.r, col.r, col.r) * 0.5, col, battery * 0.7);
  
            gl_FragColor = vec4(col, 1.0);
        }
    `
  });


// Shaders 1
AFRAME.registerShader('1', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec2 vUv;
        void main() {
            float angle = atan(vUv.y - 0.5, vUv.x - 0.5) * 20.0;
            float radius = length(vUv - vec2(0.5));
            float pattern = sin(angle + time * 0.005) * cos(radius * 25.0 + time * 0.005);
            vec3 color1 = vec3(0.8, 0.2, 0.5) * sin(time * 0.003 + pattern);
            vec3 color2 = vec3(0.2, 0.8, 0.5) * cos(time * 0.003 - pattern);
            vec3 finalColor = mix(color1, color2, 0.5 + 0.5 * sin(time * 0.003));
            gl_FragColor = vec4(finalColor, 1.0);
        }
    `
});

// Shader 2: Spiral Kaleidoscope
AFRAME.registerShader('2', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec2 vUv;
        void main() {
            vec2 p = vUv - vec2(0.5);
            float r = length(p);
            float a = atan(p.y, p.x);
            float spiral = sin(10.0 * (r + a + time * 0.01));
            vec3 color = vec3(0.5 + 0.5 * spiral, 0.5 + 0.5 * cos(spiral), 0.5 + 0.5 * sin(spiral));
            gl_FragColor = vec4(color, 1.0);
        }
    `
});

// Shader 3: Radial Kaleidoscope
AFRAME.registerShader('3', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec2 vUv;
        void main() {
            vec2 p = vUv - vec2(0.5);
            float r = length(p);
            float a = atan(p.y, p.x);
            float radial = sin(10.0 * r + time * 0.01);
            vec3 color = vec3(0.5 + 0.5 * radial, 0.5 + 0.5 * cos(radial), 0.5 + 0.5 * sin(radial));
            gl_FragColor = vec4(color, 1.0);
        }
    `
});

// Shader 4: Fractal Kaleidoscope
AFRAME.registerShader('4', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec2 vUv;
        void main() {
            vec2 p = vUv - vec2(0.5);
            float r = length(p);
            float a = atan(p.y, p.x);
            float fractal = sin(10.0 * r + time * 0.01) * cos(10.0 * a + time * 0.01);
            vec3 color = vec3(0.5 + 0.5 * fractal, 0.5 + 0.5 * cos(fractal), 0.5 + 0.5 * sin(fractal));
            gl_FragColor = vec4(color, 1.0);
        }
    `
});

// Shader 5: Wave Kaleidoscope
AFRAME.registerShader('5', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec2 vUv;
        void main() {
            vec2 p = vUv - vec2(0.5);
            float r = length(p);
            float a = atan(p.y, p.x);
            float wave = sin(10.0 * r + time * 0.01) * cos(10.0 * a + time * 0.01);
            vec3 color = vec3(0.5 + 0.5 * wave, 0.5 + 0.5 * cos(wave), 0.5 + 0.5 * sin(wave));
            gl_FragColor = vec4(color, 1.0);
        }
    `
});

// Shader 6: Espejo Fractal
AFRAME.registerShader('6', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec2 vUv;
        void main() {
            vec2 p = vUv - vec2(0.5);
            float r = length(p);
            float a = atan(p.y, p.x);
            float fractal = sin(10.0 * r + time * 0.01) * cos(10.0 * a + time * 0.01);
            vec3 color = vec3(
                0.5 + 0.5 * fractal,
                0.5 + 0.5 * cos(fractal + time * 0.02),
                0.5 + 0.5 * sin(fractal + time * 0.03)
            );
            gl_FragColor = vec4(color, 1.0);
        }
    `
});

// Shader 7: Vortex de Colores
AFRAME.registerShader('7', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec2 vUv;
        void main() {
            vec2 p = vUv - vec2(0.5);
            float r = length(p);
            float a = atan(p.y, p.x);
            float vortex = sin(10.0 * r + time * 0.01) * cos(10.0 * a + time * 0.01);
            vec3 color = vec3(
                0.5 + 0.5 * sin(vortex + time * 0.01),
                0.5 + 0.5 * cos(vortex + time * 0.02),
                0.5 + 0.5 * sin(vortex + time * 0.03)
            );
            gl_FragColor = vec4(color, 1.0);
        }
    `
});

// Shader 8: Espejo Caleidoscópico
AFRAME.registerShader('8', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec2 vUv;
        void main() {
            vec2 p = vUv - vec2(0.5);
            float r = length(p);
            float a = atan(p.y, p.x);
            float mirror = sin(10.0 * r + time * 0.01) * cos(10.0 * a + time * 0.01);
            vec3 color = vec3(
                0.5 + 0.5 * sin(mirror + time * 0.01),
                0.5 + 0.5 * cos(mirror + time * 0.02),
                0.5 + 0.5 * sin(mirror + time * 0.03)
            );
            gl_FragColor = vec4(color, 1.0);
        }
    `
});

// Shader 9: Liminal Space
AFRAME.registerShader('9', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec2 vUv;
        void main() {
            vec2 p = vUv - vec2(0.5);
            float r = length(p);
            float a = atan(p.y, p.x);
            float liminal = sin(10.0 * r + time * 0.01) * cos(10.0 * a + time * 0.01);
            vec3 color = vec3(
                0.5 + 0.5 * sin(liminal + time * 0.01),
                0.5 + 0.5 * cos(liminal + time * 0.02),
                0.5 + 0.5 * sin(liminal + time * 0.03)
            );
            gl_FragColor = vec4(color, 1.0);
        }
    `
});

// Shader 10: AR Espejo
AFRAME.registerShader('10', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec2 vUv;
        void main() {
            vec2 p = vUv - vec2(0.5);
            float r = length(p);
            float a = atan(p.y, p.x);
            float arMirror = sin(10.0 * r + time * 0.01) * cos(10.0 * a + time * 0.01);
            vec3 color = vec3(
                0.5 + 0.5 * sin(arMirror + time * 0.01),
                0.5 + 0.5 * cos(arMirror + time * 0.02),
                0.5 + 0.5 * sin(arMirror + time * 0.03)
            );
            gl_FragColor = vec4(color, 1.0);
        }
    `
});
// Shader 11: Neon Vortex
AFRAME.registerShader('11', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
    varying vec2 vUv;
    void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
    `,
    fragmentShader: `
    uniform float time;
    varying vec2 vUv;
    void main() {
        vec2 p = vUv - 0.5;
        float angle = atan(p.y, p.x) + time * 0.05;
        float radius = length(p);
        float glow = sin(radius * 20.0 - time * 0.1) * cos(angle * 10.0);
        vec3 color = vec3(0.8 + 0.2 * glow, 0.2 + 0.8 * cos(glow * 2.0), 0.3 + 0.7 * sin(glow * 3.0));
        gl_FragColor = vec4(color, 1.0);
    }
    `
});

// Shader 12: Galactic Feathers
AFRAME.registerShader('12', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
    varying vec2 vUv;
    void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
    `,
    fragmentShader: `
    uniform float time;
    varying vec2 vUv;
    void main() {
        vec2 p = vUv * 2.0 - 1.0;
        float wave = sin(p.x * 15.0 + time * 0.1) * cos(p.y * 15.0 + time * 0.1);
        float feather = smoothstep(0.3, 0.7, wave);
        vec3 color = vec3(0.2 + 0.8 * feather, 0.4 + 0.6 * cos(feather * 2.0), 0.6 + 0.4 * sin(feather * 3.0));
        gl_FragColor = vec4(color, 1.0);
    }
    `
});

// Shader 13: Star Explosion
AFRAME.registerShader('13', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
    varying vec2 vUv;
    void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
    `,
    fragmentShader: `
    uniform float time;
    varying vec2 vUv;
    void main() {
        vec2 p = vUv - 0.5;
        float r = length(p);
        float a = atan(p.y, p.x);
        float explosion = sin(r * 30.0 - time * 0.2) * cos(a * 20.0);
        vec3 color = vec3(0.5 + 0.5 * explosion, 0.5 + 0.5 * cos(explosion * 3.0), 0.5 + 0.5 * sin(explosion * 5.0));
        gl_FragColor = vec4(color, 1.0);
    }
    `
});

// Shader 14: Cosmic Peacock
AFRAME.registerShader('14', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
    varying vec2 vUv;
    void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
    `,
    fragmentShader: `
    uniform float time;
    varying vec2 vUv;
    void main() {
        vec2 p = vUv * 2.0 - 1.0;
        float pattern = sin(p.x * 10.0 + time * 0.1) * cos(p.y * 20.0 - time * 0.2);
        vec3 color = vec3(0.3 + 0.7 * pattern, 0.5 + 0.5 * sin(pattern * 4.0), 0.2 + 0.8 * cos(pattern * 3.0));
        gl_FragColor = vec4(color, 1.0);
    }
    `
});

// Shader 15: Diamond Nebula
AFRAME.registerShader('15', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
    varying vec2 vUv;
    void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
    `,
    fragmentShader: `
    uniform float time;
    varying vec2 vUv;
    void main() {
        vec2 p = vUv * 2.0 - 1.0;
        float diamond = abs(sin(p.x * 25.0 + time * 0.1) * cos(p.y * 25.0 - time * 0.1));
        vec3 color = vec3(0.6 + 0.4 * diamond, 0.3 + 0.7 * cos(diamond * 2.0), 0.8 + 0.2 * sin(diamond * 3.0));
        gl_FragColor = vec4(color, 1.0);
    }
    `
});
// Shader 16: celestial-vortex
AFRAME.registerShader('16', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec3 vPosition;
        void main() {
            vPosition = position;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec3 vPosition;

        void main() {
            vec3 p = normalize(vPosition);
            float angle = atan(p.y, p.x) + sin(time * 0.1) * 0.5;
            float radius = length(p);
            float waves = sin(radius * 15.0 - time * 0.2) * cos(angle * 10.0);
            vec3 color = vec3(0.3 + 0.7 * waves, 0.6 + 0.4 * cos(waves * 2.0), 0.9 + 0.1 * sin(waves * 3.0));
            gl_FragColor = vec4(color, 1.0);
        }
    `
});
// Shader 17:    starfield-hyperspace
AFRAME.registerShader('17', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec3 vPosition;
        void main() {
            vPosition = position;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec3 vPosition;

        void main() {
            vec3 p = normalize(vPosition);
            float angle = atan(p.y, p.x) + sin(time * 0.1) * 0.5;
            float radius = length(p);
            float waves = sin(radius * 15.0 - time * 0.2) * cos(angle * 10.0);
            vec3 color = vec3(0.3 + 0.7 * waves, 0.6 + 0.4 * cos(waves * 2.0), 0.9 + 0.1 * sin(waves * 3.0));
            gl_FragColor = vec4(color, 1.0);
        }
    `
});
// Shader 18:    starfield-hyperspace
AFRAME.registerShader('18', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec3 vPosition;
        void main() {
            vPosition = position;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec3 vPosition;

        void main() {
            vec3 p = normalize(vPosition);
            float noise = fract(sin(dot(p.xy, vec2(12.9898, 78.233))) * 43758.5453);
            float nebula = sin(time * 0.05 + noise * 15.0) * 0.5 + 0.5;
            vec3 color = mix(vec3(0.1, 0.0, 0.3), vec3(1.0, 0.5, 0.2), nebula);
            gl_FragColor = vec4(color, 1.0);
        }
    `
});
// Shader 19
AFRAME.registerShader('19', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec3 vPosition;
        void main() {
            vPosition = position;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec3 vPosition;

        void main() {
            vec3 p = normalize(vPosition);
            float depth = sin(p.y * 5.0 + time * 0.1) * 0.1;
            float light = smoothstep(0.3, 1.0, sin(time * 0.1 + p.y * 10.0));
            vec3 color = vec3(0.0, 0.3 + depth, 0.6 + light * 0.5);
            gl_FragColor = vec4(color, 1.0);
        }
    `
});
// Shader 20
AFRAME.registerShader('20', {
    schema: { time: { type: 'time', is: 'uniform' } },
    vertexShader: `
        varying vec3 vPosition;
        void main() {
            vPosition = position;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float time;
        varying vec3 vPosition;

        void main() {
            vec3 p = normalize(vPosition);
            float pulse = sin(time * 0.2 + p.y * 10.0) * 0.1;
            vec3 color = vec3(0.5 + pulse, 0.0, 0.0);
            gl_FragColor = vec4(color, 1.0);
        }
    `
});
