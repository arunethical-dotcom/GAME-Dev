"""
Block castle builder: rebuilds the castle plan out of my own pixel blocks.

  python3 block_castle/build.py [--cell 4] [--palette 128] [--detail 0.06] [--shapes basic|extended]

Every cell of the plan (cell x cell plan px) becomes one block:
  * a block SHAPE from a fixed vocabulary (solid, halves, quarters, diagonal steps, stripes ...)
  * two COLOURS from a palette fitted to the castle (k-means in Lab)
  * a MATERIAL surface texture I draw (stone courses, roof slates, water ripples, grass, wood, cloth, glow)
The shape/colours per cell are chosen to match the plan as closely as possible (least squares in Lab).

Outputs (block_castle/godot/): blockmap.png (R=colour A, G=colour B, B=shape), matmap.png (material),
palette.png, shapes.png, materials.png, block_castle.gdshader, BlockCastle.tscn, build_info.json
"""
import argparse, json, os
import numpy as np
from PIL import Image
from skimage.color import rgb2lab, lab2rgb
from scipy.cluster.vq import kmeans2

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'godot'); os.makedirs(OUT, exist_ok=True)
PLAN = os.path.join(ROOT, 'docs/reference/castle_reference.png')

def shape_vocab(c, extended):
    """Binary masks c x c (1 = colour B). Colour swapping covers every inverse."""
    S = [np.zeros((c, c), np.uint8)]                                   # solid
    yy, xx = np.mgrid[0:c, 0:c]
    for k in range(1, c): S.append((yy >= k).astype(np.uint8))         # horizontal splits
    for k in range(1, c): S.append((xx >= k).astype(np.uint8))         # vertical splits
    for k in range(-(c - 1), c): S.append((xx - yy >= k).astype(np.uint8))   # diagonal steps \
    for k in range(1, 2 * c - 1): S.append((xx + yy >= k).astype(np.uint8))  # diagonal steps /
    h = c // 2
    for (y0, x0) in ((0, 0), (0, h), (h, 0), (h, h)):                  # quarters
        m = np.zeros((c, c), np.uint8); m[y0:y0 + h, x0:x0 + h] = 1; S.append(m)
    m = np.zeros((c, c), np.uint8); m[c // 4:c - c // 4, c // 4:c - c // 4] = 1; S.append(m)   # centre
    S.append((yy % 2).astype(np.uint8)); S.append((xx % 2).astype(np.uint8)); S.append(((xx + yy) % 2).astype(np.uint8))
    if extended:   # thin lines and single-pixel features: outlines, windows, mortar, slits
        for k in range(c):
            m = np.zeros((c, c), np.uint8); m[k, :] = 1; S.append(m)
            m = np.zeros((c, c), np.uint8); m[:, k] = 1; S.append(m)
        for y in range(c):
            for x in range(c):
                m = np.zeros((c, c), np.uint8); m[y, x] = 1; S.append(m)
        for y in range(c - 1):
            for x in range(c - 1):
                m = np.zeros((c, c), np.uint8); m[y:y + 2, x:x + 2] = 1; S.append(m)
        for k in range(c):
            for j in range(k + 1, c):
                m = np.zeros((c, c), np.uint8); m[:, k:j + 1] = 1; S.append(m)
                m = np.zeros((c, c), np.uint8); m[k:j + 1, :] = 1; S.append(m)
    uniq = []
    for m in S:
        if not any((m == u).all() or (m == 1 - u).all() for u in uniq): uniq.append(m)
    return np.array(uniq)

# ---------------------------------------------------------------- my material blocks (20 x 20 art px each)
def material_tiles(n=20):
    rng = np.random.default_rng(5)
    T = {}
    yy, xx = np.mgrid[0:n, 0:n]
    stone = np.full((n, n), 0.5)                                       # ashlar courses: 2 courses of 10, offset joints
    stone[(yy % 10) == 9] -= 0.10; stone[((yy // 10) % 2 == 0) & (xx == 4)] -= 0.08; stone[((yy // 10) % 2 == 1) & (xx == 14)] -= 0.08
    stone[(yy % 10) == 0] += 0.05; T['stone'] = stone
    roof = np.full((n, n), 0.5)                                        # slates: rows of rounded tiles
    for r in range(0, n, 5):
        for x in range(n):
            off = 0 if (r // 5) % 2 == 0 else 3
            if (x + off) % 6 == 0: roof[r:r + 4, x] -= 0.06
        roof[r + 4 if r + 4 < n else n - 1, :] -= 0.08; roof[r, :] += 0.04
    T['roof'] = roof
    water = np.full((n, n), 0.5)                                       # ripple dashes
    for (y, x0, L) in ((3, 2, 5), (8, 11, 6), (13, 4, 4), (17, 13, 5)):
        water[y, x0:x0 + L] += 0.08
    T['water'] = water
    grass = np.full((n, n), 0.5) + rng.normal(0, 0.025, (n, n))        # blade ticks
    for _ in range(14):
        y, x = rng.integers(2, n), rng.integers(0, n); grass[y - 2:y, x] += 0.07
    T['grass'] = grass
    wood = np.full((n, n), 0.5); wood[:, ::5] -= 0.08; wood[(yy * 7 + xx * 3) % 23 == 0] -= 0.05; T['wood'] = wood
    cloth = np.full((n, n), 0.5) + 0.04 * np.sin(xx / n * 2 * np.pi * 2); T['cloth'] = cloth
    paving = np.full((n, n), 0.5); paving[(yy % 10) == 9] -= 0.07; paving[(xx % 10) == 9] -= 0.07; T['paving'] = paving
    T['glow'] = np.full((n, n), 0.5)
    return T
MATS = ['stone', 'roof', 'water', 'grass', 'wood', 'cloth', 'paving', 'glow']

def classify(rgb_mean):
    """Material per cell from its mean colour (0..1)."""
    r, g, b = rgb_mean[..., 0], rgb_mean[..., 1], rgb_mean[..., 2]
    mx = rgb_mean.max(-1); mn = rgb_mean.min(-1); s = (mx - mn) / np.maximum(mx, 1e-6); v = mx
    m = np.zeros(r.shape, np.uint8)                                    # stone
    m[(b > r + 0.08) & (g > r) & (s > 0.35)] = 2                        # water (cyan-blue)
    m[(b > r + 0.06) & (g <= r + 0.12) & (s > 0.3) & (m == 0)] = 1      # roof (navy blue)
    m[(g > r + 0.03) & (g > b) & (s > 0.2)] = 3                         # grass / trees
    m[(r > g + 0.12) & (r > b + 0.12) & (v > 0.35) & (s > 0.45)] = 5    # banners
    m[(r > b + 0.12) & (g > b + 0.05) & (s > 0.35) & (s <= 0.6) & (v < 0.75)] = 4   # wood / dirt
    m[(v > 0.8) & (r > b + 0.2) & (s > 0.4)] = 7                        # glow / fire
    m[(m == 0) & (v > 0.62) & (s < 0.22)] = 6                           # light paving
    return m

def build(cell, palette_n, detail, shapes_kind):
    img = np.asarray(Image.open(PLAN).convert('RGB'), float) / 255
    H, W, _ = img.shape; gh, gw = H // cell, W // cell
    lab = rgb2lab(img)
    # palette: k-means in Lab on a sample of plan pixels
    rng = np.random.default_rng(0)
    sample = lab.reshape(-1, 3)[rng.choice(H * W, 120000, replace=False)]
    cent, _ = kmeans2(sample, palette_n, minit='++', seed=1, iter=25)
    # cells as (gh, gw, c*c, 3)
    L = lab[:gh * cell, :gw * cell].reshape(gh, cell, gw, cell, 3).transpose(0, 2, 1, 3, 4).reshape(gh, gw, cell * cell, 3)
    S = shape_vocab(cell, shapes_kind == 'extended').reshape(-1, cell * cell).astype(bool)
    def nearest(c):   # palette index for Lab colours (...,3)
        d = ((c[..., None, :] - cent[None, None, :, :]) ** 2).sum(-1) if c.ndim == 3 else ((c[:, None, :] - cent[None, :, :]) ** 2).sum(-1)
        return d.argmin(-1)
    best_err = np.full((gh, gw), np.inf); bA = np.zeros((gh, gw), int); bB = np.zeros((gh, gw), int); bS = np.zeros((gh, gw), int)
    for si, m in enumerate(S):
        nb = m.sum(); na = m.size - nb
        mA = L[:, :, ~m].mean(2) if na else np.zeros((gh, gw, 3))
        mB = L[:, :, m].mean(2) if nb else mA
        iA = nearest(mA.reshape(-1, 3)).reshape(gh, gw); iB = nearest(mB.reshape(-1, 3)).reshape(gh, gw)
        cA = cent[iA]; cB = cent[iB]
        rec = np.where(m[None, None, :, None], cB[:, :, None, :], cA[:, :, None, :])
        err = ((L - rec) ** 2).sum(-1).mean(-1)
        better = err < best_err
        best_err[better] = err[better]; bA[better] = iA[better]; bB[better] = iB[better]; bS[better] = si
    # material per cell from the plan's mean colour
    rgbm = img[:gh * cell, :gw * cell].reshape(gh, cell, gw, cell, 3).mean((1, 3))
    mat = classify(rgbm)
    # ---- write Godot data
    pal_rgb = np.clip(lab2rgb(cent[None, :, :])[0], 0, 1)
    pal = np.zeros((1, 256, 3), np.uint8); pal[0, :palette_n] = (pal_rgb * 255 + 0.5).astype(np.uint8)
    Image.fromarray(pal).save(os.path.join(OUT, 'palette.png'))
    bm = np.dstack([bA, bB, bS]).astype(np.uint8); Image.fromarray(bm, 'RGB').save(os.path.join(OUT, 'blockmap.png'))
    Image.fromarray(mat.astype(np.uint8), 'L').save(os.path.join(OUT, 'matmap.png'))
    nS = len(S); sh = np.zeros((cell, nS * cell), np.uint8)
    for i, m in enumerate(S): sh[:, i * cell:(i + 1) * cell] = m.reshape(cell, cell) * 255
    Image.fromarray(sh, 'L').save(os.path.join(OUT, 'shapes.png'))
    T = material_tiles(20); at = np.zeros((20, 20 * len(MATS)), np.uint8)
    for i, k in enumerate(MATS): at[:, i * 20:(i + 1) * 20] = np.clip(T[k] * 255, 0, 255).astype(np.uint8)
    Image.fromarray(at, 'L').save(os.path.join(OUT, 'materials.png'))
    # preview reconstruction in Python (same maths as the shader) for quick checks
    pal_f = pal[0].astype(float) / 255
    rec = np.zeros((gh * cell, gw * cell, 3))
    sub = S.reshape(nS, cell, cell)
    yy, xx = np.mgrid[0:gh * cell, 0:gw * cell]
    cy, cx = yy // cell, xx // cell; m = sub[bS[cy, cx], yy % cell, xx % cell]
    col = np.where(m[..., None], pal_f[bB[cy, cx]], pal_f[bA[cy, cx]])
    dpx = (xx * 20 // cell) % 20; dpy = (yy * 20 // cell) % 20
    d = at[dpy, mat[cy, cx] * 20 + dpx].astype(float) / 255
    col = np.clip(col * (1 + (d * 2 - 1) * detail / 0.1)[..., None], 0, 1)
    Image.fromarray((col * 255 + 0.5).astype(np.uint8)).save(os.path.join(OUT, 'preview.png'))
    info = dict(cell=cell, grid=[gw, gh], palette=palette_n, shapes=nS, detail=detail, shapes_kind=shapes_kind,
                world_size=[gw * cell * 10, gh * cell * 10])
    json.dump(info, open(os.path.join(OUT, 'build_info.json'), 'w'), indent=1)
    return info

SHADER = r'''shader_type canvas_item;
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
'''

def write_godot(info):
    open(os.path.join(OUT, 'block_castle.gdshader'), 'w').write(SHADER)
    gw, gh = info['grid']; cell = info['cell']
    for f in ('blockmap', 'matmap', 'palette', 'shapes', 'materials'):
        open(os.path.join(OUT, f + '.png.import'), 'w').write(f'''[remap]

importer="texture"
type="CompressedTexture2D"

[deps]

source_file="res://block_castle/godot/{f}.png"

[params]

compress/mode=0
mipmaps/generate=false
process/fix_alpha_border=false
process/premult_alpha=false
detect_3d/compress_to=0
''')
    P = 'res://block_castle/godot/'
    open(os.path.join(OUT, 'BlockCastle.tscn'), 'w').write(f'''[gd_scene load_steps=8 format=3]

[ext_resource type="Shader" path="{P}block_castle.gdshader" id="sh"]
[ext_resource type="Texture2D" path="{P}blockmap.png" id="bm"]
[ext_resource type="Texture2D" path="{P}matmap.png" id="mm"]
[ext_resource type="Texture2D" path="{P}palette.png" id="pal"]
[ext_resource type="Texture2D" path="{P}shapes.png" id="shp"]
[ext_resource type="Texture2D" path="{P}materials.png" id="mat"]

[sub_resource type="ShaderMaterial" id="m"]
shader = ExtResource("sh")
shader_parameter/blockmap = ExtResource("bm")
shader_parameter/matmap = ExtResource("mm")
shader_parameter/palette = ExtResource("pal")
shader_parameter/shapes = ExtResource("shp")
shader_parameter/materials = ExtResource("mat")
shader_parameter/cell = {cell}
shader_parameter/plan_size = Vector2({gw * cell}, {gh * cell})
shader_parameter/detail = {info["detail"]}

[node name="BlockCastle" type="Sprite2D"]
texture_filter = 1
material = SubResource("m")
texture = ExtResource("bm")
centered = false
scale = Vector2({cell * 10}, {cell * 10})
''')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--cell', type=int, default=4); ap.add_argument('--palette', type=int, default=128)
    ap.add_argument('--detail', type=float, default=0.06); ap.add_argument('--shapes', default='basic')
    a = ap.parse_args()
    info = build(a.cell, a.palette, a.detail, a.shapes); write_godot(info); print(json.dumps(info))
