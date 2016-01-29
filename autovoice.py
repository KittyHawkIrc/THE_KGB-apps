ignore = {'invisiblecalories', 'justnotfair', '}o{', 'LimitServ', 'TY-info', 'VALIS', 'FatStats'}

def declare():
    return {"overkill": "userjoin"}

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):
    if channel == '#fatpeoplesuck':
        u = user.split('!',1)[0]
        if not u in ignore:
            self.msg('ChanServ', 'voice %s %s' % (channel, u))
