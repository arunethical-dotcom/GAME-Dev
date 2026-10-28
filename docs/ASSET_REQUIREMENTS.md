# Castle asset requirements: highest-quality build

> **To generate the art, use `docs/prompts/CASTLE_PROMPTS.xlsx`** (one sheet, one complete prompt per image). It splits multi-piece items into single images, and animations are done in code, so no frame sheets are needed. Sizes below are the final in-game sizes I resize to.

> **Where each asset goes:** see `docs/ASSET_MAP.md`. It shows the plan with a grid (A–AV × 1–32) and every ID below marked on it.

This is everything still needed to bring the castle (as built from `docs/reference/castle_reference.png`)
to full quality: what to make, exact sizes, frames, and rules.

Every size below is the **exact size the piece is drawn at in the game**, measured from the current scene.
Deliver at that size and it renders 1:1, with no scaling and no blur.

---

## 0. Why new assets are needed
The castle's layout now matches the plan, but most art is **borrowed from packs and rescaled**:
- **Towers:** one tower sprite is drawn at **7 different scales** (0.6× to 1.35×) across 42 towers.
- **Staircases:** stretched **non-uniformly** (0.62 × 1.01 and 0.62 × 0.81).
- **Waterfalls:** stretched **0.89 × 1.46**.
- **Gatehouse, palace keep, cathedral, domed hall:** enlarged 1.3×–1.75× beyond their source detail.
- **Pixel density:** the packs come in at about 2.6–3.4 screen px per art pixel, all non-integer, so no two packs line up on a pixel grid.
- **Colour:** stone was recoloured from sandstone to the plan's grey-blue by script. That works, but hand-painted grey stone will always look better.

Pixel art only looks sharp at **1:1 or integer scales**. So the main job is **native-size art at one shared pixel density**.

---

## 1. Rules for every asset (please read first)

| Rule | Value |
|---|---|
| **Format** | PNG, 32-bit RGBA, **real transparency** (no magenta or green background), no embedded colour profile |
| **Pixel density** | **1 art pixel = 2 × 2 screen pixels** at 1080p. Either draw at half the listed size and we upscale 2× nearest-neighbour, or deliver at full size made of 2×2 blocks. Never use soft brushes, blur or anti-aliased resampling |
| **World scale** | Base canvas 1920 × 1080. A **character is 128 px tall** (64 art px). 1 px on the plan = 10 world px |
| **View** | Top-down **¾ oblique** (JRPG style), **not isometric**. Fronts of walls and towers face the camera straight on, vertical lines stay vertical, and top surfaces are seen from above-front. **Symmetric** front-facing art: no angled or corner views unless listed |
| **Light** | Warm late-afternoon light from the **upper left**. Shadows fall right and down. Left-facing surfaces are lit, right-facing are in shade |
| **Palette** (sampled from the plan) | Stone ramp `#151a30 #3c3e52 #595768 #706b77 #887f86 #a69a96 #dccabb` · Roof blue `#1f2f5a → #486f91 → #8fb0d0` · Banner red `#7e1a39 / #b64e3f` with gold `#e0b040` · Wood `#4a2e1e → #8a5a36` · Glass glow `#ffd27a → #fff3c4` · Water `#033361 / #045282 / #5fc6ff` |
| **Anchor** | Sprites are placed by the **bottom-centre of their footprint** (where the object meets the ground). Keep that point at the bottom middle of the image, with no empty padding below it |
| **Tiling textures** | Must tile seamlessly: test as a 2 × 2 (or 3 × 1 for strips) before sending |
| **Emission masks** | Anything with lit windows, flames or glass ships a **matching `*_emission.png`** (same size, black background, white where it glows). Drives the night window glow and bloom |
| **Animation** | Frames are separate PNGs (`name_0.png`, `name_1.png` …) or one horizontal strip with equal cells. Frame count and fps are listed per asset |
| **Naming** | `snake_case`, e.g. `tower_m_body.png`, `roof_cone_m.png`, `wall_face_tile.png` |
| **Delivery folder** | `assets/castle_hd/<category>/` (create it). Don't overwrite the existing folders |

Size codes: **S / M / L** = small / medium / large tower family (section 3).

---

## 2. Tileable surface textures (the wall kit)
These are drawn by the wall builder along any angle, so they **must tile**.

| ID | Texture | Size (px) | Tiles | Where it's used | Details |
|---|---|---|---|---|---|
| T1 | **Wall face (ashlar)** | **512 × 240** | X and Y | Every wall face: curtain wall (660 px tall), barbican (400–620), terraces (160–300) | Grey-blue dressed blocks, ~40 × 20 art px per block, 2 px mortar, slight bevel lit top-left. Two variants: `wall_face_a`, `wall_face_b` |
| T2 | **Wall base / waterline band** | **512 × 96** | X | Bottom of every wall standing in the moat | Darker wet stone, green-black algae, dripping streaks. Overlays the bottom of T1 |
| T3 | **Merlon (battlement) strip, front** | **480 × 80** | X | Top of every wall edge facing the camera | 6 merlons per tile (80 px period: ~48 px merlon, 32 px gap), each with a lit top face and front face. Plan merlons ≈ 8 × 7 plan px |
| T4 | **Merlon strip, back** (seen from behind) | **480 × 80** | X | Wall edges facing away from the camera | Same rhythm as T3, inner face in shade, walkway side |
| T5 | **Merlon corner caps** | **96 × 96** each | — | Wall corners | 4 pieces: outer 90°, inner 90°, outer 135°, inner 135° (the plan's diagonal corners) |
| T6 | **Corbel / machicolation band** | **480 × 64** | X | Under the parapet on the curtain wall and barbican | Stepped corbels every 80 px (matching T3), dark gaps between |
| T7 | **Wall-walk (top of wall)** | **512 × 512** | X and Y | Walkway band inside parapets, bridge and causeway tops | Worn flagstones, lighter than T1 |
| T8 | **Courtyard cobbles** | **512 × 512** | X and Y | Lower ward floor (largest visible area) | Irregular rounded cobbles, warm grey `#b5a49f`, a few cracks and moss in joints |
| T9 | **Palace terrace paving** | **512 × 512** | X and Y | Palace terrace, landing | Larger cut flagstones, lighter and cleaner than T8 |
| T10 | **Causeway road** | **512 × 512** | X and Y | Causeway | Cobbles with wheel-worn centre, warmer tone |
| T11 | **Formal lawn** | **512 × 512** | X and Y | Cathedral, domed-hall, garden terraces | Short trimmed grass, low-contrast; must not tile visibly at zoom 0.25 |
| T12 | **Dirt yard** | **512 × 512** | X and Y | Market, training yard | Packed earth, footprints, gravel |
| T13 | **Bridge arch face** | **1024 × 720** per arch | X | Flank bridges (3 per side), colonnades | One arch per tile, centred; **transparent opening**; voussoir ring + keystone; ivy optional; waterline algae at the piers |
| T14 | **Cliff face** | **512 × 440** | X | Rock outcrops under the barbican, camera-facing shores | Grey-blue rock columns, grass lip on top 24 px, wet dark base 40 px |
| T15 | **Pool / fountain rim** | **512 × 48** | X | Reflecting pools, pool edges | Carved stone coping seen from above-front |

---

## 3. Towers: the biggest quality gain (42 in the castle)
The game currently draws one 485 × 986 tower at 7 scales. Replace it with **three native size families**, body and roof as separate pieces so roofs can be swapped.

| ID | Piece | Size (px) | Count in scene | Details |
|---|---|---|---|---|
| TW1 | **Tower body S** | **292 × 592** | 6 (colonnade towers, gargoyle pillars) | Round, 8 visible stone courses, 1 arrow slit, corbelled ring at top, flared base |
| TW2 | **Tower body M** | **484 × 984** | 22 (standard ward and moat towers) | As TW1, 2 arrow slits, iron banner hook at 330 px from top |
| TW3 | **Tower body L** | **656 × 1332** | 4 (big moat towers) | As TW2 plus a lit window and a carved string course |
| TW4 | **In-water base** variants of M and L | M **484 × 160**, L **656 × 200** | 18 | Replaces the bottom of the body when standing in the moat: wet dark stone, algae |
| TW5 | **Crenellated top cap** (no roof) S / M | S **292 × 140**, M **484 × 220** | 8 barbican + 2 pillars | Ring of 7 merlons seen from above-front, floor visible inside |
| TW6 | **Blue cone roof** S / M / L | S **336 × 320**, M **560 × 532**, L **756 × 718** | 32 | 8-sided slate cone, gold ridge trims, gold finial, small dormer optional. Overlaps the top of the body by 220 / 300 px |
| TW7 | **Square pillar tower** | **330 × 600** | 2 | Square pedestal tower for the landing gargoyles; flat top with low parapet, banner niche |
| TW8 | **Tower banner** S / M / L | **90 × 200**, **148 × 330**, **200 × 446** | 32 | Red with gold cross, hanging from a rod. **4-frame sway, 6 fps** |
| TW9 | **Pennant flag** | **132 × 148** | 2 | Red swallow-tail on a pole tip. **6-frame wave, 10 fps** |
| TW10 | Emission masks for TW2, TW3 | same as body | — | Lit windows only |

---

## 4. Gatehouse and gate
| ID | Piece | Size (px) | Details |
|---|---|---|---|
| G1 | **Main gatehouse**, front-facing and **symmetric** | **1384 × 1208** | Two half-round flanking turrets, central arch ≈ 300 px wide, crenellated top, emblem plaque, 2 banners, 2 wall torches. The current one shows an angled right side; it must be straight-on |
| G2 | **Portcullis** | **300 × 360** | Separate layer behind the arch. **6 frames** closed → open (lifted), 8 fps, play once |
| G3 | **Gate doors** (open / closed) | **300 × 340** | Iron-strapped oak, 2 frames |
| G4 | Gatehouse emission | 1384 × 1208 | Torches, arrow-slit glow |

---

## 5. Royal palace (top of the castle, 6000 px wide)
The palace is currently one keep enlarged 1.55× plus four copies of a single facade, which repeats visibly. Build it as a **modular set**:

| ID | Piece | Size (px) | Details |
|---|---|---|---|
| P1 | **Central keep** | **1600 × 2000** | Tallest block: giant banner, main double door at the bottom centre, balcony, 2 knight niches, stained-glass windows |
| P2 | **Wing segment A** | **800 × 1050** | 2 storeys of lit Gothic windows, blue roof with dormers, tileable left/right |
| P3 | **Wing segment B** (variation) | **800 × 1050** | Same height as P2 with a bay window or chimney so wings don't repeat |
| P4 | **Wing end / corner pavilion** | **600 × 1250** | Taller square pavilion with a pyramid roof |
| P5 | **Back silhouette layer** | **6000 × 900** | Turret cluster *behind* the palace (the plan's crowded roofline of 8–10 spires). One wide sprite, drawn behind P1–P4 |
| P6 | **Giant banner** | **300 × 800** | Red and gold, palace front. **4-frame sway** |
| P7 | Emission masks for P1–P5 | same sizes | All windows |

---

## 6. Grand staircase and landing
| ID | Piece | Size (px) | Details |
|---|---|---|---|
| S1 | **Upper flight (plain)** | **660 × 480** | 9 steps, stone balustrade both sides, from the palace door down to the landing |
| S2 | **Lower flight (carpeted)** | **660 × 600** | 11 steps, wine-red carpet with gold edge running over each tread, balustrades, lamp posts on the newel posts |
| S3 | **Landing balustrade** | **480 × 120** (tile X) | Low stone rail with urns, along the landing front |
| S4 | **Gargoyle** | **180 × 212** | Winged, dark iron, crouching on the pillar top (S/M mirror pair OK) |
| S5 | **Knight statue on plinth** | **128 × 256** | Dark iron, sword planted, at the foot of the stairs |

---

## 7. Inner buildings (front-facing, grey stone, symmetric where the plan is)
| ID | Building | Size (px) | Details |
|---|---|---|---|
| B1 | **Cathedral** | **1000 × 1300** | Rose window (stained glass), twin spires, blue roof, entrance stair, 2 banners. Emission mask |
| B2 | **Chapel** | **660 × 940** | Small Gothic chapel, bell turret |
| B3 | **Domed hall** | **1228 × 1100** | Dark-blue dome with lantern cupola, ring of lit windows under the dome, wide stair. Emission mask |
| B4 | **Manor** | **1212 × 880** | 2-storey, blue hipped roof, central arched door. Emission mask |
| B5 | **Arched colonnade** (×2) | **790 × 380** | 3 arches with dark interior, columns, merlon top. Replaces the generated one |
| B6 | **Central fountain** | **570 × 480** | Tiered, water in a separate layer (see E4) |

---

## 8. Statues, props and fixtures
| ID | Piece | Size (px) | Count | Details |
|---|---|---|---|---|
| F1 | **Knight statue, dark** | **142 × 285** | 4 | Barbican landing, gate |
| F2 | **Lantern pillar** | **156 × 390** | 2 + more | Stone pillar with a glass lantern. Emission mask |
| F3 | **Brazier on tripod** | **100 × 225** | 10 | Causeway. Flame separate (E5) |
| F4 | **Wall torch sconce** | **40 × 90** | ~20 | Iron bracket for wall faces; flame separate |
| F5 | **Wall banner** | **130 × 290** | ~30 | Red with gold cross on a rod. **4-frame sway** |
| F6 | **Sluice arch grate** | **60 × 70** | 6 | Iron grille in the barbican arches above the waterfalls |
| F7 | **Wall-walk details** (optional) | 60–120 px | — | Arrow-slit decals, drain spouts, iron rings, ivy patches for wall faces (decal sprites to break up long walls) |

---

## 9. Effects (animated)
| ID | Effect | Size per frame (px) | Frames / fps | Details |
|---|---|---|---|---|
| E1 | **Barbican waterfall** | **560 × 880** | 8 / 10 fps, loop | Falls from the 3 sluice arches; currently stretched 1.46× |
| E2 | **Waterfall splash / foam** | **600 × 200** | 6 / 10 fps, loop | Base of E1 |
| E3 | **Tower water ring** | M **520 × 130**, L **700 × 170** | 4 / 6 fps, loop | Ripples around towers standing in the moat |
| E4 | **Fountain water + spray** | **570 × 480** | 6 / 10 fps, loop | Layer over B6 |
| E5 | **Flame** (brazier, torch) | **44 × 100** | 6 / 12 fps, loop | Exists; redo at 2-px density with an emission mask |
| E6 | **Window glow flicker** | — | — | Done in shader from the emission masks (no art needed) |
| E7 | **Seagulls** (optional) | **48 × 32** | 6 / 10 fps | Over the moat |

---

## 10. Terrain right around the castle
| ID | Piece | Size (px) | Details |
|---|---|---|---|
| R1 | **Rock outcrop sprites** | 300–600 wide | 4 variants of mossy grey-blue boulders to sit under the barbican and on the shoreline |
| R2 | **Moat shore edge strip** | **512 × 64** (tile X) | Grass-to-water edge with pebbles, used where land meets the moat without a cliff |
| R3 | **Water texture** | **1024 × 1024** | Exists and works; optional redo at 2-px density |

---

## 11. Later: your designs (sizes so they fit)
Not needed for the castle structure. Listed so they match the scale.
| Item | Size (px) | Notes |
|---|---|---|
| Pine tree | **200 × 420** (4 variants) | Base = trunk centre |
| Cypress column | **90 × 330** (3 variants) | Plan's avenue and garden rows |
| Clipped hedge strip | **512 × 96** (tile X) | Garden borders |
| Flower bed / bush | **120 × 100** (6 variants) | |
| Market stall | **260 × 270** (8 variants) | Plan's market: ~8 timber stalls |
| Market house (timber, shingle roof) | **420 × 400** (4 variants) | Plan's market buildings |
| Training dummy / weapon rack | **120 × 185** / **240 × 200** | Training yard |
| Town house (orange roof) | **740 × 670** (6 variants) | Town across the river |
| Player character | **128 px tall**, 4 or 8 directions | Walk 6–8 frames, idle 4 |

---

## 12. Priority order (biggest visible gain first)
1. **Wall kit T1–T7**: every wall in the castle uses it.
2. **Towers TW1–TW9**: 42 towers, currently rescaled 7 ways.
3. **Gatehouse G1–G2** and **staircase S1–S2**: both centre stage and both currently stretched.
4. **Palace P1–P7**: largest single structure; fixes the repeating wings.
5. **Waterfall E1–E2** and **water rings E3**.
6. **Inner buildings B1–B6** at native size plus emission masks.
7. Floors T8–T12, bridges T13, cliffs T14, props and decals.

**Total, castle only:** 15 textures · ~25 tower pieces · 4 gate pieces · 7 palace pieces · 5 stair pieces · 6 buildings · ~8 prop types · ~7 effects · 3 terrain pieces.

## 13. What can stay as is
- **Water, foam and shore shaders**, and the **day/night lighting**: all code, no art needed.
- **Banner sway**: done by shader, so single-frame banners also work; animated frames are optional extra polish.
- **Layout and wall geometry**: generated from `blueprint/castle_blueprint.py`; new textures drop straight in.
