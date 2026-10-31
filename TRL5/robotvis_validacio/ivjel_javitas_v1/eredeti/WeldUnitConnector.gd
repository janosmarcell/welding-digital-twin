extends Node

enum LoginState {
	LOGIN_STATE_NONE = 0,
	LOGIN_STATE_LOGIN_REQUEST = 1,
	LOGIN_STATE_LOGGED_IN = 2,
	LOGIN_STATE_ERROR = 3,
};

enum CurrentDataQuery {
	CURRENT_DATA_QUERY_NONE = 0,
	CURRENT_DATA_QUERY_SYSTEM_DATA = 1,
};

enum WebSocketConnectionState {
	WEB_SOCKET_CONNECTION_NONE = 0,
	WEB_SOCKET_CONNECTION_CONNECTING = 1,
	WEB_SOCKET_CONNECTION_CONNECTED = 2,
};

var login_state : int = LoginState.LOGIN_STATE_NONE
var cookie : String = ""

var data_query : int = CurrentDataQuery.CURRENT_DATA_QUERY_NONE

var web_socket_connetion_state = WebSocketConnectionState.WEB_SOCKET_CONNECTION_NONE
var web_socket_connection : WebSocketClient

#function X() {
#    var s = {
#      STX: 2,
#      COMMANDEND: ';',
#      DELIMITER: ',',
#      RESULTDELIMITER: '=',
#      STRINGMAKER: '"'
#    };
#    this.Tag = {
#      SET: L,
#      GET: R,
#      FUNCTION: U,
#      NOTIFICATION: N,
#      ERROR: o
#    };

var http_request : HTTPRequest

func login() -> void:
	if login_state != LoginState.LOGIN_STATE_NONE:
		return
		
	login_state = LoginState.LOGIN_STATE_LOGIN_REQUEST
	
	#try logging in
	var body = "username=***&password=***"
	var error = http_request.request("https://10.192.70.129/login", [], false, HTTPClient.METHOD_POST, body)
	if error != OK:
		PLogger.log_error("WeldUnitConnector: An error occurred in the login() HTTP request. " + str(error))

func query_system_data() -> void:
	if login_state == LoginState.LOGIN_STATE_ERROR:
		PLogger.log_error("WeldUnitConnector: query_system_data(): LOGIN_STATE_ERROR!")
		return
	
	data_query = CurrentDataQuery.CURRENT_DATA_QUERY_SYSTEM_DATA
	
	var header : PoolStringArray = PoolStringArray()
	header.push_back("cookie:  " + cookie + ";")
	var error = http_request.request("https://10.192.70.129/actualSystemData/actualSystemData.html", header, false)
	if error != OK:
		PLogger.log_error("WeldUnitConnector: An error occurred in the query_system_data() HTTP request. " + str(error))
			

func _process(delta: float) -> void:
	if web_socket_connection:
		web_socket_connection.poll()

func connect_web_socket() -> void:
	PLogger.log_message("WeldUnitConnector: Web Socket: Connecting.")
	
	web_socket_connection = WebSocketClient.new()
	web_socket_connection.verify_ssl = false
	web_socket_connection.connect("data_received", self, "ws_data_received")
	var protocols : PoolStringArray = PoolStringArray()
	protocols.push_back("sec-websocket-protocol")
	var header : PoolStringArray = PoolStringArray()
	header.push_back("cookie:  " + cookie + ";")
	web_socket_connection.connect_to_url("wss://10.192.70.129/WSspeedNet", protocols, false, header)
	
	#connect_to_url(url: String, protocols: PoolStringArray = PoolStringArray(  ), gd_mp_api: bool = false, custom_headers: PoolStringArray = PoolStringArray(  ))

func setup() -> void:
	if login_state == LoginState.LOGIN_STATE_NONE:
		PLogger.log_message("WeldUnitConnector: setup(): Connecting and logging in to the weld unit.!")
		login()

func _ready() -> void:
	http_request = get_node("HTTPRequest")
	http_request.connect("request_completed", self, "_on_HTTPRequest_request_completed")
	
	call_deferred("setup")
	
	#https://10.192.70.129/actualSystemData/actualSystemData.html
	#https://10.192.70.129/cgi-bin/getJob.cgi?151
	#file:///home/relintai/Downloads/tags.xml
	#https://10.192.70.129/cgi-bin/getJoblist.cgi
	#https://10.192.70.129/cgi-bin/getTag.cgi?44&1687354259210
	#https://10.192.70.129/visualize/visualize.html
	#https://10.192.70.129/cgi-bin/grab.cgi?1687356038395
	#https://10.192.70.129/dyn/output.png?1687356039645
	


func _on_HTTPRequest_request_completed(result: int, response_code: int, headers: PoolStringArray, body: PoolByteArray) -> void:
	if result != OK:
		PLogger.log_error("WeldUnitConnector: _on_HTTPRequest_request_completed: result is not OK! " + str(result))
		return

	if response_code != 200:
		PLogger.log_warning("WeldUnitConnector: _on_HTTPRequest_request_completed: response_code is not 200! " + str(response_code))
	

	if login_state == LoginState.LOGIN_STATE_LOGIN_REQUEST:
		for i in range(headers.size()):
			var h : String = headers[i]
			
			if h.begins_with("SET-Cookie: "):
				
				var c : String = h.replace_first("SET-Cookie: ", "")
				
				var csp : PoolStringArray = c.split(";")
				
				for j in range(csp.size()):
					var cs : String = csp[j]
					cs = cs.strip_edges()
					
					if cs.begins_with("sessionid="):
						cookie = cs
				
						PLogger.log_message("WeldUnitConnector: Session cookie successfully obtained from the weld unit!")
						login_state = LoginState.LOGIN_STATE_LOGGED_IN
						#call_deferred("query_system_data")
						call_deferred("connect_web_socket")
						return
				
		PLogger.log_error("WeldUnitConnector: Wasn't able to get a Session cookie from the weld unit!")
		login_state = LoginState.LOGIN_STATE_ERROR
		return
		
	if data_query == CurrentDataQuery.CURRENT_DATA_QUERY_SYSTEM_DATA:
		var body_str : String = body.get_string_from_utf8()
		
		PLogger.log_message("WeldUnitConnector: CURRENT_DATA_QUERY_SYSTEM_DATA:")
		PLogger.log_message(body_str)
		PLogger.log_message(str(headers))
		PLogger.log_message(str(response_code))
		PLogger.log_message(str(result))


func ws_data_received() -> void:
	print(web_socket_connection.get_packet().get_string_from_utf8())

