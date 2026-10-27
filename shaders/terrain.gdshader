shader_type canvas_item;
// Ground texture (grass, dirt, stone) mapped in world space so neighbouring shapes line up
// seamlessly. Large-scale noise varies brightness and blends in a second offset sample so
// the 1024 px tile never reads as a repeating grid when the camera zooms out.

uniform sampler2D albedo : source_color, repeat_enable, filter_nearest_mipmap;
uniform sampler2D noise_tex : repeat_enable, filter_linear;
uniform float tile_size = 1024.0;
uniform float macro_scale = 5000.0;        // world px per noise tile
uniform float brightness_variation = 0.08; // +/- brightness from macro noise
uniform float break_repetition = 1.0;      // 0 = off (use for geometric textures like flagstone)
uniform vec4 tint : source_color = vec4(1.0);
// Optional grime/moss layer, multiplied in patches. Breaks up repetition on geometric
// textures (flagstone) without ghosting the stone shapes.
uniform sampler2D grime_tex : source_color, repeat_enable, filter_nearest_mipmap;
uniform float grime_amount = 0.0;
uniform float grime_tile = 900.0;
uniform vec3 warm_cool = vec3(0.0);       // large-scale colour drift (r,g,b) amplitude

varying vec2 world_pos;

void vertex() {
	world_pos = (MODEL_MATRIX * vec4(VERTEX, 0.0, 1.0)).xy;
}

void fragment() {
	vec2 uv = world_pos / tile_size;
	vec3 col = texture(albedo, uv).rgb;
	if (break_repetition > 0.0) {
		vec3 alt = texture(albedo, uv + vec2(0.371, 0.613)).rgb;
		float m = texture(noise_tex, world_pos / (macro_scale * 0.7) + vec2(0.5)).r;
		m = smoothstep(0.42, 0.58, m) * break_repetition;
		col = mix(col, alt, m);
	}
	float n = texture(noise_tex, world_pos / macro_scale).r;
	col *= 1.0 + (n - 0.5) * 2.0 * brightness_variation;
	if (grime_amount > 0.0) {
		vec3 g = texture(grime_tex, world_pos / grime_tile).rgb;
		float gm = smoothstep(0.45, 0.75, texture(noise_tex, world_pos / 2600.0 + vec2(0.2, 0.7)).r);
		col = mix(col, col * (g * 1.6), gm * grime_amount);
	}
	float c = texture(noise_tex, world_pos / (macro_scale * 1.7) + vec2(0.61, 0.13)).r - 0.5;
	col += warm_cool * c;
	COLOR = vec4(col * tint.rgb, 1.0);
}
