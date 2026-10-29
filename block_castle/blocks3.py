"""3-colour 4x4 blocks: per-cell colour clustering -> ternary shape dictionary -> palette colours."""
import numpy as np
from PIL import Image
from skimage.color import rgb2lab, lab2rgb, deltaE_ciede2000
from scipy.cluster.vq import kmeans2
PLAN='/home/claude/grand-castle-island/docs/reference/castle_reference.png'

def cells(lab, c):
    H, W, _ = lab.shape; gh, gw = H // c, W // c
    return lab[:gh*c, :gw*c].reshape(gh, c, gw, c, 3).transpose(0, 2, 1, 3, 4).reshape(gh*gw, c*c, 3), gh, gw

def per_cell_kmeans(L, n=3, iters=8):
    lum = L[..., 0]
    q = np.quantile(lum, np.linspace(0, 1, n + 2)[1:-1], axis=1).T
    idx = np.argmin(np.abs(lum[:, :, None] - q[:, None, :]), axis=2)
    for _ in range(iters):
        C = np.stack([np.where((idx == k)[..., None], L, 0).sum(1) / np.maximum((idx == k).sum(1), 1)[:, None] for k in range(n)], 1)
        idx = ((L[:, :, None, :] - C[:, None, :, :]) ** 2).sum(-1).argmin(2)
    # canonical order: by luminance of the cluster centre (empty clusters pushed to the end)
    C = np.stack([np.where((idx == k)[..., None], L, 0).sum(1) / np.maximum((idx == k).sum(1), 1)[:, None] for k in range(n)], 1)
    cnt = np.stack([(idx == k).sum(1) for k in range(n)], 1)
    key = np.where(cnt > 0, C[..., 0], 1e9); order = np.argsort(key, 1); rank = np.argsort(order, 1)
    idx = np.take_along_axis(rank, idx, 1)
    return idx

def build_dictionary(idx, K, n=3):
    codes = (idx * (n ** np.arange(idx.shape[1], dtype=np.int64))).sum(1)
    u, inv, cnt = np.unique(codes, return_inverse=True, return_counts=True)
    top = u[np.argsort(-cnt)[:K]]
    D = np.stack([(top // 3 ** np.arange(idx.shape[1])) % 3 for _ in [0]][0], 0) if False else ((top[:, None] // (n ** np.arange(idx.shape[1], dtype=np.int64))[None, :]) % n)
    return D, codes

def assign(L, idx, D, pal, chunk=4000, n=3, ncand=12):
    """For each cell choose the dictionary shape + palette colours minimising Lab error.
    Candidates: the shapes nearest (Hamming) to the cell's own map."""
    ncol = n; n = len(L); best_s = np.zeros(n, int); best_c = np.zeros((n, ncol), int); best_e = np.full(n, np.inf)
    for s0 in range(0, n, chunk):
        Li = L[s0:s0+chunk]; Ii = idx[s0:s0+chunk]
        ham = (Ii[:, None, :] != D[None, :, :]).sum(-1)           # (m, K)
        cand = np.argsort(ham, 1)[:, :ncand]
        for j in range(cand.shape[1]):
            S = D[cand[:, j]]                                      # (m,16)
            cols = np.zeros((len(Li), n), int); rec = np.zeros_like(Li)
            for k in range(n):
                mk = (S == k)
                mean = np.where(mk[..., None], Li, 0).sum(1) / np.maximum(mk.sum(1), 1)[:, None]
                pi = ((mean[:, None, :] - pal[None]) ** 2).sum(-1).argmin(1)
                cols[:, k] = pi; rec = np.where(mk[..., None], pal[pi][:, None, :], rec)
            e = ((Li - rec) ** 2).sum(-1).mean(1)
            b = e < best_e[s0:s0+chunk]
            best_e[s0:s0+chunk][b] = e[b]; best_s[s0:s0+chunk][b] = cand[b, j]; best_c[s0:s0+chunk][b] = cols[b]
    return best_s, best_c

def reconstruct(D, s, cols, pal, gh, gw, c):
    S = D[s]; rec = pal[np.take_along_axis(cols, S, 1)]            # (n,16,3)
    return rec.reshape(gh, gw, c, c, 3).transpose(0, 2, 1, 3, 4).reshape(gh*c, gw*c, 3)

def palette(lab, n, seed=1):
    rng = np.random.default_rng(0); s = lab.reshape(-1, 3)[rng.choice(lab.shape[0]*lab.shape[1], 150000, replace=False)]
    c, _ = kmeans2(s, n, minit='++', seed=seed, iter=30); return c
