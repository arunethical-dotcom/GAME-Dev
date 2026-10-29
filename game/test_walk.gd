extends SceneTree
## Automated play test: walk the player and take screenshots.  godot --path . -s res://game/test_walk.gd -- out_prefix
func _initialize() -> void:
	var out: String = OS.get_cmdline_user_args()[0]
	var game: Node = load("res://game/Game.tscn").instantiate()
	root.add_child(game)
	current_scene = game
	await _frames(10)
	var p := game.find_child("Player", true, false) as CharacterBody2D
	print("start ", p.global_position)
	await _shot(out + "_0_start.png")
	Input.action_press("cam_up"); await _frames(90); Input.action_release("cam_up")
	print("after walking up ", p.global_position)
	await _shot(out + "_1_up.png")
	var x0 := p.global_position.x
	Input.action_press("cam_right"); await _frames(120); Input.action_release("cam_right")
	print("after walking right into moat ", p.global_position, " moved ", p.global_position.x - x0)
	await _shot(out + "_2_moat.png")
	var ev := InputEventKey.new(); ev.physical_keycode = KEY_T; ev.pressed = true
	Input.parse_input_event(ev); await _frames(30)
	print("after T ", p.global_position)
	await _shot(out + "_3_block.png")
	quit()

func _frames(n: int) -> void:
	for i in n: await physics_frame

func _shot(path: String) -> void:
	for i in 3: await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(path)
