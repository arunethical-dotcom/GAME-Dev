"""
Castle blueprint, traced from docs/reference/castle_reference.png on a 32 px grid.

All coordinates are REFERENCE-IMAGE PIXELS in screen space (x right, y down), as seen in
the 3/4 view. World px = ref px * 10.  Only the WEST half is listed; the castle is mirrored
about x = 768 (the causeway axis).

TERRACE  : a raised level. `top` is the outline of its top surface as seen on screen.
           Every edge whose outward normal faces the camera gets a vertical stone face that
           hangs `drop` px down to the level below. All edges get a crenellated parapet unless
           listed in `open_edges` (indices of edges with no parapet, e.g. where stairs or
           another terrace continue).
WALL     : a free-standing wall (barbican, links between towers): a thin terrace whose top is
           the walkway, centred on `line`, `thick` px deep.
BRIDGE   : like WALL but the face uses the arched bridge texture.
TOWER    : (kind, x, base_y, scale). base_y = where the tower meets the ground / water.
"""
AXIS = 768

def mirror_pt(p):
    return (2 * AXIS - p[0], p[1])

# ---------------------------------------------------------------- terraces
# heights (drop) measured from the plan: face top -> face bottom
TERRACES = [
    dict(name="LowerWard", level=1, drop=66, floor="cobble",
         # the main island inside the curtain wall; mirrored + joined at the axis
         top=[(768, 100), (352, 100), (262, 160), (214, 226), (214, 420), (172, 444),
              (172, 548), (258, 592), (298, 612), (404, 612), (474, 638), (768, 638)]),
    dict(name="CathedralTerrace", level=2, drop=22, floor="grass",
         top=[(236, 232), (300, 232), (440, 232), (470, 300), (520, 400), (430, 466),
              (282, 466), (236, 440)]),
    dict(name="InnerGarden", level=2, drop=18, floor="grass",
         top=[(602, 410), (690, 410), (690, 498), (602, 498)]),
    dict(name="SouthGarden", level=2, drop=16, floor="grass",
         top=[(452, 536), (636, 536), (636, 586), (470, 586)]),
    dict(name="PalaceTerrace", level=3, drop=30, floor="cobble_light",
         top=[(768, 100), (440, 100), (440, 206), (548, 214), (580, 300), (706, 300), (768, 300)],
         open_edges=[5, 6]),   # stair opening at the front centre
]

# ---------------------------------------------------------------- free-standing walls
WALLS = [
    # outer barbican (south): one continuous wall per side. `drops` = face height at each vertex
    # (the wall stands on rocks nearer the gate, so its visible face gets shorter).
    dict(name="Barbican", line=[(150, 800), (295, 800), (395, 860), (503, 864), (712, 868)],
         drops=[62, 62, 58, 46, 40], thick=16),
    # north-west flank: wall from the corner tower to the palace back wall
    dict(name="NorthWestLink", line=[(236, 168), (352, 112)], drops=[60, 60], thick=18),
]
BRIDGES = [  # one stone arch per ~100 px of span
    dict(name="FlankBridgeLower", line=[(70, 528), (172, 528)], thick=24, drop=70),
    dict(name="FlankBridgeUpper", line=[(96, 326), (214, 326)], thick=24, drop=62),
    dict(name="FlankBridgeTop", line=[(140, 196), (236, 180)], thick=22, drop=50),
]

# ---------------------------------------------------------------- towers
# kind: "blue" (round, blue cone roof, banner) | "flat" (barbican, crenellated top)
#       "gate" (blue roof + pennant) | "big" (large blue tower)
TOWERS = [
    ("big",  57, 624, 1.35), ("blue", 80, 400, 1.0), ("blue", 123, 296, 0.95), ("blue", 236, 222, 1.0),
    ("blue", 178, 590, 0.95), ("blue", 277, 694, 1.0), ("big", 438, 795, 1.35),
    ("blue", 603, 728, 1.0), ("blue", 690, 705, 1.0),
    ("flat", 150, 862, 1.0), ("flat", 295, 880, 1.0), ("flat", 395, 935, 1.0), ("flat", 503, 942, 1.05),
    ("gate", 640, 960, 1.05),
    ("blue", 355, 150, 1.0), ("blue", 455, 400, 0.85), ("blue", 563, 402, 0.85), ("pillar", 688, 342, 0.6),
    ("blue", 470, 598, 0.8), ("blue", 600, 598, 0.8),
    ("blue", 497, 486, 0.6), ("blue", 593, 486, 0.6),
]

# ---------------------------------------------------------------- set pieces
GATEHOUSE = (768, 706)                  # base centre of the main gatehouse
CAUSEWAY = (716, 820, 640, 1035)        # x0, x1, y_from, y_to
GRAND_STAIRS = (768, 300, 395)          # centre x, top y, bottom y
FOUNTAIN = (768, 448)
PALACE = (768, 225)
BUILDINGS = [("Cathedral", 340, 440), ("Chapel", 380, 236), ("DomedHall", 1192, 300), ("Manor", 1170, 445)]

# red banners hanging on the curtain wall face (x positions, west half; mirrored)
CURTAIN_BANNERS = [222, 383, 530]          # measured from the plan (red blobs on the wall faces)
BARBICAN_BANNERS = [338]

# ---------------------------------------------------------------- details (pass 2, from the 50% overlay)
STAIRS_UPPER = dict(x=768, top=228, base=276, half_w=33)     # plain flight, palace door -> landing
STAIRS_LOWER = dict(x=768, top=300, base=360, half_w=33)     # carpeted flight, landing -> plaza
GARGOYLES = [(688, 288)]                                    # on top of the square pillar towers
STAIR_KNIGHTS = [(720, 386)]
COLONNADES = [dict(line=[(507, 470), (586, 470)], drop=38, arches=3)]
POOLS = [[(505, 482), (560, 482), (560, 512), (505, 512)]]
YARDS = [[(230, 494), (402, 482), (424, 590), (262, 590)]]     # dirt floor: market (west), training yard (mirrored)
ROCKS = [  # rocky outcrops under the barbican (plan px), get cliff faces automatically
    [(112, 852), (192, 858), (198, 900), (188, 945), (150, 972), (110, 940)],   # left of the barbican waterfall: the fall drops into open water (plan)
    [(330, 902), (470, 900), (505, 925), (470, 948), (345, 946), (322, 925)],
]
BARBICAN_FALLS = [dict(x=228, base=946, sluice_y=(842, 862), arches=3, width=56)]
GATE_LANDING = dict(knight=(690, 934), lantern=(692, 996), block=[(664, 892), (716, 892), (716, 1002), (664, 1002)], drop=34)

# ---------------------------------------------------------------- Surendar batch placements (west half; mirrored)
ROCK_SPRITES = [(152, 925, True), (128, 968, False), (415, 948, True), (480, 950, False)]
WALL_TORCHES = [(722, 318), (458, 634), (300, 618)]       # palace terrace by the stairs, curtain wall faces
SEAGULLS = [(330, 750), (1200, 760), (560, 800), (1000, 690), (140, 560)]   # centres of their flight loops (both halves)
