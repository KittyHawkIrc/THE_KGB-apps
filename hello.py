def declare():
    return {"hello": "privmsg"}

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):

    if channel.startswith('#'):
        return self.msg(channel, "And a hello to you too, " + ("operator" if isop else "user") + " %s!" % (user))

class api:
	def msg(self, channel, text):
		return "[%s] %s" % (channel, text)

if __name__ == "__main__":
    api = api()
    u = "joe!username@hostmask"
    c = '#test'

    if callback(api, '', True, channel=c, user=u) != '[%s] And a hello to you too, operator %s' % (c, u) or callback(api, '', False, channel=c, user=u) != '[%c] And a hello to you too, user %s' % (c, u):
        exit(1)
