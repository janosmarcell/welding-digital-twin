extends Node

var results : Array = Array()
var log_text : String = ""

var current_result_index : int = 0

var _control_bar : Control = null
var _result_data_viewer : Spatial = null

func apply_result():
	if current_result_index >= results.size():
		return
		
	_control_bar.set_data(results[current_result_index])
	_result_data_viewer.set_data(results[current_result_index])
	
	update_prev_next_buttons()
	update_page_counters()
	
func update_prev_next_buttons():
	_control_bar.set_prev_next_buttons(current_result_index > 0, current_result_index < results.size() - 1)

func update_page_counters():
	if results.size() == 0:
		_control_bar.set_page_counter(0, 0)
	else:
		_control_bar.set_page_counter(current_result_index + 1, results.size())

func _on_Processor_new_log(p_log_text : String) -> void:
	log_text = p_log_text
	
	_control_bar.on_new_log(log_text)

func _on_Processor_results_changed(p_results : Array) -> void:
	var orig_results_size : int = results.size()
	
	results = p_results
	
	if results.size() < current_result_index:
		current_result_index = 0
		
		apply_result()
	else:
		if orig_results_size == 0:
			apply_result()
		else:
			update_prev_next_buttons()
			update_page_counters()

func _on_ControlBar_next_button_pressed() -> void:
	if results.size() - 1 == current_result_index:
		return
		
	current_result_index += 1
	apply_result()

func _on_ControlBar_prev_button_pressed() -> void:
	if current_result_index == 0:
		return
		
	current_result_index -= 1
	apply_result()

func _on_ControlBar_open_button_pressed() -> void:
	$FileOpener.show()

func _ready() -> void:
	_control_bar = $ControlBar
	_result_data_viewer = $ResultDataViewer
	
	update_prev_next_buttons()
	update_page_counters()

func _on_Processor_working_state_changed(state : bool) -> void:
	_control_bar.on_working_state_changed(state)

func _on_FileOpener_load_requested(template_model_path, object_model_path) -> void:
	$Processor.request_load(template_model_path, object_model_path)
