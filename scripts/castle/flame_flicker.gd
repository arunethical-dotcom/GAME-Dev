extends Sprite2D
## Makes a single flame image feel alive: stretches, sways and pulses with smooth noise.
## Pixel-snapped so the art stays crisp.

@export var speed := 9.0
@export var stretch := 0.12
@export var sway := 0.06

var _t := randf() * 100.0

func _process(delta: float) -> void:
	_t += delta * speed
	var n1 := sin(_t) * 0.6 + sin(_t * 2.7 + 1.3) * 0.4
	var n2 := sin(_t * 1.7 + 0.5) * 0.7 + sin(_t * 3.9) * 0.3
	scale = Vector2(1.0 - n1 * stretch * 0.4, 1.0 + n1 * stretch)
	skew = n2 * sway
	modulate = Color(1.0 + n1 * 0.08, 1.0 + n1 * 0.05, 1.0, 1.0)
