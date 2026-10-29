"""Draws the player sprite sheet: 24x32 art px per frame, 4 frames x 4 directions (down, up, left, right),
then scales 4x (96x128 px frames). Row order: down, up, left, right. Frame 0/2 = stand, 1/3 = step."""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
C = {'skin': (232, 180, 138), 'skin_d': (185, 128, 96), 'hair': (90, 58, 34), 'hair_d': (60, 38, 22),
     'tunic': (46, 90, 168), 'tunic_d': (31, 61, 120), 'tunic_l': (80, 128, 206), 'belt': (107, 66, 40), 'gold': (224, 176, 64),
     'pants': (58, 58, 74), 'boot': (74, 46, 30), 'cape': (182, 58, 58), 'cape_d': (130, 36, 44), 'eye': (24, 20, 32), 'white': (240, 236, 228)}
OUT = (26, 20, 32)
W, H = 24, 32

def blank(): return np.zeros((H, W, 4), np.uint8)
def rect(a, x0, y0, x1, y1, col):
    a[y0:y1 + 1, x0:x1 + 1, :3] = C[col]; a[y0:y1 + 1, x0:x1 + 1, 3] = 255

def legs(a, step, side=False):
    # step: 0 stand, 1 left forward, -1 right forward
    if not side:
        ll = 29 + (1 if step == 1 else 0) - (1 if step == -1 else 0)
        rl = 29 + (1 if step == -1 else 0) - (1 if step == 1 else 0)
        rect(a, 8, 23, 10, ll - 2, 'pants'); rect(a, 8, ll - 1, 10, ll, 'boot'); rect(a, 7, ll, 10, ll, 'boot')
        rect(a, 13, 23, 15, rl - 2, 'pants'); rect(a, 13, rl - 1, 15, rl, 'boot'); rect(a, 13, rl, 16, rl, 'boot')
    else:
        f = [0, 2, 0, -2][step % 4]
        rect(a, 10 + f, 23, 12 + f, 27, 'pants'); rect(a, 10 + f, 28, 13 + f, 29, 'boot')
        rect(a, 11 - f, 23, 13 - f, 27, 'pants_back' if False else 'pants'); rect(a, 11 - f, 28, 14 - f, 29, 'boot')

def front(step):
    a = blank()
    rect(a, 6, 13, 17, 21, 'cape_d')                      # cape edges behind
    rect(a, 7, 13, 16, 22, 'tunic'); rect(a, 8, 13, 9, 21, 'tunic_l'); rect(a, 15, 14, 16, 22, 'tunic_d')
    rect(a, 7, 20, 16, 20, 'belt'); rect(a, 11, 20, 12, 20, 'gold')
    sw = [0, 1, 0, -1][step]
    rect(a, 5, 14 - sw, 6, 19 - sw, 'tunic'); rect(a, 5, 20 - sw, 6, 21 - sw, 'skin')
    rect(a, 17, 14 + sw, 18, 19 + sw, 'tunic'); rect(a, 17, 20 + sw, 18, 21 + sw, 'skin')
    legs(a, [0, 1, 0, -1][step])
    rect(a, 8, 5, 15, 12, 'skin'); rect(a, 14, 6, 15, 12, 'skin_d')
    rect(a, 7, 3, 16, 6, 'hair'); rect(a, 7, 7, 8, 9, 'hair'); rect(a, 15, 7, 16, 8, 'hair_d')
    rect(a, 10, 9, 10, 10, 'eye'); rect(a, 13, 9, 13, 10, 'eye'); rect(a, 11, 12, 12, 12, 'skin_d')
    return a

def back(step):
    a = blank()
    sw = [0, 1, 0, -1][step]
    rect(a, 5, 14 + sw, 6, 21 + sw, 'tunic'); rect(a, 17, 14 - sw, 18, 21 - sw, 'tunic')
    legs(a, [0, -1, 0, 1][step])
    rect(a, 6, 13, 17, 24, 'cape'); rect(a, 6, 13, 7, 24, 'cape_d'); rect(a, 16, 13, 17, 24, 'cape_d'); rect(a, 11, 13, 12, 24, 'cape_d')
    rect(a, 8, 5, 15, 12, 'hair'); rect(a, 7, 3, 16, 9, 'hair'); rect(a, 14, 4, 16, 11, 'hair_d')
    return a

def side(step):   # facing right
    a = blank()
    rect(a, 7, 13, 9, 24, 'cape'); rect(a, 7, 13, 7, 24, 'cape_d')
    legs(a, step, side=True)
    rect(a, 9, 13, 15, 22, 'tunic'); rect(a, 14, 14, 15, 22, 'tunic_d'); rect(a, 9, 20, 15, 20, 'belt')
    sw = [0, 2, 0, -2][step]
    rect(a, 11 + sw, 14, 13 + sw, 19, 'tunic_l'); rect(a, 11 + sw, 20, 13 + sw, 21, 'skin')
    rect(a, 9, 5, 16, 12, 'skin'); rect(a, 9, 5, 11, 12, 'skin_d')
    rect(a, 8, 3, 16, 6, 'hair'); rect(a, 8, 7, 11, 11, 'hair')
    rect(a, 14, 9, 14, 10, 'eye'); rect(a, 16, 10, 16, 11, 'skin_d')
    return a

def outline(a):
    op = a[..., 3] > 0; ring = ndi.binary_dilation(op) & ~op
    a[ring, :3] = OUT; a[ring, 3] = 255; return a

rows = [[front(s) for s in range(4)], [back(s) for s in range(4)], [side(s)[:, ::-1] for s in range(4)], [side(s) for s in range(4)]]
sheet = np.zeros((H * 4, W * 4, 4), np.uint8)
for r, fr in enumerate(rows):
    for c, f in enumerate(fr): sheet[r * H:(r + 1) * H, c * W:(c + 1) * W] = outline(f)
img = Image.fromarray(sheet).resize((W * 4 * 4, H * 4 * 4), Image.NEAREST)
img.save('/home/claude/grand-castle-island/game/player_sheet.png'); print(img.size)
