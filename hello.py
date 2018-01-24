try:
    import encoder
except:
    print ''

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

def declare():
    return {"hello": "privmsg", "henlo": "privmsg"}

def callback(self):
    if self.channel.startswith('#'):
        if 'b64' in self.message:
            self.user = encoder.encode('b64:' + self.user)

        if self.command.lower() == 'hello':
            return self.msg(self.channel, "And a hello to you too, " + ("operator" if self.isop else "user") + " %s (%s)!" % (self.profile.username, self.profile.userhost))
        return self.msg(self.channel, "and a henlo 2 u STINKY, " + ("operator" if self.isop else "user") + " %s (%s), go post a shit ugly" % (self.profile.username, self.profile.userhost))

class api:

    def msg(self, channel, text):
        return "[%s] %s" % (channel, text)

class profile:
    pass

if __name__ == "__main__":
    api = api()
    profile = profile()

    setattr(profile, 'username', 'joe')
    setattr(profile, 'nickname', 'joe')
    setattr(profile, 'ident', '~user')
    setattr(profile, 'hostname', '@kitty.hawk')
    setattr(profile, 'userhost', 'joe!~user@kitty.hawk')
    setattr(profile, 'lat', -8.783195)
    setattr(profile, 'lon', -124.508523)
    setattr(profile, 'unit', 'us')
    setattr(profile, 'gender', 1)
    setattr(profile, 'height', 1.8542)
    setattr(profile, 'weight', 90)
    setattr(profile, 'privacy', False)
    setattr(profile, 'isverified', True)
    setattr(profile, 'isop', True)
    setattr(profile, 'trusted', True)

    setattr(api, 'isop', profile.isop)
    setattr(api, 'type', 'privmsg')
    setattr(api, 'command', 'hello')
    setattr(api, 'message', '^hello')
    setattr(api, 'user', profile.userhost)
    setattr(api, 'channel', '#test')
    setattr(api, 'profile', profile)


    if callback(api) != "[#test] And a hello to you too, operator joe (joe!~user@kitty.hawk)!":
        exit(1)
