import discord
import random
import os
import json
from urban_dictionary import udscraper as ud
from quote import quotemanager as qm
from space import astronauts as astro

class MyClient(discord.Client):

	guild_prefixes = {} # holds guild ids and the correlating prefixes
	async def bonk_meri(self, message):
		current_bonks = "ERROR"
		with open("bonks.txt", "r") as bonks:
			current_bonks = int(bonks.read())
		with open("bonks.txt", "w") as bonks:
			current_bonks += 1
			bonks.write(str(current_bonks))
		msg = discord.Embed(title="BONKED", colour=discord.Colour.from_rgb(107, 250, 143), description=f"MERI HAS BEEN BONKED **{current_bonks}** TIMES.")
		await message.channel.send(embed=msg)
	# function that adds the prefix to the dictionary and to the file.
	def add_prefix(self, guild, prefix):
		self.guild_prefixes[str(guild.id)] = prefix
		# dumps the new dictionary to the file as json
		with open("prefixes.json", "w") as json_file:
			json.dump(self.guild_prefixes, json_file)

	# functiod accessed directly through bot command that displays avatar of mentioned user
	async def avatar(self, message):
		mention = message.author
		if len(message.mentions) > 0:
			mention = message.mentions[0]
		msg = discord.Embed(colour=discord.Colour.from_rgb(107, 250, 143))
		print(str(mention.avatar_url).replace(".webp", ".png"))
		msg.set_image(url=mention.avatar)
		await message.channel.send(embed=msg)

	# function accessed directly through bot command that sets that guild's prefix
	async def set_prefix(self, message):
		#begins to create embed to send
		msg = discord.Embed(title="PREFIX", colour=discord.Colour.from_rgb(107, 250, 143))
		#removes command from message
		args = message.content.split(" ")[1:]
		# ensures there is a prefix to be set
		if len(args) < 1:
			return
		# sets the prefix to the first word of the command
		prefix = args[0]
		self.add_prefix(message.guild, prefix)
		msg.description = "Successfully changed prefix to: `{0}`".format(prefix)
		await message.channel.send(embed=msg)
	
	# function accessed directly through bot command that returns all of the people in space
	async def space(self, message):
		# gets the list of astronauts currently in space
		people = astro.get_people("http://api.open-notify.org/astros.json")
		msg = discord.Embed(title="ASTRONAUTS", colour=discord.Colour.from_rgb(107,250,143), description="All of the people currently in space.")
		for person in people:
			msg.add_field(name=person.name, value="**{0.name}** - {0.craft}".format(person), inline=False)
		msg.set_footer(text=("People: {}".format(len(people))))
		await message.channel.send(embed=msg)

	# function accessed directly through bot command summons bot to user's voice channel
	async def join_channel(self, message):
		# gets the user as a member so member functions/variables can be accessed
		member = message.guild.get_member(message.author.id)
		msg = discord.Embed(title="ERROR", colour=discord.Colour.from_rgb(255, 32, 28), description="You aren't in a voice channel.")
		# ensures that memeber is in a voice channel by checking they have voice state
		if member.voice is None:
			await message.channel.send(embed=msg)
			return
		msg = discord.Embed(title="SUCCESS", colour=discord.Colour.from_rgb(107,250,143), description="Successfully joined")
		# joins voice channel
		try:
			voice = await member.voice.channel.connect()
		# if the bot is already in a voice channel, it will throw a ClientException in which case the bot moves voice channel
		except discord.ClientException:
			voice.move_to(member.voice.channel)
		finally:
			await message.channel.send(embed=msg)

	# function accessed directly through bot command causes bot to leave voice channe
	async def leave_channel(self, message):
		msg = discord.Embed(title="SUCCESSFUL", colour=discord.Colour.from_rgb(107,250,143), description="Successfully disconnected")
		# needs to find the voice channel of guild of message, loops through its own VoiceClients (connections)
		for v in self.voice_clients:
			# VoiceClient is found
			if v.guild == message.guild:
				# disconnects and ends function
				await v.disconnect()
				await message.channel.send(embed=msg)
				return
		# if loop is completed, the bot is not in a voice channel for the respective guild
		msg = discord.Embed(title="ERROR", colour=discord.Colour.from_rgb(255,32,28), description="I'm not in a voice channel.")
		await message.channel.send(embed=msg)

	# function accessed directly through bot command grabs definition from urban dictionary using custom-built urban dicitonary module
	async def urbandictionary_definition(self, message):
		# removes the command from the message to get the args as a string
		args = message.content.split(" ")[1:]
		to_define = " ".join(word for word in args)
		# grabs the definition using the module, it is a UDefinition object
		top_def = ud.UDefinition.define(to_define)
		# begins to create the definition embed
		msg = discord.Embed(title=top_def.word, colour=discord.Colour.from_rgb(107,250,143), description="Top Urban Dictionary result for: `{}`".format(top_def.word))

		# prepares to add the fields to the embed
		definition = top_def.definition
		example = top_def.example
		# embed has max length of 1024 characters
		if len(definition) > 1024:
			# cuts defintion and adds punctuation to show there is more
			definition = str(definition[:1019]) + "[...]"
		if len(example) > 1024:
			example = str(example[:1019]) + "[...]"
		# adds the fields and footer
		msg.add_field(name="Definition",value=definition,inline=False).add_field(name="Example Usage", value=example, inline=False).add_field(name="Rating", value="{0.upvotes} :thumbsup: {0.downvotes} :thumbsdown:".format(top_def), inline=False)
		msg.set_footer(text="Author: {0.author} - Written at: {0.timestamp}".format(top_def))
		await message.channel.send(embed=msg)

	async def role_count(self, message):
		if not message.mentions:
			mentioned_user = message.author
		else:
			mentioned_user = message.mentions[0]
		await message.channel.send(embed=discord.Embed(title=f"{mentioned_user.name} has {len(mentioned_user.roles)} roles.", colour=discord.Colour.from_rgb(107, 250, 143), description="")) 
	# function accessed directly through bot command that makes bot repeat the user
	async def say(self, message):
		# removes command
		args = message.content.split(" ")[1:]
		# ensures there is something to mimic
		if len(args) > 0:
			# deletes users message. if it can't, there is no issue (unimportant to command)
			try:
				await message.delete()
			except:
				pass
			await message.channel.send(" ".join(word for word in args))
			return
		await message.channel.send(embed=discord.Embed(title="ERROR", colour=discord.Colour.from_rgb(255, 32, 28), description="There's nothing to say!"))

	# function accessed directly through bot command that returns the latency in milliseconds
	async def ping(self, message):
		msg = discord.Embed(title=":ping_pong: **PONG**", colour=discord.Colour.from_rgb(107, 250, 143))
		latency = int(self.latency * 1000)
		msg.add_field(name="Latency", value="{0}ms".format(latency))
		await message.channel.send(embed=msg)

	# function accessed directly through bot command that generates an invite for the user to use
	async def invite(self, message):
		msg = discord.Embed(title=":envelope: Invite me to your server! :envelope:",
							colour=discord.Colour.from_rgb(107, 250, 143), url = "https://discordapp.com/api/oauth2/authorize?client_id={0}&scope=bot&permissions={1}".format(
			self.user.id, 8))
		await message.channel.send(embed=msg)

	# function accessed directly through bot command that uses api purge method to delete x amount of messages
	async def bulkdelete(self, message):
		try:
			amount = int(message.content.split(" ")[1])
			await message.channel.purge(limit=amount)
		# bot does not have permission to delete messages
		except discord.Forbidden:
			await message.channel.send(embed=discord.Embed(title="ERROR", colour=discord.Colour.from_rgb(255, 32, 28), description="I'm missing the permissions to delete messages."))

	# function accessed directly through bot command that sends a list of commands and their brief description as a message
	async def commandhelp(self, message):
		# will format prefix and command as field names 
		prefix = self.guild_prefixes[str(message.guild.id)]
		msg = discord.Embed(title=":question: HELP", colour=discord.Colour.from_rgb(107, 250, 143))
		# loops through dictionary, formatting correct data as a field
		for command in self.commands:
			msg.add_field(name="{0}{1}".format(prefix,command), value="`{0}` - {1}".format(command, self.commands[command][1]), inline=False)
		await message.channel.send(embed=msg)

	# beginning of quote functions
	QUOTEFILE = "quotes.txt"

	# function accessed directly through bot command that adds a quote to the quote file under respective guild using custom-built quote module
	async def make_quote(self, message):
		# removes command from message
		args = message.content.split(" ")[1:]
		msg = discord.Embed(title="ERROR", colour=discord.Colour.from_rgb(255, 32, 28), description="There's nothing to quote.")
		# ensures there is something to quote
		if len(args) > 0:
			msg = discord.Embed(title="SUCCESSFUL", colour=discord.Colour.from_rgb(107, 250, 143), description="Successfully quoted.")
		quote = " ".join(word for word in args)
		# adds quote to list with the, quote and author id for the object and guild for the placement
		qm.add_quote(self.QUOTEFILE, quote, message.author.id, message.guild)
		await message.channel.send(embed=msg)

	# function accessed directly through bot command that removes a quote from the quote file under the guilds quote list using quote
	async def delete_quote(self, message):
		msg = discord.Embed(title="ERROR", colour=discord.Colour.from_rgb(255, 32, 28), description="Quote not found in the file.")
		args = message.content.split(" ")[1:]
		quote = " ".join(word for word in args)
		# uses quote module remove quote function to remove a quote from respective guild, has boolean return to check if quote exists
		inFile = qm.remove_quote(self.QUOTEFILE, quote, message.guild)
		if inFile:
			# changes embed depending of whether quote exists
			msg = discord.Embed(title="SUCCESSFUL", colour=discord.Colour.from_rgb(107, 250, 143))
			msg.description = "Successfully removed quote"
		await message.channel.send(embed=msg)

	# function accessed directly through bot command that gets a random quote from quote file under guild's quote list
	async def quote(self, message):
		guild = message.guild
		# uses quote module function to get list of specific guild's quotes
		quotes = qm.get_quotes(self.QUOTEFILE, guild)
		msg = discord.Embed(title="ERROR", colour=discord.Colour.from_rgb(255, 32, 28), description="There are no quotes in your server.")
		# ensures there are actual quotes in the server
		if len(quotes) > 0:
			# if there are quotes, the quote is picked using randint
			quote = quotes[random.randint(0, len(quotes) - 1)]
			msg = "\"{0}\" -{1}".format(quote.quote, self.get_user(quote.author))
			# it is sent as a plain text message and the function is ended
			await message.channel.send(msg)
			return
		# the error embed is sent
		await message.channel.send(embed=msg)
	
	# end of quote functions

	# the command dictionary holds a command tuple formatted as so: (command_function, "help context for command") and its respective bot command that will be looked for
	commands = {"help": (commandhelp, "a list of the commands and their function."), "say": (say, "make the bot say what you want it to say."), "ping": (ping, "returns the latency of the bot."), "invite": (invite, "get an invite link and invite me to your own server."), "makequote": (make_quote, "add a quote to your server's quote list."),"removequote":(delete_quote, "removes a quote from your server's quote list."), "quote": (quote, "get a quote from your server's quote list."),
				"purge": (bulkdelete,"delete up to 100 messages."), "setprefix": (set_prefix,"change the prefix for your server."), "roles": (role_count, "how many roles does a user have?"), "define": (urbandictionary_definition, "returns the top result of an urban dictionary definition."),"summon":(join_channel, "connects me to the voice channel you are in."), "banish":(leave_channel, "disconnects me from any voice channel I am in."), "space":(space, "shows you all of the people in space right now."), "avatar":(avatar, "displays the avatar of the mentioned person!"),
				"bonk": (bonk_meri, "bonks meri.")}
	# event for when bot connects to discord
	async def on_connect(self):
		# checks that prefixes.json isn't empty, otherwise don't continue
		if os.stat('prefixes.json').st_size == 0:
			return
		# loads json from file onto the guild_prefixes dictionary
		with open("prefixes.json", "r") as json_file:
			self.guild_prefixes = json.load(json_file)

	# event for when the bot is ready to work, sends basic log message to signify this
	async def on_ready(self):
		print("LOGGED ON AS: {0}".format(self.user))

	# event for when bot joins a guild
	async def on_guild_join(self, guild):
		# adds that guild to the quotefile and its prefix
		qm.add_guild(self.QUOTEFILE, guild)
		self.add_prefix(guild, "$")

	# event for message send in any of it's guilds
	async def on_message(self, message):
		# code to handle message
		content = message.content
		# makes sure the message isn't from the bot account
		if message.author == self.user:  
			return
		# makes sure the message starts with the corresponding guild prefix
		if not content.startswith(self.guild_prefixes[str(message.guild.id)]):  
			return
		command = str(content.split(" ")[0][len(self.guild_prefixes[str(message.guild.id)]):])
		# makes sure the message (with the prefix removed) is in the command dictionary
		if command not in self.commands:  
			return
		# runs the corresponding function
		await self.commands[command][0](self, message)

client = MyClient()
# grabs token from config.json and runs bot with token
with open("config.json", "r") as config:
	token = json.load(config)["token"]	
client.run(token)
