pimpdb = {}

def declare():
    return {"pimp": "privmsg"}

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):
    u = user.split('!')[0]
    if channel.startswith('#'):

        chan = channel.lower()

        var = msg.lower().split()

        try:
            target = var[1]
        except:
            target = u

        try:
            com = var[2]
        except:
            com = 'get'

        if chan not in pimpdb:
            pimpdb[chan] = {}

        if u == target and com != 'get':
            self.msg(chan, "%s: Y'all can't pimp yourself, ma nigga" % (u))
            return

        if com == '+1':

            if u not in pimpdb[chan]:
                pimpdb[chan][u] = 1

            elif pimpdb[chan][u] > 0:
                pimpdb[chan][u] = pimpdb[chan][u] - 1
            else:
                self.msg(channel, "%s: You ain't got no pimp points" % (u))
                return

            try: #modifies users points
                pimpdb[chan][target] += 1
            except:
                pimpdb[chan][target] = 2

        elif com == '-1':

            if u not in pimpdb[chan]:
                pimpdb[chan][u] = 1

            elif pimpdb[chan][u] > 0:
                pimpdb[chan][u] = pimpdb[chan][u] - 1
            else:
                self.msg(channel, "%s: You ain't got no pimp points" % (u))
                return

            try: #also modifies users pounts
                pimpdb[chan][target] = pimpdb[chan][target] - 1
            except:
                pimpdb[chan][chan][target] = 0

        elif com == 'get':
            try:
                pimp = pimpdb[chan][target]
                if pimp > 0:
                    self.msg(channel, "that nigga got %s pimp points up in this bitch" % (pimp))
                else:
                    self.msg(channel, "that nigga got %s bitch points" % (pimp))
            except:
                self.msg(channel, "that nigga ain't got no pimp points")

        else:
            self.msg(channel, "%s: Nigga, you really think you that og, just giving out more points like that?" % (u))

    elif isop:
        var = msg.lower().split()
        com = var[1]
        chan = var[2]
        target = var[3]

        try:
            val = var[4]
        except:
            val = 5

        if com == 'set':
            try:
                pimpdb[chan][target] = val
                self.msg(u, "%s's score in %s is now set to %s" % (target, chan, val))
            except:
                self.msg(u, "%s doesn't exist in %s" % (target, chan))
        elif com == 'add':
            try:
                pimpdb[chan][target] += val
                self.msg(u, "%s's score in %s is now set to %s" % (target, chan, val))
            except:
                self.msg("Doesn't %s exist in %s" % (target, chan))
        elif com == 'remove':
            if target in pimpdb[chan]:
                pimpdb[chan].pop(target)
                self.msg(u, "%s is now removed from that channel's list" % (target))
            else:
                self.msg(u, "%s is not in that channel's list")
        elif com == 'new':
            if chan not in pimpdb:
                pimpdb['chan'] = {}
            if target not in pimpdb[chan]:
                pimpdb[chan][target] = val
                self.msg(u, "%s is now added to the channel with %s points" % (target, val))
            else:
                self.msg(u, "%s is already in the channel with %s points, please remove them before adding them again" % (target, val))
        else:
            self.msg(u, "unavailable")
