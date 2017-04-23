import sys
import urllib.parse

from os import environ  # The environment variables.
from Request import Request


def generate_request():
    """Generates an instance of the Request class."""
    headers = get_headers()
    post_params, post_params_dict = get_post_params()
    raw_request = make_raw_request(headers, post_params)
    return Request(environ["REMOTE_ADDR"], environ["REMOTE_PORT"], raw_request,
                   environ["REQUEST_METHOD"],
                   environ["REQUEST_URI"], headers, post_params,
                   post_params_dict)


def make_raw_request(headers, post_params):
    """Makes the raw HTTP request using the environment variables."""
    raw_request = environ["REQUEST_METHOD"] + " " + \
                  environ["REQUEST_URI"] + \
                  " HTTP/1.1\r\n"  # The request line.
    # Adds the headers.
    for header in headers:
        raw_request += header + ": " + headers[header] + "\r\n"
    raw_request += "\r\n" + post_params
    return raw_request


def get_headers():
    """Gets the headers out of the environment variables.
    This function is necessary because the headers of a request are not provided in a convenient way such as
    a dictionary - each header is provided as an environment variable."""
    headers = {}
    for field in environ:
        # If an environment variable starts with HTTP_ it is a header.
        if field.startswith("HTTP_"):
            header_value = environ[field]
            header_key = parse_header(field)
            headers[header_key] = header_value
    return headers


def parse_header(field):
    """Parses a single header key and converts it to the way it appears on a HTTP request.
    This function is necessary because the headers' keys are provided in the environment variables
    not as they appear in a HTTP request.
    For example, it converts HTTP_USER_AGENT to User-Agent."""
    header_key = field[5:]  # Gets rid of the "HTTP_" prefix of the field.
    header_list = header_key.split("_")
    header_list = [string.capitalize() for string in header_list]
    return "-".join(header_list)


def get_post_params():
    """Returns the parameters provided to a POST request.
    These parameters are provided through STDIN."""
    if environ["REQUEST_METHOD"] == "POST":  # If the request is a POST request...
        post_params = sys.stdin.read()
        post_params_dict = urllib.parse.parse_qs(post_params)
        return post_params, post_params_dict

    else:
        return None, {}
