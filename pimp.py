pimpdb = {}

def declare():
    return {"pimp": "privmsg"}

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):
    u = user.lower().split('!')[0]
    global pimpdb
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
            print(chan, "%s: Y'all can't pimp yourself, ma nigga" % (u))
            return

        if com == '+1':

            if u not in pimpdb[chan]:
                pimpdb[chan][u] = 5

            elif pimpdb[chan][u] > 0:
                pimpdb[chan][u] = int(pimpdb[chan][u]) - 1
            else:
                print(channel, "%s: You ain't got no pimp points" % (u))
                return

            try: #modifies users points
                pimpdb[chan][target] += 1
            except:
                pimpdb[chan][target] = 6

        elif com == '-1':

            if u not in pimpdb[chan]:
                pimpdb[chan][u] = 5

            elif pimpdb[chan][u] > 0:
                pimpdb[chan][u] = pimpdb[chan][u] - 1
            else:
                print(channel, "%s: You ain't got no pimp points" % (u))
                return

            try: #also modifies users pounts
                pimpdb[chan][target] = pimpdb[chan][target] - 1
            except:
                pimpdb[chan][target] = 4

        elif com == 'get':
            try:
                pimp = pimpdb[chan][target]
                if pimp > 0:
                    print(channel, "that nigga got %s pimp points up in this bitch" % (pimp))
                else:
                    print(channel, "that nigga got %s bitch points" % (pimp))
            except:
                print(channel, "that nigga ain't got no pimp points")

        else:
            print(channel, "%s: Nigga, you really think you that og, just giving out more points like that?" % (u))

    elif isop:
        var = msg.lower().split()
        com = var[1]

        try:
            chan = var[2]
            target = var[3]
        except:
            if not (com == 'load' or com == 'dump' or com == 'inflate' or com == 'addToAll'):
                return

        try:
            val = var[4]
        except:
            val = 5

        if com == 'set':
            try:
                pimpdb[chan][target] = int(val)
                print(u, "%s's score in %s is now set to %s" % (target, chan, val))
            except:
                print(u, "%s doesn't exist in %s" % (target, chan))
        elif com == 'add':
            try:
                pimpdb[chan][target] += val
                print(u, "%s's score in %s is now set to %s" % (target, chan, val))
            except:
                print("Doesn't %s exist in %s" % (target, chan))
        elif com == 'remove':
            if target in pimpdb[chan]:
                pimpdb[chan].pop(target)
                print(u, "%s is now removed from that channel's list" % (target))
            else:
                print(u, "%s is not in that channel's list")
        elif com == 'new':
            if chan not in pimpdb:
                pimpdb[chan] = {}
            if target not in pimpdb[chan]:
                pimpdb[chan][target] = int(val)
                print(u, "%s is now added to the channel with %s points" % (target, val))
            else:
                print(u, "%s is already in the channel with %s points, please remove them before adding them again" % (target, val))

        elif com == 'dump':
            print(u, str(pimpdb))
        elif com == 'load':
            pimpdb = eval(msg.lower().split('load')[1])
        elif com == 'inflate': #target == value to multiply by
            for k, v in pimpdb[chan].items():
                if v > 0:
                    pimpdb[chan][k] *= int(target)
                else:
                    pimpdb[chan][k] /= int(target)
        elif com == 'addtoall': #target == value to add to each user
            for k,v in pimpdb[chan].items():
                pimpdb[chan][k] += int(target)
        else:
            print(u, "unavailable")
