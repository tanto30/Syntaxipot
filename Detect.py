from pylibinjection import *


def detect(msg):
    return detect_sqli(bytes(msg, encoding="utf-8"))["sqli"]
