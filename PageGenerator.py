import pickle

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
    url = request.full_url
    with open('filename.pickle', 'rb') as handle:
        xss_url_to_ip = pickle.load(handle)
    # New XSS attack - add to banned list.
    if url not in xss_url_to_ip:
        xss_url_to_ip[url] = request.ip
        with open('filename.pickle', 'wb') as handle:
            pickle.dump(xss_url_to_ip, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return url
    # Old XSS attack, if attacker requested url, give him the malicious url
    if url in xss_url_to_ip and xss_url_to_ip[url] == request.ip:
        return url
    # Case IP is of victim, return notification page.
    if url in xss_url_to_ip and xss_url_to_ip[url] != request.ip:
        return "XSSAttackedNote.html"
