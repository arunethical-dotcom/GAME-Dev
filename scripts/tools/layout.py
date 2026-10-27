# Reference-image coordinates (1536x1024). World = x8.
W=1536
def mirror(poly): return [(W-x,y) for x,y in reversed(poly)]
LAND=[  # outer forest / shore land (grass)
 ('TopForest',[(0,0),(1250,0),(1230,40),(1175,70),(1100,62),(400,62),(330,95),(260,120),(170,112),(110,125),(55,160),(0,170)]),
 ('TownShore',[(1290,0),(1536,0),(1536,215),(1490,210),(1440,175),(1390,150),(1345,118),(1300,60)]),
 ('WestShore',[(0,255),(38,262),(52,320),(40,400),(0,420)]),
 ('EastShore',[(1536,250),(1505,262),(1488,330),(1500,420),(1536,440)]),
 ('SouthWestShore',[(0,610),(60,628),(110,670),(140,730),(130,790),(105,850),(150,920),(205,960),(300,975),(450,985),(600,990),(690,1000),(700,1024),(0,1024)]),
]
LAND.append(('SouthEastShore',mirror(LAND[-1][1])))
CASTLE=[  # castle island foundation (flagstone)
 ('CastleIsland',[(230,62),(1306,62),(1290,160),(1350,240),(1346,420),(1436,430),(1470,470),(1470,600),(1464,600),(1464,619.5),(1266,619.5),(1266,661.5),(1096,661.5),(1096,694.5),(803,694.5),(803,701.5),(733,701.5),(733,694.5),(440,694.5),(440,661.5),(270,661.5),(270,619.5),(72,619.5),(72,600),(66,600),(66,470),(100,430),(190,420),(186,240),(246,160)]),
 ('Causeway',[(700,700),(836,700),(836,1024),(700,1024)]),
]
GARDEN_L=[
 ('CathedralLawn',[(250,160),(540,150),(585,230),(560,455),(330,470),(205,430),(190,320)]),
 ('AvenueGardenWest',[(595,330),(718,330),(718,560),(610,560)]),
]
GARDEN=GARDEN_L+[(n.replace('West','East').replace('Cathedral','DomedHall'),mirror(p)) for n,p in GARDEN_L]
DIRT=[('MarketYard',[(205,480),(420,470),(440,600),(225,615)])]
DIRT.append(('TrainingYard',mirror(DIRT[0][1])))

# ---- Curtain wall (world px). Mirror: x' = 15360 - x
WORLD_W=15360
GATE=(7680,7030)
WALLS=[  # (x_from, x_to, base_y, tile_offset)
 (4400,7240,6960,0),(960,2700,6210,90),(2700,4400,6630,170)]
TOWERS=[  # (x, base_y, in_water)
 (6000,6985,True),(4400,7010,True),(2700,6660,True),(960,6240,True)]

# ---- Outer barbican (world px, west half; mirrored for east)
ROAD_L, ROAD_R = 7446, 7914          # causeway edges
APRON = [(6850, 9170), (8510, 9170), (8510, 9520), (6850, 9520)]   # stone landing at the barbican gate
BARB_WALLS = [  # (x_from, x_to, base_y, banner_at or None)
 (1350, 2700, 8600, None), (2700, 4150, 8900, 0.5), (4150, 5600, 9200, None),
 (5600, 7080, 9250, 0.55), (7080, ROAD_L, 9250, None)]
BARB_TOWERS = [(1350, 8630), (2700, 8930), (4150, 9230), (5600, 9280)]
GATE_TOWER = (7080, 9335)
WATERFALLS = [(2025, 9175)]   # base centre of the wide waterfall under the first wall
ISLETS = [(3700, 9760, False)]
STATUE = (7372, 9430)
LANTERNS = [(ROAD_L + 40, 9515)]
BRAZIER_X = ROAD_L + 46
BRAZIER_Y = [7480, 8040, 8600, 9900]

# ---- Side flanks (world px, west half; mirrored for east)
FLANK_TOWERS = [  # (x, base_y, in_water)
 (900, 4180, True), (860, 2780, True), (2250, 2050, False), (1950, 5050, False)]
FLANK_BRIDGES = [  # (x_from, x_to, base_y)
 (1030, 1900, 4110), (990, 1890, 2710)]

# ---- Palace and grand staircase (world px)
PALACE = (7680, 2250)
TERRACE_Y = 3250                       # base of the terrace retaining wall / bottom of the stairs
TERRACE_WALLS = [(5600, 7152), (8208, 9760)]
TERRACE_TOWERS = [(5600, 3280), (9760, 3280)]
PALACE_Y_NOTE = 'keep scaled 1.55x so it rises above the wings'
STAIRS = (7680, 3250)
GARGOYLES = [(7060, 2700), (8300, 2700)]
STAIR_KNIGHTS = [(7070, 3360), (8290, 3360)]
STAIR_LANTERNS = [(6930, 3380), (8430, 3380)]
