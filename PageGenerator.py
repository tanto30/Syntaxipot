def sqli_error_page(query):
    generated_sqli_path = "fake_sqli_page.txt"
    with open(generated_sqli_path, "w") as wfile:
        rfile = open("fake_page.txt")
        rfile_contents = rfile.read()
        wfile.write(rfile_contents.format(query=query))
        rfile.close()
    return generated_sqli_path


def generate_page_filename(query, vuln_type):
    if vuln_type == "sqli":
        return sqli_error_page(query)
    else:
        return "fake_page.txt"
