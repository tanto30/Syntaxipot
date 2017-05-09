#! python
import sys

import Classifier
import RequestGenerator
from PageGenerator import generate_page_filename
from ServePage import serve_page
from logger import log


class HoneypotRequestHandler:
    def __init__(self):
        self.request = RequestGenerator.generate_request()

    def __handle_malicious(self):
        log(self.request)
        page_name = "/" + generate_page_filename(self.request.query_params,
                                                 self.request.attack_type)
        return page_name

    def __handle_legitimate(self):
        return self.request.path

    def handle_request(self):
        self.request = Classifier.classify(self.request)
        if self.request.is_malicious():
            page_name = self.__handle_malicious()
        else:
            page_name = self.__handle_legitimate()
        self.request.set_return_path(page_name)
        return serve_page(self.request)


def write_output(bytes_to_write):
    sys.stdout.buffer.write(bytes_to_write)
    sys.stdout.buffer.flush()


def run():
    handler = HoneypotRequestHandler()
    out = handler.handle_request()
    write_output(out)


run()
