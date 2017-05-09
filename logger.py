from datetime import datetime

from Request import ClassifiedRequest


def log(request: ClassifiedRequest):
    date = str(datetime.now()).split(".")[0]
    filename = "attacks.log"
    with open(filename, "a") as f:
        f.write(f"{date} {request.ip}:{request.port} {request.attack_type}" +
                f"{request.return_path}\n")
