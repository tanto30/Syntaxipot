from datetime import datetime

from Request import ClassifiedRequest


def log(classified_request: ClassifiedRequest):
    date = str(datetime.now()).split(".")[0]
    filename = "attacks.log"
    with open(filename, "a") as f:
        f.write(f"{date} {classified_request.ip}:{classified_request.port} "
                f"{classified_request.attack_type} " +
                f"{classified_request.full_url}\n")
