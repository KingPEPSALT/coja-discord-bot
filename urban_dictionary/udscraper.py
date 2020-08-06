import urllib.request
import json

class UDefinition:
	def __init__(self, word, definition, example, url, upvotes, downvotes, author, timestamp):
		self.word = word
		self.definition = definition
		self.example = example
		self.url = url
		self.upvotes = upvotes
		self.downvotes = downvotes
		self.author = author
		self.timestamp = timestamp
	@staticmethod
	def define(word):
		data = scrape("http://api.urbandictionary.com/v0/define?term={}".format(word.replace(" ", "%20")))
		return UDefinition(data["word"], data["definition"], data["example"], data["permalink"], data["thumbs_up"], data["thumbs_down"], data["author"], str(data["written_on"][:10]))

def scrape(url):
	response = urllib.request.urlopen(url)
	return json.loads(response.read())['list'][0]
