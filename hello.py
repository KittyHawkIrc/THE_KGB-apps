try:
    import encoder
except:
    print ''

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.1

def declare():
    return {"hello": "privmsg", "henlo": "privmsg"}

def callback(self):
    if self.channel.startswith('#'):
        if 'b64' in self.message:
            self.user = encoder.encode('b64:' + self.user)

        if self.command.lower() == 'hello':
            return self.msg(self.channel, "And a hello to you too, " + ("operator" if self.isop else "user") + "  %s (%s)!" % (self.profile.username, self.profile.userhost))
        return self.msg(self.channel, "and a henlo 2 u 2, " + ("operator" if self.isop else "user") + "  %s (%s)!" % (self.profile.username, self.profile.userhost))

class api:

    def msg(self, channel, text):
        return "[%s] %s" % (channel, text)

class profile:

    pass

if __name__ == "__main__":
    api = api()
    profile = profile()

    setattr(profile, 'username', "joe")
    setattr(profile, 'userhost', "joe!username@hostmask")
    setattr(profile, 'isop', True)

    setattr(api, 'isop', profile.isop)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'command', 'hello')
    setattr(api, 'message', '^hello')
    setattr(api, 'user', profile.userhost)
    setattr(api, 'channel', '#test')
    setattr(api, 'profile', profile)


    if callback(api) != '[%s] And a hello to you too, operator %s (%s)!' % (api.channel, api.profile.userhost, api.profile.username):
        exit(1)
