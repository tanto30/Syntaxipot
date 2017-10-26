import pylibinjection
import re
import urllib.parse
from Request import ClassifiedRequest


def detect_sqli(request):
    return pylibinjection.detect_sqli(bytes(request, encoding="utf-8"))["sqli"]


def detect_xss(request):
    m = re.search(r"((%3C)|<)((%2F)|/)*[a-z0-9%]+((%3E)|>)", request)
    if m is not None:
        return True
    m = re.search(
        r"((%3C)|<)((%69)|i|(%49))((%6D)|m|(%4D))((%67)|g|(%47))[^\n]+((%3E)|>)",
        request)
    if m is not None:
        return True
    return False


def classify(request):
    """
    :param request: object, Request.classified_request instance
    :return: object, ClassifiedRequest instance
    """

    # checks is a dictionary of
    # keys: function of vulnerability checks, should return boolean
    # values: attack types of the appropriate checks.
    checks = {detect_sqli: "sqli", detect_xss: "xss"}
    # malicious: boolean
    malicious = False
    # attack type: empty string if not malicious is False
    attack_type = ""
    raw_decoded = urllib.parse.unquote_plus(request.raw_request)
    for check in checks:
        malicious = check(raw_decoded)
        if malicious:
            attack_type = checks[check]
            break
    return ClassifiedRequest(request, malicious, attack_type)
