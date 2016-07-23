#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

def declare():
    return {"ultimatetruth": "privmsg", 'msc': 'privmsg'}

def callback(self):
    message = self.message.split(self.command, 1)[1].strip()

    if self.command.lower() == 'ultimatetruth':
        return self.msg(self.channel, emulate(message, 'RielDtok is a tranny'))
    if self.command.lower() == 'msc':
        return self.msg(self.channel, emulate(message, '^billdred\n<MsC> I like it black like my dicks? <billdred> we agree on that too!'))

def emulate(message, output):
    try:
        try:
            return '%s: %s' % (message.split()[0], output.split('\n')[0])
        except:
            return '%s: %s' % (message.split()[0], output)
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
    if 'cats: ^billdred' != callback(api):
        exit(4)
