shader_type canvas_item;
// Animated lake / moat water.
// Two layers of the hand-painted water texture drift in different directions and are
// distorted by noise, so the surface never visibly repeats. Motion is snapped to the
// art-pixel grid so the water keeps the crisp pixel-art look instead of smearing.

uniform sampler2D water_tex : source_color, repeat_enable, filter_nearest_mipmap;
uniform sampler2D noise_tex : repeat_enable, filter_linear;
uniform float tile_size = 1024.0;          // world px covered by one texture tile
uniform float pixel_size = 4.0;            // art-pixel size in world px (motion snaps to this)
uniform vec2 flow_a = vec2(0.012, 0.005);  // tiles per second
uniform vec2 flow_b = vec2(-0.007, 0.010);
uniform float distortion = 0.015;
uniform float sparkle = 0.35;              // extra highlight where both layers' crests meet
uniform vec4 tint : source_color = vec4(1.0, 1.0, 1.0, 1.0);

varying vec2 world_pos;

void vertex() {
	world_pos = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
}

float luma(vec3 c) { return dot(c, vec3(0.299, 0.587, 0.114)); }

void fragment() {
	vec2 p = floor(world_pos / pixel_size) * pixel_size;
	vec2 uv = p / tile_size;
	float t = TIME;
	vec2 n = vec2(
		texture(noise_tex, uv * 0.35 + vec2(t * 0.010, 0.0)).r,
		texture(noise_tex, uv * 0.35 + vec2(0.43, 0.17) - vec2(0.0, t * 0.008)).r) - 0.5;
	vec3 a = texture(water_tex, uv + flow_a * t + n * distortion).rgb;
	vec3 b = texture(water_tex, uv * 0.87 + vec2(0.5, 0.31) + flow_b * t - n * distortion).rgb;
	vec3 col = mix(a, b, 0.5);
	float crest = min(luma(a), luma(b));
	col += vec3(0.75, 0.9, 1.0) * pow(crest, 3.0) * sparkle;
	COLOR = vec4(col * tint.rgb, tint.a);
}
