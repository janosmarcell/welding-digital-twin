extends Spatial

# We have 4 types atm:
#		self.append_result(Dictionary({ 
#			"result_type": "display_single_mesh",
#			"mesh_data": self.o3dpoint_cloud_to_mesh(object_cloud),
#			"result_description": "Step 2, 2 / 3:\n\nObject Mesh: Uniformly sampled mesh cloud display",
#		}), False)
#
#		self.append_result(Dictionary({ 
#			"result_type": "display_meshes",
#			"meshes": Array([self.o3dpoint_cloud_to_mesh(template_cloud), self.o3dpoint_cloud_to_mesh(object_cloud)]),
#			"result_description": "Step 2, 3 / 3:\n\nBoth meshes: Uniformly sampled mesh cloud display",
#		}))
#
#		self.append_result(Dictionary({ 
#			"result_type": "display_text",
#			"result_description": disttext,
#		}), False)
#
#		self.append_result(Dictionary({ 
#			"result_type": "display_image",
#			"image": res_img,
#			"result_description": "Step 5, 2 / 2:\n\nDistance Histogram",
#		}))

var data : Dictionary = Dictionary()

var _single_mesh_view : MeshInstance
var _multi_mesh_view_root : Spatial
#var _image_display : TextureRect

var _material : SpatialMaterial

func set_data(p_data : Dictionary):
	data = p_data
	
	_single_mesh_view.hide()
	_multi_mesh_view_root.hide()
#	_image_display.hide()
	
	for c in _multi_mesh_view_root.get_children():
		c.queue_free()
	
	if !data.has("result_type"):
		return
		
	var rt : String = data["result_type"]
	
	if rt == "display_single_mesh":
		_single_mesh_view.mesh = data["mesh_data"]
		_single_mesh_view.show()
	elif rt == "display_meshes":
		var meshes : Array = data["meshes"]
		
		for m in meshes:
			var mi : MeshInstance = MeshInstance.new()
			mi.mesh = m
			mi.material_override = _material
			_multi_mesh_view_root.add_child(mi)
		
		_multi_mesh_view_root.show()
#	elif rt == "display_image":
#		var img : Image = data["image"]
#		var t : ImageTexture = ImageTexture.new()
#		t.create_from_image(img)
#		_image_display.texture = t
#		_image_display.show()
	#elif rt == "display_text":
	#Nothing to do here
	#	pass

func _ready() -> void:
	_material = load("res://data_viewer/new_spatialmaterial.tres")
	
	_single_mesh_view = $SingleMeshView
	_multi_mesh_view_root = $MultiMeshViewRoot
#	_image_display = $ImageDisplay

func _on_ControlBar_center_camera_button_pressed() -> void:
	var aabb : AABB = AABB()
		
	if _single_mesh_view.visible:
		aabb = _single_mesh_view.get_aabb()
	elif _multi_mesh_view_root.visible:
		var first : bool = true
		for c in _multi_mesh_view_root.get_children():
			if first:
				aabb = c.get_aabb()
				continue
			
			aabb.merge_with(c.get_aabb())
	else:
		return
	
	$Camera.center_on(aabb)

func _on_ControlBar_camera_Speed_slider_changed(new_speed : float) -> void:
	$Camera.speed = new_speed
