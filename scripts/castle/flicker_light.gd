extends PointLight2D
## Firelight: energy and size wobble with smooth noise; brightness follows the day/night cycle.

@export var base_energy := 1.0
@export var flicker := 0.25
@export var speed := 7.0
@export var night_only := false   ## if true, the light is off in full daylight

var _t := randf() * 100.0
var _base_scale := 1.0

func _ready() -> void:
	_base_scale = texture_scale

func _process(delta: float) -> void:
	_t += delta * speed
	var n := sin(_t) * 0.5 + sin(_t * 2.31 + 1.7) * 0.3 + sin(_t * 5.17 + 0.4) * 0.2
	var night := DayNight.night
	var day_factor := night if night_only else lerpf(0.35, 1.0, night)
	energy = base_energy * day_factor * (1.0 + n * flicker)
	texture_scale = _base_scale * (1.0 + n * flicker * 0.15)
