def declare():
        return {"ultimatetruth": "privmsg"}
        
def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):
        if channel.startswith('#'):
                return self.msg(channel, "RielDtok is a tranny")

class api:
        def msg(self, channel, text):
	        return "[%s] %s" % (channel, text)

if __name__ == "__main__":
        api = api()
        u = "joe!username@hostmask"
        c = '#test'
        
        if callback(api, '', True, command="ultimatetruth", msg="^ultimatetruth", channel=c, user=u) != "RielDtok is a tranny":
                exit(1)
