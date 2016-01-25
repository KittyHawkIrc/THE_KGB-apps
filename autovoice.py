channels = {'#fatpeoplesuck' '#fathateelite'}
ignore = {self.nickname,'}o{','FatStats','justnotfair'}

def declare():
    return {"autovoice": "userjoin"}

def callback(self):
    u = self.user.split('!')[0]
    if self.channel in channels and u not in ignore:
        self.mode(channel ,True, 'v', mask=user)
