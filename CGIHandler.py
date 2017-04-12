import os
import re

from subprocess import run, PIPE, STDOUT


def sanitize(shell_command):
    # TODO: make sanitize as secure as possible
    """
    :param shell_command: unsanitized string
    :return: string containing only alphanumeric characters, periods, underscores, dashes, equal marks
    """
    return re.sub('[^\w._\-\=]', '', shell_command)

def setup_environment(request_obj):
    h = request_obj.headers
    if 'Cookie' not in h:
        h['Cookie'] = ''
    env_var_to_attribute = {
                            "HTTP_COOKIE": h['Cookie'],
                            "HTTP_USER_AGENT": h['User-Agent'],
                            "PATH_INFO": "/",
                            "QUERY_STRING": request_obj.query_params,
                            "REMOTE_ADDR": request_obj.ip,
                            "REMOTE_HOST": request_obj.ip,
                            "REQUEST_METHOD": request_obj.method,
                            "SCRIPT_FILENAME": os.path.abspath(request_obj.path),
                            "SCRIPT_NAME": request_obj.path.split("/")[-1],
                            "SERVER_NAME": "SyntaxiPOT",
                            "SERVER_SOFTWARE": "Python 3.6"
                            }

    if request_obj.method == "POST":
        new_env_var_to_attribute = {"CONTENT_TYPE": "text/html",
                                    "CONTENT_LENGTH": len(bytes(request_obj.POST_params_str, 'utf-8'))}
        env_var_to_attribute.update(new_env_var_to_attribute)

    for var, value in env_var_to_attribute.items():
        os.environ[var] = value

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
    setup_environment(request_obj)
    query_params = sanitize(request_obj.query_params)
    params = query_params.split('&')
    sanitized_params = [sanitize(param) for param in params]
    completed_out = run(['php-cgi', '-f', request_obj.path, *sanitized_params], shell=True, stdout=PIPE, stderr=PIPE)
    return completed_out.stdout


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
