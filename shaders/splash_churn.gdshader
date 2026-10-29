shader_type canvas_item;
// Churning foam: the painted splash flickers between brighter and dimmer patches that drift outward.
uniform sampler2D noise_tex : repeat_enable, filter_linear;
uniform float pixel_size = 2.0;
void fragment() {
	vec2 px = floor(UV / TEXTURE_PIXEL_SIZE / pixel_size) * pixel_size * TEXTURE_PIXEL_SIZE;
	float side = sign(px.x - 0.5);
	float n = texture(noise_tex, vec2(px.x * 4.0 - side * TIME * 0.25, px.y * 3.0 + TIME * 0.6)).r;
	vec4 c = texture(TEXTURE, UV);
	c.rgb *= 0.88 + n * 0.35;
	c.a *= step(0.22, n + c.a * 0.6);
	COLOR = c;
}
