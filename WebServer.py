import CGIHandler
import urllib.parse as urlparse


from os.path import isfile
from Classifier import is_malicious
from PageGenerator import generate_page
from cgi import parse_header, parse_multipart
from http.server import BaseHTTPRequestHandler, HTTPServer


#  HTTPRequestHandler class
class TestHTTPServerRequestHandler(BaseHTTPRequestHandler):
    # GET
    @staticmethod
    def __check_path(request_path):
        """@:return True if requests an exisiting page, valid HTTP request, according to protocol"""
        requested_file = urlparse.urlparse(request_path).path
        if not isfile("." + requested_file):
            return False
        return True

    def is_valid(self):
        """Check if get request is valid (currently just check if file exists)
            Error handling and response should be done here
        """
        requested_file = urlparse.urlparse(self.path).path
        if not TestHTTPServerRequestHandler.__check_path(requested_file):
            self.send_error(404)
            return False
        return True

    def parse_POST(self):
        """ Converts post data for example(pass=1234&id=123456) to dict {'pass': 12345, 'id': 123456}
            :returns post variables dict and post data as string """
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':  # TODO: Handle this case later.
            postvars = parse_multipart(self.rfile, pdict)
            post_string = ""
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            post_string = str(self.rfile.read(length), "utf-8")
            postvars = urlparse.parse_qs(post_string,
                                         keep_blank_values=1)
        else:
            postvars = {}
            post_string = ""
        return postvars, post_string

    def send_malicious_response(self, generated_page):
        """
        Returns page generated by Yoav&Talmon page generator.
        Actual response code/headers content will be changed in the future
        """

        # 200 OK - normal http response, meaning server served the requested page
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        # Write content as utf-8 data
        self.wfile.write(bytes(generated_page, "utf-8"))

    def send_nonmalicious_response(self):
        """
          Returns page requested by client.
          """
        # Parse path of file
        requested_file_path = "." + urlparse.urlparse(self.path).path
        with open(requested_file_path, "rb") as file:
            requested_file = file.read()
        # 200 OK - normal http response, meaning server served the requested page
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')  # We will probably need to add more headers.
        self.end_headers()

        # Send message back to client
        # Write content as utf-8 data
        self.wfile.write(requested_file)

    def do_GET(self):
        """
        Handle GET requests
        Check if request is valid HTTP request
        Check if request is non-malicious HTTP request
        return Appropriate response
        """
        # HTTP request str ends with two CRLF's (\r\n\r\n)
        http_request_str = self.requestline + "\r\n" + str(self.headers)
        if self.is_valid():
            # Currently a valid HTTP request
            if not is_malicious(http_request_str):
                # Currently non-malicious HTTP request
                self.send_nonmalicious_response()
            else:
                # Currently MALICIOUS HTTP request
                tmp_page = generate_page(http_request_str)
                # tmp_page should be written and saved inside the server's filesystem
                self.send_malicious_response(tmp_page)

    def do_POST(self):
        """
        Handle POST requests
        Check if request is valid HTTP request
        Check if request is non-malicious HTTP request
        return Appropriate response
        """
        if self.is_valid():
            postvars, post_string = self.parse_POST()
            # HTTP request str ends with to CRLF's (\r\n\r\n), so no need to add them between the post string
            http_request_str = self.requestline + "\r\n" + str(self.headers) + post_string
            if not is_malicious(http_request_str):
                # Currently non-malicious HTTP request
                self.send_nonmalicious_response()
            else:
                # Currently MALICIOUS HTTP request
                tmp_page = generate_page(http_request_str)
                # tmp_page should be written and saved inside the server's filesystem
                self.send_malicious_response(tmp_page)


def run():
    print('Starting Server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, TestHTTPServerRequestHandler)
    print('Server Running on: {}:{}'.format(server_address[0], server_address[1]))
    httpd.serve_forever()


run()
