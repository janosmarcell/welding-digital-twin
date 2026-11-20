extends Node

var is_running : bool = false
var last_log_version : int = 0
var last_log_text : String = ""

var last_result_version : int = 0
var result : Array = Array()

var template_mesh_path : String
var object_mesh_path : String

signal new_log(log_text)
signal results_changed(results)
signal working_state_changed(state)

var _processor : Node = null

func request_load(p_template_mesh_path : String, p_object_mesh_path : String):
	call_deferred(@"run", p_template_mesh_path, p_object_mesh_path)

func cancel():
	_processor.cancel()

func run(p_template_mesh_path : String, p_object_mesh_path : String):
	template_mesh_path = p_template_mesh_path
	object_mesh_path = p_object_mesh_path
	
	_processor.cancel()
	_processor.run(template_mesh_path, object_mesh_path)
	# The python extension does not support signals yet
	is_running = true
	
	last_log_version = 0
	last_log_text = ""
	
	last_result_version = 0
	result = Array()
	
	emit_signal(@"new_log", last_log_text)
	emit_signal(@"results_changed", result)
	emit_signal(@"working_state_changed", true)
	
	set_process(true)
	
func _process(delta: float) -> void:
	if _processor.work_finished:
		_on_generator_work_finished()
		set_process(false)
	
	var lv : int = _processor.get_log_version()
	if last_log_version != lv:
		last_log_version = lv
		last_log_text = _processor.get_log()
		emit_signal(@"new_log", last_log_text)
		print(last_log_text)
		
	var rv : int = _processor.get_results_version()
	if last_result_version != rv:
		last_result_version = rv
		result = _processor.get_results()
		emit_signal(@"results_changed", result)
		print("Res!")
	
func _on_generator_work_finished() -> void:
	last_log_version = _processor.get_log_version()
	last_log_text = _processor.get_log()
	
	emit_signal(@"new_log", last_log_text)
	
	last_result_version = _processor.get_results_version()
	result = _processor.get_results()
	
	emit_signal(@"results_changed", result)
	
	emit_signal(@"working_state_changed", false)
	
	is_running = false
	set_process(false)

func _ready():
	_processor = $PointCloudProcessor
