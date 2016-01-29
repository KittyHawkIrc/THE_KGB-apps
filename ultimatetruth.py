def declare():
        return {"ultimatetruth": "privmsg"}

def callback(self):
        if self.channel.startswith('#'):
                return self.msg(self.channel, "RielDtok is a tranny")

class api:
        def msg(self, channel, text):
	        return "[%s] %s" % (channel, text)

if __name__ == "__main__":
        api = api()
        u = "joe!username@hostmask"
        c = '#test'
	
	setattr(api,'channel',c)

        if callback(api) != "[%s] RielDtok is a tranny" % (c):
                exit(1)
