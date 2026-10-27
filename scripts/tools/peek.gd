extends SceneTree
func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	var out: String = a[0]
	var scene: Node = load("res://scenes/castle/Castle.tscn").instantiate()
	root.add_child(scene)
	var cam := scene.get_node("DebugCamera") as Camera2D
	cam.set_script(null)
	var i := 1
	while i + 3 < a.size() + 1:
		cam.position = Vector2(float(a[i]), float(a[i+1]))
		cam.zoom = Vector2(float(a[i+2]), float(a[i+2]))
		for k in 6: await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(out + "_" + str(i/3) + ".png")
		i += 3
	quit()
