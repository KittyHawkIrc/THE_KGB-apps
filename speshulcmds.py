#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

speshulcmds = {'ultimatetruth': 'RielDtok is a tranny', 'msc': '^billdred\n<MsC> I like it black like my dicks? <billdred> we agree on that too!'}

def declare():
    dec = {}
    cmdlist = speshulcmds.keys()
    for cmd in cmdlist:
        dec[cmd] = 'privmsg'
    return dec

def callback(self):
    try:
        user = self.message.split()[1]
    except:
        user = False

    cmdlist = speshulcmds.keys()

    for cmd in cmdlist:
        if self.command == cmd:
            if user:
                return '%s: %s' % (user, speshulcmds[cmd].split('\n')[0])
            return speshulcmds[cmd]

class api:
	def msg(self, channel, text):
		return "[%s] %s" % (channel, text)

if __name__ == "__main__":
    api = api()
    u = "joe!username@hostmask"
    c = '#test'

    setattr(api, 'isop', True)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'user', 'joe!username@hostmask')
    setattr(api, 'channel', '#test')

    setattr(api, 'command', 'ultimatetruth')
    setattr(api, 'message', '^ultimatetruth')

    print callback(api)
    if 'RielDtok is a tranny' not in callback(api):
        exit(1)

    setattr(api, 'message', '^ultimatetruth cats')
    print callback(api)
    if 'cats: RielDtok' not in callback(api):
        exit(2)

    setattr(api, 'command', 'msc')
    setattr(api, 'message', '^msc')
    print callback(api)
    if '^billdred\n<MsC>' not in callback(api):
        exit(3)

    setattr(api, 'message', '^msc cats')
    print callback(api)
    if 'cats: ^billdred' not in callback(api):
        exit(4)
