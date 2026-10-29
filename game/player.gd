extends CharacterBody2D
## Simple adventurer: WASD / arrows to walk, Shift to run, mouse wheel to zoom,
## T to travel between the Godot castle and the block castle, N for day / golden hour / night.
## Water is not walkable (walk mask traced from the castle plan); castle walls and towers block via their colliders.

const PLAN_SCALE := 10.0                 # world px per plan px
const BLOCK_X0 := 25000.0                # block castle offset (same as gen_castle.py)
@export var speed := 520.0
@export var run_mult := 1.8

var _mask: Image
var _facing := "down"
@onready var _sprite: AnimatedSprite2D = $Sprite
@onready var _cam: Camera2D = $Camera

func _ready() -> void:
	_mask = (load("res://game/walk_mask.png") as Texture2D).get_image()
	_cam.make_current()
	var dbg := get_tree().current_scene.find_child("DebugCamera", true, false)
	if dbg:
		dbg.enabled = false
		dbg.set_process(false)
		dbg.set_process_unhandled_input(false)

func walkable(p: Vector2) -> bool:
	var x := p.x
	if x >= BLOCK_X0 - 1000.0: x -= BLOCK_X0
	var px := Vector2i(int(x / PLAN_SCALE), int(p.y / PLAN_SCALE))
	if px.x < 0 or px.y < 0 or px.x >= _mask.get_width() or px.y >= _mask.get_height():
		return true
	return _mask.get_pixelv(px).r > 0.5

func _physics_process(_delta: float) -> void:
	var dir := Input.get_vector("cam_left", "cam_right", "cam_up", "cam_down")
	if dir == Vector2.ZERO:
		dir = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	var spd := speed * (run_mult if Input.is_key_pressed(KEY_SHIFT) else 1.0)
	var v := dir * spd
	# water check per axis so the player slides along shorelines
	var step := v * get_physics_process_delta_time()
	if not walkable(global_position + Vector2(step.x, 0) + Vector2(sign(step.x) * 18.0, 0)): v.x = 0.0
	if not walkable(global_position + Vector2(0, step.y) + Vector2(0, sign(step.y) * 10.0)): v.y = 0.0
	velocity = v
	move_and_slide()
	if dir != Vector2.ZERO:
		if abs(dir.x) > abs(dir.y): _facing = "right" if dir.x > 0 else "left"
		else: _facing = "down" if dir.y > 0 else "up"
		_sprite.play("walk_" + _facing)
		_sprite.speed_scale = 1.6 if Input.is_key_pressed(KEY_SHIFT) else 1.0
	else:
		_sprite.play("idle_" + _facing)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.physical_keycode == KEY_T:
		global_position.x += -BLOCK_X0 if global_position.x >= BLOCK_X0 - 1000.0 else BLOCK_X0
		_cam.reset_smoothing()
	if event is InputEventMouseButton and event.pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP: _cam.zoom = (_cam.zoom * 1.12).clamp(Vector2(0.15, 0.15), Vector2(2, 2))
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN: _cam.zoom = (_cam.zoom / 1.12).clamp(Vector2(0.15, 0.15), Vector2(2, 2))
