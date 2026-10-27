@tool
extends Node2D
## A straight run of curtain wall built from a seamless wall tile.
## Origin = bottom-left of the wall face (y-sort anchor). Adjust `length` in the inspector.

const WALL_TILE := preload("res://assets/sprites/walls/curtain_wall_tile.png")
const BANNER := preload("res://assets/sprites/banners/banner_red_cross_wall.png")
const FOAM := preload("res://resources/shore_foam_material.tres")

@export var length := 1200.0:
	set(v): length = maxf(v, 50.0); _rebuild()
@export var banner_spacing := 760.0:  ## 0 = no banners
	set(v): banner_spacing = v; _rebuild()
@export var banner_start := 380.0:
	set(v): banner_start = v; _rebuild()
@export var tile_offset := 0.0:       ## shifts the stone pattern so neighbouring runs don't line up
	set(v): tile_offset = v; _rebuild()
@export var in_water := true:          ## foam along the base where the wall meets the moat
	set(v): in_water = v; _rebuild()
@export var collision_depth := 90.0:
	set(v): collision_depth = v; _rebuild()

func _ready() -> void:
	_rebuild()

func _rebuild() -> void:
	if not is_inside_tree():
		return
	for c in get_children():
		if c.has_meta("generated"):
			remove_child(c)
			c.queue_free()
	var h := float(WALL_TILE.get_height())

	if in_water:
		var foam := Line2D.new()
		foam.material = FOAM
		foam.width = 200.0
		foam.texture_mode = Line2D.LINE_TEXTURE_TILE
		foam.z_as_relative = false
		foam.z_index = -85
		foam.points = PackedVector2Array([Vector2(0, -6), Vector2(length, -6)])
		_add(foam)

	var face := Sprite2D.new()
	face.texture = WALL_TILE
	face.centered = false
	face.texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
	face.region_enabled = true
	face.region_rect = Rect2(tile_offset, 0, length, h)
	face.position = Vector2(0, -h)
	_add(face)

	if banner_spacing > 0.0:
		var x := banner_start
		while x < length - 60.0:
			var b := Sprite2D.new()
			b.texture = BANNER
			b.centered = false
			b.position = Vector2(round(x - BANNER.get_width() * 0.5), -h + 175.0)
			_add(b)
			x += banner_spacing

	var body := StaticBody2D.new()
	var shape := CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	rect.size = Vector2(length, collision_depth)
	shape.shape = rect
	shape.position = Vector2(length * 0.5, -collision_depth * 0.5)
	body.add_child(shape)
	_add(body)

func _add(n: Node) -> void:
	n.set_meta("generated", true)
	add_child(n)
