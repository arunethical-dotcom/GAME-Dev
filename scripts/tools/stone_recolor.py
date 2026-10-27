"""Recolour sandstone art to the castle plan's grey stone (sampled from the reference).
Only warm, low/mid-saturation 'stone' pixels are mapped; roofs, banners, wood, iron and
flames keep their colour."""
import numpy as np
STONE = [(0.0, '#151a30'), (0.12, '#3c3e52'), (0.32, '#595768'), (0.52, '#706b77'),
         (0.70, '#887f86'), (0.86, '#a69a96'), (1.0, '#dccabb')]
def _hex(h): return np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], float)
def hsv(a):
    r, g, b = a[..., 0] / 255, a[..., 1] / 255, a[..., 2] / 255
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b); d = mx - mn
    h = np.zeros_like(mx); m = d > 1e-6
    rr = (mx == r) & m; gg = (mx == g) & m & ~rr; bb = m & ~rr & ~gg
    h[rr] = ((g - b)[rr] / d[rr]) % 6; h[gg] = (b - r)[gg] / d[gg] + 2; h[bb] = (r - g)[bb] / d[bb] + 4
    return h / 6, np.where(mx > 0, d / np.maximum(mx, 1e-6), 0), mx
def stone_mask(a):
    h, s, v = hsv(a[..., :3].astype(float))
    warm = ((h > 0.02) & (h < 0.17)) | (s < 0.12)
    # flames: orange cores (hue 0.03-0.075, very saturated, bright) plus their halo.
    # Sandstone highlights sit at hue ~0.1 and are recoloured.
    from scipy import ndimage as ndi
    seed = (h > 0.03) & (h < 0.075) & (s > 0.8) & (v > 0.75)
    seed = ndi.binary_opening(seed, iterations=1)
    flame = ndi.binary_dilation(seed, iterations=7) & (s > 0.35) & (v > 0.55) & (h < 0.17)
    gold = (h > 0.1) & (h < 0.17) & (s > 0.7) & (v > 0.55)     # banner trim / finials
    return warm & ~flame & ~gold & (a[..., 3] > 0)
def recolor(a, stops=STONE, lo=1, hi=99.5, mask=None):
    a = a.astype(float).copy(); m = stone_mask(a) if mask is None else mask
    L = a[..., :3] @ np.array([0.299, 0.587, 0.114])
    if not m.any(): return a.astype(np.uint8)
    p0, p1 = np.percentile(L[m], lo), np.percentile(L[m], hi)
    t = np.clip((L - p0) / max(p1 - p0, 1), 0, 1)
    xs = [q for q, _ in stops]; cs = np.array([_hex(c) for _, c in stops])
    out = np.dstack([np.interp(t, xs, cs[:, k]) for k in range(3)])
    out += (a[..., :3] - L[..., None]) * 0.08
    a[m, :3] = np.clip(out[m], 0, 255)
    return a.astype(np.uint8)
