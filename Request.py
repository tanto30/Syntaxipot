import urllib.parse as urlparse

class Request:
    """
    Request class description:
    This class represents a HTTP request in a way that it is easy to handle.
    This class does not have either queries or methods (except for the constructor), it contains only attributes.

    The class' attributes:
    ip - the ip of the client making the request
    port - the port of the client's socket which requested the server
    raw_request - the raw HTTP request.
    method - The method that was used (e.g. GET, POST etc.).
    path - The requested file (e.g /docs/index.html).
    query_params - The parameters of the query. For example, in the request 'GET /docs/index.html?qa=1&qa=2 HTTP/1.1'
                   the query_params is 'qa=1&qa=2'.
    headers - A dictionary that represents the headers of the request.
    POST_params_str - The parameters of the POST request as string(e.g. user=admin&pass=123).
    POST_params_dict - The  parameters of the POST request as dict(param:value, e.g. {'user':'admin', 'pass':'123'})
    """

    def __init__(self, ip, port, raw_request, method, path, headers, post_parameters, post_dict):
        """
        
        :param ip: e.g. '127.0.0.1'
        :param port: e.g. 5912 (unsure if int or str)
        :param raw_request: whole HTTP Request, with request line, headers and body. (string)
        :param method: e.g. 'GET' 
        :param path: whole path of url <path>;<params>?<query>#<fragment>
        :param headers: BaseHTTPRequestHandler.headers 
        :param post_parameters: e.g. user=admin&pass=123
        :param post_dict:  e.g. {'user':'admin', 'pass':'123'
        """
        self.ip = ip
        self.port = port
        self.raw_request = raw_request
        self.method = method
        # Parse the url into 6 components  <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
        url_parsed = urlparse.urlparse(path)
        self.path = url_parsed.path
        self.query_params = url_parsed.query

        self.POST_params_str = post_parameters
        self.POST_params_dict = post_dict

        # construct a dictionary containing the headers
        self.headers = dict(headers.items())
