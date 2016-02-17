ignore = {'invisiblecalories', 'justnotfair', '}o{', 'LimitServ', 'YT-info', 'VALIS', 'FatStats'}

def declare():
    return {"overkill": "userjoin"}

def callback(self):

    if self.channel == '#fatpeoplesuck':
        u = self.user.split('!',1)[0]
        if not u in ignore:
            self.msg('ChanServ', 'voice %s %s' % (self.channel, u))
