from re import sub
from sys import stderr, modules

import pip

full_apache_path = input("Enter full path to the apache server: (e.g. "
                         "C:\\apache)\n")

files = ["Classifier.py", "fake_page.txt", "logger.py", "PageGenerator.py",
         "Request.py", "RequestGenerator.py", "ServePage.py", "Syntaxipot.py"]

for filename in files:
    with open(filename) as f_read, open(full_apache_path + "\\cgi-bin\\" +
                                        filename) as f_write:
        f_write.write(f_read.read())

with open(full_apache_path + "\\conf\\httpd.conf", "r") as f:
    httpdconf_lines = f.readlines()
    for line in httpdconf_lines:
        if "AddHandler cgi-script" in line:
            line = line[:-1] + " .py\n"
        elif "AllowOverride None" in line:
            sub(r"None", "All", line)

with open(full_apache_path + "\\conf\\httpd.conf", "w") as f:
    httpdconf_lines += [
        "RewriteEngine on\n",
        "RewriteCond %{REMOTE_ADDR} !127.0.0.1\n",
        "RewriteRule \"(.*)\" \"/cgi-bin/Syntaxipot.py\"[PT, H = cgi - script]"
    ]
    f.writelines(httpdconf_lines)

if 'pylibinjection' not in modules:
    try:
        pip.main(['install', 'pylibinjection'])
    except Exception as e:
        print("Error in downloading and installing pylibinjection")
        print(e, file=stderr)

print("Done!!!")
