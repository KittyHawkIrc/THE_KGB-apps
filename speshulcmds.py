#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

speshulcmds = {'ultimatetruth': 'RielDtok is a tranny', 'MsC': '^billdred\n<MsC> I like it black like my dicks? <billdred> we agree on that too!'}

def declare():
    dec = {}
    cmdlist = speshulcmds.keys()
    for cmd in cmdlist:
        dec[cmd] = 'privmsg'
    return dec

def callback(self):
    message = self.message.lower().split(self.command, 1)[1].strip()

    cmdlist = speshulcmds.keys()

    for cmd in cmdlist:
        if self.command.lower() == cmd.lower():
            try:
                return '%s: %s' % (message.split()[0], speshulcmds[cmd].split('\n')[0])
            except:
                return speshulcmds[cmd]

def emulate(message, output):
    try:
        return '%s: %s' % (message.split()[0], output.split('\n')[0])
    except:
        return output

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
    if callback(api) != "[%s] RielDtok is a tranny" % (c):
        exit(1)

    setattr(api, 'message', '^ultimatetruth cats')
    print callback(api)
    if 'cats: RielDtok' not in callback(api):
        exit(2)

    setattr(api, 'command', 'MsC')
    setattr(api, 'message', '^MsC')
    print callback(api)
    if '^billdred\n<MsC>' not in callback(api):
        exit(3)

    setattr(api, 'message', '^MsC cats')
    print callback(api)
    if 'cats: ^billdred' not in callback(api):
        exit(4)
