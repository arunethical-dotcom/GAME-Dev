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
     ('Texture2D','res://assets/tilesets/terrain/dirt_gravel.png','t_dirt'),('Texture2D','res://assets/tilesets/floors/flagstone.png','t_flag'),('Texture2D','res://assets/tilesets/floors/causeway_road.png','t_road'),('PackedScene','res://scenes/castle/parts/Tower.tscn','p_tower'),('PackedScene','res://scenes/castle/parts/Gatehouse.tscn','p_gate'),('PackedScene','res://scenes/castle/parts/CurtainWall.tscn','p_wall')]
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
n.append('[node name="SandBanks" type="Node2D" parent="Ground"]')
for name,p in LANDO:
    n.append(f'[node name="{name}Bank" type="Line2D" parent="Ground/SandBanks"]\nmaterial = SubResource("m_sand")\npoints = {closed(p)}\nwidth = 110.0\njoint_mode = 0\nsharp_limit = 4.0')
n.append('[node name="Land" type="Node2D" parent="Ground"]')
for name,p in LANDO:
    n.append(f'[node name="{name}" type="Polygon2D" parent="Ground/Land"]\nmaterial = SubResource("m_grass")\npolygon = {pv(p)}')
    n.append(f'[node name="GrassEdge" type="Line2D" parent="Ground/Land/{name}"]\nmaterial = SubResource("m_grass_edge")\npoints = {closed(p)}\nwidth = 36.0\njoint_mode = 0\nsharp_limit = 4.0')
n.append('[node name="CastleGround" type="Node2D" parent="Ground"]')
for name,p in [('CastleIsland',ISL)]:
    n.append(f'[node name="{name}" type="Polygon2D" parent="Ground/CastleGround"]\nmaterial = SubResource("m_flag")\npolygon = {pv(p)}')
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
for i,(x,y,w) in enumerate(TOWERS):
    for side in 'WE':
        xx=x if side=='W' else WORLD_W-x
        n.append(f'[node name="Tower{i+1}{side}" parent="YSorted/Structures/CurtainWall" instance=ExtResource("p_tower")]\nposition = Vector2({xx}, {y})\nin_water = {"true" if w else "false"}')
n.append('[node name="Effects" type="Node2D" parent="."]')
n.append(f'[node name="Reference" type="Sprite2D" parent="."]\nvisible = false\nmodulate = Color(1, 1, 1, 0.45)\nz_index = 100\nscale = Vector2({K}, {K})\ntexture = ExtResource("ref")\ncentered = false')
n.append(f'[node name="DebugCamera" type="Camera2D" parent="."]\nposition = Vector2({768*K}, {800*K})\nzoom = Vector2(0.5, 0.5)\nscript = ExtResource("cam")\nreference_path = NodePath("../Reference")')
head=f'[gd_scene load_steps={len(ext)+len(sub)+1} format=3]\n'
body=head+'\n'+'\n'.join(f'[ext_resource type="{t}" path="{p}" id="{i}"]' for t,p,i in ext)+'\n\n'+'\n\n'.join(sub)+'\n\n'+'\n\n'.join(n)+'\n'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../scenes/castle/Castle.tscn'),'w').write(body)
print(len(body))
