import pickle
from _md5 import md5

from Request import ClassifiedRequest


def sqli_error_page(query):
    generated_sqli_path = "fake_sqli_page.html"
    with open("..\\htdocs\\" + generated_sqli_path, "w") as wfile:
        rfile = open("fake_page.txt")
        rfile_contents = rfile.read()
        wfile.write(rfile_contents.format(query=query))
        rfile.close()
    return generated_sqli_path


def generate_page_filename(request: ClassifiedRequest):
    vuln_type = request.attack_type
    if vuln_type == "sqli":
        return sqli_error_page(request.query_params)
    elif vuln_type == "xss":
        return xss_page(request)
    else:
        return "fake_page.txt"


def xss_page(request):
    url_hash = md5(request.path).hexdigest()
    with open('filename.pickle', 'rb') as handle:
        xss_url_to_ip = pickle.load(handle)
    # New XSS attack - add to banned list.
    if url_hash not in xss_url_to_ip:
        xss_url_to_ip[url_hash] = request.ip
        with open('filename.pickle', 'wb') as handle:
            pickle.dump(xss_url_to_ip, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return request.path
    # Old XSS attack, victim user - report
    if url_hash in xss_url_to_ip and xss_url_to_ip[url_hash] == request.ip:
        return request.path
    if url_hash in xss_url_to_ip and xss_url_to_ip[url_hash] != request.ip:
        return "XSSAttackedNote.html"
