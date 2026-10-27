extends Camera2D
## Free-look camera for inspecting the world while we build it.
## WASD / arrows: pan · mouse wheel: zoom (toward cursor) · middle-mouse drag: pan · R: toggle reference overlay

@export var pan_speed := 1600.0
@export var zoom_step := 1.12
@export var min_zoom := 0.08
@export var max_zoom := 3.0
@export var reference_path: NodePath

var _dragging := false

func _process(delta: float) -> void:
	var dir := Input.get_vector("cam_left", "cam_right", "cam_up", "cam_down")
	if dir == Vector2.ZERO:
		dir = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	position += dir * pan_speed * delta / zoom.x

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("toggle_reference") and has_node(reference_path):
		var ref := get_node(reference_path) as CanvasItem
		ref.visible = not ref.visible
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP and event.pressed:
			_zoom_at(zoom.x * zoom_step)
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN and event.pressed:
			_zoom_at(zoom.x / zoom_step)
		elif event.button_index == MOUSE_BUTTON_MIDDLE:
			_dragging = event.pressed
	elif event is InputEventMouseMotion and _dragging:
		position -= event.relative / zoom.x

func _zoom_at(z: float) -> void:
	z = clampf(z, min_zoom, max_zoom)
	var m := get_viewport().get_mouse_position() - get_viewport_rect().size * 0.5
	var world_under_mouse := position + m / zoom.x
	zoom = Vector2(z, z)
	position = world_under_mouse - m / z
