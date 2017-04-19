import http.client


def response_to_str(resp):
	header = ''
	for field, value in resp.getheaders():
		header += '{}: {}\r\n'.format(field, value)
	body = resp.read()
	return str(header) + '\r\n' + str(body)


def serve_page(request):
	request.headers['X-Forwarded-For'] = request.ip
	connection = http.client.HTTPConnection('localhost', 80)
	connection.request(request.method, request.path, request.POST_params_str,
					   request.headers)
	response = connection.getresponse()
	return response_to_str(response)
