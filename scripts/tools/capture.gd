extends SceneTree
## Renders screenshots of the castle scene for review.
## godot --path . -s res://scripts/tools/capture.gd -- out_dir
var shots := [
	["overview", Vector2(7680, 5120), 0.125],
	["curtain_wall", Vector2(7680, 6300), 0.3],
	["gate_closeup", Vector2(7400, 6650), 0.8],
	["tower_closeup", Vector2(4500, 6500), 0.75],
	["barbican", Vector2(4300, 8700), 0.3],
	["barbican_gate", Vector2(7680, 9050), 0.6],
	["waterfall", Vector2(2100, 8800), 0.7],
	["flank", Vector2(1800, 3500), 0.3],
	["flank_closeup", Vector2(1600, 3700), 0.75],
	["palace", Vector2(7680, 2300), 0.35],
	["palace_closeup", Vector2(7680, 2200), 0.7],
	["stairs_closeup", Vector2(7680, 3000), 0.8],
	["cliffs_topleft", Vector2(2600, 1500), 0.35],
	["cliffs_closeup", Vector2(1400, 1500), 0.8],
	["gate_moat", Vector2(7680, 7400), 0.75],
	["shore_closeup", Vector2(1900, 8700), 1.0],
	["garden_closeup", Vector2(4000, 3400), 1.0],
]
func _initialize() -> void:
	var out: String = OS.get_cmdline_user_args()[0] if OS.get_cmdline_user_args().size() > 0 else "user://"
	var scene: Node = load("res://scenes/castle/Castle.tscn").instantiate()
	root.add_child(scene)
	var cam := scene.get_node("DebugCamera") as Camera2D
	cam.set_script(null)
	cam.make_current()
	for s in shots:
		cam.position = s[1]
		cam.zoom = Vector2(s[2], s[2])
		for i in 8:
			await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(out.path_join(s[0] + ".png"))
		print("saved ", s[0])
	quit()
