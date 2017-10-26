import urllib.parse


class Request:
    """
    Request class description:
    This class represents a HTTP classified_request in a way that it is easy to handle.
    This class does not have either queries or methods (except for the constructor), it contains only attributes.

    The class' attributes:
    ip - the ip of the client making the classified_request
    port - the port of the client's socket which requested the server
    raw_request - the raw HTTP classified_request.
    method - The method that was used (e.g. GET, POST etc.).
    path - The requested file (e.g /docs/index.html).
    query_params - The parameters of the query. For example, in the classified_request 'GET /docs/index.html?qa=1&qa=2 HTTP/1.1'
                   the query_params is 'qa=1&qa=2'.
    headers - A dictionary that represents the headers of the classified_request.
    POST_params - The parameters of the POST classified_request as bytes(e.g. user=admin&pass=123).
                        None if classified_request.method = 'GET'
    """

    def __init__(self, ip, port, raw_request, method, full_url, headers,
                 post_parameters):
        """
        
        :param ip: e.g. '127.0.0.1'
        :param port: e.g. 5912 (unsure if int or str)
        :param raw_request: whole HTTP Request, with classified_request line, headers and body. (string)
        :param method: e.g. 'GET' 
        :param full_url: whole path of url <path>;<params>?<query>#<fragment>
        :param headers: BaseHTTPRequestHandler.headers 
        :param post_parameters: e.g. user=admin&pass=123
        """
        self.ip = ip
        self.port = port
        self.raw_request = raw_request
        self.method = method
        # Parse the url into 6 components  <scheme>://<netloc>/<full_url>;<params>?<query>#<fragment>
        full_url = urllib.parse.unquote_plus(full_url)
        self.full_url = urllib.parse.urlparse(full_url)
        self.query_params = full_url.query
        self.POST_params = post_parameters
        # construct a dictionary containing the headers
        self.headers = headers

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return self.__repr__()


class ClassifiedRequest(Request):
    """
    This class represents an HTTP classified_request which can be easily handled,
    Child Class of classified_request, ClassifiedRequest is intended to be used by the Classifier,
    to check if a classified_request is malicious and what type of attack it is if is malicious.
    """

    def __init__(self, request, malicious, attack_type):
        """
        :param malicious: boolean, True if classified_request is malicious
        :param attack_type: string, the type of the attack, e.g., 'xss', 'sqli',
        or an empty string if not malicious
        """
        Request.__init__(self, request.ip, request.port, request.raw_request,
                         request.method, request.full_url, request.headers,
                         request.POST_params)

        self.query_params = request.query_params
        self.malicious = malicious
        self.attack_type = attack_type

    def is_malicious(self):
        return self.malicious
