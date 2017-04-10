import urllib.parse as urlparse
import re

from subprocess import check_output


def sanitize(shell_command):
    # TODO: fix sanitize to not remove relavent query string input.
    """
    :param shell_command: unsanitized string
    :return: string containing only alphanumeric characters, periods, underscores, dashs
    """
    return re.sub('[^\w._\-]', '', shell_command)


def handle_generic(request_obj):
    with open(request_obj.path, "rb") as f:
        file_contents = f.read()
    return file_contents


def handle_php(request_obj):
    params_str = sanitize(request_obj.query_parameters_str)
    params = params_str.split('&')
    return check_output(['php-cgi', '-f', request_obj.path, *params])


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
