extends ImmediateGeometry

func _ready() -> void:
	begin(Mesh.PRIMITIVE_LINES)
	
	set_color(Color.red)
	add_vertex(Vector3(-500, 0, 0))
	add_vertex(Vector3(500, 0, 0))
	
	set_color(Color.blue)
	add_vertex(Vector3(0, 0, -500))
	add_vertex(Vector3(0, 0, 500))
	
	set_color(Color.green)
	add_vertex(Vector3(0, -500, 0))
	add_vertex(Vector3(0, 500, 0))
	
	set_color(Color.burlywood)
	
	for x in range(-50, 60, 10):
		if x == 0:
			continue
			
		add_vertex(Vector3(x, 0, -60))
		add_vertex(Vector3(x, 0, 60))
		
	for z in range(-50, 60, 10):
		if z == 0:
			continue
				
		add_vertex(Vector3(-60, 0, z))
		add_vertex(Vector3(60, 0, z))
	
	set_color(Color.darkkhaki)
	
	for x in range(-20, 21, 1):
		if x == 0 || x % 10 == 0:
			continue
			
		add_vertex(Vector3(x, 0, -20))
		add_vertex(Vector3(x, 0, 20))
		
	for z in range(-20, 21, 1):
		if z == 0 || z % 10 == 0:
			continue
				
		add_vertex(Vector3(-20, 0, z))
		add_vertex(Vector3(20, 0, z))
			
	
	end()
