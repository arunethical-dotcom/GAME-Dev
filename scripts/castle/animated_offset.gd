extends AnimatedSprite2D
## Starts the animation on a random frame so neighbouring waterfalls/splashes don't move in lockstep.
func _ready() -> void:
	play()
	frame = randi() % sprite_frames.get_frame_count(animation)
	speed_scale = randf_range(0.9, 1.1)
