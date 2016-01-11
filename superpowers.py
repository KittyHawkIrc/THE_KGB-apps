spdb =	{
		"creative":"turning everything into corn",
		"marlow":"creating buncy balls and quicksand",
		"terriblefuhrer":"controlling the trees",
		"ruston":"controlling squirrels",
		"redubious":"turning inorganic matter into glass",
		"homersimpson":"shooting Christmas lights out of his wrists like spiderman",
		"rieldtok":"instantly giving anyone an orgasm",
		"gyst":"making any liquid into bubbles",
		"uvulectomy":"having superpowered sneezes",
		"marvin":"having the power of conversation",
		"[deleted]":"turning into gas powered vehicles",
		"justnotfair":"turning plants into weapons, and is also not black",
		"moudi":"turning into rocks",
		"dr_durex":"controlling paper",
		"nwo-chan":"boiling liquid instantly",
		"billdred":"just flying. That's it.",
	}

def declare():
	return {"superpower": "privmsg"}

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):
	if channel.startswith('#'):
		var = msg.split()

		if var[1] == "help":
			self.msg(channel,"^superpower username")
			return

		try:
			self.msg(channel,"%s's superpower is %s" % (var[1], spdb[var[1].lower]))
			return
		except:
			self.msg(channel,"%s's not on the list" % (var[1]))
