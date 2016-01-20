def declare():
    return {"hello": "privmsg"}

def callback(self):

    if self.channel.startswith('#'):
        self.msg(self.channel, 'test')
        return self.msg(self.channel, "And a hello to you too, " + ("operator" if self.isop else "user") + " %s!" % (self.user))

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

    if callback(api) != '[%s] And a hello to you too, operator %s!' % (api.channel, api.user):
        exit(1)
