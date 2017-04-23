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

    def __handle_malicious(self, classified_request):
        log(classified_request)
        page_name = generate_page_filename(self.request.query_params,
                                           classified_request.attack_type)
        return page_name

    def __handle_legitimate(self):
        return self.request.path

    def handle_request(self):
        classified_request = Classifier.classify(self.request)
        if classified_request.is_malicious():
            page_name = self.__handle_malicious(classified_request)
        else:
            page_name = self.__handle_legitimate()
        classified_request.set_return_path(page_name)
        return serve_page(classified_request)


def write_output(bytes_to_write):
    sys.stdout.buffer.write(bytes_to_write)
    sys.stdout.buffer.flush()


def run():
    handler = HoneypotRequestHandler()
    out = handler.handle_request()
    write_output(out)


run()
