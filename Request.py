import email
from io import StringIO


class Request:
    """
    Request class description:
    This class represents a HTTP request in a way that it is easy to handle.
    This class does not have either queries or methods (except for the constructor), it contains only attributes.

    The class' attributes:
    raw_request - the raw HTTP request.
    method - The method that was used (e.g GET, POST etc.).
    path - The requested file (e.g /docs/index.html).
    query_params - The parameters of the query. For example, in the request 'GET /docs/index.html?qa=1&qa=2 HTTP/1.1'
                   the query_params is 'qa=1&qa=2'.
    headers - A dictionary that represents the headers of the request.
    POST_params - The parameters of the POST request (they appear in the bottom of a HTTP request).
    """

    def __init__(self, raw_request):
        self.raw_request = raw_request

        request_line, rest_of_request = raw_request.split('\r\n', 1)
        raw_headers, self.POST_params = rest_of_request.split("\r\n\r\n", 1)

        split_request_line = request_line.split(" ")
        self.method, query = split_request_line[0], split_request_line[1]
        query_split = query.split("?")
        self.path = query_split[0]
        self.query_params = ""
        if len(query_split) > 1:
            self.query_params = query_split[1]

        # construct a message from the request string
        message = email.message_from_file(StringIO(raw_headers))

        # construct a dictionary containing the headers
        self.headers = dict(message.items())
