"""
Builds scenes/castle/Castle.tscn from blueprint/castle_blueprint.py.

Run:  python3 scripts/tools/gen_castle.py

The castle is drawn in true 3/4 (oblique) view from the blueprint's terraces and walls:
  * every terrace edge that faces the camera gets a stone face hanging down to the level below,
    with bricks continuous around corners, shaded by facing direction and darkened toward the base
  * curtain-type faces get a corbel (machicolation) band under the parapet
  * every edge gets a crenellated parapet (merlons), except edges listed as open
  * a walkway band runs inside each parapet
  * free-standing walls (barbican, links) and bridges are thin terraces built the same way
Towers, the gatehouse, palace and other set pieces are placed as Y-sorted sprites on top.
No trees, houses or market props: the castle only (design those later).
"""
import math, os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, 'blueprint'))
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union
import castle_blueprint as BP
import layout as LY                     # outer land, water extents, cliffs

K = 10                                   # reference px -> world px
MERLON_H = 68.0                          # world px (texture height)
CORBEL_H = 65.0
WALKWAY_W = 130.0
FACE_TEX_H = 240.0                       # stone_face.png height (one full repeat)

# ------------------------------------------------------------------ helpers
def full_poly(top):
    """Mirror a west-half outline about the axis and join it into one closed polygon."""
    xs = [p[0] for p in top]
    if max(xs) < BP.AXIS - 1:            # entirely west of the axis: return as is
        return [list(top)]
    # outline touches the axis: build west half + mirrored east half
    west = list(top)
    east = [BP.mirror_pt(p) for p in reversed(top)]
    pts = west + [p for p in east if not any(abs(p[0]-q[0]) < 0.5 and abs(p[1]-q[1]) < 0.5 for q in west)]
    return [pts]

def both_sides(poly):
    if max(p[0] for p in poly) >= BP.AXIS - 1:
        return full_poly(poly)
    return [list(poly), [BP.mirror_pt(p) for p in reversed(poly)]]

def ccw(poly):
    a = sum(x0*y1 - x1*y0 for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]))
    return poly if a < 0 else poly[::-1]     # screen y down: negative area == clockwise on screen

def outward_normals(poly):
    """Outward unit normals for each edge (poly in screen coords, y down)."""
    P = Polygon(poly); out = []
    for i in range(len(poly)):
        (x0, y0), (x1, y1) = poly[i], poly[(i+1) % len(poly)]
        dx, dy = x1-x0, y1-y0; L = math.hypot(dx, dy) or 1
        nx, ny = dy/L, -dx/L
        mx, my = (x0+x1)/2, (y0+y1)/2
        if P.contains(Polygon([(mx+nx*0.5, my+ny*0.5), (mx+nx*0.6, my+ny*0.5), (mx+nx*0.5, my+ny*0.6)]).centroid):
            nx, ny = -nx, -ny
        out.append((nx, ny))
    return out

def W(p): return (p[0]*K, p[1]*K)
def fmt(pts): return 'PackedVector2Array(' + ', '.join(f'{x:.1f}, {y:.1f}' for x, y in pts) + ')'
def fcol(c): return f'Color({c[0]:.3f}, {c[1]:.3f}, {c[2]:.3f}, {c[3] if len(c) > 3 else 1:.3f})'

# ------------------------------------------------------------------ scene assembly
ext, sub, nodes = [], [], []
def E(kind, path):
    for k, p, i in ext:
        if p == path: return i
    i = f'e{len(ext)+1}'; ext.append((kind, path, i)); return i
def S(text): sub.append(text)
def N(text): nodes.append(text)

S('[sub_resource type="FastNoiseLite" id="noise"]\nnoise_type = 3\nfrequency = 0.012\nfractal_octaves = 4')
S('[sub_resource type="NoiseTexture2D" id="noise_tex"]\nwidth = 512\nheight = 512\nseamless = true\nnoise = SubResource("noise")')
def MAT(id, shader, params):
    s = f'[sub_resource type="ShaderMaterial" id="{id}"]\nshader = ExtResource("{E("Shader", shader)}")'
    for k, v in params.items(): s += f'\nshader_parameter/{k} = {v}'
    S(s)
NT = 'SubResource("noise_tex")'
T = lambda p: f'ExtResource("{E("Texture2D", p)}")'
MAT('m_water', 'res://shaders/water.gdshader', {'water_tex': T('res://assets/tilesets/water/deep_water.png'), 'noise_tex': NT, 'tile_size': '1024.0', 'pixel_size': '4.0'})
MAT('m_grass', 'res://shaders/terrain.gdshader', {'albedo': T('res://assets/tilesets/terrain/meadow_grass.png'), 'noise_tex': NT, 'tile_size': '1024.0', 'brightness_variation': '0.09'})
MAT('m_lawn', 'res://shaders/terrain.gdshader', {'albedo': T('res://assets/tilesets/terrain/meadow_grass.png'), 'noise_tex': NT, 'tile_size': '700.0', 'brightness_variation': '0.05', 'tint': 'Color(0.95, 1.02, 0.92, 1)'})
MAT('m_sand', 'res://shaders/terrain.gdshader', {'albedo': T('res://assets/tilesets/terrain/dirt_gravel.png'), 'noise_tex': NT, 'tile_size': '900.0', 'brightness_variation': '0.05', 'tint': 'Color(1.12, 1.06, 0.92, 1)'})
MAT('m_court', 'res://shaders/terrain.gdshader', {'albedo': T('res://assets/tilesets/castle/courtyard.png'), 'noise_tex': NT, 'tile_size': '380.0', 'brightness_variation': '0.06', 'break_repetition': '0.0',
     'grime_tex': T('res://assets/tilesets/terrain/dirt_gravel.png'), 'grime_amount': '0.18', 'warm_cool': 'Vector3(0.03, 0.015, -0.02)'})
MAT('m_court_light', 'res://shaders/terrain.gdshader', {'albedo': T('res://assets/tilesets/castle/courtyard.png'), 'noise_tex': NT, 'tile_size': '340.0', 'brightness_variation': '0.05', 'break_repetition': '0.0', 'tint': 'Color(1.07, 1.05, 1.03, 1)'})
MAT('m_walk', 'res://shaders/terrain.gdshader', {'albedo': T('res://assets/tilesets/castle/walkway.png'), 'noise_tex': NT, 'tile_size': '512.0', 'brightness_variation': '0.04', 'break_repetition': '0.0', 'tint': 'Color(1.08, 1.05, 1.02, 1)'})
MAT('m_foam', 'res://shaders/shore_foam.gdshader', {'noise_tex': NT, 'pixel_size': '4.0'})
FLOORS = {'cobble': 'm_court', 'cobble_light': 'm_court_light', 'grass': 'm_lawn', 'walk': 'm_walk'}

TEX_FACE = T('res://assets/tilesets/castle/stone_face.png')
TEX_MERLON = T('res://assets/tilesets/castle/merlon_band.png')
TEX_CORBEL = T('res://assets/tilesets/castle/corbel_band.png')
TEX_BRIDGE = T('res://assets/tilesets/castle/bridge_arch_face.png')
TEX_CLIFF = T('res://assets/castle_hd/wall_kit/T14_cliff_face.png')

N('[node name="Castle" type="Node2D"]')
X0, Y0, X1, Y1 = LY.WORLD_RECT
N(f'[node name="Water" type="Polygon2D" parent="."]\nz_index = -100\nmaterial = SubResource("m_water")\npolygon = {fmt([(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)])}')

# ------------------------------------------------------------------ outer land (no trees)
import gen_scene_helpers as GH
N('[node name="Ground" type="Node2D" parent="."]\nz_index = -90')
N('[node name="ShoreFoam" type="Node2D" parent="Ground"]')
LANDO = [(nm, GH.organic(p, seed=i+3)) for i, (nm, p) in enumerate(LY.LAND)]
for i, r in enumerate(BP.ROCKS):
    LANDO.append((f'RockW{i}', GH.organic(r, step=8, amp=3.0, seed=40+i)))
    LANDO.append((f'RockE{i}', GH.organic([BP.mirror_pt(p) for p in reversed(r)], step=8, amp=3.0, seed=50+i)))
for nm, p in LANDO:
    N(f'[node name="{nm}Foam" type="Line2D" parent="Ground/ShoreFoam"]\nmaterial = SubResource("m_foam")\npoints = {fmt([W(q) for q in p + [p[0]]])}\nwidth = 420.0\ntexture_mode = 1\njoint_mode = 2')
SHORE_FLIP = False
N('[node name="SandBanks" type="Node2D" parent="Ground"]')
for nm, p in LANDO:
    q = p if sum(x0*y1 - x1*y0 for (x0, y0), (x1, y1) in zip(p, p[1:] + p[:1])) < 0 else p[::-1]
    if SHORE_FLIP: q = q[::-1]
    N(f'[node name="{nm}Bank" type="Line2D" parent="Ground/SandBanks"]\ntexture_repeat = 2\ntexture = {T("res://assets/castle_hd/terrain/R2_shore_edge.png")}\ntexture_mode = 1\npoints = {fmt([W(v) for v in q + [q[0]]])}\nwidth = 128.0\njoint_mode = 2')
# cliffs under camera-facing shores (vertical slices)
N('[node name="Cliffs" type="Node2D" parent="Ground"]')
CLIFF_H, TEXH = 440.0, 440.0
for nm, p in LANDO:
    for j, r in enumerate(GH.south_runs(p)):
        pts = [W(r[0])]
        for q in r[1:]:
            q = W(q)
            if q[0] > pts[-1][0] + 2: pts.append(q)
        if len(pts) < 2: continue
        verts, uvs, polys = [], [], []
        for (x, y) in pts:
            verts += [(x, y-14), (x, y-14+CLIFF_H)]; uvs += [(x*TEXH/CLIFF_H, 1.0), (x*TEXH/CLIFF_H, TEXH-4.0)]
        for i in range(len(pts)-1):
            a = 2*i; polys.append(f'PackedInt32Array({a}, {a+2}, {a+3}, {a+1})')
        N(f'[node name="{nm}BaseFoam{j}" type="Line2D" parent="Ground/ShoreFoam"]\nmaterial = SubResource("m_foam")\npoints = {fmt([(x, y+CLIFF_H-30) for x, y in pts])}\nwidth = 260.0\ntexture_mode = 1\njoint_mode = 2')
        N(f'[node name="{nm}Cliff{j}" type="Polygon2D" parent="Ground/Cliffs"]\ntexture_repeat = 2\ntexture = {TEX_CLIFF}\npolygon = {fmt(verts)}\nuv = {fmt(uvs)}\npolygons = [{", ".join(polys)}]')
N('[node name="Land" type="Node2D" parent="Ground"]')
for nm, p in LANDO:
    N(f'[node name="{nm}" type="Polygon2D" parent="Ground/Land"]\nmaterial = SubResource("m_grass")\npolygon = {fmt([W(q) for q in p])}')

# ------------------------------------------------------------------ castle geometry
N('[node name="CastleGeometry" type="Node2D" parent="."]\nz_index = -40')
N('[node name="Waterline" type="Node2D" parent="CastleGeometry"]\nz_index = -45\nz_as_relative = false')
CG = 'CastleGeometry'
uid = [0]
def nid(prefix): uid[0] += 1; return f'{prefix}{uid[0]}'

def shade_for(nx, ny):
    """Light from the upper-left: faces turned left are lit, faces turned right are in shadow."""
    return max(0.62, min(1.08, 0.9 - 0.24 * nx + 0.04 * ny))

def face_strip(parent, a, b, u0, drop, nx, ny, tex=None, tex_h=720.0, rail=0.0, uv_scale=1.0, base_dark=0.68, drop_b=None, tex_k=None):
    """Vertical face hanging from the top edge a->b by `drop`."""
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1-x0, y1-y0)
    s = shade_for(nx, ny)
    top0, top1 = (x0, y0-rail), (x1, y1-rail)
    drop_b = drop if drop_b is None else drop_b
    bot0, bot1 = (x0, y0+drop), (x1, y1+drop_b)
    H = max(drop, drop_b) + rail
    us = uv_scale
    uv = [(u0, 0), (u0+L, 0), (u0+L, drop_b+rail), (u0, drop+rail)]
    if tex:  # bridge: one arch per tile; the arch texture is stretched to the face height
        kx = tex_k or 1.0; ky = tex_h / H
        uv = [(u0*kx, 0), ((u0+L)*kx, 0), ((u0+L)*kx, (drop_b+rail)*ky), (u0*kx, (drop+rail)*ky)]
    cols = [(s*1.0, s*1.0, s*1.02, 1), (s, s, s*1.02, 1), (s*base_dark, s*base_dark, s*base_dark*1.06, 1), (s*base_dark, s*base_dark, s*base_dark*1.06, 1)]
    N(f'[node name="{nid("Face")}" type="Polygon2D" parent="{parent}"]\ntexture_repeat = 2\ntexture = {tex or TEX_FACE}\n'
      f'polygon = {fmt([top0, top1, bot1, bot0])}\nuv = {fmt(uv)}\nvertex_colors = PackedColorArray({", ".join(fcol(c)[6:-1] for c in cols)})')

def band(parent, a, b, u0, h, tex, up=True, shade=1.0, period=275.0):
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1-x0, y1-y0)
    if up: quad = [(x0, y0-h), (x1, y1-h), (x1, y1), (x0, y0)]
    else:  quad = [(x0, y0), (x1, y1), (x1, y1+h), (x0, y0+h)]
    uv = [(u0, 0), (u0+L, 0), (u0+L, h), (u0, h)]
    N(f'[node name="{nid("Band")}" type="Polygon2D" parent="{parent}"]\ntexture_repeat = 2\ntexture = {tex}\ncolor = Color({shade:.3f}, {shade:.3f}, {shade*1.02:.3f}, 1)\n'
      f'polygon = {fmt(quad)}\nuv = {fmt(uv)}')

def foam_line(pts):
    N(f'[node name="{nid("Foam")}" type="Line2D" parent="{CG}/Waterline"]\nmaterial = SubResource("m_foam")\npoints = {fmt(pts)}\nwidth = 200.0\ntexture_mode = 1\njoint_mode = 2')

def build_block(name, poly_ref, drop_ref, floor, parapet=True, corbels=False, open_edges=(), in_water=False,
                face_tex=None, rail=0.0, walkway=True, merlon_all=True, vdrop=None, tex_k=None, banners=()):
    poly = ccw([W(p) for p in poly_ref])
    drop = drop_ref * K
    vd = (lambda p: vdrop(p) * K) if vdrop else (lambda p: drop)
    parent = f'{CG}/{name}'
    N(f'[node name="{name}" type="Node2D" parent="{CG}"]')
    normals = outward_normals(poly)
    n = len(poly)
    # cumulative arc length -> bricks continue around corners
    cum = [0.0]
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i+1) % n]; cum.append(cum[-1] + math.hypot(x1-x0, y1-y0))
    front = [i for i in range(n) if normals[i][1] > 0.18]
    open_set = set(open_edges)
    # faces
    N(f'[node name="Faces" type="Node2D" parent="{parent}"]')
    for i in front:
        if i in open_set and not face_tex: continue
        a, b = poly[i], poly[(i+1) % n]
        face_strip(f'{parent}/Faces', a, b, cum[i], vd(a), *normals[i], tex=face_tex, rail=rail, drop_b=vd(b), tex_k=tex_k)
        if in_water: foam_line([(a[0], a[1]+vd(a)-8), (b[0], b[1]+vd(b)-8)])
    # wall details (Surendar F7): arrow slits high, ivy / spouts low; deterministic
    if corbels and in_water and not face_tex:
        rnd = random.Random(len(nodes))
        DEC = [('F7A_arrow_slit', 0.30), ('F7C_ivy_patch', 0.62), ('F7B_drain_spout', 0.50), ('F7A_arrow_slit', 0.30), ('F7D_barred_window', 0.35)]
        for i in front:
            a, b = poly[i], poly[(i+1) % n]; L = math.hypot(b[0]-a[0], b[1]-a[1])
            k = 0; t = 260.0
            while t < L - 260:
                x = a[0] + (b[0]-a[0]) * t / L; y = a[1] + (b[1]-a[1]) * t / L
                if all(abs(x - bx*K) > 200 for bx in banners) and all(abs(x - tx*K) > 150 and abs(x - (2*BP.AXIS - tx)*K) > 150 for tx, _ in BP.WALL_TORCHES):
                    name_, frac = DEC[(k + int(x)) % len(DEC)]; d_ = vd((x, y))
                    N(f'[node name="{nid("Decal")}" type="Sprite2D" parent="{parent}/Faces"]\nposition = Vector2({x:.0f}, {y + CORBEL_H + (d_ - CORBEL_H) * frac:.0f})\ntexture = {T("res://assets/castle_hd/props/" + name_ + ".png")}')
                    k += 1
                t += rnd.uniform(300, 420)
    # banners hanging on camera-facing faces
    for bx in banners:
        bx *= K
        for i in front:
            a, b = poly[i], poly[(i+1) % n]
            if min(a[0], b[0]) + 90 < bx < max(a[0], b[0]) - 90:
                t = (bx - a[0]) / (b[0] - a[0]); y = a[1] + t * (b[1] - a[1])
                N(f'[node name="{nid("Banner")}" type="Sprite2D" parent="{parent}/Faces"]\nmaterial = ExtResource("{E("Material", "res://resources/banner_sway_material.tres")}")\n'
                  f'position = Vector2({bx:.0f}, {y + 150:.0f})\ntexture = {T("res://assets/castle_hd/props/F5_wall_banner.png")}\noffset = Vector2(0, 200)')
                break
    # floor
    N(f'[node name="Floor" type="Polygon2D" parent="{parent}"]\nmaterial = SubResource("{FLOORS[floor]}")\npolygon = {fmt(poly)}')
    # walkway band inside the parapet
    if walkway and parapet:
        inner = Polygon(poly).buffer(-WALKWAY_W/2, join_style=2, mitre_limit=4)
        if not inner.is_empty and inner.geom_type == 'Polygon':
            ring = list(inner.exterior.coords)[:-1]
            N(f'[node name="Walkway" type="Line2D" parent="{parent}"]\nmaterial = SubResource("m_walk")\npoints = {fmt(ring + [ring[0]])}\nwidth = {WALKWAY_W}\njoint_mode = 0\nsharp_limit = 6.0')
    # corbels on camera-facing faces, merlons on all edges
    if corbels:
        for i in front:
            if i in open_set: continue
            a, b = poly[i], poly[(i+1) % n]
            band(parent, a, b, cum[i], CORBEL_H, TEX_CORBEL, up=False, shade=shade_for(*normals[i]))
    if parapet:
        N(f'[node name="Parapet" type="Node2D" parent="{parent}"]')
        for i in range(n):
            if i in open_set or abs(normals[i][0]) < 0.8: continue
            a, b = poly[i], poly[(i+1) % n]
            inset = -normals[i][0] * 22
            N(f'[node name="{nid("SideParapet")}" type="Line2D" parent="{parent}/Parapet"]\nmaterial = SubResource("m_walk")\n'
              f'points = {fmt([(a[0]+inset, a[1]), (b[0]+inset, b[1])])}\nwidth = 44.0\ndefault_color = Color(1, 1, 1, 1)\nmodulate = Color(0.78, 0.76, 0.8, 1)')
            N(f'[node name="{nid("SideLip")}" type="Line2D" parent="{parent}/Parapet"]\n'
              f'points = {fmt([(a[0]+inset*2, a[1]), (b[0]+inset*2, b[1])])}\nwidth = 6.0\ndefault_color = Color(0.17, 0.18, 0.26, 0.85)')
        order = sorted(range(n), key=lambda i: (poly[i][1] + poly[(i+1) % n][1]))   # back edges first
        for i in order:
            if i in open_set: continue
            if not merlon_all and i not in front: continue
            a, b = poly[i], poly[(i+1) % n]
            band(f'{parent}/Parapet', a, b, cum[i], MERLON_H, TEX_MERLON, up=True, shade=shade_for(*normals[i]) if i in front else 0.86)
    return poly

def line_block(line_ref, thick_ref):
    ls = LineString([W(p) for p in line_ref]).buffer(thick_ref*K/2, cap_style=2, join_style=2)
    return [(x/K, y/K) for x, y in list(ls.exterior.coords)[:-1]]

# terraces, low to high, back to front within a level
items = []
for t in BP.TERRACES:
    for k, poly in enumerate(both_sides(t['top'])):
        items.append((t['level'], min(p[1] for p in poly), f"{t['name']}{'' if len(both_sides(t['top'])) == 1 else 'WE'[k]}", poly, t))
items.sort(key=lambda x: (x[0], x[1]))
for lvl, _, name, poly, t in items:
    oe = t.get('open_edges', [])
    if lvl == 1:
        build_block(name, poly, t['drop'], t['floor'], corbels=True, in_water=True, banners=BP.CURTAIN_BANNERS + [2*BP.AXIS - x for x in BP.CURTAIN_BANNERS])
    else:
        # open edges are listed for the west-half outline; map by matching edge endpoints
        open_idx = []
        if oe:
            src = t['top']
            P = ccw([W(p) for p in poly]); n = len(P)
            keys = set()
            for e in oe:
                a, b = src[e], src[(e+1) % len(src)]
                for q in (a, b, BP.mirror_pt(a), BP.mirror_pt(b)): keys.add((round(q[0]*K), round(q[1]*K)))
            for i in range(n):
                a, b = P[i], P[(i+1) % n]
                if (round(a[0]), round(a[1])) in keys and (round(b[0]), round(b[1])) in keys: open_idx.append(i)
        build_block(name, poly, t['drop'], t['floor'], corbels=False, open_edges=open_idx)

def drop_along(line, drops):
    ls = LineString(line); cum = [0.0]
    for (x0, y0), (x1, y1) in zip(line, line[1:]): cum.append(cum[-1] + math.hypot(x1-x0, y1-y0))
    def f(p):
        d = ls.project(ls.interpolate(ls.project(__import__('shapely').geometry.Point(p[0]/K, p[1]/K))))
        for i in range(len(cum)-1):
            if d <= cum[i+1] or i == len(cum)-2:
                t = 0 if cum[i+1] == cum[i] else (d-cum[i])/(cum[i+1]-cum[i]); return drops[i] + t*(drops[i+1]-drops[i])
    return f
for w in BP.WALLS:
    for k, (line, drops) in enumerate([(w['line'], w['drops']), ([BP.mirror_pt(p) for p in reversed(w['line'])], list(reversed(w['drops'])))]):
        bn = BP.BARBICAN_BANNERS if w['name'] == 'Barbican' else []
        if k == 1: bn = [2*BP.AXIS - x for x in bn]
        build_block(f"{w['name']}{'WE'[k]}", line_block(line, w['thick']), max(drops), 'walk', corbels=True, in_water=True, walkway=False,
                    vdrop=drop_along(line, drops), banners=bn)
for b in BP.BRIDGES:
    for k, line in enumerate([b['line'], [BP.mirror_pt(p) for p in reversed(b['line'])]]):
        span = math.hypot(line[1][0]-line[0][0], line[1][1]-line[0][1]) * K
        arches = max(1, round(span / 1000)); kx = 1024.0 * arches / span
        build_block(f"{b['name']}{'WE'[k]}", line_block(line, b['thick']), b['drop'], 'walk', parapet=True, in_water=True,
                    face_tex=TEX_BRIDGE, walkway=False, tex_k=kx)

# ---- details on top of the geometry
MAT('m_dirt', 'res://shaders/terrain.gdshader', {'albedo': T('res://assets/tilesets/terrain/dirt_gravel.png'), 'noise_tex': NT, 'tile_size': '700.0', 'brightness_variation': '0.06'})
N(f'[node name="Details" type="Node2D" parent="{CG}"]')
DT = f'{CG}/Details'
def mirrored(poly): return [poly, [BP.mirror_pt(p) for p in reversed(poly)]]
for yard in BP.YARDS:
    for poly in mirrored(yard):
        P = [W(p) for p in poly]
        N(f'[node name="{nid("Yard")}" type="Polygon2D" parent="{DT}"]\nmaterial = SubResource("m_dirt")\npolygon = {fmt(P)}')
        N(f'[node name="{nid("YardEdge")}" type="Line2D" parent="{DT}"]\nmaterial = SubResource("m_walk")\npoints = {fmt(P + [P[0]])}\nwidth = 36.0\njoint_mode = 0\nsharp_limit = 6.0')
for pool in BP.POOLS:
    for poly in mirrored(pool):
        P = [W(p) for p in poly]
        N(f'[node name="{nid("PoolRimBack")}" type="Polygon2D" parent="{DT}"]\ncolor = Color(0.3, 0.31, 0.4, 1)\npolygon = {fmt([(x, y-24) for x, y in P])}')
        N(f'[node name="{nid("Pool")}" type="Polygon2D" parent="{DT}"]\nmaterial = SubResource("m_water")\npolygon = {fmt(P)}')
        N(f'[node name="{nid("PoolRim")}" type="Line2D" parent="{DT}"]\ntexture_repeat = 2\ntexture = {T("res://assets/castle_hd/wall_kit/T15_pool_rim.png")}\ntexture_mode = 1\npoints = {fmt(P + [P[0]])}\nwidth = 48.0\njoint_mode = 0\nsharp_limit = 6.0')
for c in BP.COLONNADES:
    for line in mirrored(c['line']):
        (x0, y0), (x1, y1) = W(line[0]), W(line[1])
        if x0 > x1: (x0, y0), (x1, y1) = (x1, y1), (x0, y0)
        top = y0 - c['drop'] * K
        N(f'[node name="{nid("ColonnadeBack")}" type="Polygon2D" parent="{DT}"]\ncolor = Color(0.1, 0.11, 0.17, 1)\npolygon = {fmt([(x0, top), (x1, top), (x1, y0), (x0, y0)])}')
        span = x1 - x0; kx = 1024.0 * c['arches'] / span
        N(f'[node name="{nid("Colonnade")}" type="Polygon2D" parent="{DT}"]\ntexture_repeat = 2\ntexture = {TEX_BRIDGE}\npolygon = {fmt([(x0, top), (x1, top), (x1, y0), (x0, y0)])}\n'
          f'uv = {fmt([(0, 0), (span*kx, 0), (span*kx, 720), (0, 720)])}')
        band(DT, (x0, top), (x1, top), 0, MERLON_H, TEX_MERLON, up=True, shade=0.95)
for f in BP.BARBICAN_FALLS:
    for side in (1, -1):
        cxp = (BP.AXIS + (f['x'] - BP.AXIS) * side) * K; y0s, y1s = f['sluice_y'][0] * K, f['sluice_y'][1] * K
        w = f['width'] * K / f['arches']
        for j in range(f['arches']):
            ax = cxp - f['width'] * K / 2 + j * w + w * 0.12; aw = w * 0.76; r = aw / 2
            pts = [(ax, y1s)] + [(ax + r - r * math.cos(t * math.pi / 12), y0s + r - r * math.sin(t * math.pi / 12)) for t in range(13)] + [(ax + aw, y1s)]
            N(f'[node name="{nid("Sluice")}" type="Polygon2D" parent="{DT}"]\ncolor = Color(0.07, 0.09, 0.16, 1)\npolygon = {fmt(pts)}')
            gs = 2.0
            N(f'[node name="{nid("SluiceGrate")}" type="Sprite2D" parent="{DT}"]\nposition = Vector2({ax + aw / 2:.0f}, {y1s:.0f})\nscale = Vector2({gs}, {gs})\ntexture = {T("res://assets/castle_hd/props/F6_sluice_grate.png")}\noffset = Vector2(0, -30)')

# causeway: raised stone road from the gate to the south shore
cx0, cx1, cy0, cy1 = BP.CAUSEWAY
cpoly = ccw([W(p) for p in [(cx0, cy0), (cx1, cy0), (cx1, cy1), (cx0, cy1)]])
c_open = [i for i in range(4) if abs(cpoly[i][1] - cpoly[(i+1) % 4][1]) < 1]   # no parapet across either end of the road
build_block('Causeway', [(cx0, cy0), (cx1, cy0), (cx1, cy1), (cx0, cy1)], 34, 'cobble_light', parapet=True, corbels=False, in_water=True, walkway=False, open_edges=c_open)
for k, poly in enumerate([BP.GATE_LANDING['block'], [BP.mirror_pt(p) for p in reversed(BP.GATE_LANDING['block'])]]):
    build_block(f'GateLanding{"WE"[k]}', poly, BP.GATE_LANDING['drop'], 'walk', corbels=True, in_water=True, walkway=False)

# ------------------------------------------------------------------ set pieces (Y-sorted)
N('[node name="YSorted" type="Node2D" parent="."]\ny_sort_enabled = true')
N('[node name="Towers" type="Node2D" parent="YSorted"]\ny_sort_enabled = true')
P_TOWER = E('PackedScene', 'res://scenes/castle/parts/Tower.tscn')
P_FLAT = E('PackedScene', 'res://scenes/castle/parts/BarbicanTower.tscn')
P_GATET = E('PackedScene', 'res://scenes/castle/parts/GateTowerTall.tscn')
KIND = {'blue': P_TOWER, 'big': P_TOWER, 'flat': P_TOWER, 'pillar': P_TOWER, 'gate': P_GATET}
WATER_TOWERS = {(57, 624), (80, 400), (123, 296), (277, 694), (438, 795), (603, 728), (690, 705),
                (150, 862), (163, 862), (295, 880), (395, 935), (503, 942), (640, 960)}
for i, (kind, x, y, sc) in enumerate(BP.TOWERS):
    for side, (xx, yy) in (('W', (x, y)), ('E', BP.mirror_pt((x, y)))):
        inw = 'true' if (x, y) in WATER_TOWERS else 'false'
        N(f'[node name="{kind.capitalize()}Tower{i+1}{side}" parent="YSorted/Towers" instance=ExtResource("{KIND[kind]}")]\n'
          f'position = Vector2({xx*K}, {yy*K})\nscale = Vector2({sc}, {sc})\nin_water = {inw}' + ('\nshow_roof = false\nshow_banner = false' if kind in ('flat', 'pillar') else ''))

N('[node name="SetPieces" type="Node2D" parent="YSorted"]\ny_sort_enabled = true')
gx, gy = BP.GATEHOUSE
N(f'[node name="Gatehouse" parent="YSorted/SetPieces" instance=ExtResource("{E("PackedScene", "res://scenes/castle/parts/Gatehouse.tscn")}")]\nposition = Vector2({gx*K}, {gy*K})\nscale = Vector2(1.35, 1.35)')
px, py = BP.PALACE
N(f'[node name="Palace" parent="YSorted/SetPieces" instance=ExtResource("{E("PackedScene", "res://scenes/castle/parts/Palace.tscn")}")]\nposition = Vector2({px*K}, {py*K})')
P_ST = E('PackedScene', 'res://scenes/castle/parts/GrandStairs.tscn')
P_STP = E('PackedScene', 'res://scenes/castle/parts/GrandStairsPlain.tscn')
for nm, d, pid in (('StairsUpper', BP.STAIRS_UPPER, P_STP), ('StairsLower', BP.STAIRS_LOWER, P_ST)):
    sxs = d['half_w'] * 2 * K / 1057.0; sys_ = (d['base'] - d['top']) * K / 594.0
    N(f'[node name="{nm}" parent="YSorted/SetPieces" instance=ExtResource("{pid}")]\nposition = Vector2({d["x"]*K}, {d["base"]*K})\nscale = Vector2({sxs:.3f}, {sys_:.3f})')
fx, fy = BP.FOUNTAIN
N(f'[node name="Fountain" parent="YSorted/SetPieces" instance=ExtResource("{E("PackedScene", "res://scenes/castle/parts/FountainPlaza.tscn")}")]\nposition = Vector2({fx*K}, {fy*K})\nscale = Vector2(0.85, 0.85)')
for nm, x, y in BP.BUILDINGS:
    N(f'[node name="{nm}" parent="YSorted/SetPieces" instance=ExtResource("{E("PackedScene", f"res://scenes/castle/parts/{nm}.tscn")}")]\nposition = Vector2({x*K}, {y*K})' + ('\nscale = Vector2(1.3, 1.3)' if nm in ('Cathedral', 'DomedHall') else ''))
P_G = E('PackedScene', 'res://scenes/castle/parts/Gargoyle.tscn'); P_KN = E('PackedScene', 'res://scenes/castle/parts/KnightStatueTall.tscn')
P_KD = E('PackedScene', 'res://scenes/castle/parts/KnightStatue.tscn'); P_BR = E('PackedScene', 'res://scenes/castle/parts/Brazier.tscn')
for side in (1, -1):
    def X(x): return (BP.AXIS + (x - BP.AXIS) * side) * K
    flip = '\nflip_h = true' if side < 0 else ''
    for gx_, gy_ in BP.GARGOYLES:
        N(f'[node name="Gargoyle{side}" parent="YSorted/SetPieces" instance=ExtResource("{P_G}")]\nposition = Vector2({X(gx_)}, {gy_*K}){flip}\nz_index = 1')
    for kx_, ky_ in BP.STAIR_KNIGHTS:
        N(f'[node name="StairKnight{side}" parent="YSorted/SetPieces" instance=ExtResource("{P_KN}")]\nposition = Vector2({X(kx_)}, {ky_*K}){flip}')
    kx_, ky_ = BP.GATE_LANDING['knight']; lx_, ly_ = BP.GATE_LANDING['lantern']
    N(f'[node name="LandingKnight{side}" parent="YSorted/SetPieces" instance=ExtResource("{P_KD}")]\nposition = Vector2({X(kx_)}, {ky_*K}){flip}')
    N(f'[node name="LandingLantern{side}" parent="YSorted/SetPieces" instance=ExtResource("{E("PackedScene", "res://scenes/castle/parts/LanternPillar.tscn")}")]\nposition = Vector2({X(lx_)}, {ly_*K})\nscale = Vector2(1.3, 1.3)')
    for f in BP.BARBICAN_FALLS:
        N(f'[node name="BarbicanFall{side}" parent="YSorted/SetPieces" instance=ExtResource("{E("PackedScene", "res://scenes/castle/parts/BarbicanWaterfall.tscn")}")]\nposition = Vector2({X(f["x"])}, {f["base"]*K})' + ('\nscale = Vector2(-1, 1)' if side < 0 else ''))
    N(f'[node name="GateKnight{side}" parent="YSorted/SetPieces" instance=ExtResource("{P_KD}")]\nposition = Vector2({X(722)}, {722*K}){flip}')
    for j, y in enumerate(range(760, 1020, 62)):
        N(f'[node name="CausewayBrazier{side}_{j}" parent="YSorted/SetPieces" instance=ExtResource("{P_BR}")]\nposition = Vector2({X(cx0+7)}, {y*K})')

# ---- Surendar pieces: rocks on the outcrops, wall torches, seagulls
P_RL = E('PackedScene', 'res://scenes/castle/parts/RockLarge.tscn'); P_RS = E('PackedScene', 'res://scenes/castle/parts/RockSmall.tscn')
P_WT = E('PackedScene', 'res://scenes/castle/parts/WallTorch.tscn'); P_SG = E('PackedScene', 'res://scenes/castle/parts/Seagull.tscn')
for side in (1, -1):
    def X(x): return (BP.AXIS + (x - BP.AXIS) * side) * K
    flip = '\nflip_h = true' if side < 0 else ''
    for j, (x, y, big) in enumerate(BP.ROCK_SPRITES):
        N(f'[node name="Rock{side}_{j}" parent="YSorted/SetPieces" instance=ExtResource("{P_RL if big else P_RS}")]\nposition = Vector2({X(x)}, {y*K}){flip}')
    for j, (x, y) in enumerate(BP.WALL_TORCHES):
        N(f'[node name="WallTorch{side}_{j}" parent="{CG}/Details" instance=ExtResource("{P_WT}")]\nposition = Vector2({X(x)}, {y*K})')
for j, (x, y) in enumerate(BP.SEAGULLS):
    N(f'[node name="Seagull{j}" parent="." instance=ExtResource("{P_SG}")]\nposition = Vector2({x*K}, {y*K})\nspeed = {0.08 + 0.02*j:.2f}')

# ------------------------------------------------------------------ lighting, camera, reference
N(f'[node name="WorldTint" type="CanvasModulate" parent="."]\ncolor = Color(1, 0.9, 0.78, 1)')
N(f'[node name="DayNight" type="Node" parent="."]\nscript = ExtResource("{E("Script", "res://scripts/castle/day_night.gd")}")\ncanvas_modulate = NodePath("../WorldTint")')
S('[sub_resource type="Environment" id="env"]\nbackground_mode = 3\nglow_enabled = true\nglow_intensity = 0.6\nglow_strength = 0.9\nglow_bloom = 0.05\nglow_blend_mode = 1\nglow_hdr_threshold = 1.05')
N('[node name="Environment" type="WorldEnvironment" parent="."]\nenvironment = SubResource("env")')
N(f'[node name="Reference" type="Sprite2D" parent="."]\nvisible = false\nmodulate = Color(1, 1, 1, 0.45)\nz_index = 100\nscale = Vector2({K}, {K})\ntexture = ExtResource("{E("Texture2D", "res://docs/reference/castle_reference.png")}")\ncentered = false')
L0, T0, R0, B0 = LY.CAMERA_LIMITS
N(f'[node name="DebugCamera" type="Camera2D" parent="."]\nposition = Vector2({768*K}, {600*K})\nzoom = Vector2(0.25, 0.25)\nscript = ExtResource("{E("Script", "res://scripts/debug_camera.gd")}")\n'
  f'reference_path = NodePath("../Reference")\nlimit_left = {L0}\nlimit_top = {T0}\nlimit_right = {R0}\nlimit_bottom = {B0}')

head = f'[gd_scene load_steps={len(ext)+len(sub)+1} format=3]\n'
body = head + '\n' + '\n'.join(f'[ext_resource type="{t}" path="{p}" id="{i}"]' for t, p, i in ext) + '\n\n' + '\n\n'.join(sub) + '\n\n' + '\n\n'.join(nodes) + '\n'
open(os.path.join(ROOT, 'scenes/castle/Castle.tscn'), 'w').write(body)
print('nodes', len(nodes), 'bytes', len(body))
