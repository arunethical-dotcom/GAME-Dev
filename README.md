# Grand Castle Island

A 2D pixel-art game built in **Godot 4** (4.3+). Step 1: build the castle world.

![Castle reference](docs/reference/castle_reference.png)

## Open it
1. `git clone` / `git pull` this repo.
2. Godot → **Import** → select `project.godot`.
3. Press **F5**. You'll see the reference castle at 50 % opacity (WASD/arrows to pan, mouse wheel to zoom).

## Where things go
| Folder | Contents |
|---|---|
| `docs/CASTLE_OBSERVATION.md` | Full breakdown of the castle: zones, structures, palette, animations, asset checklist, build plan |
| `docs/ASSETS.md` | Every asset, what was processed/straightened, and which castle feature it belongs to |
| `docs/reference/` | The reference artwork |
| `assets/tilesets/` | terrain, water, walls, floors, roofs |
| `assets/sprites/` | towers, buildings, statues, banners, props, vegetation, ambient |
| `assets/effects/` | torch, water, waterfall animations |
| `scenes/castle/Castle.tscn` | Main castle scene (Ground / Floors / Walls tile layers + Y-sorted objects) |
| `scripts/` | GDScript |

## Status
- [x] Castle observed & documented
- [x] Project skeleton + reference scene
- [x] Assets uploaded, backgrounds removed, tilted assets straightened
- [ ] Pick a common pixel scale (see docs/ASSETS.md)
- [ ] Ground & water
- [ ] Walls & towers
- [ ] Buildings & props
- [ ] Animation, lighting, collision
