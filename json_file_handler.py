
from colored_printing import *
import json



class JsonFileHandler():
	def __init__(self, filename):
		self.filename = filename
		try:
			file = open(str(self.filename),"r")
			file.close()
		except IOError:
			file = open(str(self.filename), "w")
			file_content = []
			json.dump(file_content, file, indent=4, sort_keys=True)
			file.close()

	def read(self):
		file = open(str(self.filename),"r")
		try:
			file_content = json.load(file)
			file.close()
		except IOError:
			file = open(str(self.filename), "w")
			file_content = []
			json.dump(file_content, file, indent=4, sort_keys=True)
			file.close()
		except ValueError:
			file_content = []
			file.close()
		return file_content

	def write(self, element):

		file_content = self.read()
		try:
			if element not in file_content:
				file_content.append(element)

			with open(str(self.filename), 'w') as file:
				json.dump(file_content, file, indent=4, sort_keys=True)	

			file.close()

			return True

		except KeyError:
			printError("MMAelementFileHandler.write(element) KeyError with element = {}".format(element))
			return False
		try:
			with open(str(self.filename), 'w') as file:
				json.dump(file_content, file, indent=4, sort_keys=True)
		except TypeError:
			printError("MMAelementFileHandler TypeError with file_content == {}".format(file_content))
			return False
		file.close()

	def has_element(self, element):
		file_content = self.read()
		if element in file_content:
			return True
		else:
			return False




def file_get_username(filename):
	try:
		file = open(str(filename),"r")
		file_content = json.load(file)
		username = file_content["username"]
		file.close()
		return password
	except:
		print("file_get_password IOError {} probably not found".format(filename))
		username = file_generate(filename)["username"]
		return username

def file_get_password(filename):
	try:
		file = open(str(filename),"r")			
		file_content = json.load(file)
		print(file_content)
		password = file_content["password"]
		file.close()
		return password
	except:
		print("file_get_password IOError {} probably not found".format(filename))
		password = file_generate(filename)["password"]
		return password

def file_generate(filename):
	print("Couldn't find account_info.txt file, creating one now...")
	file_content = {
		"username": "ED974228",
		"password": "#B0tSw4g9"
	}
	# username = input("Type username and press enter...")	
	# password = input("Type password and press enter...")
	with open(str(filename), 'w') as file:
		json.dump(file_content, file, indent=4, sort_keys=True)	
	file.close()
	print("password successfully generated continuing program with username and password")
	print("file content = ", file_content)
	return file_content
