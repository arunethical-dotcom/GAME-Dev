shader_type canvas_item;
// Animates the painted water inside a sprite: blue pixels get drifting ripples and sparkles,
// pale spray pixels shimmer. Stone and flowers are left untouched.
uniform sampler2D noise_tex : repeat_enable, filter_linear;
uniform float pixel_size = 2.0;

void fragment() {
	vec4 c = texture(TEXTURE, UV);
	vec2 px = floor(UV / TEXTURE_PIXEL_SIZE / pixel_size) * pixel_size * TEXTURE_PIXEL_SIZE;
	float water = smoothstep(0.12, 0.3, c.b - c.r) * step(0.45, c.b);
	float spray = step(0.75, c.b) * step(0.7, c.g) * step(0.6, c.r) * step(0.1, c.b - c.r);
	float n1 = texture(noise_tex, px * 3.0 + vec2(TIME * 0.05, TIME * 0.03)).r;
	float n2 = texture(noise_tex, px * 5.0 - vec2(TIME * 0.04, TIME * 0.07)).r;
	float ripple = (n1 + n2 - 1.0);
	c.rgb += water * vec3(0.35, 0.55, 0.75) * ripple * 0.35;
	c.rgb += water * vec3(0.9, 0.97, 1.0) * step(0.78, n1 * n2 * 1.6) * 0.5;
	float sh = texture(noise_tex, px * 8.0 + vec2(0.0, -TIME * 0.35)).r;
	c.rgb += spray * (sh - 0.45) * 0.45;
	COLOR = c;
}
