# Grand Castle Island

A 2D HD pixel-art game built in **Godot 4** (4.4+). Step 1: build the castle world.

![Castle reference](docs/reference/castle_reference.png)

## Open it
1. `git clone` / `git pull` this repo.
2. Godot → **Import** → select `project.godot`.
3. Press **F5**. You'll see the textured island with animated water. WASD/arrows pan, the mouse wheel zooms, and **R** toggles the reference castle overlay.

## Where things go
| Folder | Contents |
|---|---|
| `docs/CASTLE_OBSERVATION.md` | Full breakdown of the castle: zones, structures, palette, animations, asset checklist, build plan |
| `docs/ASSETS.md` | Every asset, what was processed/straightened, and which castle feature it belongs to |
| `docs/TEXTURE_QUALITY.md` | Render/import settings, shaders, rules for new art |
| `shaders/` | Water, terrain and shore-foam shaders |
| `docs/reference/` | The reference artwork |
| `assets/tilesets/` | terrain, water, walls, floors, roofs |
| `assets/sprites/` | towers, buildings, statues, banners, props, vegetation, ambient |
| `assets/effects/` | torch, water, waterfall animations |
| `scenes/castle/Castle.tscn` | Main castle scene: ground, water, Y-sorted structures |
| `scenes/castle/parts/` | Reusable pieces: `Tower`, `BarbicanTower`, `GateTower`, `CurtainWall` (set `length` and `wall_tile` in the inspector), `Gatehouse`, `WideWaterfall`, `KnightStatue`, `LanternPillar`, `Brazier`, `Islet`. Bridges reuse `CurtainWall` with `wall_tile = arched_bridge_tile.png` |
| `scripts/` | GDScript |

## Status
- [x] Castle observed & documented
- [x] Project skeleton + reference scene
- [x] Assets uploaded, backgrounds removed, tilted assets straightened
- [x] One shared world scale (character = 128 px)
- [x] Seamless ground textures, quality render settings
- [x] Ground & animated water
- [x] Main curtain wall, 8 towers, gatehouse (with collision)
- [x] Outer barbican: 8 flat-top towers, 2 pennant gate towers, knight statues, lanterns, braziers, animated waterfalls
- [x] Side flanks: towers in the moat with arched bridges to the island
- [x] Rocky cliffs under every south-facing shoreline
- [ ] Inner terraces, buildings (palace, cathedral, domed hall, manor), props
- [ ] Buildings & props
- [ ] Animation, lighting, collision
