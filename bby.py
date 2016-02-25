def declare():
    return {"bby": "privmsg"}

def callback(self):

    if self.channel.startswith('#'):
        try:
            u = self.message.split()[1]
        except:
            u = self.user.split('!',1)[0]
        if u != 'bym':
            return self.msg(self.channel, "Wow %s, you look absolutely gorgeous today" % (u))
        else:
            return self.msg(self.channel, "Wow %s, you look like absolute shit today. Maybe you should go kill yourself you emo faggot." % (u))
class api:

    def msg(self, channel, text):
        return "[%s] %s" % (channel, text)

if __name__ == "__main__":
    api = api()
    setattr(api, 'isop', True)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'command', 'hello')
    setattr(api, 'message', '^hello')
    setattr(api, 'user', 'joe!username@hostmask')
    setattr(api, 'channel', '#test')
    
    u = api.user.split('!',1)[0]

    if callback(api) != '[%s] Wow %s, you look absolutely gorgeous today' % (api.channel, u):
        exit(1)
