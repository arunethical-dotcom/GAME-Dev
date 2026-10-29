extends SceneTree
func _initialize() -> void:
	var out: String = OS.get_cmdline_user_args()[0]
	var game: Node = load("res://game/Game.tscn").instantiate()
	root.add_child(game); current_scene = game
	var p := game.find_child("Player", true, false) as CharacterBody2D
	var spots := [["gate", Vector2(7680, 7350), "up"], ["fountain", Vector2(7400, 4800), "right"], ["block", Vector2(25000 + 7680, 7350), "up"]]
	for s in spots:
		p.global_position = s[1]
		(p.get_node("Camera") as Camera2D).reset_smoothing()
		(p.get_node("Sprite") as AnimatedSprite2D).play("walk_" + s[2])
		for i in 20: await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(out + "_" + s[0] + ".png")
	quit()
