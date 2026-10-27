# Asset Guide

77 images from three packs (Surendhar, Bhuvanesh, Gokhul), processed and sorted into `assets/`.

## What was done to every image
1. **Magenta background removed** → real transparency (PNG RGBA), including magenta gaps inside sprites and the pink fringe around edges.
2. **Scale-reference adventurer removed** from the 24 sheets that had him (he was not a game asset).
3. **Trimmed** to the visible content.
4. Seamless textures (water, grass, dirt) left untouched as full-bleed RGB.

## Straightened (tilted → front-facing)
The reference castle is drawn **front-facing (¾ top-down)**. Seven assets were drawn at an angle, so each pixel column was shifted to make the base level. Vertical lines stay vertical, so the pixel detail is preserved.

| File | Was | Now |
|---|---|---|
| `sprites/walls/wall_segment_long.png` | diagonal wall | straight front wall |
| `sprites/walls/wall_segment_short.png` | diagonal wall | straight front wall |
| `sprites/walls/wall_segment_curved.png` | diagonal curved wall | front-facing curved wall |
| `sprites/buildings/aqueduct_bridge.png` | diagonal bridge | side-on arched bridge (the moat bridges in the reference) |
| `sprites/vegetation/cypress_planter.png` | isometric planter | front-facing planter (the avenue planters) |
| `sprites/buildings/manor.png` | slightly angled | front-facing |
| `sprites/buildings/chapel.png` | angled | front-facing |

![before/after](reference/straightened_before_after.png)

**Left angled on purpose:**
- `sprites/buildings/taverns_pair.png`: corner views with two equal faces; straightening one face would warp the other. These suit the **town** (top-right), where an angled look is acceptable.
- `sprites/towers/tower_pieces_angled.png`, plus the diagonal pieces in `bridges_walkways_sheet` and `blue_roof_pieces_sheet`: these are **corner pieces** meant to be angled.

## Map: castle feature → asset

| Castle feature (see CASTLE_OBSERVATION.md) | Asset(s) |
|---|---|
| Lake / moat water | `tilesets/water/deep_water`, `shallow_water`, `coastal_shoreline` |
| Grass, dirt paths | `tilesets/terrain/meadow_grass`, `dirt_gravel` |
| Cliffs | `tilesets/terrain/cliff_tileset`, `rocky_cliff_tileset`, `sprites/nature/rocks_sheet` |
| Waterfalls (×3) | `effects/waterfall/waterfall_animation_sheet` (4 frames + splash), `sprites/nature/waterfall_cliff` |
| Rock islets | `sprites/nature/islets_sheet` |
| Causeway / plaza / walkways | `tilesets/floors/flagstone`, `castle_corridor_walkway`, `stone_bridge_walkway` |
| Curtain walls | `sprites/walls/*`, `tilesets/walls/castle_walls_towers_sheet` |
| Towers (blue roofs) | `sprites/towers/round_tower_flat_top` + `blue_cone_roof`, `tower_top_ring`, `tower_base_rings` (incl. in-water version), `turret_tops_finials_sheet` |
| Gatehouse + portcullis | `sprites/buildings/gatehouse`, `castle_gate_parts_sheet`, `doors_gates_portcullis_sheet` |
| Side bridges over moat | `sprites/buildings/aqueduct_bridge`, `sprites/props/bridges_walkways_sheet` |
| Royal palace / keep | `sprites/buildings/palace_facade`, `palace_entrance_keep` |
| Grand staircase | `sprites/props/stairs_with_brazier`, `stairs_platforms_sheet`, carpet in `interior/carpets_drapery_sheet` |
| Cathedral (left) | `sprites/buildings/cathedral_facade` (rose window), `chapel` |
| Domed hall (right) | `sprites/buildings/domed_hall` (near-exact match) |
| Manor (right) | `sprites/buildings/manor` |
| Market (left) | `sprites/props/market_stalls_carts_sheet`, `barrels_crates_sacks_sheet` |
| Training yard (right) | `sprites/interior/armory_sheet` (weapon racks, dummies) |
| Fountains | `sprites/props/fountain_plaza_large`, `fountains_wells_sheet` |
| Statues & gargoyles | `sprites/statues/statues_gargoyles_sheet` |
| Banners & pennants | `sprites/banners/heraldic_banners_sheet` |
| Torches & lanterns | `effects/torch/fire_animation_sheet`, `sprites/props/lanterns_lampposts_sheet`, `sconces_torches_candles_sheet` |
| Trees, cypress columns, hedges | `sprites/vegetation/trees_pines_cypress_bushes`, `flowering_hedge`, `plants_flowers_sheet`, `wetland_plants_sheet` |
| Town (top-right) | `sprites/buildings/taverns_pair` |
| Roofs | `tilesets/roofs/blue_roof_pieces_sheet` |

**Interior** sheets (`sprites/interior/`) and `sprites/items/` are not needed for the castle exterior. They're kept for building interiors later.

## Still missing
- **Seagulls** (`sprites/ambient/` is empty)
- **Water ripple / tower-base splash animation** (`effects/water/` is empty)
- **Fountain spray animation frames** (the fountains are static)
- **Banner sway frames** (optional)

## World scale (applied)
Everything is resampled to **one shared world scale**: a character is **128 px** tall at a 1920×1080 base resolution.
Resampling used Lanczos with premultiplied alpha, so edges stay clean and there's no dark halo.
Factors were measured from the scale-reference figure where one existed, and otherwise estimated from doors, gates and known objects.

| Asset | Factor | How it was set |
|---|---|---|
| `effects/torch/fire_animation_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `effects/waterfall/waterfall_animation_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/banners/heraldic_banners_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/buildings/aqueduct_bridge` | 0.637 | measured: figure 201px |
| `sprites/buildings/balconies_railings_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/buildings/castle_gate_parts_sheet` | 0.826 | measured: figure 155px |
| `sprites/buildings/cathedral_facade` | 0.719 | estimated: cathedral door = 2 figures |
| `sprites/buildings/chapel` | 0.711 | measured: figure 180px |
| `sprites/buildings/domed_hall` | 0.723 | estimated: grand door = 1.5 figures |
| `sprites/buildings/doors_gates_ornate_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/buildings/doors_gates_portcullis_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/buildings/doors_windows_curtains_sheet` | 0.677 | measured: figure 189px |
| `sprites/buildings/gatehouse` | 0.640 | estimated: gate arch = 2.7 figures |
| `sprites/buildings/manor` | 0.928 | measured: figure 138px |
| `sprites/buildings/palace_entrance_keep` | 0.826 | estimated: grand door = 1.5 figures |
| `sprites/buildings/palace_facade` | 0.736 | estimated: windows = 1.3 doors |
| `sprites/buildings/pillars_arches_balustrades_sheet` | 0.677 | measured: figure 189px |
| `sprites/buildings/stone_parts_debris_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/buildings/taverns_pair` | 0.883 | measured: figure 145px |
| `sprites/interior/armory_sheet` | 0.677 | measured: figure 189px |
| `sprites/interior/bedroom_sheet` | 0.677 | measured: figure 189px |
| `sprites/interior/carpets_drapery_sheet` | 0.677 | measured: figure 189px |
| `sprites/interior/feast_food_sheet` | 0.677 | measured: figure 189px |
| `sprites/interior/furniture_sheet` | 0.677 | measured: figure 189px |
| `sprites/interior/kitchen_sheet` | 0.677 | measured: figure 189px |
| `sprites/interior/library_sheet` | 0.677 | measured: figure 189px |
| `sprites/interior/study_furniture_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/interior/wardrobe_sheet` | 0.677 | measured: figure 189px |
| `sprites/items/keys_tools_potions_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/nature/islets_sheet` | 0.677 | measured: figure 189px |
| `sprites/nature/rocks_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/nature/waterfall_cliff` | 0.688 | measured: figure 186px |
| `sprites/props/barrels_crates_sacks_sheet` | 0.677 | measured: figure 189px |
| `sprites/props/bridges_walkways_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/props/castle_details_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/props/chandeliers_lamps_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/props/dungeon_gates_chains_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/props/fences_gates_sheet` | 0.677 | measured: figure 189px |
| `sprites/props/fountain_plaza_large` | 0.564 | measured: figure 227px |
| `sprites/props/fountains_wells_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/props/garden_furniture_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/props/lanterns_lampposts_sheet` | 0.711 | estimated: lamppost = 1.7 figures |
| `sprites/props/market_stalls_carts_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/props/pots_baskets_containers_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/props/sconces_torches_candles_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/props/signposts_and_signs_sheet` | 0.677 | measured: figure 189px |
| `sprites/props/stairs_platforms_sheet` | 0.677 | measured: figure 189px |
| `sprites/props/stairs_with_brazier` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/props/treasure_chests_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/statues/statues_gargoyles_sheet` | 0.674 | estimated: statue on plinth = 1.5 figures |
| `sprites/towers/blue_cone_roof` | 0.620 | wall set: face = 4.5 figures |
| `sprites/towers/round_tower_flat_top` | 0.620 | wall set: face = 4.5 figures |
| `sprites/towers/tower_base_rings` | 0.620 | wall set: face = 4.5 figures |
| `sprites/towers/tower_pieces_angled` | 0.620 | wall set: face = 4.5 figures |
| `sprites/towers/tower_top_ring` | 0.620 | wall set: face = 4.5 figures |
| `sprites/towers/turret_tops_finials_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/vegetation/cypress_planter` | 0.531 | measured: figure 241px |
| `sprites/vegetation/flowering_hedge` | 0.557 | measured: figure 230px |
| `sprites/vegetation/plants_flowers_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/vegetation/trees_pines_cypress_bushes` | 0.853 | estimated: pine = 3 figures |
| `sprites/vegetation/wetland_plants_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `sprites/walls/curved_tower_walls_pair` | 0.620 | wall set: face = 4.5 figures |
| `sprites/walls/wall_segment_curved` | 0.620 | wall set: face = 4.5 figures |
| `sprites/walls/wall_segment_long` | 0.620 | wall set: face = 4.5 figures |
| `sprites/walls/wall_segment_short` | 0.620 | wall set: face = 4.5 figures |
| `tilesets/floors/castle_corridor_walkway` | 0.680 | estimated: same pack density |
| `tilesets/floors/flagstone` | 1.000 | seamless 1024 |
| `tilesets/floors/stone_bridge_walkway` | 0.680 | estimated: same pack density |
| `tilesets/roofs/blue_roof_pieces_sheet` | 0.680 | estimated: same pack density as measured sheets |
| `tilesets/terrain/cliff_tileset` | 0.680 | estimated: same pack density |
| `tilesets/terrain/dirt_gravel` | 0.817 | seamless 1254->1024 |
| `tilesets/terrain/meadow_grass` | 0.817 | seamless 1254->1024 |
| `tilesets/terrain/rocky_cliff_tileset` | 0.680 | estimated: same pack density |
| `tilesets/walls/castle_walls_towers_sheet` | 0.620 | wall set: face = 4.5 figures |
| `tilesets/water/coastal_shoreline` | 0.817 | estimated: matches meadow_grass blade size |
| `tilesets/water/deep_water` | 0.817 | seamless 1254->1024 |
| `tilesets/water/shallow_water` | 0.817 | seamless 1254->1024 |

`tilesets/floors/causeway_road.png` is cut from `stone_bridge_walkway` at one exact pillar repeat (520 px), so it tiles vertically with no seam.

## Seamless ground textures
`meadow_grass`, `dirt_gravel`, `deep_water`, `shallow_water` and `flagstone` did not tile: their edges differed 2–4× more than their interiors, so a grid of seams would have shown.
Each one was re-made seamless with an offset-and-blend that uses an irregular noise mask, then resampled to 1024×1024 with wrap padding so the edges still match after resizing.

## Assets built for the curtain wall
| File | What |
|---|---|
| `sprites/walls/curtain_wall_tile.png` | `wall_segment_long` levelled (top and base made horizontal), then cut at an exact 403 px repeat so it tiles horizontally with no seam |
| `sprites/towers/tower_roof_blue.png` | Blue cone roof sized to sit on `round_tower_flat_top` |
| `sprites/buildings/gatehouse.png` | Levelled (its base sloped 114 px) and scaled 1.3× so it rises above the wall |
| `sprites/banners/banner_red_cross_wall.png`, `banner_red_cross_tower.png` | Red banner with gold cross from the heraldic sheet, matching the reference |
| `sprites/banners/pennant_red.png` | Red pennant for the outer gate towers |

## Assets built for the outer barbican
| File | What |
|---|---|
| `sprites/walls/barbican_wall_tile.png` | Curtain wall tile with the window band removed (lower wall), recoloured to the reference's cool blue-grey stone |
| `sprites/towers/barbican_tower.png` | Round tower with the window band removed (squat), same recolour |
| `sprites/banners/pennant_red_top.png` | Red pennant flag, pole stand removed, for the gate tower roofs |
| `sprites/statues/knight_statue_dark.png` | Knight statue recoloured to dark iron, like the reference |
| `sprites/props/lantern_pillar.png`, `brazier.png` | From the lantern sheet |
| `sprites/nature/islet_pine.png` | Islet with its painted water removed so it sits in our animated water |
| `effects/waterfall/frames/fall_wide_*.png` | 4-frame waterfall: three streams joined between two cliffs, base faded into the lake |

## Assets built for the flanks and cliffs
| File | What |
|---|---|
| `sprites/walls/arched_bridge_tile.png` | `aqueduct_bridge` with its painted water removed, cut at a clean two-arch repeat (seamless), scaled 1.3× |
| `tilesets/terrain/cliff_face_strip.png` | Rock face from `cliff_tileset`, made seamless sideways with a narrow overlap so there's no ghosting |

Cliffs are drawn as vertical slices (`Ground/Cliffs` in the scene), so the rock columns stay upright however the shoreline curves. The generator finds every shore edge that faces the camera and hangs a cliff under it.
