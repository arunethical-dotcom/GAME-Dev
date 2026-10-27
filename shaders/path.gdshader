shader_type canvas_item;
// Dirt path drawn as a Line2D. Texture is sampled in world space (no stretching on curves);
// the edges fade out with noise so the path blends into the grass instead of having a hard border.
uniform sampler2D albedo : source_color, repeat_enable, filter_nearest_mipmap;
uniform sampler2D noise_tex : repeat_enable, filter_linear;
uniform float tile_size = 1024.0;
uniform float pixel_size = 4.0;
uniform vec4 tint : source_color = vec4(1.0);
varying vec2 world_pos;
void vertex() { world_pos = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy; }
void fragment() {
	vec2 p = floor(world_pos / pixel_size) * pixel_size;
	vec3 col = texture(albedo, p / tile_size).rgb * tint.rgb;
	float d = abs(UV.y - 0.5) * 2.0;
	float n = texture(noise_tex, p / 420.0).r;
	float edge = 1.0 - step(0.62 + n * 0.45, d);
	float rim = step(0.5 + n * 0.45, d) * edge;           // darker trodden rim
	col *= 1.0 - rim * 0.18;
	COLOR = vec4(col, edge);
}
