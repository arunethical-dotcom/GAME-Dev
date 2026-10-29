extends SceneTree
## Play test: walk north through the gatehouse in both castles, screenshot mid-gate, report fade + stops.
## godot --path . -s res://game/test_gate.gd -- <out_prefix>
func _walk(p: CharacterBody2D, action: String, frames: int) -> void:
	Input.action_press(action)
	for i in frames: await physics_frame
	Input.action_release(action)

func _shot(name: String) -> void:
	var args := OS.get_cmdline_user_args()
	if args.is_empty(): return
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(args[0] + "_" + name + ".png")

func _initialize() -> void:
	var game: Node = load("res://game/Game.tscn").instantiate()
	root.add_child(game); current_scene = game
	for i in 10: await physics_frame
	var p := game.find_child("Player", true, false) as CharacterBody2D
	var cam := p.get_node("Camera") as Camera2D
	var gh := game.find_child("Gatehouse", true, false) as Node2D
	for x0 in [0.0, 25000.0]:
		var tag := "godot" if x0 == 0.0 else "block"
		p.global_position = Vector2(x0 + 7680, 8600); cam.reset_smoothing()
		await _walk(p, "cam_up", 70)
		print(tag, " at gate ", p.global_position, " gatehouse alpha ", gh.modulate.a if gh and x0 == 0.0 else -1.0)
		await _shot(tag + "_in_gate")
		await _walk(p, "cam_up", 120)
		print(tag, " through gate -> ", p.global_position)
		await _shot(tag + "_past_gate")
		# side test: walk west along the lower ward then south into the curtain wall
		p.global_position = Vector2(x0 + 6600, 5700); cam.reset_smoothing()
		await _walk(p, "cam_down", 200)
		print(tag, " south into curtain wall stopped at ", p.global_position)
		# tower test: walk east into a tower
		p.global_position = Vector2(x0 + 7680, 4120); cam.reset_smoothing()
		await _walk(p, "cam_up", 400)
		print(tag, " north up the grand stairs -> ", p.global_position)
		await _shot(tag + "_stairs")
	quit()
