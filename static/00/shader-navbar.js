const initHeaderShader = () => {
    const canvas = document.getElementById('shader-canvas');
    if (!canvas) return;

    // Limpiar canvas primero
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({
        canvas,
        antialias: true,
        alpha: false,
        powerPreference: "high-performance",
        preserveDrawingBuffer: true
    });

    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    renderer.setClearColor(0x000000, 0);
    renderer.autoClear = false;

    // Guardar referencias para ajustes posteriores
    canvas.__threeRenderer = renderer;

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

    const material = new THREE.ShaderMaterial({
        vertexShader,
        fragmentShader,
        uniforms: {
            iTime: { value: 0 },
            iResolution: { value: new THREE.Vector2(canvas.clientWidth, canvas.clientHeight) },
        },
        transparent: false
    });

    // Guardar referencia al material
    canvas.__threeMaterial = material;

    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);
    camera.position.z = 1;

    const animate = (time) => {
        requestAnimationFrame(animate);

        // Limpieza manual controlada
        renderer.clearColor();
        renderer.clearDepth();

        material.uniforms.iTime.value = time * 0.001;
        renderer.render(scene, camera);
    };

    const onResize = () => {
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;

        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();

        if (material.uniforms.iResolution) {
            material.uniforms.iResolution.value.set(width, height);
        }
    };

    // Usar ResizeObserver para mejores resultados
    const resizeObserver = new ResizeObserver(entries => {
        for (let entry of entries) {
            if (entry.contentBoxSize) {
                onResize();
            }
        }
    });

    resizeObserver.observe(canvas);
    animate(0);
};

const initNavbarShader = () => {
    const canvas = document.getElementById('navbar-shader');
    if (!canvas) return;

    // Limpiar canvas primero
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({
        canvas,
        antialias: true,
        alpha: true,
        powerPreference: "high-performance"
    });

    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    renderer.setClearColor(0x000000, 0);

    const geometry = new THREE.PlaneGeometry(2, 2);

    const fragmentShader = `
    uniform float iTime;
    uniform vec2 iResolution;

    void mainImage(out vec4 fragColor, in vec2 fragCoord) {
        vec2 uv = fragCoord.xy / iResolution.xy;
        float speed = iTime * 0.5;

        // Efecto de ondas simples
        float wave1 = sin(uv.x * 20.0 + speed) * 0.1;
        float wave2 = cos(uv.y * 15.0 + speed * 1.3) * 0.1;

        vec3 color = vec3(
            0.1 + 0.1 * sin(speed + uv.x * 5.0),
                          0.1 + 0.1 * cos(speed + uv.y * 3.0),
                          0.3 + 0.1 * sin(speed * 0.7 + uv.x * 7.0 + uv.y * 4.0)
        );

        // Añadir líneas de grid sutiles
        float grid = max(
            smoothstep(0.01, 0.0, abs(fract(uv.x * 10.0) - 0.5)),
                         smoothstep(0.01, 0.0, abs(fract(uv.y * 5.0) - 0.5))
        ) * 0.2;

        fragColor = vec4(color + grid, 0.7);
    }

    void main() {
        mainImage(gl_FragColor, gl_FragCoord.xy);
    }
    `;

    const material = new THREE.ShaderMaterial({
        uniforms: {
            iTime: { value: 0 },
            iResolution: { value: new THREE.Vector2() }
        },
        fragmentShader,
        vertexShader: `
        void main() {
            gl_Position = vec4(position, 1.0);
        }
        `,
        transparent: true
    });

    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);
    camera.position.z = 1;

    const animate = (time) => {
        requestAnimationFrame(animate);
        material.uniforms.iTime.value = time * 0.001;
        renderer.render(scene, camera);
    };

    const onResize = () => {
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        material.uniforms.iResolution.value.set(width, height);
    };

    window.addEventListener('resize', onResize);
    onResize();
    animate(0);
};

// Inicialización controlada
let shadersInitialized = false;

function initShaders() {
    if (shadersInitialized) return;

    initHeaderShader();
    initNavbarShader();
    shadersInitialized = true;
}

document.addEventListener('DOMContentLoaded', () => {
    // Limpieza inicial
    const cleanCanvas = (canvas) => {
        if (!canvas) return;
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        if (gl) {
            gl.clearColor(0, 0, 0, 1);
            gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
        }
    };

    cleanCanvas(document.getElementById('shader-canvas'));
    cleanCanvas(document.getElementById('navbar-shader'));

    // Inicializar shaders después de un breve retraso
    setTimeout(initShaders, 100);
});
