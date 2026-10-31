# GDSC version 13
extends HBoxContainer

export(PoolIntArray) var auto_voltage_label_path: PoolIntArray
export(PoolIntArray) var auto_current_label_path: PoolIntArray
export(PoolIntArray) var auto_ws_label_path: PoolIntArray
export(PoolIntArray) var auto_torch_signal_cb_path: PoolIntArray

signal on_recording_button_toggled(button_pressed)

signal on_browser_toggled(value)
signal on_browser_selected(value)

signal on_torch_signal_toggled(value)
signal on_current_value_changed(value)
signal on_voltage_value_changed(value)
signal on_weld_speed_value_changed(value)

signal on_log_prefix_changed(value)

var _auto_torch_signal_cb: CheckBox
var _auto_voltage_label: Label
var _auto_current_label: Label
var _auto_ws_label: Label

func _ready() -> void:
	_auto_torch_signal_cb = get_node(auto_torch_signal_cb_path)
	_auto_voltage_label = get_node(auto_voltage_label_path)
	_auto_current_label = get_node(auto_current_label_path)
	_auto_ws_label = get_node(auto_ws_label_path)

func _on_Connector_connection_changed(alive) -> void:
	var l: Label = get_node('VBoxContainer/PanelContainer/MarginContainer/VBoxContainer/HBoxContainer/ConnectionLabel')
		
	if alive:
		l.text = 'Connected'
	else:
		l.text = 'Not Connected'


func _on_OpenLogsFolder_pressed() -> void:
	OS.shell_open(ProjectSettings.globalize_path('user://'))


func _on_CheckButton_toggled(button_pressed: bool) -> void:
	emit_signal('on_recording_button_toggled', button_pressed)


func _on_Connector_logfile_changed(log_file, file_abspath) -> void:
	var lb: LinkButton = get_node('VBoxContainer2/HBoxContainer/LogPathButton')
	lb.text = log_file
	lb.uri = file_abspath


func _on_CurrentSpinBox_value_changed(value: float) -> void:
	emit_signal('on_current_value_changed', value)


func _on_VoltageSpinBox_value_changed(value: float) -> void:
	emit_signal('on_voltage_value_changed', value)


func _on_WeldSpeedSpinBox_value_changed(value: float) -> void:
	emit_signal('on_weld_speed_value_changed', value)


func _on_TorchSignalButton_toggled(button_pressed: bool) -> void:
	emit_signal('on_torch_signal_toggled', button_pressed)


func _on_BrowserCheckButton_toggled(button_pressed: bool) -> void:
	emit_signal('on_browser_toggled', button_pressed)

func set_auto_weld_values(torch_signal: bool, voltage: float, current: float, weld_speed: float):
	_auto_torch_signal_cb.pressed = torch_signal
	_auto_voltage_label.text = builtin62(voltage) + ' V'
	_auto_current_label.text = builtin62(current) + ' A'
	_auto_ws_label.text = builtin62(weld_speed) + ' m/min'

func _on_PrefixLE_text_entered(new_text: String) -> void:
	emit_signal('on_log_prefix_changed', new_text)

func _on_PrefixLE_text_changed(new_text: String) -> void:
	emit_signal('on_log_prefix_changed', new_text)

func _on_BrowserSelectOB_item_selected(index: int) -> void:
	if index == - 1:
		index = 0
		
	emit_signal('on_browser_selected', index)

