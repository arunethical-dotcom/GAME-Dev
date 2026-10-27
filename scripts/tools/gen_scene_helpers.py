"""Shared shoreline helpers (organic outlines, camera-facing shore runs)."""
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
