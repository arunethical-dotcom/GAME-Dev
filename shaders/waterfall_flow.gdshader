shader_type canvas_item;
// Makes a single painted waterfall image flow: bright streaks and foam noise scroll downward
// over the painted water, and the outline ripples slightly. Only affects opaque pixels.
uniform sampler2D noise_tex : repeat_enable, filter_linear;
uniform float speed = 0.55;          // texture heights per second
uniform float streak_strength = 0.35;
uniform float wobble = 0.004;
uniform float pixel_size = 2.0;

void fragment() {
	vec2 px = floor(UV / TEXTURE_PIXEL_SIZE / pixel_size) * pixel_size * TEXTURE_PIXEL_SIZE;
	float w = (texture(noise_tex, vec2(px.y * 2.0 - TIME * speed, px.x * 3.0)).r - 0.5) * wobble;
	vec4 c = texture(TEXTURE, UV + vec2(w, 0.0));
	float n1 = texture(noise_tex, vec2(px.x * 6.0, px.y * 1.2 - TIME * speed)).r;
	float n2 = texture(noise_tex, vec2(px.x * 11.0 + 0.3, px.y * 2.5 - TIME * speed * 1.6)).r;
	float streak = smoothstep(0.58, 0.8, n1) * 0.7 + smoothstep(0.62, 0.85, n2) * 0.5;
	float dark = smoothstep(0.35, 0.2, n1) * 0.18;
	c.rgb += vec3(0.75, 0.9, 1.0) * streak * streak_strength - dark * c.rgb;
	COLOR = c;
}
