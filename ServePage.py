import urllib.request


def headers_dict_to_str(header_dict):
	header_str = ''
	for field, value in header_dict.items():
		header_str += '{}: {}\r\n'.format(field, value)
	return header_str


def response_to_str(resp):
	headers = headers_dict_to_str(dict(resp.info()))
	body = str(resp.read(), encoding='utf-8')
	return headers + '\r\n' + body


def serve_page(request_obj):
	"""
	:param request_obj: instance of Request.ClassifiedRequest
	:return: HTTP Response for the request as str 
	"""
	# Full path to requested file
	url = "http://127.0.0.1" + request_obj.return_path
	# POST data as bytes object, None if request_obj.method = 'GET'
	data = request_obj.POST_params_bytes
	req = urllib.request.Request(url, data,
								 request_obj.headers,
								 method=request_obj.method)
	resp = urllib.request.urlopen(req)
	resp_str = response_to_str(resp)
	return resp_str
