#import http.client
import urllib.request


def headers_dict_to_str(header_dict):
    header_str = ''
    for field, value in header_dict:
        header_str += '{}: {}\r\n'.format(field, value)
    return header_str


def response_to_str(resp):
    with open("debug.txt", 'a') as f:
        f.write("STARTED RESPONSE_TWO_STR\n")
    headers = headers_dict_to_str(dict(resp.info()))
    body = str(resp.read(), encoding='utf-8')
    with open("debug.txt", 'a') as f:
        f.write("FINISHED RESPONSE_TO_STR\n")
    return headers + '\r\n' + body


def serve_page(request_obj):
    """
    :param request_obj: instance of Request.ClassifiedRequest
    :return: HTTP Response for the request as str 
    """
    # request.headers['X-Forwarded-For'] = request.ip
    # connection = http.client.HTTPConnection('localhost', 80)
    # connection.request(request.method, request.path, request.POST_params_str,
    #                  request.headers)
    # Full path to requested file
    with open("debug.txt", 'a') as f:
        f.write("STARTED SERVE PAGE\n")
    url = "http://localhost" + request_obj.return_path
    # POST data as bytes object, None if request_obj.method = 'GET'
    data = request_obj.POST_params_bytes
    req = urllib.request.Request(url, data,
                                 request_obj.headers, origin_req_host=request_obj.ip,
                                 method=request_obj.method)

    resp = urllib.request.urlopen(req)
    resp_str = response_to_str(resp)
    with open("debug.txt", 'a') as f:
        f.write("FINISHED SERVER PAGE\n")
    return resp_str
