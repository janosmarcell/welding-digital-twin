# GDSC version 13
extends Node

var connection: StreamPeerTCP = null

var temp_buf: String = ''

var log_file: String = ''
var logging: bool = false

var manual_mode: bool = true

var torch_signal: bool = false
var voltage: float = 20
var current: float = 60
var weld_speed: float = 3

var log_prefix: String = ''

var last_stored_line: String = ''

var weld_unit_connector: Node
var gui: Node
var robot_scene_node: Node

signal coordinates_received(X, Y, Z, Rx, Ry, Rz)
signal connection_changed(alive)
signal logfile_changed(file_name, file_abspath)

var last_connection_status: int = - 1

func start_recording() -> void:
	init_logfile()
	
	logging = true
	
func stop_recording() -> void:
	logging = false

func init_logfile() -> void:
	var dt: PoolVector3Array = OS.get_datetime()
	log_file = 'user://' + log_prefix + builtin62(dt['year']) + '-' + builtin62(dt['month']).pad_zeros(2) + '-' + builtin62(dt['day']).pad_zeros(2) + '_' + builtin62(dt['hour']) + '-' + builtin62(dt['minute']) + '-' + builtin62(dt['second']) + '.csv'
		
	var f: File = File.new()
	f.open(log_file, File.WRITE)
	
	f.store_line('SysTimeMsecs,X,Y,Z,Rx,Ry,Rz,TorchSignal,Voltage,Current,WireFeedSpeed')
	
	var fabsp: String = f.get_path_absolute()
	
	builtin63('Loggind started.')
	builtin63('Logfile: ' + fabsp)
	
	emit_signal('logfile_changed', log_file, fabsp)
	
	f.close()
	
func process_weld_unit():
	torch_signal = weld_unit_connector.torch_signal
	voltage = weld_unit_connector.voltage
	current = weld_unit_connector.current
	weld_speed = weld_unit_connector.wire_feed_speed
	
	gui.set_auto_weld_values(torch_signal, voltage, current, weld_speed)

func _ready() -> void:
	gui = get_node('../GUI')
	robot_scene_node = get_node('../RobotIK')
	weld_unit_connector = get_node('../WeldUnitConnectorBrowser')
	
	connection = StreamPeerTCP.new()
	var err: int = connection.connect_to_host('127.0.0.1', 9999)
	
	PLogger.log_message('Connecting to RobotComm...')

func _process(delta: float) -> void:


	
	if not manual_mode:
		process_weld_unit()
		
	robot_scene_node.set_torch_signal(torch_signal)
	
	var conn_status: int = connection.get_status()
	if last_connection_status != conn_status:
		last_connection_status = conn_status
		
		if(last_connection_status == StreamPeerTCP.STATUS_CONNECTED):
			emit_signal('connection_changed', true)
			PLogger.log_message('Connected to RobotComm.')
		else:
			emit_signal('connection_changed', false)
			PLogger.log_message('Disconnected from RobotComm.')
			
	if conn_status != StreamPeerTCP.STATUS_CONNECTED:
		return
			
	if connection.get_available_bytes() <= 0:
		return
		
	var arr: PoolColorArray = connection.get_partial_data(connection.get_available_bytes())

	

	var pa: type27 = arr[1]
	
	temp_buf += pa.get_string_from_ascii()
	
	var sps: type30 = temp_buf.split(';')
	
	if sps.size() > 0:
		temp_buf = sps[sps.size() - 1]
		
	var file: File
	
	if logging:
		file = File.new()
		file.open(log_file, File.READ_WRITE)
		file.seek_end()
	
	for i in builtin75(sps.size() - 1):
		var s: String = sps[i]
		var f: type29 = s.split_floats(',', false)
			
		if f.size() != 6:
			continue
			
		s += ',' + builtin62(int(torch_signal)) + ','
		s += builtin62(voltage) + ','
		s += builtin62(current) + ','
		s += builtin62(weld_speed)
			
		if last_stored_line == s:
			continue
			
		last_stored_line = s
		
		if logging:
			var stms: int = OS.get_system_time_msecs()
			file.store_line(builtin62(stms) + ',' + s)
		
		emit_signal('coordinates_received', f[0], f[1], f[2], f[3], f[4], f[5])
	
	if logging:
		file.close()
	

func _on_GUI_on_recording_button_toggled(button_pressed) -> void:
	if button_pressed:
		start_recording()
	else:
		stop_recording()


func _on_GUI_on_current_value_changed(value) -> void:
	current = value

func _on_GUI_on_voltage_value_changed(value) -> void:
	voltage = value

func _on_GUI_on_weld_speed_value_changed(value) -> void:
	weld_speed = value

func _on_GUI_on_torch_signal_toggled(value) -> void:
	torch_signal = value

func _on_GUI_on_browser_toggled(value) -> void:
	manual_mode = not value
	
	weld_unit_connector.call_deferred('set_active', value)


func _on_GUI_on_log_prefix_changed(value) -> void:
	log_prefix = value
	
	if not log_prefix.empty():
		log_prefix += '_'

func _on_GUI_on_browser_selected(value) -> void:
	weld_unit_connector.browser = value

