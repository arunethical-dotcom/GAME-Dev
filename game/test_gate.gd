extends SceneTree
## Walk from the causeway straight north through the gate into the castle.
func _initialize() -> void:
	var game: Node = load("res://game/Game.tscn").instantiate()
	root.add_child(game); current_scene = game
	for i in 10: await physics_frame
	var p := game.find_child("Player", true, false) as CharacterBody2D
	Input.action_press("cam_up")
	for i in 600: await physics_frame
	Input.action_release("cam_up")
	print("walked north to ", p.global_position)
	p.global_position = Vector2(5400, 5900)          # inside the lower ward, south of the curtain wall
	for i in 5: await physics_frame
	Input.action_press("cam_down")
	for i in 240: await physics_frame
	Input.action_release("cam_down")
	print("walked south toward the wall, stopped at ", p.global_position)
	quit()
