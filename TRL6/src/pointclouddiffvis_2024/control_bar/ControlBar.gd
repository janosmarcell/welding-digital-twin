extends Container

signal next_button_pressed()
signal prev_button_pressed()
signal open_button_pressed()
signal center_camera_button_pressed()
signal camera_Speed_slider_changed(new_speed)

var data : Dictionary = Dictionary()

var _image_display_container : PanelContainer
var _image_display : TextureRect

var _text_display_container : PanelContainer
var _text_display : Label

func on_working_state_changed(state : bool) -> void:
	get_node(^"%WorkingLabel").visible = state

func on_new_log(log_text : String):
	get_node(^"%WorkLog").text = log_text

func set_prev_next_buttons(has_prev : bool, has_next : bool):
	get_node(^"%NextButton").disabled = !has_next
	get_node(^"%PrevButton").disabled = !has_prev

func set_page_counter(current_page : int, max_pages : int):
	get_node(^"%PageLabel").text = str(current_page) + " / " + str(max_pages)

func set_data(p_data : Dictionary):
	data = p_data
	
	_image_display_container.hide()
	_text_display_container.hide()

	var result_description : String = ""
	
	if data.has("result_description"):
		result_description = data["result_description"]
	
	var rt : String = data["result_type"]
	
	if rt == "display_image":
		var img : Image = data["image"]
		var t : ImageTexture = ImageTexture.new()
		t.create_from_image(img)
		_image_display.texture = t
		_image_display_container.show()
	elif rt == "display_text":
		_text_display.text = data["result_description"]
		_text_display_container.show()
	
	get_node(^"%CurrentStepInfo").text = result_description

func _on_NextButton_pressed() -> void:
	emit_signal(@"next_button_pressed")
	
func _on_PrevButton_pressed() -> void:
	emit_signal(@"prev_button_pressed")

func _on_OpenButton_pressed() -> void:
	emit_signal(@"open_button_pressed")

func _ready() -> void:
	_image_display_container = get_node(^"%ImageDisplayContainer")
	_image_display = get_node(^"%ImageDisplay")
	_image_display_container.hide()
	
	_text_display_container = get_node(^"%TextResultDisplayContainer")
	_text_display = get_node(^"%TextResultLabel")
	_text_display_container.hide()
	
	on_working_state_changed(false)

func _on_CenterCameraButton_pressed() -> void:
	emit_signal(@"center_camera_button_pressed")

func _on_CameraSpeedSlider_value_changed(value: float) -> void:
	emit_signal(@"camera_Speed_slider_changed", value)

