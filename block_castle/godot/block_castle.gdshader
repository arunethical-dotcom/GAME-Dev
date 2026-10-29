shader_type canvas_item;
// Block castle renderer: every cell is one of my pixel blocks
// (shape from the shape vocabulary, two palette colours, material surface texture).
uniform sampler2D blockmap : filter_nearest;      // R = colour A, G = colour B, B = shape id
uniform sampler2D matmap : filter_nearest;        // material id
uniform sampler2D palette : source_color, filter_nearest;
uniform sampler2D shapes : filter_nearest;        // CELL x (CELL * n_shapes), white = colour B
uniform sampler2D materials : filter_nearest;     // 20 x (20 * n_materials), 0.5 = neutral
uniform int cell = 4;
uniform vec2 plan_size = vec2(1536.0, 1024.0);
uniform float detail = 0.06;

void fragment() {
	vec2 px = floor(UV * plan_size * 5.0) / 5.0;          // plan px, snapped to my 20-px block art grid
	ivec2 c = ivec2(floor(px / float(cell)));
	vec3 bm = texelFetch(blockmap, c, 0).rgb;
	int ia = int(bm.r * 255.0 + 0.5); int ib = int(bm.g * 255.0 + 0.5); int is = int(bm.b * 255.0 + 0.5);
	int mat = int(texelFetch(matmap, c, 0).r * 255.0 + 0.5);
	ivec2 sub = ivec2(floor(mod(px, float(cell))));
	float m = texelFetch(shapes, ivec2(is * cell + sub.x, sub.y), 0).r;
	vec3 col = texelFetch(palette, ivec2(m > 0.5 ? ib : ia, 0), 0).rgb;
	ivec2 d = ivec2(floor(mod(px * 20.0 / float(cell), 20.0)));
	float t = texelFetch(materials, ivec2(mat * 20 + d.x, d.y), 0).r;
	col *= 1.0 + (t * 2.0 - 1.0) * detail / 0.1;
	COLOR = vec4(col, 1.0);
}
