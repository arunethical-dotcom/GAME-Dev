"""Builds docs/prompts/castle_asset_prompts.xlsx: one ready-to-paste image-generation prompt per asset ID."""
import csv, os
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.comments import Comment

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
cells = defaultdict(list); uses = defaultdict(int)
for r in csv.DictReader(open(os.path.join(ROOT, 'docs/asset_map/asset_placements.csv'))):
    uses[r['id']] += 1
    if r['grid_cell'] not in cells[r['id']]: cells[r['id']].append(r['grid_cell'])
def _ck(c):
    L = c.rstrip('0123456789'); n = 0
    for ch in L: n = n * 26 + ord(ch) - 64
    return (n, int(c[len(L):]))
for k in cells: cells[k].sort(key=_ck)

STYLE = ("High-quality 2D pixel art game asset for a top-down 3/4 view (JRPG style) fantasy castle. "
         "Crisp hard-edged pixels, every art pixel is an exact 2x2 block, clean dark outlines, no blur, no anti-aliasing, no painterly brush strokes, no noise grain. "
         "Cool grey-blue castle stone (#3c3e52 to #a69a96, highlights #dccabb), deep blue slate roofs (#1f2f5a to #8fb0d0), crimson banners (#b64e3f) with gold trim (#e0b040). "
         "Warm late-afternoon light from the UPPER LEFT: left-facing surfaces lit, right-facing surfaces in shade, shadows fall right and down.")
STRAIGHT = ("CAMERA: perfectly straight-on front elevation, camera centred and level, facing the object directly. "
            "NO tilt, NO rotation, NO isometric angle, NO dutch angle, NO three-quarter turn, NO perspective convergence. "
            "Vertical edges perfectly vertical, base line perfectly horizontal, object upright and centred, left/right symmetric unless stated.")
MAGENTA = ("BACKGROUND: solid flat pure magenta #FF00FF filling everything outside the object, perfectly uniform, no gradient, no texture, no floor, no ground shadow, no glow or halo on the background. "
           "Do not use any pink, magenta or purple colour inside the object. Keep a clear margin of magenta around the object (at least 4% of the canvas on every side), object must not touch or be cut by the canvas edge. "
           "The object's base sits horizontally at the bottom, centred.")
TILE = ("SEAMLESS TILE: fills the entire canvas edge to edge, no background, no border, no frame, no vignette, no magenta. "
        "Edges wrap perfectly so copies placed side by side show no seam. Flat even lighting across the tile (soft upper-left light only on each block), no large light/dark gradient across the tile. "
        "Viewed perfectly straight-on and flat, no perspective, no tilt, no rotation.")
TILE_X = TILE.replace("Edges wrap perfectly", "Left and right edges wrap perfectly (horizontal tiling strip)")
STRIP = ("ANIMATION SHEET: {n} frames in ONE horizontal row, each frame exactly {w}x{h} px, equal spacing, no gaps, no frame borders or numbers. "
         "The object stays in exactly the same position and scale in every frame; only the animated part moves. Frames loop smoothly from last to first.")
NEG_BASE = ("isometric, angled view, tilted, rotated, skewed, slanted base, perspective, vanishing point, dutch angle, three-quarter turn, side view, top-down plan view, "
            "blurry, soft focus, anti-aliased edges, painterly, oil painting, watercolor, 3D render, photorealistic, noise, jpeg artifacts, text, watermark, signature, logo, "
            "frame, border, UI, characters, people, cropped object, cut off edges, multiple objects (unless asked), drop shadow on background, gradient background, ")
NEG_SPRITE = NEG_BASE + "pink object, purple object, magenta inside the object, magenta reflections, glow halo"
NEG_TILE = NEG_BASE + "visible seams, borders, vignette, background, magenta, isolated object, large lighting gradient, repeating obvious pattern"

# id, name, category, priority, W, H, frames, fps, kind(sprite/tile/tilex/strip/script), subject, accept
A = []
def a(*r): A.append(r)
# ---- wall kit
a('T1','Wall face (ashlar), variants A and B','Wall kit',1,512,240,1,0,'tile',
  "Castle wall face texture: dressed ashlar stone blocks in even horizontal courses, each block about 80x40 px with 4 px dark mortar joints, staggered running bond. Cool grey-blue weathered stone, subtle bevel lit on top-left edges, a few small chips and hairline cracks, very slight moss in some joints. Make two variants with different block arrangements.",
  "Tiles 2x2 with no seam; courses perfectly horizontal; no windows or doors")
a('T2','Wall base / waterline band','Wall kit',1,512,96,1,0,'tilex',
  "Bottom band of a castle wall standing in a moat: the same grey-blue ashlar as T1 but darker and wet, green-black algae and slime along the lower half, vertical drip streaks, a thin bright wet line at the very bottom.",
  "Tiles horizontally; matches T1 block size; bottom edge perfectly horizontal")
a('T3','Merlon (battlement) strip, front','Wall kit',1,480,80,1,0,'sprite',
  "A horizontal crenellated battlement parapet strip seen from the front: exactly 6 identical stone merlons evenly spaced every 80 px (each merlon 48 px wide, 32 px gap between), each merlon showing a lit top face and a front face, sitting on a continuous coping course along the bottom 16 px. The strip must tile left-right: the pattern continues seamlessly across the left and right edges.",
  "6 merlons, 80 px period, top edges level, tiles horizontally")
a('T4','Merlon strip, back (seen from behind)','Wall kit',2,480,80,1,0,'sprite',
  "The same crenellated parapet as T3 but seen from the inside of the castle: merlons in shade (back face), darker tones, with the walkway coping along the bottom 16 px. 6 merlons, 80 px period, tiles left-right seamlessly.",
  "Same rhythm as T3; darker; tiles horizontally")
a('T5','Merlon corner caps (4 pieces)','Wall kit',2,384,96,1,0,'sprite',
  "Four separate battlement corner pieces in one row on magenta, each 96x96 px with magenta between: (1) outer 90-degree corner merlon, (2) inner 90-degree corner, (3) outer 135-degree corner, (4) inner 135-degree corner. Same stone and lighting as the T3 merlon strip.",
  "4 pieces, each centred in its own 96x96 cell")
a('T6','Corbel / machicolation band','Wall kit',1,480,64,1,0,'sprite',
  "A horizontal band of stepped stone corbels (machicolations) that hangs under a castle parapet: 6 corbels evenly spaced every 80 px, each a three-step stacked stone bracket, dark shadow gaps between them, continuous stone course along the top 16 px. Tiles left-right seamlessly.",
  "80 px period matching T3; tiles horizontally")
a('T7','Wall-walk paving (top of wall)','Wall kit',1,512,512,1,0,'tile',
  "Worn rectangular flagstones of a castle wall-walk seen from above, light grey-beige stone slightly lighter than the wall, slabs about 96x64 px, thin dark joints, gentle wear in the centre.",
  "Tiles 2x2 with no seam")
a('T8','Courtyard cobbles','Floors',3,512,512,1,0,'tile',
  "Irregular rounded cobblestones of a castle courtyard seen from above, warm light grey #b5a49f, stones 24-48 px, dark joints with occasional tiny moss, a few cracked stones. Even and calm, no large patterns.",
  "Tiles 2x2 with no seam; no obvious repeat at small size")
a('T9','Palace terrace paving','Floors',3,512,512,1,0,'tile',
  "Large neatly cut square and rectangular flagstones (about 128x96 px) of a royal palace terrace seen from above, clean pale grey-beige stone #c6b8b1, thin precise joints, very light wear.",
  "Tiles 2x2 with no seam")
a('T10','Causeway road cobbles','Floors',3,512,512,1,0,'tile',
  "Cobbled road surface seen from above, warmer beige-grey cobbles, slightly smoother wheel-worn band through the middle running top to bottom, small gravel between stones.",
  "Tiles 2x2 with no seam")
a('T11','Formal lawn','Floors',3,512,512,1,0,'tile',
  "Short neatly trimmed castle garden lawn seen from above, medium green #4f7f3f to #7d9b37, fine grass blades, very low contrast, a few tiny clover patches.",
  "Tiles 2x2 with no seam; no flowers; low contrast")
a('T12','Dirt yard','Floors',3,512,512,1,0,'tile',
  "Packed earth yard of a castle market and training ground seen from above, warm tan #c2a48a, scattered small pebbles, faint footprints and cart ruts, a few dry grass tufts.",
  "Tiles 2x2 with no seam")
a('T13','Bridge arch face (one arch per tile)','Wall kit',3,1024,720,1,0,'sprite',
  "Front face of a stone arched bridge section: grey-blue ashlar wall with ONE large semicircular arch centred, arch opening about 600 px wide and 560 px tall from the bottom, ring of wedge-shaped voussoir stones with a keystone, short piers on both sides with dark wet algae at the bottom 60 px. The arch OPENING is filled with magenta (it must be see-through). The stone continues to the left and right edges so sections tile side by side.",
  "Arch opening is magenta; left/right edges tile; bottom horizontal")
a('T14','Cliff face strip','Terrain',3,512,440,1,0,'tilex',
  "Vertical rock cliff face below a grassy bank: grey-blue stone columns and ledges, a grass lip with a few hanging tufts along the top 24 px, darker wet rock at the bottom 40 px where it meets water. Rock columns vertical.",
  "Tiles horizontally; grass lip on top; columns vertical")
a('T15','Pool / fountain rim','Floors',3,512,48,1,0,'tilex',
  "Carved stone coping edge of an ornamental pool seen from above-front: a rounded lip with a lit top, a short front face in shade below. Pale grey stone.",
  "Tiles horizontally; perfectly straight")
# ---- towers
TB = "Round castle tower BODY only (no roof, flat cut top): grey-blue ashlar stone in horizontal courses that curve slightly with the round shape, a corbelled ring of stepped brackets under the top rim, a slightly flared stepped base."
a('TW1','Tower body S','Towers',2,292,592,1,0,'sprite', TB+" Small size: 1 narrow arrow slit in the middle.", "Width 292, height 592; symmetric; flat top for a roof")
a('TW2','Tower body M','Towers',2,484,984,1,0,'sprite', TB+" Medium size: 2 arrow slits stacked, an iron banner rod 330 px below the top.", "Width 484, height 984; symmetric")
a('TW3','Tower body L','Towers',2,656,1332,1,0,'sprite', TB+" Large size: 2 arrow slits, one warm lit arched window, a carved string course halfway up.", "Width 656, height 1332; symmetric")
a('TW4','In-water tower base (M and L)','Towers',2,1140,200,1,0,'sprite',
  "Two separate pieces on magenta, side by side: the bottom section of a round stone tower where it rises out of a moat, M version 484x160 px and L version 656x200 px. Wet dark stone, green-black algae band, bright wet line at the bottom edge which is perfectly horizontal (the waterline). Same stone as the tower bodies.",
  "Two pieces; bottoms horizontal; widths 484 and 656")
a('TW5','Crenellated tower top cap (S and M)','Towers',2,776,220,1,0,'sprite',
  "Two separate pieces on magenta: the open top of a round stone tower seen from above-front, a ring of 7 merlons around a flagstone floor that is visible inside. S version 292x140 px and M version 484x220 px. No roof.",
  "Two pieces; widths 292 and 484; symmetric")
a('TW6','Blue cone roof (S, M, L)','Towers',2,1652,718,1,0,'sprite',
  "Three separate conical tower roofs on magenta, in a row: 8-sided steep cone of deep blue slate tiles, gold ridge trims along each edge, gold finial spike with a small orb on top, overhanging eaves with a gold-trimmed rim. Sizes S 336x320, M 560x532, L 756x718 px. Perfectly symmetric, tip exactly above the centre.",
  "Three roofs, exact sizes, symmetric, tips vertical")
a('TW7','Square pillar tower','Towers',2,330,600,1,0,'sprite',
  "Square stone pedestal tower seen straight-on: grey-blue ashlar, a flat top with a low parapet ledge (a statue will stand on top), one recessed niche with a small red banner, stepped base.",
  "Square, symmetric, flat top")
a('TW8','Tower banner (S, M, L), 4-frame sway','Towers',3,148,330,4,6,'strip',
  "Hanging crimson banner on a horizontal iron rod with gold finials: crimson cloth with a gold cross emblem and gold border, swallow-tail bottom. The cloth sways gently in the wind across the frames; the rod stays fixed. (Make the M size; S and L are scaled versions: 90x200 and 200x446.)",
  "4 frames; rod fixed; same emblem every frame")
a('TW9','Pennant flag, 6-frame wave','Towers',3,132,148,6,10,'strip',
  "A red swallow-tail pennant flag with a small gold emblem on the tip of a thin golden pole, waving in the wind to the right; the pole stays fixed.",
  "6 frames; pole fixed and vertical")
a('TW10','Emission masks for tower bodies','Masks',4,484,984,1,0,'script',"Not generated by AI: made by script from the approved TW2/TW3 sprites.","Generated automatically")
# ---- gatehouse
a('G1','Main gatehouse (symmetric, front-facing)','Gatehouse',3,1384,1208,1,0,'sprite',
  "Castle main gatehouse seen perfectly straight-on: a wide grey-blue stone gate block with two half-round flanking turrets, a large pointed arch entrance in the exact centre (about 300 px wide, 360 px tall) with a dark interior, crenellated top with merlons, a carved stone shield emblem above the arch, two crimson-and-gold banners hanging on the turrets, two iron wall torches with small flames beside the arch, a few arrow slits. Perfectly symmetric left-right. The portcullis is NOT included: the arch opening is dark stone passage.",
  "Symmetric; arch centred; no portcullis; no side faces visible")
a('G2','Portcullis, 6 frames rising','Gatehouse',3,300,360,6,8,'strip',
  "Iron portcullis grid of dark forged bars with spiked bottom tips, seen straight-on, rising upward from fully closed (frame 1) to fully open/lifted out of view (frame 6). Bars perfectly vertical and horizontal.",
  "6 frames; bars straight; same width every frame")
a('G3','Gate doors (open / closed)','Gatehouse',3,300,340,2,0,'strip',
  "Pair of heavy oak castle gate doors with black iron straps and ring handles, shaped to fit a pointed arch. Frame 1 closed, frame 2 open inward (doors swung back, dark passage visible).",
  "2 frames; arched top; symmetric")
a('G4','Gatehouse emission mask','Masks',4,1384,1208,1,0,'script',"Not generated by AI: made by script from the approved G1 sprite.","Generated automatically")
# ---- palace
a('P1','Palace central keep','Palace',4,1600,2000,1,0,'sprite',
  "The central keep of a royal fantasy palace seen straight-on: tall grey-blue stone Gothic block with pinnacles and four slender spires with blue cone roofs, a huge crimson banner with gold cross hanging down the centre, a grand arched double door of dark wood at the bottom centre with a small stone balcony above, two knight statues in niches, rows of tall stained-glass windows glowing warm yellow, blue slate roofs. Perfectly symmetric.",
  "Symmetric; door bottom-centre; base horizontal")
a('P2','Palace wing segment A','Palace',4,800,1050,1,0,'sprite',
  "A straight section of a royal palace wing seen straight-on: two storeys of tall Gothic windows glowing warm yellow, grey-blue stone with buttresses, steep blue slate roof with two dormer windows and gold ridge, small red banners between windows. Designed to repeat: left and right edges continue the same wall so copies join seamlessly.",
  "Left/right edges join seamlessly; base horizontal")
a('P3','Palace wing segment B','Palace',4,800,1050,1,0,'sprite',
  "Variation of palace wing segment A with the same height, roof line and edge joins, but with a central bay window tower and a chimney so the wing does not look repeated.",
  "Same edges and height as P2")
a('P4','Palace corner pavilion','Palace',4,600,1250,1,0,'sprite',
  "Square corner pavilion of a royal palace seen straight-on: taller than the wings, grey-blue stone, steep pyramid blue slate roof with gold finial, lit Gothic windows on three storeys, a crimson banner. Symmetric.",
  "Symmetric; taller than P2")
a('P5','Palace back silhouette layer','Palace',4,6000,900,1,0,'sprite',
  "A wide row of palace rooftops and spires seen from the front, meant to sit BEHIND the palace: 8-10 slender towers of different heights with steep blue cone roofs and gold finials, connecting blue slate roofs, a few lit windows. Symmetric overall, tallest spire in the centre.",
  "Very wide 6000x900; symmetric; bottom edge straight")
a('P6','Giant palace banner, 4-frame sway','Palace',4,300,800,4,6,'strip',
  "A very long crimson banner with a large gold cross-and-fleur emblem and gold border, hanging from a gold rod, gently swaying in the wind; rod fixed.",
  "4 frames; rod fixed")
a('P7','Palace emission masks','Masks',4,1600,2000,1,0,'script',"Not generated by AI: made by script from the approved P1-P5 sprites.","Generated automatically")
# ---- stairs
a('S1','Upper grand stair flight (plain)','Staircase',3,660,480,1,0,'sprite',
  "A wide straight stone staircase seen from the front and slightly above, going UP away from the viewer: 9 grey-blue stone steps, each tread lit and each riser in shade, a carved stone balustrade with square posts on both sides. Perfectly symmetric, steps perfectly horizontal.",
  "9 steps; treads horizontal; symmetric")
a('S2','Lower grand stair flight (red carpet)','Staircase',3,660,600,1,0,'sprite',
  "A wide straight stone staircase seen from the front and slightly above, going UP away from the viewer: 11 grey-blue stone steps, a wine-red carpet (#7e1a39) with gold edging running down the exact centre over every step (follows each tread and riser), carved balustrades both sides ending in square newel posts with small lamps. Perfectly symmetric.",
  "11 steps; carpet centred; symmetric")
a('S3','Landing balustrade','Staircase',3,480,120,1,0,'sprite',
  "A low carved stone balustrade railing seen straight-on: round balusters under a flat handrail, square posts at both ends with small stone urns on top. Tiles left-right.",
  "Straight; tiles horizontally")
a('S4','Gargoyle statue','Staircase',3,180,212,1,0,'sprite',
  "A crouching winged gargoyle statue of dark iron-grey stone, wings half-raised, facing the viewer, on a small square base. Front view.",
  "Front-facing; base horizontal")
a('S5','Knight statue on plinth (stairs)','Staircase',3,128,256,1,0,'sprite',
  "A dark iron knight statue in full plate armour standing guard, both hands resting on a sword planted point-down in front, on a square stone plinth, facing the viewer.",
  "Front-facing; symmetric")
# ---- buildings
a('B1','Cathedral','Buildings',5,1000,1300,1,0,'sprite',
  "Gothic cathedral front facade seen straight-on: grey-blue stone, a large circular stained-glass rose window (blue, red, gold) above a pointed-arch double door, two tall spires with blue slate roofs, pinnacles, lit lancet windows, steep blue roof behind, two crimson banners, a short entrance stair. Symmetric.",
  "Symmetric; rose window centred")
a('B2','Chapel','Buildings',5,660,940,1,0,'sprite',
  "Small Gothic stone chapel front seen straight-on: grey-blue stone, pointed-arch door, small stained-glass window, steep blue slate roof, a slender bell turret with a cross on top. Symmetric.",
  "Symmetric")
a('B3','Domed hall','Buildings',5,1228,1100,1,0,'sprite',
  "Grand domed hall seen straight-on: central dark-blue tiled dome with a small lantern cupola and gold finial, a ring of glowing arched windows under the dome, grey-blue stone facade with columns, two small side wings with blue roofs, a wide entrance stair in the centre. Symmetric.",
  "Symmetric; dome centred")
a('B4','Manor house','Buildings',5,1212,880,1,0,'sprite',
  "Two-storey stone manor house seen straight-on: grey-blue stone walls, blue slate hipped roof with dormers and chimneys, central arched oak door with a small porch, rows of lit windows, small red banners. Symmetric.",
  "Symmetric")
a('B5','Arched colonnade','Buildings',5,790,380,1,0,'sprite',
  "A straight stone colonnade wall seen straight-on: three equal tall round arches with dark shadowed interiors, slender columns between them, a crenellated parapet on top. Symmetric.",
  "3 equal arches; symmetric")
a('B6','Central fountain','Buildings',5,570,480,1,0,'sprite',
  "An ornate tiered stone fountain seen from the front and slightly above: octagonal basin with carved rim, two stacked bowls on a central column with a small finial, small flower planters at the basin corners. The WATER is NOT included: basins and bowls are empty and dry (water is a separate animated layer).",
  "Symmetric; no water")
# ---- props
a('F1','Knight statue, dark (gate)','Props',6,142,285,1,0,'sprite',
  "Dark iron knight statue in plate armour holding a tall shield and sword, on a square stone pedestal with a carved crest, facing the viewer.",
  "Front-facing; base horizontal")
a('F2','Lantern pillar','Props',6,156,390,1,0,'sprite',
  "A square carved stone pillar topped by a black iron lantern with glass panes glowing warm yellow inside, seen straight-on.",
  "Symmetric; vertical")
a('F3','Brazier on tripod (no flame)','Props',6,100,225,1,0,'sprite',
  "A black iron fire brazier: a round bowl full of glowing embers on a tall three-legged tripod stand, seen straight-on. NO flames (flames are a separate animation).",
  "No flames; tripod vertical")
a('F4','Wall torch sconce (no flame)','Props',6,40,90,1,0,'sprite',
  "A black iron wall torch bracket holding a wooden torch with a charred top, seen straight-on, as mounted on a wall. NO flame.",
  "No flame; vertical")
a('F5','Wall banner, 4-frame sway','Props',6,130,290,4,6,'strip',
  "A crimson castle wall banner with a gold cross emblem and gold border, swallow-tail bottom, hanging from a short iron rod; cloth sways gently, rod fixed.",
  "4 frames; rod fixed")
a('F6','Sluice arch grate','Props',6,60,70,1,0,'sprite',
  "A small round-topped iron grate of vertical bars set in a stone arch, seen straight-on, with water stains below.",
  "Bars vertical; symmetric")
a('F7','Wall decals set','Props',7,480,240,1,0,'sprite',
  "A set of 8 small separate wall decorations on magenta in a grid of 4 columns x 2 rows of 120x120 px cells: arrow slit, stone drain spout, iron mooring ring, ivy patch, crack, moss patch, small barred window, carved crest. Each flat on a wall, straight-on.",
  "8 items each in its own 120x120 cell")
# ---- effects
a('E1','Barbican waterfall, 8 frames','Effects',5,560,880,8,10,'strip',
  "A waterfall pouring straight down from three small arched openings at the top: bright white-blue water streams with foam, falling vertically, widening slightly to the bottom. Falling-water motion loops across the frames.",
  "8 frames; water vertical; loops")
a('E2','Waterfall splash, 6 frames','Effects',5,600,200,6,10,'strip',
  "White foam and spray splash where a waterfall hits a lake: churning foam, small droplets, bubbles spreading outward horizontally; loops.",
  "6 frames; loops")
a('E3','Tower water ring, 4 frames','Effects',5,700,170,4,6,'strip',
  "A flat elliptical ring of gentle white water ripples and foam around the base of a round tower standing in water (the tower itself NOT included, centre is empty magenta), seen from above-front. Make the L size; the M size 520x130 is a scaled version.",
  "4 frames; ellipse horizontal; empty centre")
a('E4','Fountain water and spray, 6 frames','Effects',5,570,480,6,10,'strip',
  "Animated water for the B6 fountain: clear blue water filling the octagonal basin and both bowls, water spilling over the bowl edges in thin curtains, a small jet at the top; must line up exactly with B6.",
  "6 frames; matches B6 outline")
a('E5','Flame, 6 frames','Effects',5,44,100,6,12,'strip',
  "A small bright torch flame: orange-yellow core, red edges, a few sparks, flickering upward; the base point stays fixed.",
  "6 frames; base fixed")
a('E7','Seagull flying, 6 frames (optional)','Effects',7,48,32,6,10,'strip',
  "A small white seagull with grey wingtips flying to the right, side view, full wing-flap cycle.",
  "6 frames; loops")
# ---- terrain
a('R1','Rock outcrops (4 variants)','Terrain',6,2400,400,1,0,'sprite',
  "Four separate mossy grey-blue rock outcrops for a lake shore, on magenta in a row, each about 300-600 px wide, flat bottoms (they sit in water), patches of grass and moss on top.",
  "4 rocks; flat bottoms")
a('R2','Moat shore edge strip','Terrain',6,512,64,1,0,'tilex',
  "Narrow strip of lake shoreline seen from above: green grass at the top fading to pebbles and wet sand, ending at the bottom edge where water begins.",
  "Tiles horizontally")
a('R3','Water texture (optional redo)','Terrain',7,1024,1024,1,0,'tile',
  "Deep blue lake water seen from above #033361 to #045282, gentle wave patterns with small bright #5fc6ff highlights.",
  "Tiles 2x2 with no seam")


# ------------------------------------------------------------------ colours per asset (hex, sampled from the plan)
STONE = "stone #151a30 (deepest shadow/outline), #3c3e52 (shadow), #595768 (dark), #706b77 (mid), #887f86 (light), #a69a96 (lit face), #dccabb (top highlight); mortar #2a2b3c"
WET = "wet stone #2a3040, #3a4252; algae #1f3326, #2f4a2e; wet highlight #8fb6c8"
ROOF = "slate roof #1f2f5a (shadow), #2e4677, #486f91 (mid), #6b8fb3, #8fb0d0 (highlight); gold trim/finial #8a6420, #c9952e, #e0b040, #ffe08a"
BANNER = "banner crimson #5a1026 (shadow), #7e1a39, #b64e3f (lit); gold emblem/border #c9952e, #e0b040, #ffe08a; iron rod #1e2230, #4a4f60"
IRON = "dark iron #12141c, #23283a, #3a4155, #5b6378 (highlight)"
GLASS = "window glow #b0602a (frame shadow), #ffb347, #ffd27a, #fff3c4 (core); stained glass #1d4fa0, #b3262e, #e0b040, #3f8f4f"
WOOD = "oak #2e1c12, #4a2e1e, #6b4228, #8a5a36"
FIRE = "flame #7a1a08, #c8380e, #f07a1a, #ffb52e, #ffe680, #fffbe0 (core); embers #ff6a1a"
WATER = "water #022448, #033361, #045282, #1d7fb8, #5fc6ff; foam #cfeeff, #ffffff"
GRASS = "grass #24402a, #335a33, #4f7f3f, #6f9a45, #95b65a"
ROCK = "rock #1c2233, #2f3648, #4a5263, #6b7385, #9aa1ae; moss #3a5a2e, #5c7f3a"
FLAG = "paving #5d5866, #8c8088, #a89a98, #bfb1aa, #d8cbc2; joints #2a2a3a"
COBBLE = "cobbles #6a6372, #958a8e, #ad9f9d, #b5a49f, #c0b2ac, #dacdc4; joints #2e2e3e; moss #4a5a36"
DIRT = "earth #6b4f36, #8f6e4e, #b08c6a, #c2a48a, #d6bc9e; pebbles #7a7470, #a39a90"
CARPET = "carpet wine #4a0e22, #7e1a39, #a3264a; gold edge #c9952e, #e0b040"
BIRD = "white #f4f6f8, #d8dde3; grey wingtip #4a5060; beak #e0a030"
CLR = {
 'T1': STONE, 'T2': STONE + "; " + WET, 'T3': STONE, 'T4': STONE + " (use the darker half)", 'T5': STONE, 'T6': STONE,
 'T7': FLAG, 'T8': COBBLE, 'T9': FLAG, 'T10': COBBLE + " (slightly warmer)", 'T11': GRASS, 'T12': DIRT,
 'T13': STONE + "; " + WET + "; arch opening #FF00FF", 'T14': ROCK + "; " + GRASS + "; " + WET, 'T15': FLAG,
 'TW1': STONE + "; arrow slit #0c0e16", 'TW2': STONE + "; arrow slit #0c0e16; " + IRON, 'TW3': STONE + "; arrow slit #0c0e16; " + GLASS,
 'TW4': STONE + "; " + WET, 'TW5': STONE + "; " + FLAG, 'TW6': ROOF, 'TW7': STONE + "; " + BANNER, 'TW8': BANNER, 'TW9': BANNER + "; gold pole #c9952e, #e0b040",
 'TW10': "mask: black #000000, glow white #ffffff",
 'G1': STONE + "; " + BANNER + "; " + IRON + "; " + FIRE + "; arch interior #0c0e16, #1a1d2a", 'G2': IRON, 'G3': WOOD + "; " + IRON, 'G4': "mask: black #000000, glow white #ffffff",
 'P1': STONE + "; " + ROOF + "; " + BANNER + "; " + GLASS + "; " + WOOD, 'P2': STONE + "; " + ROOF + "; " + GLASS + "; " + BANNER, 'P3': STONE + "; " + ROOF + "; " + GLASS,
 'P4': STONE + "; " + ROOF + "; " + GLASS + "; " + BANNER, 'P5': STONE + "; " + ROOF + "; " + GLASS, 'P6': BANNER, 'P7': "mask: black #000000, glow white #ffffff",
 'S1': STONE + "; " + FLAG, 'S2': STONE + "; " + CARPET + "; lamp glow #ffd27a", 'S3': STONE, 'S4': IRON + "; " + STONE, 'S5': IRON + "; " + STONE,
 'B1': STONE + "; " + ROOF + "; " + GLASS + "; " + BANNER + "; " + WOOD, 'B2': STONE + "; " + ROOF + "; " + GLASS + "; " + WOOD,
 'B3': STONE + "; " + ROOF + "; " + GLASS + "; " + WOOD, 'B4': STONE + "; " + ROOF + "; " + GLASS + "; " + BANNER + "; " + WOOD,
 'B5': STONE + "; arch interiors #0c0e16, #1a1d2a", 'B6': STONE + "; flowers #b3262e, #e0b040, #3f8f4f",
 'F1': IRON + "; " + STONE, 'F2': STONE + "; " + IRON + "; " + GLASS, 'F3': IRON + "; embers #ff6a1a, #ffb52e, #3a1a10", 'F4': IRON + "; " + WOOD + "; charred #1a1410",
 'F5': BANNER, 'F6': IRON + "; " + STONE + "; water stain #2a3a4a", 'F7': STONE + "; " + IRON + "; ivy #24402a, #4f7f3f; " + WET,
 'E1': WATER, 'E2': WATER, 'E3': WATER, 'E4': WATER, 'E5': FIRE, 'E7': BIRD,
 'R1': ROCK + "; " + GRASS, 'R2': GRASS + "; pebbles #7a7470, #a39a90; wet sand #8f7a5e, #b8a080", 'R3': WATER,
}

MULTI = {'T5', 'TW4', 'TW5', 'TW6', 'F7', 'R1'}
def prompt(r):
    id_, name, cat, pri, w, h, fr, fps, kind, subj, acc = r
    if kind == 'script': return ('(No image to generate: created automatically by script.)', '')
    subj = subj + "\n\nCOLOURS (use only these, exact hex): " + CLR[id_] + "."
    if kind == 'tile':
        body = f"{subj}\n\n{TILE}\n\nSIZE: {w}x{h} px tile."; neg = NEG_TILE
    elif kind == 'tilex':
        body = f"{subj}\n\n{TILE_X}\n\nSIZE: {w}x{h} px strip."; neg = NEG_TILE
    elif kind == 'strip':
        body = f"{subj}\n\n{STRAIGHT}\n\n{STRIP.format(n=fr, w=w, h=h)}\n\n{MAGENTA}\n\nSIZE: whole sheet {w*fr}x{h} px ({fr} frames of {w}x{h})."; neg = NEG_SPRITE
    else:
        body = f"{subj}\n\n{STRAIGHT}\n\n{MAGENTA}\n\nSIZE: {w}x{h} px" + (" (whole canvas holding all the pieces listed above)." if id_ in MULTI else "."); neg = NEG_SPRITE
    return (f"{STYLE}\n\nSUBJECT ({id_} – {name}): {body}", neg)


# ------------------------------------------------------------------ workbook
FONT = 'Arial'
wb = Workbook()
H1 = Font(name=FONT, bold=True, size=14, color='FFFFFF'); HB = Font(name=FONT, bold=True, color='FFFFFF'); N = Font(name=FONT, size=10); B = Font(name=FONT, bold=True, size=10)
INPUT = Font(name=FONT, size=10, color='0000FF')
HEAD = PatternFill('solid', fgColor='2B3249'); TITLE = PatternFill('solid', fgColor='1C2036'); YEL = PatternFill('solid', fgColor='FFFF00')
thin = Side(style='thin', color='B0B4C0'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical='top')
CATFILL = {'Wall kit': 'FFF2B3', 'Floors': 'FFF8D6', 'Towers': 'D6E8FF', 'Gatehouse': 'FFDCC8', 'Palace': 'F6D6F6', 'Staircase': 'EDEDED',
           'Buildings': 'D8F5DD', 'Props': 'FFE0EA', 'Effects': 'D4F7F7', 'Terrain': 'EADCCB', 'Masks': 'E0E0E0'}

# --- Read Me
ws = wb.active; ws.title = 'Read Me'
ws.column_dimensions['A'].width = 4; ws.column_dimensions['B'].width = 30; ws.column_dimensions['C'].width = 120
ws['B2'] = 'Grand Castle Island – asset generation prompts'; ws['B2'].font = Font(name=FONT, bold=True, size=16)
rows = [
 ('What this is', 'One ready-to-paste image-generation prompt per asset ID in docs/ASSET_REQUIREMENTS.md. Each prompt in the Prompts sheet is complete on its own (style + subject + camera + background + size): copy column "Full prompt" and, if your tool supports it, column "Negative prompt".'),
 ('Where it goes', 'Column "Grid cells" refers to docs/asset_map (plan grid: columns A–AV, rows 1–32, 32 px cells). Crop docs/asset_map/asset_map_grid_only.png at those cells and attach it as a reference image when your tool allows.'),
 ('Background', 'Every sprite is generated on SOLID FLAT MAGENTA #FF00FF. I remove the magenta automatically. Tileable textures (Kind = tile / tilex) have NO background: they fill the whole canvas.'),
 ('No tilt / rotation', 'Every prompt locks the camera straight-on: vertical edges vertical, base horizontal, symmetric, no isometric or angled views. Reject any image that is tilted, rotated or shows an angled side; regenerate it.'),
 ('Size', 'AI tools rarely output exact pixel sizes. Generate at the aspect ratio shown (column "Aspect W:H") and at the "Generate at" size or larger; I resize to the exact final size and snap it to the pixel grid. Do not resize or crop yourself.'),
 ('Animations', 'Kind = strip: all frames in ONE horizontal row, equal cells, object fixed in place. If your tool cannot do sheets, generate frame 1, then the others with the same seed / image reference.'),
 ('File names', 'Save exactly as column "Output file name" into assets/castle_hd/<Category>/. Keep the ID at the start of the name.'),
 ('Order', 'Work by Priority (1 first). Priority 1 = wall kit, used by every wall in the castle.'),
 ('Colours', 'Column "Colours (hex)" lists the exact colours for each asset, and the same list is written into its prompt. The Palette sheet shows every colour as a swatch. Magenta #FF00FF is only the background, never part of an asset.'),
 ('Your inputs', 'Only edit the blue cells in columns "Status" and "Notes" (Prompts sheet). Status: To do → Generated → Approved / Redo. Row 2 (T1) shows an example entry.'),
 ('After generating', 'Check every image with the QA Checklist sheet before sending. Upload the files; I key out the magenta, check size and alignment against the plan, and place them.'),
]
for i, (k, v) in enumerate(rows):
    ws.cell(4 + i, 2, k).font = B; c = ws.cell(4 + i, 3, v); c.font = N; c.alignment = WRAP
    ws.row_dimensions[4 + i].height = 46
for i in range(len(rows)):
    for col in (2, 3): ws.cell(4 + i, col).border = BOX
ws['B17'] = 'Totals'; ws['B17'].font = B
ws['B18'] = 'Assets in the list'; ws['C18'] = f"=COUNTA(Prompts!B2:B{len(A)+1})"
ws['B19'] = 'Approved'; ws['C19'] = f'=COUNTIF(Prompts!T2:T{len(A)+1},"Approved")'
ws['B20'] = 'Still to do'; ws['C20'] = f'=COUNTIF(Prompts!T2:T{len(A)+1},"To do")'
for r in (18, 19, 20):
    ws.cell(r, 2).font = N; ws.cell(r, 3).font = N; ws.cell(r, 3).alignment = Alignment(horizontal='left')

# --- Prompts
ps = wb.create_sheet('Prompts')
cols = ['#', 'ID', 'Asset', 'Category', 'Priority', 'Final width (px) – whole canvas', 'Final height (px)', 'Aspect W:H', 'Generate at (long side ≥ 2048)',
        'Frames', 'FPS', 'Kind', 'Background', 'Grid cells (asset map)', 'Uses in castle', 'Colours (hex)', 'Full prompt (copy this)', 'Negative prompt',
        'Acceptance check', 'Status', 'Output file name', 'Notes']
widths = [5, 7, 30, 12, 8, 10, 10, 10, 18, 7, 6, 8, 16, 26, 9, 48, 110, 60, 34, 12, 34, 30]
for i, (h, w) in enumerate(zip(cols, widths), 1):
    c = ps.cell(1, i, h); c.font = HB; c.fill = HEAD; c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center'); c.border = BOX
    ps.column_dimensions[c.column_letter].width = w
ps.row_dimensions[1].height = 34
for n, r in enumerate(A, 1):
    id_, name, cat, pri, w, h, fr, fps, kind, subj, acc = r
    full, neg = prompt(r); row = n + 1
    sheet_w = f'=F{row}*J{row}'
    bg = {'tile': 'None (seamless, full canvas)', 'tilex': 'None (seamless strip)', 'script': '—'}.get(kind, 'Magenta #FF00FF')
    fname = '' if kind == 'script' else f"{id_}_{name.split('(')[0].strip().lower().replace(' / ', '_').replace(' ', '_').replace(',', '').replace('-', '_')}.png"
    vals = [n, id_, name, cat, pri, w, h, None, None, fr, fps or None, kind, bg, ', '.join(cells.get(id_, [])) or '—', uses.get(id_, 0) or None,
            CLR.get(id_, ''), full, neg, acc, 'To do', fname, None]
    for i, v in enumerate(vals, 1):
        c = ps.cell(row, i, v); c.font = N; c.alignment = WRAP; c.border = BOX
    # formulas: aspect ratio of the whole image (sheet width for strips), generation size on the long side
    ps.cell(row, 8, f'=TEXT(F{row}*J{row}/G{row},"0.00")&":1"')
    ps.cell(row, 9, f'=IF(F{row}*J{row}>=G{row},MAX(2048,F{row}*J{row})&" x "&ROUND(MAX(2048,F{row}*J{row})*G{row}/(F{row}*J{row}),0),ROUND(MAX(2048,G{row})*F{row}*J{row}/G{row},0)&" x "&MAX(2048,G{row}))')
    ps.cell(row, 4).fill = PatternFill('solid', fgColor=CATFILL.get(cat, 'FFFFFF'))
    ps.cell(row, 2).font = B
    for col in (20, 22): ps.cell(row, col).font = INPUT
    ps.row_dimensions[row].height = 230 if kind != 'script' else 30
last = len(A) + 1
ps.cell(2, 22, 'Example: generated in 2 tries; variant B picked').font = INPUT
ps.cell(2, 20).comment = Comment('Your input: set Status per asset (To do / Generated / Approved / Redo).', 'Claude')
dv = DataValidation(type='list', formula1='"To do,Generated,Approved,Redo"', allow_blank=True); ps.add_data_validation(dv); dv.add(f'T2:T{last}')
ps.conditional_formatting.add(f'T2:T{last}', FormulaRule(formula=['T2="Approved"'], fill=PatternFill('solid', fgColor='C6EFCE')))
ps.conditional_formatting.add(f'T2:T{last}', FormulaRule(formula=['T2="Redo"'], fill=PatternFill('solid', fgColor='FFC7CE')))
ps.conditional_formatting.add(f'T2:T{last}', FormulaRule(formula=['T2="Generated"'], fill=PatternFill('solid', fgColor='FFEB9C')))
ps.freeze_panes = 'C2'; ps.auto_filter.ref = f'A1:V{last}'
ps.cell(last + 2, 2, 'Blue cells (Status, Notes) are yours to edit. Aspect and Generate-at are formulas from the final size × frames. All other columns come from docs/ASSET_REQUIREMENTS.md and docs/ASSET_MAP.md.').font = Font(name=FONT, italic=True, size=9)

# --- Style block
ss = wb.create_sheet('Style Block'); ss.column_dimensions['A'].width = 26; ss.column_dimensions['B'].width = 140
for i, (k, v) in enumerate([('Shared style (in every prompt)', STYLE), ('Camera lock – no tilt (sprites)', STRAIGHT), ('Magenta background (sprites)', MAGENTA),
                             ('Seamless tile (textures)', TILE), ('Seamless strip (X only)', TILE_X), ('Animation sheet', STRIP.format(n='N', w='W', h='H')),
                             ('Negative prompt – sprites', NEG_SPRITE), ('Negative prompt – textures', NEG_TILE)], 1):
    a_ = ss.cell(i, 1, k); a_.font = B; a_.alignment = WRAP; a_.border = BOX
    b_ = ss.cell(i, 2, v); b_.font = N; b_.alignment = WRAP; b_.border = BOX; ss.row_dimensions[i].height = 75

# --- Palette
pl = wb.create_sheet('Palette')
for i, h in enumerate(['Use', 'Hex', 'Swatch'], 1):
    c = pl.cell(1, i, h); c.font = HB; c.fill = HEAD
pl.column_dimensions['A'].width = 30; pl.column_dimensions['B'].width = 12; pl.column_dimensions['C'].width = 14
PAL = [('Stone darkest', '151A30'), ('Stone dark', '3C3E52'), ('Stone mid-dark', '595768'), ('Stone mid', '706B77'), ('Stone mid-light', '887F86'),
       ('Stone light', 'A69A96'), ('Stone highlight', 'DCCABB'), ('Roof blue dark', '1F2F5A'), ('Roof blue mid', '486F91'), ('Roof blue light', '8FB0D0'),
       ('Banner red dark', '7E1A39'), ('Banner red', 'B64E3F'), ('Gold trim', 'E0B040'), ('Wood dark', '4A2E1E'), ('Wood light', '8A5A36'),
       ('Window glow', 'FFD27A'), ('Window glow core', 'FFF3C4'), ('Water deep', '033361'), ('Water mid', '045282'), ('Water highlight', '5FC6FF'),
       ('Courtyard cobble', 'B5A49F'), ('Dirt yard', 'C2A48A'), ('Lawn', '4F7F3F'), ('Background key (sprites only)', 'FF00FF')]
for i, (u, h) in enumerate(PAL, 2):
    pl.cell(i, 1, u).font = N; pl.cell(i, 2, '#' + h).font = N; pl.cell(i, 3).fill = PatternFill('solid', fgColor=h)
pl.cell(len(PAL) + 3, 1, 'Sampled from docs/reference/castle_reference.png. Magenta is only for the background, never inside an asset.').font = Font(name=FONT, italic=True, size=9)

# --- QA
qa = wb.create_sheet('QA Checklist'); qa.column_dimensions['A'].width = 5; qa.column_dimensions['B'].width = 110; qa.column_dimensions['C'].width = 16
for i, h in enumerate(['#', 'Check every generated image before sending', 'Applies to'], 1):
    c = qa.cell(1, i, h); c.font = HB; c.fill = HEAD
QA = [('Straight-on: vertical edges are vertical, the base is horizontal, nothing is tilted or rotated', 'All'),
      ('No angled side faces, no isometric look, no perspective (lines do not converge)', 'All'),
      ('Symmetric left/right where the prompt says symmetric (fold it in half mentally)', 'Sprites'),
      ('Background is one flat magenta #FF00FF everywhere outside the object: no gradient, shadow, floor or glow', 'Sprites'),
      ('No pink, magenta or purple pixels inside the object', 'Sprites'),
      ('Object fully inside the canvas with a magenta margin on every side; base at the bottom, centred', 'Sprites'),
      ('Aspect ratio matches column "Aspect W:H"', 'All'),
      ('Crisp pixel art: hard edges, no blur, no painterly strokes, no noise or JPEG artifacts', 'All'),
      ('Light from the upper left; right side in shade', 'All'),
      ('Colours within the Palette sheet (grey-blue stone, blue roofs, crimson + gold)', 'All'),
      ('Tiles: place 2 copies side by side (and above/below for full tiles): no visible seam', 'Textures'),
      ('Animation: correct frame count in ONE row, equal cells, object does not drift between frames, loops smoothly', 'Animations'),
      ('Counts are exact (e.g. 6 merlons, 9 / 11 steps, 3 arches)', 'Where stated'),
      ('Saved as PNG with the exact name from "Output file name"', 'All')]
for i, (t, ap) in enumerate(QA, 2):
    qa.cell(i, 1, i - 1).font = N; c = qa.cell(i, 2, t); c.font = N; c.alignment = WRAP; qa.cell(i, 3, ap).font = N
    for col in (1, 2, 3): qa.cell(i, col).border = BOX

out = os.path.join(ROOT, 'docs/prompts/castle_asset_prompts.xlsx'); wb.save(out); print(out, len(A), 'assets')
