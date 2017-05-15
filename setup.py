from os.path import isfile
from re import sub
from sys import stderr, modules

import pip

full_apache_path = input("Enter full path to the apache server: (e.g. "
                         "C:\\apache)\n")

project_files = ["Classifier.py", "fake_page.txt", "logger.py",
                 "PageGenerator.py", "Request.py", "RequestGenerator.py",
                 "ServePage.py", "Syntaxipot.py"]


def unpack_project():
    fail_count = 0
    for filename in project_files:
        if isfile(filename):
            print("Unpacking File: {}".format(filename))
            bin_filename = full_apache_path + "\\cgi-bin\\" + filename
            with open(filename) as f_read, \
                    open(bin_filename) as f_write:
                f_write.write(f_read.read())
        else:
            print("[ERROR] File '{}' not found".format(filename), file=stderr)
            fail_count += 1
    return fail_count


def modify_httpd_conf():
    conf_path = full_apache_path + "\\conf\\httpd.conf"
    if not isfile(conf_path):
        print("[ERROR] Apache http config: '{}' not found".format(
            conf_path), file=stderr)

    with open(conf_path, "r") as f:
        httpdconf_lines = f.readlines()
        for i in range(len(httpdconf_lines)):
            if "AddHandler cgi-script" in httpdconf_lines[i]:
                httpdconf_lines[i] = httpdconf_lines[i].strip() + " .py\n"
            elif "AllowOverride None" in httpdconf_lines[i]:
                sub(r"None", "All", httpdconf_lines[i])

    with open(full_apache_path + "\\conf\\httpd.conf", "w") as f:
        httpdconf_lines += [
            "RewriteEngine on\n",
            "RewriteCond %{REMOTE_ADDR} !127.0.0.1\n",
            "RewriteRule \"(.*)\" \"/cgi-bin/Syntaxipot.py\"[PT, H = cgi - "
            "script]\n"
        ]
        f.writelines(httpdconf_lines)


def install_pylib():
    if 'pylibinjection' not in modules:
        try:
            pip.main(['install', 'pylibinjection'])
        except Exception as e:
            print("Error in downloading and installing pylibinjection")
            print(e, file=stderr)


def run():
    print('Unpacking Files...')
    fails = unpack_project()
    print("Unpacked Successfuly {}/{} files".format(len(project_files),
                                                    len(
                                                        project_files) - fails))
    print("Modifying httpd.conf...")
    modify_httpd_conf()
    print("Installing pylibinjection...")
    install_pylib()
    print("Installation Finished.")


if __name__ == "__main__":
    run()
