import urllib.request


def headers_dict_to_str(header_dict):
    header_str = ''
    for field, value in header_dict.items():
        header_str += '{}: {}\r\n'.format(field, value)
    return bytes(header_str, encoding='utf-8')


def response_to_bytes(resp):
    headers_bytes = headers_dict_to_str(dict(resp.info()))
    body = resp.read()
    return headers_bytes + b'\r\n' + body


def serve_page(request_obj):
    """
    :param request_obj: instance of Request.ClassifiedRequest
    :return: HTTP Response for the request as str 
    """
    # Full path to requested file
    url = "http://localhost" + request_obj.return_path
    # POST data as bytes object, None if request_obj.method = 'GET'
    data = request_obj.POST_params
    req = urllib.request.Request(url, data,
                                 request_obj.headers,
                                 method=request_obj.method)
    # TODO: Add HTTP Error handling, program crashes for example on HTTP Error 404
    resp = urllib.request.urlopen(req)
    resp_bytes = response_to_bytes(resp)
    return resp_bytes
