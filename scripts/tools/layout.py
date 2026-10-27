# Reference-image coordinates (1536x1024). World = x8.
W=1536
def mirror(poly): return [(W-x,y) for x,y in reversed(poly)]
LAND=[  # outer land (grass). Extends past the reference edges so the world has no hard border.
 ('TopForest',[(-500,-450),(1250,-450),(1250,0),(1230,40),(1175,70),(1100,62),(400,62),(330,95),(260,120),(170,112),(110,125),(55,160),(0,170),(-500,178)]),
 ('TownShore',[(1395,-450),(2036,-450),(2036,222),(1560,222),(1500,212),(1455,170),(1425,112),(1405,50)]),
 ('WestShore',[(-500,250),(0,255),(38,262),(52,320),(40,400),(0,420),(-500,426)]),
 ('EastShore',[(2036,248),(1536,250),(1505,262),(1488,330),(1500,420),(1536,440),(2036,444)]),
 ('SouthWestShore',[(-500,604),(0,610),(60,628),(110,670),(140,730),(130,790),(105,850),(150,920),(205,960),(300,975),(450,985),(600,990),(690,1000),(700,1035),(768,1035),(768,1500),(-500,1500)]),
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

# ---- Middle ring buildings (world px). West side listed; mirror flag mirrors to east.
BUILDINGS = [  # (part, x, y, scale, flip)
 ('Cathedral', 3550, 4450, 1.5, False),
 ('Chapel', 3950, 2780, 0.8, False),
 ('DomedHall', 12060, 3150, 1.4, False),
 ('Manor', 11650, 4560, 1.1, False),
 ('FountainPlaza', 7680, 4420, 1.6, False),
]
AVENUE_PLANTERS = [(7680 - 600, 5980), (7680 + 600, 5980)]
AVENUE_LANTERNS = [(7680 - 330, 4950), (7680 + 330, 4950), (7680 - 330, 5600), (7680 + 330, 5600)]
CYPRESS_COLS = [6230, 6600, 6970]            # west avenue lawn; mirrored east
CYPRESS_ROWS = list(range(3720, 5500, 330))
TREE_EXCLUDE = [  # world rects (x0, y0, x1, y1) kept free of scattered trees
 (2900, 2850, 4200, 4750), (3600, 1900, 4300, 2950),        # cathedral, chapel
 (11300, 1850, 12800, 3350), (10850, 3500, 12450, 4800),    # domed hall, manor
 (4700, 1500, 5500, 2400), (9860, 1500, 10660, 2400),       # palace corner towers
 (5350, 2900, 5850, 3450), (9510, 2900, 10010, 3450),       # terrace towers
 (3300, 4450, 3800, 4900), (11400, 4550, 11900, 4900),                                  # cathedral doorstep
]

# ---- Market (west yard) and training yard (east yard): (part, folder, x, y, flip)
MARKET = [
 ('Stall1','market',2420,5150,False),('Stall2','market',2800,5150,False),('Stall3','market',3180,5150,False),('Stall4','market',3560,5150,False),('Stall5','market',3940,5150,False),
 ('Stall6','market',2960,5620,False),('Stall7','market',3340,5620,False),('Stall8','market',3720,5620,False),('Stall10','market',4100,5620,False),
 ('MarketTent','market',2330,5560,False),('Parasol','market',2200,5250,False),
 ('CoveredWagon','market',3100,5940,False),('HayCart','market',3420,5990,True),('BarrelCart','market',3820,5990,False),('CrateStack','market',4180,5960,False),
 ('Crate','market',2610,5180,False),('Barrel','market',2990,5185,False),('AppleCrate','market',3370,5185,False),('Sacks','market',3750,5175,False),
 ('BarrelStack','market',4180,5180,False),('Baskets','market',3150,5650,False),('HayBales','market',3530,5660,False),('BarrelPile','market',3910,5650,False),
 ('HangingLantern','market',2240,4920,False),('HangingLantern','market',4280,4900,True),('ScaleStand','market',2700,5600,False),
 ('FishRack','market',4300,5300,False),('MeatRack','market',2150,5000,False),
]
TRAINING = [
 ('WeaponRackSwords','training',11300,4960,False),('WeaponRackAxes','training',11650,4960,False),('WeaponRackBows','training',12000,4960,False),
 ('WeaponRackSpears','training',12350,4960,False),('WeaponRackMaces','training',12700,4960,False),('ShieldRack','training',13000,4980,False),
 ('TrainingBanner','training',11100,5000,False),('BannerStand','training',13200,5100,False),
 ('Dummy','training',11550,5380,False),('Dummy','training',11900,5380,True),('Dummy','training',12250,5380,False),('Dummy','training',12600,5380,True),
 ('Dummy','training',11550,5780,True),('Dummy','training',11900,5780,False),('Dummy','training',12150,5720,True),('Dummy','training',12600,5780,False),
 ('ArmorStand','training',12950,5350,False),('ArmorStandBlue','training',13150,5420,False),('ArmorStandGold','training',12950,5580,True),
 ('ArmoryStall','training',11300,5990,False),('WeaponChest','training',11720,5990,False),('WeaponBarrels','training',12080,5990,False),
 ('MarketTent','market',12300,5900,True),('HayBales','market',13100,5560,False),('Barrel','market',11200,5600,False),('CrateStack','market',11250,5800,False),
]


# ---- Outer world (world px)
WORLD_RECT = (-7000, -6500, 22400, 17000)     # water polygon
CAMERA_LIMITS = (-4300, -4100, 19660, 14300)  # left, top, right, bottom
TOWN_BRIDGE = (12950, 14430, 1380)            # x_from, x_to, base_y
TOWN_ROADS = [
 [(14300, 1180), (15200, 1150), (16600, 1150), (18200, 1200), (19800, 1250)],
 [(16600, 1150), (16620, 200), (16600, -950), (16640, -2600), (16500, -4400)],
 [(14700, -950), (15600, -980), (16600, -950), (17700, -920), (19800, -960)],
]
TOWN_SQUARE = (16600, -950, 700)               # centre x, y, radius
TOWN_ROWS = [-2300, -1200, -170, 950]          # house base lines
TOWN_X = (14850, 19500, 860)                   # first x, last x, spacing
PATHS = [  # dirt paths through the countryside
 [(7680, 10250), (7700, 11200), (7300, 12300), (6400, 13300), (5800, 14800)],
 [(7600, 11400), (9000, 11900), (11200, 12300), (13800, 12500), (16500, 12900), (20000, 13100)],
 [(7500, 11600), (5600, 11950), (3400, 12000), (1200, 11600), (-1200, 11900), (-4600, 11700)],
 [(2600, 700), (1300, -300), (-200, -900), (-2200, -1300), (-4600, -1500)],
 [(6500, 300), (6200, -1200), (5200, -2600), (5400, -4600)],
 [(10200, 300), (10500, -1500), (11800, -2800), (12000, -4600)],
]
STREAM = [(300, 1700), (150, 1000), (-300, 200), (-500, -900), (-1300, -2000), (-1500, -3200), (-2600, -4600)]
STREAM_FALL = (380, 2010)
FOREST_STEP = 270
FOREST_EXCLUDE = [  # world rects kept clear of forest
 (14000, -4600, 20500, 1900),   # town (gets its own sparse trees)
 (-200, 1300, 1000, 2100),      # waterfall lip
]
