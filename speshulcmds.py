#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

def declare():
    return {"ultimatetruth": "privmsg", 'msc': 'privmsg'}

def callback(self):
    if self.command.lower() == 'ultimatetruth':
        return self.msg(self.channel, "RielDtok is a tranny")
    if self.command.lower() == 'msc':
        return self.msg(self.channel, '^billdred\n<MsC> I like it black like my dicks? <billdred> we agree on that too!')

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
    print callback(api)
    if callback(api) != "[%s] RielDtok is a tranny" % (c):
        exit(1)

    setattr(api, 'command', 'MsC')
    print callback(api)
    if '^billdred\n<MsC>' not in callback(api):
        exit(2)
