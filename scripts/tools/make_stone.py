"""Procedural, perfectly seamless ashlar stone textures in the castle plan's palette.
Generated at half resolution and upscaled 2x (nearest) so they read as pixel art."""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

def _hex(h): return np.array([int(h[i:i+2], 16) for i in (1, 3, 5)], float)
RAMP = [(0.0, '#1c2036'), (0.18, '#3d3f53'), (0.38, '#5a5868'), (0.56, '#726c77'),
        (0.74, '#8b8288'), (0.9, '#a99d98'), (1.0, '#cbbdb2')]
def ramp(t, stops=RAMP):
    xs = [q for q, _ in stops]; cs = np.array([_hex(c) for _, c in stops])
    return np.dstack([np.interp(t, xs, cs[:, k]) for k in range(3)])

def wrap_noise(shape, sigma, rng):
    return ndi.gaussian_filter(rng.standard_normal(shape), sigma, mode='wrap')

def ashlar(W=256, H=120, course=20, bmin=26, bmax=52, mortar=2, seed=1, stops=RAMP,
           tone=0.0, moss=0.0):
    """W,H at half resolution; returns RGBA uint8 at full resolution (2W x 2H)."""
    rng = np.random.default_rng(seed)
    assert H % course == 0
    L = np.zeros((H, W)); bid = np.zeros((H, W), int); edge = np.zeros((H, W))
    k = 0
    for r in range(H // course):
        y0 = r * course
        x = rng.integers(0, bmax)          # random phase per course, wraps horizontally
        xs = []
        while True:
            xs.append(x); x += rng.integers(bmin, bmax + 1)
            if x - xs[0] >= W - bmin: break
        xs.append(xs[0] + W)
        for a, b in zip(xs, xs[1:]):
            k += 1; base = 0.52 + rng.normal(0, 0.07)
            cols = np.arange(a, b) % W
            for yy in range(y0, y0 + course):
                L[yy, cols] = base; bid[yy, cols] = k
    # bevel: light from upper-left
    up = np.roll(bid, 1, 0) != bid; left = np.roll(bid, 1, 1) != bid
    down = np.roll(bid, -1, 0) != bid; right = np.roll(bid, -1, 1) != bid
    m = np.zeros_like(L, bool)
    for s in range(mortar):
        m |= np.roll(down, -s, 0) | np.roll(right, -s, 1)
    hl = (np.roll(up, 1, 0) | up | np.roll(left, 1, 1) | left) & ~m
    sh = (np.roll(down, 1, 0) | np.roll(right, 1, 1)) & ~m & ~hl
    L = L + hl * 0.16 - sh * 0.14
    L = L + wrap_noise((H, W), 0.8, rng) * 0.05 + wrap_noise((H, W), 6, rng) * 0.08
    # chips / cracks
    for _ in range(W * H // 900):
        cy, cx = rng.integers(0, H), rng.integers(0, W)
        L[cy, cx:(cx + rng.integers(2, 6)) % W or W] -= 0.12
    L[m] = 0.08
    L = np.clip(L + tone, 0, 1)
    rgb = ramp(L, stops)
    if moss > 0:
        mm = (wrap_noise((H, W), 4, rng) > 0.9 - moss) & ~m
        rgb[mm] = rgb[mm] * 0.55 + np.array([70, 95, 55]) * 0.45
    img = np.dstack([np.clip(rgb, 0, 255), np.full((H, W), 255)]).astype(np.uint8)
    return np.array(Image.fromarray(img).resize((W * 2, H * 2), Image.NEAREST))

def flagstones(W=256, H=256, seed=3, stops=None):
    stops = stops or [(0.0, '#2a2a3a'), (0.2, '#5d5866'), (0.45, '#8c8088'), (0.7, '#a89a98'),
                      (0.88, '#bfb1aa'), (1.0, '#d8cbc2')]
    a = ashlar(W, H, course=32, bmin=30, bmax=70, mortar=2, seed=seed, stops=stops, tone=0.08)
    return a

if __name__ == '__main__':
    import sys, os
    out = sys.argv[1]
    Image.fromarray(ashlar(seed=7)).save(os.path.join(out, 'stone_face.png'))
    Image.fromarray(ashlar(seed=11, moss=0.04, tone=-0.06)).save(os.path.join(out, 'stone_face_mossy.png'))
    Image.fromarray(ashlar(W=256, H=120, course=24, bmin=30, bmax=60, seed=21, tone=0.1)).save(os.path.join(out, 'stone_face_tower.png'))
    Image.fromarray(flagstones()).save(os.path.join(out, 'walkway.png'))
    Image.fromarray(flagstones(seed=9, stops=[(0.0, '#2b2c3c'), (0.2, '#6a6372'), (0.45, '#9a8d90'),
                    (0.7, '#b4a6a2'), (0.88, '#c6b8b1'), (1.0, '#ddd0c6')])).save(os.path.join(out, 'courtyard.png'))
    print('ok')
