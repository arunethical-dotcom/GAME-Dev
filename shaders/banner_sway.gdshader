shader_type canvas_item;
// Gentle wind sway for hanging banners. The top edge (UV.y = 0) is pinned; the tail swings.
// Each banner gets its own phase from its world position, so a row of banners never moves in unison.
uniform float amplitude = 5.0;   // px at the tail
uniform float speed = 1.6;
uniform float pixel_size = 2.0;
varying float sway;

void vertex() {
	float phase = MODEL_MATRIX[3].x * 0.013 + MODEL_MATRIX[3].y * 0.007;
	float s = sin(TIME * speed + phase) + 0.35 * sin(TIME * speed * 2.7 + phase * 1.9);
	sway = sin(TIME * speed + phase);
	VERTEX.x += round(s * amplitude * UV.y * UV.y / pixel_size) * pixel_size;
}

void fragment() {
	vec4 c = texture(TEXTURE, UV);
	// slight shading as the cloth turns
	c.rgb *= 1.0 - 0.06 * sway * UV.y;
	COLOR = c;
}
