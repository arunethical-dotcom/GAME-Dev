# Castle Observation — Grand Castle Island

Reference image: [`docs/reference/castle_reference.png`](reference/castle_reference.png) (1536 × 1024)

This document breaks the reference down into everything we need to rebuild it in Godot:
layout, every structure, every prop, the palette, what animates, and the build order.
Positions are given as **image pixel coordinates** (x → right, y → down) so they map
directly onto the reference sprite in `scenes/castle/Castle.tscn`.

---

## 1. Camera & art style

| Aspect | Observation | Godot implication |
|---|---|---|
| Projection | **Top-down ¾ (oblique / "JRPG") view**, not isometric. Walls show their *front face* toward the viewer; roofs seen from above-front. | Use a **square-grid `TileMapLayer`**, not isometric. Wall faces are tiles stacked vertically under a wall-top tile. |
| Symmetry | Almost perfectly **mirror-symmetric on the vertical centre axis (x ≈ 768)**. | Build the left half, mirror for the right. Saves ~half the work. |
| Depth | Tall things (towers, keep) overlap what is behind them. | Turn on **Y-Sort** for towers/buildings/statues/props so the player walks behind/in front correctly. |
| Pixel scale | Detailed "HD pixel" look; a stone block ≈ 4–6 image px. | Recommend **16 × 16 tiles**, nearest-neighbour filtering (already set in `project.godot`). |
| Lighting | Late-afternoon warm light, light from **upper-left**, shadows fall right/down. Windows glow warm amber. | Keep shading direction consistent across all assets. Optional `CanvasModulate` + `PointLight2D` for torches/windows. |

---

## 2. Overall layout (outside → inside)

The castle is built as **concentric rings on an island**, entered from the bottom along one straight axis.

```
                 [ Forest + cliffs ]                [ Town (top-right) ]
     waterfall ▸                                          ▲ stone bridge
   ┌──────────────────── RING 3: INNER KEEP / PALACE ──────────────────┐
   │   Royal palace (top-centre), grand stairs, red carpet, gargoyles   │
   ├──────────── RING 2: INNER WARD (gardens, plazas, terraces) ────────┤
   │ Cathedral (L)   │  Fountain plaza + hedge avenue  │  Domed hall (R) │
   │ Market (L-low)  │                                  │  Manor (R)      │
   │                 │                                  │  Training yard  │
   ├──────────── RING 1: MAIN CURTAIN WALL + GATEHOUSE ─────────────────┤
   │      moat-standing towers  ·  portcullis gate  ·  banners          │
   └──────────────────────────── INNER MOAT ────────────────────────────┘
   ════════ OUTER BARBICAN WALL (lowest, flat-topped towers) ════════════
        waterfall ▸           causeway + bridge ▲            ◂ waterfall
                       [ Forest shore / entry point ]
```

### Zones (approximate image bounds)

| # | Zone | Bounds (x, y) | Notes |
|---|---|---|---|
| Z0 | Surrounding land: forest, cliffs, grass, dirt paths | whole border | Pine forest, grey rocky cliffs dropping into water |
| Z1 | Lake / moat water | everywhere between land and walls | Two levels: outer lake and inner moat |
| Z2 | Outer barbican wall | x 140–1400, y 760–900 | Low wall, flat-topped crenellated towers, no roofs except the two gate towers |
| Z3 | Causeway / entry road | x 690–850, y 690–1024 | Straight cobbled road, torch-lined, crosses both moats |
| Z4 | Main curtain wall + gatehouse | x 20–1520, y 480–700 | Blue-roofed towers standing *in* the water, red banners on every tower and wall section |
| Z5 | Lower inner ward (left: market, right: training yard) | x 200–520 / 1100–1330, y 470–620 | Ground-level service areas |
| Z6 | Middle ward: gardens, plazas, fountain | x 420–1120, y 300–560 | Hedge-lined avenues, pine trees, cobbled plaza |
| Z7 | Side precincts: cathedral (L), domed hall + manor (R) | x 200–460 / 1100–1300, y 150–440 | Each in its own walled terrace |
| Z8 | Upper terrace + grand staircase | x 660–880, y 220–390 | Stairs with red carpet, gargoyle statues |
| Z9 | Royal palace / keep | x 470–1080, y 0–230 | Tallest structure, giant central banner |
| Z10 | Town across the river | x 1170–1536, y 0–130 | Orange-roofed houses — **outside** the castle, reached by the NE bridge |

---

## 3. Every structure, in detail

### 3.1 Royal palace (keep) — top centre
- Massive cluster of towers; **~8–10 turrets** of different heights, all with **steep blue conical/pyramid roofs** and small gold finials.
- Central tall block with the **largest banner**: long red banner with gold trim and a **gold cross / fleur emblem**, hanging over the main door.
- Main door: large arched wooden double door with glowing light inside, small balcony above.
- Many **lit arched windows** (warm yellow) across all levels.
- Two inner courtyards flanking the keep (left and right) each with a **small fountain**.
- Thick connecting walls run left and right to two big corner towers (≈ x 300 and x 1290).

### 3.2 Grand staircase & upper terrace — centre
- Wide stone stairs in **two flights** down from the palace door, with a **red carpet** running down the middle.
- A landing between flights with two **winged gargoyle / griffin statues** on pedestals (dark stone).
- Two **knight statues** on pillars at the bottom of the stairs.
- Lamp posts / torches on both sides.
- Flanked by two square watchtowers with blue roofs and banners.

### 3.3 Central plaza & fountain
- Cobbled plaza below the stairs with a **round tiered fountain** (blue water) at the centre (~x 768, y 410).
- A **long avenue** runs from the fountain down to the gatehouse, lined both sides with **tall narrow cypress/hedge columns** and low clipped hedges.
- Two **rectangular reflecting pools** left and right of the avenue (~y 500).
- Arched colonnades (3 arches) set into the walls on both sides.

### 3.4 Cathedral — left precinct
- Large Gothic church, steep blue roof with side gables.
- **Big stained-glass window** (multi-coloured: blue, red, gold) above the entrance — signature detail.
- Small entrance stair, lit side windows, small bell tower/turret on its right.
- Behind it (higher up, ~x 370, y 200) a **small chapel/shrine** with blue roof.
- Surrounded by its own lawn with pine trees.

### 3.5 Domed hall — right precinct (mirror of cathedral)
- Building with a **dark blue dome** and a lantern/cupola on top, ring of glowing windows under the dome.
- Wide stair in front. Reads as library / mage tower / throne hall — **purpose TBD**.

### 3.6 Manor house — right, lower
- Two-storey manor, blue hipped roof, central arched door, lit windows.
- Sits on a lawn with a **few small gravestones/markers** behind it (possible small graveyard or garden ornaments).

### 3.7 Market quarter — left inner ward
- Dirt/plank floor yard with **~8 wooden market stalls/houses**, brown shingle roofs.
- A small blue-roofed guard post at its corner, a few tiny figures/crates.

### 3.8 Training yard — right inner ward (mirror of market)
- Sandy dirt yard with **training dummies** (cross-shaped wooden posts) in rows.
- **Weapon racks** along the back wall, a few wooden sheds/stables on the right side.

### 3.9 Main curtain wall & gatehouse
- Long crenellated wall, front face of large grey stone blocks.
- **Towers**: round/octagonal, blue roofs, gold finial, **red banner with gold emblem on each**. Several stand **directly in the water** with water ripples at the base.
- Smaller banners hang on the flat wall sections between towers (~every 100 px).
- **Gatehouse** (x 690–850): two tall towers, big arch with **iron portcullis**, emblem plaque above, two **dark knight statues** flanking the opening.
- Left and right ends: walls turn back and run up along the sides as **bridges/arched aqueduct walls** over the moat, joining the upper corner towers.

### 3.10 Outer barbican wall
- Lower than the main wall. Towers here are **flat-topped with crenellations and no roof** (except the two gate towers).
- The **two gate towers** (≈ x 640 and x 900) have blue roofs and **small red pennant flags** on poles.
- Causeway passes between them flanked by **armoured knight statues** on pedestals and **lantern pillars** with glowing light.
- Wall ends at both sides on rocky cliffs, each with an **arched sluice under the wall feeding a waterfall** (bottom-left ~x 230, bottom-right ~x 1310).

### 3.11 Causeway
- Straight cobblestone road from the bottom edge to the gatehouse, low stone parapet walls on both sides.
- **Torches on posts** every ~60 px on both sides (5 pairs visible), lit.

### 3.12 Side bridges & towers (left and right)
- Each side has a chain of 3–4 towers linked by **arched stone bridges** over the water, forming the flanks of the island.
- Bridge arches show light reflections in the water beneath.
- Some wall bases have **glowing blue water** where it flows through grates.

### 3.13 Outside the walls
- **Top-left**: tall grey cliff with a **waterfall** falling into the lake, small rock islet.
- **Top-right**: a **town** of orange/red-roofed half-timbered houses, connected to the castle by a **long arched stone bridge** over the river.
- Dirt paths winding through the forest at top-left and bottom edges.
- **Seagulls** flying over the water (white birds, left of the gate, and right).
- Small rocky islets with grass and trees in the lake.

---

## 4. Colour palette (sampled from the image)

| Material | Hex (sampled) | Notes |
|---|---|---|
| Moat water | `#045282` | Main water tone; lighter cyan `#5fc6ff`-ish highlights on ripples |
| Deep water | `#033361` | Far/outer water |
| Wall stone (lit) | `#ab9c97` | Warm grey |
| Wall stone (shadow) | `#3c4563` | Cool blue-grey shadow |
| Roof blue | `#486f91` | Range from dark navy to bright slate blue |
| Banner red | `#b64e3f` | Deep crimson body, gold `#e0b040`-ish emblem & trim |
| Red carpet | `#7e1a39` | Darker wine red |
| Grass | `#326446` → `#7d9b37` | Dark under trees to bright yellow-green |
| Cobble / plaza | `#b6a095` | Light warm stone |
| Dirt yard | `#c2a48a` | Market & training yard |
| Cliff rock | `#3c4b64` | Blue-grey |
| Torch / window glow | `#c28054` → bright yellow | Warm orange glow |

Overall: **cool blues + greys** for the castle, **warm red/gold** accents, **warm glow** for life. Keep every new asset inside this palette.

---

## 5. Things that should animate

| Element | Count (approx.) | Animation |
|---|---|---|
| Water surface / ripples at tower bases | everywhere | Looping tile animation (3–4 frames) |
| Waterfalls | 3 (top-left cliff, bottom-left, bottom-right) | Vertical scroll loop + foam at base |
| Torches on causeway & gate | ~12 | Flicker (4 frames) + `PointLight2D` |
| Banners | ~40 | Gentle sway (2–4 frames) — optional |
| Pennant flags on outer gate towers | 2 | Wave (4 frames) |
| Fountains | 3 (central + 2 palace courtyards) | Water spray loop |
| Seagulls | ~10 | Flying sprite moving along a path |
| Window glow | many | Static, optional slow pulse at night |

---

## 6. Asset checklist (what to upload)

Upload into the matching folder. `.png`, transparent background, 16 × 16 grid for tiles.

**Tilesets — `assets/tilesets/`**
- [ ] `terrain/` grass (light/dark), dirt path, cliff top + cliff face, rocky shore
- [ ] `water/` lake water (animated), shoreline edges, waterfall tiles
- [ ] `walls/` wall top (crenellated), wall face, wall corners, arched bridge, wall-in-water base
- [ ] `floors/` cobblestone, plaza stone, dirt yard, red carpet, stairs
- [ ] `roofs/` (only if roofs are tiled instead of part of building sprites)

**Sprites — `assets/sprites/`**
- [ ] `towers/` blue-roof tower (large, small), flat-top barbican tower, gate tower with pennant
- [ ] `buildings/` palace/keep, cathedral, domed hall, manor, chapel, market stalls, sheds, guard post, town houses
- [ ] `statues/` knight statue, winged gargoyle, lion/griffin
- [ ] `banners/` wall banner, tower banner, giant palace banner, pennant flag
- [ ] `props/` fountain (large, small), torch post, lantern pillar, training dummy, weapon rack, crates, gravestones, benches
- [ ] `vegetation/` pine tree, cypress column, hedge, bush, flower beds
- [ ] `ambient/` seagull

**Effects — `assets/effects/`**
- [ ] `torch/` flame frames
- [ ] `water/` ripple frames, fountain spray
- [ ] `waterfall/` fall + foam frames

If an asset pack comes as one big sheet, drop it in the closest folder — we'll slice it in Godot.

---

## 7. Build plan in Godot

1. **Reference layer** — `Castle.tscn` already contains the reference image at 50 % opacity so we can trace over it. ✅ (this commit)
2. **Ground** — `TileMapLayer` "Ground": water, grass, cliffs, shoreline.
3. **Floors** — `TileMapLayer` "Floors": cobble, plazas, dirt yards, causeway, carpet.
4. **Walls**: ✅ main curtain wall + gatehouse + 8 towers (`scenes/castle/parts/`). ✅ outer barbican, ✅ side flanks & bridges, ✅ shore cliffs. Next: → inner terraces → palace walls.
5. **Big structures** — `Sprite2D`/scenes in a Y-sorted node: towers, gatehouse, palace, cathedral, domed hall, manor.
6. **Props & vegetation** — Y-sorted: trees, hedges, statues, stalls, dummies, fountains.
7. **Life** — animated water/waterfalls/torches/banners, seagulls, lights.
8. **Collision & navigation** — so a player can walk the causeway → gate → avenue → stairs → palace.

Mirror rule: finish the **left half** of each ring, then duplicate & flip for the right half, then fix the asymmetric bits (cathedral ↔ domed hall, market ↔ training yard, town in the top-right).

---

## 8. Open questions for you

1. Is the domed hall on the right a library, mage tower, or throne hall? (affects interior later)
2. Will the player walk on the walls (ramparts) or only on the ground?
3. Do we include the town (top-right) in this first map, or leave it for the next step?
4. Target resolution — I've set **640 × 360** base, scaled up. OK, or do you prefer 480 × 270 / 320 × 180?
