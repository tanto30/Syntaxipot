import os.path


def sqli_error_page(query):
    file_name = "fake_sqli_error_page.html"
    with open(file_name, "w") as f:
        fpage = open("fake_page.txt")
        page = fpage.read()
        f.write(page.format(query=query))
        fpage.close()
    return file_name


def generate_page_filename(query, vuln_type):
    if vuln_type == "sqli":
        return sqli_error_page(query)
    else:
        return "fake_page.txt"
