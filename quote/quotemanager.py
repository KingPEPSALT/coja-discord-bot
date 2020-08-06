class Quote:
	def __init__(self, quote, author):
		self.quote = quote
		self.author = author
	@staticmethod
	def quote_from_line(line):
		args = line.split(":")
		return Quote(args[0], int(args[1]))

def file_as_list(filename):
	file_list = []
	with open(filename, "r") as rstream:
		for line in rstream:
			file_list.append(line)
	return file_list

def list_as_file(filename, file_list):
	string_to_write = ""
	with open(filename, "w") as wstream:
		for line in file_list:
			string_to_write += line
		wstream.write(string_to_write)

def add_guild(filename, guild):
	with open(filename, "a") as astream:
		astream.write("{}\n@".format(guild.id))

def add_quote(filename, quote, author_id, guild):
	file_list = file_as_list(filename)
	i = 0
	str_author_id = str(author_id)
	str_author_id += "\n"
	for line in file_list:
		i += 1
		if str(line[1:len(line) - 1]) == str(guild.id):
			file_list.insert(i, "{0}:{1}".format(quote.replace(":",""), str_author_id))
	list_as_file(filename, file_list)
def remove_quote(filename, quote, guild):
	file_list = file_as_list(filename)
	startFlag = False
	i = 0
	s_quote = "\"{}\"".format(quote)
	for line in file_list:
		if startFlag and line.split(":")[0] == s_quote:
			file_list.pop(i)
			list_as_file(filename, file_list)
			return True
		if str(line[1:len(line) - 1]) == str(guild.id):
			startFlag = True
		i += 1
	return False
def get_quotes(filename, guild):
	quotes = []
	with open(filename, "r") as rstream:
		startFlag = False
		for line in rstream:
			if startFlag and line.startswith("@"):
				return quotes
			if startFlag:
				quote = Quote.quote_from_line(line[:len(line)-1])
				quotes.append(quote)
			if str(line[1:len(line) - 1]) == str(guild.id):
				startFlag = True
	return quotes
