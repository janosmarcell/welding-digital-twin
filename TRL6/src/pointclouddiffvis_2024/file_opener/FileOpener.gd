extends PanelContainer

enum BrowseMode {
	TEMPLATE,
	OBJECT
}

signal load_requested(template_model_path, object_model_path)

var _template_model_path : String = ""
var _object_model_path : String = ""

var _browse_mode : int = 0

func popup_error(err_str : String) -> void:
	var error_dialog : AcceptDialog = get_node(^"%ErrorDialog")
	
	error_dialog.dialog_text = err_str
	error_dialog.popup_centered()

func _on_CancelButton_pressed() -> void:
	hide()

func _on_LoadButton_pressed() -> void:
	if _template_model_path == "":
		popup_error("Please select a Template mesh file!")
		return
		
	if _object_model_path == "":
		popup_error("Please select an Object mesh file!")
		return
	
	emit_signal(@"load_requested", _template_model_path, _object_model_path)
	hide()

func _on_TemplateMeshBrowseButton_pressed() -> void:
	_browse_mode = BrowseMode.TEMPLATE
	get_node(^"%FileDialog").popup_centered()

func _on_ObjectMeshBrowseButton_pressed() -> void:
	_browse_mode = BrowseMode.OBJECT
	get_node(^"%FileDialog").popup_centered()

func _on_FileDialog_file_selected(path: String) -> void:
	if path == "":
		return
	
	var abspath : String = ProjectSettings.globalize_path(path)
	
	if !abspath.to_lower().ends_with(".ply"):
		popup_error("Error opening file! " + abspath + " - " + path)
		return
		
	if !abspath.to_lower().ends_with(".ply"):
		popup_error("Error opening file! " + abspath + " - " + path)
		return
	
	if _browse_mode == BrowseMode.TEMPLATE:
		_template_model_path = abspath
		get_node(^"%TemplateMeshPathLabel").text = abspath
	elif _browse_mode == BrowseMode.OBJECT:
		_object_model_path = abspath
		get_node(^"%ObjectMeshPathLabel").text = abspath

func _ready() -> void:
	hide()
