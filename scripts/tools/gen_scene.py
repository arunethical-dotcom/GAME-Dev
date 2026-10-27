# Generates scenes/castle/Castle.tscn from layout.py. Run: python3 scripts/tools/gen_scene.py
# Coordinates in layout.py are reference-image px (x10 = world px) unless noted.
import sys; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from layout import *
K=10  # reference px -> world px  (map = 15360 x 10240)
import math, random
def organic(poly, step=14, amp=7.0, seed=1, closed_shape=True):
    # subdivide, displace along the normal with smooth noise, then Chaikin-smooth
    rnd=random.Random(seed); pts=[]
    P=poly+([poly[0]] if closed_shape else [])
    for (x0,y0),(x1,y1) in zip(P,P[1:]):
        L=math.hypot(x1-x0,y1-y0); n=max(1,int(L/step))
        for i in range(n): t=i/n; pts.append((x0+(x1-x0)*t,y0+(y1-y0)*t))
    N=len(pts); ph=[rnd.uniform(0,6.28) for _ in range(3)]
    out=[]
    for i,(x,y) in enumerate(pts):
        xa,ya=pts[i-1]; xb,yb=pts[(i+1)%N]; dx,dy=xb-xa,yb-ya; L=math.hypot(dx,dy) or 1
        nx,ny=-dy/L,dx/L
        # world-position based noise so mirrored shapes don't look identical
        d=amp*(0.6*math.sin(x*0.045+ph[0])*math.cos(y*0.038+ph[1])+0.4*math.sin((x+y)*0.11+ph[2]))
        out.append((x+nx*d,y+ny*d))
    for _ in range(2):
        q=[]
        for i in range(len(out)):
            (ax,ay),(bx,by)=out[i],out[(i+1)%len(out)]
            q+= [(0.75*ax+0.25*bx,0.75*ay+0.25*by),(0.25*ax+0.75*bx,0.25*ay+0.75*by)]
        out=q
    return out
def pv(poly): return 'PackedVector2Array('+', '.join(f'{x*K}, {y*K}' for x,y in poly)+')'
def closed(poly): return pv(poly+[poly[0]])
ext=[('Texture2D','res://docs/reference/castle_reference.png','ref'),('Script','res://scripts/debug_camera.gd','cam'),
     ('Shader','res://shaders/water.gdshader','sh_water'),('Shader','res://shaders/terrain.gdshader','sh_terrain'),('Shader','res://shaders/shore_foam.gdshader','sh_foam'),
     ('Texture2D','res://assets/tilesets/water/deep_water.png','t_water'),('Texture2D','res://assets/tilesets/terrain/meadow_grass.png','t_grass'),
     ('Texture2D','res://assets/tilesets/terrain/dirt_gravel.png','t_dirt'),('Texture2D','res://assets/tilesets/floors/flagstone.png','t_flag'),('Texture2D','res://assets/tilesets/floors/causeway_road.png','t_road'),('PackedScene','res://scenes/castle/parts/Tower.tscn','p_tower'),('PackedScene','res://scenes/castle/parts/Gatehouse.tscn','p_gate'),('PackedScene','res://scenes/castle/parts/CurtainWall.tscn','p_wall'),('PackedScene','res://scenes/castle/parts/BarbicanTower.tscn','p_btower'),('PackedScene','res://scenes/castle/parts/GateTower.tscn','p_gtower'),('PackedScene','res://scenes/castle/parts/WideWaterfall.tscn','p_fall'),('PackedScene','res://scenes/castle/parts/KnightStatue.tscn','p_statue'),('PackedScene','res://scenes/castle/parts/LanternPillar.tscn','p_lantern'),('PackedScene','res://scenes/castle/parts/Brazier.tscn','p_brazier'),('PackedScene','res://scenes/castle/parts/Islet.tscn','p_islet'),('Texture2D','res://assets/sprites/walls/barbican_wall_tile.png','t_bwall'),('Material','res://resources/shore_foam_material.tres','m_foam_res'),('Texture2D','res://assets/sprites/walls/arched_bridge_tile.png','t_bridge'),('Texture2D','res://assets/tilesets/terrain/cliff_face_strip.png','t_cliff'),('PackedScene','res://scenes/castle/parts/Palace.tscn','p_palace'),('PackedScene','res://scenes/castle/parts/GrandStairs.tscn','p_stairs'),('PackedScene','res://scenes/castle/parts/Gargoyle.tscn','p_garg'),('PackedScene','res://scenes/castle/parts/KnightStatueTall.tscn','p_knight2')]+[('PackedScene','res://scenes/castle/parts/Cathedral.tscn','p_Cathedral'),('PackedScene','res://scenes/castle/parts/Chapel.tscn','p_Chapel'),('PackedScene','res://scenes/castle/parts/DomedHall.tscn','p_DomedHall'),('PackedScene','res://scenes/castle/parts/Manor.tscn','p_Manor'),('PackedScene','res://scenes/castle/parts/FountainPlaza.tscn','p_FountainPlaza'),('PackedScene','res://scenes/castle/parts/CypressPlanter.tscn','p_CypressPlanter'),('PackedScene','res://scenes/castle/parts/PineA.tscn','p_PineA'),('PackedScene','res://scenes/castle/parts/PineB.tscn','p_PineB'),('PackedScene','res://scenes/castle/parts/PineC.tscn','p_PineC'),('PackedScene','res://scenes/castle/parts/PineD.tscn','p_PineD'),('PackedScene','res://scenes/castle/parts/CypressA.tscn','p_CypressA'),('PackedScene','res://scenes/castle/parts/CypressB.tscn','p_CypressB'),('PackedScene','res://scenes/castle/parts/CypressC.tscn','p_CypressC'),('PackedScene','res://scenes/castle/parts/Bush.tscn','p_Bush'),('PackedScene','res://scenes/castle/parts/BushWhite.tscn','p_BushWhite'),('PackedScene','res://scenes/castle/parts/BushRed.tscn','p_BushRed')]
out=[]
sub=[]
sub.append('[sub_resource type="FastNoiseLite" id="noise"]\nnoise_type = 3\nfrequency = 0.012\nfractal_octaves = 4')
sub.append('[sub_resource type="NoiseTexture2D" id="noise_tex"]\nwidth = 512\nheight = 512\nseamless = true\nnoise = SubResource("noise")')
def mat(id,shader,params):
    s=f'[sub_resource type="ShaderMaterial" id="{id}"]\nshader = ExtResource("{shader}")'
    for k,v in params.items(): s+=f'\nshader_parameter/{k} = {v}'
    sub.append(s)
mat('m_water','sh_water',{'water_tex':'ExtResource("t_water")','noise_tex':'SubResource("noise_tex")','tile_size':'1024.0','pixel_size':'4.0'})
mat('m_grass','sh_terrain',{'albedo':'ExtResource("t_grass")','noise_tex':'SubResource("noise_tex")','tile_size':'1024.0','brightness_variation':'0.09'})
mat('m_garden','sh_terrain',{'albedo':'ExtResource("t_grass")','noise_tex':'SubResource("noise_tex")','tile_size':'768.0','brightness_variation':'0.05','tint':'Color(1.05, 1.08, 0.95, 1)'})
mat('m_dirt','sh_terrain',{'albedo':'ExtResource("t_dirt")','noise_tex':'SubResource("noise_tex")','tile_size':'1024.0','brightness_variation':'0.07'})
mat('m_sand','sh_terrain',{'albedo':'ExtResource("t_dirt")','noise_tex':'SubResource("noise_tex")','tile_size':'900.0','brightness_variation':'0.05','tint':'Color(1.12, 1.06, 0.92, 1)'})
mat('m_grass_edge','sh_terrain',{'albedo':'ExtResource("t_grass")','noise_tex':'SubResource("noise_tex")','tile_size':'1024.0','brightness_variation':'0.09','tint':'Color(0.72, 0.78, 0.7, 1)'})
mat('m_flag','sh_terrain',{'albedo':'ExtResource("t_flag")','noise_tex':'SubResource("noise_tex")','tile_size':'512.0','brightness_variation':'0.07','break_repetition':'0.0','grime_tex':'ExtResource("t_dirt")','grime_amount':'0.35','warm_cool':'Vector3(0.04, 0.02, -0.03)'})
mat('m_foam','sh_foam',{'noise_tex':'SubResource("noise_tex")','pixel_size':'4.0'})
n=[]
n.append('[node name="Castle" type="Node2D"]')
n.append('[node name="Water" type="Polygon2D" parent="."]\nz_index = -100\nmaterial = SubResource("m_water")\npolygon = '+pv([(-200,-200),(1736,-200),(1736,1224),(-200,1224)]))
n.append('[node name="Ground" type="Node2D" parent="."]\nz_index = -90')
n.append('[node name="ShoreFoam" type="Node2D" parent="Ground"]')
LANDO=[(nm,organic(p,seed=i+3)) for i,(nm,p) in enumerate(LAND)]
ISL=organic(CASTLE[0][1],step=10,amp=0.6,seed=99)
for name,p in LANDO+[('CastleIsland',ISL)]:
    n.append(f'[node name="{name}Foam" type="Line2D" parent="Ground/ShoreFoam"]\nmaterial = SubResource("m_foam")\npoints = {closed(p)}\nwidth = 420.0\ntexture_mode = 1\njoint_mode = 0\nsharp_limit = 4.0')
CLIFF_H=440.0
def inside(pt,poly):
    x,y=pt; c=False
    for (x0,y0),(x1,y1) in zip(poly,poly[1:]+poly[:1]):
        if (y0>y)!=(y1>y) and x < x0+(y-y0)*(x1-x0)/(y1-y0): c=not c
    return c
def south_runs(poly,min_len=18):
    N=len(poly); flags=[]
    for i in range(N):
        (x0,y0),(x1,y1)=poly[i],poly[(i+1)%N]; dx,dy=x1-x0,y1-y0; L=math.hypot(dx,dy) or 1
        nx,ny=dy/L,-dx/L; mx,my=(x0+x1)/2,(y0+y1)/2
        if inside((mx+nx*0.8,my+ny*0.8),poly): nx,ny=-nx,-ny
        flags.append(ny>0.45)
    # rotate so we start at a non-flagged edge
    if all(flags): return [poly+[poly[0]]]
    k=flags.index(False); idx=list(range(k,N))+list(range(0,k)); runs=[]; cur=[]
    for i in idx:
        if flags[i]:
            if not cur: cur=[poly[i]]
            cur.append(poly[(i+1)%N])
        elif cur: runs.append(cur); cur=[]
    if cur: runs.append(cur)
    out=[]
    for r in runs:
        if sum(math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(r,r[1:]))>=min_len:
            if r[0][0]>r[-1][0]: r=r[::-1]
            out.append(r)
    return out
CLIFFS=[]
for name,p in LANDO:
    for j,r in enumerate(south_runs(p)):
        CLIFFS.append((f'{name}Cliff{j+1}',[(x*K,y*K) for x,y in r]))
for name,r in CLIFFS:
    base=[(x,y+CLIFF_H-20) for x,y in r]
    n.append(f'[node name="{name}BaseFoam" type="Line2D" parent="Ground/ShoreFoam"]\nmaterial = SubResource("m_foam")\npoints = PackedVector2Array({", ".join(f"{x:.0f}, {y:.0f}" for x,y in base)})\nwidth = 260.0\ntexture_mode = 1\njoint_mode = 2')
n.append('[node name="SandBanks" type="Node2D" parent="Ground"]')
for name,p in LANDO:
    n.append(f'[node name="{name}Bank" type="Line2D" parent="Ground/SandBanks"]\nmaterial = SubResource("m_sand")\npoints = {closed(p)}\nwidth = 110.0\njoint_mode = 0\nsharp_limit = 4.0')
n.append('[node name="Cliffs" type="Node2D" parent="Ground"]')
TEXW,TEXH=311.0,331.0
for name,r in CLIFFS:
    # keep x strictly increasing so every slice faces the camera
    pts=[r[0]]
    for q in r[1:]:
        if q[0]>pts[-1][0]+2: pts.append(q)
    if len(pts)<2: continue
    verts=[]; uvs=[]; polys=[]
    for (x,y) in pts:
        verts+= [(x,y-14),(x,y-14+CLIFF_H)]
        uvs+= [(x*TEXH/CLIFF_H,1.0),(x*TEXH/CLIFF_H,TEXH-4.0)]
    for i in range(len(pts)-1):
        a=2*i; polys.append(f'PackedInt32Array({a}, {a+2}, {a+3}, {a+1})')
    V=", ".join(f"{x:.0f}, {y:.0f}" for x,y in verts); U=", ".join(f"{u:.1f}, {v:.1f}" for u,v in uvs)
    n.append(f'[node name="{name}" type="Polygon2D" parent="Ground/Cliffs"]\ntexture_repeat = 2\ntexture = ExtResource("t_cliff")\npolygon = PackedVector2Array({V})\nuv = PackedVector2Array({U})\npolygons = [{", ".join(polys)}]')
n.append('[node name="Land" type="Node2D" parent="Ground"]')
for name,p in LANDO:
    n.append(f'[node name="{name}" type="Polygon2D" parent="Ground/Land"]\nmaterial = SubResource("m_grass")\npolygon = {pv(p)}')
    n.append(f'[node name="GrassEdge" type="Line2D" parent="Ground/Land/{name}"]\nmaterial = SubResource("m_grass_edge")\npoints = {closed(p)}\nwidth = 36.0\njoint_mode = 0\nsharp_limit = 4.0')
n.append('[node name="CastleGround" type="Node2D" parent="Ground"]')
for name,p in [('CastleIsland',ISL)]:
    n.append(f'[node name="{name}" type="Polygon2D" parent="Ground/CastleGround"]\nmaterial = SubResource("m_flag")\npolygon = {pv(p)}')
def wpv(poly): return 'PackedVector2Array('+', '.join(f'{x}, {y}' for x,y in poly)+')'
for side in 'WE':
    ap=APRON if side=='W' else [(WORLD_W-x,y) for x,y in APRON]
    if side=='E': continue   # apron spans both sides already
    n.append(f'[node name="GateApronFoam" type="Line2D" parent="Ground/ShoreFoam"]\nmaterial = SubResource("m_foam")\npoints = {wpv(ap+[ap[0]])}\nwidth = 300.0\ntexture_mode = 1\njoint_mode = 0\nsharp_limit = 4.0')
    n.append(f'[node name="GateApron" type="Polygon2D" parent="Ground/CastleGround"]\nmaterial = SubResource("m_flag")\npolygon = {wpv(ap)}')
    n.append(f'[node name="GateApronEdge" type="Line2D" parent="Ground/CastleGround"]\npoints = {wpv(ap+[ap[0]])}\nwidth = 16.0\ndefault_color = Color(0.2, 0.22, 0.3, 0.8)\njoint_mode = 0\nsharp_limit = 4.0')
n.append(f'[node name="IslandEdge" type="Line2D" parent="Ground/CastleGround"]\npoints = {closed(ISL)}\nwidth = 16.0\ndefault_color = Color(0.2, 0.22, 0.3, 0.8)\njoint_mode = 0\nsharp_limit = 4.0')
RX,RW=768*K,469; RY0=690*K; RY1=1030*K
for side,x in (('W',RX-RW/2+6),('E',RX+RW/2-6)):
    n.append(f'[node name="CausewayFoam{side}" type="Line2D" parent="Ground/ShoreFoam"]\nmaterial = SubResource("m_foam")\npoints = PackedVector2Array({x}, {RY0}, {x}, {RY1})\nwidth = 300.0\ntexture_mode = 1')
n.append(f'[node name="Causeway" type="Sprite2D" parent="Ground/CastleGround"]\ntexture_repeat = 2\nposition = Vector2({RX-RW/2}, {RY0})\ntexture = ExtResource("t_road")\ncentered = false\nregion_enabled = true\nregion_rect = Rect2(0, 0, {RW}, {RY1-RY0})')
n.append('[node name="Gardens" type="Node2D" parent="Ground"]')
for name,p in GARDEN:
    n.append(f'[node name="{name}" type="Polygon2D" parent="Ground/Gardens"]\nmaterial = SubResource("m_garden")\npolygon = {pv(p)}')
    n.append(f'[node name="Curb" type="Line2D" parent="Ground/Gardens/{name}"]\npoints = {closed(p)}\nwidth = 22.0\ndefault_color = Color(0.62, 0.57, 0.5, 1)\njoint_mode = 0\nsharp_limit = 4.0')
for name,p in DIRT:
    n.append(f'[node name="{name}" type="Polygon2D" parent="Ground/Gardens"]\nmaterial = SubResource("m_dirt")\npolygon = {pv(p)}')
n.append('[node name="YSorted" type="Node2D" parent="."]\ny_sort_enabled = true')
for c in ['Structures','Props','Vegetation']:
    n.append(f'[node name="{c}" type="Node2D" parent="YSorted"]\ny_sort_enabled = true')
n.append('[node name="CurtainWall" type="Node2D" parent="YSorted/Structures"]\ny_sort_enabled = true')
gx,gy=GATE
n.append(f'[node name="Gatehouse" parent="YSorted/Structures/CurtainWall" instance=ExtResource("p_gate")]\nposition = Vector2({gx}, {gy})')
k=0
for x0,x1,y,off in WALLS:
    for side in 'WE':
        k+=1
        a,b=(x0,x1) if side=='W' else (WORLD_W-x1,WORLD_W-x0)
        if side=='E' and x1==7240: a=8240  # gatehouse is wider on its east side
        n.append(f'[node name="Wall{k}{side}" parent="YSorted/Structures/CurtainWall" instance=ExtResource("p_wall")]\nposition = Vector2({a}, {y})\nlength = {b-a}.0\ntile_offset = {off+ (37 if side=="E" else 0)}.0\nbanner_start = {260 if side=="W" else 420}.0')
n.append('[node name="Barbican" type="Node2D" parent="YSorted/Structures"]\ny_sort_enabled = true')
M=lambda x: WORLD_W-x
B='YSorted/Structures/Barbican'
for i,(x0,x1,y,ban) in enumerate(BARB_WALLS):
    L=x1-x0
    for side in 'WE':
        a=x0 if side=='W' else M(x1)
        bn=f'banner_spacing = 99999.0\nbanner_start = {round(L*ban)}.0' if ban else 'banner_spacing = 0.0'
        n.append(f'[node name="BWall{i+1}{side}" parent="{B}" instance=ExtResource("p_wall")]\nposition = Vector2({a}, {y})\nwall_tile = ExtResource("t_bwall")\nbanner_top = 120.0\nlength = {L}.0\ntile_offset = {i*61 + (29 if side=="E" else 0)}.0\n{bn}')
for i,(x,y) in enumerate(BARB_TOWERS):
    for side in 'WE':
        n.append(f'[node name="BTower{i+1}{side}" parent="{B}" instance=ExtResource("p_btower")]\nposition = Vector2({x if side=="W" else M(x)}, {y})')
for side in 'WE':
    gx,gy=GATE_TOWER
    n.append(f'[node name="GateTower{side}" parent="{B}" instance=ExtResource("p_gtower")]\nposition = Vector2({gx if side=="W" else M(gx)}, {gy})')
    sx,sy=STATUE
    n.append(f'[node name="KnightStatue{side}" parent="{B}" instance=ExtResource("p_statue")]\nposition = Vector2({sx if side=="W" else M(sx)}, {sy})' + ('\nflip_h = true' if side=='E' else ''))
    for j,(lx,ly) in enumerate(LANTERNS):
        n.append(f'[node name="Lantern{j+1}{side}" parent="{B}" instance=ExtResource("p_lantern")]\nposition = Vector2({lx if side=="W" else M(lx)}, {ly})')
    for j,by in enumerate(BRAZIER_Y):
        n.append(f'[node name="Brazier{j+1}{side}" parent="YSorted/Props" instance=ExtResource("p_brazier")]\nposition = Vector2({BRAZIER_X if side=="W" else M(BRAZIER_X)}, {by})')
    for j,(fx,fy) in enumerate(WATERFALLS):
        n.append(f'[node name="Waterfall{j+1}{side}" parent="{B}" instance=ExtResource("p_fall")]\nposition = Vector2({fx if side=="W" else M(fx)}, {fy})')
    for j,(ix,iy,fl) in enumerate(ISLETS):
        X=ix if side=='W' else M(ix); flip=(fl!=(side=='E'))
        pts=', '.join(f'{X+math.cos(t*math.pi/24)*230:.0f}, {iy-60+math.sin(t*math.pi/24)*80:.0f}' for t in range(49))
        n.append(f'[node name="Islet{j+1}{side}Foam" type="Line2D" parent="Ground/ShoreFoam"]\nmaterial = SubResource("m_foam")\npoints = PackedVector2Array({pts})\nwidth = 200.0\ntexture_mode = 1')
        n.append(f'[node name="Islet{j+1}{side}" parent="YSorted/Vegetation" instance=ExtResource("p_islet")]\nposition = Vector2({X}, {iy})' + ('\nflip_h = true' if flip else ''))
n.append('[node name="Palace" type="Node2D" parent="YSorted/Structures"]\ny_sort_enabled = true')
PB='YSorted/Structures/Palace'
n.append(f'[node name="RoyalPalace" parent="{PB}" instance=ExtResource("p_palace")]\nposition = Vector2({PALACE[0]}, {PALACE[1]})')
n.append(f'[node name="GrandStairs" parent="{PB}" instance=ExtResource("p_stairs")]\nposition = Vector2({STAIRS[0]}, {STAIRS[1]})')
for i,(a,b) in enumerate(TERRACE_WALLS):
    n.append(f'[node name="TerraceWall{i+1}" parent="{PB}" instance=ExtResource("p_wall")]\nposition = Vector2({a}, {TERRACE_Y})\nlength = {b-a}.0\ntile_offset = {i*131}.0\nbanner_start = {420 if i==0 else 1130}.0\nbanner_spacing = 99999.0\nin_water = false')
for i,(x,y) in enumerate(TERRACE_TOWERS):
    n.append(f'[node name="TerraceTower{i+1}" parent="{PB}" instance=ExtResource("p_tower")]\nposition = Vector2({x}, {y})')
for i,(x,y) in enumerate(GARGOYLES):
    n.append(f'[node name="Gargoyle{i+1}" parent="{PB}" instance=ExtResource("p_garg")]\nposition = Vector2({x}, {y})' + ('\nflip_h = true' if i==1 else ''))
for i,(x,y) in enumerate(STAIR_KNIGHTS):
    n.append(f'[node name="StairKnight{i+1}" parent="{PB}" instance=ExtResource("p_knight2")]\nposition = Vector2({x}, {y})' + ('\nflip_h = true' if i==1 else ''))
for i,(x,y) in enumerate(STAIR_LANTERNS):
    n.append(f'[node name="StairLantern{i+1}" parent="{PB}" instance=ExtResource("p_lantern")]\nposition = Vector2({x}, {y})')
n.append('[node name="MiddleRing" type="Node2D" parent="YSorted/Structures"]\ny_sort_enabled = true')
MR='YSorted/Structures/MiddleRing'
for (part,x,y,sc,fl) in BUILDINGS:
    n.append(f'[node name="{part}" parent="{MR}" instance=ExtResource("p_{part}")]\nposition = Vector2({x}, {y})' + (f'\nscale = Vector2({sc}, {sc})' if sc!=1.0 else '') + ('\nflip_h = true' if fl else ''))
for i,(x,y) in enumerate(AVENUE_PLANTERS):
    n.append(f'[node name="AvenuePlanter{i+1}" parent="{MR}" instance=ExtResource("p_CypressPlanter")]\nposition = Vector2({x}, {y})' + ('\nflip_h = true' if x>7680 else ''))
for i,(x,y) in enumerate(AVENUE_LANTERNS):
    n.append(f'[node name="AvenueLantern{i+1}" parent="{MR}" instance=ExtResource("p_lantern")]\nposition = Vector2({x}, {y})')
# vegetation
V='YSorted/Vegetation'
rnd=random.Random(42); vi=0
def addtree(kind,x,y,flip=False,sc=1.0):
    global vi; vi+=1
    n.append(f'[node name="{kind}{vi}" parent="{V}" instance=ExtResource("p_{kind}")]\nposition = Vector2({x:.0f}, {y:.0f})' + ('\nflip_h = true' if flip else '') + (f'\nscale = Vector2({sc:.2f}, {sc:.2f})' if abs(sc-1)>0.01 else ''))
for side in 'WE':
    for cx in CYPRESS_COLS:
        X=cx if side=='W' else M(cx)
        for j,y in enumerate(CYPRESS_ROWS):
            addtree(['CypressA','CypressC','CypressB'][(j+CYPRESS_COLS.index(cx))%3],X+rnd.uniform(-20,20),y+rnd.uniform(-15,15),rnd.random()<0.5)
def in_poly(x,y,poly):
    c=False
    for (x0,y0),(x1,y1) in zip(poly,poly[1:]+poly[:1]):
        if (y0>y)!=(y1>y) and x < x0+(y-y0)*(x1-x0)/(y1-y0): c=not c
    return c
for name,p in GARDEN:
    if 'Avenue' in name: continue
    poly=[(x*K,y*K) for x,y in p]
    xs=[q[0] for q in poly]; ys=[q[1] for q in poly]
    step=300
    for gy in range(int(min(ys))+200,int(max(ys))-40,step):
        for gx in range(int(min(xs))+120,int(max(xs))-80,step):
            x=gx+rnd.uniform(-110,110)+(step/2 if (gy//step)%2 else 0); y=gy+rnd.uniform(-90,90)
            if not in_poly(x,y,poly) or not in_poly(x,y-120,poly): continue
            if any(a<=x<=c and b<=y<=d for a,b,c,d in TREE_EXCLUDE): continue
            r=rnd.random()
            if r<0.12: continue
            kind=rnd.choice(['PineA','PineB','PineC','PineD']) if r<0.8 else rnd.choice(['Bush','BushWhite','BushRed','CypressA'])
            addtree(kind,x,y,rnd.random()<0.5,rnd.uniform(0.9,1.12))
# market + training yard props (ext resources added on demand)
used={}
for grp,label in [(MARKET,'Market'),(TRAINING,'TrainingYard')]:
    n.append(f'[node name="{label}" type="Node2D" parent="YSorted/Props"]\ny_sort_enabled = true')
    for i,(part,folder,x,y,fl) in enumerate(grp):
        rid=f'pp_{folder}_{part}'
        if rid not in used:
            used[rid]=1; ext.append(('PackedScene',f'res://scenes/castle/parts/{folder}/{part}.tscn',rid))
        n.append(f'[node name="{part}{i+1}" parent="YSorted/Props/{label}" instance=ExtResource("{rid}")]\nposition = Vector2({x}, {y})' + ('\nflip_h = true' if fl else ''))
n.append('[node name="Flanks" type="Node2D" parent="YSorted/Structures"]\ny_sort_enabled = true')
for i,(x0,x1,y) in enumerate(FLANK_BRIDGES):
    for side in 'WE':
        a=x0 if side=='W' else M(x1)
        n.append(f'[node name="Bridge{i+1}{side}" parent="YSorted/Structures/Flanks" instance=ExtResource("p_wall")]\nposition = Vector2({a}, {y})\nwall_tile = ExtResource("t_bridge")\nlength = {x1-x0}.0\ntile_offset = {i*97+(53 if side=="E" else 0)}.0\nbanner_spacing = 0.0\ncollision_depth = 40.0')
for i,(x,y,w) in enumerate(FLANK_TOWERS):
    for side in 'WE':
        n.append(f'[node name="FlankTower{i+1}{side}" parent="YSorted/Structures/Flanks" instance=ExtResource("p_tower")]\nposition = Vector2({x if side=="W" else M(x)}, {y})\nin_water = {"true" if w else "false"}')
for i,(x,y,w) in enumerate(TOWERS):
    for side in 'WE':
        xx=x if side=='W' else WORLD_W-x
        n.append(f'[node name="Tower{i+1}{side}" parent="YSorted/Structures/CurtainWall" instance=ExtResource("p_tower")]\nposition = Vector2({xx}, {y})\nin_water = {"true" if w else "false"}')
n.append('[node name="Effects" type="Node2D" parent="."]')
ext.append(('Script','res://scripts/castle/day_night.gd','daynight'))
n.append('[node name="WorldTint" type="CanvasModulate" parent="."]\ncolor = Color(1, 0.9, 0.78, 1)')
n.append('[node name="DayNight" type="Node" parent="."]\nscript = ExtResource("daynight")\ncanvas_modulate = NodePath("../WorldTint")')
sub.append('[sub_resource type="Environment" id="env"]\nbackground_mode = 3\nglow_enabled = true\nglow_intensity = 0.6\nglow_strength = 0.9\nglow_bloom = 0.05\nglow_blend_mode = 1\nglow_hdr_threshold = 1.05')
n.append('[node name="Environment" type="WorldEnvironment" parent="."]\nenvironment = SubResource("env")')
n.append(f'[node name="Reference" type="Sprite2D" parent="."]\nvisible = false\nmodulate = Color(1, 1, 1, 0.45)\nz_index = 100\nscale = Vector2({K}, {K})\ntexture = ExtResource("ref")\ncentered = false')
n.append(f'[node name="DebugCamera" type="Camera2D" parent="."]\nposition = Vector2({768*K}, {800*K})\nzoom = Vector2(0.5, 0.5)\nscript = ExtResource("cam")\nreference_path = NodePath("../Reference")')
head=f'[gd_scene load_steps={len(ext)+len(sub)+1} format=3]\n'
body=head+'\n'+'\n'.join(f'[ext_resource type="{t}" path="{p}" id="{i}"]' for t,p,i in ext)+'\n\n'+'\n\n'.join(sub)+'\n\n'+'\n\n'.join(n)+'\n'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../scenes/castle/Castle.tscn'),'w').write(body)
print(len(body))
