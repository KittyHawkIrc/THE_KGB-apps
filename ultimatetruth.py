#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

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

        setattr(api, 'isop', True)
        setattr(api, 'type', 'privmsg')
        setattr(api, 'command', 'ultimatetruth')
        setattr(api, 'user', 'joe!username@hostmask')
        setattr(api, 'channel', '#test')

        if callback(api) != "[%s] RielDtok is a tranny" % (c):
                exit(1)
