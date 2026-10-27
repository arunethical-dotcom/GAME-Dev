shader_type canvas_item;
// Lit windows: pixels marked in the glow mask brighten as night falls. Output goes above 1.0,
// so with HDR 2D + glow enabled they bloom softly; with CanvasModulate dimming the world at
// night, the windows stay bright and warm.
global uniform float night;
uniform sampler2D glow_mask : filter_linear;
uniform float strength = 1.8;
uniform vec3 glow_tint : source_color = vec3(1.0, 0.82, 0.5);

void fragment() {
	vec4 base = texture(TEXTURE, UV);
	float m = texture(glow_mask, UV).r;
	float flicker = 0.92 + 0.08 * sin(TIME * 2.3 + UV.x * 40.0 + UV.y * 23.0);
	vec3 add = mix(base.rgb, glow_tint, 0.35) * m * strength * (0.25 + night) * flicker;
	COLOR = vec4(base.rgb + add, base.a);
}
