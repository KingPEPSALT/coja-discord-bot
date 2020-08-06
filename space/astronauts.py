import requests
class Person:
	def __init__(self, name, craft):
		self.name = name
		self.craft = craft


def obj_decode(info:dict) -> Person:
	return Person(info["name"], info["craft"])

def get_people(url:str) -> list:
	response = requests.get(url)
	dict_json = response.json()
	people = []
	for info in dict_json["people"]:
		people.append(obj_decode(info))
	return people
