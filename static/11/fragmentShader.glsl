uniform float uTime;
varying vec2 vUv;

void main() {

  float blurAmount = 0.01 + sin(uTime) * 0.005;
  vec3 color = vec3(0.0);

  for (int i = -5; i <= 5; i++) {
    for (int j = -5; j <= 5; j++) {
      vec2 offset = vec2(float(i), float(j)) * blurAmount;
      color += texture2D(map, vUv + offset).rgb;
    }
  }

  color /= 121.0;
  gl_FragColor = vec4(color, 1.0);
}