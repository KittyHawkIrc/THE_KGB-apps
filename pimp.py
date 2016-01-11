pimpdb = {}

def declare():
    return {"pimp": "privmsg"}

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):
    if channel.startswith('#'):
        u = user.split('!')[0]

        var = msg.split()

        try:
            target = var[1]
        except:
            target = u

        target = target.lower()

        try:
            com = var[2]
        except:
            com = 'get'

        if u == target and com != 'get':
            self.msg(channel, "%s: Y'all can't pimp yourself, ma nigga" % (u))
            return


        if com == '+1':
            try:
                pimpdb[channel][target] += 1
            except:
                try:
                    pimpdb[channel][target] = 1
                except:
                    pimpdb[channel] = {}
                    pimpdb[channel][target] = 1

        elif com == '-1':
            try:
                pimpdb[channel][target] = pimpdb[channel][target] - 1
            except:
                try:
                    pimpdb[channel][target] = 1
                except:
                    pimpdb[channel] = {}
                    pimpdb[channel][target] = 1

        elif com == 'get':
            try:
                pimp = pimpdb[channel][target]
                if pimp > 0:
                    self.msg(channel, "that nigga got %s pimp points up in this bitch" % (pimp))
                else:
                    self.msg(channel, "that nigga got %s bitch points" % (pimp))
            except:
                self.msg(channel, "that nigga ain't got no pimp points")

        else:
            self.msg(channel, "%s: Nigga, you really think you that og, just giving out more points like that?" % (u))
