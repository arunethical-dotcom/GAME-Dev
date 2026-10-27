class_name DayNight
extends Node
## Time of day for the castle. Drives CanvasModulate (world tint), the global `night`
## shader value (window glow), and firelight brightness.
## Press N in game to cycle Day → Golden hour → Night.

const PRESETS := [
	{"name": "Day", "night": 0.0, "tint": Color(1, 1, 1)},
	{"name": "Golden hour", "night": 0.45, "tint": Color(1.0, 0.9, 0.78)},
	{"name": "Night", "night": 1.0, "tint": Color(0.38, 0.42, 0.62)},
]

@export_range(0, 2) var preset := 1
@export var canvas_modulate: NodePath

var _tween: Tween

## Current night amount (0 = day, 1 = night), readable from anywhere as DayNight.night.
static var night := 0.45

static func _set_night(v: float) -> void:
	night = v
	RenderingServer.global_shader_parameter_set("night", v)

func _ready() -> void:
	_apply(PRESETS[preset], 0.0)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.physical_keycode == KEY_N:
		preset = (preset + 1) % PRESETS.size()
		_apply(PRESETS[preset], 1.5)

func set_preset(i: int, seconds := 0.0) -> void:
	preset = i
	_apply(PRESETS[i], seconds)

func _apply(p: Dictionary, seconds: float) -> void:
	var cm := get_node_or_null(canvas_modulate) as CanvasModulate
	if _tween:
		_tween.kill()
	if seconds <= 0.0:
		_set_night(p.night)
		if cm:
			cm.color = p.tint
		return
	_tween = create_tween().set_parallel(true)
	_tween.tween_method(_set_night, night, p.night, seconds)
	if cm:
		_tween.tween_property(cm, "color", p.tint, seconds)
