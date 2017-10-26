#! python
import sys

import Classifier
import RequestGenerator
from PageGenerator import generate_page_filename
from ServePage import serve_page
from logger import log


class HoneypotRequestHandler:
    def __init__(self):
        self.classified_request = RequestGenerator.generate_request()

    def __handle_malicious(self):
        log(self.classified_request)
        page_name = "/" + generate_page_filename(self.classified_request)
        return page_name

    def __handle_legitimate(self):
        return self.classified_request.full_url

    def handle_request(self):
        self.classified_request = Classifier.classify(self.classified_request)
        if self.classified_request.is_malicious():
            self.__handle_malicious()
        else:
            self.__handle_legitimate()
        return serve_page(self.classified_request)


def write_output(bytes_to_write):
    sys.stdout.buffer.write(bytes_to_write)
    sys.stdout.buffer.flush()


def run():
    handler = HoneypotRequestHandler()
    out = handler.handle_request()
    write_output(out)


run()
