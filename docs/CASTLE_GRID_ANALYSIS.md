# Castle plan: grid analysis and rebuild

Plan: `docs/reference/castle_reference.png` (1536 × 1024).
Grid: 32 px cells (48 columns × 32 rows), with 16 px sub-lines: `docs/blueprint/plan_grid_32px.png`.
Traced blueprint over the plan: `docs/blueprint/plan_traced.png`.
Result vs plan: `docs/screenshots/plan_vs_build.jpg`.

All coordinates below are plan pixels; world px = plan px × 10. The castle is mirror-symmetric
about **x = 768** (the causeway), so the blueprint lists the west half only.

## 1. What the plan actually is
The plan is not a set of separate walls. It is a **stack of stone platforms (terraces)**, seen in
3/4 view. Every platform edge that faces the viewer shows a vertical stone face; every edge carries
a crenellated parapet. Towers stand at the corners where faces change direction.

| Level | What | Face height (plan px) | Floor |
|---|---|---|---|
| 0 | Moat / lake | – | water |
| 1 | **Lower ward**: the whole island inside the curtain wall. Its front face *is* the curtain wall | 66 | cobbles |
| 2 | **Cathedral / domed-hall terraces**, **inner gardens**, **south gardens** | 16–22 | grass |
| 3 | **Palace terrace** with the grand stair cut into its front | 30 | light cobbles |
| – | **Outer barbican**: a free-standing wall in the water, south of the moat | 62 → 40 (shorter near the gate, where it stands on rocks) | walkway |
| – | **Flank bridges**: three arched bridges per side, linking moat towers to the island | 48–70 | walkway |

## 2. Wall lines traced from the grid (west half)
**Curtain wall / lower ward outline** (clockwise from the back centre):
`(768,100) (352,100) (262,160) (214,226) (214,420) (172,444) (172,548) (258,592) (298,612) (404,612) (474,638) (768,638)`
- The front between the gate and x≈474 runs straight at y=638; it then **steps back diagonally** to x≈404 and runs straight again. That diagonal step is what the old build missed: it had flat, offset segments that didn't meet.
- The west side runs as two straight north–south faces (x=214 and x=172) joined by a short diagonal at y≈420–444.

**Outer barbican**: `(150,800) (295,800) (395,860) (503,864) (712,868)`. One continuous wall: a straight run, a **diagonal run toward the viewer**, then straight to the gate towers. The old build had disconnected straight pieces at three heights with gaps between them.

**Flank bridges**: `y=528 (x 70→172)`, `y=326 (x 96→214)`, `(140,196)→(236,180)`.
**North-west link wall**: `(236,168)→(352,112)`, a diagonal high wall from the corner tower to the palace back wall.

## 3. Towers (west half, base position)
- **Moat towers**, standing in the water: (57,624) large, (80,400), (123,296), (277,694), (438,795) large, (603,728), (690,705).
- **Barbican flat-tops**: (150,862), (295,880), (395,935), (503,942).
- **Barbican gate tower**, tall with a pennant: (640,960).
- **Ward and terrace towers**: (236,222), (178,590), (355,150), (455,400), (563,402), (688,396), (470,598), (600,598).

## 4. What was wrong in the previous build, and the fix
| Problem | Cause | Fix |
|---|---|---|
| Walls didn't join; gaps and overlaps at corners | Each wall was a separate horizontal sprite strip, so it could only run left to right | New generator builds walls as **3D-style faces along any polyline**: diagonal runs, continuous bricks around corners |
| Barbican was a chain of disconnected pieces | Same as above | One continuous wall with the plan's diagonal, and a face height that shrinks toward the gate |
| No terraces: the inner castle was flat | Not modelled | Five terrace types at three heights, each with faces, parapets and a walkway |
| Sandstone walls next to grey towers | Mixed asset packs | All stone recoloured to the palette sampled from the plan (`scripts/tools/stone_recolor.py`): walls, towers, gatehouse, palace, cathedral, domed hall, manor, chapel. Windows, glass, banners and roofs keep their colour |
| Wall texture showed seams and repeats | The texture was cut from a sprite | New procedural ashlar stone, **perfectly seamless** (`scripts/tools/make_stone.py`) |
| Bridge was a balustrade sprite | Wrong asset | Real stone arch face with an open arch, so the water shows through |
| Flame-coloured flecks on recoloured stone | Bright sandstone highlights were treated as flame | Flame detection narrowed to true fire colours |

## 5. How to change the castle
1. Edit `blueprint/castle_blueprint.py` (plan pixel coordinates; west half only).
2. Run `python3 scripts/tools/gen_castle.py`.
3. Open Godot. The scene `scenes/castle/Castle.tscn` is regenerated; press R to overlay the plan.

Not in this pass, by request: trees, houses, the town and market props.

## 6. Overlay check (pass 2)
The build is rendered at exactly the plan's size and framing (`docs/screenshots/build_at_plan_size.png`)
and laid over the plan at 50 % opacity (`docs/screenshots/overlay_50_on_plan.png`).

Note: rendering at 1536 × 1024 needs camera zoom 0.125, not 0.1, because the game canvas is 1080p-based.

Aligned with the plan: curtain wall and its diagonals, all moat and barbican towers, gatehouse, causeway, flank bridges, palace terrace.

Added in this pass, from the differences the overlay showed:
| Plan feature | Built |
|---|---|
| Two-flight grand staircase with a landing | Plain upper flight (palace door → landing), carpeted lower flight (landing → plaza) |
| Gargoyles on square pillars at the landing | The two blue towers there replaced with roofless pillar towers topped by gargoyles |
| Three-arch colonnades in the inner gardens | Arched colonnade wall between two small blue towers, each side |
| Reflecting pools in front of the colonnades | Stone-rimmed pools with the animated water |
| Inner cypress garden | Re-traced to its real outline (x 602–690), clear of the pool |
| Market / training yard ground | Dirt floors with stone edging (no buildings, by request) |
| Waterfalls under the barbican ends | Three sluice arches in the wall face, waterfall falling onto a rock outcrop |
| Rock outcrops under the barbican | Two rock islands per side with cliff faces |
| Stone landings at the barbican gate | Raised platforms on both sides of the causeway with knight statues and lantern pillars |
| Causeway | Parapets along the sides only, open at both ends |
