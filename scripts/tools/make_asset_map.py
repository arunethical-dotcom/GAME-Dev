"""
Asset map: the original castle plan with a chess-style grid and every asset ID from
docs/ASSET_REQUIREMENTS.md marked where it is used.

  python3 scripts/tools/make_asset_map.py

Outputs (docs/asset_map/):
  asset_map_full.png         whole plan, 2x, grid + all IDs
  asset_map_<region>.png     zoomed regions (3x) for reading labels
  asset_map_grid_only.png    plan + grid, no labels (for prompts / tracing)
  asset_placements.csv       every placement: id, plan x, plan y, grid cell, note
and docs/ASSET_MAP.md (index: ID -> grid cells).

Grid: 32 px cells on the 1536 x 1024 plan. Columns A..Z, AA..AV (48); rows 1..32 (top to bottom).
Cell "K12" = column K, row 12. Coordinates in the CSV are plan pixels (world px = plan px x 10).
"""
import os, sys, csv, math
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'blueprint'))
import castle_blueprint as BP

CELL = 32
OUT = os.path.join(ROOT, 'docs', 'asset_map'); os.makedirs(OUT, exist_ok=True)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'
if not os.path.exists(FONT): FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def col_name(i):
    s = ''; i += 1
    while i: i, r = divmod(i - 1, 26); s = chr(65 + r) + s
    return s
def cell(x, y): return f'{col_name(int(x // CELL))}{int(y // CELL) + 1}'

# ---------------------------------------------------------------- categories (colour, title)
CAT = {
    'T':  ((255, 214, 64), 'Textures / wall kit'),
    'TW': ((90, 170, 255), 'Towers'),
    'G':  ((255, 120, 60), 'Gatehouse'),
    'P':  ((235, 90, 235), 'Palace'),
    'S':  ((255, 255, 255), 'Staircase'),
    'B':  ((120, 235, 140), 'Buildings'),
    'F':  ((255, 170, 200), 'Props / fixtures'),
    'E':  ((80, 235, 235), 'Effects'),
    'R':  ((190, 150, 110), 'Terrain'),
}
def cat_of(i):
    for k in ('TW', 'T', 'G', 'P', 'S', 'B', 'F', 'E', 'R'):
        if i.startswith(k) and (k != 'T' or not i.startswith('TW')): return k
    return 'T'

# ---------------------------------------------------------------- placements
P = []   # (ids list, x, y, note)
def add(ids, x, y, note='', mirror=True):
    P.append((ids, x, y, note))
    if mirror and abs(x - BP.AXIS) > 2: P.append((ids, 2 * BP.AXIS - x, y, note))

TOWER_H = {'S': 59, 'M': 98, 'L': 133}
for kind, x, y, sc in BP.TOWERS:
    size = 'L' if sc >= 1.3 else ('S' if sc <= 0.65 else 'M')
    body = {'S': 'TW1', 'M': 'TW2', 'L': 'TW3'}[size]
    water = (x, y) in {(57, 624), (80, 400), (123, 296), (277, 694), (438, 795), (603, 728), (690, 705),
                       (150, 862), (295, 880), (395, 935), (503, 942), (640, 960)}
    if kind == 'pillar': ids = ['TW7']
    elif kind == 'flat': ids = [body, 'TW5']
    else: ids = [body, 'TW6', 'TW8'] + (['TW9'] if kind == 'gate' else [])
    if water and kind != 'pillar': ids += ['TW4', 'E3']
    add(ids, x, y - TOWER_H[size] * sc * 0.55, f'{kind} tower, scale {sc}, base at y={y}')

# walls and wall kit
for x, y, n in [(560, 662, 'curtain wall face (front)'), (330, 636, 'curtain wall face (diagonal step)'),
                (196, 500, 'curtain wall face (west side)'), (230, 830, 'barbican face'), (450, 888, 'barbican face')]:
    add(['T1', 'T2', 'T3', 'T6'], x, y, n)
for x, y, n in [(380, 482, 'cathedral terrace face'), (640, 318, 'palace terrace face'), (600, 520, 'garden terrace face')]:
    add(['T1', 'T3'], x, y, n)
for x, y in [(474, 636), (404, 610), (258, 590), (300, 804), (395, 860), (214, 226)]:
    add(['T5'], x, y, 'wall corner')
add(['T4'], 300, 104, 'back of wall (seen from behind)')
add(['T7'], 560, 628, 'wall-walk on curtain wall')
add(['T8'], 640, 590, 'lower ward courtyard')
add(['T8'], 300, 180, 'lower ward courtyard')
add(['T9'], 610, 262, 'palace terrace paving')
add(['T10'], 768, 820, 'causeway road', mirror=False)
add(['T11'], 330, 330, 'cathedral lawn'); add(['T11'], 646, 450, 'cypress garden'); add(['T11'], 545, 560, 'south garden')
add(['T12'], 326, 540, 'market / training yard')
for x, y, n in [(121, 540, 'lower flank bridge'), (155, 338, 'upper flank bridge'), (188, 196, 'top flank bridge')]:
    add(['T13'], x, y, n)
add(['T14', 'R1'], 205, 900, 'rock outcrop under barbican'); add(['T14', 'R1'], 420, 935, 'rock outcrop under barbican')
add(['T15'], 532, 497, 'reflecting pool rim')
add(['R2'], 70, 700, 'moat shore edge'); add(['R3'], 330, 740, 'moat water')

# gatehouse
gx, gy = BP.GATEHOUSE
add(['G1', 'G4'], gx, gy - 70, 'main gatehouse', mirror=False)
add(['G2', 'G3'], gx, gy - 18, 'portcullis + doors', mirror=False)
add(['F4', 'E5'], gx - 36, gy - 40, 'gate wall torch')

# palace
px, py = BP.PALACE
add(['P1', 'P7'], px, py - 90, 'central keep', mirror=False)
add(['P6'], px, py - 140, 'giant banner', mirror=False)
add(['P2'], px - 120, py - 60, 'wing segment A'); add(['P3'], px - 205, py - 60, 'wing segment B')
add(['P4'], px - 262, py - 70, 'corner pavilion')
add(['P5'], px, 26, 'back turret silhouette (behind)', mirror=False)

# stairs
add(['S1'], 768, 252, 'upper flight (plain)', mirror=False)
add(['S3'], 768, 287, 'landing balustrade', mirror=False)
add(['S2'], 768, 330, 'lower flight (carpet)', mirror=False)
for x, y in BP.GARGOYLES: add(['S4'], x, y - 10, 'gargoyle on pillar')
for x, y in BP.STAIR_KNIGHTS: add(['S5'], x, y - 12, 'knight at stair foot')

# buildings
pos = {n: (x, y) for n, x, y in BP.BUILDINGS}
add(['B1'], pos['Cathedral'][0], pos['Cathedral'][1] - 70, 'cathedral', mirror=False)
add(['B2'], pos['Chapel'][0], pos['Chapel'][1] - 45, 'chapel', mirror=False)
add(['B3'], pos['DomedHall'][0], pos['DomedHall'][1] - 60, 'domed hall', mirror=False)
add(['B4'], pos['Manor'][0], pos['Manor'][1] - 45, 'manor', mirror=False)
add(['B5'], 546, 452, 'arched colonnade')
fx, fy = BP.FOUNTAIN
add(['B6', 'E4'], fx, fy - 18, 'central fountain', mirror=False)

# props / fixtures
add(['F1'], *BP.GATE_LANDING['knight'], 'knight statue, barbican landing')
add(['F1'], 722, 718, 'knight statue at the gate')
add(['F2'], *BP.GATE_LANDING['lantern'], 'lantern pillar')
for j, y in enumerate(range(760, 1020, 62)): add(['F3', 'E5'], 723, y - 8, 'causeway brazier')
for x in BP.CURTAIN_BANNERS: add(['F5'], x, 660 if x > 474 else 646, 'wall banner (curtain wall)')
for x in BP.BARBICAN_BANNERS:
    y = 820 if x < 295 else (836 + (x - 300) * 0.55 if x < 395 else 872)
    add(['F5'], x, y, 'wall banner (barbican)')
add(['F6', 'E1', 'E2'], 228, 870, 'sluice grates + waterfall + splash')
add(['F7'], 610, 676, 'wall decals (slits, spouts, ivy)')
add(['E7'], 110, 720, 'seagulls (optional)')

# ---------------------------------------------------------------- drawing
def draw_map(scale, crop=None, labels=True, out='x.png'):
    plan = Image.open(os.path.join(ROOT, 'docs/reference/castle_reference.png')).convert('RGB')
    W, H = plan.size
    img = plan.resize((W * scale, H * scale), Image.NEAREST)
    img = Image.blend(img, Image.new('RGB', img.size, (10, 14, 28)), 0.30 if labels else 0.12).convert('RGBA')
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    fsz = max(11, int(7.5 * scale)); f = ImageFont.truetype(FONT, fsz); fg = ImageFont.truetype(FONT, max(10, int(6 * scale)))
    # grid
    for i in range(0, W + 1, CELL // 2):
        major = i % CELL == 0; X = i * scale
        d.line([(X, 0), (X, img.height)], fill=(255, 255, 255, 120 if major else 40), width=1)
    for j in range(0, H + 1, CELL // 2):
        major = j % CELL == 0; Y = j * scale
        d.line([(0, Y), (img.width, Y)], fill=(255, 255, 255, 120 if major else 40), width=1)
    for c in range(W // CELL):
        for r in range(H // CELL):
            if (c + r) % 2 == 0 or scale >= 3:
                d.text((c * CELL * scale + 3, r * CELL * scale + 2), f'{col_name(c)}{r+1}', font=fg, fill=(255, 255, 255, 95))
    if labels:
        placed = []
        for ids, x, y, note in P:
            X, Y = x * scale, y * scale
            text = ' '.join(ids); col = CAT[cat_of(ids[0])][0]
            tw = d.textlength(text, font=f); th = fsz + 6
            cand = [(0, -th - 6), (0, 8), (tw / 2 + 10, -th / 2), (-tw / 2 - 10, -th / 2), (0, -2 * th - 10), (0, th + 12),
                    (tw / 2 + 14, -th - 8), (-tw / 2 - 14, -th - 8), (tw / 2 + 14, 10), (-tw / 2 - 14, 10)]
            for dx, dy in cand:
                bx0, by0 = X + dx - tw / 2 - 5, Y + dy
                box = (bx0, by0, bx0 + tw + 10, by0 + th)
                if not any(not (box[2] < b[0] or box[0] > b[2] or box[3] < b[1] or box[1] > b[3]) for b in placed): break
            placed.append(box)
            r = max(3, scale * 2)
            d.ellipse([X - r, Y - r, X + r, Y + r], fill=col + (255,), outline=(0, 0, 0, 255))
            cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
            if abs(cx - X) + abs(cy - Y) > th: d.line([(X, Y), (cx, cy)], fill=col + (200,), width=max(1, scale // 2))
            d.rounded_rectangle(box, radius=4, fill=(12, 14, 24, 225), outline=col + (255,), width=max(1, scale // 2))
            d.text((box[0] + 5, box[1] + 2), text, font=f, fill=col + (255,))
    img = Image.alpha_composite(img, ov).convert('RGB')
    if crop:
        img = img.crop(tuple(v * scale for v in crop))
    # column / row rulers
    rw = 30 * max(1, scale // 2)
    x0, y0 = (crop[0], crop[1]) if crop else (0, 0)
    canvas = Image.new('RGB', (img.width + rw, img.height + rw), (18, 20, 30)); canvas.paste(img, (rw, rw))
    d2 = ImageDraw.Draw(canvas); fr = ImageFont.truetype(FONT, max(12, int(6.5 * scale)))
    for c in range(W // CELL):
        X = (c * CELL - x0) * scale + rw
        if rw <= X + CELL * scale / 2 < canvas.width: d2.text((X + CELL * scale / 2 - 8, 6), col_name(c), font=fr, fill=(255, 230, 120))
    for r in range(H // CELL):
        Y = (r * CELL - y0) * scale + rw
        if rw <= Y + CELL * scale / 2 < canvas.height: d2.text((4, Y + CELL * scale / 2 - 8), str(r + 1), font=fr, fill=(255, 230, 120))
    canvas.save(os.path.join(OUT, out), optimize=True)
    return canvas

def legend(out):
    f = ImageFont.truetype(FONT, 22); fb = ImageFont.truetype(FONT, 26)
    img = Image.new('RGB', (1500, 90 + 46 * len(CAT)), (18, 20, 30)); d = ImageDraw.Draw(img)
    d.text((24, 20), 'Asset map legend: IDs refer to docs/ASSET_REQUIREMENTS.md · grid = 32 px cells (A–AV × 1–32)', font=fb, fill=(255, 230, 120))
    for i, (k, (c, t)) in enumerate(CAT.items()):
        y = 80 + 46 * i
        d.rounded_rectangle([24, y, 110, y + 34], radius=5, fill=(12, 14, 24), outline=c, width=2); d.text((36, y + 4), k, font=f, fill=c)
        d.text((130, y + 4), t, font=f, fill=(230, 230, 230))
    img.save(os.path.join(OUT, out))

draw_map(2, out='asset_map_full.png')
draw_map(2, labels=False, out='asset_map_grid_only.png')
REGIONS = {'palace': (380, 0, 1156, 420), 'west': (0, 60, 560, 720), 'centre': (420, 200, 1116, 720),
           'gate_south': (380, 560, 1156, 1024), 'barbican_west': (80, 740, 760, 1024), 'east': (976, 60, 1536, 720)}
for n, b in REGIONS.items(): draw_map(3, crop=b, out=f'asset_map_{n}.png')
legend('asset_map_legend.png')

# ---------------------------------------------------------------- index
rows = []
for ids, x, y, note in P:
    for i in ids: rows.append((i, round(x), round(y), cell(x, y), note))
with open(os.path.join(OUT, 'asset_placements.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['id', 'plan_x', 'plan_y', 'grid_cell', 'note']); w.writerows(sorted(rows, key=lambda r: (r[0], r[3])))
from collections import OrderedDict
by = OrderedDict()
def key(i):
    k = cat_of(i); n = int(''.join(ch for ch in i if ch.isdigit()) or 0)
    return (list(CAT).index(k), n)
for i, x, y, c, note in sorted(rows, key=lambda r: key(r[0])):
    by.setdefault(i, {'cells': [], 'notes': set()}); by[i]['cells'].append(c); by[i]['notes'].add(note)
lines = ['# Asset map: where every asset goes', '',
         'The original plan with a grid and every asset ID from `docs/ASSET_REQUIREMENTS.md` marked where it is used.', '',
         '- **Grid:** 32 px cells on the 1536 × 1024 plan. Columns **A–AV** (left → right), rows **1–32** (top → bottom). Cell `K12` = column K, row 12.',
         '- **Full map:** `docs/asset_map/asset_map_full.png` (2×). **Zoomed regions:** `asset_map_palace / west / east / centre / gate_south / barbican_west.png` (3×).',
         '- **Grid only** (no labels, for reference prompts): `asset_map_grid_only.png`. **Every placement with exact coordinates:** `asset_placements.csv`.',
         '- The castle is mirror-symmetric about the line between columns **X** and **Y** (x = 768); most IDs appear on both sides.', '',
         '![legend](asset_map/asset_map_legend.png)', '', '![map](asset_map/asset_map_full.png)', '',
         '## Index', '', '| ID | Uses | Grid cells | Where |', '|---|---|---|---|']
for i, v in by.items():
    cells = sorted(set(v['cells']), key=lambda c: (len(c.rstrip('0123456789')), c.rstrip('0123456789'), int(c[len(c.rstrip('0123456789')):])))
    lines.append(f"| **{i}** | {len(v['cells'])} | {', '.join(cells)} | {'; '.join(sorted(v['notes']))} |")
lines += ['', '## How to use it to generate art', '',
          '1. Find the ID in `ASSET_REQUIREMENTS.md` for its size, frames and rules.',
          '2. Crop the plan at the listed grid cells (`asset_map_grid_only.png`) and use that crop as the visual reference for that asset.',
          '3. Deliver at the listed size into `assets/castle_hd/`, named after the ID, e.g. `TW2_tower_m_body.png`.', '']
open(os.path.join(ROOT, 'docs', 'ASSET_MAP.md'), 'w').write('\n'.join(lines))
print('placements', len(P), 'rows', len(rows), 'ids', len(by))
