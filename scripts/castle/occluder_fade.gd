extends Node2D
## Top-down RPG see-through: when the player walks behind this structure (inside its picture,
## north of its base), it fades so the player stays visible, e.g. while passing through the gate.
@export var faded_alpha := 0.38
@export var bottom_margin := 12.0
@export var fade_parent := false   ## fade the parent node (for scenes whose root already has a script)
var _tgt: Node2D
var _rect := Rect2()
var _has_rect := false

func _compute_rect() -> void:
	_tgt = get_parent() as Node2D if fade_parent else self
	var items: Array = _tgt.find_children("*", "Sprite2D", true, false)
	if _tgt is Sprite2D: items.append(_tgt)
	for s in items:
		var sp := s as Sprite2D
		if sp.texture == null or not sp.visible: continue
		var gr := sp.get_global_transform() * sp.get_rect()
		_rect = gr if not _has_rect else _rect.merge(gr)
		_has_rect = true

func _process(delta: float) -> void:
	if not _has_rect:
		_compute_rect()
		if not _has_rect: return
	var p := get_tree().get_first_node_in_group("player") as Node2D
	if p == null: return
	var body := p.global_position + Vector2(0, -60)
	var behind := _rect.has_point(body) and p.global_position.y < _tgt.global_position.y - bottom_margin
	_tgt.modulate.a = move_toward(_tgt.modulate.a, faded_alpha if behind else 1.0, delta * 4.0)
