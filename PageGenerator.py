import os.path


def sqli_error_page(query):
    file_name = "fake_page_" + str(hash(query))
    if not os.path.isfile(file_name):
        with open(file_name, "rw") as f:
            fpage = open("fake_page.txt")
            page = fpage.read()
            f.write(page.format(query=query))
            fpage.close()
    return file_name


def generate_page_filename(query, vuln_type):
    if vuln_type == "sqli":
        filename = sqli_error_page(query)
    else:
        return "fake_page.txt"
