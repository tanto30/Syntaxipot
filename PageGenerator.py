import os.path


def generate_page(query):
	file_name = "fake_page_"+str(hash(query))
	if not os.path.isfile(file_name):
		with open(file_name, "w") as f:
			fpage = open("fake_page.txt")
			page = fpage.read()
			f.write(page.format(query=query))
			fpage.close()
	return file_name
