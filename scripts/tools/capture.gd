extends SceneTree
## Renders screenshots of the castle scene for review.
## godot --path . -s res://scripts/tools/capture.gd -- out_dir
var shots := [
	["castle_overview", Vector2(7680, 5120), 0.125],
	["gate", Vector2(6800, 6700), 0.45],
	["west_flank", Vector2(2400, 5600), 0.45],
	["barbican", Vector2(3800, 8500), 0.5],
	["palace_stairs", Vector2(7680, 2600), 0.32],
	["north_west", Vector2(2600, 2300), 0.35],
]
func _initialize() -> void:
	var out: String = OS.get_cmdline_user_args()[0] if OS.get_cmdline_user_args().size() > 0 else "user://"
	var scene: Node = load("res://scenes/castle/Castle.tscn").instantiate()
	root.add_child(scene)
	var cam := scene.get_node("DebugCamera") as Camera2D
	cam.set_script(null)
	cam.make_current()
	var dn := scene.get_node_or_null("DayNight")
	var night_shots := [["night_castle", Vector2(7680, 5120), 0.125], ["night_gate", Vector2(7680, 7200), 0.4]]
	for s in shots + night_shots:
		if dn:
			dn.set_preset(2 if String(s[0]).begins_with("night") else 1)
		cam.position = s[1]
		cam.zoom = Vector2(s[2], s[2])
		for i in 8:
			await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(out.path_join(s[0] + ".png"))
		print("saved ", s[0])
	quit()
