import urllib.error
import urllib.parse
import urllib.request


def headers_dict_to_str(header_dict):
    header_str = ''
    for field, value in header_dict.items():
        header = '{}: {}\r\n'.format(field, value)
        if field == "Status":
            # Status must be the first header
            header_str = header + header_str
        else:
            header_str += header
    return bytes(header_str, encoding='utf-8')


def response_to_bytes(resp):
    """
    :param resp: urllib.request.Response instance
    :return: bytes of response
    """
    header_dict = dict(resp.info())
    if isinstance(resp, urllib.error.HTTPError):
        header_dict["Status"] = '{} {}'.format(resp.code, resp.msg)
    headers_bytes = headers_dict_to_str(header_dict)
    body = resp.read()
    return headers_bytes + b'\r\n' + body


def serve_page(request_obj):
    """
    :param request_obj: instance of Request.ClassifiedRequest
    :return: HTTP Response for the request as bytes 
    """
    # Full path to requested file
    url = "http://127.0.0.1" + urllib.parse.quote(request_obj.return_path)
    # POST data as bytes object, None if request_obj.method = 'GET'
    data = request_obj.POST_params
    req = urllib.request.Request(url, data,
                                 request_obj.headers,
                                 method=request_obj.method)
    try:
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        resp = e
    resp_bytes = response_to_bytes(resp)
    return resp_bytes
