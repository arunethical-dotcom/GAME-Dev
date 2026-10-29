"""Walk masks (plan resolution, 255 = walkable):
  walk_mask.png        Godot castle: only water is blocked (walls/towers/buildings use colliders)
  walk_mask_block.png  block castle (a flat picture): built from what each pixel shows:
                       walkable = light paving, roads, lawns; blocked = water, roofs, wall faces, trees, buildings.
                       Gate passage and stair runs are carved open; only the area connected to the causeway is kept."""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
a = np.asarray(Image.open('docs/reference/castle_reference.png').convert('RGB'), float) / 255
r, g, b = a[..., 0], a[..., 1], a[..., 2]
mx = a.max(2); mn = a.min(2); s = (mx - mn) / np.maximum(mx, 1e-6); v = mx
water = (r < 0.25) & (b > 0.35) & (g > 0.25) & (b > g)
water = ndi.binary_opening(ndi.binary_closing(water, iterations=2), iterations=2)
lab, n = ndi.label(water); sz = ndi.sum(water, lab, range(1, n + 1)); water = np.isin(lab, [i + 1 for i, k in enumerate(sz) if k > 300])
Image.fromarray(((~water) * 255).astype(np.uint8), 'L').save('game/walk_mask.png')

# ---- block castle: same rules as the Godot castle's colliders, from the traced blueprint
import sys, math; sys.path.insert(0, 'blueprint')
import castle_blueprint as BP
from PIL import ImageDraw
from shapely.geometry import Polygon, LineString
H, W = a.shape[:2]
ok = Image.new('L', (W, H), 0); dO = ImageDraw.Draw(ok)          # walkable surfaces
no = Image.new('L', (W, H), 0); dN = ImageDraw.Draw(no)          # blocked on top of them
def mirror(poly): return [BP.mirror_pt(p) for p in reversed(poly)]
def full(top): return top + [BP.mirror_pt(p) for p in reversed(top) if p[0] < BP.AXIS - 0.5]
def both(top): return [full(top)] if max(p[0] for p in top) >= BP.AXIS - 1 else [top, mirror(top)]
def faces(poly, drop):
    P = Polygon(poly); n = len(poly)
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1; nx, ny = dy / L, -dx / L
        mp = ((x0 + x1) / 2 + nx * 0.6, (y0 + y1) / 2 + ny * 0.6)
        if P.contains(Polygon([mp, (mp[0] + .1, mp[1]), (mp[0], mp[1] + .1)]).centroid): nx, ny = -nx, -ny
        if ny > 0.18: dN.polygon([(x0, y0 - 2), (x1, y1 - 2), (x1, y1 + drop), (x0, y0 + drop)], fill=255)
T = {t['name']: t for t in BP.TERRACES}
for poly in both(T['LowerWard']['top']): dO.polygon(poly, fill=255); faces(poly, T['LowerWard']['drop'])
for nm in ('PalaceTerrace', 'CathedralTerrace'):
    for poly in both(T[nm]['top']): dO.polygon(poly, fill=255)
for nm in ('PalaceTerrace', 'CathedralTerrace'):
    for poly in both(T[nm]['top']): faces(poly, T[nm]['drop'])
for nm in ('InnerGarden', 'SouthGarden'):                           # gardens: hedges and trees, no entry
    for poly in both(T[nm]['top']): dN.polygon(poly, fill=255); faces(poly, T[nm]['drop'])
cx0, cx1, cy0, cy1 = BP.CAUSEWAY; dO.rectangle([cx0, cy0, cx1, cy1], fill=255)
for poly in (BP.GATE_LANDING['block'], mirror(BP.GATE_LANDING['block'])): dO.polygon(poly, fill=255)
for kind, x, y, sc in BP.TOWERS:
    h = {'S': 59, 'M': 98, 'L': 133}['L' if sc >= 1.3 else ('S' if sc <= 0.65 else 'M')] * sc * 1.25
    for xx in (x, 2 * BP.AXIS - x): dN.rectangle([xx - 23 * sc, y - h, xx + 23 * sc, y + 3], fill=255)
dN.rectangle([468, 0, 1068, 218], fill=255)                           # palace
for nm, x, y in BP.BUILDINGS:
    w_, h_ = {'Cathedral': (68, 118), 'Chapel': (32, 58), 'DomedHall': (62, 108), 'Manor': (62, 58)}[nm]
    dN.rectangle([x - w_, y - h_, x + w_, y + 2], fill=255)
# market and training yards stay walkable (open grounds)
for poly in BP.POOLS + [mirror(p) for p in BP.POOLS]: dN.polygon(poly, fill=255)
for c in BP.COLONNADES:
    for line in (c['line'], mirror(c['line'])):
        xs = [p[0] for p in line]; y = line[0][1]; dN.rectangle([min(xs), y - c['drop'], max(xs), y + 2], fill=255)
fx, fy = BP.FOUNTAIN; dN.ellipse([fx - 22, fy - 30, fx + 22, fy + 6], fill=255)
walk = (np.asarray(ok) > 0) & ~(np.asarray(no) > 0) & ~water
def carve(x0, y0, x1, y1): walk[y0:y1, x0:x1] = True
carve(752, 600, 785, 712)       # gate passage
carve(740, 222, 796, 402)       # grand stairs (both flights + landing)
carve(334, 458, 347, 494)       # cathedral entrance stairs
carve(1189, 458, 1202, 494)     # domed hall terrace entrance stairs
carve(716, 700, 820, 1024)      # causeway
# keep only the region connected to the causeway
lab, n = ndi.label(walk); keep = lab == lab[990, 768]; walk = keep
Image.fromarray((walk * 255).astype(np.uint8), 'L').save('game/walk_mask_block.png')
for name, (x, y) in {'causeway': (768, 990), 'inside gate': (768, 590), 'plaza': (768, 520), 'fountain side': (720, 450),
                     'stairs foot': (768, 395), 'palace terrace': (700, 250), 'cathedral terrace': (300, 300), 'market': (330, 560), 'training yard': (1206, 560)}.items():
    print(f'{name:16s} reachable={bool(walk[y, x])}')
print('walkable % of plan', round(walk.mean() * 100, 1))
