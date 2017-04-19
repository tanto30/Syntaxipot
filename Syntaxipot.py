#! python
import Classifier
import RequestGenerator
from PageGenerator import generate_page_filename
from ServePage import serve_page


class HoneypotRequestHandler:
	def __init__(self):
		self.request = RequestGenerator.generate_request()

	def __log(self):
		pass

	def __handle_malicious(self, attack_type):
		self.__log()
		page_name = generate_page_filename(self.request.query_params, attack_type)
		return page_name

	def __handle_legitimate(self):
		return self.request.path

	def handle_request(self):
		classified_request = Classifier.classify(self.request)
		if classified_request.is_malicious():
			page_name = self.__handle_malicious(classified_request.attack_type)
		else:
			page_name = self.__handle_legitimate()
		classified_request.set_return_path(page_name)
		return serve_page(classified_request)


def run():
	handler = HoneypotRequestHandler()
	print(handler.handle_request())

run()
