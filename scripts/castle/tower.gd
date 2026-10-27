@tool
extends Node2D
## Round blue-roofed tower. Origin = centre of the tower's base (y-sort anchor).

@export var show_banner := true:
	set(v): show_banner = v; _apply()
@export var in_water := false:  ## adds a foam ring where the base meets the moat
	set(v): in_water = v; _apply()
@export var show_roof := true:
	set(v): show_roof = v; _apply()

func _ready() -> void:
	_apply()
	if has_node("WaterFoam"):
		var foam := $WaterFoam as Line2D
		if foam.points.is_empty():
			var pts := PackedVector2Array()
			for i in 49:
				var a := TAU * i / 48.0
				pts.append(Vector2(cos(a) * 250.0, sin(a) * 62.0 - 40.0))
			foam.points = pts

func _apply() -> void:
	if not is_inside_tree():
		return
	$Banner.visible = show_banner
	$Roof.visible = show_roof
	$WaterFoam.visible = in_water
