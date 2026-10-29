"""
Block castle builder v2: multi-colour 4x4 blocks from a shape dictionary.

  python3 block_castle/build2.py --colours 4 --shapes 4096 --palette 1024 --detail 0.03

Each 4x4 plan-px cell = one block:
  shape  : one of K block shapes (each pixel of the block takes colour slot 0..n-1); the shape set is
           learned from the castle's own cells (most common layouts), so the blocks fit its details
  colours: n palette colours (palette fitted to the castle, k-means in Lab)
  surface: my material texture (stone courses, roof slates, water ripples, grass, wood, cloth, paving, glow)
Godot data: bm1.png (RGBA = colour slots, low 8 bits), bm2.png (R = high bits of the 4 slots, G/B = shape id,
A = material), palette.png (P x 1), shapes.png (4 x 4K, value = slot * 85), materials.png.
"""
import argparse, json, os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from blocks3 import cells, per_cell_kmeans, build_dictionary, assign, palette, PLAN
from build import material_tiles, MATS, classify
from skimage.color import rgb2lab, lab2rgb

OUT = os.path.join(HERE, 'godot')

SHADER = r'''shader_type canvas_item;
// Block castle (v2): each 4x4 plan-px cell is one of my pixel blocks:
// a shape from the block-shape set, up to 4 palette colours, and a material surface texture.
uniform sampler2D bm1 : filter_nearest;           // RGBA = colour slots 0..3 (low 8 bits)
uniform sampler2D bm2 : filter_nearest;           // R = high bits (2 per slot), G/B = shape id, A = material
uniform sampler2D palette : source_color, filter_nearest;
uniform sampler2D shapes : filter_nearest;        // 4 x (4 * K), value = slot * 85
uniform sampler2D materials : filter_nearest;     // 20 x (20 * M), 0.5 = neutral
uniform vec2 plan_size = vec2(1536.0, 1024.0);
uniform float detail = 0.03;

int b8(float v) { return int(v * 255.0 + 0.5); }

void fragment() {
	vec2 px = floor(UV * plan_size * 5.0) / 5.0;
	ivec2 c = ivec2(floor(px / 4.0));
	vec4 a = texelFetch(bm1, c, 0);
	vec4 b = texelFetch(bm2, c, 0);
	int hi = b8(b.r);
	int shape = b8(b.g) + 256 * b8(b.b);
	int mat = b8(b.a);
	ivec2 sub = ivec2(floor(mod(px, 4.0)));
	int slot = int(texelFetch(shapes, ivec2(shape * 4 + sub.x, sub.y), 0).r * 3.0 + 0.5);
	int lo = slot == 0 ? b8(a.r) : (slot == 1 ? b8(a.g) : (slot == 2 ? b8(a.b) : b8(a.a)));
	int idx = lo + 256 * ((hi >> (slot * 2)) & 3);
	vec3 col = texelFetch(palette, ivec2(idx, 0), 0).rgb;
	ivec2 d = ivec2(floor(mod(px * 5.0, 20.0)));
	float t = texelFetch(materials, ivec2(mat * 20 + d.x, d.y), 0).r;
	col *= 1.0 + (t * 2.0 - 1.0) * detail / 0.1;
	COLOR = vec4(col, 1.0);
}
'''

def main(nc, K, P, detail):
    img = np.asarray(Image.open(PLAN).convert('RGB'), float) / 255; lab = rgb2lab(img)
    L, gh, gw = cells(lab, 4)
    idx = per_cell_kmeans(L, nc)
    pal = palette(lab, P)
    D, _ = build_dictionary(idx, K, nc)
    s, cols = assign(L, idx, D, pal, n=nc)
    # material per cell
    rgbm = img[:gh * 4, :gw * 4].reshape(gh, 4, gw, 4, 3).mean((1, 3)); mat = classify(rgbm).reshape(-1)
    # pack
    c4 = np.zeros((len(s), 4), int); c4[:, :nc] = cols
    bm1 = (c4 & 255).astype(np.uint8).reshape(gh, gw, 4)
    hi = sum(((c4[:, k] >> 8) & 3) << (2 * k) for k in range(4))
    bm2 = np.stack([hi, s & 255, s >> 8, mat], 1).astype(np.uint8).reshape(gh, gw, 4)
    Image.fromarray(bm1, 'RGBA').save(os.path.join(OUT, 'bm1.png'))
    Image.fromarray(bm2, 'RGBA').save(os.path.join(OUT, 'bm2.png'))
    pal_rgb = np.clip(lab2rgb(pal[None])[0], 0, 1)
    Image.fromarray((pal_rgb[None] * 255 + 0.5).astype(np.uint8), 'RGB').save(os.path.join(OUT, 'palette.png'))
    sh = np.zeros((4, 4 * len(D)), np.uint8)
    for i, m in enumerate(D): sh[:, i * 4:(i + 1) * 4] = (m.reshape(4, 4) * 85).astype(np.uint8)
    Image.fromarray(sh, 'L').save(os.path.join(OUT, 'shapes.png'))
    T = material_tiles(20); at = np.zeros((20, 20 * len(MATS)), np.uint8)
    for i, k in enumerate(MATS): at[:, i * 20:(i + 1) * 20] = np.clip(T[k] * 255, 0, 255).astype(np.uint8)
    Image.fromarray(at, 'L').save(os.path.join(OUT, 'materials.png'))
    # python preview with identical maths (palette rounded to 8 bit, like the texture)
    p8 = (pal_rgb * 255 + 0.5).astype(np.uint8).astype(float) / 255
    slot = D[s]                                                # (n,16)
    colx = np.take_along_axis(c4, slot, 1)                     # palette idx per pixel
    rec = p8[colx].reshape(gh, gw, 4, 4, 3).transpose(0, 2, 1, 3, 4).reshape(gh * 4, gw * 4, 3)
    yy, xx = np.mgrid[0:gh * 4, 0:gw * 4]
    t = at[(yy * 5) % 20, mat.reshape(gh, gw)[yy // 4, xx // 4] * 20 + (xx * 5) % 20].astype(float) / 255
    rec = np.clip(rec * (1 + (t * 2 - 1) * detail / 0.1)[..., None], 0, 1)
    Image.fromarray((rec * 255 + 0.5).astype(np.uint8)).save(os.path.join(OUT, 'preview.png'))
    # godot files
    open(os.path.join(OUT, 'block_castle.gdshader'), 'w').write(SHADER)
    for f in ('bm1', 'bm2', 'palette', 'shapes', 'materials'):
        open(os.path.join(OUT, f + '.png.import'), 'w').write(f'[remap]\n\nimporter="texture"\ntype="CompressedTexture2D"\n\n[deps]\n\nsource_file="res://block_castle/godot/{f}.png"\n\n[params]\n\ncompress/mode=0\nmipmaps/generate=false\nprocess/fix_alpha_border=false\nprocess/premult_alpha=false\ndetect_3d/compress_to=0\n')
    for old in ('blockmap.png', 'matmap.png', 'blockmap.png.import', 'matmap.png.import'):
        try: os.remove(os.path.join(OUT, old))
        except FileNotFoundError: pass
    Pp = 'res://block_castle/godot/'
    open(os.path.join(OUT, 'BlockCastle.tscn'), 'w').write(f'''[gd_scene load_steps=8 format=3]

[ext_resource type="Shader" path="{Pp}block_castle.gdshader" id="sh"]
[ext_resource type="Texture2D" path="{Pp}bm1.png" id="bm1"]
[ext_resource type="Texture2D" path="{Pp}bm2.png" id="bm2"]
[ext_resource type="Texture2D" path="{Pp}palette.png" id="pal"]
[ext_resource type="Texture2D" path="{Pp}shapes.png" id="shp"]
[ext_resource type="Texture2D" path="{Pp}materials.png" id="mat"]

[sub_resource type="ShaderMaterial" id="m"]
shader = ExtResource("sh")
shader_parameter/bm1 = ExtResource("bm1")
shader_parameter/bm2 = ExtResource("bm2")
shader_parameter/palette = ExtResource("pal")
shader_parameter/shapes = ExtResource("shp")
shader_parameter/materials = ExtResource("mat")
shader_parameter/plan_size = Vector2({gw * 4}, {gh * 4})
shader_parameter/detail = {detail}

[node name="BlockCastle" type="Sprite2D"]
texture_filter = 1
material = SubResource("m")
texture = ExtResource("bm1")
centered = false
scale = Vector2(40, 40)
''')
    info = dict(version=2, cell=4, colours_per_block=nc, block_shapes=len(D), palette=P, detail=detail, grid=[gw, gh])
    json.dump(info, open(os.path.join(OUT, 'build_info.json'), 'w'), indent=1); print(json.dumps(info))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--colours', type=int, default=4); ap.add_argument('--shapes', type=int, default=4096)
    ap.add_argument('--palette', type=int, default=1024); ap.add_argument('--detail', type=float, default=0.03)
    a = ap.parse_args(); main(a.colours, a.shapes, a.palette, a.detail)
