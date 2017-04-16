import os.path


def generate_page(query):
	file_name = "fake_page_"+str(hash(query))
	if not os.path.isfile(file_name):
		with open(file_name, "w") as f:
			page = open("fake_page.txt").read()
			f.write(page.format(query=query))

