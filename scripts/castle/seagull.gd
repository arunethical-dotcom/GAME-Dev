extends Sprite2D
## Seagull gliding in a lazy loop over the water: flaps (swaps two frames) now and then, faces its direction.
@export var wings_up: Texture2D
@export var wings_down: Texture2D
@export var radius := Vector2(900, 320)
@export var speed := 0.12

var _t := randf() * TAU
var _flap := 0.0
var _centre := Vector2.ZERO

func _ready() -> void:
	_centre = position

func _process(delta: float) -> void:
	_t += delta * speed
	var p := _centre + Vector2(cos(_t) * radius.x, sin(_t * 1.3) * radius.y)
	flip_h = p.x < position.x
	position = p
	_flap += delta
	var cycle := fmod(_flap, 3.0)
	texture = wings_down if (cycle < 1.2 and fmod(cycle, 0.3) < 0.15) else wings_up
