# -*- coding: utf-8 -*-

__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 2.0


def declare():
    return {"autovoice": "userjoin", "verify": "privmsg"}

def callback(self):
    if self.type == 'userjoin':
        if self.channel == '#fatpeoplesuck' and self.profile.isverified:
            self.mode(self.channel, True, 'v', user=self.profile.nickname)
    else:
        privlist = self.message.split()

        if len(privlist) == 1: #^verify
            return self.msg(self.channel, '%s: You %s verified.' % (
            self.profile.nickname, ("are" if self.profile.isverified else "are not")))

        elif len(privlist) == 2:
            selector = self.profileManager.getuser_bynick(privlist[1])

            if selector:
                return self.msg(self.channel, '%s: %s %s verified.' % (
                self.profile.nickname, selector.nickname, ("is" if selector.isverified else "is not")))

            else:
                return self.msg(self.channel, "%s: That user couldn't be found." % (
                self.profile.nickname))

        elif len(privlist) == 3:

            if self.isop:
                selector = self.profileManager.getuser_bynick(privlist[1])

                if selector:
                    if 'y' in privlist[2].lower():
                        self.profileManager.update(selector.username, isverified=True)
                    elif 'n' in privlist[2].lower():
                        self.profileManager.update(selector.username, isverified=False)

                    return self.msg(self.channel, "%s: %s %s verified." % (
                        self.profile.nickname, selector.nickname, ("is now" if self.profileManager.getuser_bynick(privlist[1]).isverified else "is no longer")))

                else:
                    return self.msg(self.channel, "%s: That user couldn't be found." % (
                        self.profile.nickname))

            else:
                return self.msg(self.channel, "%s: You don't have permissions to verify others" % (
                    self.profile.nickname))
