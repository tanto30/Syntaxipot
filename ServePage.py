import http.client


def response_to_str(resp):
    status = 'HTTP /1.{} {} {}\r\n'.format(resp.version, resp.status, resp.reason)
    header = ''
    for field, value in resp.getheaders():
        header += '{}: {}\r\n'.format(field, value)
    body = resp.read()
    return status + header + '\r\n' + body


def serve_page(request):
    request.headers['X-Forwarded-For'] = request.ip
    connection = http.client.HTTPConnection('localhost', 80)
    connection.request(request.method, request.path, request.POST_params_str, request.headers)
    response = connection.getresponse()
    return response_to_str(response)
