extends SceneTree
## Renders the block castle at exactly the plan's framing (1536x1024, daylight) for scoring.
## godot --resolution 1536x1024 --path . -s res://block_castle/capture.gd -- out.png [x0]
func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	var out: String = a[0]
	var x0: float = float(a[1]) if a.size() > 1 else 25000.0
	var scene: Node = load("res://scenes/castle/Castle.tscn").instantiate()
	root.add_child(scene)
	var dn := scene.get_node_or_null("DayNight")
	if dn: dn.set_preset(0)
	var cam := scene.get_node("DebugCamera") as Camera2D
	cam.set_script(null)
	cam.limit_right = 100000
	cam.position = Vector2(x0 + 7680, 5120)
	cam.zoom = Vector2(0.125, 0.125)
	for k in 8: await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(out)
	quit()
