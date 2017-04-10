import urllib.parse as urlparse
import re

from subprocess import check_output


def sanitize(shell_command):
    # TODO: make sanitize as secure as possible
    """
    :param shell_command: unsanitized string
    :return: string containing only alphanumeric characters, periods, underscores, dashes, equal marks
    """
    return re.sub('[^\w._\-\=]', '', shell_command)


def handle_generic(request_obj):
    """
    Handles all other file types, (e.g., .htm, .html, .txt)
    :param request_obj:  Request class from Request.py
    :return: string of file contents.
    """
    with open(request_obj.path, "rb") as f:
        file_contents = f.read()
    return file_contents


def handle_php(request_obj):
    """
    :param request_obj:  Request class from Request.py
    :return: string of generated html file by executing php.
    """
    query_params = sanitize(request_obj.query_params)
    params = query_params.split('&')
    sanitized_params = [sanitize(param) for param in params]
    return check_output(['php-cgi', '-f', request_obj.path, *sanitized_params])


def serve_file(request_obj):
    """
    :param request_obj: instance of Request 
    :return: HTML content to put in response to client
    """

    if request_obj.path.endswith(".php"):
        out = handle_php(request_obj)
    else:
        out = handle_generic(request_obj)
    return out
