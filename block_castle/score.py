"""Accuracy of a render against the castle plan (both 1536x1024).
  python3 block_castle/score.py <render.png> [out_prefix]
Headline 'build accuracy' = % of pixels whose colour difference CIEDE2000 < 10 (same colour at a glance).
Also: SSIM (luminance), mean dE2000. Writes <out_prefix>_heat.png (red = mismatch) and _blend50.png."""
import sys, json, numpy as np
from PIL import Image
from skimage.color import rgb2lab, deltaE_ciede2000
from skimage.metrics import structural_similarity
PLAN = '/home/claude/grand-castle-island/docs/reference/castle_reference.png'
def score(render, out=None):
    r = np.asarray(Image.open(PLAN).convert('RGB'), float) / 255
    b = np.asarray(Image.open(render).convert('RGB'), float) / 255
    assert r.shape == b.shape, (r.shape, b.shape)
    dE = deltaE_ciede2000(rgb2lab(r), rgb2lab(b))
    acc = float((dE < 10).mean() * 100)
    ssim = float(structural_similarity(r.mean(2), b.mean(2), data_range=1.0))
    res = dict(build_accuracy=round(acc, 2), ssim=round(ssim * 100, 2), mean_dE=round(float(dE.mean()), 2))
    if out:
        h = np.clip(dE / 25, 0, 1); heat = np.dstack([h, 1 - h, np.zeros_like(h)]) * 0.6 + r.mean(2, keepdims=True) * 0.4
        Image.fromarray((heat * 255).astype(np.uint8)).save(out + '_heat.png')
        Image.fromarray(((r + b) / 2 * 255).astype(np.uint8)).save(out + '_blend50.png')
    return res
if __name__ == '__main__':
    print(json.dumps(score(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)))
