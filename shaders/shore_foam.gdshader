shader_type canvas_item;
// Foam where water meets land or stone. Applied to a Line2D that traces each shoreline and
// is drawn *under* the land, so only the water-side half shows. Waves roll toward the shore.

uniform sampler2D noise_tex : repeat_enable, filter_linear;
uniform vec4 foam_color : source_color = vec4(0.93, 0.97, 1.0, 1.0);
uniform float wave_count = 3.0;
uniform float wave_speed = 0.6;
uniform float pixel_size = 4.0;

varying vec2 world_pos;

void vertex() {
	world_pos = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
}

void fragment() {
	vec2 p = floor(world_pos / pixel_size) * pixel_size;
	float d = abs(UV.y - 0.5) * 2.0;                 // 0 at the shoreline, 1 at the outer edge
	float n = texture(noise_tex, p / 900.0).r;
	float phase = d * wave_count - TIME * wave_speed + n * 2.5;
	float fade = 1.0 - smoothstep(0.25, 1.0, d);
	float lace = texture(noise_tex, p / 120.0 + vec2(TIME * 0.015, -TIME * 0.01)).r;
	float wave = smoothstep(0.86, 0.95, fract(phase)) * fade * step(0.42, lace);
	float edge = (1.0 - smoothstep(0.08, 0.16 + n * 0.22, d)) * step(0.3, lace);  // broken foam right at the bank
	float shallow = (1.0 - smoothstep(0.1, 0.75, d)) * 0.16;    // lighter shallow-water band
	float speckle = step(0.66, lace) * fade * 0.35;
	float a = clamp(max(max(max(edge * 0.7, wave * 0.45), speckle), shallow), 0.0, 1.0);
	COLOR = vec4(foam_color.rgb, a * foam_color.a);
}
