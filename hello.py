def declare():
    return {"hello": "privmsg"}

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):

    if channel.startswith('#'):
        self.msg(channel, "And a hello to you too, " + ("operator" if isop else "user") + " %s!" % (user))
