"""
Intake for generated assets (magenta-background sprites, horizontal strips, seamless tiles).

  python3 scripts/tools/ingest_assets.py <batch_dir> <mapping.json> <author>

mapping.json: {"<file in batch_dir>": "<SAVE AS name from CASTLE_PROMPTS.xlsx>", ...}

For every image:
  1. background removed: flat magenta (also magenta holes inside the object) or existing alpha
  2. magenta spill on the edges cleaned (no pink fringe)
  3. stone pixels nudged from warm beige to the plan's cool grey (shading untouched)
  4. trimmed, scaled to its final in-game size on a 2 px art-pixel grid (hard pixel edges, hard alpha)
  5. strips (cliff, rim, shore) made seamless left-right
Outputs: assets/castle_hd/<category>/<ID>.png and the untouched original in assets/castle_hd/_raw/<author>/.
"""
import json, os, shutil, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
HD = os.path.join(ROOT, 'assets', 'castle_hd')

# final in-game size (px) per ID: sprites = fit inside (w, h); bands = target height, width follows aspect
SPEC = {
 'F1': ('sprite', 142, 285, True), 'F2': ('sprite', 156, 390, True), 'F3': ('sprite', 100, 225, False), 'F4': ('sprite', 40, 90, False),
 'F5': ('sprite', 130, 290, False), 'F6': ('sprite', 60, 70, True), 'F7A': ('sprite', 60, 120, True), 'F7B': ('sprite', 120, 120, True),
 'F7C': ('sprite', 120, 120, False), 'F7D': ('sprite', 120, 120, True),
 'E1': ('sprite', 560, 880, False), 'E2': ('sprite', 600, 200, False), 'E4': ('sprite', 570, 480, False), 'E5': ('sprite', 44, 100, False),
 'E7A': ('sprite', 48, 32, False), 'E7B': ('sprite', 48, 32, False),
 'R1A': ('sprite', 600, 300, False), 'R1B': ('sprite', 300, 200, False),
 'T5A': ('sprite', 96, 96, True), 'T5B': ('sprite', 96, 96, True),
 'R2': ('band', 0, 64, False), 'T14': ('band', 0, 440, False), 'T15': ('band', 0, 48, True),
}
CATEGORY = {'F': 'props', 'E': 'effects', 'R': 'terrain', 'T': 'wall_kit', 'TW': 'towers', 'G': 'gatehouse', 'P': 'palace', 'S': 'stairs', 'B': 'buildings'}
MAGENTA = np.array([255, 0, 255], float)
STONE_CHROMA = np.array([1.0, -2.0, 8.0])     # plan wall colour minus its luminance (cool grey-blue)

def asset_id(name):
    return name.split('_')[0]

def category(i):
    for k in ('TW', 'F', 'E', 'R', 'T', 'G', 'P', 'S', 'B'):
        if i.startswith(k): return CATEGORY[k]
    return 'misc'

def key_background(img):
    a = np.array(img.convert('RGBA')).astype(float)
    if img.mode == 'RGBA' and (a[..., 3] < 128).mean() > 0.05:
        alpha = (a[..., 3] >= 128)
    else:
        d = np.linalg.norm(a[..., :3] - MAGENTA, axis=2)
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        pinkish = (r > 150) & (b > 150) & (g < 110) & (np.abs(r - b) < 80)
        bg = (d < 95) | pinkish
        alpha = ~bg
        # spill clean on the outline: remove the magenta cast (r and b raised above g)
        ring = ndi.binary_dilation(bg, iterations=3) & alpha
        spill = np.clip(np.minimum(r, b) - g - 8, 0, None) * ring
        a[..., 0] -= spill; a[..., 2] -= spill
        # outline pixels that are mostly magenta: drop them
        alpha &= ~(ring & (d < 150))
    alpha = ndi.binary_opening(alpha, iterations=1)
    lab, n = ndi.label(alpha)
    if n > 1:   # drop dust specks smaller than 0.05 % of the object
        sz = ndi.sum(alpha, lab, range(1, n + 1)); keep = np.isin(lab, [i + 1 for i, s in enumerate(sz) if s >= alpha.sum() * 0.0005])
        alpha &= keep
    a[..., 3] = alpha * 255
    return np.clip(a, 0, 255)

def cool_stone(a):
    rgb = a[..., :3]; L = rgb @ np.array([0.299, 0.587, 0.114])
    mx, mn = rgb.max(2), rgb.min(2); sat = (mx - mn) / np.maximum(mx, 1)
    hue_warm = (rgb[..., 0] >= rgb[..., 2])
    w = np.clip((0.32 - sat) / 0.12, 0, 1) * hue_warm * (a[..., 3] > 0) * np.clip((L - 25) / 30, 0, 1)
    cur = rgb - L[..., None]
    a[..., :3] = np.clip(rgb + (STONE_CHROMA - cur) * w[..., None] * 0.85, 0, 255)
    return a

def trim(a):
    ys, xs = np.nonzero(a[..., 3] > 0)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def resize_art(a, W, H):
    """Premultiplied Lanczos to (W/2, H/2) art pixels, hard alpha, then 2x nearest."""
    w2, h2 = max(1, round(W / 2)), max(1, round(H / 2))
    p = a.astype(np.float32) / 255; p[..., :3] *= p[..., 3:4]
    ch = [np.array(Image.fromarray(p[..., c]).resize((w2, h2), Image.LANCZOS)) for c in range(4)]
    o = np.clip(np.dstack(ch), 0, 1); al = o[..., 3:4]
    rgb = np.where(al > 1e-4, o[..., :3] / np.maximum(al, 1e-4), 0)
    out = np.dstack([np.clip(rgb, 0, 1), (al > 0.5).astype(np.float32)]) * 255
    out = out.astype(np.uint8); out[out[..., 3] == 0, :3] = 0
    return np.array(Image.fromarray(out).resize((w2 * 2, h2 * 2), Image.NEAREST))

def seamless_x(a, frac=0.08):
    H, W = a.shape[:2]; F = max(8, int(W * frac))
    w = np.linspace(0, 1, F)[None, :, None]
    start = a[:, :F] * w + a[:, -F:] * (1 - w)
    return np.concatenate([start, a[:, F:W - F]], 1)

def process(src, save_as):
    i = asset_id(save_as); kind, W, H, stone = SPEC[i]
    a = key_background(Image.open(src))
    if stone: a = cool_stone(a)
    if kind == 'band':
        rows = np.nonzero((a[..., 3] > 0).mean(1) > 0.985)[0]
        a = a[rows.min() + 2:rows.max() - 1]
        # any leftover magenta/pink pixel takes the colour of its nearest clean neighbour
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        bad = (a[..., 3] == 0) | ((np.minimum(r, b) - g > 70) & (r > 150) & (b > 120))
        if bad.any():
            idx = ndi.distance_transform_edt(bad, return_distances=False, return_indices=True)
            a[..., :3] = a[..., :3][idx[0], idx[1]]
        a[..., 3] = 255
        a = seamless_x(a)
        h, w = a.shape[:2]; Wt = int(round(w * H / h / 2) * 2)
        pad = 24; big = np.concatenate([a[:, -pad:], a, a[:, :pad]], 1)
        r = resize_art(big, int(round(big.shape[1] * Wt / w / 2) * 2), H)
        p2 = int(round(pad * Wt / w / 2) * 2); out = r[:, p2:p2 + Wt]
    else:
        a = trim(a); h, w = a.shape[:2]; s = min(W / w, H / h)
        out = resize_art(a, max(2, int(round(w * s / 2) * 2)), max(2, int(round(h * s / 2) * 2)))
    return out

def main(batch, mapping, author):
    M = json.load(open(mapping)); report = []
    os.makedirs(os.path.join(HD, '_raw', author), exist_ok=True)
    for src, save_as in M.items():
        i = asset_id(save_as)
        if i not in SPEC: report.append((save_as, 'skipped: no size spec')); continue
        out = process(os.path.join(batch, src), save_as)
        d = os.path.join(HD, category(i)); os.makedirs(d, exist_ok=True)
        Image.fromarray(out).save(os.path.join(d, save_as), optimize=True)
        shutil.copy(os.path.join(batch, src), os.path.join(HD, '_raw', author, save_as))
        report.append((save_as, f'{out.shape[1]}x{out.shape[0]}'))
    for r in report: print(*r)

if __name__ == '__main__':
    main(*sys.argv[1:4])
